"""Inter-rater agreement metrics for behavior/lameness annotation (Light db03/m06 asset).

Cohen's kappa, quadratic weighted kappa (QWK, for ordinal lameness score),
Fleiss' kappa (>=3 raters), and ICC(2,1) (continuous, two-way random).

Label-scale semantics (verified by adversarial gate):
- Default (num_classes=None): collapses to sorted OBSERVED labels, so weighted kappa
  matches sklearn.cohen_kappa_score EXACTLY even when labels have gaps (e.g. {0,1,4}).
- Ordinal mode (num_classes=K): uses the full 0..K-1 scale, so a missing middle score
  (e.g. lameness 1 vs 4) keeps its true ordinal distance of 3. This is the CORRECT
  choice for lameness scoring; it intentionally differs from sklearn's default.
Run:  python agreement.py
"""
import numpy as np


def confusion(a, b, k=None):
    a = np.asarray(a, int); b = np.asarray(b, int)
    if k is None:
        k = int(max(a.max(), b.max())) + 1
    m = np.zeros((k, k), float)
    for i, j in zip(a, b):
        m[i, j] += 1
    return m


def cohen_kappa(a, b, weights=None, num_classes=None):
    """weights: None | 'linear' | 'quadratic'. Returns kappa in [-1,1].

    num_classes=None -> collapse to observed labels (matches sklearn default).
    num_classes=K    -> use full 0..K-1 ordinal scale (preserves gap distances).
    """
    a = np.asarray(a, int); b = np.asarray(b, int)
    if num_classes is None:
        labels = np.unique(np.concatenate([a, b]))
        remap = {int(v): i for i, v in enumerate(labels)}
        a = np.array([remap[int(v)] for v in a], int)
        b = np.array([remap[int(v)] for v in b], int)
        k = len(labels)
    else:
        k = num_classes
    m = confusion(a, b, k)
    n = m.sum()
    po_row = m.sum(1) / n
    po_col = m.sum(0) / n
    expected = np.outer(po_row, po_col) * n
    if weights is None:
        w = 1.0 - np.eye(k)
    else:
        idx = np.arange(k)
        d = np.abs(idx[:, None] - idx[None, :]).astype(float)
        w = d if weights == 'linear' else d ** 2
        w = w / w.max()
    obs = (w * m).sum()
    exp = (w * expected).sum()
    return 1.0 - obs / exp if exp != 0 else 0.0


def quadratic_weighted_kappa(a, b):
    return cohen_kappa(a, b, weights='quadratic')


def fleiss_kappa(table):
    """table: (n_items, n_categories) counts of raters per category. >=3 raters."""
    table = np.asarray(table, float)
    n, k = table.shape
    n_rat = table.sum(1)[0]
    p_j = table.sum(0) / (n * n_rat)
    P_i = (np.square(table).sum(1) - n_rat) / (n_rat * (n_rat - 1))
    Pbar = P_i.mean()
    Pe = np.square(p_j).sum()
    return (Pbar - Pe) / (1 - Pe) if (1 - Pe) != 0 else 0.0


def icc21(data):
    """ICC(2,1) two-way random, single rater absolute agreement.
    data: (n_subjects, n_raters) continuous ratings."""
    data = np.asarray(data, float)
    n, k = data.shape
    gm = data.mean()
    ms_r = k * ((data.mean(1) - gm) ** 2).sum() / (n - 1)          # between subjects
    ms_c = n * ((data.mean(0) - gm) ** 2).sum() / (k - 1)          # between raters
    ss_t = ((data - gm) ** 2).sum()
    ss_e = ss_t - (k * ((data.mean(1) - gm) ** 2).sum()) - (n * ((data.mean(0) - gm) ** 2).sum())
    ms_e = ss_e / ((n - 1) * (k - 1))
    return (ms_r - ms_e) / (ms_r + (k - 1) * ms_e + k * (ms_c - ms_e) / n)


if __name__ == '__main__':
    rng = np.random.default_rng(0)
    a = rng.integers(0, 5, 200)
    b = a.copy()
    flip = rng.random(200) < 0.3
    b[flip] = rng.integers(0, 5, flip.sum())

    from sklearn.metrics import cohen_kappa_score
    ok = True

    mine = cohen_kappa(a, b)
    ref = cohen_kappa_score(a, b)
    print(f"cohen_kappa      mine={mine:.6f} sklearn={ref:.6f} diff={abs(mine-ref):.2e}")
    ok &= abs(mine - ref) < 1e-9

    mine = quadratic_weighted_kappa(a, b)
    ref = cohen_kappa_score(a, b, weights='quadratic')
    print(f"QWK              mine={mine:.6f} sklearn={ref:.6f} diff={abs(mine-ref):.2e}")
    ok &= abs(mine - ref) < 1e-9

    mine = cohen_kappa(a, b, weights='linear')
    ref = cohen_kappa_score(a, b, weights='linear')
    print(f"linear_kappa     mine={mine:.6f} sklearn={ref:.6f} diff={abs(mine-ref):.2e}")
    ok &= abs(mine - ref) < 1e-9

    # adversarial-gate reproduction: labels with a GAP ({0,1,4}, missing 2,3)
    ga = np.array([0, 0, 1, 1, 4, 4, 0, 1, 4, 1])
    gb = np.array([0, 1, 1, 1, 4, 0, 0, 1, 4, 4])
    # default mode (collapse observed) MUST equal sklearn default
    md = quadratic_weighted_kappa(ga, gb)
    rd = cohen_kappa_score(ga, gb, weights='quadratic')
    print(f"QWK gap/default  mine={md:.6f} sklearn={rd:.6f} diff={abs(md-rd):.2e}")
    ok &= abs(md - rd) < 1e-9
    # ordinal mode (full 0..4 scale) MUST equal sklearn WITH labels=arange(5)
    mo = cohen_kappa(ga, gb, weights='quadratic', num_classes=5)
    ro = cohen_kappa_score(ga, gb, weights='quadratic', labels=np.arange(5))
    print(f"QWK gap/ordinal  mine={mo:.6f} sklearn(labels=0..4)={ro:.6f} diff={abs(mo-ro):.2e}")
    ok &= abs(mo - ro) < 1e-9

    # perfect agreement -> kappa 1, ICC ~1
    print(f"fleiss(perfect)  ={fleiss_kappa([[3,0],[0,3],[3,0]]):.4f} (expect 1.0)")
    perfect = np.array([[1.,1.],[2.,2.],[3.,3.],[4.,4.]])
    print(f"icc21(perfect)   ={icc21(perfect):.4f} (expect ~1.0)")

    print("ALL PASS" if ok else "FAIL")
