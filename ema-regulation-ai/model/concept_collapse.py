# -*- coding: utf-8 -*-
"""Diagnostic: does the ontology parser collapse its concept vectors?

Every strategy family lies within two hops of every other through the
superordinate classes, so repeated neighbourhood averaging over the
ontology drives the leaf representations together. This script measures
the collapse directly, by training the proposed model with and without
the residual term in the ontology graph-attention layer and recording
the cosine similarity between the five learned concept vectors. The
figures it writes are quoted in the description of the parser.
"""
from __future__ import annotations

import json
import os

import numpy as np

import ema_data as D
from dpapt import DPAPT, train

HERE = os.path.dirname(os.path.abspath(__file__))
TAB = os.path.abspath(os.path.join(HERE, "..", "tables"))
SEEDS = (0, 1, 2)


def collapse(C):
    Cn = C / (np.linalg.norm(C, axis=1, keepdims=True) + 1e-12)
    S = np.abs(Cn @ Cn.T)
    off = S[~np.eye(S.shape[0], dtype=bool)]
    return float(off.mean()), float(off.max())


def main():
    data = D.generate()
    tr, va, te = D.splits()
    out = {}
    for label, res in (("with residual", True), ("without residual", False)):
        means, maxes = [], []
        for seed in SEEDS:
            m = DPAPT(D.F_DIM, d_model=32, layers=2, use_attn=False,
                      residual=res, seed=seed)
            train(m, data, tr, va, epochs=90, batch=48, lr=4e-3, lam=0.0,
                  seed=seed, verbose=False, patience=20, warmup=0)
            mu, mx = collapse(m.concepts().data)
            means.append(mu)
            maxes.append(mx)
        out[label] = dict(mean_abs_cosine=float(np.mean(means)),
                          max_abs_cosine=float(np.mean(maxes)))
        print("  %-18s mean |cos| %.3f  max |cos| %.3f"
              % (label, out[label]["mean_abs_cosine"],
                 out[label]["max_abs_cosine"]), flush=True)
    path = os.path.join(TAB, "concept_collapse.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    print("written to", path)


if __name__ == "__main__":
    main()
