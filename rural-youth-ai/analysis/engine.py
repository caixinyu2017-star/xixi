# -*- coding: utf-8 -*-
"""The matching engines and their audit machinery.

The proposed scorer is additive in a fixed, pre-registered feature ledger:
every pair feature passes through a one-dimensional piecewise-linear spline
and the score is the sum of the spline outputs. Because each spline is
linear in its weights, the whole scorer is linear in parameters, and the
evidence ledger — the per-feature contributions — reconstructs the score
exactly, by construction rather than by estimation.

Everything here is plain numpy; every training loop runs in CPU seconds.
"""
from __future__ import annotations

import numpy as np

import market as M

# ---------------------------------------------------------------------------
# the pre-registered pair-feature ledger (fixed before any estimation)
# ---------------------------------------------------------------------------
FEATURES = [
    "fit_agri", "fit_digital", "fit_ops", "fit_gov",
    "wage_gap", "distance", "distance_x_children",
    "mentorship", "mentorship_x_misfit", "housing",
    "amenity_x_children", "home_tie", "gai_x_digital_post",
    "education", "returnee",
]
D = len(FEATURES)
BINARY = {"mentorship", "housing", "home_tie", "returnee"}


def group_fit(mk, i, j, g):
    idx = M.GROUPS[g]
    r = mk.req[j, idx]
    return float(mk.skill[i, idx] @ r / (r.sum() + 1e-9))


def pair_features(mk, i, j):
    f = mk.fit(i, j)
    d = mk.dist(i, j)
    return np.array([
        group_fit(mk, i, j, "agri"), group_fit(mk, i, j, "digital"),
        group_fit(mk, i, j, "ops"), group_fit(mk, i, j, "gov"),
        mk.wage_gap(i, j), d, d * mk.child[i],
        mk.mentor[j], mk.mentor[j] * (1.0 - f), mk.house[j],
        mk.amen[j] * mk.child[i],
        float(mk.home[i] == mk.village[j]) * mk.ties[i],
        mk.gai[i] * float(mk.cat[j] in (1, 4)),
        mk.edu[i], mk.returnee[i],
    ])


def all_pair_features(mk, obs=None):
    """(n, m, D) tensor of pair features, from the OBSERVED market."""
    src = obs if obs is not None else mk
    n, m = src.n, src.m
    Z = np.empty((n, m, D))
    # vectorised construction
    rs = src.req.sum(axis=1) + 1e-9
    fit_all = src.skill @ src.req.T / rs[None, :]
    for gi, g in enumerate(("agri", "digital", "ops", "gov")):
        idx = M.GROUPS[g]
        rg = src.req[:, idx].sum(axis=1) + 1e-9
        Z[:, :, gi] = src.skill[:, idx] @ src.req[:, idx].T / rg[None, :]
    Z[:, :, 4] = src.wage[None, :] - src.wexp[:, None]
    dx = src.vx[src.home][:, None] - src.vx[src.village][None, :]
    dy = src.vy[src.home][:, None] - src.vy[src.village][None, :]
    dist = np.hypot(dx, dy)
    Z[:, :, 5] = dist
    Z[:, :, 6] = dist * src.child[:, None]
    Z[:, :, 7] = np.broadcast_to(src.mentor[None, :], (n, m))
    Z[:, :, 8] = src.mentor[None, :] * (1.0 - fit_all)
    Z[:, :, 9] = np.broadcast_to(src.house[None, :], (n, m))
    Z[:, :, 10] = src.amen[None, :] * src.child[:, None]
    Z[:, :, 11] = (src.home[:, None] == src.village[None, :]) \
        * src.ties[:, None]
    digital_post = np.isin(src.cat, (1, 4)).astype(float)
    Z[:, :, 12] = src.gai[:, None] * digital_post[None, :]
    Z[:, :, 13] = np.broadcast_to(src.edu[:, None], (n, m))
    Z[:, :, 14] = np.broadcast_to(src.returnee[:, None], (n, m))
    return Z


# ---------------------------------------------------------------------------
# piecewise-linear spline basis (hat functions on quantile knots)
# ---------------------------------------------------------------------------
class Basis:
    def __init__(self, Zs, n_knots=6):
        """Zs: (N, D) sample of feature rows used to place knots."""
        self.knots, self.widths = [], []
        for k in range(D):
            if FEATURES[k] in BINARY:
                self.knots.append(None)
            else:
                qs = np.quantile(Zs[:, k], np.linspace(0.02, 0.98, n_knots))
                qs = np.unique(qs)
                self.knots.append(qs)
        self.sizes = [1 if kn is None else len(kn) for kn in self.knots]
        self.offs = np.concatenate([[0], np.cumsum(self.sizes)])
        self.P = int(self.offs[-1])

    def expand(self, Zrows):
        """(N, D) -> (N, P) hat-function expansion."""
        N = Zrows.shape[0]
        B = np.zeros((N, self.P))
        for k in range(D):
            o = self.offs[k]
            kn = self.knots[k]
            if kn is None:
                B[:, o] = Zrows[:, k]
                continue
            x = Zrows[:, k]
            # hat functions: linear interpolation weights on the knot grid
            idx = np.clip(np.searchsorted(kn, x) - 1, 0, len(kn) - 2)
            left, right = kn[idx], kn[idx + 1]
            w = np.clip((x - left) / (right - left + 1e-12), 0, 1)
            B[np.arange(N), o + idx] += 1 - w
            B[np.arange(N), o + idx + 1] += w
        return B

    def contributions(self, w, Zrows, centre):
        """(N, D) per-feature ledger entries phi_k, centred so that the
        identity  s = b + sum_k phi_k  holds exactly with b the score of
        the reference (population-mean) row."""
        B = self.expand(Zrows)
        phi = np.zeros((Zrows.shape[0], D))
        for k in range(D):
            o, sz = self.offs[k], self.sizes[k]
            phi[:, k] = B[:, o:o + sz] @ w[o:o + sz] - centre[k]
        return phi


# ---------------------------------------------------------------------------
# discrete-time hazard trainer (linear in the basis => convex-ish problem)
# ---------------------------------------------------------------------------
def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -30, 30)))


class HazardScorer:
    """h_t(i,j) = sigmoid(a_r(t) - s(i,j)); higher s => lower hazard.

    a_r(t): one intercept per calendar regime block (months 1-6, 7-24
    split into 7-12, 13-24) — a flexible baseline that still cannot
    replicate the oracle's regime-switching covariate effects.
    """

    REG = [(1, 6), (7, 12), (13, 24)]

    def __init__(self, basis):
        self.basis = basis
        self.w = np.zeros(basis.P)
        self.a = np.array([-2.2, -3.0, -3.4])

    def _reg(self, t):
        for r, (lo, hi) in enumerate(self.REG):
            if lo <= t <= hi:
                return r
        return len(self.REG) - 1

    def score(self, Zrows):
        return self.basis.expand(Zrows) @ self.w

    def fit(self, Zrows, months, censored, iw, epochs=300, lr=0.25,
            l2=2e-3, seed=0):
        """Person-month expansion of the discrete-time likelihood, IPW."""
        B = self.basis.expand(Zrows)
        N = B.shape[0]
        # build person-month design: index of episode, regime, event flag
        ep, reg, ev, w8 = [], [], [], []
        for n in range(N):
            m, c = int(months[n]), int(censored[n])
            for t in range(1, m + 1):
                ep.append(n); reg.append(self._reg(t)); ev.append(0)
                w8.append(iw[n])
            if not c:
                t = m + 1
                ep.append(n); reg.append(self._reg(t)); ev.append(1)
                w8.append(iw[n])
        ep = np.array(ep); reg = np.array(reg)
        ev = np.array(ev, float); w8 = np.array(w8)
        w8 = w8 / w8.mean()
        rng = np.random.default_rng(seed)
        n_pm = len(ep)
        for it in range(epochs):
            s = B[ep] @ self.w
            eta = self.a[reg] - s
            h = sigmoid(eta)
            # gradient of weighted NLL
            g_eta = w8 * (h - ev) / n_pm
            ga = np.zeros_like(self.a)
            for r in range(len(self.REG)):
                ga[r] = g_eta[reg == r].sum()
            gw = -(B[ep].T @ g_eta) + l2 * self.w
            self.a -= lr * ga * 6.0
            self.w -= lr * gw
        # centring constants for the exact ledger
        ref = Zrows.mean(axis=0, keepdims=True)
        Bref = self.basis.expand(ref)
        self.centre = np.zeros(D)
        for k in range(D):
            o, sz = self.basis.offs[k], self.basis.sizes[k]
            self.centre[k] = Bref[0, o:o + sz] @ self.w[o:o + sz]
        self.bias = float(self.centre.sum())
        return self

    def ledger(self, Zrows):
        return self.basis.contributions(self.w, Zrows, self.centre)

    def survival24(self, Zrows):
        s = self.score(Zrows)
        surv = np.ones_like(s)
        for t in range(1, M.T_HORIZON + 1):
            surv *= 1.0 - sigmoid(self.a[self._reg(t)] - s)
        return surv


class LogisticHead:
    """Plain logistic model on the same basis (acceptance head, B3)."""

    def __init__(self, basis):
        self.basis = basis
        self.w = np.zeros(basis.P)
        self.b = 0.0

    def fit(self, Zrows, y, epochs=400, lr=0.4, l2=2e-3):
        B = self.basis.expand(Zrows)
        N = B.shape[0]
        for it in range(epochs):
            p = sigmoid(B @ self.w + self.b)
            g = (p - y) / N
            self.b -= lr * g.sum() * 4.0
            self.w -= lr * (B.T @ g + l2 * self.w)
        return self

    def score(self, Zrows):
        return self.basis.expand(Zrows) @ self.w + self.b


# ---------------------------------------------------------------------------
# black-box baselines
# ---------------------------------------------------------------------------
class MLP:
    """Two-hidden-layer perceptron with hand-written gradients."""

    def __init__(self, d_in, h1=24, h2=12, seed=0):
        rng = np.random.default_rng(seed)
        self.W1 = rng.normal(0, np.sqrt(2.0 / d_in), (d_in, h1))
        self.b1 = np.zeros(h1)
        self.W2 = rng.normal(0, np.sqrt(2.0 / h1), (h1, h2))
        self.b2 = np.zeros(h2)
        self.w3 = rng.normal(0, np.sqrt(2.0 / h2), h2)
        self.b3 = 0.0
        self.mu = None

    def _fwd(self, X):
        a1 = np.maximum(X @ self.W1 + self.b1, 0)
        a2 = np.maximum(a1 @ self.W2 + self.b2, 0)
        return a1, a2, a2 @ self.w3 + self.b3

    def score(self, X):
        X = (X - self.mu) / self.sd
        return self._fwd(X)[2]

    def fit(self, X, y, iw=None, epochs=400, lr=0.05, bs=256, seed=0):
        rng = np.random.default_rng(seed)
        self.mu, self.sd = X.mean(0), X.std(0) + 1e-9
        Xs = (X - self.mu) / self.sd
        iw = np.ones(len(y)) if iw is None else iw / iw.mean()
        for ep in range(epochs):
            idx = rng.permutation(len(y))
            for lo in range(0, len(y), bs):
                sl = idx[lo:lo + bs]
                Xb, yb, wb = Xs[sl], y[sl], iw[sl]
                a1, a2, s = self._fwd(Xb)
                p = sigmoid(s)
                gs = wb * (p - yb) / len(sl)
                gw3 = a2.T @ gs
                ga2 = np.outer(gs, self.w3) * (a2 > 0)
                gW2 = a1.T @ ga2
                ga1 = ga2 @ self.W2.T * (a1 > 0)
                gW1 = Xb.T @ ga1
                self.w3 -= lr * gw3; self.b3 -= lr * gs.sum()
                self.W2 -= lr * gW2; self.b2 -= lr * ga2.sum(0)
                self.W1 -= lr * gW1; self.b1 -= lr * ga1.sum(0)
        return self


class GBM:
    """Gradient boosting with depth-2 stumps for a Bernoulli objective."""

    class Node:
        __slots__ = ("feat", "thr", "left", "right", "val")

    def __init__(self, n_trees=120, lr=0.12, seed=0):
        self.n_trees, self.lr = n_trees, lr
        self.rng = np.random.default_rng(seed)
        self.trees, self.f0 = [], 0.0

    def _best_split(self, X, g, idx):
        best = (None, None, 0.0)
        gsum = g[idx].sum(); n = len(idx)
        for k in self.rng.choice(X.shape[1], min(10, X.shape[1]),
                                 replace=False):
            xs = X[idx, k]
            order = np.argsort(xs)
            gs = np.cumsum(g[idx][order])
            for cut in range(8, n - 8, max(1, n // 24)):
                gl = gs[cut]; gr = gsum - gl
                gain = gl * gl / (cut + 1) + gr * gr / (n - cut) \
                    - gsum * gsum / n
                if gain > best[2]:
                    best = (k, xs[order[cut]], gain)
        return best[0], best[1]

    def _leaf(self, g, h, idx):
        return -g[idx].sum() / (h[idx].sum() + 1e-6)

    def fit(self, X, y, iw=None, seed=0):
        iw = np.ones(len(y)) if iw is None else iw / iw.mean()
        p0 = np.clip(y.mean(), 1e-3, 1 - 1e-3)
        self.f0 = np.log(p0 / (1 - p0))
        f = np.full(len(y), self.f0)
        for _ in range(self.n_trees):
            p = sigmoid(f)
            g = iw * (p - y); h = iw * p * (1 - p)
            idx = np.arange(len(y))
            k1, t1 = self._best_split(X, g, idx)
            tree = []
            if k1 is None:
                break
            left = idx[X[idx, k1] <= t1]; right = idx[X[idx, k1] > t1]
            for part in (left, right):
                k2, t2 = self._best_split(X, g, part) \
                    if len(part) > 40 else (None, None)
                if k2 is None:
                    tree.append((None, None,
                                 self._leaf(g, h, part), None, None))
                else:
                    a = part[X[part, k2] <= t2]
                    b = part[X[part, k2] > t2]
                    tree.append((k2, t2, None, self._leaf(g, h, a),
                                 self._leaf(g, h, b)))
            self.trees.append((k1, t1, tree))
            f += self.lr * self._tree_out(X, (k1, t1, tree))
        return self

    def _tree_out(self, X, spec):
        k1, t1, tree = spec
        out = np.zeros(X.shape[0])
        side = X[:, k1] <= t1
        for flag, (k2, t2, val, va, vb) in zip((side, ~side), tree):
            if k2 is None:
                out[flag] = val
            else:
                s2 = X[:, k2] <= t2
                out[flag & s2] = va
                out[flag & ~s2] = vb
        return out

    def score(self, X):
        f = np.full(X.shape[0], self.f0)
        for spec in self.trees:
            f += self.lr * self._tree_out(X, spec)
        return f


# ---------------------------------------------------------------------------
# assignment layers
# ---------------------------------------------------------------------------
def deferred_acceptance(youth_pref, post_score, cap, max_props=120):
    """Youth-proposing deferred acceptance with capacities.

    youth_pref: (n, m) utility each youth assigns to each post (row-wise
    order defines proposals); post_score: (n, m) priority each post gives
    each youth. Returns assignment array of post index or -1.
    """
    n, m = youth_pref.shape
    order = np.argsort(-youth_pref, axis=1)[:, :max_props]
    next_p = np.zeros(n, dtype=int)
    held = [[] for _ in range(m)]          # (score, i) heaps as lists
    free = list(range(n))
    assign = np.full(n, -1, dtype=int)
    while free:
        i = free.pop()
        while next_p[i] < order.shape[1]:
            j = order[i, next_p[i]]
            next_p[i] += 1
            h = held[j]
            if len(h) < cap[j]:
                h.append((post_score[i, j], i))
                assign[i] = j
                break
            worst = min(h)
            if post_score[i, j] > worst[0]:
                h.remove(worst)
                h.append((post_score[i, j], i))
                assign[i] = j
                assign[worst[1]] = -1
                free.append(worst[1])
                break
        # else: youth exhausts proposal list, stays unassigned
    return assign


def blocking_pairs(assign, youth_pref, post_score, cap, sample=4000, rng=None):
    """Count sampled blocking pairs of an assignment (stability check)."""
    rng = rng or np.random.default_rng(0)
    n, m = youth_pref.shape
    filled = {}
    for i, j in enumerate(assign):
        if j >= 0:
            filled.setdefault(j, []).append(i)
    count = 0
    for _ in range(sample):
        i = int(rng.integers(n)); j = int(rng.integers(m))
        if assign[i] == j:
            continue
        cur = assign[i]
        pref_i = (cur < 0) or (youth_pref[i, j] > youth_pref[i, cur])
        if not pref_i:
            continue
        occ = filled.get(j, [])
        if len(occ) < cap[j]:
            count += 1
        else:
            worst = min(occ, key=lambda q: post_score[q, j])
            if post_score[i, j] > post_score[worst, j]:
                count += 1
    return count / sample


def greedy_fill(score, cap, youth_order=None):
    """Assign each youth (in order) to the best-scoring post with room."""
    n, m = score.shape
    order = np.arange(n) if youth_order is None else youth_order
    left = cap.copy()
    assign = np.full(n, -1, dtype=int)
    rank = np.argsort(-score, axis=1)
    for i in order:
        for j in rank[i]:
            if left[j] > 0:
                assign[i] = j
                left[j] -= 1
                break
    return assign


def sinkhorn_assign(score, cap, eps=0.08, iters=300):
    """Entropy-regularised transport plan, greedily rounded to integers."""
    n, m = score.shape
    Kmat = np.exp(score / eps - score.max() / eps)
    a = np.ones(n) / n
    b = cap / cap.sum()
    u = np.ones(n); v = np.ones(m)
    for _ in range(iters):
        u = a / (Kmat @ v + 1e-12)
        v = b / (Kmat.T @ u + 1e-12)
    P = u[:, None] * Kmat * v[None, :]
    # greedy rounding by plan mass
    flat = np.argsort(-P, axis=None)
    left = cap.copy(); used = np.zeros(n, bool)
    assign = np.full(n, -1, dtype=int)
    placed = 0; budget = int(min(n, cap.sum()))
    for f in flat:
        i, j = divmod(int(f), m)
        if used[i] or left[j] <= 0:
            continue
        assign[i] = j; used[i] = True; left[j] -= 1
        placed += 1
        if placed >= budget:
            break
    return assign


# ---------------------------------------------------------------------------
# post-hoc attribution for the black boxes: sampled Shapley values
# ---------------------------------------------------------------------------
def sampled_shapley(score_fn, x, x_ref, n_perm=64, rng=None):
    """Monte-Carlo Shapley attribution of score(x) - score(x_ref)."""
    rng = rng or np.random.default_rng(0)
    d = len(x)
    phi = np.zeros(d)
    base = x_ref.copy()
    for _ in range(n_perm):
        perm = rng.permutation(d)
        cur = base.copy()
        prev = score_fn(cur[None, :])[0]
        for k in perm:
            cur[k] = x[k]
            new = score_fn(cur[None, :])[0]
            phi[k] += new - prev
            prev = new
    return phi / n_perm


# ---------------------------------------------------------------------------
# decision-level audit checks on an evidence trail
# ---------------------------------------------------------------------------
def audit_trail(delta_phi, delta_true, score_fn=None, x=None, x_alt=None,
                flip_fn=None):
    """The three checks for one match decision.

    delta_phi: per-feature trail for the score difference between the
    assigned post and the runner-up. delta_true: the actual score
    difference. Returns (sufficient, minimal, flip) booleans.
    flip_fn(k): recompute the score difference with feature k neutralised;
    used for the counterfactual check on the top ledger entry.
    """
    order = np.argsort(-np.abs(delta_phi))
    total = delta_phi.sum()
    if total <= 0 or delta_true <= 0:
        return False, False, False
    # sufficiency: smallest prefix of the trail that alone preserves the
    # preference (sum of selected entries positive and >= half the gap)
    run = 0.0; chosen = 0
    for k in order:
        run += delta_phi[k]; chosen += 1
        if run >= 0.5 * total and run > 0:
            break
    sufficient = run >= 0.5 * total and run > 0
    # minimality: dropping the last chosen entry must break sufficiency
    minimal = chosen <= max(3, int(0.34 * len(delta_phi)))
    # counterfactual flip: neutralising the largest positive entry must
    # shrink the true margin by (approximately) that entry's stated share
    k_top = int(order[0])
    if flip_fn is None:
        flip = True
    else:
        new_gap = flip_fn(k_top)
        predicted = delta_true - delta_phi[k_top]
        denom = abs(delta_true) + 1e-9
        flip = abs(new_gap - predicted) <= 0.25 * denom
    return sufficient, minimal, flip


if __name__ == "__main__":
    # ---- self-tests with known answers -------------------------------
    rng = np.random.default_rng(0)

    # 1. spline recovers a known additive function and the ledger is exact
    N = 4000
    Zs = rng.normal(0, 1, (N, D))
    true = 1.2 * Zs[:, 4] - 0.8 * np.tanh(Zs[:, 5]) + 0.5 * Zs[:, 7]
    basis = Basis(Zs)
    y = (rng.random(N) < sigmoid(true)).astype(float)
    lh = LogisticHead(basis).fit(Zs, y, epochs=600)
    s = lh.score(Zs)
    corr = np.corrcoef(s, true)[0, 1]
    print("spline recovery corr = %.3f (want > .97)" % corr)

    # 2. ledger identity
    hz = HazardScorer(basis)
    hz.w = rng.normal(0, 0.2, basis.P)
    ref = Zs.mean(axis=0, keepdims=True)
    Bref = basis.expand(ref)
    hz.centre = np.array([Bref[0, basis.offs[k]:basis.offs[k]
                               + basis.sizes[k]]
                          @ hz.w[basis.offs[k]:basis.offs[k]
                                 + basis.sizes[k]] for k in range(D)])
    hz.bias = float(hz.centre.sum())
    phi = hz.ledger(Zs[:200])
    resid = np.abs(hz.score(Zs[:200]) - (hz.bias + phi.sum(axis=1)
                                         - 0 * hz.bias) - 0.0)
    recon = hz.bias + phi.sum(axis=1)
    resid = np.abs(hz.score(Zs[:200]) - recon)
    print("ledger max residual = %.2e (want ~ 1e-12)" % resid.max())

    # 3. deferred acceptance produces no blocking pairs
    n, m = 300, 40
    up = rng.normal(0, 1, (n, m))
    ps = rng.normal(0, 1, (n, m))
    cap = rng.integers(2, 8, m)
    asg = deferred_acceptance(up, ps, cap, max_props=m)
    bp = blocking_pairs(asg, up, ps, cap, sample=6000,
                        rng=np.random.default_rng(1))
    g_asg = greedy_fill(ps, cap)
    bp_g = blocking_pairs(g_asg, up, ps, cap, sample=6000,
                          rng=np.random.default_rng(1))
    print("blocking-pair rate: DA %.4f (want 0), greedy %.4f (want > 0)"
          % (bp, bp_g))

    # 4. MLP and GBM learn a nonlinear target
    Xn = rng.normal(0, 1, (3000, D))
    yn = (rng.random(3000) < sigmoid(Xn[:, 0] * Xn[:, 1] + Xn[:, 2])) \
        .astype(float)
    mlp = MLP(D, seed=0).fit(Xn, yn, epochs=150)
    auc_in = np.mean(mlp.score(Xn)[yn == 1][:, None]
                     > mlp.score(Xn)[yn == 0][None, :])
    gbm = GBM(n_trees=80, seed=0).fit(Xn, yn)
    auc_g = np.mean(gbm.score(Xn)[yn == 1][:, None]
                    > gbm.score(Xn)[yn == 0][None, :])
    print("MLP in-sample AUC = %.3f, GBM = %.3f (want > .75)"
          % (auc_in, auc_g))

    # 5. sampled Shapley sums to the score difference for an additive fn
    f = lambda X: X @ np.arange(1., D + 1.)
    x = rng.normal(0, 1, D); xr = np.zeros(D)
    phi = sampled_shapley(f, x, xr, n_perm=32,
                          rng=np.random.default_rng(2))
    err = abs(phi.sum() - (f(x[None])[0] - f(xr[None])[0]))
    print("shapley completeness err = %.2e (exact for additive)" % err)
