---
name: image2-diagram
description: Generate raster figures with OpenAI's GPT Image 2 model (aka "image 2" / ChatGPT Images 2.0). Use when the user explicitly asks to draw with image 2 / GPT Image / 图像生成模型, or wants a presentation-grade one-off visual — 封面图, 宣传图, 海报, 概念示意图, slide hero image — where aesthetics matter more than element-level editability. Requires the OPENAI_API_KEY environment variable and network access to api.openai.com. For editable technical diagrams (技术路线图/框架图/流程图 that will be revised), prefer baoyu-diagram + academic-diagram-style instead and say why — unless the user insists on the image model.
version: 1.0.0
---

# GPT Image 2 Figure Generator

Calls OpenAI's Images API (`gpt-image-2`) through the bundled script and returns a PNG.

## Preconditions — check before calling

1. `OPENAI_API_KEY` must be set in the environment. If missing, tell the user exactly how
   to set it (the script prints the same instructions) and stop — never ask them to paste
   the key into chat, and never write a key into any file inside a repository.
2. Network must reach `api.openai.com`. In Claude Code remote/web environments this
   requires the domain to be allowed in the environment's network policy; if the script
   reports a CONNECT/network error, relay that fix.
3. Remind the user each image costs money (quality `low` for drafts, `high` for finals).

## Workflow

1. **Set expectations** when the figure is a technical diagram: output is a flat raster —
   labels can't be edited afterwards, regeneration shifts layout, and small text may
   render imperfectly. Offer the SVG route once, then respect the user's choice.
2. **Craft the prompt in English**, even for Chinese-labeled figures, but quote every
   label verbatim in its own language. A reliable structure:
   - subject + figure type ("a clean technical roadmap infographic with three phases…")
   - explicit layout ("horizontal timeline, three columns left to right…")
   - every text label in quotes, grouped by region ('Phase 1 titled "基础能力建设" containing
     boxes "文献检索引擎", "数据管线"…')
   - style block — for 科研风格: "flat vector style, white background, thin 1px outlines,
     muted colorblind-safe palette (blue #0072B2, green #009E73, vermillion #D55E00),
     Helvetica-like sans-serif labels, no gradients, no shadows, no decorative icons,
     no watermark, publication-quality journal figure"
   - negative constraints: "no spelling errors in labels, no extra text"
3. **Generate**:

   ```bash
   python3 {baseDir}/scripts/generate.py \
     --prompt "..." --out figure.png --size 1536x1024 --quality high
   ```

   Landscape `1536x1024` suits roadmaps/architecture; `--transparent` for slide assets;
   `--n 2` when the user wants options. If the account lacks `gpt-image-2` access, retry
   with `--model gpt-image-1`.
4. **Inspect the result yourself** (view the PNG): verify every label is spelled
   correctly — CJK glyph errors are the most common defect. If a label is wrong, fix the
   prompt (put the broken label FIRST and add "render this text exactly") and regenerate;
   more than ~3 retries means the text is too small — enlarge the layout or switch to SVG.
5. **Deliver** the PNG and the final prompt used (so the user can re-run or tweak it).
