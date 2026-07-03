---
name: academic-diagram-style
description: Publication-grade academic styling for SVG diagrams. Use whenever a diagram/figure is for a paper, thesis, grant proposal, journal, conference slide, or research report, or when the user says 科研风格/学术风格/论文风格/期刊风格/publication style — including every 技术路线图, 框架图, 流程图 drawn in an academic context. This skill OVERRIDES the dark tech theme of baoyu-diagram — keep baoyu-diagram's layout math, spacing rules, and diagram-type references, but replace its colors, typography, and effects with the light publication style defined here. Default to this style when the surrounding project is academic unless the user explicitly asks for a dark/tech look.
version: 1.0.0
---

# Academic Diagram Style (科研风格)

A light, journal-ready design system for SVG diagrams. Compose it with `baoyu-diagram`:
that skill supplies the diagram types, layout algorithms (`references/*.md`), spacing math,
z-order/masking technique, and the standalone-SVG output rules; this skill replaces its
**visual layer** so figures look like they belong in a paper, not a product landing page.

## Hard rules (what makes it read as 科研)

1. **White background** (`#ffffff`). No background grid, no rounded dark canvas, no glow,
   no drop shadows, no gradients. Every element flat.
2. **Dark text on light fills — never light-on-dark.** Body text `#1a1a1a`; secondary
   annotations `#555555`.
3. **Thin strokes.** Node borders `1`px, emphasized borders `1.5`px, connectors `1`px,
   region boundaries `0.75`px dashed (`4,3`). Arrowheads small (6–7px), solid, same color
   as their line.
4. **Muted, colorblind-safe palette** (Okabe–Ito). Fill = 12% opacity tint of the stroke
   color; stroke = full color; text stays dark:

   | Role | Stroke | Fill | Use for |
   |------|--------|------|---------|
   | Category A | `#0072B2` (blue) | `rgba(0,114,178,0.12)` | primary modules, phase 1 |
   | Category B | `#009E73` (green) | `rgba(0,158,115,0.12)` | processes, phase 2 |
   | Category C | `#D55E00` (vermillion) | `rgba(213,94,0,0.12)` | outputs, phase 3, emphasis |
   | Category D | `#E69F00` (orange) | `rgba(230,159,0,0.12)` | infrastructure, resources |
   | Category E | `#CC79A7` (pink) | `rgba(204,121,167,0.12)` | evaluation, feedback |
   | Category F | `#56B4E9` (sky) | `rgba(86,180,233,0.12)` | data, inputs |
   | Neutral | `#999999` (grey) | `rgba(153,153,153,0.10)` | external, misc |

   Use as few colors as the content allows (2–4 is typical for a journal figure).
5. **Typography** — one sans-serif family throughout, journal standard:

   ```
   font-family: "Helvetica Neue", Helvetica, Arial, "PingFang SC",
                "Microsoft YaHei", "Noto Sans CJK SC", sans-serif;
   ```

   | Element | Size | Weight | Color |
   |---------|------|--------|-------|
   | Figure title (optional, often omitted — journals use captions) | 15px | 700 | `#1a1a1a` |
   | Region / phase label | 12px | 600 | `#1a1a1a` |
   | Node label | 11px | 400 | `#1a1a1a` |
   | Sub-label / annotation | 9.5px | 400 (italic allowed) | `#555555` |
   | Axis / year / unit label | 10px | 400 | `#555555` |

   Do NOT `@import` web fonts: papers get compiled offline, so the SVG must render
   correctly with system fonts only.
6. **Restraint over decoration.** No icons/emoji inside nodes; no rounded corners beyond
   `rx="3"`; numbering (①②③ or a/b/c) only when order is meaningful; whitespace does the
   separating, not boxes-inside-boxes.

## Conventions borrowed from journal figures

- **Legend**: simple swatch row (12×12 filled rects + 9.5px labels), bottom-left or
  top-right inside the canvas, only when >2 colors carry meaning.
- **Caption slot**: leave the bottom 8px empty; the caption ("图 1 / Figure 1 …") belongs
  in the manuscript, not inside the image — do not bake it in unless asked.
- **Dashed = optional/feedback/future**; solid =实线主流程. State this in the legend when used.
- **Line routing**: orthogonal (H/V with one bend) for architecture/框架图; straight or
  gentle curves for 路线图 timelines. Never crossing text.
- **Bilingual labels**: if the paper is Chinese, Chinese main label + optional 9.5px
  English sub-label beneath, both centered.

## Output

Follow baoyu-diagram's output rules (single self-contained `.svg`, `viewBox` without fixed
width/height) with white background. For LaTeX, mention the SVG converts cleanly via
`rsvg-convert -f pdf` or Inkscape; for Word/PPT it inserts directly.
