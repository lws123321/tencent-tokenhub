import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import dify_plugin
import yaml
from dify_plugin.entities.model import AIModelEntity
from dify_plugin.entities.model.message import UserPromptMessage
from openai.types.chat import ChatCompletionChunk

from models.llm.llm import TokenHubLargeLanguageModel


ROOT = Path(__file__).resolve().parents[1]


class ModelConfigurationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schemas = [
            AIModelEntity(**yaml.safe_load(path.read_text(encoding="utf-8")))
            for path in (ROOT / "models/llm").glob("*.yaml")
            if path.name != "_position.yaml"
        ]
        cls.adapter = TokenHubLargeLanguageModel(cls.schemas)

    def test_all_llm_limits_defaults_and_prices(self):
        for schema in self.schemas:
            with self.subTest(model=schema.model):
                rules = {rule.name: rule for rule in schema.parameter_rules}
                limit_name = "max_completion_tokens" if schema.model == "kimi-k3" else "max_tokens"
                self.assertIn(limit_name, rules)
                self.assertGreater(rules[limit_name].max, 0)
                self.assertIsNotNone(schema.pricing)
                for rule in rules.values():
                    if rule.min is not None:
                        self.assertGreaterEqual(rule.default, rule.min)
                    if rule.max is not None:
                        self.assertLessEqual(rule.default, rule.max)
                    if rule.options:
                        self.assertIn(rule.default, rule.options)

    def test_all_declared_parameters_are_forwarded(self):
        for schema in self.schemas:
            with self.subTest(model=schema.model):
                defaults = {rule.name: rule.default for rule in schema.parameter_rules}
                result = self.adapter._build_extra_kwargs(schema.model, {}, defaults)
                forwarded = {**result, **result.get("extra_body", {})}
                for name in defaults:
                    if schema.model in {"mimo-v2.5-pro", "mimo-v2.6-pro", "mimo-v2.6-flash"} and name in {"temperature", "top_p"}:
                        self.assertNotIn(name, forwarded)
                    elif name == "json_mode":
                        self.assertNotIn("response_format", forwarded)
                    else:
                        self.assertIn(name, forwarded)
                if "thinking" in defaults:
                    disabled = self.adapter._build_extra_kwargs(schema.model, {}, {"thinking": False})
                    self.assertEqual(disabled["extra_body"]["thinking"], {"type": "disabled"})

    def test_kimi_preview_uses_its_own_token_parameter(self):
        result = self.adapter._build_extra_kwargs(
            "kimi-k2.8-preview", {},
            {"max_tokens": 32768, "reasoning_effort": "low", "thinking": False,
             "temperature": 0.7, "top_p": 0.8},
        )
        self.assertEqual(result, {"max_tokens": 32768, "reasoning_effort": "low"})

    def test_mimo_non_thinking_sampling_and_json_mode(self):
        result = self.adapter._build_extra_kwargs(
            "mimo-v2.6-flash", {},
            {"thinking": False, "temperature": 0.4, "top_p": 0.9, "json_mode": True},
        )
        self.assertEqual(result["temperature"], 0.4)
        self.assertEqual(result["top_p"], 0.9)
        self.assertEqual(result["response_format"], {"type": "json_object"})

    def test_flashx_cannot_disable_thinking(self):
        result = self.adapter._build_extra_kwargs(
            "glm-5.3-flashx", {"support_thinking": "true"},
            {"thinking": False, "reasoning_effort": "max"},
        )
        self.assertEqual(result, {"extra_body": {"reasoning_effort": "max"}})

    def test_non_stream_reasoning_content_is_preserved(self):
        class Message:
            content = "最终答案"
            reasoning_content = "推理过程"
            tool_calls = None

        class Choice:
            message = Message()

        class Response:
            choices = [Choice()]
            usage = None

        result = self.adapter._handle_response("deepseek-v4-pro-202606", {}, [], Response())
        self.assertEqual(result.message.content, "<think>\n推理过程\n</think>最终答案")

    def test_stream_completion_and_usage_serialization(self):
        for schema in self.schemas:
            for separate_usage in (True, False):
                with self.subTest(model=schema.model, separate_usage=separate_usage):
                    chunk_fields = {
                        "id": "test-completion",
                        "created": 0,
                        "model": schema.model,
                        "object": "chat.completion.chunk",
                    }
                    usage = {"prompt_tokens": 12, "completion_tokens": 3, "total_tokens": 15}
                    chunks = [
                        ChatCompletionChunk(
                            **chunk_fields,
                            choices=[{"index": 0, "delta": {"content": "answer"}, "finish_reason": None}],
                        ),
                        ChatCompletionChunk(
                            **chunk_fields,
                            choices=[{"index": 0, "delta": {}, "finish_reason": "stop"}],
                            usage=None if separate_usage else usage,
                        ),
                    ]
                    if separate_usage:
                        chunks.append(ChatCompletionChunk(**chunk_fields, choices=[], usage=usage))
                    client = MagicMock()
                    client.chat.completions.create.return_value = iter(chunks)
                    adapter = TokenHubLargeLanguageModel(self.schemas)
                    with patch.object(adapter, "_get_client", return_value=client):
                        results = list(adapter.invoke(
                            model=schema.model,
                            credentials={"api_key": "test-key"},
                            prompt_messages=[UserPromptMessage(content="hello")],
                            model_parameters={},
                            stream=True,
                        ))
                    self.assertEqual("".join(result.delta.message.content or "" for result in results), "answer")
                    self.assertEqual(results[-1].delta.finish_reason, "stop")
                    self.assertEqual(results[-1].delta.usage.total_tokens, 15)
                    self.assertGreaterEqual(results[-1].delta.usage.latency, 0)
                    self.assertLess(results[-1].delta.usage.latency, 60)
                    self.assertEqual(client.chat.completions.create.call_args.kwargs["model"], schema.model)
                    for result in results:
                        self.assertTrue(result.model_dump_json())

    def test_stream_without_finish_reason_gets_synthetic_stop_chunk(self):
        schema = self.schemas[0]
        chunk_fields = {
            "id": "test-completion",
            "created": 0,
            "model": schema.model,
            "object": "chat.completion.chunk",
        }
        chunks = [
            ChatCompletionChunk(
                **chunk_fields,
                choices=[{"index": 0, "delta": {"content": "answer"}, "finish_reason": None}],
            ),
            ChatCompletionChunk(**chunk_fields, choices=[], usage={
                "prompt_tokens": 12,
                "completion_tokens": 3,
                "total_tokens": 15,
            }),
        ]
        client = MagicMock()
        client.chat.completions.create.return_value = iter(chunks)
        with patch.object(self.adapter, "_get_client", return_value=client):
            results = list(self.adapter.invoke(
                model=schema.model,
                credentials={"api_key": "test-key"},
                prompt_messages=[UserPromptMessage(content="hello")],
                model_parameters={},
                stream=True,
            ))
        self.assertEqual(results[-1].delta.finish_reason, "stop")
        self.assertEqual(results[-1].delta.usage.total_tokens, 15)


if __name__ == "__main__":
    unittest.main()