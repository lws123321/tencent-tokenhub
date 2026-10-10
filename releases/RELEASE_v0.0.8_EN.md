# Tencent TokenHub Dify Plugin v0.0.8 Release

> Connect Dify to Tencent TokenHub through OpenAI-compatible LLM, embedding, TTS, and speech-to-text interfaces.

**Release Date:** 2026-10-09 | **Version:** 0.0.8 | **Type:** Model Provider

---

## Highlights

- Updated the plugin against the official TokenHub catalog and calling guides.
- Removed models marked offline or scheduled for offline removal: GLM-5, GLM-5.1,
   GLM-5-Turbo, GLM-5V-Turbo, Qwen3.5-Flash, and Qwen3.5-Plus.
- Added current language and multimodal understanding models, including Hy4 Preview,
   DeepSeek V4.1, DeepSeek V4 0731/0813, GLM-5.3-FlashX, Kimi K2.8 Preview,
   MiMo V2.6, Step 5 Preview, HY-Vision, and YT-VITA.
- Added TokenHub text/multimodal embeddings, MiniMax Speech TTS, and WAND/Hy ASR.
- Split predefined model configuration by Dify model type: `llm`, `text_embedding`,
   `tts`, and `speech2text`.

## Added

- 40 LLM definitions with complete context, output, sampling, thinking, and reasoning
   settings where supported.
- 4 embedding models, 6 TTS models, and 2 speech-to-text models.
- Image and video message conversion for models that support multimodal understanding.
- Non-streaming preservation of TokenHub `reasoning_content` in Dify thought output.

## Changed

- DeepSeek snapshot IDs `deepseek-v4-flash-202605` and `deepseek-v4-pro-202606` are
   retained because they remain in the official catalog and are sent directly to
   TokenHub without runtime alias rewriting.
- README files now link to the official catalog and calling guides instead of keeping
   a duplicated model table.

## Supported Types

The plugin currently supports four Dify model types:

- LLM, including image/video understanding models
- Text embedding and multimodal embedding
- Text-to-speech
- Speech-to-text

The current model IDs and service availability are maintained by TokenHub. See the
official documentation rather than relying on a release-time static list.

## Installation / Upgrade

1. Create an **API Key** in the [Tencent TokenHub Console](https://console.cloud.tencent.com/tokenhub).
2. Install or upgrade to **0.0.8** from the Dify plugin marketplace or local plugin entry.
3. Configure:
    - `API Key` (required)
    - `API Base URL` (optional, default `https://tokenhub.tencentmaas.com/v1`)
4. Select a supported model type and model.

## Links

- Source repository: https://github.com/lws123321/tencent-tokenhub
- TokenHub model list: https://cloud.tencent.com/document/product/1823/130051
- Language model overview: https://cloud.tencent.com/document/product/1823/130079
- DeepSeek calling guide: https://cloud.tencent.com/document/product/1823/132248
- Embedding models: https://cloud.tencent.com/document/product/1823/133515
- Speech models: https://cloud.tencent.com/document/product/1823/135321
- Contact: 1073900600@qq.com
