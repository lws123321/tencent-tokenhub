# Tencent TokenHub Dify Plugin

Tencent TokenHub plugin for Dify. It is compatible with the OpenAI API protocol and supports a wide range of LLMs.

## Overview

- Plugin Name: Tencent TokenHub
- Provider Type: LLM
- Runtime: Python 3.12
- Authentication: API Key (custom API Base URL is optional)

## Supported Models

Aligned with the official [TokenHub model list](https://cloud.tencent.com/document/product/1823/130051) (language models; offline models excluded).

| Model Name | `model` Value | Capabilities |
|------------|---------------|--------------|
| Hy3 | hy3 | Tool calling, thinking toggle, reasoning effort |
| Hy-MT2-Pro | hy-mt2-pro | Translation |
| Hy-MT2-Plus | hy-mt2-plus | Translation |
| Hy-MT2-Lite | hy-mt2-lite | Translation |
| Hy-Role-Latest | hunyuan-role-latest | Role-play |
| Hy-Role | hy-role | Role-play |
| DeepSeek-V4-Flash Official (Factory Direct) | deepseek-v4-flash-202605 | Tool calling, thinking toggle, reasoning effort |
| DeepSeek-V4-Pro (Factory Direct) | deepseek-v4-pro-202606 | Tool calling, thinking toggle, reasoning effort |
| DeepSeek-V4-Flash | deepseek-v4-flash | Tool calling, thinking toggle, reasoning effort |
| DeepSeek-V4-Pro | deepseek-v4-pro | Tool calling, thinking toggle, reasoning effort |
| GLM-5.2 | glm-5.2 | Tool calling, thinking toggle |
| GLM-5.1 | glm-5.1 | Tool calling, thinking toggle |
| GLM-5V-Turbo | glm-5v-turbo | Vision, tool calling, thinking toggle |
| GLM-5-Turbo | glm-5-turbo | Tool calling, thinking toggle |
| GLM-5 | glm-5 | Tool calling, thinking toggle |
| Kimi K2.7 Code HighSpeed | kimi-k2.7-code-highspeed | Tool calling, thinking toggle |
| Kimi K3 | kimi-k3 | Tool calling, thinking toggle |
| Kimi K2.7 Code | kimi-k2.7-code | Tool calling, thinking toggle |
| Kimi-K2.6 | kimi-k2.6 | Tool calling, thinking toggle |
| Kimi-K2.5 | kimi-k2.5 | Tool calling, thinking toggle |
| MiniMax-M3 | minimax-m3 | Tool calling (thinking always on) |
| MiniMax-M2.7 | minimax-m2.7 | Tool calling (thinking always on) |
| Qwen3.5-Flash | qwen3.5-flash | Tool calling, thinking toggle |
| Qwen3.5-Plus | qwen3.5-plus | Tool calling, thinking toggle |
| MiMo-V2.5-Pro | mimo-v2.5-pro | Tool calling, thinking toggle |

> Thinking toggle is forwarded to TokenHub as `thinking: {"type": "enabled" | "disabled"}`. Reasoning effort is forwarded as `reasoning_effort: low | medium | high` and only takes effect when thinking is enabled. See the [TokenHub thinking docs](https://cloud.tencent.com/document/product/1823/131208) for details.

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

## Privacy

This plugin does not persist user prompts, model outputs, or API keys on the plugin side.
To complete model inference, request content will be sent to Tencent TokenHub servers for processing. See `PRIVACY.md` for details.
