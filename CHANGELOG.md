# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.7] - 2026-08-27

### Added
- Add `glm-5.3-flash` with tool calling and reasoning effort support.
- Refresh bilingual README model tables against the official TokenHub pricing and model catalog.

### Fixed
- Configure `glm-5.3-flash` as an always-thinking model with `low` / `high` / `max`
  reasoning effort options instead of the unsupported thinking toggle.
- Configure `glm-5.3` as an always-thinking model and add its documented reasoning
  effort options.
- Add the documented reasoning effort options for `glm-5.2` while retaining its
  thinking toggle.
- Align Kimi model parameters with the official Kimi calling guide: use top-level
  `reasoning_effort` for `kimi-k3`, keep K2.7 models always thinking with fixed
  sampling parameters, and declare visual input support for all Kimi models.
- Align DeepSeek reasoning-effort options with the official calling guide: Flash
  supports `low` / `high` / `max`, while Pro supports `high` / `max` with legacy
  compatibility mappings; update the recommended temperature default to `1.0`.

## [0.0.6] - 2026-08-24

### Added
- Add `glm-5.3` and factory-direct `deepseek/deepseek-v4-flash-vision-exp`.

### Changed
- Point factory-direct DeepSeek models at latest aliases instead of snapshot IDs:
  `deepseek/deepseek-v4-flash` and `deepseek/deepseek-v4-pro`.
- Keep snapshot IDs `deepseek-v4-flash-202605` and `deepseek-v4-pro-202606` as
  compatibility aliases so existing Dify apps do not need to reselect models;
  invoke requests are rewritten to the latest factory aliases.
- Refresh bilingual README model tables against the official TokenHub catalog.

## [0.0.5] - 2026-08-06

### Added
- Add language models from the latest TokenHub catalog: `hy3`, `hy-mt2-pro`,
  `hy-mt2-plus`, `hy-mt2-lite`, `hy-role`, `glm-5.2`, `kimi-k3`,
  `kimi-k2.7-code`, `kimi-k2.7-code-highspeed`, `qwen3.5-flash`,
  `qwen3.5-plus`, `mimo-v2.5-pro`.

### Changed
- Align predefined model order and metadata with the official
  [TokenHub model list](https://cloud.tencent.com/document/product/1823/130051).
- Update thinking / reasoning-effort allowlists and provider credential probe
  model to current TokenHub IDs.
- Refresh bilingual README model tables.

### Removed
- Remove offline models `hy3-preview` and `minimax-m2.5`.
- Remove models no longer listed: `hunyuan-2.0-*`, `deepseek-v3.2`,
  `deepseek-v3.1-terminus`, `deepseek-r1-0528`, `deepseek-v3-0324`.

## [0.0.4] - 2026-06-03

### Added
- Support **customizable models** in Dify: users can add TokenHub models from the UI
  without waiting for a new plugin release. Enable `customizable-model` alongside the
  existing `predefined-model` flow.
- Add `model_credential_schema` with per-model fields: context size, max output tokens,
  and capability toggles for thinking mode, reasoning effort, vision, and tool calling.
- Implement `get_customizable_model_schema()` in `llm.py` to build model schema
  dynamically from UI credentials (parameter rules and features follow the toggles).
- Add predefined models `deepseek-v4-pro-202606` (DeepSeek-V4-Pro factory direct) and
  `deepseek-v4-flash-202605` (DeepSeek-V4-Flash factory direct).

### Changed
- Bump `dify_plugin` dependency from `~=0.5.0` to `>=0.9.0` to satisfy Dify
  marketplace PR checks.
- Extend thinking-mode and reasoning-effort handling: predefined models still use the
  built-in allowlists; customizable models read `support_thinking` /
  `support_reasoning_effort` from credentials so new models do not require code changes.

### Fixed
- Fix plugin startup validation for select-option labels: quote `"Yes"` / `"No"` in
  `model_credential_schema` so YAML does not parse them as booleans and break Pydantic
  schema validation.

## [0.0.3] - 2026-05-09

### Fixed
- Fix the request payload of the thinking-mode parameter. The plugin now forwards
  `thinking: { "type": "enabled" | "disabled" }` per the official
  [TokenHub thinking docs](https://cloud.tencent.com/document/product/1823/131208),
  instead of the previously incorrect `reasoning_effort: high` payload, which could
  cause some models to ignore the toggle or never enter thinking mode.

### Added
- Add a `reasoning_effort` parameter (`low` / `medium` / `high`) for the four models
  that support it on the TokenHub side: `hy3-preview` (default `low`),
  `deepseek-v4-flash`, `deepseek-v4-pro`, `deepseek-v3.2` (all default `high`).

### Changed
- Align the default `thinking` value of each model with the official docs:
  - Default `enabled`: `deepseek-v4-flash`, `deepseek-v4-pro`, `glm-5`, `glm-5.1`,
    `glm-5-turbo`, `glm-5v-turbo`, `kimi-k2.5`, `kimi-k2.6`.
  - Default `disabled`: `hy3-preview`, `deepseek-v3.2`.
- Align the `label` field of every model yaml with the "Model Name" column in the
  official [TokenHub model list](https://cloud.tencent.com/document/product/1823/130051)
  (e.g. `deepseek-v4-pro` -> `DeepSeek-V4-Pro`, `glm-5.1` -> `GLM-5.1`).
- Split `hy3-preview` reasoning controls: the `reasoning_effort` options are now the
  officially supported `[low, medium, high]` (was `[no_think, low, high]`), and the
  thinking toggle is exposed as a separate boolean `thinking` parameter.

### Removed
- Remove the `thinking` toggle from `minimax-m2.5` and `minimax-m2.7`. The official
  docs state thinking is always on for these two models and cannot be disabled, so
  exposing a toggle would mislead users.

## [0.0.2] - 2026-04-27

### Changed
- Bilingual README and minor wording cleanups for the Dify marketplace listing.

## [0.0.1] - 2026-04-27

### Added
- Initial release. Adds the Tencent TokenHub LLM integration covering the DeepSeek,
  Hunyuan, GLM, Kimi and MiniMax model families.
