"""Business-management application problems.

1. Cardinality-constrained mean-variance portfolio selection
   (Chang, Meade, Beasley & Sharaiha 2000; OR-Library port1-port5 data).
2. Customer segmentation as centroid-based clustering
   (Mall Customers, Wholesale Customers datasets).
"""
import numpy as np
from framework import Problem

DATA = '/home/user/xixi/work/data'


# ----------------------------------------------------------------- portfolio
def load_port(idx):
    """Return (mu, sigma) weekly mean returns and covariance from OR-Library file."""
    fn = f'{DATA}/port{idx}.txt'
    with open(fn) as fh:
        tokens = fh.read().split()
    it = iter(tokens)
    n = int(next(it))
    mu = np.zeros(n)
    sd = np.zeros(n)
    for i in range(n):
        mu[i] = float(next(it))
        sd[i] = float(next(it))
    cov = np.zeros((n, n))
    try:
        while True:
            i = int(next(it)); j = int(next(it)); c = float(next(it))
            cov[i - 1, j - 1] = cov[j - 1, i - 1] = c * sd[i - 1] * sd[j - 1]
    except StopIteration:
        pass
    return mu, cov


def decode_portfolio(z, mu, cov, K=10, eps=0.01):
    """Decode continuous vector z in [0,1]^n into a feasible cardinality-K portfolio."""
    n = len(mu)
    sel = np.argsort(z)[-K:]                      # K largest components are held
    zs = z[sel]
    s = zs / (zs.sum() + 1e-50)
    w = np.zeros(n)
    w[sel] = eps + s * (1 - K * eps)              # proportional floor repair
    return w

def portfolio_problem(idx, lam, K=10, eps=0.01):
    mu, cov = load_port(idx)
    n = len(mu)

    def fobj(z):
        w = decode_portfolio(np.asarray(z), mu, cov, K, eps)
        risk = w @ cov @ w
        ret = w @ mu
        return lam * risk - (1 - lam) * ret

    return Problem(fobj, 0.0, 1.0, n, f'port{idx}_lam{lam}'), mu, cov


# ----------------------------------------------------------------- clustering
def load_mall():
    import csv
    rows = []
    with open(f'{DATA}/Mall_Customers.csv') as fh:
        rd = csv.reader(fh)
        head = next(rd)
        for r in rd:
            rows.append([float(r[3]), float(r[4])])   # income, spending score
    return np.array(rows)


def load_wholesale():
    import csv
    rows = []
    with open(f'{DATA}/wholesale.csv') as fh:
        rd = csv.reader(fh)
        head = next(rd)
        for r in rd:
            rows.append([float(v) for v in r[2:]])     # six spending features
    X = np.array(rows)
    X = np.log10(X + 1.0)                              # heavy-tail correction
    return X


def sse(centers, Xdata):
    d2 = ((Xdata[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
    return float(d2.min(axis=1).sum())


def clustering_problem(Xdata, K, name):
    n, d = Xdata.shape
    lb = np.tile(Xdata.min(axis=0), K)
    ub = np.tile(Xdata.max(axis=0), K)

    def fobj(z):
        centers = np.asarray(z).reshape(K, d)
        return sse(centers, Xdata)

    p = Problem(fobj, 0, 1, K * d, name)
    p.lb, p.ub = lb, ub
    return p
