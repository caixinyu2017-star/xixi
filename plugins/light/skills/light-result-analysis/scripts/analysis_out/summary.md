# Result Analysis: `_synth_results.csv`

- Group column: **method**  |  rows: 24  |  alpha=0.05
- Metrics: acc, f1

## Metric: `acc`

| group | n | mean | std | 95% CI | normal |
|---|---|---|---|---|---|
| ours | 8 | 0.8539 | 0.0142 | [0.8420, 0.8657] | Y |
| ablation | 8 | 0.8375 | 0.0283 | [0.8138, 0.8611] | Y |
| baseline | 8 | 0.7895 | 0.0281 | [0.7660, 0.8130] | Y |

**Omnibus test**: anova_oneway -> p = 8.903e-05 (significant). normality: all normal.

Tukey HSD post-hoc:

| g1 | g2 | meandiff | p_adj | reject |
|---|---|---|---|---|
| ablation | baseline | -0.0480 | 0.0021 | True |
| ablation | ours | 0.0164 | 0.3877 | False |
| baseline | ours | 0.0644 | 0.0001 | True |

**Pairwise (Cohen's d + BH-FDR):**

| g1 | g2 | test | p | q(FDR) | sig | d | effect | mean_diff [CI] |
|---|---|---|---|---|---|---|---|---|
| ablation | baseline | welch_t | 0.004259 | 0.006388 | Y | 1.610 | large | 0.0480 [0.0178, 0.0782] |
| ablation | ours | welch_t | 0.1721 | 0.1721 | n | -0.694 | medium | -0.0164 [-0.0412, 0.0084] |
| baseline | ours | welch_t | 0.0001538 | 0.0004614 | Y | -2.736 | large | -0.0644 [-0.0890, -0.0397] |

_Top group by mean: **ours** (0.8539)._

## Metric: `f1`

| group | n | mean | std | 95% CI | normal |
|---|---|---|---|---|---|
| ours | 8 | 0.8318 | 0.0126 | [0.8213, 0.8423] | Y |
| ablation | 8 | 0.8097 | 0.0270 | [0.7872, 0.8323] | Y |
| baseline | 8 | 0.7706 | 0.0249 | [0.7498, 0.7914] | Y |

**Omnibus test**: anova_oneway -> p = 7.871e-05 (significant). normality: all normal.

Tukey HSD post-hoc:

| g1 | g2 | meandiff | p_adj | reject |
|---|---|---|---|---|
| ablation | baseline | -0.0391 | 0.0059 | True |
| ablation | ours | 0.0221 | 0.1437 | False |
| baseline | ours | 0.0612 | 0.0001 | True |

**Pairwise (Cohen's d + BH-FDR):**

| g1 | g2 | test | p | q(FDR) | sig | d | effect | mean_diff [CI] |
|---|---|---|---|---|---|---|---|---|
| ablation | baseline | welch_t | 0.00932 | 0.01398 | Y | 1.425 | large | 0.0391 [0.0113, 0.0669] |
| ablation | ours | welch_t | 0.0623 | 0.0623 | n | -0.993 | large | -0.0221 [-0.0455, 0.0014] |
| baseline | ours | welch_t | 8.637e-05 | 0.0002591 | Y | -2.934 | large | -0.0612 [-0.0831, -0.0393] |

_Top group by mean: **ours** (0.8318)._


---
_Tests auto-selected by Shapiro normality and group count. Effect sizes are Hedges'-corrected Cohen's d. p-values BH-FDR corrected per metric. See significance_test.py for the verified primitives._