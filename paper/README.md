# Environmental impact and net-zero pathways for sustainable AI servers in China

A complete, Nature Sustainability *Analysis*-style manuscript (English) on the compound
**energy–water–climate** impacts of large-scale AI-server deployment in China, 2024–2030,
modelled closely on:

- Xiao, T. *et al.* **Environmental impact and net-zero pathways for sustainable artificial
  intelligence servers in the USA.** *Nature Sustainability* **8**, 1541–1553 (2025) — *primary template*.
- Lee, H. *et al.* **Agricultural workforce as a potential bottleneck of future cropland
  availability.** *Nature Sustainability* (2026) — *secondary style reference*.

## Deliverable

- **`China_AI_Server_Sustainability.docx`** — the full manuscript with six embedded figures,
  numbered references (cited by order of appearance, Nature convention), abstract, five results
  sections, discussion, methods with governing equations, and author/competing-interest blocks.
  - **In-text citations are clickable cross-references**: every superscript citation number is an
    internal hyperlink to its bookmarked entry in the References list (Ctrl/Cmd-click to jump).
  - **Every reference carries a validated, clickable DOI/stable URL** appended in Nature style.
    All 48 references were independently re-verified (Crossref/DOI/publisher/arXiv) and several
    bibliographic errors (page ranges, truncated/incorrect titles, missing DOIs) were corrected.

## What is real vs. simulated

- **References are real (48 in total).** They are drawn from (a) the reference lists of the two
  source *Nature Sustainability* papers (directly reusable, already peer-reviewed) and (b) China-specific
  and recent (2022–2026) works whose existence and bibliographic details were verified via web search
  (Crossref / DOI / publisher pages) by a multi-agent research workflow — e.g. the DeepSeek-V3 technical
  report; the NDRC East-Data-West-Computing plan; Jia *et al.* 2024 (provincial grid emission factors,
  *Applied Energy*); Jiang, Duan & Chen 2025 (China data-centre water footprint, *Applied Energy*);
  Wang *et al.* 2023 (*Nature*, PV/wind transition in China); and the IEA *Energy and AI* (2025) report.
- **Quantitative results are scenario-based simulations.** Provincial attributes (grid carbon and
  water factors, PUE/WUE, wind+solar potential, water-stress) are grounded in publicly reported China
  facts; AI-server capacity trajectories are projections constrained by the domestic AI-accelerator
  advanced-packaging bottleneck (analogue to CoWoS/TSMC in the US study). Headline figures
  (energy 86–253 TWh yr⁻¹; water 0.46–1.37 billion m³ yr⁻¹; carbon 46–136 Mt CO₂e yr⁻¹ by 2030)
  are internally consistent (carbon = facility energy × provincial grid factors, etc.).

## Reproduce

```bash
cd paper/scripts
python3 model.py      # -> data/national_trajectories.csv, provincial.csv, summary.json
python3 figures.py    # -> figures/fig1..fig6 .png
python3 make.py        # -> China_AI_Server_Sustainability.docx
```

Requires: `python-docx matplotlib numpy pandas` (`pip install ...`).

## Layout

```
paper/
├── China_AI_Server_Sustainability.docx   # final manuscript
├── data/                                  # simulated datasets (CSV) + summary.json
├── figures/                               # six generated figures (PNG, 300 dpi)
└── scripts/
    ├── model.py        # provincial dataset + projection engine
    ├── figures.py      # six Nature-style figures
    ├── prose.py        # full manuscript text with citation markers
    ├── build_doc.py    # docx builder + reference engine (numbering by appearance)
    ├── china_refs.py   # verified China-specific references
    └── make.py          # entry point
```
