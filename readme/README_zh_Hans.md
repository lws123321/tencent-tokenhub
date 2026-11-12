# 腾讯 TokenHub Dify 插件

腾讯 TokenHub 插件适用于 Dify，支持语言、视觉、多模态理解、向量、语音合成和语音识别模型。

## 介绍

- 插件名称：Tencent TokenHub
- Provider 类型：LLM、文本向量、TTS、语音识别
- 运行环境：Python 3.12
- 认证方式：API Key（可选自定义 API Base URL）

## 支持模型

插件跟随 TokenHub 官方模型目录，支持四类 Dify 模型：LLM（包括视觉和视频理解）、文本向量、TTS、语音识别。
模型目录会独立于插件版本持续更新，当前模型 ID 和可用状态请以官方文档为准：

`minimax-m2.7` 将于 2026 年 11 月 17 日下线，已从预定义模型中移除；使用该模型的应用需改选其他模型。
对于当前官方目录未列出、但未明确公告下线的旧 ID，插件暂时保留，请在 TokenHub 控制台确认可用性。
Dify 中显示的价格仅供参考，折扣和峰谷计费等以 TokenHub 实际账单为准。

- [TokenHub 模型列表](https://cloud.tencent.com/document/product/1823/130051)
- [语言模型调用概览](https://cloud.tencent.com/document/product/1823/130079)
- [DeepSeek 调用指南](https://cloud.tencent.com/document/product/1823/132248)
- [图片理解](https://cloud.tencent.com/document/product/1823/136956)
- [视频理解](https://cloud.tencent.com/document/product/1823/136957)
- [向量模型](https://cloud.tencent.com/document/product/1823/133515)
- [语音模型调用指南](https://cloud.tencent.com/document/product/1823/135321)

> 思考开关会透传为 `thinking: {"type": "enabled" | "disabled"}`。`glm-5.2` 支持 `reasoning_effort: max | xhigh | high | medium | low | minimal | none`；`glm-5.3` 支持 `max | high | low`；`glm-5.3-flash` 支持 `low | high | max`。后两个模型始终开启思考，不接受 `thinking: {"type": "disabled"}`。详情参见 [TokenHub GLM 调用文档](https://cloud.tencent.com/document/product/1823/132061)。

> DeepSeek 推理深度会透传为顶层 `reasoning_effort` 字段。Flash 系列支持 `low` / `high` / `max`；Pro 系列支持 `high` / `max`（兼容值 `low` 会映射为 `high`，`xhigh` 会映射为 `max`）。DeepSeek 思考模式仍通过 `thinking.type` 控制。详情参见 [TokenHub DeepSeek 调用文档](https://cloud.tencent.com/document/product/1823/132248)。

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
- [图片理解](https://cloud.tencent.com/document/product/1823/136956)
- [视频理解](https://cloud.tencent.com/document/product/1823/136957)
- [向量模型](https://cloud.tencent.com/document/product/1823/133515)
- [语音模型](https://cloud.tencent.com/document/product/1823/135321)

## 隐私说明

本插件不会在插件侧持久化用户提示词、模型输出或 API Key。
为完成模型推理，请求内容会发送至腾讯 TokenHub 服务端进行处理。详情见 `PRIVACY.md`。

## 源码

- 源码仓库：https://github.com/lws123321/tencent-tokenhub
