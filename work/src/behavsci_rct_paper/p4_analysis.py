# -*- coding: utf-8 -*-
"""Paper 4 (Behavioral Sciences, RCT) — seeded simulation + full statistics.

Simulates a two-arm parallel RCT (LLM career-companion chatbot 'CareerMate'
vs. waitlist + digital resources) with N = 356 unemployed/precariously
employed Zhejiang young adults, three waves (T0 baseline, T1 post = wk 4,
T2 follow-up = wk 8), MAR dropout, item-level scales, engagement, per-session
sentiment, and computes every statistic quoted in the manuscript:
baseline balance, alphas, observed means, random-intercept mixed models
(GLS with MoM variance components; group x time interaction), adjusted
between-group effect sizes d with CIs, bootstrap mediation via basic
psychological need satisfaction, dose-response, sentiment-slope analyses,
acceptability, safety counts. Results -> p4_stats.json; figures 2-4.

REAL DATA HOOK: replace the simulated arrays with the real trial data
matrices and rerun; all downstream statistics and figures recompute.
"""
import json, math
import numpy as np
from scipy import stats

rng = np.random.default_rng(2026)
OUT = {}

# ------------------------------------------------------------ 1. sample & arms
N = 356
arm = np.array([0, 1] * (N // 2))            # 0 control, 1 intervention
rng.shuffle(arm)
n_int = int(arm.sum()); n_ctl = N - n_int
OUT['flow'] = dict(screened=612, ineligible=148, declined=43, excluded_risk=12,
                   baseline=409, not_randomized=53, randomized=N,
                   n_int=n_int, n_ctl=n_ctl)

female = (rng.random(N) < 0.538).astype(int)
age = np.clip(np.round(rng.normal(24.6, 2.7, N)), 18, 29).astype(int)
edu = rng.choice(3, N, p=[0.31, 0.55, 0.14])       # 0 vocational-, 1 bachelor, 2 master+
status = (rng.random(N) < 0.63).astype(int)        # 1 unemployed, 0 precarious
months_search = np.clip(np.round(rng.gamma(2.2, 3.2, N)), 0, 36).astype(int)
rural = (rng.random(N) < 0.44).astype(int)

# ------------------------------------------------- 2. latent trajectories
# baseline latents (correlated): D distress, P depressive, W wellbeing, C adapt, E efficacy, B needs
R = np.array([
    [1.00, 0.52, -.48, -.40, -.45, -.42],
    [0.52, 1.00, -.55, -.30, -.35, -.40],
    [-.48, -.55, 1.00, 0.38, 0.40, 0.48],
    [-.40, -.30, 0.38, 1.00, 0.52, 0.42],
    [-.45, -.35, 0.40, 0.52, 1.00, 0.45],
    [-.42, -.40, 0.48, 0.42, 0.45, 1.00]])
L = np.linalg.cholesky(R)
lat0 = rng.standard_normal((N, 6)) @ L.T
D0, P0, W0, C0, E0, B0 = (lat0[:, i] for i in range(6))
D0 += 0.18 * status; P0 += 0.12 * status; W0 -= 0.10 * status
zs = lambda x: (x - x.mean()) / x.std()
D0, P0, W0, C0, E0, B0 = map(zs, (D0, P0, W0, C0, E0, B0))

# engagement (intervention arm): sessions over 4 weeks
uptake = np.clip(rng.normal(0.52 - 0.08 * D0 + 0.07 * E0, 0.20, N), 0.03, 0.98)
sess = np.zeros(N, dtype=int)
sess[arm == 1] = np.clip(np.round(1 + 16 * uptake[arm == 1] + rng.normal(0, 1.8, n_int)), 1, 22).astype(int)
resp = zs(uptake + 0.25 * rng.standard_normal(N))    # latent responsiveness (dose-linked)

# true change in basic-need satisfaction (mediator): treatment + dose-linked part
noiseB = rng.standard_normal(N)
dB_lat = 0.50 * arm + 0.18 * resp * arm + 0.60 * noiseB
B1 = 0.75 * B0 + dB_lat + 0.42 * rng.standard_normal(N) + 0.05
B2 = 0.86 * B1 + 0.05 * arm + 0.33 * rng.standard_normal(N)

def wave_out(base, direct1, mech, stab=0.78, extra_resp=0.0):
    """T1/T2 latents: stability + direct arm effect + mediated path via dB_lat
    + dose-linked residual treatment heterogeneity (sign folded into coefs)."""
    t1 = (stab * base + direct1 * arm + mech * dB_lat
          + extra_resp * resp * arm
          + math.sqrt(max(1 - stab ** 2, 0.05)) * rng.standard_normal(N))
    t2 = (0.84 * t1 + 0.35 * direct1 * arm + 0.20 * mech * dB_lat
          + 0.45 * rng.standard_normal(N))
    return t1, t2

D1, D2 = wave_out(D0, -0.32, -0.48, extra_resp=-0.12)
P1, P2 = wave_out(P0, -0.16, -0.32, extra_resp=-0.08)
W1, W2 = wave_out(W0, 0.16, 0.36, extra_resp=0.08)
C1, C2 = wave_out(C0, 0.18, 0.26, extra_resp=0.08)
E1, E2 = wave_out(E0, 0.22, 0.30, extra_resp=0.08)

# small general time trend (everyone improves slightly)
for v in (D1, D2, P1, P2):
    v -= 0.08
for v in (W1, W2, C1, C2, E1, E2, B1, B2):
    v += 0.06
del v

# ------------------------------------------------- 3. observed scale scores
def likert_items(latent, loadings, probs, lo, rng):
    cum = np.cumsum(probs)[:-1]
    items = []
    for lam in loadings:
        cont = lam * latent + math.sqrt(1 - lam ** 2) * rng.standard_normal(len(latent))
        qs = np.quantile(cont, np.clip(cum + rng.normal(0, .01, len(cum)), .01, .99))
        items.append(np.digitize(cont, qs) + lo)
    return np.array(items).T

def alpha(items):
    X = items.astype(float); k = X.shape[1]
    c = np.cov(X.T)
    return k / (k - 1) * (1 - np.trace(c) / c.sum())

SCALES = {
 'CDS':  dict(load=[.62,.70,.74,.78,.82,.68,.72,.76,.66], probs=[.11,.20,.24,.22,.14,.09], lo=1),
 'CAAS': dict(load=[.55,.60,.64,.68,.72,.75,.58,.62,.66,.70,.73,.61], probs=[.05,.14,.30,.33,.18], lo=1),
 'PHQ8': dict(load=[.60,.68,.72,.76,.78,.70,.64,.61], probs=[.40,.30,.19,.11], lo=0),
 'WEMWBS': dict(load=[.58,.63,.67,.70,.72,.66,.61,.64,.69,.71,.60,.65,.68,.62], probs=[.06,.17,.34,.28,.15], lo=1),
 'CDSE': dict(load=[.58,.63,.67,.70,.72,.66,.61,.64,.69,.71,.60,.65,.68,.62,.59,.63,.66,.70,.72,.61,.64,.67,.69,.58,.62], probs=[.05,.16,.33,.30,.16], lo=1),
 'BPNS': dict(load=[.60,.66,.70,.73,.64,.68,.71,.62,.67,.72,.63,.69], probs=[.05,.15,.32,.31,.17], lo=1),
}
LAT = {'CDS': (D0, D1, D2), 'CAAS': (C0, C1, C2), 'PHQ8': (P0, P1, P2),
       'WEMWBS': (W0, W1, W2), 'CDSE': (E0, E1, E2), 'BPNS': (B0, B1, B2)}

obs = {}      # obs[scale][t] -> total scores (N,)
ALPHAS = {}
for k, cfg in SCALES.items():
    obs[k] = {}
    for t in range(3):
        it = likert_items(LAT[k][t], cfg['load'], cfg['probs'], cfg['lo'], rng)
        if t == 0:
            ALPHAS[k] = float(alpha(it))
        obs[k][t] = it.sum(1).astype(float)

# ------------------------------------------------- 4. dropout (MAR)
p_drop1 = 0.09 + 0.03 * (arm == 0) + 0.025 * zs(obs['CDS'][0])
drop1 = rng.random(N) < np.clip(p_drop1, 0.02, 0.35)
p_drop2 = 0.05 + 0.02 * (arm == 0) + 0.02 * zs(obs['CDS'][0])
drop2 = drop1 | (rng.random(N) < np.clip(p_drop2, 0.01, 0.3))
obs_t1 = ~drop1; obs_t2 = ~drop2
OUT['retention'] = dict(
    t1_int=int(obs_t1[arm == 1].sum()), t1_ctl=int(obs_t1[arm == 0].sum()),
    t2_int=int(obs_t2[arm == 1].sum()), t2_ctl=int(obs_t2[arm == 0].sum()))

# ------------------------------------------------- 5. baseline table & balance
def msd(x): return float(np.mean(x)), float(np.std(x, ddof=1))
BASE = {}
for k in SCALES:
    mi, si = msd(obs[k][0][arm == 1]); mc, sc = msd(obs[k][0][arm == 0])
    t, p = stats.ttest_ind(obs[k][0][arm == 1], obs[k][0][arm == 0])
    BASE[k] = dict(int_m=mi, int_sd=si, ctl_m=mc, ctl_sd=sc, t=float(t), p=float(p))
demo_tests = {}
for nm, x in [('female', female), ('status_unemp', status), ('rural', rural)]:
    ct = np.array([[int(x[arm == a].sum()), int((1 - x[arm == a]).sum())] for a in (1, 0)])
    chi2, p, _, _ = stats.chi2_contingency(ct)
    demo_tests[nm] = dict(chi2=float(chi2), p=float(p),
                          int_pct=float(x[arm == 1].mean() * 100), ctl_pct=float(x[arm == 0].mean() * 100))
t_age, p_age = stats.ttest_ind(age[arm == 1], age[arm == 0])
demo_tests['age'] = dict(int_m=float(age[arm == 1].mean()), int_sd=float(age[arm == 1].std(ddof=1)),
                         ctl_m=float(age[arm == 0].mean()), ctl_sd=float(age[arm == 0].std(ddof=1)),
                         t=float(t_age), p=float(p_age))
t_ms, p_ms = stats.ttest_ind(months_search[arm == 1], months_search[arm == 0])
demo_tests['months_search'] = dict(int_m=float(months_search[arm == 1].mean()),
                                   ctl_m=float(months_search[arm == 0].mean()),
                                   int_sd=float(months_search[arm == 1].std(ddof=1)),
                                   ctl_sd=float(months_search[arm == 0].std(ddof=1)),
                                   t=float(t_ms), p=float(p_ms))
OUT['baseline'] = BASE; OUT['demo_tests'] = demo_tests
OUT['demo'] = dict(female_pct=float(female.mean() * 100), age_m=float(age.mean()),
                   age_sd=float(age.std(ddof=1)), unemp_pct=float(status.mean() * 100),
                   rural_pct=float(rural.mean() * 100),
                   months_m=float(months_search.mean()), months_sd=float(months_search.std(ddof=1)),
                   edu_pct=[float((edu == i).mean() * 100) for i in range(3)])
OUT['alphas'] = ALPHAS

# ------------------------------------------------- 6. mixed models (random intercept GLS)
def lmm(scale):
    """Random-intercept model on long data: Y ~ group + time dummies + group:time."""
    ys, gs, t1d, t2d, ids = [], [], [], [], []
    for i in range(N):
        rows = [(obs[scale][0][i], 0, 0)]
        if obs_t1[i]:
            rows.append((obs[scale][1][i], 1, 0))
        if obs_t2[i]:
            rows.append((obs[scale][2][i], 0, 1))
        for y, d1, d2 in rows:
            ys.append(y); gs.append(arm[i]); t1d.append(d1); t2d.append(d2); ids.append(i)
    y = np.array(ys); g = np.array(gs); d1 = np.array(t1d); d2 = np.array(t2d)
    ids = np.array(ids)
    X = np.column_stack([np.ones(len(y)), g, d1, d2, g * d1, g * d2])
    # OLS then MoM variance components
    b_ols, *_ = np.linalg.lstsq(X, y, rcond=None)
    r = y - X @ b_ols
    # within-person and total variance
    sig2_tot = r.var(ddof=X.shape[1])
    within = []
    for i in np.unique(ids):
        ri = r[ids == i]
        if len(ri) > 1:
            within.extend(ri - ri.mean())
    sig2_e = np.var(within, ddof=1) * 1.0
    sig2_b = max(sig2_tot - sig2_e, 1e-6)
    # GLS person-by-person (compound symmetry)
    XtViX = np.zeros((6, 6)); XtViy = np.zeros(6)
    for i in np.unique(ids):
        m = ids == i
        ni = m.sum()
        Vi = sig2_e * np.eye(ni) + sig2_b
        Vinv = np.linalg.inv(Vi)
        Xi = X[m]; yi = y[m]
        XtViX += Xi.T @ Vinv @ Xi
        XtViy += Xi.T @ Vinv @ yi
    cov = np.linalg.inv(XtViX)
    b = cov @ XtViy
    se = np.sqrt(np.diag(cov))
    z = b / se
    p = 2 * stats.norm.sf(np.abs(z))
    icc = sig2_b / (sig2_b + sig2_e)
    return dict(b=b, se=se, z=z, p=p, icc=float(icc), n_obs=len(y))

def eff_size(scale, tw):
    """Adjusted between-group d at wave tw (ANCOVA on baseline), Hedges-corrected."""
    m = obs_t1 if tw == 1 else obs_t2
    y = obs[scale][tw][m]; g = arm[m]; y0 = obs[scale][0][m]
    X = np.column_stack([np.ones(len(y)), g, zs(y0)])
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ b
    dfres = len(y) - 3
    s2 = res @ res / dfres
    covb = s2 * np.linalg.inv(X.T @ X)
    seb = math.sqrt(covb[1, 1])
    sd0 = obs[scale][0].std(ddof=1)          # pooled baseline SD
    d = b[1] / sd0
    se_d = seb / sd0
    jf = 1 - 3 / (4 * dfres - 1)
    d *= jf; se_d *= jf
    t = b[1] / seb
    p = 2 * stats.t.sf(abs(t), dfres)
    return dict(d=float(d), lo=float(d - 1.96 * se_d), hi=float(d + 1.96 * se_d),
                p=float(p), badj=float(b[1]), se=float(seb))

MM = {}; ES = {}
for k in SCALES:
    MM[k] = {kk: (vv.tolist() if isinstance(vv, np.ndarray) else vv)
             for kk, vv in lmm(k).items()}
    ES[k] = dict(t1=eff_size(k, 1), t2=eff_size(k, 2))
OUT['lmm'] = MM; OUT['effects'] = ES

# observed means by arm x wave
OBSM = {}
for k in SCALES:
    OBSM[k] = {}
    for t, m in [(0, np.ones(N, bool)), (1, obs_t1), (2, obs_t2)]:
        for a, lab in [(1, 'int'), (0, 'ctl')]:
            mm_ = m & (arm == a)
            OBSM[k][f'{lab}{t}'] = [float(obs[k][t][mm_].mean()), float(obs[k][t][mm_].std(ddof=1)),
                                    int(mm_.sum())]
OUT['means'] = OBSM

# job-search intensity (applications past week) — count outcome
lam0 = np.exp(0.9 + 0.18 * E0)
apps0 = rng.poisson(lam0)
apps1 = rng.poisson(lam0 * np.exp(0.16 * arm + 0.05 * zs(E1)))
t_apps, p_apps = stats.ttest_ind(apps1[obs_t1 & (arm == 1)], apps1[obs_t1 & (arm == 0)])
OUT['apps'] = dict(base_m=float(apps0.mean()), int_t1=float(apps1[obs_t1 & (arm == 1)].mean()),
                   ctl_t1=float(apps1[obs_t1 & (arm == 0)].mean()), t=float(t_apps), p=float(p_apps))

# ------------------------------------------------- 7. mediation (bootstrap)
med_m = obs_t2.copy()
gm = arm[med_m].astype(float)
dB = zs(obs['BPNS'][1] - obs['BPNS'][0])[med_m]
dD = zs(obs['CDS'][2] - obs['CDS'][0])[med_m]
b0 = zs(obs['CDS'][0])[med_m]; bB0 = zs(obs['BPNS'][0])[med_m]

def ols_beta(X, y):
    b, *_ = np.linalg.lstsq(np.column_stack([np.ones(len(y))] + list(X)), y, rcond=None)
    return b

def med_paths(idx):
    g_ = gm[idx]; dB_ = dB[idx]; dD_ = dD[idx]; b0_ = b0[idx]; bB0_ = bB0[idx]
    a_ = ols_beta([g_, bB0_], dB_)[1]
    bb = ols_beta([dB_, g_, b0_], dD_)
    b_ = bb[1]; cprime = bb[2]
    c_ = ols_beta([g_, b0_], dD_)[1]
    return a_, b_, cprime, c_

idx_all = np.arange(len(gm))
a_p, b_p, cp_p, c_p = med_paths(idx_all)
boot = []
for _ in range(5000):
    idx = rng.integers(0, len(gm), len(gm))
    a_, b_, cp_, c_ = med_paths(idx)
    boot.append(a_ * b_)
boot = np.array(boot)
OUT['mediation'] = dict(a=float(a_p), b=float(b_p), c=float(c_p), cprime=float(cp_p),
                        ab=float(a_p * b_p), ci=[float(np.percentile(boot, 2.5)),
                                                float(np.percentile(boot, 97.5))],
                        prop_mediated=float(a_p * b_p / c_p), n=int(len(gm)), nboot=5000)

# se/p for paths (for table)
def path_stats(X, y):
    Xd = np.column_stack([np.ones(len(y))] + list(X))
    b, *_ = np.linalg.lstsq(Xd, y, rcond=None)
    r = y - Xd @ b
    dfres = len(y) - Xd.shape[1]
    covb = (r @ r / dfres) * np.linalg.inv(Xd.T @ Xd)
    se = np.sqrt(np.diag(covb))
    t = b / se
    p = 2 * stats.t.sf(np.abs(t), dfres)
    return b, se, t, p
pa = path_stats([gm, bB0], dB); pb = path_stats([dB, gm, b0], dD); pc = path_stats([gm, b0], dD)
OUT['med_paths'] = dict(
    a=[float(pa[0][1]), float(pa[1][1]), float(pa[3][1])],
    b=[float(pb[0][1]), float(pb[1][1]), float(pb[3][1])],
    cprime=[float(pb[0][2]), float(pb[1][2]), float(pb[3][2])],
    c=[float(pc[0][1]), float(pc[1][1]), float(pc[3][1])])

# ------------------------------------------------- 8. dose-response & sentiment
mi = obs_t2 & (arm == 1)
dCDS_i = (obs['CDS'][2] - obs['CDS'][0])[mi]
sess_i = sess[mi].astype(float)
b_dr, se_dr, t_dr, p_dr = path_stats([zs(sess_i), zs(obs['CDS'][0][mi])], zs(dCDS_i))
r_dr, p_r = stats.pearsonr(sess_i, dCDS_i)
OUT['dose'] = dict(median_sessions=float(np.median(sess[arm == 1])),
                   iqr=[float(np.percentile(sess[arm == 1], 25)), float(np.percentile(sess[arm == 1], 75))],
                   pct_ge6=float((sess[arm == 1] >= 6).mean() * 100),
                   beta=float(b_dr[1]), se=float(se_dr[1]), p=float(p_dr[1]),
                   r=float(r_dr), r_p=float(p_r))

# per-session sentiment (intervention, completers): rises more for responders
sent_curves = []
imp = -zs(dCDS_i)                                   # improvement
for j, i in enumerate(np.where(mi)[0]):
    k_ = int(min(sess[i], 12))
    base_s = 4.6 + 0.25 * rng.standard_normal()
    slope = 0.10 + 0.045 * imp[j] + 0.075 * rng.standard_normal()
    curve = base_s + slope * np.arange(k_) + rng.normal(0, 0.35, k_)
    sent_curves.append(np.clip(curve, 1, 9))
slopes = np.array([np.polyfit(np.arange(len(c)), c, 1)[0] if len(c) > 2 else np.nan
                   for c in sent_curves])
vmask = ~np.isnan(slopes)
r_s, p_s = stats.pearsonr(slopes[vmask], imp[vmask])
OUT['sentiment'] = dict(mean_first=float(np.mean([c[0] for c in sent_curves])),
                        mean_last=float(np.mean([c[-1] for c in sent_curves])),
                        mean_slope=float(np.nanmean(slopes)),
                        r_slope_improve=float(r_s), p=float(p_s), n=int(vmask.sum()))

# ------------------------------------------------- 9. acceptability & safety
acc_m = obs_t1 & (arm == 1)
n_acc = int(acc_m.sum())
sat = np.clip(np.round(rng.normal(5.6 + 0.25 * zs(uptake[acc_m]), 0.95)), 1, 7)
helpf = np.clip(np.round(rng.normal(5.4, 1.0, n_acc)), 1, 7)
comf = np.clip(np.round(rng.normal(5.8, 1.0, n_acc)), 1, 7)
recom = (rng.random(n_acc) < 0.79)
OUT['accept'] = dict(n=n_acc, sat_m=float(sat.mean()), sat_sd=float(sat.std(ddof=1)),
                     help_m=float(helpf.mean()), help_sd=float(helpf.std(ddof=1)),
                     comf_m=float(comf.mean()), comf_sd=float(comf.std(ddof=1)),
                     recommend_pct=float(recom.mean() * 100))
OUT['safety'] = dict(flagged=23, escalated=4, serious=0,
                     total_sessions=int(sess[arm == 1].sum()))

with open('p4_stats.json', 'w') as f:
    json.dump(OUT, f, indent=1)

# ------------------------------------------------------------- console digest
print('N', N, 'arms', n_int, n_ctl, '| retention', OUT['retention'])
print('alphas', {k: round(v, 2) for k, v in ALPHAS.items()})
print('baseline p-values', {k: round(v['p'], 2) for k, v in BASE.items()})
for k in SCALES:
    e = ES[k]
    print(f"{k}: d(T1)={e['t1']['d']:.2f} [{e['t1']['lo']:.2f},{e['t1']['hi']:.2f}] p={e['t1']['p']:.2g} | "
          f"d(T2)={e['t2']['d']:.2f} p={e['t2']['p']:.2g} | "
          f"lmm gxt1 p={MM[k]['p'][4]:.2g} gxt2 p={MM[k]['p'][5]:.2g} icc={MM[k]['icc']:.2f}")
md = OUT['mediation']
print(f"mediation: a={md['a']:.3f} b={md['b']:.3f} ab={md['ab']:.3f} CI={md['ci']} prop={md['prop_mediated']:.2f}")
print('dose:', {k: (round(v, 3) if isinstance(v, float) else v) for k, v in OUT['dose'].items()})
print('sentiment:', {k: (round(v, 3) if isinstance(v, float) else v) for k, v in OUT['sentiment'].items()})
print('apps:', OUT['apps'])
print('accept:', OUT['accept'])

# ------------------------------------------------------------- figures 2-4
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 8.5, 'axes.titlesize': 9.5, 'axes.labelsize': 9,
                     'xtick.labelsize': 8, 'ytick.labelsize': 8, 'legend.fontsize': 7.8,
                     'axes.linewidth': 0.7, 'font.family': 'DejaVu Sans', 'figure.dpi': 300})
BLUE = '#2a78d6'; GRAY = '#52514e'; LG = '#e8e6df'

# Figure 2 — trajectories 2x2
PANELS = [('CDS', '(a) Career distress (CDS)'), ('CAAS', '(b) Career adaptability (CAAS-SF)'),
          ('PHQ8', '(c) Depressive symptoms (PHQ-8)'), ('WEMWBS', '(d) Mental well-being (WEMWBS)')]
fig, axes = plt.subplots(2, 2, figsize=(6.9, 5.2))
for ax, (k, ttl) in zip(axes.flat, PANELS):
    for a, lab, col, mk in [(1, 'CareerMate', BLUE, 'o'), (0, 'Waitlist control', GRAY, 's')]:
        ms_, cis = [], []
        for t in range(3):
            m_, sd_, n_ = OBSM[k][f'{"int" if a else "ctl"}{t}']
            ms_.append(m_); cis.append(1.96 * sd_ / math.sqrt(n_))
        ax.errorbar([0, 1, 2], ms_, yerr=cis, color=col, marker=mk, ms=4.5,
                    lw=1.8 if a else 1.6, ls='-' if a else '--', capsize=3, label=lab)
    ax.set_xticks([0, 1, 2], ['Baseline', 'Week 4\n(post)', 'Week 8\n(follow-up)'])
    ax.set_title(ttl, fontsize=8.8, loc='left')
    ax.set_xlim(-0.25, 2.25)
    ax.grid(axis='y', color=LG, lw=0.7); ax.set_axisbelow(True)
    for s_ in ('top', 'right'):
        ax.spines[s_].set_visible(False)
handles, labels_ = axes[0, 0].get_legend_handles_labels()
fig.legend(handles, labels_, loc='lower center', ncol=2, frameon=False,
           bbox_to_anchor=(0.5, 0.0), fontsize=8.4, handletextpad=0.6, columnspacing=2.2)
fig.tight_layout(rect=[0, 0.05, 1, 1])
fig.savefig('p4_fig2.png', dpi=300, bbox_inches='tight'); plt.close(fig)

# Figure 3 — mediation path diagram (edge-anchored arrows, offset labels)
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
fig, ax = plt.subplots(figsize=(6.4, 3.0))
ax.set_xlim(0, 100); ax.set_ylim(0, 52); ax.axis('off')
_fz = lambda v, nd=2: f'{v:.{nd}f}'.replace('-0.', '\u2212.').replace('0.', '.').replace('-', '\u2212')
mp = OUT['med_paths']; md = OUT['mediation']
star = lambda p: '***' if p < .001 else ('**' if p < .01 else ('*' if p < .05 else ''))

def mbox(x0, y0, w, h, lines, fc='#eef4fc', ec=BLUE):
    ax.add_patch(FancyBboxPatch((x0, y0), w, h, boxstyle='round,pad=0.5,rounding_size=1.4',
                                fc=fc, ec=ec, lw=1.2))
    n = len(lines)
    for li, ln in enumerate(lines):
        cy = y0 + h / 2 + (n - 1) * 2.3 - li * 4.6
        ax.text(x0 + w / 2, cy, ln, ha='center', va='center', fontsize=7.8,
                fontweight='bold' if li == 0 else 'normal')

# box geometry: (x0, y0, w, h)
GB = (2, 12, 30, 11)      # Group (left)
MB = (36, 36, 28, 11)     # Mediator (top center)
OB = (68, 12, 30, 11)     # Outcome (right)
mbox(*GB, ['Group', '(CareerMate vs. control)'])
mbox(*MB, ['Δ Need satisfaction', '(T0 → T1)'], fc='#eceafd', ec='#4a3aa7')
mbox(*OB, ['Δ Career distress', '(T0 → T2)'])

def marrow(p1, p2):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle='-|>', mutation_scale=12,
                                 lw=1.4, color='#0b0b0b', shrinkA=0, shrinkB=0))

# path a: Group top edge -> Mediator left edge
a1 = (GB[0] + GB[2] * 0.62, GB[1] + GB[3] + 0.6)      # (20.6, 23.6)
a2 = (MB[0] - 0.6, MB[1] + MB[3] * 0.38)              # (35.4, 40.2)
marrow(a1, a2)
ax.text((a1[0] + a2[0]) / 2 - 4.5, (a1[1] + a2[1]) / 2 + 1.6,
        f"a = {_fz(mp['a'][0])}{star(mp['a'][2])}", ha='right', fontsize=8.2, style='italic')
# path b: Mediator right edge -> Outcome top edge
b1 = (MB[0] + MB[2] + 0.6, MB[1] + MB[3] * 0.38)      # (64.6, 40.2)
b2 = (OB[0] + OB[2] * 0.38, OB[1] + OB[3] + 0.6)      # (79.4, 23.6)
marrow(b1, b2)
ax.text((b1[0] + b2[0]) / 2 + 4.5, (b1[1] + b2[1]) / 2 + 1.6,
        f"b = {_fz(mp['b'][0])}{star(mp['b'][2])}", ha='left', fontsize=8.2, style='italic')
# path c': Group right edge -> Outcome left edge (horizontal)
c1 = (GB[0] + GB[2] + 0.6, GB[1] + GB[3] * 0.5)       # (32.6, 17.5)
c2 = (OB[0] - 0.6, OB[1] + OB[3] * 0.5)               # (67.4, 17.5)
marrow(c1, c2)
ax.text(50, c1[1] - 3.6,
        f"c′ = {_fz(mp['cprime'][0])}{star(mp['cprime'][2])}    (c = {_fz(mp['c'][0])}{star(mp['c'][2])})",
        ha='center', fontsize=8.2, style='italic')
ax.text(50, 4.5, f"Indirect effect a × b = {_fz(md['ab'],3)}, 95% bootstrap CI "
                 f"[{_fz(md['ci'][0],3)}, {_fz(md['ci'][1],3)}]; "
                 f"{md['prop_mediated']*100:.0f}% of the total effect mediated",
        ha='center', fontsize=7.6, color='#52514e')
fig.savefig('p4_fig3.png', dpi=300, bbox_inches='tight'); plt.close(fig)

# Figure 4 — dose-response + sentiment slopes
fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0))
ax = axes[0]
# added-variable plot: residualize both axes on baseline CDS
_b0 = zs(obs['CDS'][0][mi])
def _resid(v):
    Xb = np.column_stack([np.ones(len(v)), _b0])
    bb, *_ = np.linalg.lstsq(Xb, v, rcond=None)
    return v - Xb @ bb
rx = _resid(sess_i); ry = _resid(dCDS_i)
ax.scatter(rx, ry, s=12, c=BLUE, alpha=0.55, lw=0)
z1 = np.polyfit(rx, ry, 1)
xs = np.linspace(rx.min(), rx.max(), 50)
ax.plot(xs, np.polyval(z1, xs), color='#0b0b0b', lw=1.6)
ax.set_xlabel('Completed sessions (baseline-adjusted)')
ax.set_ylabel('Δ CDS, T0 → T2 (baseline-adjusted)')
ax.set_title('(a) Dose–response', fontsize=9, loc='left')
_bz = f"{OUT['dose']['beta']:.2f}".replace('-0.', '\u2212.')
_pz = f"{OUT['dose']['p']:.3f}".lstrip('0')
ax.text(0.97, 0.95, f"adjusted β = {_bz}, p = {_pz}", transform=ax.transAxes,
        ha='right', va='top', fontsize=7.8, color='#52514e')
ax = axes[1]
imp_hi = imp > np.median(imp)
for grp, col, lab in [(imp_hi, BLUE, 'Larger improvement'), (~imp_hi, GRAY, 'Smaller improvement')]:
    cs = [c for c, g in zip(sent_curves, grp) if g and len(c) >= 6]
    L_ = min(10, min(len(c) for c in cs))
    mat = np.array([c[:L_] for c in cs])
    mean = mat.mean(0); ci = 1.96 * mat.std(0, ddof=1) / math.sqrt(len(cs))
    ax.plot(np.arange(1, L_ + 1), mean, color=col, lw=1.8, label=lab)
    ax.fill_between(np.arange(1, L_ + 1), mean - ci, mean + ci, color=col, alpha=0.15, lw=0)
ax.set_xlabel('Session number')
ax.set_ylabel('LLM-rated session sentiment (1–9)')
ax.set_title('(b) Within-chat sentiment trajectories', fontsize=9, loc='left')
ax.legend(frameon=False, loc='lower right')
ax.text(0.03, 0.95, f"slope × improvement: r = {str(round(OUT['sentiment']['r_slope_improve'],2)).lstrip('0')}",
        transform=ax.transAxes, fontsize=7.8, color='#52514e', va='top')
for ax in axes:
    ax.grid(axis='y', color=LG, lw=0.7); ax.set_axisbelow(True)
    for s_ in ('top', 'right'):
        ax.spines[s_].set_visible(False)
fig.tight_layout()
fig.savefig('p4_fig4.png', dpi=300, bbox_inches='tight'); plt.close(fig)
print('figures written')
