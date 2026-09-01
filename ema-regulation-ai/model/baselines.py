# -*- coding: utf-8 -*-
"""Baseline assessment models and the evaluation metrics.

Five comparison models are implemented on the same autodiff engine and
trained with the same optimiser, schedule and early-stopping rule as the
proposed architecture, so that differences in the reported numbers are
attributable to the model rather than to the training protocol:

*   a person-level penalised logistic regression on aggregated EMA
    features, representing the psychometric scoring practice that
    momentary assessment currently relies on;
*   a gated recurrent sequence encoder;
*   a single-head self-attentive sequence encoder;
*   a temporal graph encoder with mean pooling, i.e. the episode
    pathway of the proposed model without the ontology pathway and
    without concept-conditioned attention;
*   an attention-based diagnostic model with free concept embeddings,
    representing inherently interpretable diagnostic architectures.

Explanations for the two sequence encoders, which expose no attention
distribution, are obtained by integrated gradients along a straight path
from an all-zero baseline sequence.
"""
from __future__ import annotations

import numpy as np

from autodiff import Tensor, param, Adam, bce, cat
from dpapt import DPAPT, _shift_tensor

K_FAM = 5


# ---------------------------------------------------------------------------
class AggregateLogistic:
    """Penalised logistic regression on person-level aggregates."""

    name = "Aggregated logistic regression"

    def __init__(self, f_dim, seed=0, l2=1e-3):
        rng = np.random.default_rng(seed)
        self.l2 = l2
        self.W = param((2 * f_dim, K_FAM), scale=0.05, rng=rng)
        self.b = param((K_FAM,), zeros=True)
        self.params = [self.W, self.b]

    @staticmethod
    def features(X, M):
        m3 = M[:, :, None]
        n = M.sum(axis=1, keepdims=True) + 1e-9
        mean = (X * m3).sum(axis=1) / n
        var = ((X - mean[:, None, :]) ** 2 * m3).sum(axis=1) / n
        return np.concatenate([mean, np.sqrt(var)], axis=1)

    def forward(self, X, M):
        Z = Tensor(self.features(X, M))
        return (Z @ self.W + self.b).sigmoid(), None

    def loss(self, X, M, Y, lam=0.0, mu=0.0):
        pred, _ = self.forward(X, M)
        l = bce(pred, Y)
        reg = (self.W * self.W).sum() * self.l2
        return l + reg, l, Tensor(0.0), pred, None


# ---------------------------------------------------------------------------
class GRUSequence:
    """Gated recurrent encoder over the episode sequence."""

    name = "Gated recurrent encoder"

    def __init__(self, f_dim, d_model=32, seed=0):
        rng = np.random.default_rng(seed)
        self.d = d_model
        P = []

        def mk(shape, scale=None, zeros=False):
            t = param(shape, scale=scale, rng=rng, zeros=zeros)
            P.append(t)
            return t

        d = d_model
        self.Wi = mk((f_dim, d));  self.bi = mk((d,), zeros=True)
        self.Wz = mk((d, d));  self.Uz = mk((d, d))
        self.bz = mk((d,), zeros=True)
        self.Wr = mk((d, d));  self.Ur = mk((d, d))
        self.br = mk((d,), zeros=True)
        self.Wh = mk((d, d));  self.Uh = mk((d, d))
        self.bh = mk((d,), zeros=True)
        self.Wo = mk((d, K_FAM));  self.bo = mk((K_FAM,), zeros=True)
        self.params = P

    def encode(self, X, M):
        m3 = M[:, :, None]
        Xe = (Tensor(X) @ self.Wi + self.bi).tanh().masked_scale(m3)
        H = Xe
        for _ in range(2):
            prev = _shift_tensor(H, -1)
            z = (H @ self.Wz + prev @ self.Uz + self.bz).sigmoid()
            r = (H @ self.Wr + prev @ self.Ur + self.br).sigmoid()
            cand = ((r * H) @ self.Wh + prev @ self.Uh + self.bh).tanh()
            H = ((1.0 - z) * H + z * cand).masked_scale(m3)
        return H

    def forward(self, X, M):
        H = self.encode(X, M)
        n = M.sum(axis=1, keepdims=True) + 1e-9
        pooled = H.sum(axis=1) * (1.0 / n)
        return (pooled @ self.Wo + self.bo).sigmoid(), None

    def loss(self, X, M, Y, lam=0.0, mu=0.0):
        pred, _ = self.forward(X, M)
        l = bce(pred, Y)
        return l, l, Tensor(0.0), pred, None


# ---------------------------------------------------------------------------
class SelfAttentive:
    """Single-head self-attentive encoder with mean pooling."""

    name = "Self-attentive encoder"

    def __init__(self, f_dim, d_model=32, seed=0):
        rng = np.random.default_rng(seed)
        self.d = d_model
        P = []

        def mk(shape, scale=None, zeros=False):
            t = param(shape, scale=scale, rng=rng, zeros=zeros)
            P.append(t)
            return t

        d = d_model
        self.Wi = mk((f_dim, d));  self.bi = mk((d,), zeros=True)
        self.Wq = mk((d, d));  self.Wk = mk((d, d));  self.Wv = mk((d, d))
        self.W1 = mk((d, d));  self.b1 = mk((d,), zeros=True)
        self.Wo = mk((d, K_FAM));  self.bo = mk((K_FAM,), zeros=True)
        self.params = P

    def forward(self, X, M):
        m3 = M[:, :, None]
        H = (Tensor(X) @ self.Wi + self.bi).tanh().masked_scale(m3)
        Q, Kk, V = H @ self.Wq, H @ self.Wk, H @ self.Wv
        sc = (Q @ Kk.transpose(0, 2, 1)) * (1.0 / np.sqrt(self.d))
        mask2 = np.repeat(M[:, None, :], M.shape[1], axis=1)
        A = sc.softmax(axis=-1, mask=mask2)
        ctx = (A @ V).masked_scale(m3)
        H2 = ((ctx + H) @ self.W1 + self.b1).relu().masked_scale(m3)
        n = M.sum(axis=1, keepdims=True) + 1e-9
        pooled = H2.sum(axis=1) * (1.0 / n)
        return (pooled @ self.Wo + self.bo).sigmoid(), None

    def loss(self, X, M, Y, lam=0.0, mu=0.0):
        pred, _ = self.forward(X, M)
        l = bce(pred, Y)
        return l, l, Tensor(0.0), pred, None


# ---------------------------------------------------------------------------
class GraphPooled(DPAPT):
    """Temporal graph encoder with mean pooling (no ontology, no fusion)."""

    name = "Temporal graph encoder"

    def __init__(self, f_dim, d_model=32, seed=0):
        super().__init__(f_dim, d_model=d_model, layers=2,
                         use_onto=False, use_graph=True, use_attn=False,
                         seed=seed)


class AttnDiagnostic(DPAPT):
    """Attention-based diagnostic model with free concept embeddings."""

    name = "Attentive diagnostic model"

    def __init__(self, f_dim, d_model=32, seed=0):
        super().__init__(f_dim, d_model=d_model, layers=2,
                         use_onto=False, use_graph=False, use_attn=True,
                         seed=seed)


# ---------------------------------------------------------------------------
# metrics
# ---------------------------------------------------------------------------
def auc_roc(y, s):
    """Area under the receiver operating characteristic, by rank sum."""
    y = np.asarray(y, float)
    n1, n0 = y.sum(), (1 - y).sum()
    if n1 == 0 or n0 == 0:
        return np.nan
    order = np.argsort(s, kind="mergesort")
    ranks = np.empty(len(s), float)
    sorted_s = np.asarray(s)[order]
    i = 0
    r = np.arange(1, len(s) + 1, dtype=float)
    while i < len(s):
        j = i
        while j + 1 < len(s) and sorted_s[j + 1] == sorted_s[i]:
            j += 1
        ranks[order[i:j + 1]] = r[i:j + 1].mean()
        i = j + 1
    return float((ranks[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def auc_pr(y, s):
    """Average precision (area under the precision-recall curve)."""
    y = np.asarray(y, float)
    order = np.argsort(-np.asarray(s), kind="mergesort")
    y = y[order]
    tp = np.cumsum(y)
    prec = tp / np.arange(1, len(y) + 1)
    n1 = y.sum()
    if n1 == 0:
        return np.nan
    return float((prec * y).sum() / n1)


def macro_auc(Y, S):
    roc = [auc_roc(Y[:, k], S[:, k]) for k in range(Y.shape[1])]
    pr = [auc_pr(Y[:, k], S[:, k]) for k in range(Y.shape[1])]
    return float(np.nanmean(roc)), float(np.nanmean(pr)), roc, pr


# ---------------------------------------------------------------------------
def integrated_gradients(model, X, M, steps=16):
    """Per-episode attribution magnitude for models without attention.

    Returns an array of shape (B, K, T) holding, for each participant and
    strategy family, the attribution assigned to every episode.
    """
    B, T, F = X.shape
    out = np.zeros((B, K_FAM, T))
    for k in range(K_FAM):
        total = np.zeros((B, T, F))
        for s in range(1, steps + 1):
            a = s / steps
            Xi = Tensor(X * a, requires_grad=True)
            pred = _forward_from_tensor(model, Xi, M)
            pred[:, k].sum().backward()
            total += Xi.grad if Xi.grad is not None else 0.0
        attr = (total / steps) * X
        out[:, k, :] = np.abs(attr).sum(axis=-1) * M
    return out


def _forward_from_tensor(model, Xt, M):
    """Model forward that starts from an existing input tensor."""
    if isinstance(model, GRUSequence):
        m3 = M[:, :, None]
        H = (Xt @ model.Wi + model.bi).tanh().masked_scale(m3)
        for _ in range(2):
            prev = _shift_tensor(H, -1)
            z = (H @ model.Wz + prev @ model.Uz + model.bz).sigmoid()
            r = (H @ model.Wr + prev @ model.Ur + model.br).sigmoid()
            cand = ((r * H) @ model.Wh + prev @ model.Uh
                    + model.bh).tanh()
            H = ((1.0 - z) * H + z * cand).masked_scale(m3)
        n = M.sum(axis=1, keepdims=True) + 1e-9
        pooled = H.sum(axis=1) * (1.0 / n)
        return (pooled @ model.Wo + model.bo).sigmoid()
    if isinstance(model, SelfAttentive):
        m3 = M[:, :, None]
        H = (Xt @ model.Wi + model.bi).tanh().masked_scale(m3)
        Q, Kk, V = H @ model.Wq, H @ model.Wk, H @ model.Wv
        sc = (Q @ Kk.transpose(0, 2, 1)) * (1.0 / np.sqrt(model.d))
        mask2 = np.repeat(M[:, None, :], M.shape[1], axis=1)
        A = sc.softmax(axis=-1, mask=mask2)
        ctx = (A @ V).masked_scale(m3)
        H2 = ((ctx + H) @ model.W1 + model.b1).relu().masked_scale(m3)
        n = M.sum(axis=1, keepdims=True) + 1e-9
        pooled = H2.sum(axis=1) * (1.0 / n)
        return (pooled @ model.Wo + model.bo).sigmoid()
    raise TypeError("integrated gradients are only used for the two "
                    "sequence baselines")


# ---------------------------------------------------------------------------
def occlusion_scores(model, X, M, weights, topk, keep_only=False):
    """Predictions after removing (or keeping only) the top-k episodes.

    ``weights`` has shape (B, K, T). For each strategy family the k
    highest-weighted observed episodes are either masked out
    (comprehensiveness) or retained alone (sufficiency).
    """
    B, T, _ = X.shape
    out = np.zeros((B, K_FAM))
    for k in range(K_FAM):
        w = np.where(M > 0, weights[:, k, :], -np.inf)
        idx = np.argsort(-w, axis=1)[:, :topk]
        sel = np.zeros_like(M)
        np.put_along_axis(sel, idx, 1.0, axis=1)
        Mk = (sel * M) if keep_only else (M * (1.0 - sel))
        # a participant must retain at least one episode
        empty = Mk.sum(axis=1) == 0
        if empty.any():
            Mk[empty] = M[empty]
        pred, _ = model.forward(X * Mk[:, :, None], Mk)
        out[:, k] = pred.data[:, k]
    return out


def faithfulness(model, X, M, weights, topk=5):
    """Comprehensiveness and sufficiency of an explanation."""
    full, _ = model.forward(X, M)
    full = full.data
    without = occlusion_scores(model, X, M, weights, topk, keep_only=False)
    only = occlusion_scores(model, X, M, weights, topk, keep_only=True)
    comp = float(np.mean(np.abs(full - without)))
    suff = float(np.mean(np.abs(full - only)))
    return comp, suff


def justification_alignment(weights, used, M, topk=5):
    """Share of the top-k highlighted episodes in which the family that
    the explanation is justifying was the family actually deployed."""
    B, K, T = weights.shape
    hits, tot = 0.0, 0
    for k in range(K):
        w = np.where(M > 0, weights[:, k, :], -np.inf)
        idx = np.argsort(-w, axis=1)[:, :topk]
        picked = np.take_along_axis(used, idx, axis=1)
        hits += float((picked == k).sum())
        tot += picked.size
    return hits / tot


def chance_alignment(used, M):
    """Deployment share of each family, i.e. the alignment a random
    explanation would attain, averaged over families."""
    vals = [float(((used == k) & (M > 0)).sum() / max(1, (M > 0).sum()))
            for k in range(K_FAM)]
    return float(np.mean(vals))


def oracle_alignment(X, M, used, tr, te, topk=5, iters=600, lr=0.5,
                     l2=1e-4):
    """Upper bound on justification alignment.

    A multinomial logistic regression is fitted on the training
    episodes to predict which family was deployed from the momentary
    features alone, and its per-family probabilities are then used as an
    explanation. The resulting alignment is the best any episode-level
    evidence trail could achieve on this corpus given the features, and
    it bounds the measure from above as the marginal deployment rate
    bounds it from below.
    """
    Mb = M > 0
    xtr = X[tr][Mb[tr]]
    ytr = used[tr][Mb[tr]]
    xtr = np.hstack([xtr, np.ones((len(xtr), 1))])
    W = np.zeros((xtr.shape[1], K_FAM))
    Yoh = np.eye(K_FAM)[ytr]
    for _ in range(iters):
        z = xtr @ W
        z = z - z.max(axis=1, keepdims=True)
        p = np.exp(z)
        p /= p.sum(axis=1, keepdims=True)
        W -= lr * (xtr.T @ (p - Yoh) / len(xtr) + l2 * W)
    hits = tot = 0
    correct = n_ep = 0
    for i in te:
        m = Mb[i]
        xi = np.hstack([X[i][m], np.ones((int(m.sum()), 1))])
        z = xi @ W
        z = z - z.max(axis=1, keepdims=True)
        P = np.exp(z)
        P /= P.sum(axis=1, keepdims=True)
        ui = used[i][m]
        correct += int((P.argmax(axis=1) == ui).sum())
        n_ep += len(ui)
        for k in range(K_FAM):
            idx = np.argsort(-P[:, k])[:topk]
            hits += int((ui[idx] == k).sum())
            tot += len(idx)
    return float(hits / tot), float(correct / n_ep)
