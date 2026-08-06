import json
import logging
from collections.abc import Generator
from typing import cast, Optional

from openai import OpenAI, Stream
from openai.types.chat import ChatCompletion, ChatCompletionChunk

from dify_plugin.entities import I18nObject
from dify_plugin.entities.model import (
    AIModelEntity,
    FetchFrom,
    ModelFeature,
    ModelPropertyKey,
    ModelType,
    ParameterRule,
    ParameterType,
)
from dify_plugin.entities.model.llm import LLMResult, LLMResultChunk, LLMResultChunkDelta
from dify_plugin.entities.model.message import (
    AssistantPromptMessage,
    ImagePromptMessageContent,
    PromptMessage,
    PromptMessageContentType,
    PromptMessageTool,
    SystemPromptMessage,
    TextPromptMessageContent,
    ToolPromptMessage,
    UserPromptMessage,
)
from dify_plugin.errors.model import (
    CredentialsValidateFailedError,
    InvokeAuthorizationError,
    InvokeBadRequestError,
    InvokeConnectionError,
    InvokeError,
    InvokeRateLimitError,
    InvokeServerUnavailableError,
)
from dify_plugin.interfaces.model.large_language_model import LargeLanguageModel

logger = logging.getLogger(__name__)

TOKENHUB_DEFAULT_BASE_URL = "https://tokenhub.tencentmaas.com/v1"

REASONING_EFFORT_MODELS = {
    "hy3",
    "deepseek-v4-flash",
    "deepseek-v4-pro",
    "deepseek-v4-pro-202606",
    "deepseek-v4-flash-202605",
}

THINKING_TOGGLE_MODELS = {
    "hy3",
    "deepseek-v4-pro",
    "deepseek-v4-flash",
    "deepseek-v4-pro-202606",
    "deepseek-v4-flash-202605",
    "glm-5.2",
    "glm-5.1",
    "glm-5v-turbo",
    "glm-5-turbo",
    "glm-5",
    "kimi-k2.7-code-highspeed",
    "kimi-k3",
    "kimi-k2.7-code",
    "kimi-k2.6",
    "kimi-k2.5",
    "qwen3.5-flash",
    "qwen3.5-plus",
    "mimo-v2.5-pro",
}


class TokenHubLargeLanguageModel(LargeLanguageModel):
    """
    腾讯TokenHub大语言模型实现，使用 OpenAI Python SDK 调用兼容接口。
    """

    def _invoke(
        self,
        model: str,
        credentials: dict,
        prompt_messages: list[PromptMessage],
        model_parameters: dict,
        tools: list[PromptMessageTool] | None = None,
        stop: list[str] | None = None,
        stream: bool = True,
        user: str | None = None,
    ) -> LLMResult | Generator:
        client = self._get_client(credentials)
        messages = self._convert_prompt_messages(prompt_messages)
        extra_kwargs = self._build_extra_kwargs(model, credentials, model_parameters, tools, stop)

        if stream:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,
                stream_options={"include_usage": True},
                user=user or "",
                **extra_kwargs,
            )
            return self._handle_stream_response(model, credentials, prompt_messages, response)

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=False,
            user=user or "",
            **extra_kwargs,
        )
        return self._handle_response(model, credentials, prompt_messages, response)

    def validate_credentials(self, model: str, credentials: dict) -> None:
        import openai

        try:
            client = self._get_client(credentials)
            client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "hi"}],
                max_tokens=10,
                stream=False,
            )
        except openai.AuthenticationError as e:
            raise CredentialsValidateFailedError(f"Invalid API Key: {e}")
        except openai.APIStatusError as e:
            # 402 (quota exhausted) / 429 (rate limit) 说明 API Key 本身有效
            if e.status_code in (402, 429):
                return
            raise CredentialsValidateFailedError(f"Credentials validation failed: {e}")
        except Exception as e:
            raise CredentialsValidateFailedError(f"Credentials validation failed: {e}")

    def get_customizable_model_schema(self, model: str, credentials: dict) -> AIModelEntity:
        """
        为界面自定义添加的模型动态生成 schema（相当于动态生成一份模型 yaml）。

        用户在 Dify 界面添加模型时填写的字段会以凭据形式传入：
        - ``context_size`` / ``max_tokens_limit``：上下文长度与最大输出上限。
        - ``support_thinking`` / ``support_reasoning_effort``：是否暴露思考模式、推理深度参数。
        - ``support_vision`` / ``support_tool_call``：是否声明视觉、工具调用能力。

        这样新增模型无需再手动添加 yaml 或改代码。
        """
        context_size = self._safe_int(credentials.get("context_size"), 131072)
        max_tokens_limit = self._safe_int(credentials.get("max_tokens_limit"), 8192)

        parameter_rules = [
            ParameterRule(
                name="temperature",
                use_template="temperature",
                label=I18nObject(zh_Hans="温度", en_US="Temperature"),
                type=ParameterType.FLOAT,
                default=0.7,
                min=0.0,
                max=2.0,
            ),
            ParameterRule(
                name="top_p",
                use_template="top_p",
                label=I18nObject(zh_Hans="Top P", en_US="Top P"),
                type=ParameterType.FLOAT,
                default=1.0,
                min=0.0,
                max=1.0,
            ),
            ParameterRule(
                name="max_tokens",
                use_template="max_tokens",
                label=I18nObject(zh_Hans="最大输出长度", en_US="Max Tokens"),
                type=ParameterType.INT,
                default=min(8192, max_tokens_limit),
                min=1,
                max=max_tokens_limit,
            ),
        ]

        if self._supports_thinking(model, credentials):
            parameter_rules.append(
                ParameterRule(
                    name="thinking",
                    label=I18nObject(zh_Hans="思考模式", en_US="Thinking mode"),
                    type=ParameterType.BOOLEAN,
                    default=True,
                    help=I18nObject(
                        zh_Hans="是否开启思考模式。开启后模型会先进行推理再给出最终答案。",
                        en_US="Whether to enable thinking mode. When enabled, the model reasons before answering.",
                    ),
                )
            )

        if self._supports_reasoning_effort(model, credentials):
            parameter_rules.append(
                ParameterRule(
                    name="reasoning_effort",
                    label=I18nObject(zh_Hans="推理深度", en_US="Reasoning Effort"),
                    type=ParameterType.STRING,
                    default="high",
                    options=["low", "medium", "high"],
                    help=I18nObject(
                        zh_Hans="推理深度控制，仅在开启思考模式时生效。",
                        en_US="Control reasoning depth. Only takes effect when thinking mode is enabled.",
                    ),
                )
            )

        features = [ModelFeature.AGENT_THOUGHT]
        if self._credential_truthy(credentials, "support_tool_call"):
            features += [
                ModelFeature.TOOL_CALL,
                ModelFeature.MULTI_TOOL_CALL,
                ModelFeature.STREAM_TOOL_CALL,
            ]
        if self._credential_truthy(credentials, "support_vision"):
            features.append(ModelFeature.VISION)

        return AIModelEntity(
            model=model,
            label=I18nObject(zh_Hans=model, en_US=model),
            model_type=ModelType.LLM,
            fetch_from=FetchFrom.CUSTOMIZABLE_MODEL,
            features=features,
            model_properties={
                ModelPropertyKey.MODE: "chat",
                ModelPropertyKey.CONTEXT_SIZE: context_size,
            },
            parameter_rules=parameter_rules,
        )

    @staticmethod
    def _safe_int(value, default: int) -> int:
        """将凭据中的字符串数字安全转换为 int，转换失败时回退到默认值。"""
        try:
            return int(str(value).strip())
        except (TypeError, ValueError):
            return default

    def _get_client(self, credentials: dict) -> OpenAI:
        api_key = credentials.get("api_key", "")
        base_url = credentials.get("api_base", "").strip() or TOKENHUB_DEFAULT_BASE_URL
        return OpenAI(api_key=api_key, base_url=base_url, timeout=120)

    @staticmethod
    def _credential_truthy(credentials: dict, key: str) -> bool:
        """判断凭据中某个开关字段是否为真（兼容字符串/布尔/数字写法）。"""
        return str(credentials.get(key, "")).strip().lower() in {"true", "1", "yes", "on"}

    def _supports_thinking(self, model: str, credentials: dict) -> bool:
        """
        判断模型是否支持思考模式开关。

        预定义模型走内置名单；自定义模型（界面添加）则读取凭据里的
        ``support_thinking`` 开关，从而无需改代码即可支持新模型。
        """
        return model in THINKING_TOGGLE_MODELS or self._credential_truthy(credentials, "support_thinking")

    def _supports_reasoning_effort(self, model: str, credentials: dict) -> bool:
        """判断模型是否支持推理深度参数（逻辑同 ``_supports_thinking``）。"""
        return model in REASONING_EFFORT_MODELS or self._credential_truthy(credentials, "support_reasoning_effort")

    def _build_extra_kwargs(
        self,
        model: str,
        credentials: dict,
        model_parameters: dict,
        tools: list[PromptMessageTool] | None = None,
        stop: list[str] | None = None,
    ) -> dict:
        """
        根据模型参数和工具列表构建额外请求参数。

        - 思考模式：通过 ``thinking`` 参数控制，传递格式为
          ``{"thinking": {"type": "enabled" | "disabled"}}``。
        - 推理深度：通过 ``reasoning_effort`` 参数控制，可选值为
          ``low`` / ``medium`` / ``high``。

        参考腾讯云 TokenHub 文档：
        https://cloud.tencent.com/document/product/1823/131208
        """
        kwargs: dict = {}

        if "temperature" in model_parameters:
            kwargs["temperature"] = model_parameters["temperature"]
        if "top_p" in model_parameters:
            kwargs["top_p"] = model_parameters["top_p"]
        if "max_tokens" in model_parameters:
            kwargs["max_tokens"] = model_parameters["max_tokens"]

        extra_body: dict = {}

        if self._supports_thinking(model, credentials) and "thinking" in model_parameters:
            thinking_enabled = bool(model_parameters.get("thinking"))
            extra_body["thinking"] = {
                "type": "enabled" if thinking_enabled else "disabled"
            }

        if self._supports_reasoning_effort(model, credentials):
            reasoning_effort = model_parameters.get("reasoning_effort")
            if reasoning_effort and reasoning_effort in {"low", "medium", "high"}:
                extra_body["reasoning_effort"] = reasoning_effort

        if extra_body:
            kwargs["extra_body"] = extra_body

        if stop:
            kwargs["stop"] = stop

        if tools:
            kwargs["tools"] = [
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.parameters,
                    },
                }
                for tool in tools
            ]
            kwargs["tool_choice"] = "auto"

        return kwargs

    def _convert_prompt_messages(self, prompt_messages: list[PromptMessage]) -> list[dict]:
        """将 Dify PromptMessage 列表转换为 OpenAI 消息格式"""
        messages = []
        for message in prompt_messages:
            if isinstance(message, SystemPromptMessage):
                messages.append({"role": "system", "content": message.content})

            elif isinstance(message, UserPromptMessage):
                if isinstance(message.content, str):
                    messages.append({"role": "user", "content": message.content})
                else:
                    content_parts = []
                    for part in message.content:
                        if part.type == PromptMessageContentType.TEXT:
                            part = cast(TextPromptMessageContent, part)
                            content_parts.append({"type": "text", "text": part.data})
                        elif part.type == PromptMessageContentType.IMAGE:
                            part = cast(ImagePromptMessageContent, part)
                            content_parts.append({
                                "type": "image_url",
                                "image_url": {"url": part.data},
                            })
                    messages.append({"role": "user", "content": content_parts})

            elif isinstance(message, AssistantPromptMessage):
                msg_dict: dict = {"role": "assistant"}
                if message.tool_calls and len(message.tool_calls) > 0:
                    msg_dict["content"] = message.content or ""
                    msg_dict["tool_calls"] = [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments or "{}",
                            },
                        }
                        for tc in message.tool_calls
                    ]
                else:
                    msg_dict["content"] = message.content
                messages.append(msg_dict)

            elif isinstance(message, ToolPromptMessage):
                messages.append({
                    "role": "tool",
                    "tool_call_id": message.tool_call_id,
                    "content": message.content,
                })
            else:
                messages.append({"role": message.role.value, "content": message.content})

        return messages

    def _handle_response(
        self,
        model: str,
        credentials: dict,
        prompt_messages: list[PromptMessage],
        response: ChatCompletion,
    ) -> LLMResult:
        choice = response.choices[0]
        message = choice.message

        content = message.content or ""

        tool_calls = []
        if message.tool_calls:
            tool_calls = self._extract_tool_calls(message.tool_calls)

        assistant_message = AssistantPromptMessage(content=content, tool_calls=tool_calls)

        usage = self._calc_response_usage(
            model,
            credentials,
            response.usage.prompt_tokens if response.usage else 0,
            response.usage.completion_tokens if response.usage else 0,
        )

        return LLMResult(
            model=model,
            prompt_messages=prompt_messages,
            message=assistant_message,
            usage=usage,
        )

    def _handle_stream_response(
        self,
        model: str,
        credentials: dict,
        prompt_messages: list[PromptMessage],
        response: Stream[ChatCompletionChunk],
    ) -> Generator:
        """
        处理流式响应。
        注意：开启 stream_options.include_usage 后，API 会在所有内容 chunk 之后
        额外发送一个 choices 为空、仅携带 usage 的 chunk，因此需要缓存 finish chunk，
        等拿到 usage 后再合并 yield，避免 token 用量丢失。
        """
        is_reasoning = False
        tool_call_buf: Optional[dict] = None
        collected_tool_calls = []
        index = 0
        pending_finish_result: Optional[LLMResultChunk] = None
        final_prompt_tokens = 0
        final_completion_tokens = 0

        for chunk in response:
            if chunk.usage:
                final_prompt_tokens = chunk.usage.prompt_tokens or 0
                final_completion_tokens = chunk.usage.completion_tokens or 0

            if not chunk.choices:
                continue

            choice = chunk.choices[0]
            delta = choice.delta

            content = ""
            if delta.content is not None:
                content = delta.content

            raw_delta = {}
            if hasattr(delta, "content"):
                raw_delta["content"] = delta.content
            reasoning_content = getattr(delta, "reasoning_content", None)
            if reasoning_content is not None:
                raw_delta["reasoning_content"] = reasoning_content
            content, is_reasoning = self._wrap_thinking_by_reasoning_content(raw_delta, is_reasoning)

            if delta.tool_calls:
                for tc_delta in delta.tool_calls:
                    if tc_delta.id:
                        if tool_call_buf is not None:
                            collected_tool_calls.append(tool_call_buf)
                        tool_call_buf = {
                            "id": tc_delta.id,
                            "name": tc_delta.function.name if tc_delta.function else "",
                            "arguments": tc_delta.function.arguments if tc_delta.function else "",
                        }
                    elif tool_call_buf is not None:
                        if tc_delta.function:
                            tool_call_buf["name"] += tc_delta.function.name or ""
                            tool_call_buf["arguments"] += tc_delta.function.arguments or ""

            finish_reason = choice.finish_reason or ""

            assistant_message = AssistantPromptMessage(content=content, tool_calls=[])

            if finish_reason == "tool_calls" or finish_reason == "stop":
                if tool_call_buf is not None:
                    collected_tool_calls.append(tool_call_buf)
                    tool_call_buf = None

                if collected_tool_calls:
                    assistant_message.content = ""
                    assistant_message.tool_calls = self._build_tool_calls_from_buf(collected_tool_calls)
                    collected_tool_calls = []

            if finish_reason:
                usage = self._calc_response_usage(
                    model, credentials, final_prompt_tokens, final_completion_tokens
                )
                pending_finish_result = LLMResultChunk(
                    model=model,
                    prompt_messages=prompt_messages,
                    delta=LLMResultChunkDelta(
                        index=index,
                        role="assistant",
                        message=assistant_message,
                        usage=usage,
                        finish_reason=finish_reason,
                    ),
                )
            else:
                yield LLMResultChunk(
                    model=model,
                    prompt_messages=prompt_messages,
                    delta=LLMResultChunkDelta(
                        index=index,
                        message=assistant_message,
                    ),
                )

            index += 1

        if pending_finish_result is not None:
            pending_finish_result.delta.usage = self._calc_response_usage(
                model, credentials, final_prompt_tokens, final_completion_tokens
            )
            yield pending_finish_result

    def _extract_tool_calls(self, tool_calls) -> list:
        """从 OpenAI SDK 响应中提取工具调用"""
        from dify_plugin.entities.model.message import AssistantPromptMessage as APM

        result = []
        for tc in tool_calls:
            result.append(
                APM.ToolCall(
                    id=tc.id,
                    type=tc.type,
                    function=APM.ToolCall.ToolCallFunction(
                        name=tc.function.name,
                        arguments=tc.function.arguments,
                    ),
                )
            )
        return result

    def _build_tool_calls_from_buf(self, buf_list: list[dict]) -> list:
        """从缓冲区构建工具调用对象"""
        from dify_plugin.entities.model.message import AssistantPromptMessage as APM

        result = []
        for buf in buf_list:
            result.append(
                APM.ToolCall(
                    id=buf["id"],
                    type="function",
                    function=APM.ToolCall.ToolCallFunction(
                        name=buf["name"],
                        arguments=buf["arguments"],
                    ),
                )
            )
        return result

    def _wrap_thinking_by_reasoning_content(self, delta: dict, is_reasoning: bool) -> tuple[str, bool]:
        """
        处理模型返回的 reasoning_content，用 <think> 标签包裹思考内容，
        使其能在 Dify 的 agent-thought 功能中正确展示。
        """
        content = delta.get("content") or ""
        reasoning_content = delta.get("reasoning_content")

        if reasoning_content:
            if not is_reasoning:
                content = "<think>\n" + reasoning_content
                is_reasoning = True
            else:
                content = reasoning_content
        elif is_reasoning and content:
            content = "\n</think>" + content
            is_reasoning = False

        return content, is_reasoning

    def get_num_tokens(
        self,
        model: str,
        credentials: dict,
        prompt_messages: list[PromptMessage],
        tools: list[PromptMessageTool] | None = None,
    ) -> int:
        if not prompt_messages:
            return 0
        prompt = self._convert_messages_to_prompt(prompt_messages)
        return self._get_num_tokens_by_gpt2(prompt)

    def _convert_messages_to_prompt(self, messages: list[PromptMessage]) -> str:
        parts = []
        for msg in messages:
            if isinstance(msg, UserPromptMessage):
                parts.append(f"\n\nHuman: {msg.content}")
            elif isinstance(msg, AssistantPromptMessage):
                parts.append(f"\n\nAssistant: {msg.content}")
            elif isinstance(msg, ToolPromptMessage):
                parts.append(f"\n\nTool: {msg.content}")
            elif isinstance(msg, SystemPromptMessage):
                parts.append(str(msg.content))
            else:
                parts.append(str(msg.content))
        return "".join(parts).rstrip()

    @property
    def _invoke_error_mapping(self) -> dict[type[InvokeError], list[type[Exception]]]:
        import openai

        return {
            InvokeAuthorizationError: [openai.AuthenticationError, openai.PermissionDeniedError],
            InvokeBadRequestError: [openai.BadRequestError],
            InvokeRateLimitError: [openai.RateLimitError],
            InvokeServerUnavailableError: [openai.APIStatusError],
            InvokeConnectionError: [openai.APIConnectionError, openai.APITimeoutError],
        }
