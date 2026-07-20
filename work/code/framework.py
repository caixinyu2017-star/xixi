"""Shared experiment framework: FEs-budget metaheuristic runner.

Every algorithm is a function  algo(prob, max_fes, N, rng) -> (best_f, best_x, curve)
where curve records the best-so-far fitness at every checkpoint (per generation).
"""
import numpy as np


class Problem:
    def __init__(self, fobj, lb, ub, dim, name=""):
        self.fobj = fobj
        self.lb = np.asarray(lb, dtype=float) * np.ones(dim)
        self.ub = np.asarray(ub, dtype=float) * np.ones(dim)
        self.dim = dim
        self.name = name

    def evaluate(self, x):
        return float(self.fobj(x))


class Recorder:
    """Counts FEs and tracks best-so-far; curve sampled at NUM_POINTS even points."""
    NUM_POINTS = 100

    def __init__(self, prob, max_fes):
        self.prob = prob
        self.max_fes = max_fes
        self.fes = 0
        self.best_f = np.inf
        self.best_x = None
        self.curve = np.full(self.NUM_POINTS, np.inf)

    def eval(self, x):
        x = np.clip(x, self.prob.lb, self.prob.ub)
        f = self.prob.evaluate(x)
        self.fes += 1
        if f < self.best_f:
            self.best_f = f
            self.best_x = x.copy()
        idx = min(int(self.fes / self.max_fes * self.NUM_POINTS), self.NUM_POINTS) - 1
        if idx >= 0:
            self.curve[idx] = min(self.curve[idx], self.best_f)
        return f

    def eval_pop(self, X):
        return np.array([self.eval(x) for x in X])

    def budget_left(self):
        return self.fes < self.max_fes

    def finalize(self):
        c = self.curve
        for i in range(1, len(c)):
            if not np.isfinite(c[i]) or c[i] > c[i - 1]:
                c[i] = c[i - 1]
        return self.best_f, self.best_x, c


def init_pop(prob, N, rng):
    return prob.lb + rng.random((N, prob.dim)) * (prob.ub - prob.lb)


def clipx(x, prob):
    return np.clip(x, prob.lb, prob.ub)


def levy(rng, dim, beta=1.5):
    from math import gamma, pi, sin
    sigma = (gamma(1 + beta) * sin(pi * beta / 2) /
             (gamma((1 + beta) / 2) * beta * 2 ** ((beta - 1) / 2))) ** (1 / beta)
    u = rng.normal(0, sigma, dim)
    v = rng.normal(0, 1, dim)
    return u / np.abs(v) ** (1 / beta)
