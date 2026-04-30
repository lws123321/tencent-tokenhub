# Tencent TokenHub Dify Plugin / 腾讯 TokenHub Dify 插件

Tencent TokenHub plugin for Dify. It is compatible with the OpenAI API protocol and supports multiple LLMs.  
腾讯 TokenHub 大模型服务平台 Dify 插件，兼容 OpenAI API 协议，支持多种大语言模型。

## Overview / 介绍

- Plugin Name / 插件名称: Tencent TokenHub
- Provider Type / Provider 类型: LLM
- Runtime / 运行环境: Python 3.12
- Authentication / 认证方式: API Key (custom API Base URL optional) / API Key（可选自定义 API Base URL）

## Supported Models / 支持的模型

| Model Name | `model` Value | Capabilities / 特性 |
|------------|---------------|---------------------|
| Hy3 preview | hy3-preview | Reasoning mode (`reasoning_effort`) / 支持思考模式 (`reasoning_effort`) |
| HY 2.0 Think | hunyuan-2.0-thinking-20251109 | Reasoning model / 思考模型 |
| HY 2.0 Instruct | hunyuan-2.0-instruct-20251111 | Instruction model / 指令模型 |
| Hunyuan-role | hunyuan-role-latest | Role-play / 角色扮演 |
| DeepSeek-V4-Pro | deepseek-v4-pro | Tool calling, vision / 工具调用、视觉 |
| DeepSeek-V4-Flash | deepseek-v4-flash | Tool calling / 工具调用 |
| DeepSeek-V3.2 | deepseek-v3.2 | Tool calling / 工具调用 |
| DeepSeek-V3.1 | deepseek-v3.1-terminus | Tool calling / 工具调用 |
| DeepSeek-R1-0528 | deepseek-r1-0528 | Reasoning model / 推理模型 |
| DeepSeek-V3-0324 | deepseek-v3-0324 | Tool calling / 工具调用 |
| GLM-5.1 | glm-5.1 | Tool calling / 工具调用 |
| GLM-5V-Turbo | glm-5v-turbo | Vision, tool calling / 视觉、工具调用 |
| GLM-5-Turbo | glm-5-turbo | Tool calling / 工具调用 |
| GLM-5 | glm-5 | Tool calling / 工具调用 |
| Kimi-K2.6 | kimi-k2.6 | Tool calling / 工具调用 |
| Kimi-K2.5 | kimi-k2.5 | Tool calling / 工具调用 |
| MiniMax-M2.7 | minimax-m2.7 | Tool calling / 工具调用 |
| MiniMax-M2.5 | minimax-m2.5 | Tool calling / 工具调用 |

## Installation & Usage / 安装与使用

1. Create an API Key in [Tencent TokenHub Console](https://console.cloud.tencent.com/tokenhub).  
   在 [腾讯 TokenHub 控制台](https://console.cloud.tencent.com/tokenhub) 创建 API Key。
2. Install this plugin from the Dify plugin marketplace or local plugin installation entry.  
   在 Dify 插件市场或本地插件安装入口安装本插件。
3. Fill in plugin configuration:  
   在插件配置中填写：
   - `API Key` (required) / `API Key`（必填）
   - `API Base URL` (optional, default: `https://tokenhub.tencentmaas.com/v1`) / `API Base URL`（可选，默认：`https://tokenhub.tencentmaas.com/v1`）
4. Select any supported model to start.  
   选择任一支持模型开始调用。

## Configuration / 配置项说明

- `api_key`: Tencent TokenHub API Key for authentication. / 腾讯 TokenHub API Key，用于鉴权。
- `api_base`: OpenAI-compatible API base URL (default below). / OpenAI 兼容接口基础地址（默认如下）。
  - `https://tokenhub.tencentmaas.com/v1`

## Troubleshooting / 常见问题排查

- `401 Unauthorized`: API Key is invalid/expired or contains extra spaces. / 通常是 API Key 无效、过期或复制时包含空格。
- `404 / model not found`: Ensure the model ID matches the built-in model list. / 请确认模型 ID 与插件内置模型列表一致。
- Request timeout: Check network connectivity or retry with another model. / 检查网络连通性，或尝试切换模型后重试。
- Error with custom `api_base`: Ensure URL includes `/v1` and uses HTTPS. / 确认地址包含 `/v1` 且协议为 HTTPS。

## API Documentation / API 文档

- [Text Generation / 文本生成](https://cloud.tencent.com/document/product/1823/130079)

## Privacy / 隐私说明

This plugin does not persist user prompts, model outputs, or API keys on the plugin side.  
本插件不会在插件侧持久化用户提示词、模型输出或 API Key。  
To complete model inference, request content will be sent to Tencent TokenHub servers. See `PRIVACY.md` for details.  
为完成模型推理，请求内容会发送至腾讯 TokenHub 服务端进行处理。详情见 `PRIVACY.md`。
