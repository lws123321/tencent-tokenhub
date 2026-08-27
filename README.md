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
| DeepSeek-V4-Flash Official (Factory Direct) | deepseek/deepseek-v4-flash | Tool calling, thinking toggle, reasoning effort (`low` / `high` / `max`) |
| DeepSeek-V4-Pro Official (Factory Direct) | deepseek/deepseek-v4-pro | Tool calling, thinking toggle, reasoning effort (`high` / `max`), vision |
| DeepSeek-V4-Flash-Vision-Exp (Factory Direct) | deepseek/deepseek-v4-flash-vision-exp | Tool calling, thinking toggle, reasoning effort (`low` / `high` / `max`), vision |
| DeepSeek-V4-Flash Official (Factory Direct, legacy ID) | deepseek-v4-flash-202605 | Compatibility alias for `deepseek/deepseek-v4-flash` |
| DeepSeek-V4-Pro Official (Factory Direct, legacy ID) | deepseek-v4-pro-202606 | Compatibility alias for `deepseek/deepseek-v4-pro` |
| DeepSeek-V4-Flash | deepseek-v4-flash | Tool calling, thinking toggle, reasoning effort (`low` / `high` / `max`) |
| DeepSeek-V4-Pro | deepseek-v4-pro | Tool calling, thinking toggle, reasoning effort (`high` / `max`) |
| GLM-5.3 | glm-5.3 | Tool calling, reasoning effort (`max` / `high` / `low`); thinking always on |
| GLM-5.3-Flash | glm-5.3-flash | Tool calling, reasoning effort (`low` / `high` / `max`); thinking always on |
| GLM-5.2 | glm-5.2 | Tool calling, thinking toggle, reasoning effort (`max` / `xhigh` / `high` / `medium` / `low` / `minimal` / `none`) |
| GLM-5.1 | glm-5.1 | Tool calling, thinking toggle |
| GLM-5V-Turbo | glm-5v-turbo | Vision, tool calling, thinking toggle |
| GLM-5-Turbo | glm-5-turbo | Tool calling, thinking toggle |
| GLM-5 | glm-5 | Tool calling, thinking toggle |
| Kimi K2.7 Code HighSpeed | kimi-k2.7-code-highspeed | Vision, tool calling; thinking always on; fixed sampling parameters |
| Kimi K3 | kimi-k3 | Vision, tool calling, reasoning effort (`max` only); thinking always on |
| Kimi K2.7 Code | kimi-k2.7-code | Vision, tool calling; thinking always on; fixed sampling parameters |
| Kimi-K2.6 | kimi-k2.6 | Vision, tool calling, thinking toggle |
| Kimi-K2.5 | kimi-k2.5 | Vision, tool calling, thinking toggle |
| MiniMax-M3 | minimax-m3 | Tool calling (thinking always on) |
| MiniMax-M2.7 | minimax-m2.7 | Tool calling (thinking always on) |
| Qwen3.5-Flash | qwen3.5-flash | Tool calling, thinking toggle |
| Qwen3.5-Plus | qwen3.5-plus | Tool calling, thinking toggle |
| MiMo-V2.5-Pro | mimo-v2.5-pro | Tool calling, thinking toggle |

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

## Privacy

This plugin does not persist user prompts, model outputs, or API keys on the plugin side.
To complete model inference, request content will be sent to Tencent TokenHub servers for processing. See `PRIVACY.md` for details.

## Source

- Source repository: https://github.com/lws123321/tencent-tokenhub
