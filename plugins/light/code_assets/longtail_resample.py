"""Long-tail resampling for imbalanced behavior classes (Light db03/m02 asset).

Class-balanced sampler weights (Cui et al. 2019 effective number) and
inverse-frequency weights for loss. For dairy-goat behaviors where
standing/lying dominate and mounting/lameness are rare.
Self-test: verifies weight ordering, normalization, effective-number formula.
Run:  python longtail_resample.py
"""
import numpy as np


def class_counts(labels, num_classes=None):
    labels = np.asarray(labels, int)
    k = num_classes or int(labels.max()) + 1
    return np.bincount(labels, minlength=k).astype(float)


def effective_num_weights(counts, beta=0.999):
    """Cui 2019: w_c ∝ (1-beta)/(1-beta^{n_c}). Normalized to sum=num_classes."""
    counts = np.asarray(counts, float)
    eff = 1.0 - np.power(beta, counts)
    w = (1.0 - beta) / np.maximum(eff, 1e-12)
    return w / w.sum() * len(counts)


def inverse_freq_weights(counts):
    counts = np.asarray(counts, float)
    w = counts.sum() / np.maximum(counts, 1e-12)
    return w / w.sum() * len(counts)


def sample_weights(labels, scheme='effective', beta=0.999):
    """Per-sample weights for WeightedRandomSampler."""
    counts = class_counts(labels)
    cw = effective_num_weights(counts, beta) if scheme == 'effective' else inverse_freq_weights(counts)
    return cw[np.asarray(labels, int)]


if __name__ == '__main__':
    ok = True
    # dairy-goat-like long tail: standing=500, lying=400, feeding=200, ruminating=150, mounting=20, lameness=10
    counts = np.array([500, 400, 200, 150, 20, 10], float)

    w_eff = effective_num_weights(counts)
    w_inv = inverse_freq_weights(counts)
    print(f"counts          = {counts.astype(int).tolist()}")
    print(f"effective_num w = {np.round(w_eff,3).tolist()}")
    print(f"inverse_freq  w = {np.round(w_inv,3).tolist()}")

    # (1) rare classes must get higher weight than frequent ones
    ok &= w_eff[-1] > w_eff[0] and w_inv[-1] > w_inv[0]
    # (2) monotonic: fewer samples -> higher weight (counts descending -> weights ascending)
    ok &= bool(np.all(np.diff(w_eff) >= -1e-9)) and bool(np.all(np.diff(w_inv) >= -1e-9))
    # (3) normalized to num_classes
    ok &= abs(w_eff.sum() - len(counts)) < 1e-9 and abs(w_inv.sum() - len(counts)) < 1e-9
    print(f"rare>freq: {w_eff[-1]>w_eff[0]} | monotonic: {bool(np.all(np.diff(w_eff)>=-1e-9))} | sum=K: {abs(w_eff.sum()-len(counts))<1e-9}")

    # (4) beta=0 -> all weights equal (no reweighting); beta->1 -> approaches inverse-freq
    w0 = effective_num_weights(counts, beta=0.0)
    ok &= np.allclose(w0, np.ones_like(w0))
    print(f"beta=0 -> uniform weights: {np.allclose(w0, 1.0)}")

    # (5) per-sample mapping length matches
    labels = np.repeat(np.arange(6), counts.astype(int))
    sw = sample_weights(labels)
    ok &= len(sw) == len(labels) and sw[labels==5][0] > sw[labels==0][0]
    print(f"per-sample weights len={len(sw)} matches N={len(labels)}; rare sample heavier: {sw[labels==5][0] > sw[labels==0][0]}")

    print("ALL PASS" if ok else "FAIL")