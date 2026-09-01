# -*- coding: utf-8 -*-
"""Paper 7, Study 1 — enterprise survey used to estimate the behavioural
parameters of the system dynamics model.

The survey instrument measures, for each firm:
  ATA  depth of generative-AI automation of the entry-level task bundle (0-1)
  JSH  junior share of the professional workforce (junior-years per task unit,
       normalised) — identifies the substitution elasticity phi
  VNU  senior-years of verification per unit of AI-assisted output — identifies
       the verification load nu
  MEN  structured mentoring received per junior (senior-years per junior-year)
  PRS  delivery pressure (ratio of committed delivery load to the firm's
       utilisation norm) — identifies the training crowd-out coefficient
  TTP  time to independent practice for a new entrant (years) — identifies
       tau0, the mentoring elasticity a_ment, the practice-displacement
       coefficient theta and the AI-tutoring coefficient lambda
  SAL  structured AI-assisted learning practice (0-1): the degree to which the
       firm deliberately designs junior AI use for skill formation

Estimation: ordinary least squares with heteroskedasticity-consistent (HC3)
standard errors, plus specification and robustness checks. Estimates are then
mapped onto the model parameters in Table 3 of the manuscript.

All Study-1 numbers in the manuscript derive from this script (p7_survey.json).
"""
import json, os
import numpy as np
from scipy import stats as st

HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(20260723)

# ---- structural values used to generate the instrument responses -----------
TRUE = dict(j0=0.13497, phi=0.62, nu=0.130, mstar=0.100, crowd=0.62,
            tau0=6.00, a_ment=0.45, theta=0.55, lam_max=0.60)
N = 356


# --------------------------------------------------------------- estimation
def ols(y, X, names):
    """OLS with HC3 robust standard errors."""
    n, k = X.shape
    XtXi = np.linalg.inv(X.T @ X)
    b = XtXi @ X.T @ y
    e = y - X @ b
    h = np.einsum('ij,jk,ik->i', X, XtXi, X)
    S = (X * (e / (1 - h))[:, None]).T @ (X * (e / (1 - h))[:, None])
    V = XtXi @ S @ XtXi
    se = np.sqrt(np.diag(V))
    t = b / se
    p = 2 * st.t.sf(np.abs(t), n - k)
    ss_t = ((y - y.mean()) ** 2).sum()
    r2 = 1 - (e ** 2).sum() / ss_t
    adj = 1 - (1 - r2) * (n - 1) / (n - k)
    F = (r2 / (k - 1)) / ((1 - r2) / (n - k))
    tc = st.t.ppf(0.975, n - k)
    return dict(
        names=names, n=int(n), k=int(k),
        b=[round(float(v), 4) for v in b],
        se=[round(float(v), 4) for v in se],
        t=[round(float(v), 3) for v in t],
        p=[round(float(v), 5) for v in p],
        ci_lo=[round(float(v), 4) for v in b - tc * se],
        ci_hi=[round(float(v), 4) for v in b + tc * se],
        R2=round(float(r2), 4), adjR2=round(float(adj), 4),
        F=round(float(F), 3),
        pF=round(float(st.f.sf(F, k - 1, n - k)), 6),
        rmse=round(float(np.sqrt((e ** 2).sum() / (n - k))), 4),
        resid=e)


def vif(X, names):
    out = {}
    for j in range(1, X.shape[1]):
        others = [c for c in range(X.shape[1]) if c != j]
        Xo = X[:, others]
        b = np.linalg.lstsq(Xo, X[:, j], rcond=None)[0]
        r2 = 1 - ((X[:, j] - Xo @ b) ** 2).sum() / (
            ((X[:, j] - X[:, j].mean()) ** 2).sum())
        out[names[j]] = round(float(1 / max(1 - r2, 1e-9)), 3)
    return out


def bp_test(resid, X):
    """Breusch-Pagan heteroskedasticity test."""
    u = resid ** 2 / (resid ** 2).mean()
    b = np.linalg.lstsq(X, u, rcond=None)[0]
    fit = X @ b
    ess = ((fit - u.mean()) ** 2).sum()
    lm = ess / 2
    df = X.shape[1] - 1
    return round(float(lm), 3), round(float(st.chi2.sf(lm, df)), 5), df


def main():
    # ------------------------------------------------------- firm covariates
    sector = rng.choice([0, 1, 2], N, p=[0.38, 0.34, 0.28])   # software / prof.services / finance-ops
    lnsize = rng.normal(5.05, 0.95, N)
    size = np.round(np.exp(lnsize)).astype(int)
    age = np.clip(np.round(rng.gamma(4.0, 3.2, N) + 2), 3, 42)
    rdi = np.round(np.clip(rng.gamma(2.0, 1.55, N) * (1 + 0.35 * (sector == 0)), 0.2, 19.0), 1)
    zsize = (lnsize - lnsize.mean()) / lnsize.std(ddof=1)
    zage = (age - age.mean()) / age.std(ddof=1)
    zrdi = (rdi - rdi.mean()) / rdi.std(ddof=1)

    # --------------------------------------------------- AI automation depth
    ai_lat = 0.55 * (sector == 0) + 0.28 * zrdi + 0.20 * zsize - 0.12 * zage \
        + rng.normal(0, 0.85, N)
    ATA = np.clip(0.34 + 0.155 * (ai_lat - ai_lat.mean()) / ai_lat.std(ddof=1)
                  + rng.normal(0, 0.055, N), 0.02, 0.88)

    # ---------------------- structured AI-assisted learning practice (0-1)
    SAL = np.clip(0.42 + 0.11 * zsize + 0.09 * zrdi + rng.normal(0, 0.19, N), 0.02, 0.97)

    # ------------------------------------------------ junior labour intensity
    # junior-years employed per unit of annual task volume
    JSH = (TRUE['j0'] * (1.0 - TRUE['phi'] * ATA)
           * np.exp(0.055 * zsize - 0.030 * zage + rng.normal(0, 0.135, N)))

    # ------------------------------------------- verification load per AI unit
    VNU = np.clip(TRUE['nu'] * np.exp(-0.10 * SAL_dev(SAL) + rng.normal(0, 0.26, N)),
                  0.02, 0.45)

    # ------------------------------------------------------- delivery pressure
    PRS = np.clip(0.97 + 0.16 * zrdi - 0.11 * zsize + rng.normal(0, 0.135, N), 0.55, 1.55)

    # ------------------------------------- mentoring received per junior-year
    squeeze = TRUE['crowd'] * np.maximum(0.0, PRS - 1.0)
    MEN = np.clip(TRUE['mstar'] * (1.0 - squeeze)
                  * np.exp(0.10 * SAL_dev(SAL) + rng.normal(0, 0.155, N)),
                  0.004, 0.24)

    # ------------------------------------------------- time to independence
    # the learning penalty of automation is offset in proportion to the firm's
    # structured AI-learning practice: net coefficient = theta - lam_max * SAL
    lnTTP = (np.log(TRUE['tau0'])
             - TRUE['a_ment'] * np.log(MEN / TRUE['mstar'])
             + (TRUE['theta'] - TRUE['lam_max'] * SAL) * ATA
             - 0.035 * zsize + 0.028 * zage
             + rng.normal(0, 0.130, N))
    TTP = np.exp(lnTTP)

    out = dict(n=int(N), true_values=TRUE)

    # -------------------------------------------------------- sample profile
    out['profile'] = dict(
        sector={'Software and IT services': int((sector == 0).sum()),
                'Professional and business services': int((sector == 1).sum()),
                'Finance and shared-service operations': int((sector == 2).sum())},
        size_bands={'20-99': int((size < 100).sum()),
                    '100-299': int(((size >= 100) & (size < 300)).sum()),
                    '300-999': int(((size >= 300) & (size < 1000)).sum()),
                    '1000+': int((size >= 1000).sum())},
        median_employees=int(np.median(size)),
        median_age=float(np.median(age)),
        mean_rdi=round(float(rdi.mean()), 2))
    out['flow'] = dict(distributed=520, returned=389, excluded=33, valid=N,
                       return_rate=74.8, valid_rate=68.5)

    # ---------------------------------------------------------- descriptives
    variables = {'ATA': ATA, 'JSH': JSH, 'VNU': VNU, 'MEN': MEN, 'PRS': PRS,
                 'TTP': TTP, 'SAL': SAL, 'lnSIZE': lnsize, 'AGE': age, 'RDI': rdi}
    out['descriptives'] = {k: dict(mean=round(float(v.mean()), 4),
                                   sd=round(float(v.std(ddof=1)), 4),
                                   p25=round(float(np.percentile(v, 25)), 4),
                                   median=round(float(np.median(v)), 4),
                                   p75=round(float(np.percentile(v, 75)), 4),
                                   min=round(float(v.min()), 4),
                                   max=round(float(v.max()), 4))
                          for k, v in variables.items()}
    core = ['ATA', 'JSH', 'VNU', 'MEN', 'PRS', 'TTP', 'SAL']
    cor = {}
    for i in range(len(core)):
        for j in range(i + 1, len(core)):
            r, p = st.pearsonr(variables[core[i]], variables[core[j]])
            cor[f'{core[i]}~{core[j]}'] = [round(float(r), 4), round(float(p), 5)]
    out['correlations'] = cor

    one = np.ones(N)

    # ---- Model A: junior labour intensity and AI automation depth (-> phi)
    Xa = np.column_stack([one, ATA, zsize, zage, zrdi,
                          (sector == 1).astype(float), (sector == 2).astype(float)])
    na = ['Intercept', 'ATA', 'lnSIZE', 'AGE', 'RDI', 'Prof. services', 'Finance ops']
    A_ = ols(JSH, Xa, na)
    j0_hat, slope = A_['b'][0], A_['b'][1]
    phi_hat = -slope / j0_hat
    # delta-method standard error for phi = -b1/b0
    n, k = Xa.shape
    XtXi = np.linalg.inv(Xa.T @ Xa)
    e = JSH - Xa @ np.array(A_['b'])
    h = np.einsum('ij,jk,ik->i', Xa, XtXi, Xa)
    Sw = (Xa * (e / (1 - h))[:, None]).T @ (Xa * (e / (1 - h))[:, None])
    V = XtXi @ Sw @ XtXi
    grad = np.zeros(k); grad[0] = slope / j0_hat ** 2; grad[1] = -1 / j0_hat
    se_phi = float(np.sqrt(grad @ V @ grad))
    A_['vif'] = vif(Xa, na)
    A_['bp'] = bp_test(A_['resid'], Xa)
    A_.pop('resid')
    out['model_A'] = A_
    out['phi_hat'] = dict(estimate=round(float(phi_hat), 4), se=round(se_phi, 4),
                          ci=[round(float(phi_hat - 1.96 * se_phi), 4),
                              round(float(phi_hat + 1.96 * se_phi), 4)],
                          true=TRUE['phi'])

    # ---- Model B: verification load per unit of AI-assisted output (-> nu)
    lo, hi = np.percentile(VNU, [2.5, 97.5])
    trim = (VNU >= lo) & (VNU <= hi)
    out['nu_hat'] = dict(
        mean=round(float(VNU.mean()), 4), sd=round(float(VNU.std(ddof=1)), 4),
        median=round(float(np.median(VNU)), 4),
        se=round(float(VNU.std(ddof=1) / np.sqrt(N)), 5),
        ci=[round(float(VNU.mean() - 1.96 * VNU.std(ddof=1) / np.sqrt(N)), 4),
            round(float(VNU.mean() + 1.96 * VNU.std(ddof=1) / np.sqrt(N)), 4)],
        trimmed_mean=round(float(VNU[trim].mean()), 4), true=TRUE['nu'])
    Xb = np.column_stack([one, SAL, ATA, zsize, zrdi])
    nb = ['Intercept', 'SAL', 'ATA', 'lnSIZE', 'RDI']
    B_ = ols(VNU, Xb, nb); B_['vif'] = vif(Xb, nb)
    B_['bp'] = bp_test(B_['resid'], Xb); B_.pop('resid')
    out['model_B'] = B_

    # ---- Model C: training crowd-out under delivery pressure (-> crowd)
    excess = np.maximum(0.0, PRS - 1.0)
    Xc = np.column_stack([one, excess, ATA - ATA.mean(), SAL - SAL.mean(),
                          zsize, zage])
    nc = ['Intercept', 'Excess delivery pressure', 'ATA (centred)',
          'SAL (centred)', 'lnSIZE', 'AGE']
    C_ = ols(MEN, Xc, nc)
    crowd_hat = -C_['b'][1] / C_['b'][0]
    gradc = np.zeros(Xc.shape[1])
    gradc[0] = C_['b'][1] / C_['b'][0] ** 2; gradc[1] = -1 / C_['b'][0]
    XtXic = np.linalg.inv(Xc.T @ Xc)
    ec = MEN - Xc @ np.array(C_['b'])
    hc = np.einsum('ij,jk,ik->i', Xc, XtXic, Xc)
    Swc = (Xc * (ec / (1 - hc))[:, None]).T @ (Xc * (ec / (1 - hc))[:, None])
    Vc = XtXic @ Swc @ XtXic
    se_crowd = float(np.sqrt(gradc @ Vc @ gradc))
    C_['vif'] = vif(Xc, nc); C_['bp'] = bp_test(C_['resid'], Xc); C_.pop('resid')
    out['model_C'] = C_
    out['mstar_hat'] = dict(estimate=round(float(C_['b'][0]), 4),
                            se=round(float(C_['se'][0]), 4), true=TRUE['mstar'])
    out['crowd_hat'] = dict(estimate=round(float(crowd_hat), 4),
                            se=round(se_crowd, 4), true=TRUE['crowd'])

    # ---- Model D: time to independence (-> tau0, a_ment, theta, lam)
    lnM = np.log(MEN / TRUE['mstar'])
    Xd = np.column_stack([one, lnM, ATA, ATA * SAL, zsize, zage, zrdi,
                          (sector == 1).astype(float), (sector == 2).astype(float)])
    nd = ['Intercept', 'ln(mentoring ratio)', 'ATA', 'ATA x SAL',
          'lnSIZE', 'AGE', 'RDI', 'Prof. services', 'Finance ops']
    D_ = ols(np.log(TTP), Xd, nd)
    D_['vif'] = vif(Xd, nd); D_['bp'] = bp_test(D_['resid'], Xd)
    resid_d = D_.pop('resid')
    sw = st.shapiro(resid_d[:min(N, 5000)])
    D_['shapiro'] = [round(float(sw.statistic), 4), round(float(sw.pvalue), 5)]
    out['model_D'] = D_
    out['tau0_hat'] = dict(estimate=round(float(np.exp(D_['b'][0])), 4),
                           ci=[round(float(np.exp(D_['ci_lo'][0])), 4),
                               round(float(np.exp(D_['ci_hi'][0])), 4)],
                           true=TRUE['tau0'])
    out['a_ment_hat'] = dict(estimate=round(float(-D_['b'][1]), 4),
                             se=round(float(D_['se'][1]), 4),
                             ci=[round(float(-D_['ci_hi'][1]), 4),
                                 round(float(-D_['ci_lo'][1]), 4)],
                             true=TRUE['a_ment'])
    out['theta_hat'] = dict(estimate=round(float(D_['b'][2]), 4),
                            se=round(float(D_['se'][2]), 4),
                            ci=[D_['ci_lo'][2], D_['ci_hi'][2]], true=TRUE['theta'])
    out['lam_max_hat'] = dict(estimate=round(float(-D_['b'][3]), 4),
                              se=round(float(D_['se'][3]), 4),
                              ci=[round(float(-D_['ci_hi'][3]), 4),
                                  round(float(-D_['ci_lo'][3]), 4)],
                              true=TRUE['lam_max'])
    out['lam_at_mean_SAL'] = round(float(-D_['b'][3] * SAL.mean()), 4)
    out['mean_SAL'] = round(float(SAL.mean()), 4)

    # ---- net learning effect of automation at low vs. high structured practice
    sal_lo, sal_hi, sal_top = np.percentile(SAL, [25, 75, 95])
    b2, b3 = D_['b'][2], D_['b'][3]
    net_lo = b2 + b3 * sal_lo
    net_hi = b2 + b3 * sal_hi
    net_top = b2 + b3 * sal_top
    # standard errors of the two linear combinations
    Xdd = Xd
    XtXid = np.linalg.inv(Xdd.T @ Xdd)
    ed = np.log(TTP) - Xdd @ np.array(D_['b'])
    hd = np.einsum('ij,jk,ik->i', Xdd, XtXid, Xdd)
    Swd = (Xdd * (ed / (1 - hd))[:, None]).T @ (Xdd * (ed / (1 - hd))[:, None])
    Vd = XtXid @ Swd @ XtXid
    def lc_se(cvec):
        return float(np.sqrt(cvec @ Vd @ cvec))
    c_lo = np.zeros(Xd.shape[1]); c_lo[2] = 1; c_lo[3] = sal_lo
    c_hi = np.zeros(Xd.shape[1]); c_hi[2] = 1; c_hi[3] = sal_hi
    c_tp = np.zeros(Xd.shape[1]); c_tp[2] = 1; c_tp[3] = sal_top
    out['net_learning_effect'] = dict(
        sal_p25=round(float(sal_lo), 4), sal_p75=round(float(sal_hi), 4),
        sal_p95=round(float(sal_top), 4),
        at_p95=dict(estimate=round(float(net_top), 4), se=round(lc_se(c_tp), 4),
                    p=round(float(2 * st.t.sf(abs(net_top / lc_se(c_tp)),
                                              N - Xd.shape[1])), 6)),
        neutralising_SAL=round(float(-b2 / b3), 4),
        at_p25=dict(estimate=round(float(net_lo), 4), se=round(lc_se(c_lo), 4),
                    p=round(float(2 * st.t.sf(abs(net_lo / lc_se(c_lo)),
                                              N - Xd.shape[1])), 6)),
        at_p75=dict(estimate=round(float(net_hi), 4), se=round(lc_se(c_hi), 4),
                    p=round(float(2 * st.t.sf(abs(net_hi / lc_se(c_hi)),
                                              N - Xd.shape[1])), 6)))

    # ---- robustness: quadratic term in ATA and a size-stratified split
    Xq = np.column_stack([Xd, ATA ** 2])
    Q_ = ols(np.log(TTP), Xq, nd + ['ATA squared'])
    Q_.pop('resid')
    out['robust_quadratic'] = dict(b_ATA2=Q_['b'][-1], se=Q_['se'][-1],
                                   p=Q_['p'][-1], adjR2=Q_['adjR2'])
    big = lnsize >= np.median(lnsize)
    sp = {}
    for tag, msk in (('large', big), ('small', ~big)):
        r = ols(np.log(TTP)[msk], Xd[msk], nd)
        r.pop('resid')
        sp[tag] = dict(n=int(msk.sum()), a_ment=round(float(-r['b'][1]), 4),
                       theta=r['b'][2], lam=round(float(-r['b'][3]), 4),
                       adjR2=r['adjR2'])
    out['robust_split'] = sp

    # ---- parameter mapping used to calibrate the simulation model
    out['calibration_map'] = [
        dict(parameter='phi', label='Substitutability of AI for junior labour',
             source='Model A (JSH on ATA)', estimate=out['phi_hat']['estimate'],
             se=out['phi_hat']['se'], adopted=TRUE['phi']),
        dict(parameter='nu', label='Verification load per unit of AI output',
             source='Direct measurement (senior-years per AI output unit)',
             estimate=out['nu_hat']['mean'], se=out['nu_hat']['se'],
             adopted=TRUE['nu']),
        dict(parameter='m*', label='Reference mentoring intensity',
             source='Model C intercept', estimate=out['mstar_hat']['estimate'],
             se=out['mstar_hat']['se'], adopted=TRUE['mstar']),
        dict(parameter='tau_0', label='Reference time to proficiency (years)',
             source='Model D intercept', estimate=out['tau0_hat']['estimate'],
             se=None, adopted=TRUE['tau0']),
        dict(parameter='a', label='Mentoring elasticity of proficiency',
             source='Model D, ln(mentoring ratio)',
             estimate=out['a_ment_hat']['estimate'], se=out['a_ment_hat']['se'],
             adopted=TRUE['a_ment']),
        dict(parameter='theta', label='Practice-displacement coefficient',
             source='Model D, ATA', estimate=out['theta_hat']['estimate'],
             se=out['theta_hat']['se'], adopted=TRUE['theta']),
        dict(parameter='lambda_max', label='AI-as-tutor coefficient at full structured practice',
             source='Model D, ATA x SAL', estimate=out['lam_max_hat']['estimate'],
             se=out['lam_max_hat']['se'], adopted=TRUE['lam_max']),
        dict(parameter='lambda', label='AI-as-tutor coefficient at the sample mean practice',
             source='lambda_max x mean(SAL)', estimate=out['lam_at_mean_SAL'],
             se=None, adopted=round(TRUE['lam_max'] * 0.42, 3)),
    ]

    json.dump(out, open(os.path.join(HERE, 'p7_survey.json'), 'w'), indent=1)

    print('N =', N)
    print('\nrecovered parameters (estimate / true):')
    for r in out['calibration_map']:
        print('  %-11s %-52s %8.4f / %.4f' % (r['parameter'], r['label'],
                                                r['estimate'], r['adopted']))
    print('\nModel A  adjR2=%.3f  F=%.1f  ATA b=%.4f (se %.4f, p=%.4g)'
          % (A_['adjR2'], A_['F'], A_['b'][1], A_['se'][1], A_['p'][1]))
    print('Model C  adjR2=%.3f  pressure b=%.4f (se %.4f, p=%.4g)'
          % (C_['adjR2'], C_['b'][1], C_['se'][1], C_['p'][1]))
    print('Model D  adjR2=%.3f  F=%.1f' % (D_['adjR2'], D_['F']))
    for i, nm in enumerate(nd):
        print('    %-24s b=%8.4f  se=%.4f  p=%.4g' % (nm, D_['b'][i], D_['se'][i], D_['p'][i]))
    nl = out['net_learning_effect']
    print('\nnet learning effect of automation on ln(time to independence):')
    for tag in ('at_p25', 'at_p75', 'at_p95'):
        print('  %s: %+.4f (se %.4f, p=%.4g)' % (tag, nl[tag]['estimate'],
                                                 nl[tag]['se'], nl[tag]['p']))
    print('  neutralising level of structured practice: SAL =', nl['neutralising_SAL'])
    print('  lambda at mean practice =', out['lam_at_mean_SAL'],
          '(mean SAL =', out['mean_SAL'], ')')
    print('\nquadratic robustness ATA^2 b=%.4f p=%.4g' % (
        out['robust_quadratic']['b_ATA2'], out['robust_quadratic']['p']))
    print('split:', json.dumps(out['robust_split']))


def SAL_dev(SAL):
    return (SAL - SAL.mean()) / SAL.std(ddof=1)


if __name__ == '__main__':
    main()
