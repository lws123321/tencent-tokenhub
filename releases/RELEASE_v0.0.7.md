# 腾讯 TokenHub Dify 插件 v0.0.8 发布

> 让 Dify 通过兼容 OpenAI 协议的接口接入腾讯 TokenHub，支持语言、向量、语音合成和语音识别模型。

**发布日期：** 2026-10-09 ｜ **版本：** 0.0.8 ｜ **类型：** 模型 Provider

---

## 本次亮点

- 根据官方 TokenHub 模型列表和调用指南完成模型及参数更新。
- 移除已下线或即将下线的模型：GLM-5、GLM-5.1、GLM-5-Turbo、GLM-5V-Turbo、
   Qwen3.5-Flash、Qwen3.5-Plus。
- 新增当前语言和多模态理解模型，包括 Hy4 Preview、DeepSeek V4.1、DeepSeek V4
   0731/0813、GLM-5.3-FlashX、Kimi K2.8 Preview、MiMo V2.6、Step 5 Preview、
   HY-Vision、YT-VITA 等。
- 新增 TokenHub 文本/多模态向量、MiniMax Speech TTS、WAND/Hy ASR。
- 按 Dify 模型类型拆分预定义配置：`llm`、`text_embedding`、`tts`、`speech2text`。

## 新增

- 40 个 LLM 配置，补齐上下文、输出长度、采样、思考和推理参数。
- 4 个向量模型、6 个 TTS 模型和 2 个语音识别模型。
- 为支持多模态理解的模型增加图片和视频消息转换。
- 非流式响应保留 TokenHub 的 `reasoning_content`，在 Dify 中展示思考过程。

## 变更

- 官方目录仍列出的 `deepseek-v4-flash-202605` 和 `deepseek-v4-pro-202606` 继续保留，
   作为普通模型 ID 直接发送，不再进行运行时别名改写。
- README 改为链接官方模型列表和调用指南，不再维护重复的静态模型表。

## 支持类型

当前插件支持四类 Dify 模型：

- LLM，包括图片/视频理解模型
- 文本向量和多模态向量
- 语音合成
- 语音识别

模型 ID 和服务可用状态由 TokenHub 官方持续维护，请以官方文档为准，不依赖发布时的静态清单。

## 安装 / 升级

1. 在 [腾讯 TokenHub 控制台](https://console.cloud.tencent.com/tokenhub) 创建 **API Key**。
2. 从 Dify 插件市场或本地插件入口安装/升级至 **0.0.8**。
3. 配置：
    - `API Key`（必填）
    - `API Base URL`（可选，默认 `https://tokenhub.tencentmaas.com/v1`）
4. 选择模型类型和模型即可使用。

## 相关链接

- 源码仓库：https://github.com/lws123321/tencent-tokenhub
- TokenHub 模型列表：https://cloud.tencent.com/document/product/1823/130051
- 语言模型调用概览：https://cloud.tencent.com/document/product/1823/130079
- DeepSeek 调用指南：https://cloud.tencent.com/document/product/1823/132248
- 向量模型：https://cloud.tencent.com/document/product/1823/133515
- 语音模型：https://cloud.tencent.com/document/product/1823/135321
- 问题反馈：1073900600@qq.com
