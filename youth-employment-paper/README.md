# Artificial Intelligence Adoption and Youth Employment

A full manuscript prepared for the MDPI journal **Systems**, Special Issue *"Sustainable
Entrepreneurship, Business Model Innovation, and Strategic Approaches for Artificial Intelligence
Adoption in a Dynamic Global Ecosystem."*

**Title:** Artificial Intelligence Adoption and Youth Employment: A Socio-Technical Systems
Perspective on Business Model Innovation and Entrepreneurial Governance

## Deliverables
- `AI_Adoption_and_Youth_Employment.docx` — the manuscript. All symbols, variables and equations
  are native **Word equation-editor (OMML)** objects; equation numbers are right-aligned. Tables and
  references follow MDPI (*Systems*) style.
- `AI_Adoption_and_Youth_Employment_preview.pdf` — a rendered preview (LibreOffice).

## Paper at a glance
- **Question:** How does firm-level AI adoption affect youth employment, and through which mechanisms
  and governance conditions?
- **Framing:** Socio-technical systems theory + the task-based framework (displacement vs.
  reinstatement) — youth employment as a system-level adaptation outcome.
- **Design:** Panel of 3,186 Chinese A-share listed firms, 2011–2023 (28,974 firm-year
  observations); two-way fixed effects, mediation, moderation, PSM, and instrumental-variable
  (shift-share) identification. *The regression tables report illustrative, internally consistent
  estimates that instantiate the design; plug in your own estimation output before submission.*
- **Hypotheses:** H1 AI adoption → youth employment (+); H2a value-creation channel via business
  model innovation; H2b skill-restructuring channel via skill-structure upgrading; H3a–c moderation
  by digital entrepreneurial orientation, ESG performance, and public AI/digital-economy governance.
- **Equations:** 7 numbered display equations (measurement, min–max normalization, baseline,
  mediation, moderation) plus inline math throughout.
- **References:** 57 real references in MDPI format, predominantly 2022–2026, DOI-verified.

> The author block on the title page is a placeholder — fill in your name, affiliation and
> corresponding-author details before submission.

## Reproducing the document
The `build/` folder contains the generator. It writes native OMML (no pandoc dependency):

```
cd build
python3 build_paper.py           # -> youth_ai_employment.docx
```

Files:
- `omml.py` — low-level OMML element builders and the numbered-equation layout (centered equation +
  right-aligned number via tab stops).
- `l2omml.py` — a small LaTeX-subset → OMML converter (Greek, sub/superscripts, fractions, radicals,
  n-ary sums, delimiters, accents).
- `content.py` — the manuscript text as a structured block model with `$latex$` inline math and
  `[[citekey]]` citations.
- `tables.py` — the 9 main tables, 2 appendix tables (MDPI booktabs style) and figure placement.
- `core_refs.py`, `pool_wf.json`, `ref_pool.py`, `finalize_refs.py` → `refs.py` — the real,
  DOI-verified reference set and the key→number mapping.
- `build_paper.py` — assembles front matter, body, equations, tables, figures and references.
- `fig1_framework.png`, `fig2_psm.png` — the conceptual framework and PSM covariate-balance figures.
