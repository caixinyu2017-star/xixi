# -*- coding: utf-8 -*-
"""The Dual-Pathway Affective Process Tracing (DP-APT) architecture.

Three components are composed:

*   a Temporal Affect Graph Network (TAGN) that encodes the momentary
    reports of one participant as a banded temporal graph with attentive
    message passing and a gated node update;
*   a Regulatory Process Ontology Parser (RPOP) that turns the process
    model of emotion regulation, expressed as a directed acyclic
    ontology over strategy families and their superordinate classes,
    into differentiable concept vectors by graph attention over
    interpretable node descriptors;
*   a cross-attention fusion module that queries the encoded episode
    sequence with each concept vector, producing one regulation score
    per strategy family. Every term of that score is a sum over
    episodes, so it decomposes exactly into per-episode contributions;
    that decomposition, not the attention distribution on its own, is
    the audit trail the model reports.

Ablated variants used in the ablation study are constructed through the
constructor flags rather than through separate classes, so that every
variant shares one code path.
"""
from __future__ import annotations

import numpy as np

from autodiff import Tensor, cat, stack, param, Adam, bce

# ---------------------------------------------------------------------------
# The regulatory process ontology.
#
# Ten nodes: the root, the two temporal classes of the process model, the
# two engagement classes, and the five strategy families. The five
# families are the leaves whose concept vectors query the episode
# sequence.
ONTO_NODES = ["Emotion regulation", "Antecedent-focused",
              "Response-focused", "Engagement", "Disengagement",
              "Situation selection", "Situation modification",
              "Attentional deployment", "Cognitive change",
              "Response modulation"]
LEAF = [5, 6, 7, 8, 9]

ONTO_EDGES = [(0, 1), (0, 2), (0, 3), (0, 4),
              (1, 5), (1, 6), (1, 7), (1, 8), (2, 9),
              (3, 6), (3, 8), (4, 5), (4, 7), (2, 9)]

# Interpretable descriptors of every ontology node. The columns are:
# position in the emotion-generative cycle (0 = before the situation
# unfolds, 1 = after the response is under way); degree of engagement
# with the situation; cognitive demand; behavioural visibility to
# others; breadth (1 for superordinate classes, 0 for families);
# antecedent-versus-response membership.
ONTO_DESC = np.array([
    #  cycle  engage  cogn.  visib.  breadth  antecedent
    [0.50,  0.50,  0.50,  0.50,  1.00,  0.50],   # root
    [0.20,  0.55,  0.55,  0.45,  0.70,  1.00],   # antecedent-focused
    [0.90,  0.35,  0.40,  0.70,  0.70,  0.00],   # response-focused
    [0.35,  0.95,  0.70,  0.55,  0.70,  0.75],   # engagement
    [0.30,  0.10,  0.35,  0.30,  0.70,  0.85],   # disengagement
    [0.05,  0.15,  0.30,  0.60,  0.00,  1.00],   # situation selection
    [0.25,  0.95,  0.60,  0.75,  0.00,  1.00],   # situation modification
    [0.45,  0.10,  0.35,  0.15,  0.00,  1.00],   # attentional deployment
    [0.60,  0.85,  0.95,  0.10,  0.00,  1.00],   # cognitive change
    [0.95,  0.30,  0.45,  0.85,  0.00,  0.00],   # response modulation
], dtype=float)
D_DESC = ONTO_DESC.shape[1]


def _onto_adj():
    """Symmetric adjacency of the ontology with self-loops."""
    n = len(ONTO_NODES)
    A = np.eye(n)
    for a, b in ONTO_EDGES:
        A[a, b] = 1.0
        A[b, a] = 1.0
    return A


# ---------------------------------------------------------------------------
class DPAPT:
    """Dual-Pathway Affective Process Tracing.

    Parameters
    ----------
    f_dim   : number of momentary features per episode
    d_model : width of the episode and concept representations
    layers  : number of TAGN propagation layers
    offsets : temporal neighbourhood of the banded episode graph
    use_onto: if False the concept vectors are free parameters (the
              variant without the ontology parser)
    use_graph: if False the episode encoder is a gated recurrence with no
              graph neighbourhood (the variant without the temporal graph)
    use_attn: if False the concept-conditioned attention is replaced by
              mean pooling (the variant without cross-attention fusion)
    """

    def __init__(self, f_dim, d_model=32, layers=2, offsets=(-3, -2, -1,
                                                             1, 2, 3),
                 use_onto=True, use_graph=True, use_attn=True, heads=4,
                 compete=True, anchor=(13, 14, 15, 16),
                 residual=True, seed=0):
        rng = np.random.default_rng(seed)
        self.d = d_model
        self.heads = heads
        self.dh = d_model // heads
        self.layers = layers
        self.offsets = tuple(offsets)
        self.use_onto = use_onto
        self.use_graph = use_graph
        self.use_attn = use_attn
        self.compete = compete
        self.residual = residual
        d = d_model
        P = []

        def mk(shape, scale=None, zeros=False):
            t = param(shape, scale=scale, rng=rng, zeros=zeros)
            P.append(t)
            return t

        # -- episode encoder -------------------------------------------
        self.W_in = mk((f_dim, d))
        self.b_in = mk((d,), zeros=True)
        self.W_msg, self.a_self, self.a_nbr = [], [], []
        self.Wz, self.Uz, self.bz = [], [], []
        self.Wr, self.Ur, self.br = [], [], []
        self.Wh, self.Uh, self.bh = [], [], []
        for _ in range(layers):
            self.W_msg.append(mk((d, d)))
            self.a_self.append(mk((d, 1), scale=0.3))
            self.a_nbr.append(mk((d, 1), scale=0.3))
            self.Wz.append(mk((d, d)));  self.Uz.append(mk((d, d)))
            self.bz.append(mk((d,), zeros=True))
            self.Wr.append(mk((d, d)));  self.Ur.append(mk((d, d)))
            self.br.append(mk((d,), zeros=True))
            self.Wh.append(mk((d, d)));  self.Uh.append(mk((d, d)))
            self.bh.append(mk((d,), zeros=True))

        # -- ontology parser -------------------------------------------
        if use_onto:
            self.A = _onto_adj()
            self.W_o1 = mk((D_DESC, d))
            self.W_o2 = mk((d, d))
            self.ao_s1 = mk((d, 1), scale=0.3)
            self.ao_n1 = mk((d, 1), scale=0.3)
            self.ao_s2 = mk((d, 1), scale=0.3)
            self.ao_n2 = mk((d, 1), scale=0.3)
        else:
            self.C_free = mk((len(LEAF), d), scale=0.5)

        # -- fusion and read-out ---------------------------------------
        # One bilinear form per attention head. Each head produces its
        # own distribution over episodes for every strategy family; the
        # score remains a linear read-out of a convex combination of
        # episode representations, so the attention weights retain their
        # status as the complete evidence trail behind the score.
        self.W_det = mk((d, d), scale=0.5)
        self.b_det = mk((len(LEAF),), zeros=True)
        # Anchoring head. Each family's concept vector is mapped to the
        # profile of momentary regulation items it should produce, and the
        # detector is asked to explain the observed items of an episode as
        # a mixture of those profiles. This uses observed self-reports
        # only; no episode-level label enters training.
        self.anchor = tuple(anchor)
        self.W_rec = mk((d, len(self.anchor)), scale=0.5)
        self.b_rec = mk((len(self.anchor),), zeros=True)
        self.V_val = [mk((d, self.dh), scale=0.5) for _ in range(heads)]
        self.Q_con = [mk((d, self.dh), scale=0.5) for _ in range(heads)]
        self.B_bil = [mk((d, self.dh), scale=0.5) for _ in range(heads)]
        self.W_pool = mk((d, d), scale=0.5)
        self.q_out = mk((len(LEAF), d), scale=0.5)
        self.w_out = mk((len(LEAF), d), scale=0.5)
        self.u_out = mk((len(LEAF),), scale=0.5)
        self.b_out = mk((len(LEAF),), zeros=True)
        self.params = P

    # -- ontology pathway ----------------------------------------------
    def concepts(self):
        if not self.use_onto:
            return self.C_free
        H = (Tensor(ONTO_DESC) @ self.W_o1).tanh()
        H = self._gat(H, self.ao_s1, self.ao_n1)
        H = (H @ self.W_o2).tanh()
        H = self._gat(H, self.ao_s2, self.ao_n2)
        return H.gather_rows(np.array(LEAF))

    def _gat(self, H, a_s, a_n):
        """One graph-attention layer over the ontology adjacency.

        The residual term matters here. Every strategy family is within
        two hops of every other through the superordinate classes, so
        two rounds of plain averaging drive the leaf representations
        together: without the skip connection the five concept vectors
        collapse onto one another and the detector can no longer tell
        the families apart. Keeping each node's own state lets the
        hierarchy inform a family's representation without erasing what
        distinguishes it.
        """
        es = H @ a_s                       # (N,1)
        en = H @ a_n                       # (N,1)
        e = (es + en.T).leaky_relu(0.2)    # (N,N) broadcast
        alpha = e.softmax(axis=-1, mask=self.A)
        return (((alpha @ H) + H) if self.residual
                else (alpha @ H)).tanh()

    # -- episode pathway -----------------------------------------------
    def encode(self, X, M):
        """Encode a batch of episode sequences.

        X : (B, T, F) standardised momentary features
        M : (B, T)    1.0 where a prompt was answered
        """
        B, T, _ = X.shape
        m3 = M[:, :, None]
        H = ((Tensor(X) @ self.W_in) + self.b_in).tanh().masked_scale(m3)

        for L in range(self.layers):
            if self.use_graph:
                Hm = H @ self.W_msg[L]
                es = Hm @ self.a_self[L]            # (B,T,1)
                en = Hm @ self.a_nbr[L]             # (B,T,1)
                terms, valid = [], []
                for off in self.offsets:
                    terms.append((es + _shift_tensor(en, off)))
                    valid.append(_shift(M, off) * M)
                logits = cat(terms, axis=-1).leaky_relu(0.2)   # (B,T,O)
                Vm = np.stack(valid, axis=-1)
                # an episode with no valid neighbour attends to itself
                lonely = (Vm.sum(axis=-1, keepdims=True) == 0)
                Vm = np.where(lonely, 1.0, Vm)
                alpha_n = logits.softmax(axis=-1, mask=Vm)
                agg = None
                for k, off in enumerate(self.offsets):
                    w = alpha_n[:, :, k:k + 1]
                    term = _shift_tensor(Hm, off) * w
                    agg = term if agg is None else agg + term
                self._last_nbr_attn = alpha_n.data
            else:
                agg = _shift_tensor(H @ self.W_msg[L], -1)

            z = ((H @ self.Wz[L]) + (agg @ self.Uz[L])
                 + self.bz[L]).sigmoid()
            r = ((H @ self.Wr[L]) + (agg @ self.Ur[L])
                 + self.br[L]).sigmoid()
            cand = ((r * H) @ self.Wh[L] + (agg @ self.Uh[L])
                    + self.bh[L]).tanh()
            H = ((1.0 - z) * H + z * cand).masked_scale(m3)
        return H

    # -- fusion ---------------------------------------------------------
    def forward(self, X, M):
        H = self.encode(X, M)                     # (B,T,D)
        C = self.concepts()                       # (K,D)
        K = len(LEAF)
        mask3 = np.repeat(M[:, None, :], K, axis=1)

        n_obs = M.sum(axis=1)[:, None] + 1e-9     # (B,1)

        # (a) episode-level strategy detector. For every episode the
        # model states how strongly each family is expressed in it. This
        # is the quantity a clinician inspects, and it is what the
        # attention distribution is derived from.
        det = ((H @ self.W_det) @ C.T).transpose(0, 2, 1) * (
            1.0 / np.sqrt(self.d))                # (B,K,T)
        det = det + self.b_det.reshape(1, len(LEAF), 1)
        if self.compete:
            # The process model treats the five families as alternative
            # interventions at a given point in the emotion-generative
            # cycle, so within an episode they compete: the detector is
            # normalised across families rather than scored independently.
            # This makes the prevalence channel below an estimate of the
            # share of episodes attributed to each family, which is the
            # quantity the assessment target is partly defined on.
            p_ep = det.softmax(axis=1).masked_scale(mask3)
        else:
            p_ep = det.sigmoid().masked_scale(mask3)

        # (b) prevalence-weighted evidence pool. Attention is
        # normalised over episodes and therefore cannot carry how often
        # a family is expressed, yet habitual frequency is part of what
        # the assessment target means. This channel averages the
        # detector-weighted episode representations over the whole
        # protocol, so it grows with both the frequency and the
        # character of the episodes in which the family appears. It
        # remains an average of per-episode terms, so the evidence
        # trail stays decomposable.
        # reconstruction of the observed regulation items from the
        # detector, retained for the anchoring term of the objective
        proto = (C @ self.W_rec) + self.b_rec     # (K,R)
        self._p_ep = p_ep
        self._recon = p_ep.transpose(0, 2, 1) @ proto      # (B,T,R)
        self._recon_target = X[:, :, self.anchor]
        self._recon_mask = np.repeat(M[:, :, None], len(self.anchor),
                                     axis=2)

        vpool = H @ self.W_pool                   # (B,T,D)
        pool = (p_ep @ vpool) * (1.0 / n_obs)[:, :, None]   # (B,K,D)
        g = p_ep.sum(axis=-1) / n_obs             # (B,K)

        # (c) concept-conditioned attention over episodes, one
        # distribution per head, biased by the detector so that the
        # heads read the episodes in which the family is expressed.
        ctxs, alphas = [], []
        for h in range(self.heads):
            key = H @ self.B_bil[h]               # (B,T,dh)
            qry = C @ self.Q_con[h]               # (K,dh)
            val = H @ self.V_val[h]               # (B,T,dh)
            scores = (key @ qry.T).transpose(0, 2, 1) * (
                1.0 / np.sqrt(self.dh)) + det     # (B,K,T)
            if self.use_attn:
                a = scores.softmax(axis=-1, mask=mask3)
            else:
                unif = mask3 / (mask3.sum(axis=-1, keepdims=True) + 1e-12)
                a = Tensor(unif) + scores.masked_scale(
                    np.zeros_like(mask3))
            alphas.append(a)
            ctxs.append(a @ val)                  # (B,K,dh)
        ctx = cat(ctxs, axis=-1)                  # (B,K,D)
        logit = ((ctx * self.w_out).sum(axis=-1)
                 + (pool * self.q_out).sum(axis=-1)
                 + g * self.u_out + self.b_out)
        # the reported audit trail averages the heads
        alpha = alphas[0]
        for a in alphas[1:]:
            alpha = alpha + a
        alpha = alpha * (1.0 / self.heads)
        self._head_alphas = alphas

        # Exact per-episode decomposition of the score. Every term of the
        # logit is a sum over episodes, so the contribution of episode t
        # to the score of family k can be written down in closed form and
        # summing it over t recovers the logit up to the bias. This
        # decomposition, not the attention distribution alone, is the
        # evidence trail the model reports.
        dh, inv_n = self.dh, (1.0 / n_obs)            # (B,1)
        contrib = np.zeros((X.shape[0], K, X.shape[1]))
        for h, a in enumerate(alphas):
            wh = self.w_out.data[:, h * dh:(h + 1) * dh]      # (K,dh)
            vh = (H.data @ self.V_val[h].data)               # (B,T,dh)
            contrib += a.data * (vh @ wh.T).transpose(0, 2, 1)
        contrib += (p_ep.data
                    * (vpool.data @ self.q_out.data.T).transpose(0, 2, 1)
                    * inv_n[:, :, None])
        contrib += (p_ep.data * self.u_out.data[None, :, None]
                    * inv_n[:, :, None])
        self._contrib = contrib * mask3
        return logit.sigmoid(), alpha

    def contributions(self, X, M):
        """Per-episode contributions to each family score (B,K,T)."""
        self.forward(X, M)
        return self._contrib

    # -- objective ------------------------------------------------------
    def loss(self, X, M, Y, lam=0.05, mu=1.0):
        pred, alpha = self.forward(X, M)
        l_task = bce(pred, Y)
        ent = None
        for a in self._head_alphas:
            e = -(a * (a + 1e-8).log()).sum(axis=-1).mean()
            ent = e if ent is None else ent + e
        ent = ent * (1.0 / self.heads)
        d = self._recon + Tensor(-self._recon_target)
        rec = (d * d).masked_scale(self._recon_mask).sum() * (
            1.0 / max(1.0, float(self._recon_mask.sum())))
        return l_task + lam * ent + mu * rec, l_task, ent, pred, alpha


def _shift(arr, off):
    """Shift an array along axis 1 by ``off`` steps, zero-filling."""
    out = np.zeros_like(arr)
    if off < 0:
        out[:, -off:] = arr[:, :off]
    elif off > 0:
        out[:, :-off] = arr[:, off:]
    else:
        out[:] = arr
    return out


def _shift_tensor(t, off):
    """Differentiable version of ``_shift`` on a (B,T,D) tensor."""
    data = _shift(t.data, off)
    out = Tensor(data, _parents=(t,))

    def bw(g):
        return (_shift(g, -off),)
    out._backward = bw
    return out


# ---------------------------------------------------------------------------
def train(model, data, tr, va, epochs=80, batch=48, lr=4e-3, lam=0.05,
          seed=0, verbose=True, patience=20, warmup=15, mu=None):
    """Train with Adam and early stopping on the validation objective.

    The sparsity weight is held at zero for ``warmup`` epochs and then
    ramped linearly to its target over the same number of epochs. Without
    that schedule the entropy penalty shapes the attention before the
    episode encoder carries any signal, and the model settles into a
    peaked but uninformative attention pattern.

    Model selection uses the validation value of the full objective at
    the target sparsity weight, and only considers epochs at which the
    ramp has completed. Selecting on cross-entropy alone, or over the
    warm-up epochs, would return a checkpoint taken before the sparsity
    term was ever applied, which makes the trained model independent of
    the weight that is supposed to control it.
    """
    X, M, Y = data["X"], data["mask"].astype(float), data["Y"]
    opt = Adam(model.params, lr=lr)
    rng = np.random.default_rng(seed)
    ramp_end = 0 if (warmup <= 0 or lam == 0.0) else 2 * warmup - 1
    best, best_state, bad, hist = np.inf, None, 0, []
    for ep in range(epochs):
        if warmup <= 0:
            lam_ep = lam
        elif ep < warmup:
            lam_ep = 0.0
        else:
            lam_ep = lam * min(1.0, (ep - warmup + 1) / float(warmup))
        order = rng.permutation(tr)
        for s in range(0, len(order), batch):
            idx = order[s:s + batch]
            opt.zero_grad()
            kw = {} if mu is None else {"mu": mu}
            total, lt, ent, _, _ = model.loss(X[idx], M[idx], Y[idx],
                                              lam=lam_ep, **kw)
            total.backward()
            opt.step()
        kw = {} if mu is None else {"mu": mu}
        _, lv, ev, pv, _ = model.loss(X[va], M[va], Y[va],
                                      lam=lam_ep, **kw)
        v = float(lv.data) + lam * float(ev.data)
        hist.append(v)
        if verbose and (ep % 10 == 0 or ep == epochs - 1):
            print("    epoch %3d  val BCE %.4f  attn entropy %.3f"
                  % (ep, float(lv.data), float(ev.data)))
        if ep < ramp_end:
            continue
        if v < best - 1e-4:
            best, bad = v, 0
            best_state = [p.data.copy() for p in model.params]
        else:
            bad += 1
            if bad >= patience:
                break
    if best_state is not None:
        for p, w in zip(model.params, best_state):
            p.data = w
    return dict(best_val=best, epochs_run=len(hist))
