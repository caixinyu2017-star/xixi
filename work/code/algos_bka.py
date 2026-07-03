"""Black-winged Kite Algorithm (Wang et al., 2024, Artif. Intell. Rev.,
doi:10.1007/s10462-024-10723-4) and the proposed multi-strategy variant MSBKA.

BKA follows the paper's equations: per iteration each individual performs the
attacking update (Eq. 2-3) then the migration update (Eq. 4-5), each followed
by greedy selection; the leader is the population best at iteration start.

MSBKA adds three strategies:
  TCM - tent chaotic mapping initialization
  FDB - fitness-distance-balance companion selection in the migration phase
  CGM - adaptive Cauchy-Gaussian hybrid mutation applied to the leader
"""
import numpy as np
from framework import Recorder, init_pop, clipx


def _tent_init(N, D, lb, ub, rng, a=0.7):
    z = np.empty((N, D))
    z0 = rng.random(D)
    z0[z0 == 0] = 0.371
    for i in range(N):
        z0 = np.where(z0 < a, z0 / a, (1 - z0) / (1 - a))
        z0 = np.mod(z0 + 1e-12 * rng.random(D), 1.0)
        z[i] = z0
    return lb + z * (ub - lb)


def _bka_loop(prob, max_fes, N, rng, use_tcm=False, use_fdb=False, use_cgm=False, p=0.9):
    rec = Recorder(prob, max_fes)
    D = prob.dim
    if use_tcm:
        X = _tent_init(N, D, prob.lb, prob.ub, rng)
    else:
        X = init_pop(prob, N, rng)
    F = rec.eval_pop(X)
    T = max(1, max_fes // (2 * N + (1 if use_cgm else 0)))
    t = 0
    while rec.budget_left():
        t += 1
        tt = min(t / T, 1.0)
        lead = np.argmin(F)
        L, fL = X[lead].copy(), F[lead]
        # FDB scores for companion selection (computed once per iteration)
        if use_fdb:
            dist = np.linalg.norm(X - L, axis=1)
            nF = (F - F.min()) / (F.max() - F.min() + 1e-50)
            nD = dist / (dist.max() + 1e-50)
            score = (1 - nF) + nD
            prob_sel = score / score.sum()
        # ---------------- attacking behavior ----------------
        n = 0.05 * np.exp(-2.0 * tt ** 2)
        for i in range(N):
            if not rec.budget_left():
                break
            r = rng.random()
            if p < r:
                nx = X[i] + n * (1 + np.sin(r)) * X[i]
            else:
                nx = X[i] * (1 + n * (2 * rng.random(D) - 1))
            nx = clipx(nx, prob)
            f = rec.eval(nx)
            if f < F[i]:
                X[i], F[i] = nx, f
        # ---------------- migration behavior ----------------
        for i in range(N):
            if not rec.budget_left():
                break
            r = rng.random()
            m = 2 * np.sin(r + np.pi / 2)
            if use_fdb:
                s = rng.choice(N, p=prob_sel)
            else:
                s = rng.integers(N)
            cau = np.tan((rng.random() - 0.5) * np.pi)
            if F[i] < F[s]:
                ref = X[s] if use_fdb else L
                scale = (1 - tt) if use_fdb else 1.0
                nx = X[i] + scale * cau * (X[i] - ref)
            else:
                nx = X[i] + cau * (L - m * X[i])
            nx = clipx(nx, prob)
            f = rec.eval(nx)
            if f < F[i]:
                X[i], F[i] = nx, f
        # ---------------- Cauchy-Gaussian hybrid leader mutation ----------------
        if use_cgm and rec.budget_left():
            lead = np.argmin(F)
            L, fL = X[lead].copy(), F[lead]
            lam1 = 1 - tt ** 2
            lam2 = tt ** 2
            cau = np.tan((rng.random(D) - 0.5) * np.pi)
            gau = rng.normal(0, 1, D)
            nx = clipx(L * (1 + lam1 * cau * 0.1 + lam2 * gau * 0.1), prob)
            f = rec.eval(nx)
            if f < fL:
                w = np.argmax(F)
                X[w], F[w] = nx, f
    return rec.finalize()


def bka(prob, max_fes, N, rng):
    return _bka_loop(prob, max_fes, N, rng)


def msbka(prob, max_fes, N, rng):
    return _bka_loop(prob, max_fes, N, rng, use_tcm=True, use_fdb=True, use_cgm=True)


def bka_s1(prob, max_fes, N, rng):   # TCM only
    return _bka_loop(prob, max_fes, N, rng, use_tcm=True)


def bka_s2(prob, max_fes, N, rng):   # FDB only
    return _bka_loop(prob, max_fes, N, rng, use_fdb=True)


def bka_s3(prob, max_fes, N, rng):   # CGM only
    return _bka_loop(prob, max_fes, N, rng, use_cgm=True)
