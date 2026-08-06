# 腾讯 TokenHub Dify 插件

腾讯 TokenHub 插件适用于 Dify，兼容 OpenAI API 协议，支持多种大语言模型。

## 介绍

- 插件名称：Tencent TokenHub
- Provider 类型：LLM
- 运行环境：Python 3.12
- 认证方式：API Key（可选自定义 API Base URL）

## 支持模型

与官方 [TokenHub 模型列表](https://cloud.tencent.com/document/product/1823/130051) 中的语言模型对齐（已排除标记下线的模型）。

| 模型名称 | `model` 参数值 | 能力 |
|---------|---------------|------|
| Hy3 | hy3 | 工具调用、思考开关、推理深度 |
| Hy-MT2-Pro | hy-mt2-pro | 翻译 |
| Hy-MT2-Plus | hy-mt2-plus | 翻译 |
| Hy-MT2-Lite | hy-mt2-lite | 翻译 |
| Hy-Role-Latest | hunyuan-role-latest | 角色扮演 |
| Hy-Role | hy-role | 角色扮演 |
| DeepSeek-V4-Flash 正式版 原厂直供 | deepseek-v4-flash-202605 | 工具调用、思考开关、推理深度 |
| DeepSeek-V4-Pro 原厂直供 | deepseek-v4-pro-202606 | 工具调用、思考开关、推理深度 |
| DeepSeek-V4-Flash | deepseek-v4-flash | 工具调用、思考开关、推理深度 |
| DeepSeek-V4-Pro | deepseek-v4-pro | 工具调用、思考开关、推理深度 |
| GLM-5.2 | glm-5.2 | 工具调用、思考开关 |
| GLM-5.1 | glm-5.1 | 工具调用、思考开关 |
| GLM-5V-Turbo | glm-5v-turbo | 视觉、工具调用、思考开关 |
| GLM-5-Turbo | glm-5-turbo | 工具调用、思考开关 |
| GLM-5 | glm-5 | 工具调用、思考开关 |
| Kimi K2.7 Code HighSpeed | kimi-k2.7-code-highspeed | 工具调用、思考开关 |
| Kimi K3 | kimi-k3 | 工具调用、思考开关 |
| Kimi K2.7 Code | kimi-k2.7-code | 工具调用、思考开关 |
| Kimi-K2.6 | kimi-k2.6 | 工具调用、思考开关 |
| Kimi-K2.5 | kimi-k2.5 | 工具调用、思考开关 |
| MiniMax-M3 | minimax-m3 | 工具调用（思考常开） |
| MiniMax-M2.7 | minimax-m2.7 | 工具调用（思考常开） |
| Qwen3.5-Flash | qwen3.5-flash | 工具调用、思考开关 |
| Qwen3.5-Plus | qwen3.5-plus | 工具调用、思考开关 |
| MiMo-V2.5-Pro | mimo-v2.5-pro | 工具调用、思考开关 |

> 思考开关会透传为 `thinking: {"type": "enabled" | "disabled"}`。推理深度会透传为 `reasoning_effort: low | medium | high`，且仅在开启思考模式时生效。详情参见 [TokenHub 深度思考文档](https://cloud.tencent.com/document/product/1823/131208)。

## 安装与使用

1. 在 [腾讯 TokenHub 控制台](https://console.cloud.tencent.com/tokenhub) 创建 API Key。
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
