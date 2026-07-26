"""Shared experiment framework: FE-budget runner with batched evaluation.

Every algorithm is a function

    algo(prob, max_fes, N, rng) -> (best_f, best_x, curve)

and evaluates whole populations at once through ``Recorder.evaluate``.  The
CEC2017 implementation is vectorized over rows, so evaluating a population of
30 costs about the same as evaluating two single points; batching is therefore
worth roughly a factor of twenty and is what makes it practical to regenerate
every table in the paper from one implementation.

Consequence for the algorithms: they are written in *synchronous* form.  All
candidate positions of an iteration are generated from the population as it
stood at the start of that iteration, evaluated together, and then accepted or
rejected by greedy selection.  Every algorithm in this study - the proposed
one, its ablations and all comparison methods - follows the same convention, so
the comparison stays fair.
"""
import numpy as np


class Problem:
    def __init__(self, fobj, lb, ub, dim, name="", batch=False):
        self.fobj = fobj
        self.lb = np.asarray(lb, dtype=float) * np.ones(dim)
        self.ub = np.asarray(ub, dtype=float) * np.ones(dim)
        self.dim = dim
        self.name = name
        self.batch = batch          # True if fobj accepts an (n, D) matrix

    def evaluate(self, X):
        X = np.atleast_2d(X)
        if self.batch:
            v = np.asarray(self.fobj(X), dtype=float).ravel()
        else:
            v = np.array([float(self.fobj(x)) for x in X])
        return np.where(np.isfinite(v), v, 1e30)


class Recorder:
    """Counts FEs, tracks the best-so-far and samples a convergence curve."""

    NUM_POINTS = 100

    def __init__(self, prob, max_fes):
        self.prob = prob
        self.max_fes = int(max_fes)
        self.fes = 0
        self.best_f = np.inf
        self.best_x = None
        self.curve = np.full(self.NUM_POINTS, np.inf)

    # ------------------------------------------------------------------
    def remaining(self):
        return self.max_fes - self.fes

    def budget_left(self):
        return self.fes < self.max_fes

    def evaluate(self, X):
        """Evaluate a population, clipped to the box and to the FE budget.

        Returns the fitness vector; it is shorter than ``X`` only when the
        budget runs out mid-batch, so callers should use ``len(f)``.
        """
        X = np.atleast_2d(np.asarray(X, dtype=float))
        room = self.remaining()
        if room <= 0:
            return np.empty(0)
        if len(X) > room:
            X = X[:room]
        np.clip(X, self.prob.lb, self.prob.ub, out=X)
        f = self.prob.evaluate(X)
        self.fes += len(X)

        i = int(np.argmin(f))
        if f[i] < self.best_f:
            self.best_f = float(f[i])
            self.best_x = X[i].copy()
        idx = min(int(self.fes / self.max_fes * self.NUM_POINTS),
                  self.NUM_POINTS) - 1
        if idx >= 0:
            self.curve[idx] = min(self.curve[idx], self.best_f)
        return f

    def finalize(self):
        c = self.curve
        for i in range(len(c)):
            if not np.isfinite(c[i]):
                c[i] = c[i - 1] if i else self.best_f
            elif i and c[i] > c[i - 1]:
                c[i] = c[i - 1]
        return self.best_f, self.best_x, c


# ---------------------------------------------------------------- helpers
def init_pop(prob, N, rng):
    return prob.lb + rng.random((N, prob.dim)) * (prob.ub - prob.lb)


def clipx(X, prob):
    return np.clip(X, prob.lb, prob.ub)


def greedy(X, F, Xn, Fn):
    """Element-wise greedy acceptance; ``Fn`` may be shorter than ``F``."""
    m = len(Fn)
    if m == 0:
        return X, F
    better = Fn <= F[:m]
    X[:m][better] = Xn[:m][better]
    F[:m][better] = Fn[better]
    return X, F


def levy(rng, shape, beta=1.5):
    from math import gamma, pi, sin
    sigma = (gamma(1 + beta) * sin(pi * beta / 2) /
             (gamma((1 + beta) / 2) * beta * 2 ** ((beta - 1) / 2))) ** (1 / beta)
    u = rng.normal(0, sigma, shape)
    v = rng.normal(0, 1, shape)
    return u / np.abs(v) ** (1 / beta)
