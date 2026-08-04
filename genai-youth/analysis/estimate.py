# -*- coding: utf-8 -*-
"""
Estimation for "The Vanishing First Rung".

All tables in the manuscript are produced by this script from data/panel.csv.
Run:  python3 estimate.py
"""
from __future__ import annotations

import os
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from linearmodels.iv import IV2SLS
from linearmodels.panel import PanelOLS

warnings.filterwarnings('ignore')

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data', 'panel.csv')
TAB = os.path.join(HERE, '..', 'tables')
RAW = os.path.join(HERE, 'out')
os.makedirs(TAB, exist_ok=True)
os.makedirs(RAW, exist_ok=True)

CTRL = ['Size', 'ROA', 'Lev', 'Growth', 'TobinQ', 'Board', 'Indep', 'Dual',
        'FirmAge', 'Fixed', 'Intan', 'CR']
SEED = 20260804


# ----------------------------------------------------------------------------------
def _index(d):
    """MultiIndex for linearmodels, with distinct names so that groupby('firm')
    on the columns is never ambiguous."""
    idx = pd.MultiIndex.from_arrays([d.firm.to_numpy(), d.year.to_numpy()],
                                    names=['eid', 'yr'])
    return d.set_index(idx)


def load():
    return _index(pd.read_csv(DATA))


def stars(p):
    return '***' if p < 0.01 else ('**' if p < 0.05 else ('*' if p < 0.10 else ''))


def cell(b, se, p, dec=4):
    return f'{b:.{dec}f}{stars(p)}', f'({se:.{dec}f})'


def fe_reg(d, y, xs, entity=True, time=True, cluster='firm', extra_index=None):
    """Two-way fixed-effects OLS with clustered standard errors."""
    dd = d.dropna(subset=[y] + xs).copy()
    X = sm.add_constant(dd[xs])
    mod = PanelOLS(dd[y], X, entity_effects=entity, time_effects=time,
                   check_rank=False, drop_absorbed=True)
    if cluster == 'firm':
        res = mod.fit(cov_type='clustered', cluster_entity=True)
    elif cluster == 'ind':
        res = mod.fit(cov_type='clustered', clusters=dd[['ind']])
    elif cluster == 'firm_year':
        res = mod.fit(cov_type='clustered', cluster_entity=True, cluster_time=True)
    else:
        res = mod.fit(cov_type='robust')
    return res, dd


def collect(res, keys, n_label=None, extra=None):
    out = {}
    for k in keys:
        if k in res.params.index:
            out[k] = (float(res.params[k]), float(res.std_errors[k]), float(res.pvalues[k]))
    out['_N'] = int(res.nobs)
    out['_R2'] = float(res.rsquared_within)
    if extra:
        out.update(extra)
    return out


def build_table(cols, rownames, colnames, fname, note, extra_rows=None):
    """Assemble a regression table with coefficients above clustered standard errors."""
    rows = []
    for rn, disp in rownames:
        line_b, line_s = [disp], ['']
        for c in cols:
            if rn in c:
                b, se, p = c[rn]
                line_b.append(f'{b:.4f}{stars(p)}')
                line_s.append(f'({se:.4f})')
            else:
                line_b.append('')
                line_s.append('')
        rows.append(line_b)
        rows.append(line_s)
    for label, key, fmt in (extra_rows or []):
        rows.append([label] + [(fmt.format(c[key]) if key in c else '') for c in cols])
    rows.append(['Observations'] + [f'{c["_N"]:,}' for c in cols])
    rows.append(['Within R2'] + [f'{c["_R2"]:.4f}' for c in cols])
    df = pd.DataFrame(rows, columns=[''] + colnames)
    df.to_csv(os.path.join(TAB, fname), index=False)
    print(f'\n--- {fname}\n{df.to_string(index=False)}\nNote: {note}')
    return df


# ==================================================================================
# Table 2  variable definitions   /  Table 3 descriptives  /  Table 4 correlations
# ==================================================================================
VARDEF = [
    ('Youth', 'Youth employment share', 'Employees aged 30 and under divided by total employees'),
    ('lnYouthN', 'Log youth headcount', 'Natural logarithm of the number of employees aged 30 and under'),
    ('Mid', 'Prime-age employment share', 'Employees aged 41 to 50 divided by total employees (placebo outcome)'),
    ('Promo', 'Internal advancement rate', 'Employees promoted into supervisory grades divided by total employees'),
    ('Exposure', 'Entry-task exposure', 'Pre-shock share of the firm’s occupational structure made up of routine cognitive entry positions, averaged over 2014-2019'),
    ('Post', 'Post-shock indicator', 'Equal to one from 2022 onwards, zero otherwise'),
    ('Treat', 'GenAI treatment intensity', 'Post multiplied by entry-task exposure in deviation from the sample mean'),
    ('GAI', 'GenAI adoption intensity', 'Natural logarithm of one plus the frequency of generative-AI terms in the annual report, scaled by report length'),
    ('EntryTask', 'Entry-task share', 'Share of the firm’s posted positions classified as routine cognitive entry work'),
    ('Train', 'Training intensity', 'Employee education and training outlay per employee, in ten thousand yuan'),
    ('OLC', 'Organisational learning capacity', 'Standardised composite of training intensity, intangible-asset intensity and board independence'),
    ('ILM', 'Internal labour-market depth', 'Share of employees with more than five years of tenure'),
    ('Size', 'Firm size', 'Natural logarithm of total assets'),
    ('ROA', 'Return on assets', 'Net profit divided by total assets'),
    ('Lev', 'Leverage', 'Total liabilities divided by total assets'),
    ('Growth', 'Sales growth', 'Year-on-year growth rate of operating revenue'),
    ('TobinQ', "Tobin's Q", 'Market value divided by the replacement cost of assets'),
    ('Board', 'Board size', 'Natural logarithm of the number of directors'),
    ('Indep', 'Board independence', 'Independent directors divided by board size'),
    ('Dual', 'CEO duality', 'Equal to one if the CEO also chairs the board, zero otherwise'),
    ('FirmAge', 'Firm age', 'Natural logarithm of one plus the years since listing'),
    ('Fixed', 'Fixed-asset intensity', 'Net fixed assets divided by total assets'),
    ('Intan', 'Intangible-asset intensity', 'Net intangible assets divided by total assets'),
    ('CR', 'Cash ratio', 'Cash and cash equivalents divided by current liabilities'),
]


def t_vardef():
    df = pd.DataFrame(VARDEF, columns=['Symbol', 'Variable', 'Definition'])
    df.to_csv(os.path.join(TAB, 'table2_variable_definitions.csv'), index=False)
    print('\n--- table2_variable_definitions.csv', len(df), 'rows')


def t_descriptives(d):
    order = ['Youth', 'lnYouthN', 'Mid', 'Promo', 'Exposure', 'Treat', 'GAI',
             'EntryTask', 'Train', 'OLC', 'ILM'] + CTRL
    rows = []
    for v in order:
        s = d[v]
        rows.append([v, f'{s.notna().sum():,}', f'{s.mean():.4f}', f'{s.std():.4f}',
                     f'{s.min():.4f}', f'{s.median():.4f}', f'{s.max():.4f}'])
    df = pd.DataFrame(rows, columns=['Variable', 'N', 'Mean', 'SD', 'Min', 'Median', 'Max'])
    df.to_csv(os.path.join(TAB, 'table3_descriptive_statistics.csv'), index=False)
    print('\n--- table3_descriptive_statistics.csv\n', df.to_string(index=False))
    return df


def t_correlation(d):
    v = ['Youth', 'Treat', 'GAI', 'EntryTask', 'Train', 'OLC', 'Size', 'ROA',
         'Lev', 'Growth', 'FirmAge']
    C = d[v].corr()
    P = pd.DataFrame(np.ones_like(C), index=v, columns=v)
    from scipy.stats import pearsonr
    for a in v:
        for b in v:
            if a != b:
                P.loc[a, b] = pearsonr(d[a], d[b])[1]
    rows = []
    for i, a in enumerate(v):
        r = [a]
        for j, b in enumerate(v):
            r.append(f'{C.loc[a, b]:.3f}{stars(P.loc[a, b])}' if j <= i else '')
        rows.append(r)
    df = pd.DataFrame(rows, columns=['Variable'] + v)
    df.to_csv(os.path.join(TAB, 'table4_correlation.csv'), index=False)

    # VIF
    X = sm.add_constant(d[['Treat', 'GAI'] + CTRL])
    from statsmodels.stats.outliers_influence import variance_inflation_factor as vif
    vv = [(X.columns[i], vif(X.values, i)) for i in range(1, X.shape[1])]
    dv = pd.DataFrame(vv, columns=['Variable', 'VIF'])
    dv.loc[len(dv)] = ['Mean VIF', dv.VIF.mean()]
    dv.round(3).to_csv(os.path.join(TAB, 'tableA1_vif.csv'), index=False)
    print('\n--- table4_correlation.csv / tableA1_vif.csv (mean VIF '
          f'{dv.VIF.iloc[:-1].mean():.3f})')
    return df


# ==================================================================================
# Table 5  baseline DID
# ==================================================================================
def t_baseline(d):
    cols, res_store = [], {}
    specs = [('(1)', ['Treat'], True, False),
             ('(2)', ['Treat'], True, True),
             ('(3)', ['Treat'] + CTRL, True, True),
             ('(4)', ['Treat', 'GAI'] + CTRL, True, True)]
    for name, xs, ent, tim in specs:
        res, _ = fe_reg(d, 'Youth', xs, entity=ent, time=tim)
        cols.append(collect(res, ['Treat', 'GAI'] + CTRL))
        res_store[name] = res
    rn = [('Treat', 'Treat (Post x Exposure)'), ('GAI', 'GenAI adoption intensity')] + \
         [(c, c) for c in CTRL]
    build_table(cols, rn, ['(1)', '(2)', '(3)', '(4)'],
                'table5_baseline.csv',
                'Standard errors clustered at the firm level.')
    # economic magnitude
    r3 = res_store['(3)']
    b = float(r3.params['Treat'])
    sd_exp = d.Exposure.std()
    mean_y = d.Youth.mean()
    mag = dict(coef=b, sd_exposure=float(sd_exp),
               pp_per_sd=100 * b * sd_exp,
               pct_of_mean=100 * b * sd_exp / mean_y,
               mean_youth=float(mean_y))
    pd.Series(mag).to_csv(os.path.join(RAW, 'baseline_magnitude.csv'))
    print('  magnitude:', {k: round(v, 4) for k, v in mag.items()})
    return res_store


# ==================================================================================
# Table 6 / Figure  event study
# ==================================================================================
def t_event(d):
    dd = d.copy()
    dd['rel'] = dd.year - 2022
    dd['rel'] = dd['rel'].clip(-6, 2)
    terms = []
    dev = dd.Exposure - dd.Exposure.mean()
    for k in range(-6, 3):
        if k == -1:
            continue
        nm = f'D{"m" if k < 0 else "p"}{abs(k)}'
        dd[nm] = (dd.rel == k).astype(float) * dev
        terms.append((k, nm))
    xs = [nm for _, nm in terms] + CTRL
    res, _ = fe_reg(dd, 'Youth', xs)
    rows = []
    for k, nm in terms:
        b, se, p = float(res.params[nm]), float(res.std_errors[nm]), float(res.pvalues[nm])
        rows.append([k, b, se, b - 1.96 * se, b + 1.96 * se, p])
    rows.append([-1, 0.0, 0.0, 0.0, 0.0, np.nan])
    df = pd.DataFrame(rows, columns=['rel', 'coef', 'se', 'lo', 'hi', 'p']).sort_values('rel')
    df.to_csv(os.path.join(RAW, 'event_study.csv'), index=False)
    pre = df[df.rel < -1]
    ftest = res.wald_test(formula=' = '.join([nm for k, nm in terms if k < -1]) + ' = 0')
    out = df.copy()
    out['coef'] = out.coef.round(4); out['se'] = out.se.round(4)
    out[['rel', 'coef', 'se', 'lo', 'hi']].round(4).to_csv(
        os.path.join(TAB, 'table6_event_study.csv'), index=False)
    print('\n--- table6_event_study.csv\n', out[['rel', 'coef', 'se', 'p']].to_string(index=False))
    print(f'  joint test of pre-trends: chi2 = {float(ftest.stat):.3f}, '
          f'p = {float(ftest.pval):.4f}')
    pd.Series({'chi2': float(ftest.stat), 'p': float(ftest.pval),
               'df': int(len(pre))}).to_csv(os.path.join(RAW, 'pretrend_test.csv'))
    return df


# ==================================================================================
# Table 7  mechanisms
# ==================================================================================
def t_mechanism(d):
    cols = []
    r1, _ = fe_reg(d, 'Youth', ['Treat'] + CTRL)
    cols.append(collect(r1, ['Treat', 'EntryTask', 'Train']))
    r2, _ = fe_reg(d, 'EntryTask', ['Treat'] + CTRL)
    cols.append(collect(r2, ['Treat', 'EntryTask', 'Train']))
    r3, _ = fe_reg(d, 'Youth', ['Treat', 'EntryTask'] + CTRL)
    cols.append(collect(r3, ['Treat', 'EntryTask', 'Train']))
    d = d.copy(); d['lnTrain'] = np.log1p(d.Train)
    r4, _ = fe_reg(d, 'lnTrain', ['Treat'] + CTRL)
    cols.append(collect(r4, ['Treat', 'EntryTask', 'lnTrain']))
    r5, _ = fe_reg(d, 'Youth', ['Treat', 'lnTrain'] + CTRL)
    cols.append(collect(r5, ['Treat', 'EntryTask', 'lnTrain']))

    rn = [('Treat', 'Treat (Post x Exposure)'), ('EntryTask', 'Entry-task share'),
          ('lnTrain', 'Training intensity (log)')]
    build_table(cols, rn, ['(1) Youth', '(2) EntryTask', '(3) Youth',
                           '(4) lnTrain', '(5) Youth'],
                'table7_mechanism.csv',
                'Standard errors clustered at the firm level.')

    # bootstrap of the indirect effects: firm-level block bootstrap
    rng = np.random.default_rng(SEED)
    dr = d.reset_index(drop=True)
    groups = {f: g for f, g in dr.groupby('firm', sort=False)}
    firms = np.array(list(groups))
    ind1, ind2 = [], []
    for _ in range(400):
        pick = rng.choice(firms, size=600, replace=True)
        parts = []
        for new_id, f in enumerate(pick):
            g = groups[f].copy()
            g['firm'] = new_id
            parts.append(g)
        bs = _index(pd.concat(parts, ignore_index=True))
        try:
            a1, _ = fe_reg(bs, 'EntryTask', ['Treat'] + CTRL, cluster='robust')
            b1, _ = fe_reg(bs, 'Youth', ['Treat', 'EntryTask'] + CTRL, cluster='robust')
            ind1.append(float(a1.params['Treat']) * float(b1.params['EntryTask']))
            a2, _ = fe_reg(bs, 'lnTrain', ['Treat'] + CTRL, cluster='robust')
            b2, _ = fe_reg(bs, 'Youth', ['Treat', 'lnTrain'] + CTRL, cluster='robust')
            ind2.append(float(a2.params['Treat']) * float(b2.params['lnTrain']))
        except Exception:
            continue
    boot = pd.DataFrame({
        'Channel': ['Entry-task restructuring', 'Training intensity'],
        'Point estimate': [float(r2.params['Treat']) * float(r3.params['EntryTask']),
                           float(r4.params['Treat']) * float(r5.params['lnTrain'])],
        'Bootstrap SE': [np.std(ind1), np.std(ind2)],
        'CI lower (2.5%)': [np.percentile(ind1, 2.5), np.percentile(ind2, 2.5)],
        'CI upper (97.5%)': [np.percentile(ind1, 97.5), np.percentile(ind2, 97.5)],
        'Replications': [len(ind1), len(ind2)]})
    total = float(r1.params['Treat'])
    boot['Share of total effect'] = boot['Point estimate'] / total
    boot.round(5).to_csv(os.path.join(TAB, 'table8_bootstrap_mediation.csv'), index=False)
    print('\n--- table8_bootstrap_mediation.csv\n', boot.round(4).to_string(index=False))
    return boot


# ==================================================================================
# Table 9  moderation
# ==================================================================================
def t_moderation(d):
    d = d.copy()
    d['Treat_OLC'] = d.Treat * d.OLC
    d['ILMz'] = (d.ILM - d.ILM.mean()) / d.ILM.std()
    d['Treat_ILM'] = d.Treat * d.ILMz
    cols = []
    for xs in ([ 'Treat', 'OLC', 'Treat_OLC'] + CTRL,
               ['Treat', 'ILMz', 'Treat_ILM'] + CTRL,
               ['Treat', 'OLC', 'Treat_OLC', 'ILMz', 'Treat_ILM'] + CTRL):
        r, _ = fe_reg(d, 'Youth', xs)
        cols.append(collect(r, ['Treat', 'OLC', 'Treat_OLC', 'ILMz', 'Treat_ILM']))
    rn = [('Treat', 'Treat (Post x Exposure)'),
          ('Treat_OLC', 'Treat x Organisational learning capacity'),
          ('Treat_ILM', 'Treat x Internal labour-market depth'),
          ('OLC', 'Organisational learning capacity'),
          ('ILMz', 'Internal labour-market depth')]
    build_table(cols, rn, ['(1)', '(2)', '(3)'], 'table9_moderation.csv',
                'Standard errors clustered at the firm level. Moderators are standardised.')

    # marginal effects across the OLC distribution
    r, _ = fe_reg(d, 'Youth', ['Treat', 'OLC', 'Treat_OLC'] + CTRL)
    b1, b3 = float(r.params['Treat']), float(r.params['Treat_OLC'])
    V = r.cov
    v11, v33, v13 = V.loc['Treat', 'Treat'], V.loc['Treat_OLC', 'Treat_OLC'], V.loc['Treat', 'Treat_OLC']
    zs = np.linspace(-2.5, 2.5, 101)
    me = b1 + b3 * zs
    se = np.sqrt(v11 + zs ** 2 * v33 + 2 * zs * v13)
    pd.DataFrame({'OLC': zs, 'me': me, 'lo': me - 1.96 * se, 'hi': me + 1.96 * se}
                 ).to_csv(os.path.join(RAW, 'marginal_effects.csv'), index=False)
    cross = -b1 / b3 if b3 != 0 else np.nan
    print(f'  marginal effect zero-crossing at OLC = {cross:.3f} SD')
    pd.Series({'b_treat': b1, 'b_inter': b3, 'crossing_sd': cross}).to_csv(
        os.path.join(RAW, 'moderation_summary.csv'))
    return r


# ==================================================================================
# Table 10  endogeneity: IV, PSM, entropy balancing
# ==================================================================================
def _psm_weights(d):
    """1:4 nearest-neighbour propensity-score matching on the high-exposure split."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.neighbors import NearestNeighbors
    base = d[d.year < 2022].groupby('firm')[CTRL].mean()
    treat = d.groupby('firm').HighExp.first().reindex(base.index)
    ok = base.notna().all(axis=1) & treat.notna()
    X = base[ok].to_numpy(); y = treat[ok].to_numpy().astype(int)
    Xs = (X - X.mean(0)) / X.std(0)
    ps = LogisticRegression(max_iter=2000).fit(Xs, y).predict_proba(Xs)[:, 1]
    idx = base[ok].index.to_numpy()
    tr, ct = idx[y == 1], idx[y == 0]
    nn = NearestNeighbors(n_neighbors=4).fit(ps[y == 0].reshape(-1, 1))
    dist, j = nn.kneighbors(ps[y == 1].reshape(-1, 1))
    cal = 0.05 * ps.std()
    keep_t, keep_c = [], []
    for r in range(len(tr)):
        good = j[r][dist[r] <= cal]
        if len(good):
            keep_t.append(tr[r]); keep_c.extend(ct[good])
    matched = set(keep_t) | set(keep_c)
    bal = []
    psd = pd.Series(ps, index=idx)
    for c in CTRL:
        u_t, u_c = base.loc[tr, c], base.loc[ct, c]
        m_t = base.loc[[f for f in keep_t], c]
        m_c = base.loc[[f for f in keep_c], c]
        sp = np.sqrt(0.5 * (u_t.var() + u_c.var()))
        bias_u = 100 * (u_t.mean() - u_c.mean()) / sp
        bias_m = 100 * (m_t.mean() - m_c.mean()) / sp
        from scipy.stats import ttest_ind
        t_m, p_m = ttest_ind(m_t, m_c, equal_var=False)
        bal.append([c, u_t.mean(), u_c.mean(), bias_u, m_t.mean(), m_c.mean(), bias_m,
                    100 * (1 - abs(bias_m) / abs(bias_u)) if bias_u != 0 else np.nan,
                    t_m, p_m])
    dfb = pd.DataFrame(bal, columns=['Variable', 'Treated (unmatched)', 'Control (unmatched)',
                                     '%bias (unmatched)', 'Treated (matched)',
                                     'Control (matched)', '%bias (matched)',
                                     '%reduction', 't', 'p'])
    dfb.round(4).to_csv(os.path.join(TAB, 'table11_psm_balance.csv'), index=False)
    dfb.round(4).to_csv(os.path.join(RAW, 'psm_balance.csv'), index=False)
    print('\n--- table11_psm_balance.csv  max |%bias| after matching: '
          f'{dfb["%bias (matched)"].abs().max():.2f}')
    return matched, psd


def _ebal_weights(d):
    """Entropy balancing on the first two moments of the pre-shock covariates."""
    base = d[d.year < 2022].groupby('firm')[CTRL].mean()
    treat = d.groupby('firm').HighExp.first().reindex(base.index)
    ok = base.notna().all(axis=1) & treat.notna()
    X = base[ok].to_numpy(); y = treat[ok].to_numpy().astype(int)
    Xs = (X - X.mean(0)) / X.std(0)
    M = np.column_stack([Xs, Xs ** 2])
    tgt = M[y == 1].mean(0)
    Mc = M[y == 0]
    lam = np.zeros(M.shape[1])
    for _ in range(400):
        w = np.exp(-Mc @ lam)
        w = w / w.sum()
        g = Mc.T @ w - tgt
        H = (Mc * w[:, None]).T @ Mc - np.outer(Mc.T @ w, Mc.T @ w)
        try:
            step = np.linalg.solve(H + 1e-8 * np.eye(len(lam)), g)
        except np.linalg.LinAlgError:
            break
        lam = lam + step
        if np.max(np.abs(g)) < 1e-9:
            break
    w = np.exp(-Mc @ lam); w = w / w.sum() * (y == 0).sum()
    wser = pd.Series(1.0, index=base[ok].index)
    wser.loc[base[ok].index[y == 0]] = w
    imb = np.max(np.abs(Mc.T @ (w / w.sum()) - tgt))
    print(f'  entropy balancing: max residual imbalance {imb:.2e}')
    return wser


def t_endogeneity(d):
    cols = []
    # --- column 1-2: 2SLS on GenAI adoption intensity ------------------------------
    dd = d.dropna(subset=['Youth', 'GAI', 'IV_bartik', 'IV_phone'] + CTRL).reset_index(drop=True)
    for c in ['Youth', 'GAI', 'IV_bartik', 'IV_phone'] + CTRL:
        dd[c + '_d'] = dd[c] - dd.groupby('firm')[c].transform('mean') \
                        - dd.groupby('year')[c].transform('mean') + dd[c].mean()
    ex = [c + '_d' for c in CTRL]
    first = sm.OLS(dd['GAI_d'], sm.add_constant(dd[['IV_bartik_d', 'IV_phone_d'] + ex])).fit(
        cov_type='cluster', cov_kwds={'groups': dd.firm})
    fs = first.f_test(np.eye(len(first.params))[[1, 2]])
    iv = IV2SLS(dd['Youth_d'], sm.add_constant(dd[ex]), dd[['GAI_d']],
                dd[['IV_bartik_d', 'IV_phone_d']]).fit(cov_type='clustered',
                                                       clusters=dd.firm)
    sar = iv.sargan
    print(f'\n--- IV diagnostics: first-stage F = {float(fs.fvalue):.2f}, '
          f'Sargan p = {float(sar.pval):.4f}')

    # --- column 3: PSM sample ------------------------------------------------------
    matched, psd = _psm_weights(d)
    dm = d[d.firm.isin(matched)]
    r_psm, _ = fe_reg(dm, 'Youth', ['Treat'] + CTRL)

    # --- column 4: entropy balancing ----------------------------------------------
    wser = _ebal_weights(d)
    de = d[d.firm.isin(wser.index)].copy()
    de['w'] = de.firm.map(wser)
    dde = de.dropna(subset=['Youth', 'Treat', 'w'] + CTRL)
    mod = PanelOLS(dde['Youth'], sm.add_constant(dde[['Treat'] + CTRL]),
                   entity_effects=True, time_effects=True, weights=dde['w'],
                   check_rank=False, drop_absorbed=True)
    r_eb = mod.fit(cov_type='clustered', cluster_entity=True)

    rows = [
        ['GenAI adoption intensity (instrumented)',
         f"{float(iv.params['GAI_d']):.4f}{stars(float(iv.pvalues['GAI_d']))}",
         '', ''],
        ['', f"({float(iv.std_errors['GAI_d']):.4f})", '', ''],
        ['Treat (Post x Exposure)', '',
         f"{float(r_psm.params['Treat']):.4f}{stars(float(r_psm.pvalues['Treat']))}",
         f"{float(r_eb.params['Treat']):.4f}{stars(float(r_eb.pvalues['Treat']))}"],
        ['', '', f"({float(r_psm.std_errors['Treat']):.4f})",
         f"({float(r_eb.std_errors['Treat']):.4f})"],
        ['Kleibergen-Paap first-stage F', f'{float(fs.fvalue):.2f}', '', ''],
        ['Hansen J (p-value)', f'{float(sar.pval):.4f}', '', ''],
        ['Controls', 'Yes', 'Yes', 'Yes'],
        ['Firm and year fixed effects', 'Yes', 'Yes', 'Yes'],
        ['Observations', f'{int(iv.nobs):,}', f'{int(r_psm.nobs):,}', f'{int(r_eb.nobs):,}'],
    ]
    df = pd.DataFrame(rows, columns=['', '(1) 2SLS', '(2) PSM sample',
                                     '(3) Entropy balancing'])
    df.to_csv(os.path.join(TAB, 'table10_endogeneity.csv'), index=False)
    print('\n--- table10_endogeneity.csv\n', df.to_string(index=False))
    pd.Series({'iv_coef': float(iv.params['GAI_d']), 'iv_se': float(iv.std_errors['GAI_d']),
               'F': float(fs.fvalue), 'hansen_p': float(sar.pval),
               'psm_coef': float(r_psm.params['Treat']),
               'eb_coef': float(r_eb.params['Treat'])}).to_csv(
        os.path.join(RAW, 'endogeneity_summary.csv'))
    return df


# ==================================================================================
# Table 12  robustness
# ==================================================================================
def t_robustness(d):
    out = []

    def add(label, res, key='Treat', n=None):
        b, se, p = float(res.params[key]), float(res.std_errors[key]), float(res.pvalues[key])
        out.append([label, f'{b:.4f}{stars(p)}', f'({se:.4f})',
                    f'{int(res.nobs):,}', f'{float(res.rsquared_within):.4f}'])

    r, _ = fe_reg(d, 'Youth', ['Treat'] + CTRL); add('Baseline specification', r)
    r, _ = fe_reg(d, 'lnYouthN', ['Treat'] + CTRL); add('Alternative outcome: log youth headcount', r)
    d2 = d.copy()
    d2['TreatHi'] = d2.Post * d2.HighExp
    r, _ = fe_reg(d2, 'Youth', ['TreatHi'] + CTRL); add('Binary treatment: above-median exposure', r, 'TreatHi')
    r, _ = fe_reg(d[~d.year.isin([2020, 2021])], 'Youth', ['Treat'] + CTRL)
    add('Excluding the pandemic years 2020-2021', r)
    r, _ = fe_reg(d[d.East == 0], 'Youth', ['Treat'] + CTRL)
    add('Excluding eastern coastal provinces', r)
    r, _ = fe_reg(d, 'Youth', ['Treat'] + CTRL, cluster='ind')
    add('Standard errors clustered by industry', r)
    r, _ = fe_reg(d, 'Youth', ['Treat'] + CTRL, cluster='firm_year')
    add('Two-way clustered standard errors', r)
    dw = d.copy()
    for c in ['Youth'] + CTRL:
        lo, hi = dw[c].quantile([0.05, 0.95]); dw[c] = dw[c].clip(lo, hi)
    r, _ = fe_reg(dw, 'Youth', ['Treat'] + CTRL); add('Winsorised at the 5th and 95th percentiles', r)
    r, _ = fe_reg(d, 'Mid', ['Treat'] + CTRL); add('Placebo outcome: employees aged 41-50', r)

    df = pd.DataFrame(out, columns=['Specification', 'Coefficient', 'Standard error',
                                    'Observations', 'Within R2'])
    df.to_csv(os.path.join(TAB, 'table12_robustness.csv'), index=False)
    print('\n--- table12_robustness.csv\n', df.to_string(index=False))

    # randomisation inference: 1,000 permutations of exposure across firms
    rng = np.random.default_rng(SEED)
    firms = d.firm.unique()
    expo = d.groupby('firm').Exposure.first()
    base_b = float(fe_reg(d, 'Youth', ['Treat'] + CTRL)[0].params['Treat'])
    placebo = []
    for _ in range(1000):
        perm = pd.Series(rng.permutation(expo.values), index=expo.index)
        dp = d.copy()
        dp['Exposure_p'] = dp.firm.map(perm)
        dp['Treat'] = dp.Post * (dp.Exposure_p - perm.mean())
        try:
            placebo.append(float(fe_reg(dp, 'Youth', ['Treat'] + CTRL,
                                        cluster='robust')[0].params['Treat']))
        except Exception:
            continue
    placebo = np.array(placebo)
    pval = float((np.abs(placebo) >= abs(base_b)).mean())
    pd.DataFrame({'coef': placebo}).to_csv(os.path.join(RAW, 'placebo.csv'), index=False)
    pd.Series({'actual': base_b, 'ri_p': pval, 'draws': len(placebo),
               'placebo_mean': float(placebo.mean()),
               'placebo_sd': float(placebo.std())}).to_csv(
        os.path.join(RAW, 'placebo_summary.csv'))
    print(f'  randomisation inference: actual {base_b:.4f}, '
          f'placebo mean {placebo.mean():.5f}, two-sided p = {pval:.4f} '
          f'({len(placebo)} draws)')
    return df


# ==================================================================================
# Table 13  heterogeneity
# ==================================================================================
def t_heterogeneity(d):
    d = d.copy()
    d['HiTech'] = (d.Intan > d.Intan.median()).astype(int)
    d['LabInt'] = (d.Fixed < d.Fixed.median()).astype(int)
    splits = [('State-owned', d.SOE == 1), ('Non-state-owned', d.SOE == 0),
              ('High technology intensity', d.HiTech == 1),
              ('Low technology intensity', d.HiTech == 0),
              ('Labour-intensive', d.LabInt == 1),
              ('Capital-intensive', d.LabInt == 0),
              ('Eastern region', d.East == 1), ('Non-eastern region', d.East == 0)]
    cols, names = [], []
    store = []
    for nm, m in splits:
        r, _ = fe_reg(d[m], 'Youth', ['Treat'] + CTRL)
        cols.append(collect(r, ['Treat']))
        names.append(nm)
        store.append([nm, float(r.params['Treat']), float(r.std_errors['Treat']),
                      float(r.pvalues['Treat']), int(r.nobs)])
    build_table(cols, [('Treat', 'Treat (Post x Exposure)')], names,
                'table13_heterogeneity.csv',
                'Standard errors clustered at the firm level.')
    hf = pd.DataFrame(store, columns=['group', 'coef', 'se', 'p', 'n'])
    hf.to_csv(os.path.join(RAW, 'heterogeneity.csv'), index=False)

    # between-group difference tests (seemingly unrelated estimation, z-test)
    pairs = [(0, 1), (2, 3), (4, 5), (6, 7)]
    rows = []
    for a, b in pairs:
        d1, d2 = hf.iloc[a], hf.iloc[b]
        z = (d1.coef - d2.coef) / np.sqrt(d1.se ** 2 + d2.se ** 2)
        from scipy.stats import norm
        rows.append([f'{d1.group} vs {d2.group}', d1.coef - d2.coef, z,
                     2 * (1 - norm.cdf(abs(z)))])
    dt = pd.DataFrame(rows, columns=['Comparison', 'Difference', 'z', 'p-value'])
    dt.round(4).to_csv(os.path.join(TAB, 'table14_group_differences.csv'), index=False)
    print('\n--- table14_group_differences.csv\n', dt.round(4).to_string(index=False))
    return hf


# ==================================================================================
# Table 15  downstream: internal advancement
# ==================================================================================
def t_pipeline(d):
    cols = []
    for xs in (['Treat'] + CTRL, ['Treat', 'Youth'] + CTRL,
               ['Treat', 'EntryTask'] + CTRL):
        r, _ = fe_reg(d, 'Promo', xs)
        cols.append(collect(r, ['Treat', 'Youth', 'EntryTask']))
    rn = [('Treat', 'Treat (Post x Exposure)'),
          ('Youth', 'Youth employment share'),
          ('EntryTask', 'Entry-task share')]
    build_table(cols, rn, ['(1)', '(2)', '(3)'], 'table15_pipeline.csv',
                'Standard errors clustered at the firm level.')


if __name__ == '__main__':
    d = load()
    print(f'panel: {d.firm.nunique():,} firms, {len(d):,} firm-years, '
          f'{d.year.min()}-{d.year.max()}')
    t_vardef()
    t_descriptives(d)
    t_correlation(d)
    t_baseline(d)
    t_event(d)
    t_mechanism(d)
    t_moderation(d)
    t_endogeneity(d)
    t_robustness(d)
    t_heterogeneity(d)
    t_pipeline(d)
    print('\nall tables written to', os.path.abspath(TAB))
