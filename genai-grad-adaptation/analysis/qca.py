# -*- coding: utf-8 -*-
"""Fuzzy-set qualitative comparative analysis, from first principles.

Direct-method calibration through the logistic transform of Ragin (2008);
necessity and sufficiency consistency and coverage; the truth table with
frequency, raw-consistency and PRI thresholds; and Quine-McCluskey
minimization for the complex, parsimonious and intermediate solutions, the
intermediate solution admitting only the remainders that agree with the
stated directional expectations (the "easy counterfactuals" of the standard
analysis). Core conditions are those that survive into the parsimonious
solution, following Fiss (2011).
"""
from __future__ import annotations

import itertools

import numpy as np


# --------------------------------------------------------------- calibration
def calibrate(x, full, cross, out):
    """Direct method: anchors for full membership (0.95), the crossover
    (0.50) and full non-membership (0.05)."""
    x = np.asarray(x, dtype=float)
    up = 3.0 / (full - cross)
    dn = 3.0 / (cross - out)
    z = np.where(x >= cross, (x - cross) * up, (x - cross) * dn)
    m = 1.0 / (1.0 + np.exp(-z))
    return np.where(np.abs(m - 0.5) < 1e-9, 0.501, m)


# ------------------------------------------------------- set-theoretic sizes
def consistency(x, y):
    return float(np.minimum(x, y).sum() / x.sum())


def coverage(x, y):
    return float(np.minimum(x, y).sum() / y.sum())


def pri(x, y):
    """Proportional reduction in inconsistency."""
    a = np.minimum(x, y).sum()
    b = np.minimum.reduce([x, y, 1 - y]).sum()
    return float((a - b) / (x.sum() - b))


# --------------------------------------------------------------- truth table
def truth_table(M, y, freq_min=10, cons_min=0.80, pri_min=0.70):
    """M: (n, k) membership matrix. Returns one row per corner with its best
    membership count, consistency, PRI and outcome decision."""
    n, k = M.shape
    rows = []
    for bits in itertools.product((0, 1), repeat=k):
        mem = np.ones(n)
        for j, b in enumerate(bits):
            mem = np.minimum(mem, M[:, j] if b else 1 - M[:, j])
        nc = int((mem > 0.5).sum())
        cons = consistency(mem, y) if mem.sum() > 0 else 0.0
        p = pri(mem, y) if mem.sum() > 0 else 0.0
        keep = nc >= freq_min
        rows.append(dict(bits=bits, n=nc, cons=cons, pri=p,
                         outcome=1 if (keep and cons >= cons_min
                                       and p >= pri_min) else
                         (0 if keep else -1)))     # -1 = remainder
    return rows


# ----------------------------------------------------------- Quine-McCluskey
def _combine(a, b):
    diff = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
    if len(diff) == 1 and "-" not in (a[diff[0]], b[diff[0]]):
        c = list(a)
        c[diff[0]] = "-"
        return tuple(c)
    return None


def quine_mccluskey(ones, dontcares=()):
    """Prime implicants covering ``ones``, allowed to absorb ``dontcares``."""
    terms = {tuple(str(b) for b in t) for t in ones} | \
            {tuple(str(b) for b in t) for t in dontcares}
    primes = set()
    while terms:
        used, nxt = set(), set()
        tl = sorted(terms)
        for a, b in itertools.combinations(tl, 2):
            c = _combine(a, b)
            if c is not None:
                nxt.add(c)
                used.add(a)
                used.add(b)
        primes |= (terms - used)
        terms = nxt
    # essential cover of the ones by iterative dominance
    ones_t = [tuple(str(b) for b in t) for t in ones]

    def covers(p, t):
        return all(pp in ("-", tt) for pp, tt in zip(p, t))

    chart = {t: [p for p in primes if covers(p, t)] for t in ones_t}
    cover = []
    left = set(ones_t)
    while left:
        # essential first
        ess = None
        for t in sorted(left):
            cs = [p for p in chart[t] if p in primes]
            if len(cs) == 1:
                ess = cs[0]
                break
        if ess is None:
            # greedy: the prime covering most uncovered terms
            ess = max(sorted(primes),
                      key=lambda p: sum(1 for t in left if covers(p, t)))
        cover.append(ess)
        left = {t for t in left if not covers(ess, t)}
        primes.discard(ess)
    return sorted(set(cover))


def solution(rows, names, y, M, which="intermediate", expectations=None):
    """Minimize the truth table.

    complex: positive rows only. parsimonious: remainders are don't-cares.
    intermediate: only remainders that agree with the directional
    expectations (dict name -> 1, 0 or None) are admitted.
    """
    ones = [r["bits"] for r in rows if r["outcome"] == 1]
    rem = [r["bits"] for r in rows if r["outcome"] == -1]
    if which == "complex":
        dc = []
    elif which == "parsimonious":
        dc = rem
    else:
        exp = expectations or {}
        dc = []
        for bits in rem:
            ok = True
            for j, nm in enumerate(names):
                e = exp.get(nm)
                if e is not None and bits[j] != e:
                    ok = False
                    break
            if ok:
                dc.append(bits)
    if not ones:
        return []
    implicants = quine_mccluskey(ones, dc)
    out = []
    for imp in implicants:
        mem = np.ones(M.shape[0])
        label = []
        for j, ch in enumerate(imp):
            if ch == "-":
                continue
            mem = np.minimum(mem, M[:, j] if ch == "1" else 1 - M[:, j])
            label.append((names[j], int(ch)))
        out.append(dict(term=label, cons=consistency(mem, y),
                        rawcov=coverage(mem, y), mem=mem, imp=imp))
    # unique coverage: min-share not covered by the other terms
    for i, t in enumerate(out):
        others = [o["mem"] for j, o in enumerate(out) if j != i]
        rest = np.maximum.reduce(others) if others else np.zeros_like(t["mem"])
        t["uniqcov"] = float((np.minimum(t["mem"], y).sum()
                              - np.minimum(np.minimum(rest, t["mem"]),
                                           y).sum()) / y.sum())
    sol_mem = np.maximum.reduce([t["mem"] for t in out])
    overall = dict(cons=consistency(sol_mem, y), cov=coverage(sol_mem, y))
    return out, overall
