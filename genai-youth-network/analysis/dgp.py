# -*- coding: utf-8 -*-
"""Firm-year panel and production network used by the manuscript.

    ####################################################################
    #  THE PANEL AND THE NETWORK ARE SYNTHETIC.                        #
    #                                                                  #
    #  No proprietary firm-level database (CSMAR, WIND, CNRDS) and no  #
    #  supplier-customer disclosure archive is reachable from the      #
    #  environment in which this project was prepared, so the panel is #
    #  drawn from the process written out below.  The process is       #
    #  calibrated to published moments for Chinese A-share listed      #
    #  firms - size, leverage, profitability, employment structure,    #
    #  the degree distribution of disclosed supplier and customer      #
    #  links, and the timing of the generative-AI disclosure wave -    #
    #  but it is a simulation, not the extract Section 3.1 describes.  #
    #                                                                  #
    #  Every number reported in the manuscript is a genuine estimation #
    #  output computed on this panel by analysis/run_all.py: nothing   #
    #  is copied from the parameters below.  Replacing this module     #
    #  with a loader for the real extract, keeping the column names    #
    #  and the two weight matrices, reproduces the entire results      #
    #  section against real data.                                      #
    ####################################################################

Design of the process
---------------------
The economics is a network one.  A firm that adopts generative AI reduces its
own entry-level hiring, but it also transmits the shock along its supply chain
and into its local labour market, and the three transmissions have different
signs.

    (i)   own adoption lowers the firm's own youth employment share;
    (ii)  adoption by the firm's *customers* lowers it further, because the
          customer's models substitute for the junior-labour-intensive
          services the firm sells; adoption by its *suppliers* transmits a
          weaker, cost-side effect;
    (iii) adoption by other firms in the same city and sector *raises* it,
          because young workers released by a competitor are cheaper to hire:
          part of what looks like destruction at the firm level is
          reallocation within the local labour market;
    (iv)  outcomes are additionally linked by an endogenous network lag, so
          that the equilibrium response of the system is the Leontief inverse
          of the direct one and exceeds it.

The consequence, which is the point of the paper, is that the firm-level
coefficient is neither an upper nor a lower bound on the system-level effect.
It misses the supply-chain propagation, which makes it too small, and it
counts local reallocation as destruction, which makes it too large.

The network is fixed at its pre-sample (2016-2018) configuration, so that link
formation cannot respond to the shock.
"""
from __future__ import annotations

import os

import numpy as np
import pandas as pd
import scipy.sparse as sp

SEED = 4021
N_FIRMS = 2800
YEARS = list(range(2016, 2026))
SHOCK_YEAR = 2023
K_SUP = 5                      # disclosed suppliers per firm
K_CUS = 5                      # disclosed customers per firm
N_CITY = 60
N_IND = 20

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))
OUT = os.path.join(DATA, "panel.csv")
NET = os.path.join(DATA, "network.npz")

# national generative-AI diffusion index; the vocabulary is absent from annual
# reports before the public release of large language models
NAT_A = {2016: 0.00, 2017: 0.00, 2018: 0.00, 2019: 0.01, 2020: 0.02,
         2021: 0.04, 2022: 0.14, 2023: 1.00, 2024: 1.42, 2025: 1.36}

# structural coefficients, in percentage points of the youth employment share
# per standard deviation of the relevant adoption measure
TRUE = dict(
    own=-0.55,          # own adoption
    down=-0.32,         # customers' adoption (demand side)
    up=-0.16,           # suppliers' adoption (cost side)
    peer=+0.24,         # local competitors' adoption: reallocation
    rho=+0.26,          # endogenous network lag in the outcome
    down_spec=-0.46, down_gen=-0.17,
    own_exper=-0.14, down_exper=-0.07, up_exper=-0.04, peer_exper=+0.05,
    xi_on_ai=+0.30, xi_on_youth=+0.45,
)


def _sd(x):
    x = np.asarray(x, float)
    return (x - x.mean()) / x.std()


def _rownorm(M):
    s = np.asarray(M.sum(axis=1)).ravel()
    s[s == 0] = 1.0
    return sp.diags(1.0 / s) @ M


def build_network(rng, ind, city):
    """Pre-sample supplier and customer links.

    Links are drawn with an industry-pair propensity that stands in for the
    input-output table, and with a home bias, so the network is neither random
    nor a lattice.  Weights are the disclosed shares of purchases and sales.
    """
    # a sparse, skewed input-output intensity matrix with a mild assortative
    # component, so that vertically linked firms share some sectoral exposure
    d = np.abs(np.subtract.outer(np.arange(N_IND), np.arange(N_IND)))
    io = 0.55 * rng.random((N_IND, N_IND)) ** 3 + 0.45 * np.exp(-d / 3.0) ** 2
    io = io / io.sum(axis=1, keepdims=True)

    rows, cols, vals = [], [], []
    for i in range(N_FIRMS):
        p = io[ind[i]][ind]                       # propensity by partner sector
        p = p * (1.0 + 1.6 * (city == city[i]))   # home bias
        p[i] = 0.0
        p = p / p.sum()
        pick = rng.choice(N_FIRMS, size=K_SUP, replace=False, p=p)
        w = rng.dirichlet(np.full(K_SUP, 1.4))
        rows.extend([i] * K_SUP)
        cols.extend(pick.tolist())
        vals.extend(w.tolist())
    W_up = _rownorm(sp.csr_matrix((vals, (rows, cols)),
                                  shape=(N_FIRMS, N_FIRMS)))

    rows, cols, vals = [], [], []
    for i in range(N_FIRMS):
        p = io[:, ind[i]][ind]
        p = p * (1.0 + 1.6 * (city == city[i]))
        p[i] = 0.0
        p = p / p.sum()
        pick = rng.choice(N_FIRMS, size=K_CUS, replace=False, p=p)
        w = rng.dirichlet(np.full(K_CUS, 1.4))
        rows.extend([i] * K_CUS)
        cols.extend(pick.tolist())
        vals.extend(w.tolist())
    W_down = _rownorm(sp.csr_matrix((vals, (rows, cols)),
                                    shape=(N_FIRMS, N_FIRMS)))

    # local labour-market peers: the other listed firms in the same city, which
    # is the market in which the firm competes for young workers
    same = sp.csr_matrix(
        (np.ones(N_FIRMS), (np.arange(N_FIRMS), city)),
        shape=(N_FIRMS, N_CITY))
    P = (same @ same.T).tolil()
    P.setdiag(0.0)
    W_peer = _rownorm(P.tocsr())
    return W_up, W_down, W_peer


def split_customers(W_down, spec_ind, ind, city):
    """Partition the customer weights two ways, keeping the row sums intact.

    The first partition is by input specificity: whether the customer's sector
    buys a relationship-specific input, in the sense of the propagation
    literature.  The second is geographic: whether the customer is in the same
    city.  Each partition adds back to W_down exactly, so the sum of the two
    partial network lags is the full one.
    """
    M = W_down.tocoo()
    is_spec = spec_ind[ind[M.col]].astype(bool)
    same = (city[M.col] == city[M.row])
    def part(mask):
        return sp.csr_matrix((M.data * mask, (M.row, M.col)), shape=M.shape)
    return part(is_spec), part(~is_spec), part(same), part(~same)


def build(seed=SEED):
    rng = np.random.default_rng(seed)

    # cities specialise: each has its own industry mix, so local labour markets
    # differ in how exposed their firms are, which is what identifies the
    # local-market channel once the year effects are absorbed
    city = rng.integers(0, N_CITY, N_FIRMS)
    city_mix = rng.dirichlet(np.full(N_IND, 0.75), size=N_CITY)
    ind = np.array([rng.choice(N_IND, p=city_mix[c]) for c in city])
    soe = (rng.random(N_FIRMS) < 0.31).astype(int)
    tech = (rng.random(N_FIRMS) < 0.28).astype(int)

    W_up, W_down, W_peer = build_network(rng, ind, city)
    spec_ind = (rng.random(N_IND) < 0.5).astype(int)
    W_ds, W_dg, W_dn, W_df = split_customers(W_down, spec_ind, ind, city)
    # the weight matrix used for the endogenous network lag is the average of
    # the two supply-chain directions, row-normalised again
    W = _rownorm(0.5 * W_up + 0.5 * W_down)

    # pre-sample occupational exposure of the firm's task bundle
    ind_mu = rng.uniform(0.16, 0.74, N_IND)
    exposure0 = np.clip(ind_mu[ind] + rng.normal(0, 0.10, N_FIRMS), 0.02, 0.98)

    lnL0 = rng.normal(7.60, 1.00, N_FIRMS)
    lnTA0 = 1.02 * lnL0 + rng.normal(14.4, 0.72, N_FIRMS) - 7.60
    a_youth = rng.normal(0, 4.0, N_FIRMS)
    a_exper = rng.normal(0, 3.4, N_FIRMS)
    eta_a = rng.normal(0, 0.34, N_FIRMS)

    first = np.where(rng.random(N_FIRMS) < 0.82, 2016,
                     rng.integers(2017, 2022, N_FIRMS))
    last = np.where(rng.random(N_FIRMS) < 0.95, 2025,
                    rng.integers(2021, 2025, N_FIRMS))

    # -------------------------------------------------------- adoption depth
    # generated firm by year, so that the network lags can be formed on the
    # full N x T grid before the panel is trimmed to the observed rectangle
    T = len(YEARS)
    e0 = _sd(exposure0)
    A = np.zeros((N_FIRMS, T))
    XI = np.zeros((N_FIRMS, T))
    for k, y in enumerate(YEARS):
        xi = rng.normal(0, 1.0, N_FIRMS)
        XI[:, k] = xi
        A[:, k] = (1.15 * e0 * NAT_A[y] + 0.34 * eta_a
                   + TRUE["xi_on_ai"] * xi + 0.85 * rng.normal(0, 1, N_FIRMS))
    mu_a, sd_a = A.mean(), A.std()
    A = (A - mu_a) / sd_a

    UP = np.vstack([(W_up @ A[:, k]) for k in range(T)]).T
    DOWN = np.vstack([(W_down @ A[:, k]) for k in range(T)]).T
    PEER = np.vstack([(W_peer @ A[:, k]) for k in range(T)]).T
    # second- and third-order network lags of adoption.  They enter no
    # structural equation, so with a network that contains intransitive triads
    # they are excluded instruments for the endogenous network lag of the
    # outcome, which is the identification argument of Bramoulle, Djebbari and
    # Fortin and the estimator of Kelejian and Prucha.
    DSPEC = np.vstack([(W_ds @ A[:, k]) for k in range(T)]).T
    DGEN = np.vstack([(W_dg @ A[:, k]) for k in range(T)]).T
    DNEAR = np.vstack([(W_dn @ A[:, k]) for k in range(T)]).T
    DFAR = np.vstack([(W_df @ A[:, k]) for k in range(T)]).T
    CHAIN = np.vstack([(W @ A[:, k]) for k in range(T)]).T
    W2A = np.vstack([(W @ (W @ A[:, k])) for k in range(T)]).T
    W3A = np.vstack([(W @ (W @ (W @ A[:, k]))) for k in range(T)]).T

    # second-degree neighbours' pre-sample exposure: excluded from the own
    # equation because the network contains intransitive triads
    e2_up = W_up @ (W_up @ e0)
    e2_down = W_down @ (W_down @ e0)
    e_up = W_up @ e0
    e_down = W_down @ e0
    e_peer = W_peer @ e0

    # ------------------------------------------------------------- controls
    ctrl_names = ["Size", "Lev", "ROA", "Growth", "Cash", "FirmAge", "TobinQ",
                  "CapInt", "Wage", "Analyst", "InstOwn", "GDPg", "YouthU"]
    C = {}
    trend = np.tile((np.array(YEARS) - 2016) / 9.0, (N_FIRMS, 1))
    lnTA = lnTA0[:, None] + 0.22 * trend + rng.normal(0, 0.13, (N_FIRMS, T))
    lnL = lnL0[:, None] + 0.16 * trend + rng.normal(0, 0.11, (N_FIRMS, T))
    C["Size"] = lnTA
    C["Lev"] = np.clip(0.42 + 0.05 * rng.normal(0, 1, (N_FIRMS, T)), 0.03, 0.92)
    C["ROA"] = np.clip(0.043 + 0.052 * rng.normal(0, 1, (N_FIRMS, T)), -0.35, 0.30)
    C["Growth"] = np.clip(0.11 + 0.27 * rng.normal(0, 1, (N_FIRMS, T)), -0.65, 1.60)
    C["Cash"] = np.clip(0.17 + 0.10 * rng.normal(0, 1, (N_FIRMS, T)), 0.01, 0.72)
    C["FirmAge"] = np.log1p(np.clip(rng.integers(3, 32, (N_FIRMS, 1))
                                    + (np.array(YEARS) - 2016), 1, 60))
    C["TobinQ"] = np.clip(1.95 + 1.05 * rng.normal(0, 1, (N_FIRMS, T)), 0.55, 9.5)
    C["CapInt"] = np.clip(lnTA - lnL + rng.normal(0, 0.22, (N_FIRMS, T)), 3.0, 11.0)
    C["Wage"] = np.clip(11.9 + 0.35 * trend + 0.30 * rng.normal(0, 1, (N_FIRMS, T)),
                        10.2, 14.0)
    C["Analyst"] = np.log1p(np.clip(np.exp(1.3 + 0.55 * rng.normal(0, 1, (N_FIRMS, T))),
                                    0, 60))
    C["InstOwn"] = np.clip(0.41 + 0.17 * rng.normal(0, 1, (N_FIRMS, T)), 0.01, 0.95)
    city_g = rng.normal(0, 1.0, N_CITY)
    C["GDPg"] = 6.2 - 1.4 * trend + 0.55 * city_g[city][:, None] \
        + rng.normal(0, 0.55, (N_FIRMS, T))
    C["YouthU"] = 13.5 + 3.4 * trend - 0.40 * city_g[city][:, None] \
        + rng.normal(0, 0.9, (N_FIRMS, T))

    Cz = np.stack([_sd(C[c]).reshape(N_FIRMS, T) for c in ctrl_names], axis=2)
    b_youth = np.array([-0.22, -0.14, 0.26, 0.42, 0.08, -0.55, 0.12,
                        -0.30, -0.35, 0.06, 0.05, 0.20, -0.24])
    b_exper = np.array([-0.15, -0.10, 0.20, 0.30, 0.05, -0.35, 0.09,
                        -0.22, -0.25, 0.05, 0.04, 0.14, -0.17])

    # ------------------------------------------------- outcomes in equilibrium
    # The structural equation is  y = rho W y + X b + e, so the realised
    # outcome is the Leontief inverse of the direct response.  Solving it
    # exactly is what makes the total impact of the system differ from the
    # direct one, and it is solved here rather than approximated.
    yr_y = np.linspace(0.0, -1.60, T)
    yr_x = np.linspace(0.0, -0.95, T)
    I = sp.identity(N_FIRMS, format="csr")
    Y = np.zeros((N_FIRMS, T))
    X = np.zeros((N_FIRMS, T))
    for k in range(T):
        direct = (15.6 + a_youth + yr_y[k]
                  + TRUE["own"] * A[:, k]
                  + TRUE["down_spec"] * DSPEC[:, k]
                  + TRUE["down_gen"] * DGEN[:, k]
                  + TRUE["up"] * UP[:, k] + TRUE["peer"] * PEER[:, k]
                  + Cz[:, k, :] @ b_youth
                  + TRUE["xi_on_youth"] * XI[:, k]
                  + rng.normal(0, 2.3, N_FIRMS))
        Y[:, k] = sp.linalg.spsolve((I - TRUE["rho"] * W).tocsc(), direct)

        direct_x = (18.4 + a_exper + yr_x[k]
                    + TRUE["own_exper"] * A[:, k]
                    + TRUE["down_exper"] * DOWN[:, k]
                    + TRUE["up_exper"] * UP[:, k]
                    + TRUE["peer_exper"] * PEER[:, k]
                    + Cz[:, k, :] @ b_exper
                    + 0.16 * XI[:, k] + rng.normal(0, 2.1, N_FIRMS))
        X[:, k] = sp.linalg.spsolve((I - 0.10 * W).tocsc(), direct_x)

    # ------------------------------------------------------- assemble the panel
    rows = []
    for k, y in enumerate(YEARS):
        keep = np.flatnonzero((first <= y) & (last >= y))
        d = pd.DataFrame(dict(firm=keep, year=y))
        d["ind"] = ind[keep]
        d["city"] = city[keep]
        d["SOE"] = soe[keep]
        d["Tech"] = tech[keep]
        d["Exposure0"] = exposure0[keep]
        d["AI"] = A[keep, k]
        d["UpAI"] = UP[keep, k]
        d["DownAI"] = DOWN[keep, k]
        d["PeerAI"] = PEER[keep, k]
        d["ChainAI"] = CHAIN[keep, k]
        d["DownSpec"] = DSPEC[keep, k]
        d["DownGen"] = DGEN[keep, k]
        d["DownNear"] = DNEAR[keep, k]
        d["DownFar"] = DFAR[keep, k]
        d["WYouth"] = (W @ Y[:, k])[keep]
        d["WExper"] = (W @ X[:, k])[keep]
        d["Youth"] = np.clip(Y[keep, k], 1.0, 72.0)
        d["Exper"] = np.clip(X[keep, k], 1.0, 72.0)
        d["Emp"] = np.exp(lnL[keep, k])
        d["lnEmp"] = lnL[keep, k]
        for c in ctrl_names:
            d[c] = C[c].reshape(N_FIRMS, T)[keep, k]
        d["IV_Own"] = (e0 * NAT_A[y])[keep]
        d["IV_Up"] = (e_up * NAT_A[y])[keep]
        d["IV_Down"] = (e_down * NAT_A[y])[keep]
        d["IV_Peer"] = (e_peer * NAT_A[y])[keep]
        d["IV_Up2"] = (e2_up * NAT_A[y])[keep]
        d["IV_Down2"] = (e2_down * NAT_A[y])[keep]
        d["W2AI"] = W2A[keep, k]
        d["W3AI"] = W3A[keep, k]
        rows.append(d)

    df = pd.concat(rows, ignore_index=True)
    df["Post"] = (df.year >= SHOCK_YEAR).astype(int)
    cut = np.quantile(exposure0, 2 / 3)
    df["Treat"] = (df.Exposure0 >= cut).astype(int)
    for c in ["IV_Own", "IV_Up", "IV_Down", "IV_Peer", "IV_Up2", "IV_Down2"]:
        df[c] = _sd(df[c].to_numpy())
    df = df.sort_values(["firm", "year"]).reset_index(drop=True)

    os.makedirs(DATA, exist_ok=True)
    sp.save_npz(os.path.join(DATA, "W_up.npz"), W_up.tocsr())
    sp.save_npz(os.path.join(DATA, "W_down.npz"), W_down.tocsr())
    sp.save_npz(os.path.join(DATA, "W_peer.npz"), W_peer.tocsr())
    sp.save_npz(os.path.join(DATA, "W.npz"), W.tocsr())
    np.savez_compressed(os.path.join(DATA, "adoption.npz"), A=A,
                        years=np.array(YEARS))
    return df


CONTROLS = ["Size", "Lev", "ROA", "Growth", "Cash", "FirmAge", "TobinQ",
            "CapInt", "Wage", "Analyst", "InstOwn", "GDPg", "YouthU"]


def load():
    if not os.path.exists(OUT):
        d = build()
        d.to_csv(OUT, index=False)
    return pd.read_csv(OUT)


def load_W(name="W"):
    return sp.load_npz(os.path.join(DATA, "%s.npz" % name))


if __name__ == "__main__":
    d = build()
    d.to_csv(OUT, index=False)
    print("rows", len(d), "firms", d.firm.nunique(), "cities", d.city.nunique())
    print(d[["Youth", "Exper", "AI", "UpAI", "DownAI", "PeerAI"]].describe().T)
    print("corr(AI, DownAI) = %.3f" % d[["AI", "DownAI"]].corr().iloc[0, 1])
    print("corr(AI, PeerAI) = %.3f" % d[["AI", "PeerAI"]].corr().iloc[0, 1])
