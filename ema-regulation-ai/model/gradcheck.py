# -*- coding: utf-8 -*-
"""Central-difference verification of the autodiff engine.

Every operation used by the proposed architecture and by the baselines
is checked against numerical gradients; the script prints the maximum
relative deviation per test and fails loudly if any exceeds 1e-6.
"""
from __future__ import annotations

import numpy as np

from autodiff import Tensor, cat, stack, bce


def numeric_grad(fn, x, eps=1e-6):
    g = np.zeros_like(x.data)
    it = np.nditer(x.data, flags=["multi_index"])
    while not it.finished:
        i = it.multi_index
        old = x.data[i]
        x.data[i] = old + eps
        fp = fn().data.sum()
        x.data[i] = old - eps
        fm = fn().data.sum()
        x.data[i] = old
        g[i] = (fp - fm) / (2 * eps)
        it.iternext()
    return g


WORST = {"value": 0.0, "n": 0}


def check(name, fn, params):
    out = fn()
    out.backward()
    worst = 0.0
    for p in params:
        ana = np.zeros_like(p.data) if p.grad is None else p.grad
        num = numeric_grad(fn, p)
        denom = np.maximum(1.0, np.abs(ana) + np.abs(num))
        worst = max(worst, float(np.max(np.abs(ana - num) / denom)))
    status = "ok " if worst < 1e-6 else "FAIL"
    print("  %-28s max rel. deviation %.3e  %s" % (name, worst, status))
    WORST["value"] = max(WORST["value"], worst)
    WORST["n"] += 1
    return worst < 1e-6


def main():
    rng = np.random.default_rng(3)
    ok = True

    a = Tensor(rng.normal(size=(4, 3)), requires_grad=True)
    b = Tensor(rng.normal(size=(3, 5)), requires_grad=True)
    c = Tensor(rng.normal(size=(4, 5)), requires_grad=True)
    d = Tensor(rng.normal(size=(5,)), requires_grad=True)

    print("gradient checks")
    ok &= check("matmul + broadcast add", lambda: (a @ b + d), [a, b, d])
    ok &= check("mul, sub, div", lambda: (c * c - c) / (c * c + 3.0),
                [c])
    ok &= check("tanh", lambda: (a @ b).tanh(), [a, b])
    ok &= check("sigmoid", lambda: (a @ b).sigmoid(), [a, b])
    ok &= check("relu", lambda: (a @ b).relu(), [a, b])
    ok &= check("leaky_relu", lambda: (a @ b).leaky_relu(0.2), [a, b])
    ok &= check("exp / log", lambda: ((c * 0.1).exp() + 2.0).log(), [c])
    ok &= check("pow", lambda: (c + 3.0) ** 3, [c])
    ok &= check("sum(axis)", lambda: (a @ b).sum(axis=0), [a, b])
    ok &= check("mean(axis)", lambda: (a @ b).mean(axis=1), [a, b])
    ok &= check("max(axis)", lambda: (a @ b).max(axis=1), [a, b])
    ok &= check("softmax", lambda: (a @ b).softmax(axis=-1), [a, b])

    mask = (rng.random((4, 5)) > 0.3).astype(float)
    mask[:, 0] = 1.0
    ok &= check("masked softmax",
                lambda: (a @ b).softmax(axis=-1, mask=mask), [a, b])
    ok &= check("masked_scale", lambda: (a @ b).masked_scale(mask),
                [a, b])
    ok &= check("transpose", lambda: (a @ b).T @ c, [a, b, c])
    ok &= check("reshape", lambda: (a @ b).reshape(2, 10), [a, b])

    idx = np.array([0, 2, 2, 3, 1])
    ok &= check("gather_rows", lambda: a.gather_rows(idx) @ b, [a, b])
    ok &= check("getitem slice", lambda: (a @ b)[1:3], [a, b])
    ok &= check("cat", lambda: cat([a @ b, c], axis=1), [a, b, c])
    ok &= check("stack", lambda: stack([a @ b, c], axis=0), [a, b, c])

    tgt = (rng.random((4, 5)) > 0.5).astype(float)
    ok &= check("bce", lambda: bce((a @ b).sigmoid(), tgt), [a, b])

    # a gated recurrence, i.e. the update actually used by the encoder
    Wz = Tensor(rng.normal(size=(3, 3)) * 0.3, requires_grad=True)
    Wr = Tensor(rng.normal(size=(3, 3)) * 0.3, requires_grad=True)
    Wh = Tensor(rng.normal(size=(3, 3)) * 0.3, requires_grad=True)
    x0 = Tensor(rng.normal(size=(2, 3)), requires_grad=True)

    def gru():
        h = x0
        for _ in range(3):
            z = (h @ Wz).sigmoid()
            r = (h @ Wr).sigmoid()
            cand = ((r * h) @ Wh).tanh()
            h = (1.0 - z) * h + z * cand
        return h.sum()

    ok &= check("gated recurrence (3 steps)", gru, [Wz, Wr, Wh, x0])

    # attention entropy, i.e. the sparsity regulariser
    def ent():
        al = (a @ b).softmax(axis=-1)
        return (al * (al + 1e-8).log()).sum()

    ok &= check("attention entropy", ent, [a, b])

    print("ALL GRADIENT CHECKS PASSED" if ok else "SOME CHECKS FAILED")
    # the manuscript quotes the worst deviation, so it is recorded here
    # rather than restated by hand
    import json
    import os
    tab = os.path.abspath(os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "..", "tables"))
    os.makedirs(tab, exist_ok=True)
    with open(os.path.join(tab, "gradcheck.json"), "w",
              encoding="utf-8") as fh:
        json.dump(dict(n_checks=WORST["n"],
                       max_relative_deviation=WORST["value"],
                       all_passed=bool(ok)), fh, indent=1)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
