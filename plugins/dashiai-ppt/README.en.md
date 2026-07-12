# DashiAI PPT Skill · Web Decks / Per-Page Console / Editable PPTX Export

![GitHub stars](https://img.shields.io/github/stars/chuspeeism/dashiAI-ppt-skill?style=flat-square)
![Skill](https://img.shields.io/badge/Skill-Agent-111111?style=flat-square)
![HTML Deck](https://img.shields.io/badge/HTML-Deck-0A7CFF?style=flat-square)
![PPTX Export](https://img.shields.io/badge/PPTX-Editable%20Export-D24726?style=flat-square)
![Claude Code](https://img.shields.io/badge/Claude%20Code-Supported-6B5B95?style=flat-square)
![Codex](https://img.shields.io/badge/Codex-Supported-222222?style=flat-square)
![Doubao](https://img.shields.io/badge/Doubao-Supported-3370FF?style=flat-square)
![Marvis](https://img.shields.io/badge/Marvis-Supported-FF5A5F?style=flat-square)
![Workbuddy](https://img.shields.io/badge/Workbuddy-Supported-2EA44F?style=flat-square)
![Dumate](https://img.shields.io/badge/Dumate-Supported-F59E0B?style=flat-square)
![Qclaw](https://img.shields.io/badge/Qclaw-Supported-14B8A6?style=flat-square)
[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue?style=flat-square)](./LICENSE)

> 🌏 **中文版：[README.md](./README.md)**

A PPT skill built for people who actually present at work. Throw a document at your AI agent and get back, minutes later, a web-based deck that **opens offline, flips through horizontally, and puts an editing console on every single page** — fix whatever you don't like right in the browser, then **export a real, editable PPTX with one click**.

- **12 visual themes**: Soft Neumorphic, Neon Glow, Code Mono, Glass Candy, Spectrum Charts, Dark Atlas, Cool White Research, Black Gold Lab, Deep Blue Editorial, Golden Index, High-Energy Growth, Soundwave Neon
- **1,020 layout pages**: from dozens of chart types and analysis frameworks like SWOT / Porter's Five Forces / Business Model Canvas, to architecture diagrams, timelines, and photo galleries — every page you'd actually need in a real presentation comes as a ready-made layout
- **8,576 tunable controls**: 2,372 sliders, 4,276 toggles, 1,825 dropdowns, plus a hundred-odd image / icon pickers — drag a slider to add or remove page modules
- **Generation ≠ done**: edit text, swap layouts, switch charts, change palettes, restyle the whole deck — all in the browser, with every edit written back to the file automatically

> We spent over two months polishing this skill together with the best designers on our team. The rich visuals are just the surface — the real problem we set out to solve: **Making a deck editable after generation matters more than the generation itself.**

![Generated deck demo](https://github.com/chuspeeism/dashiAI-ppt-skill/releases/download/readme-assets-v1/hero-result.gif)

## 12 Built-in Visual Themes

At generation time the skill shows you previews to choose from, and you can ask the agent to swap the whole theme at any point. Each preview below shows 4 body layouts picked from that theme's own layout library (charts, analysis frameworks, cards, table of contents, etc.) — **all actually rendered by this skill, not mockups**:

|  |  |
|---|---|
| <img src="https://github.com/chuspeeism/dashiAI-ppt-skill/releases/download/readme-assets-v1/theme01.jpg" width="440" alt="theme01 Soft Neumorphic body layouts preview"><br>**theme01 Soft Neumorphic (轻拟态风)**<br>Best for: product intros, corporate reports, proposal walkthroughs, lightweight launches<br>Made for: startup teams, product managers, sales consultants | <img src="https://github.com/chuspeeism/dashiAI-ppt-skill/releases/download/readme-assets-v1/theme02.jpg" width="440" alt="theme02 Neon Glow body layouts preview"><br>**theme02 Neon Glow (炫光紫绿风)**<br>Best for: tech launch events, AI / autonomous driving / robotics topics, growth stories<br>Made for: tech founders, engineering leads |
| <img src="https://github.com/chuspeeism/dashiAI-ppt-skill/releases/download/readme-assets-v1/theme03.jpg" width="440" alt="theme03 Code Mono body layouts preview"><br>**theme03 Code Mono (深浅代码风)**<br>Best for: technical proposals, developer conferences, system architecture, AI engineering practice<br>Made for: engineers, architects, developer communities | <img src="https://github.com/chuspeeism/dashiAI-ppt-skill/releases/download/readme-assets-v1/theme04.jpg" width="440" alt="theme04 Glass Candy body layouts preview"><br>**theme04 Glass Candy (玻璃糖果风)**<br>Best for: youthful brands, consumer products, creative pitches, social-media-flavored content<br>Made for: brand teams, designers, content creators |
| <img src="https://github.com/chuspeeism/dashiAI-ppt-skill/releases/download/readme-assets-v1/theme05.jpg" width="440" alt="theme05 Spectrum Charts body layouts preview"><br>**theme05 Spectrum Charts (色谱图表风)**<br>Best for: data reports, market analysis, KPI reviews, industry research<br>Made for: data analysts, consultants, researchers | <img src="https://github.com/chuspeeism/dashiAI-ppt-skill/releases/download/readme-assets-v1/theme06.jpg" width="440" alt="theme06 Dark Atlas body layouts preview"><br>**theme06 Dark Atlas (深色图谱风)**<br>Best for: dense data displays, strategic analysis, tech / finance / industry reports<br>Made for: strategy teams, investors, executive presenters |
| <img src="https://github.com/chuspeeism/dashiAI-ppt-skill/releases/download/readme-assets-v1/theme07.jpg" width="440" alt="theme07 Cool White Research body layouts preview"><br>**theme07 Cool White Research (冷白调研风)**<br>Best for: research reports, whitepapers, competitive analysis, academic / policy communication<br>Made for: research institutes, consulting teams, think tanks | <img src="https://github.com/chuspeeism/dashiAI-ppt-skill/releases/download/readme-assets-v1/theme08.jpg" width="440" alt="theme08 Black Gold Lab body layouts preview"><br>**theme08 Black Gold Lab (黑金实验风)**<br>Best for: premium launches, brand pitches, experimental concepts, luxury-tech storytelling<br>Made for: high-end brands, creative directors |
| <img src="https://github.com/chuspeeism/dashiAI-ppt-skill/releases/download/readme-assets-v1/theme09.jpg" width="440" alt="theme09 Deep Blue Editorial body layouts preview"><br>**theme09 Deep Blue Editorial (深蓝杂志风)**<br>Best for: brand stories, interviews, corporate profiles, long-form features<br>Made for: PR teams, media editors, founders | <img src="https://github.com/chuspeeism/dashiAI-ppt-skill/releases/download/readme-assets-v1/theme10.jpg" width="440" alt="theme10 Golden Index body layouts preview"><br>**theme10 Golden Index (金色指数风)**<br>Best for: financial data, investment reports, business indices, annual rankings<br>Made for: investment firms, financial analysts, business media |
| <img src="https://github.com/chuspeeism/dashiAI-ppt-skill/releases/download/readme-assets-v1/theme11.jpg" width="440" alt="theme11 High-Energy Growth body layouts preview"><br>**theme11 High-Energy Growth (高能增长风)**<br>Best for: growth reviews, business plans, fundraising pitches, market expansion plans<br>Made for: founders, growth teams, VC/PE roadshows | <img src="https://github.com/chuspeeism/dashiAI-ppt-skill/releases/download/readme-assets-v1/theme12.jpg" width="440" alt="theme12 Soundwave Neon body layouts preview"><br>**theme12 Soundwave Neon (声波霓虹风)**<br>Best for: music and entertainment, trend events, livestream content, youth-oriented launches<br>Made for: entertainment brands, event planners, trend-driven consumer brands |

## Get Started in 30 Seconds

Install (or update) with a single command — it detects common skills directories automatically, installs into every one it finds, and keeps already-installed dependencies:

```bash
npx dashiai-ppt-skill
```

Use `--dir <path>` to target a specific skills directory (e.g. `--dir ~/.claude/skills`), or `--list` to see what gets detected.

Or just hand this to your AI agent and let it figure out the install:

```text
Install the dashiai-ppt skill for me: run `npx dashiai-ppt-skill`, or clone https://github.com/chuspeeism/dashiAI-ppt-skill
```

> When installing from the repo instead of npm, the skill content lives in the `skills/dashiai-ppt/` subdirectory — the agent should place that subdirectory into its own skills directory. Agents with no fixed skills-directory convention (e.g. Marvis / Workbuddy / Dumate / Qclaw) can just drop that subdirectory anywhere and point them at its `SKILL.md`.

Already installed? Re-run `npx dashiai-ppt-skill` to update in place.

Requirements: a machine that runs **Node.js 18+ and npm** (dependencies auto-install on first generation); exporting PPTX / PDF requires Chrome / Chromium / Edge installed locally.

Once installed, just tell your agent:

```text
帮我制作一份年终总结汇报 PPT。
(Make me a year-end summary deck.)
```

Or try these:

```text
根据我这份文档，生成一份科技感的 PPT，10 页左右。
(Turn this document of mine into a tech-styled deck, about 10 pages.)
把这套 PPT 的风格换成学术感拉满的专业风格。
(Restyle this deck into something thoroughly academic and professional.)
用 dashiai-ppt 直接生成 PPT 格式的文件（跳过网页，直接交付可编辑 PPTX）。
(Use dashiai-ppt to generate a PPT file directly — skip the web deck, deliver an editable PPTX.)
```

## Highlights

- 🎨 **12 visual themes**: from Soft Neumorphic to Soundwave Neon, covering product intros, technical proposals, data reports, brand stories, fundraising pitches, and more
- 🧩 **1,020 layout pages**: each theme has its own page structures and visual language, spanning 20 page roles (cover, table of contents, metrics, trends, comparison, process, risk, closing...)
- 📊 **Charts and analysis frameworks out of the box**: radar, waterfall, treemap, funnel, heatmap, Sankey, and Gantt charts, plus framework layouts for SWOT, Porter's Five Forces, PEST, Business Model Canvas, Double Diamond, and more
- 🎛 **A console on every page**: sliders, toggles, dropdowns — switch layouts, tune module counts, change palettes, shift the page's focus, all with a single drag
- ✏️ **All text is editable**: click any text to edit it in place; decorated text auto-adapts as the length changes
- 🖼 **Click-to-swap images / videos**: click or drag onto a media slot to replace it, with automatic image compression; text-only source material gets image placeholders reserved automatically
- 🔄 **One-click restyling**: reskin the same content across all 12 themes in real time, with 9 page-transition animations to choose from
- 📄 **Three export formats**: single-file offline HTML / PDF / editable PPTX — or ask for PPTX from the very start
- 💾 **Fully local**: generation, editing, and export all happen on your machine; edits write back to the file automatically, and the finished deck doesn't depend on the original asset paths

## Good Fit / Not a Fit

**✅ Good fit**: industry research / fundraising reviews / competitive analysis / trend reports / project reports / proposal presentations / pitch materials / internal training — anywhere you need a structurally complete, visually consistent deck you can keep editing

**❌ Not a fit**: real-time multi-user collaborative editing (it's local files) / pixel-by-pixel hand-crafted visuals (template visuals are locked by default — trading freedom for a guaranteed aesthetic floor) / pure web chatbots with no filesystem or shell

## Common Use Cases

| Task | Recommended approach |
|------|---------|
| Long document → report deck | Hand the document to the agent, state the audience and page count; the skill asks which style you want first |
| Year-end summary / business review | Just say "make me a year-end summary deck" — data and metric pages get laid out automatically |
| Data / research reports | Pick Spectrum Charts, Dark Atlas, or Cool White Research — their layout pools are chart-heavy |
| Fundraising pitch / growth story | Pick High-Energy Growth or Golden Index — capital-flow, index, and milestone layouts built in |
| Deliver PPTX directly | Say explicitly "generate a PPT file / export PPTX" to skip the web intermediate |
| Presenting to your boss / teammates | The preview server allows LAN access by default — open it on a phone or tablet; presentation mode is one click away |

## Why an HTML Deck — and Why It Doesn't Stop at HTML

- **Better for agents to generate and modify**: HTML / JSON is text — an agent can read, edit, and validate it directly; every page is "layout + copy fields", so editing copy never breaks the visuals.
- **More expressive**: entrance animations, page transitions, interactive controls, dark/light mode — experiences static formats simply can't deliver.
- **The output is itself the editor**: what you get isn't a stack of pasted images, it's a web-based PPT editor — flip pages, edit text, swap images, tune layouts, ready the moment you open it.
- **Lighter to deliver**: bundle into a single offline HTML file with one click; the local preview server allows LAN access by default, so phones and tablets on the same WiFi can open it directly.
- **It doesn't lock you into the web**: if you're tired of the AI era's "fake PPTs dressed up as web pages", export a real PPTX with one click — reconstructed node by node, with text kept editable. The export engine, [html-deck-to-pptx](skills/dashiai-ppt/project/packages/html-deck-to-pptx), is open-sourced under MIT.

Page-by-page comparison between the HTML deck and the exported PPTX:

![Page-by-page comparison of HTML deck and exported PPTX](https://github.com/chuspeeism/dashiAI-ppt-skill/releases/download/readme-assets-v1/html-vs-pptx.gif)

## Platform Support

> **This skill is agent-agnostic.** The real bar is capability, not brand — any AI agent that can **read/write local files, run shell commands, and has a local Node.js environment** can use it to generate and export decks. The table below only lists platforms we've tested; it does not mean "these only".

| Platform | Status | Notes |
|------|------|------|
| Claude Code | Supported | Native skill workflow: generation, iteration, and export end to end |
| Codex | Supported | Ships with an `agents/openai.yaml` config; can also call image generation to fill in visuals |
| Doubao | Supported | Doubao only just added skill support — and already runs this one remarkably well |
| Marvis / Workbuddy / Dumate / Qclaw | Supported | Local agents with their own skill systems and no `~/.claude/skills` convention — drop `skills/dashiai-ppt/` anywhere and point them at `SKILL.md` |
| Cursor / other local agents | Works | Needs file read/write and shell execution |
| Plain web chatbots | Not recommended | The generator needs a local Node.js environment |

## How It Works

Drop in whatever document you have and say you want a deck (the agent discovers this skill on its own — or name `dashiai-ppt` to force it), then wait a few minutes for a complete deck:

1. **Describe what you need** — topic, audience, page count, the takeaways you want to land (a bare topic is fine too; the AI will draft the content)
2. **Pick a style** — if you haven't specified one, the skill shows previews of all 12 themes and lets you choose (it never decides for you), and confirms whether you need images / video
3. **Auto-drafting** — the skill distills your request into a structured `goal.json`, picks pages from the layout library, fills in the copy, and renders after multiple validation passes
4. **Get a link** — generation ends with a local URL; open it and you're inside the web deck editor
5. **Edit as you go** — every page has a console: edit text, swap images, tune module counts, change palettes; every change saves back to the file automatically
6. **Deliver** — not happy? Ask the agent to restyle and redo. Happy? Export offline HTML / PDF / editable PPTX

If your source material is text-only, the skill reserves image slots on the right pages as appropriate; click a placeholder later to fill it in:

![One-click image fill for placeholders](https://github.com/chuspeeism/dashiAI-ppt-skill/releases/download/readme-assets-v1/image-placeholder.gif)

## Editing After Generation: Every Page Has Its Own Console

The single most important design decision in this skill: **how you edit after generation matters more than the generation itself.** Every page ships with a console, and across the system we designed 20+ dimensions of editing space — content, layout, module count, page focus, preset palettes, page transitions. Everything you routinely need to change has a knob (colors and fonts use preset schemes, not free-form values — the reasoning is below).

### Direct edits: text and images

Click any text anywhere to edit it; decorated text auto-adapts to its length. Click or drag onto image and video slots to replace them; uploaded images are compressed automatically.

| Click any text to edit in place | Add an image |
|---|---|
| ![Click text to edit in place; decorative elements adapt to text length](https://github.com/chuspeeism/dashiAI-ppt-skill/releases/download/readme-assets-v1/text-edit.gif) | ![Insert an image into a page](https://github.com/chuspeeism/dashiAI-ppt-skill/releases/download/readme-assets-v1/add-image.gif) |

### Console edits: layout, module count, charts, palettes

TOC pages, table pages, multi-item pages (layouts with several parallel entries), and image-text pages — drag the slider on the right of the console to set how many modules a page shows; you can also shift the page's logical emphasis with a slider to control the pacing of your talk.

| Drag a slider to add or remove modules | Switch layouts |
|---|---|
| ![Drag sliders to adjust TOC, table, multi-item, and image counts](https://github.com/chuspeeism/dashiAI-ppt-skill/releases/download/readme-assets-v1/slider-edit.gif) | ![Switch a page layout in one sentence](https://github.com/chuspeeism/dashiAI-ppt-skill/releases/download/readme-assets-v1/layout-switch.gif) |

| Swap charts | Palette switching within a theme |
|---|---|
| ![Swap chart types in one sentence](https://github.com/chuspeeism/dashiAI-ppt-skill/releases/download/readme-assets-v1/chart-switch.gif) | ![Each theme supports local palette swaps](https://github.com/chuspeeism/dashiAI-ppt-skill/releases/download/readme-assets-v1/palette-switch.gif) |

### Page transitions

9 built-in transition animations: liquid morph, cut-in, horizontal slide, line sweep, zoom, vertical bars, blend, horizontal cut, gallery (you can also switch animations off entirely with one click). Pick the one you like in the console and switch instantly:

![Page transition animations](https://github.com/chuspeeism/dashiAI-ppt-skill/releases/download/readme-assets-v1/transitions.gif)

### And more

- The thumbnail sidebar supports **drag-and-drop page reordering**; pages can be **skipped / deleted / duplicated**
- The top bar gives you one-click **presentation mode**, **dark/light theme** toggle, and **reset all** changes
- When opened through the local preview server, every edit **writes back into `index.html` itself**; when you double-click the HTML file directly, edits are stored in the browser — remember to export before distributing

## What's in the Layout Library

While writing this README, we rendered all 12 themes for real and went through the full list of 1,020 layouts. Just about every page you'd actually use in a report has a ready-made layout:

- **Chart pages**: line, bar, waterfall, radar, treemap, funnel, heatmap, Sankey, dumbbell, bubble, scatter, rose, Pareto, sunburst, waffle, slope... dozens of chart forms as ready-made pages — the AI rewrites both the data and the takeaway copy to fit your content
- **Analysis frameworks**: SWOT, Porter's Five Forces, PEST, Business Model Canvas, BCG Matrix, Double Diamond, AARRR, RFM, flywheel, technology hype cycle, swimlane diagrams, Gantt scheduling
- **Architecture and relationships**: industry chain tiers, hierarchies, radial relationships, network graphs, mind maps, org charts, ecosystems
- **Image-text pages**: galleries, filmstrips, mosaic collages, polaroids, diptychs/triptychs, mood boards, photo walls
- **Narrative pacing pages**: pull quotes, manifestos, chapter dividers, TOC, timelines, milestones, FAQ, team intros, closing pages

A pass through the chart layouts (at 2x speed):

![Tour of chart layouts](https://github.com/chuspeeism/dashiAI-ppt-skill/releases/download/readme-assets-v1/layouts-tour.gif)

Built-in analysis frameworks and specialized layouts (SWOT, Porter's Five Forces, PEST, Business Model Canvas, Double Diamond, capital-flow Sankey...):

![Built-in analysis framework layouts](https://github.com/chuspeeism/dashiAI-ppt-skill/releases/download/readme-assets-v1/analysis-models.png)

The high-frequency staples — TOC, table, big-number poster, and image-text pages:

![Common layouts](https://github.com/chuspeeism/dashiAI-ppt-skill/releases/download/readme-assets-v1/common-layouts.png)

How the library is organized:

- **20 page roles**: cover, summary, TOC, chapter divider, background, metrics, trends, comparison, proportion, relationship, case study, image, process, risk, outlook, atmosphere, action, key points, team, closing
- **One primary information role per page**: when there's too much to say, tighten the copy, split the page, or switch layouts — never cram a page full
- **Cover rules**: the first 5 pages of each theme are cover candidates, one cover per deck, and no layout repeats within a deck

## Export: HTML / PDF / a Genuinely Editable PPTX

The export menu in the top-right corner of the browser has three options:

- **HTML**: bundled fully client-side into a single offline file — double-click to open, share with anyone
- **PDF**: for archiving and printing
- **PPTX**: **editable export** — layouts reconstructed node by node, all text kept editable; perfectly fine to hand off to your boss / professor / teammates for further edits

![One-click export to editable PPT](https://github.com/chuspeeism/dashiAI-ppt-skill/releases/download/readme-assets-v1/export-pptx.gif)

You can even skip the HTML intermediate entirely — tell the agent "use this skill to generate a PPT file" and go from prompt straight to PPTX.

Command-line export (no browser needed; if installed under Codex, replace `~/.claude` with `~/.codex`):

```bash
npm --prefix ~/.claude/skills/dashiai-ppt/project run export:pptx -- <deck-output-dir>/ppt output.pptx
npm --prefix ~/.claude/skills/dashiai-ppt/project run export:pdf  -- <deck-output-dir>/ppt
```

## Directory Structure

```
dashiAI-ppt-skill/
├── SKILL.md              ← Skill entry point: workflow, principles, command reference
├── README.md             ← Chinese README
├── README.en.md          ← This file
├── LICENSE               ← AGPL-3.0 license
├── agents/
│   └── openai.yaml       ← Codex / OpenAI agent interface config
├── assets/               ← Theme previews, icons, README images
├── project/              ← Built-in generator (React rendering, 12 themes, export engines)
│   ├── layout-manifest.json  ← Field contracts for all 1,020 layouts
│   ├── scripts/              ← Render / validate / preview / export scripts
│   └── packages/html-deck-to-pptx  ← Editable PPTX export engine (MIT)
├── references/
│   ├── options.md            ← Theme catalog and generation options
│   ├── layout-pool.md        ← Layout pools for the 12 themes
│   ├── layout-roles.md       ← The 20 page roles explained
│   ├── goal-spec.schema.json ← JSON Schema for goal.json
│   └── examples/             ← Two sample specs: product portfolio strategy, fundraising annual review
└── scripts/
    ├── render_goal_deck.sh       ← One-shot render entry (validate → render → re-validate → preview)
    └── check_latest_version.mjs  ← Silent version check
```

## Core Design Principles

1. **Editing matters more than generation** — the output is an editor, not pasted images; every page has to survive "just one more tweak"
2. **Lock the template, fill in the copy** — keep each layout's original visuals, structure, palette, and chart type by default, replacing only the text; template locking guarantees the aesthetic floor
3. **Practical layouts first** — charts, logic diagrams, architecture diagrams, and analysis frameworks are everyday report material, so they ship as ready-made pages
4. **One information role per page** — too much content means tightening, splitting, or switching layouts, never cramming a page full
5. **Validation as the safety net** — multiple automated checks before and after rendering; template placeholder copy is never allowed into a deliverable
6. **Clean deliverables** — the final deck ships without theme switchers, page indicators, or navigation hints; your audience sees a clean deck and nothing else
7. **Fully local** — generation, editing, and export all happen on your machine; the deliverable doesn't depend on original asset paths, ready for archiving and handoff

## FAQ

**Can it really export an editable PPTX?**
Yes. That's the biggest difference between this skill and "fake PPTs dressed up as web pages". The export engine reconstructs the HTML layouts into native PPTX elements node by node, keeping all text editable; regions that genuinely can't be mapped are rasterized to images, but their text is still pulled back from the live DOM and stays editable. PPTX can never match the full power of HTML, but we've preserved as much editability as possible.

**How many tokens does one deck cost?**
A 10-page deck measures around 200K tokens in practice (varies with document length and rounds of revision). Roughly, one 5-hour Claude Code usage window covers about 6–7 decks (quotas differ by subscription tier — treat this as a ballpark); many Chinese AI agents come with free quotas, in which case don't even bother counting.

**Where do my in-browser edits get saved?**
When opened through the local preview server (`http://127.0.0.1:<port>/`), edits write straight back into `index.html` itself. When you double-click the HTML file to open it, edits live in the browser's localStorage — remember to export before distributing.

**Can I customize colors / fonts?**
Not as free-form values. Visual styling is decided by the selected theme package as a whole; some page consoles offer preset palette switches. This is deliberate: stable output matters more than free color picking.

**Does it need internet access? Is my content safe?**
Zero content upload: your documents and deck content are never sent to any server — generation, editing, and export all run locally, and the output opens offline. Only two things touch the network: npm auto-installing dependencies on first generation, and a silent version check after each task (reads only the remote version number, 8-second timeout, skips on failure). Also, the local preview server allows LAN access by default (handy for phone/tablet preview) — viewing only; export endpoints are open to localhost only.

**What are the requirements?**
Node.js 18+ and npm (dependencies auto-install on first generation); PPTX / PDF export needs Chrome / Chromium / Edge installed locally (point to it with the `CHROME_PATH` environment variable if needed).

**How do I update?**
Run `git pull` in the skill directory. The skill also checks for new versions silently after each task — it stays quiet when you're up to date, and only adds a note at the end of a reply when there's a new release.

## Contributing

If something's clunky, come yell at us in an Issue; if you like it, drop a Star. We welcome:

- Bug reports and layout glitch screenshots (theme name plus a screenshot of the broken page helps a lot)
- Requests for new layouts / themes, with real use cases
- Export fidelity feedback (side-by-side screenshots of HTML vs PPTX)

> The development cost was honestly terrifying — but if the stars climb fast enough, version 2.0 inflates on the spot.

## License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)** — the strongest copyleft license among OSI-approved open source licenses. You are free to use, modify, and distribute this project, including for commercial purposes. However, if you distribute a modified version, or offer this software (or a modified version) to users over a network (e.g. as a SaaS), you must make the complete corresponding source code available under AGPL-3.0.

**Exception:** the subpackage [`project/packages/html-deck-to-pptx`](skills/dashiai-ppt/project/packages/html-deck-to-pptx) is independently licensed under the **MIT License** (see the LICENSE file in that directory) and may be freely used in closed-source or commercial projects.

Copyright (c) 2026 [chuspeeism](https://github.com/chuspeeism). See the [LICENSE](LICENSE) file for the full text. For commercial licensing beyond AGPL-3.0, please contact the author.

## Star History

<a href="https://www.star-history.com/#chuspeeism/dashiAI-ppt-skill&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=chuspeeism/dashiAI-ppt-skill&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=chuspeeism/dashiAI-ppt-skill&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=chuspeeism/dashiAI-ppt-skill&type=Date" />
 </picture>
</a>
