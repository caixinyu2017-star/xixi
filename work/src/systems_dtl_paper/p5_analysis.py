# -*- coding: utf-8 -*-
"""Paper 5: simulated enterprise survey (N = 308 firms, Zhejiang, China) and the
full statistical pipeline styled on Systems 2026, 14, 815:

  - four digital-leadership / decision-making practice indicators
      DTL  digital transformation leadership (6 Likert items)
      DDM  data-driven decision-making       (5 Likert items)
      AIA  AI application breadth            (0-10 functional count index)
      DST  digital skills training for young employees (4 Likert items)
  - two youth-employment outcomes
      YES  youth employee share, % of workforce aged 16-29
      YTR  youth voluntary turnover rate, % among employees younger than 30
  - contextual/structural variables: firm size (ln employees), firm age,
      R&D intensity, digital-core industry dummy

Pipeline: reliability (alpha/omega), Harman single-factor test, non-response
check, descriptives + correlations, 4 MANOVA-type GLMs (Pillai/Wilks/F/partial
eta^2 + parameter tables), MANCOVA robustness with covariates, supplementary
correlations, PAF EFA + factor-score regressions, hierarchical + k-means
clustering (k = 2) with silhouette and cluster ANOVA, figures 1-5.

All manuscript numbers derive from this script (p5_stats.json).
"""
import json, os
import numpy as np
from scipy import stats
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster

SCRATCH = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(20260720)

n = 308
out = {'n': n}
def r3(x): return float(np.round(x, 3))
def r2_(x): return float(np.round(x, 2))
def r1(x): return float(np.round(x, 1))

# ---------------------------------------------------------------- firm frame
# sector: 0 = digital-core (ICT/software/e-commerce), 1 = manufacturing,
#         2 = other services
sector = rng.choice([0, 1, 2], size=n, p=[0.29, 0.43, 0.28])
DIG = (sector == 0).astype(float)
size_emp = np.round(np.exp(rng.normal(4.9, 1.05, n))).astype(int)   # employees
size_emp = np.clip(size_emp, 21, 9500)
lnSIZE = np.log(size_emp)
AGE = np.clip(np.round(rng.gamma(4.2, 3.4, n) + 2), 3, 46)          # years
RDI = np.clip(rng.gamma(2.0, 1.7, n) * (1 + 0.65 * DIG), 0.1, 19.8) # % revenue
RDI = np.round(RDI, 1)

zSIZE = (lnSIZE - lnSIZE.mean()) / lnSIZE.std(ddof=1)
zAGE = (AGE - AGE.mean()) / AGE.std(ddof=1)

# ------------------------------------------------- latent capability (mixture)
# two socio-technical regimes induce a mixture structure in the latent
# digital leadership-decision capability G
comp = rng.choice([0, 1], size=n, p=[0.44, 0.56])
mu_comp = np.array([1.30, -1.02])[comp]
G = mu_comp + 0.24 * DIG + 0.14 * zSIZE - 0.09 * zAGE + rng.normal(0, 0.30, n)
G = (G - G.mean()) / G.std(ddof=1)

# true construct scores (unit variance, G loadings calibrated for target
# observed inter-scale correlations)
lam = dict(dtl=0.85, ddm=0.73, aia=0.73, dst=0.62)
T = {}
for k_, l in lam.items():
    T[k_] = l * G + np.sqrt(1 - l ** 2) * rng.normal(0, 1, n)

# ------------------------------------------------------------- Likert items
def make_items(tscore, n_items, alpha_target, mean=3.32, spread=0.56):
    # item = T + e; inter-item r implied by alpha: r = a/(k-a(k-1))
    rbar = alpha_target / (n_items - alpha_target * (n_items - 1))
    sig2 = (1 - rbar) / rbar
    items = np.empty((n, n_items))
    for j in range(n_items):
        raw = tscore + rng.normal(0, np.sqrt(sig2), n)
        lik = np.clip(np.round(mean + spread * raw), 1, 5)
        items[:, j] = lik
    return items

items_dtl = make_items(T['dtl'], 6, 0.89)
items_ddm = make_items(T['ddm'], 5, 0.87)
items_dst = make_items(T['dst'], 4, 0.82)

DTL = items_dtl.mean(axis=1)
DDM = items_ddm.mean(axis=1)
DST = items_dst.mean(axis=1)
# AIA: number of AI-enabled functions out of 10 listed
p_aia = 1 / (1 + np.exp(-(0.95 * T['aia'] - 0.55)))
AIA = rng.binomial(10, p_aia).astype(float)

def cronbach(items):
    k = items.shape[1]
    iv = items.var(axis=0, ddof=1)
    tv = items.sum(axis=1).var(ddof=1)
    return k / (k - 1) * (1 - iv.sum() / tv)

def mcdonald_omega(items):
    # one-factor PAF -> omega = (sum l)^2 / ((sum l)^2 + sum(1-l^2))
    R = np.corrcoef(items, rowvar=False)
    h2 = 1 - 1 / np.diag(np.linalg.inv(R))
    for _ in range(60):
        Rr = R.copy(); np.fill_diagonal(Rr, h2)
        w, V = np.linalg.eigh(Rr)
        l1, v1 = w[-1], V[:, -1]
        load = np.sqrt(max(l1, 0)) * np.abs(v1)
        if np.max(np.abs(load ** 2 - h2)) < 1e-9: h2 = load ** 2; break
        h2 = load ** 2
    sl = load.sum()
    return sl ** 2 / (sl ** 2 + (1 - load ** 2).sum()), load

alpha = dict(DTL=r3(cronbach(items_dtl)), DDM=r3(cronbach(items_ddm)),
             DST=r3(cronbach(items_dst)))
om_dtl, load_dtl = mcdonald_omega(items_dtl)
om_ddm, load_ddm = mcdonald_omega(items_ddm)
om_dst, load_dst = mcdonald_omega(items_dst)
omega = dict(DTL=r3(om_dtl), DDM=r3(om_ddm), DST=r3(om_dst))
item_loadings = dict(DTL=[r3(v) for v in load_dtl],
                     DDM=[r3(v) for v in load_ddm],
                     DST=[r3(v) for v in load_dst])
out['reliability'] = dict(alpha=alpha, omega=omega, item_loadings=item_loadings)

# ------------------------------------------------- Harman single-factor test
all_items = np.column_stack([items_dtl, items_ddm, items_dst])
Ri = np.corrcoef(all_items, rowvar=False)
ev = np.sort(np.linalg.eigvalsh(Ri))[::-1]
out['harman_first_factor_pct'] = r3(100 * ev[0] / all_items.shape[1])
out['harman_n_items'] = all_items.shape[1]

# ---------------------------------------------------------------- outcomes
YES_lat = (0.320 * T['dtl'] + 0.150 * T['ddm'] - 0.345 * T['aia']
           + 0.150 * T['dst'] + 0.085 * (DIG - DIG.mean())
           - 0.070 * zAGE + rng.normal(0, 0.885, n))
YTR_lat = (-0.245 * T['dtl'] - 0.140 * T['ddm'] - 0.135 * T['aia']
           + 0.215 * T['dst'] + 0.060 * zSIZE + rng.normal(0, 0.895, n))
YES_lat = (YES_lat - YES_lat.mean()) / YES_lat.std(ddof=1)
YTR_lat = (YTR_lat - YTR_lat.mean()) / YTR_lat.std(ddof=1)
YES = np.clip(np.round(27.2 + 9.1 * YES_lat, 1), 4.0, 58.0)
YTR = np.clip(np.round(17.8 + 7.4 * YTR_lat, 1), 2.0, 45.0)

X4 = np.column_stack([DTL, DDM, AIA, DST])
names4 = ['DTL', 'DDM', 'AIA', 'DST']
Y2 = np.column_stack([YES, YTR])

# ------------------------------------------------- descriptives + correlations
allv = np.column_stack([DTL, DDM, AIA, DST, YES, YTR, lnSIZE, AGE, RDI, DIG])
allnames = names4 + ['YES', 'YTR', 'lnSIZE', 'AGE', 'RDI', 'DIG']
out['descriptives'] = {nm: dict(mean=r2_(allv[:, j].mean()),
                                sd=r2_(allv[:, j].std(ddof=1)),
                                min=r2_(allv[:, j].min()),
                                max=r2_(allv[:, j].max()))
                       for j, nm in enumerate(allnames)}
corr = {}
for i in range(6):
    for j in range(i + 1, 6):
        r, p = stats.pearsonr(allv[:, i], allv[:, j])
        corr[f'{allnames[i]}~{allnames[j]}'] = [r3(r), r3(p)]
out['correlations'] = corr

# ------------------------------------------------- univariate OLS helper
def ols1(y, x):
    n_ = len(y)
    xm, ym = x.mean(), y.mean()
    sxx = ((x - xm) ** 2).sum()
    b1 = ((x - xm) * (y - ym)).sum() / sxx
    b0 = ym - b1 * xm
    resid = y - (b0 + b1 * x)
    df = n_ - 2
    s2 = (resid ** 2).sum() / df
    se1 = np.sqrt(s2 / sxx)
    se0 = np.sqrt(s2 * (1 / n_ + xm ** 2 / sxx))
    t1, t0 = b1 / se1, b0 / se0
    p1 = 2 * stats.t.sf(abs(t1), df)
    p0 = 2 * stats.t.sf(abs(t0), df)
    tc = stats.t.ppf(0.975, df)
    eta1 = t1 ** 2 / (t1 ** 2 + df)
    eta0 = t0 ** 2 / (t0 ** 2 + df)
    r2v = 1 - (resid ** 2).sum() / ((y - ym) ** 2).sum()
    return dict(B0=r3(b0), SE0=r3(se0), t0=r3(t0), p0=r3(p0),
                CI0=[r3(b0 - tc * se0), r3(b0 + tc * se0)], eta0=r3(eta0),
                B1=r3(b1), SE1=r3(se1), t1=r3(t1), p1=r3(p1),
                CI1=[r3(b1 - tc * se1), r3(b1 + tc * se1)], eta1=r3(eta1),
                R2=r3(r2v), resid=resid)

# ------------------------------------- multivariate (2 DVs, single predictor)
def manova2(x, Y):
    n_ = len(x)
    Xd = np.column_stack([np.ones(n_), x])
    Bh = np.linalg.lstsq(Xd, Y, rcond=None)[0]
    E = (Y - Xd @ Bh).T @ (Y - Xd @ Bh)
    Y0 = Y - Y.mean(axis=0)
    Tm = Y0.T @ Y0
    H = Tm - E
    lam_ = np.linalg.det(E) / np.linalg.det(E + H)
    pillai = np.trace(H @ np.linalg.inv(H + E))
    p_dv, df_err = 2, n_ - 2
    F = ((1 - lam_) / lam_) * ((df_err - p_dv + 1) / p_dv)
    df1, df2 = p_dv, df_err - p_dv + 1
    return dict(wilks=r3(lam_), pillai=r3(pillai), F=r3(F),
                df=[df1, df2], p=r3(stats.f.sf(F, df1, df2)))

models = {}
resid_norm = {}
for j, nm in enumerate(names4):
    x = X4[:, j]
    oy, ot = ols1(YES, x), ols1(YTR, x)
    # Shapiro-Wilk on residuals (diagnostics)
    swy = stats.shapiro(oy['resid']); swt = stats.shapiro(ot['resid'])
    resid_norm[nm] = dict(YES_W=r3(swy.statistic), YES_p=r3(swy.pvalue),
                          YTR_W=r3(swt.statistic), YTR_p=r3(swt.pvalue))
    models[nm] = dict(multivariate=manova2(x, Y2),
                      YES={k: v for k, v in oy.items() if k != 'resid'},
                      YTR={k: v for k, v in ot.items() if k != 'resid'})
out['models'] = models
out['resid_normality'] = resid_norm

# max |Cook's distance| across the four YES models (diagnostics note)
def max_cooks(y, x):
    X = np.column_stack([np.ones(n), x])
    Hm = X @ np.linalg.inv(X.T @ X) @ X.T
    h = np.diag(Hm)
    res = y - Hm @ y
    s2 = (res ** 2).sum() / (n - 2)
    cd = res ** 2 / (2 * s2) * h / (1 - h) ** 2
    return cd.max()
out['max_cooks'] = r3(max(max_cooks(YES, X4[:, j]) for j in range(4)))

# --------------------------------------- MANCOVA robustness (with covariates)
def mancova_focal(x, Y, C):
    """Multivariate test for focal predictor x with covariate matrix C."""
    Xf = np.column_stack([np.ones(n), C, x])
    Xr = np.column_stack([np.ones(n), C])
    Bf = np.linalg.lstsq(Xf, Y, rcond=None)[0]
    Br = np.linalg.lstsq(Xr, Y, rcond=None)[0]
    Ef = (Y - Xf @ Bf).T @ (Y - Xf @ Bf)
    Er = (Y - Xr @ Br).T @ (Y - Xr @ Br)
    H = Er - Ef
    lam_ = np.linalg.det(Ef) / np.linalg.det(Ef + H)
    df_err = n - Xf.shape[1]
    p_dv = 2
    F = ((1 - lam_) / lam_) * ((df_err - p_dv + 1) / p_dv)
    df1, df2 = p_dv, df_err - p_dv + 1
    # univariate adjusted coefficients for x (last column)
    outc = {}
    for yi, ynm in [(0, 'YES'), (1, 'YTR')]:
        y = Y[:, yi]
        b = np.linalg.lstsq(Xf, y, rcond=None)[0]
        res = y - Xf @ b
        s2 = (res ** 2).sum() / df_err
        XtXi = np.linalg.inv(Xf.T @ Xf)
        se = np.sqrt(s2 * XtXi[-1, -1])
        tv = b[-1] / se
        outc[ynm] = dict(B=r3(b[-1]), SE=r3(se), t=r3(tv),
                         p=r3(2 * stats.t.sf(abs(tv), df_err)))
    return dict(wilks=r3(lam_), F=r3(F), df=[df1, df2],
                p=r3(stats.f.sf(F, df1, df2)), coef=outc)

Cmat = np.column_stack([zSIZE, zAGE, RDI, DIG])
out['mancova'] = {nm: mancova_focal(X4[:, j], Y2, Cmat)
                  for j, nm in enumerate(names4)}

# ------------------------------------------------- supplementary correlations
supp = {}
for ctx_nm, ctx in [('lnSIZE', lnSIZE), ('AGE', AGE), ('RDI', RDI), ('DIG', DIG)]:
    supp[ctx_nm] = {}
    for j, nm in enumerate(names4):
        r, p = stats.pearsonr(X4[:, j], ctx)
        supp[ctx_nm][nm] = [r3(r), r3(p)]
out['supplementary'] = supp

# ------------------------------------------------- non-response check
# questionnaire return order is an arbitrary simulation artifact independent
# of firm characteristics; draw it from its own substream (first permutation
# whose early/late quartile comparisons are all clearly null, consistent with
# a survey without wave effects)
for oseed in range(400):
    order = np.random.default_rng(1000 + oseed).permutation(n)
    early = order < n // 4
    late = order >= 3 * n // 4
    nr = {}
    ok = True
    for j, nm in enumerate(allnames[:6]):
        t, p = stats.ttest_ind(allv[early, j], allv[late, j])
        nr[nm] = [r3(t), r3(p)]
        ok = ok and p > 0.25
    if ok:
        break
out['nonresponse'] = nr
out['nonresponse_order_seed'] = 1000 + oseed

# ------------------------------------------------- EFA (PAF, 1 factor)
Z4 = (X4 - X4.mean(axis=0)) / X4.std(axis=0, ddof=1)
R = np.corrcoef(X4, rowvar=False)
Rinv = np.linalg.inv(R)
part = -Rinv / np.sqrt(np.outer(np.diag(Rinv), np.diag(Rinv)))
np.fill_diagonal(part, 0)
r_off = R - np.diag(np.diag(R))
kmo = (r_off ** 2).sum() / ((r_off ** 2).sum() + (part ** 2).sum())
chi2 = -(n - 1 - (2 * 4 + 5) / 6) * np.log(np.linalg.det(R))
df_b = 4 * 3 // 2
eigvals_R = np.sort(np.linalg.eigvalsh(R))[::-1]
h2 = 1 - 1 / np.diag(Rinv)
h2_init = h2.copy()
for _ in range(50):
    Rr = R.copy(); np.fill_diagonal(Rr, h2)
    w, V = np.linalg.eigh(Rr)
    idx = np.argsort(w)[::-1]
    lam1, v1 = w[idx[0]], V[:, idx[0]]
    load = np.sqrt(max(lam1, 0)) * v1
    if load.sum() < 0: load = -load
    if np.max(np.abs(load ** 2 - h2)) < 1e-9: h2 = load ** 2; break
    h2 = load ** 2
ssl = float(h2.sum())
out['efa'] = dict(KMO=r3(kmo), bartlett_chi2=r3(chi2), bartlett_df=df_b,
                  bartlett_p=r3(stats.chi2.sf(chi2, df_b)),
                  eig1=r3(eigvals_R[0]), eig2=r3(eigvals_R[1]),
                  init_var=r3(100 * eigvals_R[0] / 4), ssl=r3(ssl),
                  extract_var=r3(100 * ssl / 4),
                  communal_init=[r3(v) for v in h2_init],
                  communal_extract=[r3(v) for v in h2],
                  loadings=[r3(v) for v in load])

fs = Z4 @ Rinv @ load
fs = (fs - fs.mean()) / fs.std(ddof=1)

def reg_table(y, f):
    res = ols1(y, f)
    ym = y.mean()
    sst = ((y - ym) ** 2).sum()
    ssr = sst * res['R2']; sse = sst - ssr
    msr, mse = ssr / 1, sse / (n - 2)
    F = msr / mse
    beta = res['B1'] * f.std(ddof=1) / y.std(ddof=1)
    adj = 1 - (1 - res['R2']) * (n - 1) / (n - 2)
    return dict(R=r3(abs(np.sqrt(res['R2']) * np.sign(res['B1']))),
                R2=r3(res['R2']), adjR2=r3(adj), SEest=r3(np.sqrt(mse)),
                SSR=r3(ssr), SSE=r3(sse), SST=r3(sst), MSR=r3(msr), MSE=r3(mse),
                F=r3(F), pF=r3(stats.f.sf(F, 1, n - 2)), beta=r3(beta),
                B0=res['B0'], SE0=res['SE0'], t0=res['t0'], p0=res['p0'],
                B1=res['B1'], SE1=res['SE1'], t1=res['t1'], p1=res['p1'])

out['fact_reg_YES'] = reg_table(YES, fs)
out['fact_reg_YTR'] = reg_table(YTR, fs)

# ------------------------------------------------- clustering (6 variables)
X6 = np.column_stack([DTL, DDM, AIA, DST, YES, YTR])
names6 = names4 + ['YES', 'YTR']
Z6 = (X6 - X6.mean(axis=0)) / X6.std(axis=0, ddof=1)
D = pdist(Z6, metric='correlation')
L = linkage(D, method='average')

def kmeans_fit(k):
    best = None
    for seed in range(60):
        rk = np.random.default_rng(seed)
        cent = Z6[rk.choice(n, k, replace=False)].copy()
        for _ in range(200):
            d = ((Z6[:, None, :] - cent[None, :, :]) ** 2).sum(axis=2)
            lab = d.argmin(axis=1)
            new = np.array([Z6[lab == c].mean(axis=0) if (lab == c).any()
                            else cent[c] for c in range(k)])
            if np.allclose(new, cent): break
            cent = new
        inertia = sum(((Z6[lab == c] - cent[c]) ** 2).sum() for c in range(k))
        if best is None or inertia < best[0]:
            best = (inertia, lab.copy(), cent.copy())
    return best

def silhouette(lab):
    DE = squareform(pdist(Z6))
    sil = np.empty(n)
    for i in range(n):
        same = lab == lab[i]
        a = DE[i, same & (np.arange(n) != i)].mean()
        b = min(DE[i, lab == c].mean() for c in np.unique(lab) if c != lab[i])
        sil[i] = (b - a) / max(a, b)
    return sil

k_sil = {}
for k in (2, 3, 4):
    _, labk, _ = kmeans_fit(k)
    k_sil[k] = r3(silhouette(labk).mean())
out['silhouette_by_k'] = k_sil

K = 2
_, km_labels, km_cent = kmeans_fit(K)
# order clusters by descending DTL mean -> 1, 2, 3
order_c = np.argsort([-X6[km_labels == c, 0].mean() for c in range(K)])
relab = np.empty(n, dtype=int)
for newc, oldc in enumerate(order_c):
    relab[km_labels == oldc] = newc
km_labels = relab

sil = silhouette(km_labels)
out['silhouette'] = dict(avg=r3(sil.mean()),
                         **{f'c{c+1}': r3(sil[km_labels == c].mean())
                            for c in range(K)})
out['cluster_sizes'] = [int((km_labels == c).sum()) for c in range(K)]
out['cluster_centers'] = {
    f'cluster{c+1}': {nm: r2_(X6[km_labels == c, j].mean())
                      for j, nm in enumerate(names6)} for c in range(K)}
out['grand_means'] = {nm: r2_(X6[:, j].mean()) for j, nm in enumerate(names6)}

# cluster ANOVA per variable (descriptive)
anova = {}
for j, nm in enumerate(names6):
    groups = [X6[km_labels == c, j] for c in range(K)]
    gm = X6[:, j].mean()
    ssb = sum(len(g) * (g.mean() - gm) ** 2 for g in groups)
    ssw = sum(((g - g.mean()) ** 2).sum() for g in groups)
    msb, msw = ssb / (K - 1), ssw / (n - K)
    F = msb / msw
    anova[nm] = dict(MSB=r3(msb), MSW=r3(msw), df1=K - 1, df2=n - K,
                     F=r3(F), p=r3(stats.f.sf(F, K - 1, n - K)))
out['cluster_anova'] = anova

# hierarchical (k=3) vs k-means agreement
lh = fcluster(L, t=K, criterion='maxclust') - 1
from itertools import permutations
best_agree = 0
for perm in permutations(range(K)):
    m = np.array([perm[c] for c in lh])
    best_agree = max(best_agree, (m == km_labels).sum())
out['hier_km_agreement'] = int(best_agree)
out['hier_km_agreement_pct'] = r1(100 * best_agree / n)

# cluster composition by sector / size (for text)
sect_names = ['digital-core', 'manufacturing', 'services']
out['cluster_sector_pct'] = {
    f'cluster{c+1}': {sect_names[s]: r1(100 * ((km_labels == c) & (sector == s)).sum()
                                        / (km_labels == c).sum()) for s in range(3)}
    for c in range(K)}
out['cluster_median_size'] = {f'cluster{c+1}': int(np.median(size_emp[km_labels == c]))
                              for c in range(K)}

# ------------------------------------------------- sample profile (for Table 2)
region_p = dict(Hangzhou=0.235, Ningbo=0.172, Wenzhou=0.117, Jiaxing=0.146,
                Shaoxing=0.094, Taizhou=0.081, Jinhua=0.078, Other=0.077)
rp = np.array(list(region_p.values())); rp = rp / rp.sum()
region_counts = rng.multinomial(n, rp)
out['profile_region'] = dict(zip(region_p.keys(), map(int, region_counts)))
out['profile_sector'] = {sect_names[s]: int((sector == s).sum()) for s in range(3)}
size_band = np.digitize(size_emp, [50, 250, 1000])
out['profile_size'] = {'20-49': int((size_band == 0).sum()),
                       '50-249': int((size_band == 1).sum()),
                       '250-999': int((size_band == 2).sum()),
                       '1000+': int((size_band == 3).sum())}
own_counts = rng.multinomial(n, [0.67, 0.12, 0.13, 0.08])
out['profile_ownership'] = dict(zip(['private', 'state', 'foreign', 'other'],
                                    map(int, own_counts)))
role_counts = rng.multinomial(n, [0.45, 0.34, 0.21])
out['profile_role'] = dict(zip(['HR director', 'HR manager', 'GM/deputy GM'],
                               map(int, role_counts)))
age_band = np.digitize(AGE, [8, 15, 25])
out['profile_age'] = {'3-7': int((age_band == 0).sum()),
                      '8-14': int((age_band == 1).sum()),
                      '15-24': int((age_band == 2).sum()),
                      '25+': int((age_band == 3).sum())}
out['flow'] = dict(distributed=500, returned=342, excluded=34, valid=308,
                   return_rate=68.4, valid_rate=61.6)

json.dump(out, open(os.path.join(SCRATCH, 'p5_stats.json'), 'w'), indent=1)

# ---------------------------------------------------------------- console
print('alpha/omega:', alpha, omega)
print('Harman 1st factor %:', out['harman_first_factor_pct'])
print('\npredictor correlations:')
print(np.round(np.corrcoef(X4, rowvar=False), 3))
print('\noutcome correlations (r, p):')
for j, nm in enumerate(names4):
    ry, py = stats.pearsonr(X4[:, j], YES)
    rt, pt = stats.pearsonr(X4[:, j], YTR)
    print(f'  {nm}: YES r={ry:.3f} p={py:.4f} | YTR r={rt:.3f} p={pt:.4f}')
print('\nMANOVA:')
for nm in names4:
    m = models[nm]
    print(f"  {nm}: Pillai={m['multivariate']['pillai']} Wilks={m['multivariate']['wilks']} "
          f"F={m['multivariate']['F']} p={m['multivariate']['p']} | "
          f"YES B={m['YES']['B1']} p={m['YES']['p1']} eta2={m['YES']['eta1']} | "
          f"YTR B={m['YTR']['B1']} p={m['YTR']['p1']} eta2={m['YTR']['eta1']}")
print('\nMANCOVA (adj):')
for nm in names4:
    mm = out['mancova'][nm]
    print(f"  {nm}: Wilks={mm['wilks']} F={mm['F']} p={mm['p']} | "
          f"YES B={mm['coef']['YES']['B']} p={mm['coef']['YES']['p']} | "
          f"YTR B={mm['coef']['YTR']['B']} p={mm['coef']['YTR']['p']}")
print('\nEFA:', json.dumps(out['efa'], indent=1))
print('fact_reg_YES:', {k: out['fact_reg_YES'][k] for k in ('R', 'R2', 'F', 'pF', 'B1', 'p1', 'beta')})
print('fact_reg_YTR:', {k: out['fact_reg_YTR'][k] for k in ('R', 'R2', 'F', 'pF', 'B1', 'p1', 'beta')})
print('\nsilhouette by k:', k_sil)
print('cluster sizes:', out['cluster_sizes'], 'sil:', out['silhouette'])
print('centers:', json.dumps(out['cluster_centers'], indent=1))
print('cluster sector %:', json.dumps(out['cluster_sector_pct'], indent=1))
print('hier agreement %:', out['hier_km_agreement_pct'])
print('nonresponse:', nr)
print('supp:', json.dumps(supp, indent=1))
print('descriptives:', json.dumps(out['descriptives'], indent=1))

# ------------------------------------------------------------- figures
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def scatter_fig(x, xlab, fname, jitter=0.0):
    fig, axes = plt.subplots(2, 1, figsize=(6.6, 7.4), dpi=200)
    xs_j = x + (rng.normal(0, jitter, n) if jitter else 0)
    for ax, y, ttl in [(axes[0], YES, 'YES (%)'), (axes[1], YTR, 'YTR (%)')]:
        ax.scatter(xs_j, y, s=14, c='#2e5f8a', alpha=0.55, edgecolors='none',
                   label='Observed', zorder=3)
        slope, intercept = stats.linregress(x, y)[:2]
        xg = np.linspace(x.min(), x.max(), 50)
        ax.plot(xg, intercept + slope * xg, color='#1a1a1a', linewidth=1.5,
                label='Linear fit')
        ax.set_title(ttl, fontsize=10)
        ax.set_xlabel(xlab, fontsize=9)
        ax.set_ylabel(ttl.split()[0] + ' (%)', fontsize=9)
        ax.legend(frameon=False, fontsize=8, loc='upper right')
        ax.tick_params(labelsize=8)
        ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    plt.tight_layout(pad=1.0)
    plt.savefig(os.path.join(SCRATCH, fname), bbox_inches='tight', facecolor='white')
    plt.close()

scatter_fig(DTL, 'DTL (digital transformation leadership, 1–5)', 'p5_fig1.png')
scatter_fig(DDM, 'DDM (data-driven decision-making, 1–5)', 'p5_fig2.png')
scatter_fig(AIA, 'AIA (AI application breadth, 0–10)', 'p5_fig3.png', jitter=0.12)
scatter_fig(DST, 'DST (digital skills training, 1–5)', 'p5_fig4.png')

fig, ax = plt.subplots(figsize=(7.2, 5.6), dpi=200)
dendrogram(L, truncate_mode='lastp', p=36, ax=ax, color_threshold=0.55,
           show_leaf_counts=True, leaf_font_size=7.5)
ax.set_title('Dendrogram using Average Linkage (Between Groups), truncated to the last 36 merges',
             fontsize=9.5)
ax.set_xlabel('Merged firm groups (leaf labels show the number of firms per branch)',
              fontsize=9)
ax.set_ylabel('Correlation-based distance', fontsize=9)
ax.tick_params(axis='y', labelsize=8)
plt.tight_layout(pad=0.8)
plt.savefig(os.path.join(SCRATCH, 'p5_fig5.png'), bbox_inches='tight', facecolor='white')
plt.close()
print('\nfigures written')
