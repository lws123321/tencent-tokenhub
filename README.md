# 腾讯 TokenHub Dify 插件

腾讯 TokenHub 大模型服务平台 Dify 插件，兼容 OpenAI API 协议，支持多种大语言模型。

## 介绍

- 插件名称：Tencent TokenHub
- Provider 类型：LLM
- 运行环境：Python 3.12
- 认证方式：API Key（可选自定义 API Base URL）

## 支持的模型

| 模型名称 | model 参数值 | 特性 |
|---------|------------|------|
| Hy3 preview | hy3-preview | 支持思考模式(reasoning_effort) |
| HY 2.0 Think | hunyuan-2.0-thinking-20251109 | 思考模型 |
| HY 2.0 Instruct | hunyuan-2.0-instruct-20251111 | 指令模型 |
| Hunyuan-role | hunyuan-role-latest | 角色扮演 |
| DeepSeek-V4-Pro | deepseek-v4-pro | 工具调用、视觉 |
| DeepSeek-V4-Flash | deepseek-v4-flash | 工具调用 |
| DeepSeek-V3.2 | deepseek-v3.2 | 工具调用 |
| DeepSeek-V3.1 | deepseek-v3.1-terminus | 工具调用 |
| DeepSeek-R1-0528 | deepseek-r1-0528 | 推理模型 |
| DeepSeek-V3-0324 | deepseek-v3-0324 | 工具调用 |
| GLM-5.1 | glm-5.1 | 工具调用 |
| GLM-5V-Turbo | glm-5v-turbo | 视觉、工具调用 |
| GLM-5-Turbo | glm-5-turbo | 工具调用 |
| GLM-5 | glm-5 | 工具调用 |
| Kimi-K2.6 | kimi-k2.6 | 工具调用 |
| Kimi-K2.5 | kimi-k2.5 | 工具调用 |
| MiniMax-M2.7 | minimax-m2.7 | 工具调用 |
| MiniMax-M2.5 | minimax-m2.5 | 工具调用 |

## 安装与使用

1. 在 [腾讯TokenHub控制台](https://console.cloud.tencent.com/tokenhub) 创建 API Key。
2. 在 Dify 插件市场或本地插件安装入口安装本插件。
3. 在插件配置中填写：
   - `API Key`（必填）
   - `API Base URL`（可选，默认 `https://tokenhub.tencentmaas.com/v1`）
4. 选择任一支持模型开始调用。

## 配置项说明

- `api_key`：腾讯 TokenHub API Key，用于鉴权。
- `api_base`：OpenAI 兼容接口基础地址，默认值：
  - `https://tokenhub.tencentmaas.com/v1`

## 常见问题排查

- `401 Unauthorized`：通常是 API Key 无效、过期或复制时包含空格。
- `404 / model not found`：请确认模型 ID 与插件内置模型列表一致。
- 请求超时：检查网络连通性，或尝试切换模型后重试。
- 调用报错且使用了自定义 `api_base`：确认地址包含 `/v1` 且协议为 HTTPS。

## API 文档

- [文本生成](https://cloud.tencent.com/document/product/1823/130079)

## 隐私说明

本插件不会在插件侧持久化用户提示词、模型输出或 API Key。  
为完成模型推理，请求内容会发送至腾讯 TokenHub 服务端进行处理。详情见 `PRIVACY.md`。
