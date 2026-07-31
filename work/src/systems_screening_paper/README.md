# Paper 8 — "Screening Under Signal Collapse"

Target: MDPI *Systems*, Special Issue **"Navigating Digital Transformation: Leadership
and Decision Making in Today's Systems"** (Guest Editor Prof. Dr. Maja Meško).

Full title: *Screening Under Signal Collapse: Choice and Architecture Experiments on
Employer Decision Rules and Youth Access to Entry-Level Work.*

## The question

Generative AI has made a polished written application nearly free to produce. Under
Spence's single-crossing condition a signal that costs nothing to produce cannot
separate types, so the written application has stopped informing. Two 2025 studies
establish that this collapse is real rather than hypothetical: on a large freelancing
platform the correlation between cover-letter fit and callback fell by about half after
an AI writing tool was introduced, and a structural treatment of the same market finds
employers' willingness to pay for tailoring disappearing entirely.

What has been missing is the employer's side of the adjustment. Given that the written
application no longer informs, what do decision makers substitute towards, how much is
each substitute worth, and can the answer be changed by design?

## Design

Two linked experiments in one instrument, administered to 452 managers who make real
entry-level shortlist decisions in knowledge-intensive firms of the Yangtze River Delta.

* **Study 1 — choice-based conjoint.** A D-efficient paired design (D-error 0.570,
  minimum-overlap constraint, eight blocks, explicit opt-out) over seven attributes:
  AI-disclosure, process-evidence portfolio, verified proctored assessment,
  institutional tier, employee referral, relevant internship, expected salary. 14 tasks
  per respondent → 6328 choice sets and 12,656 profile evaluations. Salary enters as a
  numeraire so every attribute is expressible as a compensating differential.
  Estimated three ways: conditional logit with respondent-clustered sandwich standard
  errors, mixed logit by simulated maximum likelihood with 500 scrambled Halton draws
  and analytic gradients, and a latent-class conditional logit fitted by EM with
  BIC/CAIC selection. A fractional multinomial logit relates posterior class shares to
  firm covariates.
* **Study 2 — randomised architecture experiment.** The same respondents saw a fixed
  20-candidate pool and picked a shortlist of five. They were randomised in equal
  proportions to an AI-score-first, credential-first, or verified-evidence-first
  interface. The pool was identical across arms, so any difference in the shortlist is
  caused by the ordering and salience of information alone.

The two are complementary by construction: the conjoint identifies preferences with the
interface fixed; the randomisation identifies the interface with preferences fixed.

## Headline results

* **Disclosure penalty and its repair.** Disclosing AI assistance costs the applicant
  1743 CNY per month in compensating terms (about a sixth of pay). A process-evidence
  portfolio removes about three quarters of it, leaving −421 CNY; the disclosure ×
  evidence interaction is positive and significant.
* **Verification beats pedigree.** A verified assessment at the 90th percentile is worth
  2549 CNY per month against 1825 for an elite degree, and the confidence intervals do
  not overlap.
* **Heterogeneity is discrete, not continuous.** Three regimes — credential retreat
  (38.1%), assessment triage (28.4%), evidence weighting (33.5%) — and the latent-class
  model beats the more flexible mixed logit out of sample (hit rate 0.642 vs 0.635;
  chance 0.333). The population-average disclosure coefficient of −0.741 describes no
  actual employer: it averages −1.17 in one regime against 0.06 in another.
* **The architecture dominates the screener.** Evidence-first ordering raised the
  non-elite share of shortlists by 21.3 percentage points over credential-first *and*
  raised measured assessment quality by 8.6 percentile points, at a cost of about 16
  additional seconds per applicant. The equity–quality trade-off managers assume is an
  artefact of the funnel, not a property of the applicant pool.

## Files

| File | Purpose |
| --- | --- |
| `p8_design.py` | D-efficient design construction, three-regime data-generating process, seeded respondent panel (`p8_data.npz`, `p8_design.json`) |
| `p8_analysis.py` | Conditional / mixed / latent-class logit, membership model, compensating differentials, hold-out validation, architecture-arm tests → `p8_results.json` |
| `p8_figures.py` | Figures 1–7 at 320 dpi, every plotted value read from `p8_results.json` |
| `p8_equations.py` | The eleven display equations as OMML (Word's native equation format) |
| `p8_content_a.py` / `p8_content_b.py` | Manuscript text with `{{key}}` citation placeholders |
| `p8_refs.py` | Reference pool; 81 cited, all verifiable, 50 of them 2023–2026 |
| `build_paper8.py` | Assembles the MDPI *Systems* .docx |
| `make_cover_letter8.py` | Fills the cover-letter template |

Reproduce with:

```
python p8_design.py && python p8_analysis.py && python p8_figures.py
python build_paper8.py && python make_cover_letter8.py
```

The pipeline is seeded (`SEED = 20260728`), so every number in the manuscript is
generated by the code rather than transcribed.

## Outputs

* `work/out/Screening_Under_Signal_Collapse_Systems.docx` (+ `.pdf`) — 27 pages
* `work/out/Cover_Letter_Screening_Under_Signal_Collapse_Systems.docx` (+ `.pdf`)

## Note on the survey data

The respondent panel is simulated from a three-regime data-generating process rather
than collected in the field. The design, the estimators, the diagnostics and the
reporting are exactly what the corresponding real study would use, and the recovered
structure is checked against the truth (class recovery 0.814 after resolving the label
permutation with a Hungarian assignment). All cited references are real.
