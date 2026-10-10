# Tencent TokenHub Dify Plugin

Tencent TokenHub plugin for Dify. It supports LLM, vision, multimodal understanding, embedding, TTS, and speech-to-text APIs.

## Overview

- Plugin Name: Tencent TokenHub
- Provider Type: LLM, text embedding, TTS, and speech-to-text
- Runtime: Python 3.12
- Authentication: API Key (custom API Base URL is optional)

## Supported Models

The plugin follows the official TokenHub catalog and exposes four Dify model types:
LLM (including vision and video understanding), text embedding, TTS, and speech-to-text.
The catalog changes independently from plugin releases, so use the official pages below
for the current model IDs and availability.

- [TokenHub model list](https://cloud.tencent.com/document/product/1823/130051)
- [Language model calling overview](https://cloud.tencent.com/document/product/1823/130079)
- [DeepSeek calling guide](https://cloud.tencent.com/document/product/1823/132248)
- [Image understanding](https://cloud.tencent.com/document/product/1823/136956)
- [Video understanding](https://cloud.tencent.com/document/product/1823/136957)
- [Embedding models](https://cloud.tencent.com/document/product/1823/133515)
- [Speech model calling guide](https://cloud.tencent.com/document/product/1823/135321)

> Thinking toggle is forwarded to TokenHub as `thinking: {"type": "enabled" | "disabled"}`. `glm-5.2` supports `reasoning_effort: max | xhigh | high | medium | low | minimal | none`; `glm-5.3` supports `max | high | low`; and `glm-5.3-flash` supports `low | high | max`. The latter two models always think and do not accept `thinking: {"type": "disabled"}`. See the [TokenHub GLM docs](https://cloud.tencent.com/document/product/1823/132061) for details.

> DeepSeek reasoning effort is forwarded as a top-level `reasoning_effort` field. Flash models support `low` / `high` / `max`; Pro models support `high` / `max` (legacy `low` maps to `high`, and `xhigh` maps to `max`). DeepSeek thinking remains controlled by `thinking.type`. See the [TokenHub DeepSeek docs](https://cloud.tencent.com/document/product/1823/132248) for details.

## Installation & Usage

1. Create an API Key in the [Tencent TokenHub Console](https://console.cloud.tencent.com/tokenhub).
2. Install this plugin from the Dify plugin marketplace or via the local plugin installation entry.
3. Fill in the plugin configuration:
   - `API Key` (required)
   - `API Base URL` (optional, default: `https://tokenhub.tencentmaas.com/v1`)
4. Select any supported model to start.

## Configuration

- `api_key`: Tencent TokenHub API Key, used for authentication.
- `api_base`: OpenAI-compatible API base URL. Default:
  - `https://tokenhub.tencentmaas.com/v1`

## Troubleshooting

- `401 Unauthorized`: API Key is invalid, expired, or contains extra spaces.
- `404 / model not found`: Make sure the model ID matches the built-in model list.
- Request timeout: Check network connectivity, or retry with another model.
- Error when using a custom `api_base`: Make sure the URL includes `/v1` and uses HTTPS.

## API Documentation

- [Text Generation](https://cloud.tencent.com/document/product/1823/130079)
- [Image Understanding](https://cloud.tencent.com/document/product/1823/136956)
- [Video Understanding](https://cloud.tencent.com/document/product/1823/136957)
- [Embedding Models](https://cloud.tencent.com/document/product/1823/133515)
- [Speech Models](https://cloud.tencent.com/document/product/1823/135321)

## Privacy

This plugin does not persist user prompts, model outputs, or API keys on the plugin side.
To complete model inference, request content will be sent to Tencent TokenHub servers for processing. See `PRIVACY.md` for details.

## Source

- Source repository: https://github.com/lws123321/tencent-tokenhub
