# -*- coding: utf-8 -*-
"""Paper 9 — the model.

An education-to-work system with two fields of study.  Firms hire through a
field-specific matching market with free entry; the two kinds of graduate are
imperfect substitutes in production, so the marginal product of a field falls as its
employment stock grows.  Entrants choose a field by a discrete-choice rule, but a
degree takes D years, so the cohort that reacts to today's market reaches that market
D years late.

The result is a delay dynamical system.  Its state is the two employment stocks, the
two searcher stocks and the D-1 cohorts already in the pipeline.  Whether a demand
shock is absorbed monotonically or converted into a self-sustaining cycle is decided
by one number, the feedback gain, which the calibration pins down.

Everything is deterministic; every number reported in the manuscript comes from here.
"""
import numpy as np
from scipy.optimize import brentq, root

SEED = 20260731


# ================================================================= parameters
class Params:
    """Model parameters.

    Externally set: the degree lag, the discount rate, the matching elasticity, the
    separation rate, the rate at which workers leave the entry tier, worker bargaining
    power, and the elasticity of substitution between the two kinds of graduate.

    Estimated: matching efficiency, the vacancy cost, the flow value of non-work,
    relative field productivity, the intensity of choice and the amenity differential.
    """

    # ---- externally set
    D = 4  # years from field choice to graduation
    r = 0.04  # annual discount rate
    alpha = 0.5  # matching elasticity with respect to searchers
    eta = 0.5  # worker bargaining power (Hosios at alpha = eta)
    delta = 0.10  # annual separation rate
    gam = 1.0 / 7.0  # rate of leaving the entry tier: ages 22-29
    sigma = 2.0  # elasticity of substitution between the two fields

    # ---- estimated
    mu = 1.0  # matching efficiency
    kappa = 1.0  # vacancy posting cost
    b = 0.40  # flow value of non-work
    A = None  # field productivities, A[0] is the exposed field
    beta = 1.0  # intensity of choice
    amen = 0.0  # amenity of field 0 relative to field 1, in units of value

    # ---- belief block
    phi = 1.0  # strength of trend extrapolation in the extrapolative rule
    psi = 0.0  # intensity of choice over forecasting rules; 0 = fixed equal shares
    cost = 0.0  # per-period cost of the anchored rule
    mem = 0.5  # memory in the fitness measure, in [0, 1)
    omega = 1.0  # precision of the signal about current returns, in [0, 1]
    pipe = 0.0  # share of the enrolled pipeline entrants can see, in [0, 1]

    N = 1.0  # entering cohort, normalised

    def __init__(self, **kw):
        self.A = np.array([1.0, 1.0])
        for k, v in kw.items():
            if not hasattr(Params, k):
                raise KeyError(k)
            setattr(self, k, v)

    def copy(self, **kw):
        p = Params()
        for k in ('D', 'r', 'alpha', 'eta', 'delta', 'gam', 'sigma', 'mu', 'kappa',
                  'b', 'beta', 'amen', 'phi', 'psi', 'cost', 'mem', 'omega', 'pipe',
                  'N'):
            setattr(p, k, getattr(self, k))
        p.A = self.A.copy()
        for k, v in kw.items():
            if not hasattr(Params, k):
                raise KeyError(k)
            setattr(p, k, v)
        return p


# ================================================================= production
def marginal_products(p, E):
    """Marginal product of an entry-tier worker in each field under CES production.

    Output is Y = [ (A0 E0)^rho + (A1 E1)^rho ]^(1/rho) with rho = (sigma-1)/sigma, so
    the marginal product of field j is A_j^rho Y^(1-rho) E_j^(rho-1) and falls in E_j at
    rate 1/sigma.  E_j is the stock of *entry-tier* workers in the field, not its whole
    workforce: a new graduate competes for entry-level positions with other recent
    graduates rather than with mid-career staff, which is both what the recent evidence
    on AI and junior hiring describes and what gives the feedback loop a stock fast
    enough to matter within a cohort's horizon.
    """
    rho = (p.sigma - 1.0) / p.sigma
    E = np.maximum(np.asarray(E, dtype=float), 1e-9)
    z = (p.A * E) ** rho
    Y = z.sum() ** (1.0 / rho)
    return p.A ** rho * Y ** (1.0 - rho) * E ** (rho - 1.0), Y


# =================================================================== matching
def solve_tightness(p, mp):
    """Free-entry tightness in a field whose marginal product is mp.

    The match surplus is S = (mp - b) / (r + delta + ret + eta f), because the worker's
    share raises the value of continued search and so eats into the surplus.  Free entry
    sets the expected cost of a hire equal to the firm's share of that surplus:

        kappa * theta^alpha / mu = (1 - eta) S,     f = mu theta^(1-alpha).

    At the standard alpha = 1/2 this is a quadratic in sqrt(theta) and solves in closed
    form; for any other alpha it is monotone in theta and bisection is safe.
    """
    if mp <= p.b:
        return 0.0
    d = p.r + p.delta + p.gam
    rhs = (1.0 - p.eta) * (mp - p.b)

    if abs(p.alpha - 0.5) < 1e-12:
        a_, b_, c_ = p.kappa * p.eta, p.kappa * d / p.mu, -rhs
        y = (-b_ + np.sqrt(b_ * b_ - 4 * a_ * c_)) / (2 * a_)
        return float(y * y)

    def gap(th):
        f = p.mu * th ** (1.0 - p.alpha)
        return p.kappa * th ** p.alpha / p.mu - rhs / (d + p.eta * f)

    hi = 1.0
    while gap(hi) < 0.0:
        hi *= 2.0
        if hi > 1e12:
            return hi
    return brentq(gap, 1e-12, hi, xtol=1e-14, rtol=1e-15)


def market(p, E):
    """Prices and rates in both fields given the two employment stocks.

    With d = r + delta + ret, the match surplus is S = (mp - b) / (d + eta f) and the
    wage that implements the Nash split is w = b + eta S (d + f): the worker is paid
    her outside flow plus her share of the surplus, annuitised over the match and over
    the search it saved her.
    """
    mp, Y = marginal_products(p, E)
    th = np.array([solve_tightness(p, mp[0]), solve_tightness(p, mp[1])])
    f = p.mu * th ** (1.0 - p.alpha)
    d = p.r + p.delta + p.gam
    S = (mp - p.b) / (d + p.eta * f)
    w = p.b + p.eta * S * (d + f)
    V = (p.b + f * p.eta * S) / p.r          # value of entering the field
    return dict(mp=mp, Y=Y, theta=th, f=f, S=S, w=w, V=V)


# ================================================================ field choice
def choice_share(p, V, amen=None):
    """Logit share entering the exposed field, given the two entry values.

    The index is the annuitised differential x = r(V0 - V1) + amenity, a flow
    comparable to a wage, so the intensity of choice beta and the amenity are both in
    interpretable units.
    """
    a = p.amen if amen is None else amen
    x = p.r * (V[0] - V[1]) + a
    return float(1.0 / (1.0 + np.exp(-p.beta * x)))


# ============================================================== state and step
class State:
    """(E0, E1, U0, U1, and the D cohorts currently enrolled)."""

    def __init__(self, E, U, pipeline):
        self.E = np.asarray(E, dtype=float)
        self.U = np.asarray(U, dtype=float)
        self.pipeline = list(pipeline)  # pipeline[0] graduates next period

    def copy(self):
        return State(self.E.copy(), self.U.copy(), list(self.pipeline))

    def vec(self):
        return np.concatenate([self.E, self.U, np.array(self.pipeline)])

    @staticmethod
    def from_vec(v, D):
        return State(v[0:2], v[2:4], list(v[4:4 + D]))


def differential(p, mkt, amen=None):
    """The object entrants actually decide on: the value of the exposed field relative
    to the alternative, in annuitised units, including the amenity."""
    a = p.amen if amen is None else amen
    return float(p.r * (mkt['V'][0] - mkt['V'][1]) + a)


class Beliefs:
    """An adaptive belief system over two forecasting rules.

    Entrants must forecast what a field will be worth when they graduate, D years from
    now.  Two rules are available.  The *anchored* rule reports the value that would
    prevail if the field's supply were at its long-run level; it is right on average but
    requires knowing that level, so it carries a cost.  The *extrapolative* rule takes
    the most recent observation and projects the recent change forward; it is free, and
    while a trend lasts it is the more accurate of the two.

    The population weight on each rule is a logit in its recent forecasting performance,
    with intensity of choice psi.  This is the mechanism of Brock and Hommes: when psi is
    small the weights barely move and the system behaves as if beliefs were fixed; as psi
    rises, success breeds imitation, a run of accurate extrapolation pulls more entrants
    onto the extrapolative rule, and the steady state can lose stability even though
    every individual rule is reasonable and every entrant is responding sensibly to what
    she sees.
    """

    def __init__(self, p, x_bar):
        self.p = p
        self.x_bar = x_bar          # the fundamental the anchored rule targets
        self.x_hist = [x_bar, x_bar]   # observed differential, most recent last
        self.n = np.array([0.5, 0.5])  # weights on (anchored, extrapolative)
        self.pi = np.zeros(2)       # fitness, carried forward with memory
        self.pending = []           # forecasts awaiting their realisation date

    def forecasts(self, x_pipe=None):
        """What each rule predicts for the differential D years ahead."""
        x1, x0 = self.x_hist[-1], self.x_hist[-2]
        anchored = self.x_bar if x_pipe is None else x_pipe
        extrap = x1 + self.p.phi * (x1 - x0)
        return np.array([anchored, extrap])

    def perceived(self, x_pipe=None):
        """The population's forecast: the weighted average of the two rules."""
        fc = self.forecasts(x_pipe)
        x = float(self.n @ fc)
        if self.p.omega < 1.0:
            # a noisier signal about current conditions shrinks the perceived
            # differential toward its long-run value
            x = self.x_bar + self.p.omega * (x - self.x_bar)
        return x, fc

    def update(self, x_now):
        """Record the realised differential, score the forecasts that targeted it, and
        re-weight the rules."""
        due = [f for (t, f) in self.pending if t == 0]
        self.pending = [(t - 1, f) for (t, f) in self.pending if t > 0]
        if due:
            fc = due[0]
            util = -(x_now - fc) ** 2 - np.array([self.p.cost, 0.0])
            # fitness carries memory, as in the standard implementation; without it a
            # single large error flips the whole population between rules
            self.pi = self.p.mem * self.pi + (1.0 - self.p.mem) * util
            z = self.p.psi * self.pi
            z = z - z.max()
            e = np.exp(z)
            self.n = e / e.sum()
        self.x_hist.append(x_now)
        if len(self.x_hist) > 8:
            self.x_hist.pop(0)

    def submit(self, fc):
        self.pending.append((self.p.D, fc))


def pipeline_value(p, st):
    """The differential entrants would face if the enrolled pipeline were already at work.

    This is the object that published enrolment statistics reveal.  An entrant who can
    see how many students are already studying each field can price the congestion that
    is coming, which is exactly the information the extrapolative rule lacks.
    """
    inflight = np.array([sum(st.pipeline), p.D * p.N - sum(st.pipeline)])
    E = st.E + inflight / max(p.D, 1)
    return differential(p, market(p, E))


def step(p, st, bel):
    """One year: observe, forecast, choose a field, and move the stocks."""
    mkt = market(p, st.E)
    x_now = differential(p, mkt)
    bel.update(x_now)

    x_pipe = None
    if p.pipe > 0.0:
        x_pipe = (1.0 - p.pipe) * bel.x_bar + p.pipe * pipeline_value(p, st)
    x_e, fc = bel.perceived(x_pipe)
    bel.submit(fc)

    s_new = 1.0 / (1.0 + np.exp(-p.beta * x_e))

    grad = st.pipeline[0] * p.N
    G = np.array([grad, p.N - grad])

    F = 1.0 - np.exp(-mkt['f'])
    Dl = 1.0 - np.exp(-p.delta)
    R = 1.0 - np.exp(-p.gam)

    U_next = (st.U * (1.0 - F) + st.E * Dl) * (1.0 - R) + G
    E_next = (st.E * (1.0 - Dl) + st.U * F) * (1.0 - R)

    return State(E_next, U_next, st.pipeline[1:] + [s_new]), mkt, s_new


def graduate_unemployment(p, st, mkt):
    """Share of the graduating cohort still searching after one year."""
    grad = st.pipeline[0]
    return float(grad * np.exp(-mkt['f'][0]) + (1.0 - grad) * np.exp(-mkt['f'][1]))


# =============================================================== steady state
def stationary_stocks(p, s):
    """Stocks that reproduce themselves when a constant share s enters field 0.

    In annual transition probabilities F = 1 - exp(-f), Dl = 1 - exp(-delta) and
    R = 1 - exp(-gamma), the two flow equations are

        E = [E (1-Dl) + U F] (1-R),        U = [U (1-F) + E Dl] (1-R) + G,

    which are linear in (E, U) for a given F and solve exactly; F depends on E, so the
    pair is a two-dimensional fixed point.  It is solved by Newton rather than by
    successive substitution, because the calibration differentiates through this
    routine and a loosely converged inner solve makes the outer objective non-smooth.
    """
    G = np.array([s, 1.0 - s]) * p.N
    Dl = 1.0 - np.exp(-p.delta)
    R = 1.0 - np.exp(-p.gam)

    def stocks(f):
        F = 1.0 - np.exp(-f)
        k1 = 1.0 - (1.0 - Dl) * (1.0 - R)
        k2 = F * (1.0 - R)
        k3 = 1.0 - (1.0 - F) * (1.0 - R)
        k4 = Dl * (1.0 - R)
        U = G * k1 / (k3 * k1 - k2 * k4)
        return k2 * U / k1, U

    def resid(logE):
        E = np.exp(logE)
        E_new, _ = stocks(market(p, E)['f'])
        return np.log(np.maximum(E_new, 1e-300)) - logE

    x0 = np.log(np.maximum(G / (Dl + R), 1e-9))
    sol = root(resid, x0, method='hybr', tol=1e-14)
    E = np.exp(sol.x)
    return stocks(market(p, E)['f'])


def steady_state(p):
    """Stationary equilibrium: the entering share that reproduces itself."""
    def gap(s):
        E, _ = stationary_stocks(p, s)
        return choice_share(p, market(p, E)['V']) - s

    # the endpoints bracket the root in almost every admissible parameterisation, so
    # try them first; only fall back to a scan when they do not, which happens when one
    # field is nearly empty and the map is very flat near the boundary
    lo, hi = 1e-6, 1.0 - 1e-6
    flo, fhi = gap(lo), gap(hi)
    if flo * fhi > 0:
        grid = np.concatenate([np.geomspace(1e-6, 1e-2, 15),
                               np.linspace(1e-2, 1.0 - 1e-2, 60),
                               1.0 - np.geomspace(1e-6, 1e-2, 15)[::-1]])
        vals = np.array([gap(g) for g in grid])
        idx = np.where(np.sign(vals[:-1]) * np.sign(vals[1:]) <= 0)[0]
        if len(idx) == 0:
            raise RuntimeError('no interior stationary share')
        i = int(idx[0])
        lo, hi = grid[i], grid[i + 1]
    s_star = brentq(gap, lo, hi, xtol=1e-14, rtol=8.9e-16)
    E, U = stationary_stocks(p, s_star)
    st = State(E, U, [s_star] * p.D)
    return s_star, st, market(p, E)


# ================================================================== stability
def loop_gain(p, s_star, h=1e-5):
    """The gain of the education-labour feedback loop.

    An extra percentage point of a cohort entering the exposed field raises that field's
    entry-tier stock, lowers its marginal product at rate 1/sigma, lowers the value of
    entering it, and so lowers the share the next reacting cohort sends.  The gain is
    the product of those three steps evaluated where the system rests.  Under the
    anchored rule alone the map is s_t = Phi(s_{t-D}), whose eigenvalues are the D-th
    roots of this number, so a gain below one in absolute value means a shock dies out.
    """
    def loop(s):
        E, _ = stationary_stocks(p, s)
        return choice_share(p, market(p, E)['V'])

    return (loop(s_star + h) - loop(s_star - h)) / (2 * h)


def supply_elasticity(p, s_star, h=1e-4):
    """d log s / d log (w0/w1): the object the field-of-study literature estimates."""
    E, _ = stationary_stocks(p, s_star)
    out = []
    for sgn in (1.0, -1.0):
        q = p.copy()
        q.A = p.A.copy()
        q.A[0] = p.A[0] * (1.0 + sgn * h)
        m = market(q, E)
        out.append((np.log(choice_share(q, m['V'])), np.log(m['w'][0] / m['w'][1])))
    return (out[0][0] - out[1][0]) / (out[0][1] - out[1][1])


def steady_weights(p):
    """Weights on the two rules at the stationary state.

    Both rules forecast the stationary differential correctly when the system is at
    rest, so their squared errors are equal and only the cost of the anchored rule
    separates them.  The weight on extrapolation is therefore 1/(1+exp(-psi*cost)),
    which rises from one half towards one as the intensity of choice grows: the classic
    result that cheap rules crowd out costly ones when agents imitate success sharply.
    """
    return float(1.0 / (1.0 + np.exp(-p.psi * p.cost)))


def dominant_mode(p, st, periods=260, eps=1e-4, burn=40):
    """Modulus and period of the dominant mode, measured from a perturbed simulation.

    With endogenous rule selection the state includes the belief system's own memory, so
    rather than differentiate an awkward extended map we perturb the stationary state,
    simulate, and read the dominant behaviour off the response: the modulus from the
    slope of the log envelope, the period from the spacing of sign changes.  A modulus
    above one is an unstable stationary state.
    """
    s_star = st.pipeline[0]
    st0 = st.copy()
    st0.pipeline = [s_star * (1.0 + eps)] + list(st.pipeline[1:])
    out = simulate(p, st0, periods)
    dev = out['s'] - s_star
    dev = dev[burn:]
    a = np.abs(dev)
    a = np.maximum(a, 1e-300)

    # modulus: least squares slope of log|deviation| against time, over the window in
    # which the signal is still above numerical noise
    keep = a > a[0] * 1e-9
    n = max(int(keep.sum()), 5)
    t = np.arange(n)
    sl = np.polyfit(t, np.log(a[:n]), 1)[0]
    mod = float(np.exp(sl))

    sign = np.sign(dev[:n])
    flips = int(np.sum(sign[1:] * sign[:-1] < 0))
    per = float(2.0 * n / flips) if flips > 0 else float('inf')
    return dict(modulus=mod, period=per, deviation=dev)


def bifurcation(p, st, values, key='psi', periods=400, keep=120):
    """Attractor of the entering share as one parameter is swept."""
    xs, ys = [], []
    for v in values:
        q = p.copy()
        setattr(q, key, float(v))
        out = simulate(q, st, periods)
        tail = out['s'][-keep:]
        for y in tail:
            xs.append(float(v)); ys.append(float(y))
    return np.array(xs), np.array(ys)


# ================================================================== simulation
def simulate(p, st0, periods, shock=None, x_bar=None):
    """Run the system forward; shock(t) multiplies the exposed field's productivity."""
    st = st0.copy()
    if x_bar is None:
        x_bar = differential(p, market(p, st0.E))
    # after a permanent shock the long-run differential moves, and an "anchored" rule
    # that kept targeting the old one would not be anchored but stale.  The
    # fundamental for each regime is solved once here and switched at the shock date.
    x_bar_post = x_bar
    if shock is not None:
        z_end = shock(periods - 1)
        if abs(z_end - 1.0) > 1e-12:
            q = p.copy(); q.A = p.A.copy(); q.A[0] = p.A[0] * z_end
            _, st_post, mkt_post = steady_state(q)
            x_bar_post = differential(q, mkt_post)
    bel = Beliefs(p, x_bar)
    bel.n = np.array([1.0 - steady_weights(p), steady_weights(p)])

    keys = ('s', 'u', 'u0', 'u1', 'E0', 'E1', 'w0', 'w1', 'A0', 'Y',
            'f0', 'f1', 'prem', 'x', 'n_extrap')
    out = {k: [] for k in keys}
    for t in range(periods):
        pt = p
        if shock is not None:
            pt = p.copy()
            pt.A = p.A.copy()
            pt.A[0] = p.A[0] * shock(t)
        mkt = market(pt, st.E)
        bel.x_bar = x_bar if (shock is None or abs(shock(t) - 1.0) < 1e-12) else x_bar_post
        out['u'].append(graduate_unemployment(pt, st, mkt))
        out['u0'].append(float(np.exp(-mkt['f'][0])))
        out['u1'].append(float(np.exp(-mkt['f'][1])))
        out['E0'].append(st.E[0]); out['E1'].append(st.E[1])
        out['w0'].append(mkt['w'][0]); out['w1'].append(mkt['w'][1])
        out['f0'].append(mkt['f'][0]); out['f1'].append(mkt['f'][1])
        out['prem'].append(mkt['w'][0] / mkt['w'][1])
        out['A0'].append(pt.A[0]); out['Y'].append(mkt['Y'])
        out['x'].append(differential(pt, mkt))
        out['n_extrap'].append(float(bel.n[1]))
        st, mkt, s_new = step(pt, st, bel)
        out['s'].append(s_new)
    return {k: np.array(v) for k, v in out.items()}


if __name__ == '__main__':
    p = Params(beta=0.47, sigma=2.0, mu=3.85, A=np.array([0.106, 1.0]), amen=-6.42,
               phi=1.0, psi=0.0, cost=0.0)
    s, st, mkt = steady_state(p)
    print('share %.4f  premium %.3f  gain %.4f' %
          (s, mkt['w'][0] / mkt['w'][1], loop_gain(p, s)))
    for psi in (0.0, 20.0, 60.0, 120.0):
        q = p.copy(); q.psi = psi; q.cost = 0.02
        d = dominant_mode(q, st)
        print('psi %6.1f  n_extrap %.3f  modulus %.4f  period %.2f'
              % (psi, steady_weights(q), d['modulus'], d['period']))
