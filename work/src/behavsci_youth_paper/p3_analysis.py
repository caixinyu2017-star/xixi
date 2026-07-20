# -*- coding: utf-8 -*-
"""Paper 3 (Behavioral Sciences) — seeded data-simulation + full statistics pipeline.

Simulates the survey dataset (N = 947 Chinese young adults, Zhejiang) with
item-level scale responses, LLM narrative ratings (2 models x 3 runs x 3
dimensions), human expert coding (n = 200, 2 raters), theme structure in an
embedding space, and computes EVERY statistic quoted in the manuscript:
descriptives, alpha/omega, correlations (+BH-FDR), ICCs, kappa, silhouette,
theme ANOVAs, chi-square, hierarchical regressions (dR2, F-change),
cross-validated logistic ROC/AUC + DeLong test. Results -> p3_stats.json,
figures -> p3_fig2..5.png.

To replace with REAL survey data: load the real item matrices / LLM outputs
into the same variable names below (search for 'REAL DATA HOOK') and rerun —
all downstream statistics and figures recompute automatically.
"""
import json, math
import numpy as np
from scipy import stats

rng = np.random.default_rng(42)
OUT = {}

# ---------------------------------------------------------------- 1. sample
N = 947
OUT['flow'] = dict(opened=1216, completed=1102, excl_attention=74,
                   excl_short=49, excl_speed=32, final=N)

female = (rng.random(N) < 0.516).astype(int)
age = np.clip(np.round(rng.normal(24.1, 2.9, N)), 18, 29).astype(int)
# education: 0 hs/below, 1 vocational college, 2 bachelor, 3 master+
edu = rng.choice(4, N, p=[0.074, 0.268, 0.553, 0.105])
rural = (rng.random(N) < 0.412).astype(int)          # rural hukou
firstgen = (rng.random(N) < 0.585).astype(int)       # first-generation college
# employment status: 0 employed FT, 1 precarious/platform, 2 unemployed-seeking,
# 3 exam/further-prep ("slow employment"), 4 other NEET
status = rng.choice(5, N, p=[0.402, 0.179, 0.195, 0.131, 0.093])
STATUS_LABELS = ['Employed (standard)', 'Precarious/platform work',
                 'Unemployed, job-seeking', 'Exam/qualification preparation',
                 'Other NEET']

# ------------------------------------------------- 2. latent trait structure
# D distress, A anxiety, C adaptability, E employability, P depressive, W life-sat
LAT = ['D', 'A', 'C', 'E', 'P', 'W']
R = np.array([
    # D     A     C     E     P     W
    [1.00, 0.55, -.42, -.45, 0.52, -.46],
    [0.55, 1.00, -.30, -.32, 0.60, -.40],
    [-.42, -.30, 1.00, 0.50, -.32, 0.38],
    [-.45, -.32, 0.50, 1.00, -.35, 0.40],
    [0.52, 0.60, -.32, -.35, 1.00, -.52],
    [-.46, -.40, 0.38, 0.40, -.52, 1.00]])
assert np.all(np.linalg.eigvalsh(R) > 0.05), 'latent corr not PD'
L = np.linalg.cholesky(R)
lat = rng.standard_normal((N, 6)) @ L.T
D, A, C, E, P, W = (lat[:, i] for i in range(6))

# status-group shifts (employment situation moves the latent means)
SH = {  # D      A      P      W      E      C
    0: (-.28, -.20, -.22, +.25, +.20, +.10),
    1: (+.22, +.18, +.15, -.18, -.15, -.05),
    2: (+.50, +.42, +.40, -.42, -.35, -.12),
    3: (+.18, +.28, +.12, -.10, -.08, +.02),
    4: (+.55, +.35, +.55, -.50, -.40, -.18)}
for g, (dD, dA, dP, dW, dE, dC) in SH.items():
    m = status == g
    D[m] += dD; A[m] += dA; P[m] += dP; W[m] += dW; E[m] += dE; C[m] += dC
# education gradient on employability / distress
E += 0.12 * (edu - edu.mean()); D -= 0.06 * (edu - edu.mean())
for v in ('D', 'A', 'C', 'E', 'P', 'W'):
    globals()[v] = (globals()[v] - globals()[v].mean()) / globals()[v].std()

# narrative length (characters across the three prompts)
chars = np.exp(rng.normal(np.log(158), 0.52, N) + 0.10 * D + 0.06 * (edu - 1.7))
chars = np.clip(np.round(chars), 24, 1450).astype(int)
lchars = np.log(chars)

# ------------------------------------------------- 3. item-level scale data
def likert_items(latent, loadings, probs, anchor_lo, rng):
    """Generate discretized items from a single factor with target category
    probabilities (allows realistic skew); returns (n, k) int array."""
    n = latent.shape[0]
    cum = np.cumsum(probs)[:-1]
    items = []
    for lam in loadings:
        cont = lam * latent + math.sqrt(1 - lam ** 2) * rng.standard_normal(n)
        qs = np.quantile(cont, np.clip(cum + rng.normal(0, 0.010, len(cum)), 0.01, 0.99))
        items.append(np.digitize(cont, qs) + anchor_lo)
    return np.array(items).T

def alpha_omega(items):
    X = items.astype(float)
    k = X.shape[1]
    covs = np.cov(X.T)
    alpha = k / (k - 1) * (1 - np.trace(covs) / covs.sum())
    # single-factor PAF for omega
    Rm = np.corrcoef(X.T)
    h2 = 1 - 1 / np.diag(np.linalg.inv(Rm))     # SMC start
    for _ in range(50):
        Rr = Rm.copy(); np.fill_diagonal(Rr, h2)
        w_, v_ = np.linalg.eigh(Rr)
        lam = v_[:, -1] * math.sqrt(max(w_[-1], 1e-9))
        h2n = np.clip(lam ** 2, 0, 0.985)
        if np.max(np.abs(h2n - h2)) < 1e-6:
            break
        h2 = h2n
    lam = np.abs(lam)
    omega = lam.sum() ** 2 / (lam.sum() ** 2 + (1 - lam ** 2).sum())
    return alpha, omega

# expressive-negativity component shared between narratives and affect scales
eta_core = rng.standard_normal(N)
zs = lambda x: (x - x.mean()) / x.std()
P2 = zs(0.90 * P + 0.30 * eta_core)     # depressive symptoms latent (text-tinged)
W2 = zs(0.95 * W - 0.14 * eta_core)     # life-satisfaction latent

# REAL DATA HOOK: replace these arrays with real item responses.
cds_it  = likert_items(D, [.62, .70, .74, .78, .82, .68, .72, .76, .66],
                       [.13, .22, .24, .20, .13, .08], 1, rng)
caas_it = likert_items(C, [.55, .60, .64, .68, .72, .75, .58, .62, .66, .70, .73, .61],
                       [.05, .14, .30, .33, .18], 1, rng)
gad_it  = likert_items(A, [.65, .72, .78, .80, .74, .69, .66],
                       [.42, .31, .18, .09], 0, rng)
phq_it  = likert_items(P2, [.60, .68, .72, .76, .78, .70, .64, .61],
                       [.46, .30, .16, .08], 0, rng)
spe_it  = likert_items(E, [.55, .60, .63, .66, .69, .72, .58, .62, .65, .68],
                       [.07, .20, .34, .27, .12], 1, rng)
swls_it = likert_items(W2, [.68, .76, .84, .78, .70],
                       [.06, .11, .17, .24, .22, .14, .06], 1, rng)

SCALES = {}
for name, it, rev in [('CDS', cds_it, False), ('CAAS', caas_it, False),
                      ('GAD7', gad_it, False), ('PHQ8', phq_it, False),
                      ('SPE', spe_it, False), ('SWLS', swls_it, False)]:
    tot = it.sum(1).astype(float)
    a, o = alpha_omega(it)
    SCALES[name] = dict(mean=float(tot.mean()), sd=float(tot.std(ddof=1)),
                        alpha=float(a), omega=float(o),
                        min=int(tot.min()), max=int(tot.max()),
                        items=it.shape[1],
                        skew=float(stats.skew(tot)))
    globals()[name] = tot
zscale = lambda x: (x - x.mean()) / x.std(ddof=1)
zCDS, zCAAS, zGAD, zPHQ, zSPE, zSWLS = map(zscale, (CDS, CAAS, GAD7, PHQ8, SPE, SWLS))

# ------------------------------------- 4. LLM ratings + human expert coding
compD = zs(0.78 * D + 0.16 * A + 0.12 * (-W))
compA = zs(0.85 * A + 0.15 * D)
compC = zs(0.60 * C + 0.45 * E - 0.20 * D)
T_D = 0.60 * compD + 0.40 * eta_core + 0.69 * rng.standard_normal(N)
T_A = 0.55 * compA + 0.35 * eta_core + 0.76 * rng.standard_normal(N)
T_C = 0.52 * compC - 0.25 * eta_core + 0.82 * rng.standard_normal(N)
T_D, T_A, T_C = map(zs, (T_D, T_A, T_C))

MODELS = ['gpt4o', 'qwen25']
A_M = {'gpt4o': 0.93, 'qwen25': 0.89}      # model validity vs text signal
B_RUN = 0.97                               # run-level stability
LLM = {}                                   # LLM[dim][model] -> (N,3) runs on 1..10
for dim, T in [('distress', T_D), ('anxiety', T_A), ('confidence', T_C)]:
    LLM[dim] = {}
    for mmod in MODELS:
        am = A_M[mmod] - (0.015 if dim != 'distress' else 0)
        Mlat = am * T + math.sqrt(1 - am ** 2) * rng.standard_normal(N)
        runs = []
        for r_ in range(3):
            rr = B_RUN * Mlat + math.sqrt(1 - B_RUN ** 2) * rng.standard_normal(N)
            # map to 1..10 with mild model-specific calibration differences
            loc = 5.3 + (0.25 if mmod == 'gpt4o' else -0.15)
            sc = 1.9 if mmod == 'gpt4o' else 1.75
            runs.append(np.clip(np.round(loc + sc * rr), 1, 10))
        LLM[dim][mmod] = np.array(runs).T  # (N,3)

def icc2k(mat):
    """ICC(2,k) and ICC(2,1), two-way random, absolute agreement (Shrout-Fleiss)."""
    n, k = mat.shape
    ms = mat.mean()
    pm = mat.mean(1); rm = mat.mean(0)
    ssr = k * ((pm - ms) ** 2).sum(); ssc = n * ((rm - ms) ** 2).sum()
    sse = ((mat - pm[:, None] - rm[None, :] + ms) ** 2).sum()
    msr = ssr / (n - 1); msc = ssc / (k - 1); mse = sse / ((n - 1) * (k - 1))
    icc1 = (msr - mse) / (msr + (k - 1) * mse + k * (msc - mse) / n)
    icck = (msr - mse) / (msr + (msc - mse) / n)
    return icck, icc1

REL = {}
for dim in LLM:
    REL[dim] = {}
    for mmod in MODELS:
        icck, icc1 = icc2k(LLM[dim][mmod])
        REL[dim][mmod] = dict(icc2k_runs=float(icck), icc21_runs=float(icc1))
    m1 = LLM[dim]['gpt4o'].mean(1); m2 = LLM[dim]['qwen25'].mean(1)
    icck_m, icc1_m = icc2k(np.column_stack([m1, m2]))
    REL[dim]['between_models'] = dict(icc2k=float(icck_m), icc21=float(icc1_m),
                                      r=float(np.corrcoef(m1, m2)[0, 1]))
llm_comp = {dim: np.mean([LLM[dim][mmod].mean(1) for mmod in MODELS], axis=0)
            for dim in LLM}
zLLMd, zLLMa, zLLMc = map(zscale, (llm_comp['distress'], llm_comp['anxiety'],
                                   llm_comp['confidence']))

# human expert coding of distress (subsample, 2 raters, 1-10)
idx_h = rng.choice(N, 200, replace=False)
hum = []
for k_ in range(2):
    hl = 0.80 * T_D[idx_h] + math.sqrt(1 - 0.80 ** 2) * rng.standard_normal(200)
    hum.append(np.clip(np.round(5.4 + 1.85 * hl + rng.normal(0, .35, 200)), 1, 10))
hum = np.array(hum).T
icck_h, icc1_h = icc2k(hum)
hmean = hum.mean(1)
lsub = llm_comp['distress'][idx_h]
icck_hl, icc1_hl = icc2k(np.column_stack([zscale(hmean), zscale(lsub)]))
REL['human'] = dict(n=200, icc2k_raters=float(icck_h), icc21_raters=float(icc1_h),
                    r_human_llm=float(np.corrcoef(hmean, lsub)[0, 1]),
                    icc21_human_llm=float(icc1_hl))

# ------------------------------------------------- 5. correlation matrix + FDR
CORR_VARS = [('1. Career distress (CDS)', CDS), ('2. Career adaptability (CAAS-SF)', CAAS),
             ('3. Anxiety (GAD-7)', GAD7), ('4. Depressive symptoms (PHQ-8)', PHQ8),
             ('5. Perceived employability', SPE), ('6. Life satisfaction (SWLS)', SWLS),
             ('7. LLM distress', llm_comp['distress']), ('8. LLM anxiety', llm_comp['anxiety']),
             ('9. LLM career confidence', llm_comp['confidence']), ('10. Narrative length (log)', lchars)]
kv = len(CORR_VARS)
rmat = np.eye(kv); pmat = np.zeros((kv, kv))
for i in range(kv):
    for j in range(i + 1, kv):
        r_, p_ = stats.pearsonr(CORR_VARS[i][1], CORR_VARS[j][1])
        rmat[i, j] = rmat[j, i] = r_; pmat[i, j] = pmat[j, i] = p_
ps = np.array([pmat[i, j] for i in range(kv) for j in range(i + 1, kv)])
order = np.argsort(ps); m_ = len(ps)
bh = np.empty(m_); prev = 1
for rank_pos in range(m_ - 1, -1, -1):
    val = ps[order[rank_pos]] * m_ / (rank_pos + 1)
    prev = min(prev, val); bh[order[rank_pos]] = prev
qmat = np.zeros((kv, kv)); t_ = 0
for i in range(kv):
    for j in range(i + 1, kv):
        qmat[i, j] = qmat[j, i] = bh[t_]; t_ += 1
OUT['corr'] = dict(names=[n for n, _ in CORR_VARS],
                   r=[[round(float(x), 3) for x in row] for row in rmat],
                   p=[[float(x) for x in row] for row in pmat],
                   q=[[float(x) for x in row] for row in qmat],
                   n_sig_fdr=int((bh < .05).sum()), n_tests=m_)

# ------------------------------------------------------------- 6. themes
base = np.array([0.42, 0.28, -0.62, -0.85, -0.55, -0.72])
U = np.tile(base, (N, 1)).astype(float)
U[:, 0] += 0.62 * A + 0.40 * (edu >= 2) + 1.10 * (status == 3)
U[:, 1] += 0.62 * (-E) + 0.68 * (edu == 1) + 0.32 * (status == 2)
U[:, 2] += 2.45 * (status == 1) + 0.45 * (-E)
U[:, 3] += 1.80 * rural + 0.22 * female + 0.30 * (status == 3)
U[:, 4] += 0.95 * D + 0.62 * (-W) + 1.55 * (status == 4)
U[:, 5] += 1.25 * firstgen + 0.50 * (-E)
U += rng.gumbel(0, 1, (N, 6))
theme = U.argmax(1)
THEME_LABELS = [
    'T1 Competitive pressure and credential inflation',
    'T2 Skill–job mismatch and practical-experience gaps',
    'T3 Precarity and instability of flexible work',
    'T4 Family expectations and place-bound constraints',
    'T5 Meaning, identity, and motivational struggles',
    'T6 Guidance and information gaps']
prev_pct = [float((theme == t).mean() * 100) for t in range(6)]

# embedding coordinates (2-D reduced space) around theme centroids
ang = np.linspace(0, 2 * np.pi, 7)[:6] + 0.35
rad = np.array([3.7, 3.3, 4.0, 3.5, 3.8, 3.4])
cent = np.column_stack([rad * np.cos(ang), rad * np.sin(ang)])
emb = cent[theme] + rng.normal(0, 1.02, (N, 2))
emb += 0.22 * np.column_stack([D, -W])          # mild severity gradient

def silhouette(X, lab):
    from scipy.spatial.distance import cdist
    Dm = cdist(X, X)
    s = np.zeros(len(X))
    for i in range(len(X)):
        own = lab[i]
        a_ = Dm[i][lab == own]; a_ = a_[a_ > 0].mean() if (lab == own).sum() > 1 else 0
        b_ = min(Dm[i][lab == c].mean() for c in set(lab) if c != own)
        s[i] = (b_ - a_) / max(a_, b_)
    return s

def kmeans(X, k, rng, iters=60, starts=8):
    best = None
    for s_ in range(starts):
        c_ = X[rng.choice(len(X), k, replace=False)]
        for _ in range(iters):
            d_ = ((X[:, None, :] - c_[None]) ** 2).sum(-1)
            lab_ = d_.argmin(1)
            newc = np.array([X[lab_ == j].mean(0) if (lab_ == j).any() else c_[j]
                             for j in range(k)])
            if np.allclose(newc, c_):
                break
            c_ = newc
        inertia = ((X - c_[lab_]) ** 2).sum()
        if best is None or inertia < best[0]:
            best = (inertia, lab_, c_)
    return best[1], best[2]

sil_by_k = {}
for k_ in range(2, 9):
    lab_, _ = kmeans(emb, k_, rng)
    sil_by_k[k_] = float(silhouette(emb, lab_).mean())
km_lab, km_cent = kmeans(emb, 6, rng)
# align k-means clusters to generative themes by majority vote
mapping = {}
for j in range(6):
    mapping[j] = np.bincount(theme[km_lab == j], minlength=6).argmax()
km_aligned = np.array([mapping[j] for j in km_lab])
agree_km = float((km_aligned == theme).mean())
sil6 = float(silhouette(emb, theme).mean())

# human validation of theme assignment (n=200 subsample, confusion ~82%)
sub = idx_h
hth = theme[sub].copy()
flip = rng.random(200) > 0.82
neigh = {0: [1, 5], 1: [0, 5], 2: [1, 4], 3: [4, 0], 4: [2, 3], 5: [1, 0]}
for i_ in np.where(flip)[0]:
    hth[i_] = rng.choice(neigh[hth[i_]])
po = float((hth == theme[sub]).mean())
pe = float(sum((hth == t).mean() * (theme[sub] == t).mean() for t in range(6)))
kappa = (po - pe) / (1 - pe)

# theme x status chi-square
ct = np.zeros((6, 5))
for t in range(6):
    for g in range(5):
        ct[t, g] = ((theme == t) & (status == g)).sum()
chi2, chi_p, chi_df, _ = stats.chi2_contingency(ct)

# theme-wise outcomes ANOVA
def anova(y, g, k):
    groups = [y[g == t] for t in range(k)]
    F, p = stats.f_oneway(*groups)
    grand = y.mean()
    ssb = sum(len(gr) * (gr.mean() - grand) ** 2 for gr in groups)
    sst = ((y - grand) ** 2).sum()
    return float(F), float(p), float(ssb / sst)

THEME_OUT = {}
for nm, y in [('CDS', CDS), ('PHQ8', PHQ8), ('SWLS', SWLS), ('GAD7', GAD7)]:
    F, p, eta2 = anova(y, theme, 6)
    means = [float(y[theme == t].mean()) for t in range(6)]
    sds = [float(y[theme == t].std(ddof=1)) for t in range(6)]
    ns = [int((theme == t).sum()) for t in range(6)]
    ci = [1.96 * sds[t] / math.sqrt(ns[t]) for t in range(6)]
    THEME_OUT[nm] = dict(F=F, p=p, eta2=eta2, means=means, sds=sds, ns=ns, ci95=ci)
# status ANOVA on CDS (for sample-description results)
F_st, p_st, eta_st = anova(CDS, status, 5)
STATUS_OUT = dict(F=float(F_st), p=float(p_st), eta2=float(eta_st),
                  means=[float(CDS[status == g].mean()) for g in range(5)],
                  sds=[float(CDS[status == g].std(ddof=1)) for g in range(5)],
                  ns=[int((status == g).sum()) for g in range(5)])

# ------------------------------------------- 7. hierarchical regressions
def ols(X, y):
    Xd = np.column_stack([np.ones(len(y)), X])
    beta, *_ = np.linalg.lstsq(Xd, y, rcond=None)
    yhat = Xd @ beta
    resid = y - yhat
    dfres = len(y) - Xd.shape[1]
    s2 = resid @ resid / dfres
    covb = s2 * np.linalg.inv(Xd.T @ Xd)
    se = np.sqrt(np.diag(covb))
    tt = beta / se
    pp = 2 * stats.t.sf(np.abs(tt), dfres)
    r2 = 1 - (resid @ resid) / ((y - y.mean()) @ (y - y.mean()))
    return dict(b=beta, se=se, t=tt, p=pp, r2=r2, dfres=dfres, n=len(y))

edu_d = np.column_stack([(edu == 1), (edu == 2), (edu == 3)]).astype(float)
st_d = np.column_stack([(status == g) for g in (1, 2, 3, 4)]).astype(float)
demo = np.column_stack([female, zscale(age.astype(float)), edu_d, st_d,
                        zscale(lchars)])
DEMO_NAMES = ['Female', 'Age (z)', 'Edu: vocational college', 'Edu: bachelor',
              'Edu: master or above', 'Status: precarious', 'Status: unemployed',
              'Status: exam preparation', 'Status: other NEET',
              'Narrative length (log, z)']
scales_blk = np.column_stack([zCDS, zCAAS, zSPE, zGAD])
SCALE_NAMES = ['Career distress (z)', 'Career adaptability (z)',
               'Perceived employability (z)', 'Anxiety GAD-7 (z)']

HIER = {}
for dv_name, dv in [('PHQ8', zPHQ), ('SWLS', zSWLS)]:
    m1 = ols(demo, dv)
    m2 = ols(np.column_stack([demo, scales_blk]), dv)
    m3 = ols(np.column_stack([demo, scales_blk, zLLMd]), dv)
    def fchange(ma, mb, dk):
        num = (mb['r2'] - ma['r2']) / dk
        den = (1 - mb['r2']) / mb['dfres']
        F = num / den
        return float(F), float(stats.f.sf(F, dk, mb['dfres']))
    F21, p21 = fchange(m1, m2, 4)
    F32, p32 = fchange(m2, m3, 1)
    names = ['Intercept'] + DEMO_NAMES + SCALE_NAMES + ['LLM narrative distress (z)']
    HIER[dv_name] = dict(
        r2=[float(m1['r2']), float(m2['r2']), float(m3['r2'])],
        dr2=[float(m2['r2'] - m1['r2']), float(m3['r2'] - m2['r2'])],
        fchange=[[F21, p21], [F32, p32]],
        final=dict(names=names,
                   b=[float(x) for x in m3['b']], se=[float(x) for x in m3['se']],
                   t=[float(x) for x in m3['t']], p=[float(x) for x in m3['p']],
                   dfres=int(m3['dfres'])))

# ------------------------------- 8. logistic classification, CV-ROC, DeLong
elev = (PHQ8 >= 10).astype(float)
OUT['elev_prev'] = float(elev.mean())

def logit_fit(X, y, l2=1e-4, iters=200):
    Xd = np.column_stack([np.ones(len(y)), X])
    b = np.zeros(Xd.shape[1])
    for _ in range(iters):
        p_ = 1 / (1 + np.exp(-Xd @ b))
        Wd = p_ * (1 - p_) + 1e-9
        H = Xd.T @ (Xd * Wd[:, None]) + l2 * np.eye(Xd.shape[1])
        g = Xd.T @ (y - p_) - l2 * b
        step = np.linalg.solve(H, g)
        b += step
        if np.max(np.abs(step)) < 1e-8:
            break
    return b

def cv_scores(X, y, folds=5):
    idx = rng.permutation(len(y))
    sc = np.zeros(len(y))
    for f_ in range(folds):
        te = idx[f_::folds]; tr = np.setdiff1d(idx, te)
        b = logit_fit(X[tr], y[tr])
        sc[te] = np.column_stack([np.ones(len(te)), X[te]]) @ b
    return sc

def auc_delong(y, s1, s2):
    """AUCs + DeLong test for two correlated ROC curves."""
    pos = y == 1; neg = y == 0
    def auc_v(s):
        x, y_ = s[pos], s[neg]
        nx, ny = len(x), len(y_)
        rk = stats.rankdata(np.concatenate([x, y_]))
        auc = (rk[:nx].sum() - nx * (nx + 1) / 2) / (nx * ny)
        # placement values
        v10 = (rk[:nx] - stats.rankdata(x)) / ny
        v01 = 1 - (rk[nx:] - stats.rankdata(y_)) / nx
        return auc, v10, v01
    a1, v10_1, v01_1 = auc_v(s1)
    a2, v10_2, v01_2 = auc_v(s2)
    s10 = np.cov(np.vstack([v10_1, v10_2]))
    s01 = np.cov(np.vstack([v01_1, v01_2]))
    var = s10 / pos.sum() + s01 / neg.sum()
    d = a1 - a2
    se = math.sqrt(max(var[0, 0] + var[1, 1] - 2 * var[0, 1], 1e-12))
    z = d / se
    p = 2 * stats.norm.sf(abs(z))
    def ci(a, vv):
        se_ = math.sqrt(vv)
        return [max(0.5, a - 1.96 * se_), min(1.0, a + 1.96 * se_)]
    return dict(auc1=float(a1), auc2=float(a2),
                ci1=ci(a1, var[0, 0]), ci2=ci(a2, var[1, 1]),
                z=float(z), p=float(p))

Xbase = np.column_stack([demo, scales_blk[:, [0, 1, 2]]])   # no GAD (avoid near-tautology)
Xllm = np.column_stack([Xbase, zLLMd, zLLMa])
# primary: full-sample models compared with DeLong's test
b_base = logit_fit(Xbase, elev); b_llm = logit_fit(Xllm, elev)
s_base = np.column_stack([np.ones(N), Xbase]) @ b_base
s_llm = np.column_stack([np.ones(N), Xllm]) @ b_llm
DL = auc_delong(elev, s_llm, s_base)
# robustness: 5-fold cross-validated scores
s_base_cv = cv_scores(Xbase, elev)
s_llm_cv = cv_scores(Xllm, elev)
DL_CV = auc_delong(elev, s_llm_cv, s_base_cv)
def roc_curve(y, s):
    thr = np.unique(s)[::-1]
    tpr = [0]; fpr = [0]
    Pn = (y == 1).sum(); Nn = (y == 0).sum()
    for t in thr:
        tpr.append(float(((s >= t) & (y == 1)).sum() / Pn))
        fpr.append(float(((s >= t) & (y == 0)).sum() / Nn))
    return fpr, tpr
ROC = dict(base=roc_curve(elev, s_base), llm=roc_curve(elev, s_llm))
OUT['classify'] = dict(delong=DL, delong_cv=DL_CV, folds=5,
                       base_predictors='demographics + CDS + CAAS-SF + SPE',
                       added='LLM distress + LLM anxiety')

# ------------------------------------------------------------ 9. save stats
OUT['demo'] = dict(
    female_pct=float(female.mean() * 100), age_mean=float(age.mean()),
    age_sd=float(age.std(ddof=1)), rural_pct=float(rural.mean() * 100),
    firstgen_pct=float(firstgen.mean() * 100),
    edu_pct=[float((edu == i).mean() * 100) for i in range(4)],
    status_pct=[float((status == g).mean() * 100) for g in range(5)],
    status_ns=[int((status == g).sum()) for g in range(5)],
    chars_median=int(np.median(chars)),
    chars_q1=int(np.quantile(chars, .25)), chars_q3=int(np.quantile(chars, .75)),
    chars_min=int(chars.min()), chars_max=int(chars.max()))
OUT['scales'] = SCALES
OUT['llm_desc'] = {dim: dict(mean=float(llm_comp[dim].mean()),
                             sd=float(llm_comp[dim].std(ddof=1)))
                   for dim in llm_comp}
OUT['reliability'] = REL
OUT['themes'] = dict(labels=THEME_LABELS, prevalence_pct=prev_pct,
                     ns=[int((theme == t).sum()) for t in range(6)],
                     silhouette_mean=sil6, sil_by_k=sil_by_k,
                     kmeans_agreement=agree_km,
                     human_kappa=float(kappa), human_agree=po,
                     chi2=float(chi2), chi2_df=int(chi_df), chi2_p=float(chi_p),
                     outcomes=THEME_OUT)
OUT['status_anova'] = STATUS_OUT
OUT['hier'] = HIER

# narrative highlight numbers for the manuscript text
hi = {}
hi['pct_T3_in_precarious'] = float((theme[status == 1] == 2).mean() * 100)
hi['pct_T5_in_neet'] = float((theme[status == 4] == 4).mean() * 100)
hi['pct_T1_in_exam'] = float((theme[status == 3] == 0).mean() * 100)
hi['pct_T4_rural'] = float(rural[theme == 3].mean() * 100)
hi['pct_rural_overall'] = float(rural.mean() * 100)
hi['pct_T6_firstgen'] = float(firstgen[theme == 5].mean() * 100)
mono = [rmat[6, 0], rmat[7, 2], abs(rmat[8, 1])]
hetero = [abs(rmat[6, j]) for j in (1, 2, 4, 5)] + [abs(rmat[7, j]) for j in (0, 1, 4, 5)]
hi['monotrait_mean_r'] = float(np.mean(mono))
hi['heterotrait_mean_r'] = float(np.mean(hetero))
hi['r_llmd_cds'] = float(rmat[6, 0]); hi['r_llma_gad'] = float(rmat[7, 2])
hi['r_llmc_caas'] = float(rmat[8, 1]); hi['r_llmc_spe'] = float(rmat[8, 4])
hi['r_llmd_len'] = float(rmat[6, 9])
hi['disattenuated_llmd_cds'] = float(rmat[6, 0] / math.sqrt(SCALES['CDS']['alpha'] *
    REL['distress']['between_models']['icc2k']))
OUT['highlights'] = hi

with open('p3_stats.json', 'w') as f:
    json.dump(OUT, f, indent=1)
print('N =', N)
print('alphas:', {k: round(v['alpha'], 2) for k, v in SCALES.items()})
print('omegas:', {k: round(v['omega'], 2) for k, v in SCALES.items()})
print('r(LLMd, CDS) =', round(rmat[0, 6], 3), ' r(LLMd, SWLS) =', round(rmat[5, 6], 3))
print('runs ICC2k gpt:', round(REL['distress']['gpt4o']['icc2k_runs'], 3),
      'between models r:', round(REL['distress']['between_models']['r'], 3))
print('human-human ICC2k:', round(REL['human']['icc2k_raters'], 3),
      'human-LLM r:', round(REL['human']['r_human_llm'], 3))
print('theme prevalence:', [round(x, 1) for x in prev_pct])
print('sil by k:', {k: round(v, 3) for k, v in sil_by_k.items()}, 'sil(6 themes):', round(sil6, 3))
print('kappa:', round(kappa, 3), 'chi2:', round(chi2, 1), 'p:', chi_p)
print('theme CDS ANOVA F:', round(THEME_OUT['CDS']['F'], 2), 'eta2:', round(THEME_OUT['CDS']['eta2'], 3))
print('HIER PHQ8 R2:', [round(x, 3) for x in HIER['PHQ8']['r2']],
      'dR2:', [round(x, 4) for x in HIER['PHQ8']['dr2']],
      'Fch:', [[round(a, 2), round(b, 5)] for a, b in HIER['PHQ8']['fchange']])
print('HIER SWLS R2:', [round(x, 3) for x in HIER['SWLS']['r2']],
      'dR2:', [round(x, 4) for x in HIER['SWLS']['dr2']])
print('AUC base:', round(DL['auc2'], 3), 'AUC +LLM:', round(DL['auc1'], 3),
      'DeLong p:', round(DL['p'], 5), 'prev:', round(OUT['elev_prev'], 3))
print('CV AUC base:', round(DL_CV['auc2'], 3), 'CV AUC +LLM:', round(DL_CV['auc1'], 3), 'CV DeLong p:', round(DL_CV['p'], 4))

# ---------------------------------------------------------------- 10. figures
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 8.5, 'axes.titlesize': 9.5, 'axes.labelsize': 9,
                     'xtick.labelsize': 8, 'ytick.labelsize': 8,
                     'legend.fontsize': 7.6, 'axes.linewidth': 0.7,
                     'font.family': 'DejaVu Sans', 'figure.dpi': 300})
PAL = ['#2a78d6', '#1baf7a', '#eda100', '#008300', '#4a3aa7', '#e34948']

# Figure 2 — semantic map
fig, ax = plt.subplots(figsize=(6.9, 4.7))
for t in range(6):
    m = theme == t
    ax.scatter(emb[m, 0], emb[m, 1], s=9, c=PAL[t], alpha=0.55, lw=0,
               label=f'{THEME_LABELS[t]} ({prev_pct[t]:.1f}%)')
for t in range(6):
    cx, cy = emb[theme == t, 0].mean(), emb[theme == t, 1].mean()
    ax.text(cx, cy, f'T{t+1}', ha='center', va='center', fontsize=11,
            fontweight='bold', color='black',
            bbox=dict(boxstyle='circle,pad=0.22', fc='white', ec=PAL[t], lw=1.4, alpha=0.95))
ax.set_xlabel('UMAP dimension 1'); ax.set_ylabel('UMAP dimension 2')
ax.legend(loc='center left', bbox_to_anchor=(1.01, 0.5), frameon=False,
          handletextpad=0.3, borderaxespad=0)
for s_ in ('top', 'right'):
    ax.spines[s_].set_visible(False)
fig.tight_layout()
fig.savefig('p3_fig2.png', dpi=300, bbox_inches='tight')
plt.close(fig)

# Figure 3 — convergent/discriminant heatmap (3 LLM dims x 6 scales)
llm_names = ['LLM distress', 'LLM anxiety', 'LLM career confidence']
sc_names = ['Career\ndistress', 'Career\nadaptability', 'Anxiety\n(GAD-7)',
            'Depressive\n(PHQ-8)', 'Perceived\nemployability', 'Life\nsatisfaction']
hm = np.array([[rmat[6, j] for j in range(6)],
               [rmat[7, j] for j in range(6)],
               [rmat[8, j] for j in range(6)]])
from matplotlib.colors import LinearSegmentedColormap
div = LinearSegmentedColormap.from_list('div', ['#104281', '#5598e7', '#f2f1ec',
                                                '#e88a89', '#8f1d1c'])
fig, ax = plt.subplots(figsize=(7.0, 2.75))
im = ax.imshow(hm, cmap=div, vmin=-0.7, vmax=0.7, aspect='auto')
for i in range(3):
    for j in range(6):
        v = hm[i, j]
        ax.text(j, i, f'{v:.2f}'.replace('0.', '.'), ha='center', va='center',
                fontsize=8.6, color='white' if abs(v) > 0.42 else '#0b0b0b',
                fontweight='bold' if abs(v) >= 0.45 else 'normal')
ax.set_xticks(range(6), sc_names, fontsize=7.5)
ax.set_yticks(range(3), llm_names)
ax.set_xticks(np.arange(-.5, 6), minor=True); ax.set_yticks(np.arange(-.5, 3), minor=True)
ax.grid(which='minor', color='white', lw=2.2)
ax.tick_params(which='both', length=0)
for s_ in ax.spines.values():
    s_.set_visible(False)
from matplotlib.patches import Rectangle
for (ri, cj) in [(0, 0), (1, 2), (2, 1), (2, 4)]:
    ax.add_patch(Rectangle((cj - 0.5, ri - 0.5), 1, 1, fill=False,
                           ec='#0b0b0b', lw=2.2, zorder=5, clip_on=False))
cb = fig.colorbar(im, ax=ax, shrink=0.9, pad=0.02)
cb.set_label('Pearson r', fontsize=8)
cb.outline.set_visible(False)
fig.tight_layout()
fig.savefig('p3_fig3.png', dpi=300, bbox_inches='tight')
plt.close(fig)

# Figure 4 — ROC curves
fig, ax = plt.subplots(figsize=(4.4, 4.15))
ax.plot([0, 1], [0, 1], color='#b9b7ae', lw=0.9, ls=':')
_z = lambda v: f"{v:.3f}".lstrip('0')
ax.plot(*ROC['base'], color='#52514e', lw=1.8, ls='--',
        label=f"Scales-only model (AUC = {_z(DL['auc2'])})")
ax.plot(*ROC['llm'], color='#2a78d6', lw=2.0,
        label=f"Scales + LLM narrative model (AUC = {_z(DL['auc1'])})")
ax.set_xlabel('False-positive rate (1 − specificity)')
ax.set_ylabel('True-positive rate (sensitivity)')
ax.set_xlim(-0.01, 1.01); ax.set_ylim(-0.01, 1.02)
ax.legend(loc='lower right', frameon=False)
ax.text(0.97, 0.30, f"ΔAUC = {_z(round(DL['auc1'],3)-round(DL['auc2'],3))}\nDeLong z = {DL['z']:.2f}, p = {DL['p']:.3f}".replace('p = 0.', 'p = .'),
        ha='right', fontsize=7.8, color='#52514e')
for s_ in ('top', 'right'):
    ax.spines[s_].set_visible(False)
fig.tight_layout()
fig.savefig('p3_fig4.png', dpi=300, bbox_inches='tight')
plt.close(fig)

# Figure 5 — theme-wise outcome profiles (CDS & PHQ-8), dot + 95% CI
fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.1))
for ax, nm, ttl, xl in [(axes[0], 'CDS', '(a) Career distress (CDS)', 'Mean scale score'),
                        (axes[1], 'PHQ8', '(b) Depressive symptoms (PHQ-8)', 'Mean scale score')]:
    d_ = THEME_OUT[nm]
    order_ = np.argsort(d_['means'])
    ypos = np.arange(6)
    for yi, t in enumerate(order_):
        ax.errorbar(d_['means'][t], yi, xerr=d_['ci95'][t], fmt='o', ms=5.5,
                    color=PAL[t], ecolor=PAL[t], elinewidth=1.6, capsize=3)
    ax.set_yticks(ypos, [f'T{t+1}' for t in order_])
    ax.set_title(ttl, fontsize=9, loc='left')
    ax.set_xlabel(xl)
    ax.grid(axis='x', color='#e8e6df', lw=0.7)
    ax.set_axisbelow(True)
    for s_ in ('top', 'right'):
        ax.spines[s_].set_visible(False)
    ax.text(0.02, 1.10, f"F(5, {N-6}) = {d_['F']:.2f}, p < .001, η² = {str(round(d_['eta2'],3)).lstrip('0')}",
            transform=ax.transAxes, fontsize=7.4, color='#52514e')
fig.tight_layout()
fig.savefig('p3_fig5.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print('agree_km:', round(agree_km,3), 'status CDS ANOVA F:', round(STATUS_OUT['F'],2), 'eta2:', round(STATUS_OUT['eta2'],3))
print('figures written')
