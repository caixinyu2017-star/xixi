# diagram-skills — 来源与许可 / Provenance & licenses

本插件把两个上游 skill 原样打包（保留原始目录结构与相对路径引用），用于高质量技术作图。
This plugin vendors two upstream skills verbatim (original layout and relative-path references intact) for high-quality technical diagramming.

## 1. baoyu-diagram

- 上游 / Upstream: <https://github.com/JimLiu/baoyu-skills> — `skills/baoyu-diagram/`
- 版本 / Version: skill v1.117.3, vendored at commit `a4e78af8136fa0bbfd7a8243d2f6813b4b6398c9` (2026-07-03)
- 许可 / License: MIT, Copyright (c) 2026 Jim Liu — see `skills/baoyu-diagram/LICENSE`
  (copied from the upstream repository root, which covers the whole repo)
- 内容 / Contents: `SKILL.md` + `references/{architecture,flowchart,sequence,structural}.md` + `scripts/main.ts`
- 说明 / Notes: 输出为单个自包含、可编辑的 `.svg` 文件。`scripts/main.ts` 是可选的 SVG→PNG
  转换脚本，需要 `bun`（或 `npx`）与 npm 包 `sharp`；不装它们不影响 SVG 输出。
  The optional SVG→PNG script needs `bun`/`npx` + the `sharp` npm package; SVG output works without them.

## 2. frontend-design

- 上游 / Upstream: <https://github.com/anthropics/skills> — `skills/frontend-design/`
- 版本 / Version: vendored at commit `9d2f1ae187231d8199c64b5b762e1bdf2244733d` (2026-07-03)
- 许可 / License: Apache-2.0 — see `skills/frontend-design/LICENSE.txt`
- 内容 / Contents: `SKILL.md` + `LICENSE.txt`（上游即这两个文件 / upstream ships exactly these two files）
- 说明 / Notes: Anthropic 官方审美校准 skill：刻意的配色/字体/版式决策，避免"模板感/AI 味"。
  与 baoyu-diagram 互补——后者固定深色主题，需要浅色或文档内嵌风格时用它校准。

## 3. academic-diagram-style / image2-diagram（本仓库原创 / original to this repo）

这两个 skill 为本仓库自研，不来自上游：`academic-diagram-style` 是叠加在 baoyu-diagram 之上的
科研/期刊风格视觉层；`image2-diagram` 封装 OpenAI Images API（`gpt-image-2`），API key 一律从
环境变量 `OPENAI_API_KEY` 读取，仓库内不存放任何密钥。
These two skills are original to this repo (not vendored): an academic/journal visual layer over
baoyu-diagram, and a GPT Image 2 wrapper that reads `OPENAI_API_KEY` from the environment — no
secrets are stored in this repository.

## 更新 / Updating

重新从上游拉取对应目录覆盖本地副本即可；两个上游目录都是自包含的（`SKILL.md` 以相对路径引用
`references/`、`scripts/`）。To update, re-copy the upstream directories; both are self-contained.
