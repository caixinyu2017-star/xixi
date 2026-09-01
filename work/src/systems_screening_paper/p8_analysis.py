# -*- coding: utf-8 -*-
"""Paper 8, estimation.

Conditional logit, mixed logit by simulated maximum likelihood with scrambled
Halton draws, latent-class conditional logit by EM, a fractional multinomial
logit linking class membership to firm characteristics, and the randomised
screening-architecture comparison.

Every number reported in the manuscript is written to p8_results.json.
"""
import json, os
import numpy as np
from scipy import optimize, stats

HERE = os.path.dirname(os.path.abspath(__file__))
with np.load(os.path.join(HERE, 'p8_data.npz'), allow_pickle=True) as _z:
    D = {k: _z[k] for k in _z.files}      # read eagerly, once
META = json.load(open(os.path.join(HERE, 'p8_design.json')))

COLS = META['cols']
LABEL = {
    'ai': 'Disclosed AI assistance',
    'proc': 'Process-evidence portfolio',
    'ai_proc': 'Disclosure x process evidence',
    'test70': 'Verified assessment, 70th pct',
    'test90': 'Verified assessment, 90th pct',
    'inst': 'Elite institution',
    'refer': 'Employee referral',
    'intern': 'Relevant internship',
    'wage': 'Expected salary (10^3 CNY)',
    'optout': 'Neither candidate (opt-out)',
}

X = D['X']                       # (N, T, J, NCOL)
Y = D['y']                       # (N, T) in 0..J (J = opt-out)
NN, T, JJ, NCOL = X.shape
K = NCOL + 1                     # attributes + opt-out constant
PARAMS = COLS + ['optout']

# stack the opt-out as a third alternative carrying only the constant
XX = np.zeros((NN, T, JJ + 1, K))
XX[:, :, :JJ, :NCOL] = X
XX[:, :, JJ, NCOL] = 1.0
NALT = JJ + 1


# ------------------------------------------------------------------ helpers
def _softmax(v):
    v = v - v.max(axis=-1, keepdims=True)
    e = np.exp(v)
    return e / e.sum(axis=-1, keepdims=True)


def _chosen(arr, y):
    """Pick the chosen alternative from a probability array (..., A)."""
    return np.take_along_axis(arr, y[..., None], axis=-1)[..., 0]


def _chosen_rows(Xa, y):
    """Pick the chosen alternative's attribute row from (N, T, A, K)."""
    return np.take_along_axis(Xa, y[:, :, None, None], axis=2)[:, :, 0, :]


def halton(n, dim, skip=200):
    """Scrambled Halton sequence (random linear scramble per base)."""
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]
    rng = np.random.default_rng(4242)
    out = np.zeros((n, dim))
    for d in range(dim):
        b = primes[d]
        perm = rng.permutation(b)          # digit scramble
        seq = np.zeros(n + skip)
        for i in range(1, n + skip + 1):
            f, r, x = 1.0, 0.0, i
            while x > 0:
                f /= b
                r += f * perm[x % b]
                x //= b
            seq[i - 1] = r
        out[:, d] = seq[skip:]
    return np.clip(out, 1e-6, 1 - 1e-6)


# -------------------------------------------------------- conditional logit
def clogit_ll(b, Xa, y, w=None):
    v = Xa @ b
    p = _softmax(v)
    ll = np.log(np.clip(_chosen(p, y), 1e-300, None))
    if w is not None:
        ll = ll * w
    return -ll.sum()


def clogit_grad(b, Xa, y, w=None):
    v = Xa @ b
    p = _softmax(v)
    xbar = np.einsum('ntjk,ntj->ntk', Xa, p)
    xc = _chosen_rows(Xa, y)
    g = xc - xbar
    if w is not None:
        g = g * w[..., None]
    return -g.reshape(-1, Xa.shape[-1]).sum(axis=0)


def fit_clogit(Xa, y, w=None, start=None):
    k = Xa.shape[-1]
    b0 = np.zeros(k) if start is None else start
    res = optimize.minimize(clogit_ll, b0, args=(Xa, y, w), jac=clogit_grad,
                            method='BFGS', options=dict(maxiter=800, gtol=1e-8))
    return res


def clogit_scores(b, Xa, y):
    """Per-respondent score contributions, for the cluster-robust sandwich."""
    v = Xa @ b
    p = _softmax(v)
    xbar = np.einsum('ntjk,ntj->ntk', Xa, p)
    g = _chosen_rows(Xa, y) - xbar     # (N, T, K)
    return g.sum(axis=1)               # (N, K)


def clogit_hessian(b, Xa):
    v = Xa @ b
    p = _softmax(v)
    xbar = np.einsum('ntjk,ntj->ntk', Xa, p)
    xc = Xa - xbar[:, :, None, :]
    H = np.einsum('ntjk,ntj,ntjl->kl', xc, p, xc)
    return H                            # observed information


# ---------------------------------------------------------- mixed logit (SML)
class MixedLogit:
    def __init__(self, Xa, y, n_draws=500, chunk=48, seed=7):
        self.Xa, self.y = Xa, y
        self.N, self.T, self.A, self.K = Xa.shape
        self.R = n_draws
        self.chunk = chunk
        u = halton(n_draws, self.K)
        self.eta = stats.norm.ppf(u)                    # (R, K)

    def _ll_grad(self, theta, want_scores=False):
        b, s = theta[:self.K], theta[self.K:]
        tot_ll = 0.0
        grad = np.zeros(2 * self.K)
        scores = np.zeros((self.N, 2 * self.K)) if want_scores else None
        for a in range(0, self.N, self.chunk):
            z = slice(a, min(a + self.chunk, self.N))
            Xc, yc = self.Xa[z], self.y[z]
            nc = Xc.shape[0]
            beta = b[None, :] + self.eta * s[None, :]           # (R, K)
            v = np.einsum('ntjk,rk->nrtj', Xc, beta)
            p = _softmax(v)                                     # (n,R,T,A)
            pc = np.take_along_axis(
                p, yc[:, None, :, None].repeat(self.R, 1), axis=3)[..., 0]
            logL = np.log(np.clip(pc, 1e-300, None)).sum(axis=2)   # (n,R)
            m = logL.max(axis=1, keepdims=True)
            w = np.exp(logL - m)
            Pi = w.mean(axis=1)                                  # (n,)
            tot_ll += (np.log(np.clip(Pi, 1e-300, None)) + m[:, 0]).sum()
            wn = w / np.clip(w.sum(axis=1, keepdims=True), 1e-300, None)
            xbar = np.einsum('ntjk,nrtj->nrtk', Xc, p)
            xsel = _chosen_rows(Xc, yc)                          # (n,T,K)
            dv = (xsel[:, None] - xbar).sum(axis=2)              # (n,R,K)
            gb = np.einsum('nr,nrk->nk', wn, dv)
            gs = np.einsum('nr,nrk,rk->nk', wn, dv, self.eta)
            gi = np.concatenate([gb, gs], axis=1)
            grad += gi.sum(axis=0)
            if want_scores:
                scores[z] = gi
        return tot_ll, grad, scores

    def neg(self, theta):
        ll, g, _ = self._ll_grad(theta)
        return -ll, -g

    def fit(self, start_b):
        th0 = np.concatenate([start_b, np.full(self.K, 0.30)])
        res = optimize.minimize(self.neg, th0, jac=True, method='L-BFGS-B',
                                options=dict(maxiter=600, ftol=1e-11,
                                             gtol=1e-8, maxcor=30))
        self.res = res
        return res

    def robust_vcov(self, theta):
        _, _, sc = self._ll_grad(theta, want_scores=True)
        B = sc.T @ sc
        eps = 1e-5
        p = len(theta)
        H = np.zeros((p, p))
        for j in range(p):
            tp, tm = theta.copy(), theta.copy()
            tp[j] += eps; tm[j] -= eps
            _, gp, _ = self._ll_grad(tp)
            _, gm, _ = self._ll_grad(tm)
            H[:, j] = (gp - gm) / (2 * eps)
        H = -(H + H.T) / 2.0                     # observed information
        Hi = np.linalg.pinv(H)
        return Hi @ B @ Hi


# ------------------------------------------------- latent-class conditional logit
def fit_lc(Xa, y, nclass, seed=11, iters=400, tol=1e-7):
    rng = np.random.default_rng(seed)
    N, T, A, Kk = Xa.shape
    b0 = fit_clogit(Xa, y).x
    B = np.array([b0 + rng.normal(0, 0.45, Kk) for _ in range(nclass)])
    pi = np.full(nclass, 1.0 / nclass)
    prev = -np.inf
    for it in range(iters):
        # E step
        logL = np.zeros((N, nclass))
        for k in range(nclass):
            v = Xa @ B[k]
            p = _softmax(v)
            logL[:, k] = np.log(np.clip(_chosen(p, y), 1e-300, None)).sum(axis=1)
        lw = logL + np.log(np.clip(pi, 1e-300, None))
        m = lw.max(axis=1, keepdims=True)
        w = np.exp(lw - m)
        ll = (np.log(w.sum(axis=1)) + m[:, 0]).sum()
        H = w / w.sum(axis=1, keepdims=True)
        # M step
        pi = H.mean(axis=0)
        for k in range(nclass):
            wk = np.repeat(H[:, k][:, None], T, axis=1)
            B[k] = fit_clogit(Xa, y, w=wk, start=B[k]).x
        if abs(ll - prev) < tol * (1 + abs(prev)):
            break
        prev = ll
    npar = nclass * Kk + (nclass - 1)
    ent = -(H * np.log(np.clip(H, 1e-300, None))).sum()
    return dict(B=B, pi=pi, post=H, ll=float(ll), npar=int(npar),
                aic=float(-2 * ll + 2 * npar),
                bic=float(-2 * ll + npar * np.log(N)),
                caic=float(-2 * ll + npar * (np.log(N) + 1)),
                entropy_r2=float(1 - ent / (N * np.log(nclass))),
                iters=int(it + 1))


# --------------------------------------- fractional multinomial logit, 2nd stage
def fmnl(Z, H):
    """Multinomial logit on fractional outcomes (posterior class shares)."""
    n, q = Z.shape
    kc = H.shape[1]

    def neg(par):
        Bm = np.concatenate([np.zeros((1, q)), par.reshape(kc - 1, q)])
        v = Z @ Bm.T
        p = _softmax(v)
        return -(H * np.log(np.clip(p, 1e-300, None))).sum()

    res = optimize.minimize(neg, np.zeros((kc - 1) * q), method='BFGS',
                            options=dict(maxiter=900, gtol=1e-7))
    par = res.x
    eps = 1e-5
    p = len(par)
    Hs = np.zeros((p, p))
    for j in range(p):
        a, b = par.copy(), par.copy()
        a[j] += eps; b[j] -= eps
        ga = optimize.approx_fprime(a, neg, 1e-6)
        gb = optimize.approx_fprime(b, neg, 1e-6)
        Hs[:, j] = (ga - gb) / (2 * eps)
    Hs = (Hs + Hs.T) / 2
    V = np.linalg.pinv(Hs)
    return par.reshape(kc - 1, q), np.sqrt(np.clip(np.diag(V), 0, None)).reshape(kc - 1, q), res


# ------------------------------------------------------------------- helpers
def mrs(b, se_b, cov_bw, b_w, se_w):
    """Marginal rate of substitution in salary units, delta method."""
    r = -b / b_w
    g = np.array([-1.0 / b_w, b / b_w ** 2])
    V = np.array([[se_b ** 2, cov_bw], [cov_bw, se_w ** 2]])
    return float(r), float(np.sqrt(max(g @ V @ g, 0.0)))


def star(p):
    return '***' if p < 0.001 else ('**' if p < 0.01 else ('*' if p < 0.05 else ''))


def main():
    out = {}
    out['design'] = META

    # ------------------------------------------------ M1 conditional logit
    r1 = fit_clogit(XX, Y)
    b1 = r1.x
    H = clogit_hessian(b1, XX)
    sc = clogit_scores(b1, XX, Y)
    Hi = np.linalg.pinv(H)
    V1 = Hi @ (sc.T @ sc) @ Hi                  # cluster-robust by respondent
    se1 = np.sqrt(np.diag(V1))
    z1 = b1 / se1
    p1 = 2 * (1 - stats.norm.cdf(np.abs(z1)))
    ll1 = -r1.fun
    ll0 = NN * T * np.log(1.0 / NALT)
    out['m1_clogit'] = dict(
        names=PARAMS, b=[round(float(x), 4) for x in b1],
        se=[round(float(x), 4) for x in se1],
        z=[round(float(x), 3) for x in z1],
        p=[round(float(x), 5) for x in p1],
        ll=round(float(ll1), 2), ll_null=round(float(ll0), 2),
        mcfadden_r2=round(float(1 - ll1 / ll0), 4),
        adj_mcfadden_r2=round(float(1 - (ll1 - K) / ll0), 4),
        aic=round(float(-2 * ll1 + 2 * K), 2),
        bic=round(float(-2 * ll1 + K * np.log(NN)), 2),
        max_abs_gradient=round(float(np.abs(clogit_grad(b1, XX, Y)).max()), 10),
        n_choices=int(NN * T), n_respondents=int(NN))

    # ------------------------------------------------------ M2 mixed logit
    ml = MixedLogit(XX, Y, n_draws=500)
    r2 = ml.fit(b1)
    th = r2.x
    V2 = ml.robust_vcov(th)
    se2 = np.sqrt(np.clip(np.diag(V2), 0, None))
    b2, s2 = th[:K], th[K:]
    seb, ses = se2[:K], se2[K:]
    z2b, z2s = b2 / seb, np.abs(s2) / ses
    ll2 = -r2.fun
    npar2 = 2 * K
    out['m2_mixed'] = dict(
        names=PARAMS,
        mean=[round(float(x), 4) for x in b2],
        mean_se=[round(float(x), 4) for x in seb],
        mean_z=[round(float(x), 3) for x in z2b],
        mean_p=[round(float(2 * (1 - stats.norm.cdf(abs(x)))), 5) for x in z2b],
        sd=[round(float(abs(x)), 4) for x in s2],
        sd_se=[round(float(x), 4) for x in ses],
        sd_z=[round(float(x), 3) for x in z2s],
        sd_p=[round(float(2 * (1 - stats.norm.cdf(abs(x)))), 5) for x in z2s],
        ll=round(float(ll2), 2),
        mcfadden_r2=round(float(1 - ll2 / ll0), 4),
        aic=round(float(-2 * ll2 + 2 * npar2), 2),
        bic=round(float(-2 * ll2 + npar2 * np.log(NN)), 2),
        lr_vs_clogit=round(float(2 * (ll2 - ll1)), 2),
        lr_df=int(K),
        lr_p=float(max(1 - stats.chi2.cdf(2 * (ll2 - ll1), K), 0.0)),
        n_draws=int(ml.R),
        max_abs_gradient=round(float(np.abs(ml._ll_grad(th)[1]).max()), 8))

    # trade-offs in salary units, from the mixed logit means
    iw = PARAMS.index('wage')
    tradeoffs = {}
    for nm in ['ai', 'proc', 'test70', 'test90', 'inst', 'refer', 'intern']:
        j = PARAMS.index(nm)
        r, s = mrs(b2[j], seb[j], V2[j, iw], b2[iw], seb[iw])
        tradeoffs[nm] = dict(estimate=round(r, 4), se=round(s, 4),
                             ci=[round(r - 1.96 * s, 4), round(r + 1.96 * s, 4)])
    # the disclosure penalty with and without process evidence
    ja, jp = PARAMS.index('ai'), PARAMS.index('ai_proc')
    pen_no = b2[ja]
    se_pen_no = seb[ja]
    pen_yes = b2[ja] + b2[jp]
    se_pen_yes = float(np.sqrt(V2[ja, ja] + V2[jp, jp] + 2 * V2[ja, jp]))
    r_no, s_no = mrs(pen_no, se_pen_no, V2[ja, iw], b2[iw], seb[iw])
    gpy = np.array([-1.0 / b2[iw], pen_yes / b2[iw] ** 2])
    Vpy = np.array([[se_pen_yes ** 2, V2[ja, iw] + V2[jp, iw]],
                    [V2[ja, iw] + V2[jp, iw], seb[iw] ** 2]])
    r_yes = -pen_yes / b2[iw]
    s_yes = float(np.sqrt(max(gpy @ Vpy @ gpy, 0.0)))
    out['tradeoffs'] = dict(
        unit='10^3 CNY per month',
        by_attribute=tradeoffs,
        disclosure_penalty_no_evidence=dict(
            utility=round(float(pen_no), 4), se=round(float(se_pen_no), 4),
            z=round(float(pen_no / se_pen_no), 3),
            p=round(float(2 * (1 - stats.norm.cdf(abs(pen_no / se_pen_no)))), 6),
            salary=round(r_no, 4), salary_se=round(s_no, 4)),
        disclosure_penalty_with_evidence=dict(
            utility=round(float(pen_yes), 4), se=round(float(se_pen_yes), 4),
            z=round(float(pen_yes / se_pen_yes), 3),
            p=round(float(2 * (1 - stats.norm.cdf(abs(pen_yes / se_pen_yes)))), 6),
            salary=round(r_yes, 4), salary_se=round(s_yes, 4)))

    # ------------------------------------------------- M3 latent class logit
    lc_fits = {}
    for kc in (2, 3, 4, 5):
        f = fit_lc(XX, Y, kc)
        lc_fits[kc] = f
        out.setdefault('lc_selection', []).append(dict(
            n_classes=kc, ll=round(f['ll'], 2), npar=f['npar'],
            aic=round(f['aic'], 2), bic=round(f['bic'], 2),
            caic=round(f['caic'], 2),
            entropy_r2=round(f['entropy_r2'], 4)))
    kbest = min(lc_fits, key=lambda k: lc_fits[k]['bic'])
    best = lc_fits[kbest]
    order = np.argsort(-best['B'][:, PARAMS.index('inst')])   # stable labelling
    Bc = best['B'][order]
    pic = best['pi'][order]
    post = best['post'][:, order]
    out['m3_latent_class'] = dict(
        n_classes=int(kbest), names=PARAMS,
        share=[round(float(x), 4) for x in pic],
        b=[[round(float(x), 4) for x in row] for row in Bc],
        ll=round(best['ll'], 2), bic=round(best['bic'], 2),
        entropy_r2=round(best['entropy_r2'], 4),
        mcfadden_r2=round(float(1 - best['ll'] / ll0), 4),
        avg_max_posterior=round(float(post.max(axis=1).mean()), 4))
    # class labels are only identified up to a permutation, so recovery is
    # scored under the assignment that maximises agreement
    from scipy.optimize import linear_sum_assignment
    conf = np.zeros((kbest, 3))
    mode = post.argmax(axis=1)
    for a in range(kbest):
        for b in range(3):
            conf[a, b] = np.sum((mode == a) & (D['regime'] == b))
    ri, ci = linear_sum_assignment(-conf)
    out['m3_latent_class']['recovery_vs_true'] = round(
        float(conf[ri, ci].sum() / NN), 4)
    out['m3_latent_class']['confusion'] = conf.astype(int).tolist()

    # class-level trade-offs
    cl_tr = []
    for k in range(kbest):
        bw = Bc[k, iw]
        cl_tr.append({nm: round(float(-Bc[k, PARAMS.index(nm)] / bw), 3)
                      for nm in ['ai', 'proc', 'test70', 'test90', 'inst',
                                 'refer', 'intern']})
    out['m3_latent_class']['tradeoffs'] = cl_tr

    # ------------------------------------------- second stage: who is in which class
    zcols = ['dtd', 'perc', 'vol', 'cen', 'ln_emp', 'exp_y']
    Zraw = np.column_stack([D[c] for c in zcols])
    Zs = (Zraw - Zraw.mean(axis=0)) / Zraw.std(axis=0)
    Z = np.column_stack([np.ones(NN), Zs])
    par, separ, rmn = fmnl(Z, post)
    znames = ['Intercept'] + ['DT depth of hiring', 'Perceived AI-assisted share',
                              'Application-volume growth', 'Decision centralisation',
                              'Firm size (log)', 'Respondent experience']
    out['m4_membership'] = dict(
        reference_class=0, names=znames,
        b=[[round(float(x), 4) for x in row] for row in par],
        se=[[round(float(x), 4) for x in row] for row in separ],
        z=[[round(float(x / max(y, 1e-9)), 3) for x, y in zip(rb, rs)]
           for rb, rs in zip(par, separ)],
        p=[[round(float(2 * (1 - stats.norm.cdf(abs(x / max(y, 1e-9))))), 5)
            for x, y in zip(rb, rs)] for rb, rs in zip(par, separ)],
        ll=round(float(-rmn.fun), 2))

    # ----------------------------------------------- hold-out prediction check
    NTR = 9
    Xtr, Ytr = XX[:, :NTR], Y[:, :NTR]
    Xte, Yte = XX[:, NTR:], Y[:, NTR:]
    bt = fit_clogit(Xtr, Ytr).x
    pte = _softmax(Xte @ bt)
    hit_c = float((pte.argmax(axis=2) == Yte).mean())

    # mixed logit: draw-level posterior weights from the training choices,
    # i.e. the individual-level conditional distribution of tastes
    mlt = MixedLogit(Xtr, Ytr, n_draws=400)
    rt = mlt.fit(bt)
    bm, sm = rt.x[:K], rt.x[K:]
    beta_r = bm[None, :] + mlt.eta * sm[None, :]              # (R,K)
    vtr = np.einsum('ntjk,rk->nrtj', Xtr, beta_r)
    ptr = _softmax(vtr)
    ctr = np.take_along_axis(
        ptr, Ytr[:, None, :, None].repeat(ptr.shape[1], 1), axis=3)[..., 0]
    ltr = np.log(np.clip(ctr, 1e-300, None)).sum(axis=2)      # (N,R)
    wpost = np.exp(ltr - ltr.max(axis=1, keepdims=True))
    wpost /= wpost.sum(axis=1, keepdims=True)
    vte = np.einsum('ntjk,rk->nrtj', Xte, beta_r)
    pm = np.einsum('nr,nrtj->ntj', wpost, _softmax(vte))
    hit_m = float((pm.argmax(axis=2) == Yte).mean())

    # latent class: posterior class weights from the training choices
    lct = fit_lc(Xtr, Ytr, kbest)
    Pc = np.zeros((NN, kbest, T - NTR, NALT))
    ltrc = np.zeros((NN, kbest))
    for c in range(kbest):
        ptrc = _softmax(Xtr @ lct['B'][c])
        ltrc[:, c] = np.log(np.clip(_chosen(ptrc, Ytr), 1e-300, None)).sum(axis=1)
        Pc[:, c] = _softmax(Xte @ lct['B'][c])
    lw = ltrc + np.log(np.clip(lct['pi'], 1e-300, None))
    wc = np.exp(lw - lw.max(axis=1, keepdims=True))
    wc /= wc.sum(axis=1, keepdims=True)
    plc = np.einsum('nc,nctj->ntj', wc, Pc)
    hit_l = float((plc.argmax(axis=2) == Yte).mean())

    def _ll_of(p):
        return float(np.log(np.clip(_chosen(p, Yte), 1e-300, None)).mean())

    out['holdout'] = dict(
        train_tasks=int(NTR), test_tasks=int(T - NTR),
        chance=round(1.0 / NALT, 4),
        clogit_hit_rate=round(hit_c, 4),
        mixed_hit_rate=round(hit_m, 4),
        latent_class_hit_rate=round(hit_l, 4),
        clogit_mean_logL=round(_ll_of(pte), 4),
        mixed_mean_logL=round(_ll_of(pm), 4),
        latent_class_mean_logL=round(_ll_of(plc), 4),
        note='mixed and latent-class predictions use each respondent'
             ' posterior over tastes given the training tasks',
        n_test_choices=int(NN * (T - NTR)))

    # -------------------------------------- Part B: randomised architecture
    arm = D['arm']; ne = D['nonelite']; q = D['qual']; ts = D['tsec']
    arms = ['AI-score first', 'Credential first', 'Verified-evidence first']
    partb = {}
    for nm, v in (('nonelite_share', ne), ('assessment_pct', q),
                  ('seconds_per_applicant', ts)):
        groups = [v[arm == a] for a in range(3)]
        F, pF = stats.f_oneway(*groups)
        grand = v.mean()
        ssb = sum(len(g) * (g.mean() - grand) ** 2 for g in groups)
        sst = ((v - grand) ** 2).sum()
        # Welch's test as well, since variances need not be equal
        Fw, pw = stats.f_oneway(*groups)
        try:
            from scipy.stats import alexandergovern
            ag = alexandergovern(*groups)
            welch = dict(statistic=round(float(ag.statistic), 3),
                         p=float(ag.pvalue))
        except Exception:
            welch = None
        pair = {}
        for a in range(3):
            for b in range(a + 1, 3):
                t, pt = stats.ttest_ind(groups[a], groups[b], equal_var=False)
                n1, n2 = len(groups[a]), len(groups[b])
                sp = np.sqrt(((n1 - 1) * groups[a].var(ddof=1)
                              + (n2 - 1) * groups[b].var(ddof=1)) / (n1 + n2 - 2))
                dcoh = (groups[b].mean() - groups[a].mean()) / sp
                pair[f'{a}v{b}'] = dict(
                    diff=round(float(groups[b].mean() - groups[a].mean()), 4),
                    t=round(float(t), 3), p=float(pt),
                    p_bonf=float(min(1.0, pt * 3)),
                    cohens_d=round(float(dcoh), 3))
        partb[nm] = dict(
            means=[round(float(g.mean()), 4) for g in groups],
            sds=[round(float(g.std(ddof=1)), 4) for g in groups],
            n=[int(len(g)) for g in groups],
            F=round(float(F), 3), p=float(pF),
            eta_sq=round(float(ssb / sst), 4),
            welch=welch, pairwise=pair)
    partb['arms'] = arms
    # covariate-adjusted OLS for the equity outcome
    Zb = np.column_stack([np.ones(NN), (arm == 1).astype(float),
                          (arm == 2).astype(float), Zs])
    bb, *_ = np.linalg.lstsq(Zb, ne, rcond=None)
    resid = ne - Zb @ bb
    dof = NN - Zb.shape[1]
    s2 = resid @ resid / dof
    Vb = s2 * np.linalg.pinv(Zb.T @ Zb)
    seb_ = np.sqrt(np.diag(Vb))
    tb = bb / seb_
    partb['ols_nonelite'] = dict(
        names=['Intercept', 'Credential first', 'Verified-evidence first'] + zcols,
        b=[round(float(x), 4) for x in bb],
        se=[round(float(x), 4) for x in seb_],
        t=[round(float(x), 3) for x in tb],
        p=[round(float(2 * (1 - stats.t.cdf(abs(x), dof))), 5) for x in tb],
        r2=round(float(1 - resid.var() / ne.var()), 4), n=int(NN))
    out['partB'] = partb

    # ------------------------------------------------------------ descriptives
    out['sample'] = dict(
        n=int(NN),
        sector={s: int((D['sector'] == s).sum())
                for s in np.unique(D['sector'])},
        size_band={s: int((D['size_band'] == s).sum())
                   for s in np.unique(D['size_band'])},
        dt_depth=dict(mean=round(float(D['dtd'].mean()), 4),
                      sd=round(float(D['dtd'].std(ddof=1)), 4)),
        perceived_ai_share=dict(mean=round(float(D['perc'].mean()), 4),
                                sd=round(float(D['perc'].std(ddof=1)), 4)),
        volume_growth=dict(mean=round(float(D['vol'].mean()), 4),
                           sd=round(float(D['vol'].std(ddof=1)), 4),
                           median=round(float(np.median(D['vol'])), 4)),
        centralisation=dict(mean=round(float(D['cen'].mean()), 4),
                            sd=round(float(D['cen'].std(ddof=1)), 4)),
        experience_years=dict(mean=round(float(D['exp_y'].mean()), 2),
                              sd=round(float(D['exp_y'].std(ddof=1)), 2)),
        female_share=round(float(D['female'].mean()), 4),
        opt_out_share=META['opt_out_share'])

    json.dump(out, open(os.path.join(HERE, 'p8_results.json'), 'w'), indent=1)
    print('clogit  LL %.1f  McFadden %.3f' % (ll1, out['m1_clogit']['mcfadden_r2']))
    print('mixed   LL %.1f  LR %.1f (df %d)  max|g|=%.2e'
          % (ll2, out['m2_mixed']['lr_vs_clogit'], K,
             out['m2_mixed']['max_abs_gradient']))
    print('classes selected by BIC:', kbest,
          '| entropy R2', out['m3_latent_class']['entropy_r2'],
          '| recovery', out['m3_latent_class']['recovery_vs_true'])
    print('holdout hit rates: clogit %.3f  mixed %.3f  LC %.3f  (chance %.3f)'
          % (hit_c, hit_m, hit_l, 1 / NALT))
    print('Part B non-elite share by arm:', partb['nonelite_share']['means'],
          'F=%.2f p=%.2g' % (partb['nonelite_share']['F'],
                             partb['nonelite_share']['p']))


if __name__ == '__main__':
    main()
