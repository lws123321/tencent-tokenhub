# Tencent TokenHub Dify Plugin

Tencent TokenHub plugin for Dify. It is compatible with the OpenAI API protocol and supports a wide range of LLMs.

## Overview

- Plugin Name: Tencent TokenHub
- Provider Type: LLM
- Runtime: Python 3.12
- Authentication: API Key (custom API Base URL is optional)

## Supported Models

| Model Name | `model` Value | Capabilities |
|------------|---------------|--------------|
| Hy3 preview | hy3-preview | Reasoning mode (`reasoning_effort`) |
| HY 2.0 Think | hunyuan-2.0-thinking-20251109 | Reasoning model |
| HY 2.0 Instruct | hunyuan-2.0-instruct-20251111 | Instruction model |
| Hunyuan-role | hunyuan-role-latest | Role-play |
| DeepSeek-V4-Pro | deepseek-v4-pro | Tool calling, vision |
| DeepSeek-V4-Flash | deepseek-v4-flash | Tool calling |
| DeepSeek-V3.2 | deepseek-v3.2 | Tool calling |
| DeepSeek-V3.1 | deepseek-v3.1-terminus | Tool calling |
| DeepSeek-R1-0528 | deepseek-r1-0528 | Reasoning model |
| DeepSeek-V3-0324 | deepseek-v3-0324 | Tool calling |
| GLM-5.1 | glm-5.1 | Tool calling |
| GLM-5V-Turbo | glm-5v-turbo | Vision, tool calling |
| GLM-5-Turbo | glm-5-turbo | Tool calling |
| GLM-5 | glm-5 | Tool calling |
| Kimi-K2.6 | kimi-k2.6 | Tool calling |
| Kimi-K2.5 | kimi-k2.5 | Tool calling |
| MiniMax-M2.7 | minimax-m2.7 | Tool calling |
| MiniMax-M2.5 | minimax-m2.5 | Tool calling |

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
