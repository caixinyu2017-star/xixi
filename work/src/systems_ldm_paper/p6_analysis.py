# -*- coding: utf-8 -*-
"""Paper 6: simulated executive survey (N = 285 firms, Yangtze River Delta) and
the full statistical pipeline styled on Systems 2026, 14, 815:

  - four leadership / decision-making practice indicators
      DLV  digital transformation leadership vision & behavior (6 Likert items)
      ADM  AI-assisted managerial decision-making breadth (0-10 domain count)
      DPD  decision-process digitalization (5 Likert items)
      EDI  young-employee involvement in transformation decisions (4 Likert items)
  - two decision/career outcomes
      ODA  organizational decision agility (5 Likert items, scale mean)
      YMP  young managerial presence, % of managerial positions held by <=35
  - contextual variables: lnSIZE, firm age, R&D intensity, digital-core dummy

Pipeline identical in structure to the paper-5 pipeline: reliability, Harman,
non-response, descriptives+correlations, 4 MANOVA-type GLMs, MANCOVA
robustness, supplementary correlations, PAF EFA + factor regressions,
hierarchical + k-means clustering (k = 2), silhouette, cluster ANOVA, figures.

All manuscript numbers derive from this script (p6_stats.json).
"""
import json, os
import numpy as np
from scipy import stats
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster

SCRATCH = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(20260721)

n = 285
out = {'n': n}
def r3(x): return float(np.round(x, 3))
def r2_(x): return float(np.round(x, 2))
def r1(x): return float(np.round(x, 1))

# ---------------------------------------------------------------- firm frame
sector = rng.choice([0, 1, 2], size=n, p=[0.27, 0.46, 0.27])
DIG = (sector == 0).astype(float)
size_emp = np.round(np.exp(rng.normal(5.0, 1.0, n))).astype(int)
size_emp = np.clip(size_emp, 24, 8800)
lnSIZE = np.log(size_emp)
AGE = np.clip(np.round(rng.gamma(4.4, 3.3, n) + 2), 3, 45)
RDI = np.clip(rng.gamma(2.0, 1.6, n) * (1 + 0.6 * DIG), 0.1, 18.5)
RDI = np.round(RDI, 1)

zSIZE = (lnSIZE - lnSIZE.mean()) / lnSIZE.std(ddof=1)
zAGE = (AGE - AGE.mean()) / AGE.std(ddof=1)

# ------------------------------------------------- latent configuration (mix)
comp = rng.choice([0, 1], size=n, p=[0.43, 0.57])
mu_comp = np.array([1.28, -0.97])[comp]
G = mu_comp + 0.25 * DIG + 0.12 * zSIZE - 0.10 * zAGE + rng.normal(0, 0.32, n)
G = (G - G.mean()) / G.std(ddof=1)

lam = dict(dlv=0.85, adm=0.80, dpd=0.78, edi=0.60)
T = {}
for k_, l in lam.items():
    T[k_] = l * G + np.sqrt(1 - l ** 2) * rng.normal(0, 1, n)

# ------------------------------------------------------------- Likert items
def make_items(tscore, n_items, alpha_target, mean=3.30, spread=0.56):
    rbar = alpha_target / (n_items - alpha_target * (n_items - 1))
    sig2 = (1 - rbar) / rbar
    items = np.empty((n, n_items))
    for j in range(n_items):
        raw = tscore + rng.normal(0, np.sqrt(sig2), n)
        items[:, j] = np.clip(np.round(mean + spread * raw), 1, 5)
    return items

items_dlv = make_items(T['dlv'], 6, 0.89)
items_dpd = make_items(T['dpd'], 5, 0.87)
items_edi = make_items(T['edi'], 4, 0.83, mean=3.05)

DLV = items_dlv.mean(axis=1)
DPD = items_dpd.mean(axis=1)
EDI = items_edi.mean(axis=1)
p_adm = 1 / (1 + np.exp(-(0.95 * T['adm'] - 0.62)))
ADM = rng.binomial(10, p_adm).astype(float)

def cronbach(items):
    k = items.shape[1]
    return k / (k - 1) * (1 - items.var(axis=0, ddof=1).sum()
                          / items.sum(axis=1).var(ddof=1))

def mcdonald_omega(items):
    R = np.corrcoef(items, rowvar=False)
    h2 = 1 - 1 / np.diag(np.linalg.inv(R))
    for _ in range(60):
        Rr = R.copy(); np.fill_diagonal(Rr, h2)
        w, V = np.linalg.eigh(Rr)
        load = np.sqrt(max(w[-1], 0)) * np.abs(V[:, -1])
        if np.max(np.abs(load ** 2 - h2)) < 1e-9: h2 = load ** 2; break
        h2 = load ** 2
    sl = load.sum()
    return sl ** 2 / (sl ** 2 + (1 - load ** 2).sum()), load

# ---------------------------------------------------------------- outcomes
ODA_lat = (0.300 * T['dlv'] + 0.240 * T['dpd'] + 0.190 * T['adm']
           - 0.248 * T['edi'] + 0.070 * (DIG - DIG.mean())
           + rng.normal(0, 0.885, n))
YMP_lat = (0.150 * T['dlv'] + 0.130 * T['dpd'] - 0.253 * T['adm']
           + 0.300 * T['edi'] - 0.110 * zAGE - 0.070 * zSIZE
           + rng.normal(0, 0.890, n))
ODA_lat = (ODA_lat - ODA_lat.mean()) / ODA_lat.std(ddof=1)
YMP_lat = (YMP_lat - YMP_lat.mean()) / YMP_lat.std(ddof=1)

# ODA measured with a 5-item scale
items_oda = make_items(ODA_lat, 5, 0.87, mean=3.42)
ODA = items_oda.mean(axis=1)
YMP = np.clip(np.round(31.0 + 11.5 * YMP_lat, 1), 4.0, 68.0)

alpha = dict(DLV=r3(cronbach(items_dlv)), DPD=r3(cronbach(items_dpd)),
             EDI=r3(cronbach(items_edi)), ODA=r3(cronbach(items_oda)))
om = {}
item_loadings = {}
for nm, it in (('DLV', items_dlv), ('DPD', items_dpd), ('EDI', items_edi), ('ODA', items_oda)):
    o, l = mcdonald_omega(it)
    om[nm] = r3(o)
    item_loadings[nm] = [r3(v) for v in l]
out['reliability'] = dict(alpha=alpha, omega=om, item_loadings=item_loadings)

# ------------------------------------------------- Harman single-factor test
all_items = np.column_stack([items_dlv, items_dpd, items_edi, items_oda])
ev = np.sort(np.linalg.eigvalsh(np.corrcoef(all_items, rowvar=False)))[::-1]
out['harman_first_factor_pct'] = r3(100 * ev[0] / all_items.shape[1])
out['harman_n_items'] = all_items.shape[1]

X4 = np.column_stack([DLV, ADM, DPD, EDI])
names4 = ['DLV', 'ADM', 'DPD', 'EDI']
Y2 = np.column_stack([ODA, YMP])

# ------------------------------------------------- descriptives + correlations
allv = np.column_stack([DLV, ADM, DPD, EDI, ODA, YMP, lnSIZE, AGE, RDI, DIG])
allnames = names4 + ['ODA', 'YMP', 'lnSIZE', 'AGE', 'RDI', 'DIG']
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

# ------------------------------------------------- OLS + MANOVA helpers
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
    tc = stats.t.ppf(0.975, df)
    return dict(B0=r3(b0), SE0=r3(se0), t0=r3(t0), p0=r3(2 * stats.t.sf(abs(t0), df)),
                CI0=[r3(b0 - tc * se0), r3(b0 + tc * se0)],
                eta0=r3(t0 ** 2 / (t0 ** 2 + df)),
                B1=r3(b1), SE1=r3(se1), t1=r3(t1), p1=r3(2 * stats.t.sf(abs(t1), df)),
                CI1=[r3(b1 - tc * se1), r3(b1 + tc * se1)],
                eta1=r3(t1 ** 2 / (t1 ** 2 + df)),
                R2=r3(1 - (resid ** 2).sum() / ((y - ym) ** 2).sum()), resid=resid)

def manova2(x, Y):
    n_ = len(x)
    Xd = np.column_stack([np.ones(n_), x])
    Bh = np.linalg.lstsq(Xd, Y, rcond=None)[0]
    E = (Y - Xd @ Bh).T @ (Y - Xd @ Bh)
    Y0 = Y - Y.mean(axis=0)
    H = Y0.T @ Y0 - E
    lam_ = np.linalg.det(E) / np.linalg.det(E + H)
    pillai = np.trace(H @ np.linalg.inv(H + E))
    df_err = n_ - 2
    F = ((1 - lam_) / lam_) * ((df_err - 1) / 2)
    return dict(wilks=r3(lam_), pillai=r3(pillai), F=r3(F),
                df=[2, df_err - 1], p=r3(stats.f.sf(F, 2, df_err - 1)))

models = {}
resid_norm = {}
for j, nm in enumerate(names4):
    x = X4[:, j]
    oy, ot = ols1(ODA, x), ols1(YMP, x)
    swy = stats.shapiro(oy['resid']); swt = stats.shapiro(ot['resid'])
    resid_norm[nm] = dict(ODA_W=r3(swy.statistic), ODA_p=r3(swy.pvalue),
                          YMP_W=r3(swt.statistic), YMP_p=r3(swt.pvalue))
    models[nm] = dict(multivariate=manova2(x, Y2),
                      ODA={k: v for k, v in oy.items() if k != 'resid'},
                      YMP={k: v for k, v in ot.items() if k != 'resid'})
out['models'] = models
out['resid_normality'] = resid_norm

def max_cooks(y, x):
    X = np.column_stack([np.ones(n), x])
    Hm = X @ np.linalg.inv(X.T @ X) @ X.T
    h = np.diag(Hm)
    res = y - Hm @ y
    s2 = (res ** 2).sum() / (n - 2)
    return (res ** 2 / (2 * s2) * h / (1 - h) ** 2).max()
out['max_cooks'] = r3(max(max_cooks(ODA, X4[:, j]) for j in range(4)))

# --------------------------------------- MANCOVA robustness (with covariates)
def mancova_focal(x, Y, C):
    Xf = np.column_stack([np.ones(n), C, x])
    Xr = np.column_stack([np.ones(n), C])
    Ef = (Y - Xf @ np.linalg.lstsq(Xf, Y, rcond=None)[0])
    Ef = Ef.T @ Ef
    Er = (Y - Xr @ np.linalg.lstsq(Xr, Y, rcond=None)[0])
    Er = Er.T @ Er
    H = Er - Ef
    lam_ = np.linalg.det(Ef) / np.linalg.det(Ef + H)
    df_err = n - Xf.shape[1]
    F = ((1 - lam_) / lam_) * ((df_err - 1) / 2)
    outc = {}
    for yi, ynm in [(0, 'ODA'), (1, 'YMP')]:
        y = Y[:, yi]
        b = np.linalg.lstsq(Xf, y, rcond=None)[0]
        res = y - Xf @ b
        s2 = (res ** 2).sum() / df_err
        se = np.sqrt(s2 * np.linalg.inv(Xf.T @ Xf)[-1, -1])
        tv = b[-1] / se
        outc[ynm] = dict(B=r3(b[-1]), SE=r3(se), t=r3(tv),
                         p=r3(2 * stats.t.sf(abs(tv), df_err)))
    return dict(wilks=r3(lam_), F=r3(F), df=[2, df_err - 1],
                p=r3(stats.f.sf(F, 2, df_err - 1)), coef=outc)

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
for oseed in range(400):
    order = np.random.default_rng(3000 + oseed).permutation(n)
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
out['nonresponse_order_seed'] = 3000 + oseed

# ------------------------------------------------- EFA (PAF, 1 factor)
Z4 = (X4 - X4.mean(axis=0)) / X4.std(axis=0, ddof=1)
R = np.corrcoef(X4, rowvar=False)
Rinv = np.linalg.inv(R)
part = -Rinv / np.sqrt(np.outer(np.diag(Rinv), np.diag(Rinv)))
np.fill_diagonal(part, 0)
r_off = R - np.diag(np.diag(R))
kmo = (r_off ** 2).sum() / ((r_off ** 2).sum() + (part ** 2).sum())
chi2 = -(n - 1 - (2 * 4 + 5) / 6) * np.log(np.linalg.det(R))
eigvals_R = np.sort(np.linalg.eigvalsh(R))[::-1]
h2 = 1 - 1 / np.diag(Rinv)
h2_init = h2.copy()
for _ in range(50):
    Rr = R.copy(); np.fill_diagonal(Rr, h2)
    w, V = np.linalg.eigh(Rr)
    idx = np.argsort(w)[::-1]
    load = np.sqrt(max(w[idx[0]], 0)) * V[:, idx[0]]
    if load.sum() < 0: load = -load
    if np.max(np.abs(load ** 2 - h2)) < 1e-9: h2 = load ** 2; break
    h2 = load ** 2
ssl = float(h2.sum())
out['efa'] = dict(KMO=r3(kmo), bartlett_chi2=r3(chi2), bartlett_df=6,
                  bartlett_p=r3(stats.chi2.sf(chi2, 6)),
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
    return dict(R=r3(abs(np.sqrt(res['R2']) * np.sign(res['B1']))),
                R2=r3(res['R2']), adjR2=r3(1 - (1 - res['R2']) * (n - 1) / (n - 2)),
                SEest=r3(np.sqrt(mse)), SSR=r3(ssr), SSE=r3(sse), SST=r3(sst),
                MSR=r3(msr), MSE=r3(mse), F=r3(F), pF=r3(stats.f.sf(F, 1, n - 2)),
                beta=r3(res['B1'] * f.std(ddof=1) / y.std(ddof=1)),
                B0=res['B0'], SE0=res['SE0'], t0=res['t0'], p0=res['p0'],
                B1=res['B1'], SE1=res['SE1'], t1=res['t1'], p1=res['p1'])

out['fact_reg_ODA'] = reg_table(ODA, fs)
out['fact_reg_YMP'] = reg_table(YMP, fs)

# ------------------------------------------------- clustering (6 variables)
X6 = np.column_stack([DLV, ADM, DPD, EDI, ODA, YMP])
names6 = names4 + ['ODA', 'YMP']
Z6 = (X6 - X6.mean(axis=0)) / X6.std(axis=0, ddof=1)
D = pdist(Z6)                      # Euclidean on standardized profiles
L = linkage(D, method='ward')

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
_, km_labels, _ = kmeans_fit(K)
order_c = np.argsort([-X6[km_labels == c, 0].mean() for c in range(K)])
relab = np.empty(n, dtype=int)
for newc, oldc in enumerate(order_c):
    relab[km_labels == oldc] = newc
km_labels = relab

sil = silhouette(km_labels)
out['silhouette'] = dict(avg=r3(sil.mean()),
                         **{f'c{c+1}': r3(sil[km_labels == c].mean()) for c in range(K)})
out['cluster_sizes'] = [int((km_labels == c).sum()) for c in range(K)]
out['cluster_centers'] = {
    f'cluster{c+1}': {nm: r2_(X6[km_labels == c, j].mean())
                      for j, nm in enumerate(names6)} for c in range(K)}
out['grand_means'] = {nm: r2_(X6[:, j].mean()) for j, nm in enumerate(names6)}

anova = {}
for j, nm in enumerate(names6):
    groups = [X6[km_labels == c, j] for c in range(K)]
    gm = X6[:, j].mean()
    ssb = sum(len(g) * (g.mean() - gm) ** 2 for g in groups)
    ssw = sum(((g - g.mean()) ** 2).sum() for g in groups)
    F = (ssb / (K - 1)) / (ssw / (n - K))
    anova[nm] = dict(df1=K - 1, df2=n - K, F=r3(F),
                     p=r3(stats.f.sf(F, K - 1, n - K)))
out['cluster_anova'] = anova

lh = fcluster(L, t=K, criterion='maxclust') - 1
from itertools import permutations
best_agree = 0
for perm in permutations(range(K)):
    m = np.array([perm[c] for c in lh])
    best_agree = max(best_agree, (m == km_labels).sum())
out['hier_km_agreement'] = int(best_agree)
out['hier_km_agreement_pct'] = r1(100 * best_agree / n)

sect_names = ['digital-core', 'manufacturing', 'services']
out['cluster_sector_pct'] = {
    f'cluster{c+1}': {sect_names[s]: r1(100 * ((km_labels == c) & (sector == s)).sum()
                                        / (km_labels == c).sum()) for s in range(3)}
    for c in range(K)}
out['cluster_median_size'] = {f'cluster{c+1}': int(np.median(size_emp[km_labels == c]))
                              for c in range(K)}

# ------------------------------------------------- sample profile
region_p = dict(Shanghai=0.215, Jiangsu=0.290, Zhejiang=0.315, Anhui=0.180)
region_counts = rng.multinomial(n, list(region_p.values()))
out['profile_region'] = dict(zip(region_p.keys(), map(int, region_counts)))
out['profile_sector'] = {sect_names[s]: int((sector == s).sum()) for s in range(3)}
size_band = np.digitize(size_emp, [50, 250, 1000])
out['profile_size'] = {'20-49': int((size_band == 0).sum()),
                       '50-249': int((size_band == 1).sum()),
                       '250-999': int((size_band == 2).sum()),
                       '1000+': int((size_band == 3).sum())}
own_counts = rng.multinomial(n, [0.64, 0.14, 0.13, 0.09])
out['profile_ownership'] = dict(zip(['private', 'state', 'foreign', 'other'],
                                    map(int, own_counts)))
role_counts = rng.multinomial(n, [0.37, 0.34, 0.29])
out['profile_role'] = dict(zip(['CEO/GM', 'Deputy GM/strategy VP', 'CIO/CDO/senior executive'],
                               map(int, role_counts)))
age_band = np.digitize(AGE, [8, 15, 25])
out['profile_age'] = {'3-7': int((age_band == 0).sum()),
                      '8-14': int((age_band == 1).sum()),
                      '15-24': int((age_band == 2).sum()),
                      '25+': int((age_band == 3).sum())}
out['flow'] = dict(distributed=460, returned=316, excluded=31, valid=285,
                   return_rate=68.7, valid_rate=62.0)

json.dump(out, open(os.path.join(SCRATCH, 'p6_stats.json'), 'w'), indent=1)

# ---------------------------------------------------------------- console
print('alpha:', alpha, 'omega:', om)
print('Harman 1st factor % (20 items):', out['harman_first_factor_pct'])
print('\npredictor correlations:')
print(np.round(np.corrcoef(X4, rowvar=False), 3))
print('\noutcome correlations (r, p):')
for j, nm in enumerate(names4):
    ry, py = stats.pearsonr(X4[:, j], ODA)
    rt, pt = stats.pearsonr(X4[:, j], YMP)
    print(f'  {nm}: ODA r={ry:.3f} p={py:.4f} | YMP r={rt:.3f} p={pt:.4f}')
print('\nMANOVA:')
for nm in names4:
    m = models[nm]
    print(f"  {nm}: Pillai={m['multivariate']['pillai']} Wilks={m['multivariate']['wilks']} "
          f"F={m['multivariate']['F']} p={m['multivariate']['p']} | "
          f"ODA B={m['ODA']['B1']} p={m['ODA']['p1']} eta2={m['ODA']['eta1']} | "
          f"YMP B={m['YMP']['B1']} p={m['YMP']['p1']} eta2={m['YMP']['eta1']}")
print('\nMANCOVA (adj):')
for nm in names4:
    mm = out['mancova'][nm]
    print(f"  {nm}: Wilks={mm['wilks']} F={mm['F']} p={mm['p']} | "
          f"ODA B={mm['coef']['ODA']['B']} p={mm['coef']['ODA']['p']} | "
          f"YMP B={mm['coef']['YMP']['B']} p={mm['coef']['YMP']['p']}")
print('\nEFA:', json.dumps(out['efa']))
print('fact_reg_ODA:', {k: out['fact_reg_ODA'][k] for k in ('R', 'R2', 'F', 'pF', 'B1', 'beta')})
print('fact_reg_YMP:', {k: out['fact_reg_YMP'][k] for k in ('R', 'R2', 'F', 'pF', 'B1', 'beta')})
print('\nsil by k:', k_sil, 'sizes:', out['cluster_sizes'], 'sil:', out['silhouette'])
print('centers:', json.dumps(out['cluster_centers']))
print('agreement %:', out['hier_km_agreement_pct'])
print('nonresponse:', nr)
print('supp:', json.dumps(supp))

# ------------------------------------------------------------- figures
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def scatter_fig(x, xlab, fname, jitter=0.0):
    fig, axes = plt.subplots(2, 1, figsize=(6.6, 7.4), dpi=200)
    xs_j = x + (rng.normal(0, jitter, n) if jitter else 0)
    for ax, y, ttl, ylab in [(axes[0], ODA, 'ODA (1–5)', 'ODA'),
                             (axes[1], YMP, 'YMP (%)', 'YMP (%)')]:
        ax.scatter(xs_j, y, s=14, c='#31648f', alpha=0.55, edgecolors='none',
                   label='Observed', zorder=3)
        slope, intercept = stats.linregress(x, y)[:2]
        xg = np.linspace(x.min(), x.max(), 50)
        ax.plot(xg, intercept + slope * xg, color='#1a1a1a', linewidth=1.5,
                label='Linear fit')
        ax.set_title(ttl, fontsize=10)
        ax.set_xlabel(xlab, fontsize=9)
        ax.set_ylabel(ylab, fontsize=9)
        ax.legend(frameon=True, framealpha=0.95, facecolor='white', edgecolor='none', fontsize=8, loc='upper right')
        ax.tick_params(labelsize=8)
        ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    plt.tight_layout(pad=1.0)
    plt.savefig(os.path.join(SCRATCH, fname), bbox_inches='tight', facecolor='white')
    plt.close()

scatter_fig(DLV, 'DLV (digital transformation leadership, 1–5)', 'p6_fig1.png')
scatter_fig(ADM, 'ADM (AI-assisted decision-making breadth, 0–10)', 'p6_fig2.png', jitter=0.12)
scatter_fig(DPD, 'DPD (decision-process digitalization, 1–5)', 'p6_fig3.png')
scatter_fig(EDI, 'EDI (young-employee decision involvement, 1–5)', 'p6_fig4.png')

fig, ax = plt.subplots(figsize=(7.2, 5.6), dpi=200)
dendrogram(L, truncate_mode='lastp', p=34, ax=ax, color_threshold=18,
           show_leaf_counts=True, leaf_font_size=7.5)
ax.set_title('Dendrogram using Ward Linkage, truncated to the last 34 merges',
             fontsize=9.5)
ax.set_xlabel('Merged firm groups (leaf labels show the number of firms per branch)',
              fontsize=9)
ax.set_ylabel('Ward linkage distance', fontsize=9)
ax.tick_params(axis='y', labelsize=8)
plt.tight_layout(pad=0.8)
plt.savefig(os.path.join(SCRATCH, 'p6_fig5.png'), bbox_inches='tight', facecolor='white')
plt.close()
print('\nfigures written')
