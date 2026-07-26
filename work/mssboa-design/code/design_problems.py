"""Visual-design optimization problems used in Section 5.

Problem 1 - aesthetic colour-harmony palette generation      (Eqs. 15-19)
Problem 2 - graphic-layout aesthetics optimization           (Eqs. 20-22)

Both are written as *minimization* problems (the optimizer minimizes -f) so
that they plug into the same runner as the CEC2017 benchmarks, and both are
evaluated a whole population at a time.

Colour space
------------
Colours live in HSV.  HSV is used because Matsuda's harmonic templates are
defined as angular sectors on the hue wheel, so hue must be an explicit,
cyclic coordinate; saturation supplies the perceptual weight of a hue (a
desaturated colour carries almost no hue information) and value supplies the
tonal contrast.

Harmonic templates
------------------
The seven chromatic templates of Matsuda, in the parameterization of
Cohen-Or et al. (SIGGRAPH 2006).  Each template is one or two sectors of
fixed angular width; the whole template may be rotated rigidly by an
arbitrary angle alpha in [0, 360).
"""
import numpy as np

from framework import Problem

# ------------------------------------------------------------------ colours
# name -> tuple of (sector centre offset in degrees, sector width in degrees)
HARMONIC_TEMPLATES = {
    'i': ((0.0, 18.0),),
    'V': ((0.0, 93.6),),
    'L': ((0.0, 18.0), (90.0, 79.2)),
    'I': ((0.0, 18.0), (180.0, 18.0)),
    'T': ((0.0, 180.0),),
    'Y': ((0.0, 93.6), (180.0, 18.0)),
    'X': ((0.0, 93.6), (180.0, 93.6)),
}
TEMPLATE_NAMES = list(HARMONIC_TEMPLATES)
N_ALPHA = 72                                   # 5-degree rotation grid
_ALPHAS = np.linspace(0.0, 360.0, N_ALPHA, endpoint=False)


def hue_arc(h1, h2):
    """Geodesic (arc-length) distance on the cyclic hue wheel.        (Eq. 15)"""
    d = np.abs(h1 - h2) % 360.0
    return np.minimum(d, 360.0 - d)


def disharmony_batch(hues, sats):
    """Saturation-weighted disharmony energy of a batch of palettes.  (Eq. 16)

    hues, sats : (B, K).  Returns (B,) energies, plus the index of the
    best-fitting template and rotation for each palette.
    """
    B, K = hues.shape
    best_e = np.full(B, np.inf)
    best_t = np.zeros(B, dtype=int)
    best_a = np.zeros(B)
    for ti, name in enumerate(TEMPLATE_NAMES):
        sectors = HARMONIC_TEMPLATES[name]
        # (n_alpha, B, K) distance of every hue to the template at every rotation
        d = np.full((N_ALPHA, B, K), 180.0)
        for off, width in sectors:
            centre = (off + _ALPHAS) % 360.0            # (n_alpha,)
            dd = hue_arc(hues[None, :, :], centre[:, None, None]) - width / 2.0
            np.minimum(d, np.maximum(dd, 0.0), out=d)
        e = np.einsum('abk,bk->ab', d, sats)            # (n_alpha, B)
        ai = np.argmin(e, axis=0)                       # (B,)
        ev = e[ai, np.arange(B)]
        upd = ev < best_e
        best_e[upd], best_t[upd], best_a[upd] = ev[upd], ti, _ALPHAS[ai[upd]]
    return best_e, best_t, best_a


def harmony_term(hues, sats):
    """Disharmony energy mapped to a harmony score in [0, 1].         (Eq. 17)

    HAR = 1 - E(P) / E_max,  E_max = 180 K.
    """
    e, t, a = disharmony_batch(hues, sats)
    return 1.0 - e / (180.0 * hues.shape[1]), t, a


def diversity_term(hues):
    """Hue-diversity term.                                            (Eq. 18)

    DIV = 2 / (K(K-1)) * sum_{i<j} d(h_i, h_j) / 180, the mean normalized
    pairwise arc distance: 0 for a monochrome palette, 1 when every pair of
    hues is complementary.
    """
    B, K = hues.shape
    if K < 2:
        return np.zeros(B)
    d = hue_arc(hues[:, :, None], hues[:, None, :]) / 180.0
    iu = np.triu_indices(K, 1)
    return d[:, iu[0], iu[1]].mean(axis=1)


def contrast_term(vals):
    """Tonal contrast: CON = min(1, (max V - min V) / 0.6)."""
    return np.minimum(1.0, (vals.max(axis=1) - vals.min(axis=1)) / 0.6)


W_COLOR = dict(har=0.60, div=0.25, con=0.15)


def palette_score(X, K, weights=None):
    """Aesthetic objective of a batch of K-colour palettes.           (Eq. 19)

    X : (B, 3K) with rows (h_1, s_1, v_1, ..., h_K, s_K, v_K).
    f = w_har HAR + w_div DIV + w_con CON,  the weights summing to one.
    """
    w = dict(W_COLOR if weights is None else weights)
    X = np.atleast_2d(np.asarray(X, float))
    P = X.reshape(len(X), K, 3)
    hues = P[:, :, 0] % 360.0
    sats = np.clip(P[:, :, 1], 0.0, 1.0)
    vals = np.clip(P[:, :, 2], 0.0, 1.0)
    har, _, _ = harmony_term(hues, sats)
    return (w['har'] * har + w['div'] * diversity_term(hues)
            + w['con'] * contrast_term(vals))


def best_template(x, K):
    """Best-fitting (template name, rotation) of a single palette."""
    P = np.asarray(x, float).reshape(1, K, 3)
    _, t, a = disharmony_batch(P[:, :, 0] % 360.0, np.clip(P[:, :, 1], 0, 1))
    return TEMPLATE_NAMES[int(t[0])], float(a[0])


def color_problem(K, weights=None):
    lb = np.tile([0.0, 0.2, 0.15], K)
    ub = np.tile([360.0, 1.0, 1.0], K)
    return Problem(lambda X: -palette_score(X, K, weights), lb, ub, 3 * K,
                   f'COLOR-K{K}', batch=True)


def hsv_to_rgb(h, s, v):
    h = float(h) % 360.0
    c = v * s
    xx = c * (1 - abs((h / 60.0) % 2 - 1))
    m = v - c
    i = int(h // 60) % 6
    r, g, b = [(c, xx, 0), (xx, c, 0), (0, c, xx),
               (0, xx, c), (xx, 0, c), (c, 0, xx)][i]
    return (min(1, r + m), min(1, g + m), min(1, b + m))


# ------------------------------------------------------------------- layouts
#  Ngo, D.C.L.; Teo, L.S.; Byrne, J.G.  Modelling interface aesthetics.
#  Inf. Sci. 2003, 152, 25-46.
W_LAYOUT = dict(BM=0.30, OV=0.22, AL=0.18, SY=0.15, DEN=0.15)
PENALTY = 2.0
ALIGN_TOL = 0.02


def _rects(X, sizes):
    """Decode a batch of decision vectors into axis-aligned rectangles.

    X : (B, 2n) normalized centres; returns (B, n, 4) as (x0, y0, x1, y1).
    """
    B = len(X)
    c = X.reshape(B, -1, 2)
    w, h = sizes[:, 0], sizes[:, 1]
    x0 = c[:, :, 0] - w / 2.0
    y0 = c[:, :, 1] - h / 2.0
    return np.stack([x0, y0, x0 + w, y0 + h], axis=2)


def balance_measure(R, areas):
    """Visual balance.                                                (Eq. 20)

    BM = 1 - (|BM_v| + |BM_h|)/2, with BM_v = (w_L - w_R)/max(|w_L|,|w_R|) and
    w_side = sum_j a_j d_j, d_j the distance of element j from the axis.
    """
    cx = (R[:, :, 0] + R[:, :, 2]) / 2.0
    cy = (R[:, :, 1] + R[:, :, 3]) / 2.0
    out = []
    for c in (cx, cy):
        d = c - 0.5
        wl = np.sum(areas * np.abs(d) * (d < 0), axis=1)
        wr = np.sum(areas * np.abs(d) * (d >= 0), axis=1)
        m = np.maximum(np.abs(wl), np.abs(wr))
        out.append(np.where(m < 1e-12, 0.0, (wl - wr) / np.where(m < 1e-12, 1, m)))
    return 1.0 - (np.abs(out[0]) + np.abs(out[1])) / 2.0


def overlap_measure(R, areas):
    """Non-overlap degree.                                            (Eq. 21)

    OV = 1 - sum_{i<j} area(R_i ^ R_j) / sum_i a_i, clipped to [0, 1].
    """
    dx = np.clip(np.minimum(R[:, :, None, 2], R[:, None, :, 2])
                 - np.maximum(R[:, :, None, 0], R[:, None, :, 0]), 0, None)
    dy = np.clip(np.minimum(R[:, :, None, 3], R[:, None, :, 3])
                 - np.maximum(R[:, :, None, 1], R[:, None, :, 1]), 0, None)
    n = R.shape[1]
    iu = np.triu_indices(n, 1)
    inter = (dx * dy)[:, iu[0], iu[1]].sum(axis=1)
    return np.clip(1.0 - inter / areas.sum(), 0.0, 1.0)


def alignment_measure(R, tol=ALIGN_TOL):
    """Alignment: fraction of element pairs sharing an alignment guide.

    A pair counts as aligned when any of their left, right, centre-x, top,
    bottom or centre-y coordinates coincide within tol.
    """
    n = R.shape[1]
    if n < 2:
        return np.ones(len(R))
    gx = np.stack([R[:, :, 0], R[:, :, 2], (R[:, :, 0] + R[:, :, 2]) / 2], axis=2)
    gy = np.stack([R[:, :, 1], R[:, :, 3], (R[:, :, 1] + R[:, :, 3]) / 2], axis=2)
    ok = np.zeros((len(R), n, n), dtype=bool)
    for g in (gx, gy):
        d = np.abs(g[:, :, None, :, None] - g[:, None, :, None, :])
        ok |= (d < tol).any(axis=(3, 4))
    iu = np.triu_indices(n, 1)
    return ok[:, iu[0], iu[1]].mean(axis=1)


def symmetry_measure(R, areas):
    """Symmetry about the vertical and horizontal axes of the canvas."""
    cx = (R[:, :, 0] + R[:, :, 2]) / 2.0
    cy = (R[:, :, 1] + R[:, :, 3]) / 2.0
    w = R[:, :, 2] - R[:, :, 0]
    h = R[:, :, 3] - R[:, :, 1]
    res = []
    for c, other, ext in ((cx, cy, w), (cy, cx, h)):
        d = c - 0.5
        vals = []
        for m in ((d < 0), (d >= 0)):
            vals.append(np.stack([
                np.sum(areas * np.abs(d) * m, axis=1),
                np.sum(areas * np.abs(other - 0.5) * m, axis=1),
                np.sum(areas * ext * m, axis=1)], axis=1))
        a, b = vals
        den = np.maximum(np.abs(a), np.abs(b))
        den = np.where(den < 1e-12, 1.0, den)
        res.append(np.mean(np.abs(a - b) / den, axis=1))
    return 1.0 - (res[0] + res[1]) / 2.0


def density_measure(R, areas, ideal=0.5):
    """White-space term: DEN = 1 - |rho - rho*| / max(rho*, 1 - rho*)."""
    rho = areas.sum()
    return np.full(len(R), float(np.clip(
        1.0 - abs(rho - ideal) / max(ideal, 1 - ideal), 0.0, 1.0)))


def out_of_canvas(R):
    """Total element area falling outside the unit canvas."""
    ox = np.clip(-R[:, :, 0], 0, None) + np.clip(R[:, :, 2] - 1.0, 0, None)
    oy = np.clip(-R[:, :, 1], 0, None) + np.clip(R[:, :, 3] - 1.0, 0, None)
    hh = R[:, :, 3] - R[:, :, 1]
    ww = R[:, :, 2] - R[:, :, 0]
    return np.sum(ox * hh + oy * ww, axis=1)


def layout_score(X, sizes, weights=None, penalty=PENALTY):
    """Overall layout aesthetic objective for a batch.                (Eq. 22)

    f = w_BM BM + w_OV OV + w_AL AL + w_SY SY + w_DEN DEN - lambda P_out
    """
    w = dict(W_LAYOUT if weights is None else weights)
    X = np.atleast_2d(np.asarray(X, float))
    R = _rects(X, sizes)
    areas = sizes[:, 0] * sizes[:, 1]
    f = (w['BM'] * balance_measure(R, areas)
         + w['OV'] * overlap_measure(R, areas)
         + w['AL'] * alignment_measure(R)
         + w['SY'] * symmetry_measure(R, areas)
         + w['DEN'] * density_measure(R, areas))
    return f - penalty * out_of_canvas(R)


def _sz(*pairs):
    return np.array(pairs, dtype=float)


LAYOUT_PROBLEMS = {
    'DL01': ('Poster',        _sz((.62, .30), (.44, .16), (.28, .10), (.22, .22), (.16, .08))),
    'DL02': ('Web banner',    _sz((.34, .40), (.40, .16), (.26, .12), (.18, .10), (.14, .08))),
    'DL03': ('Business card', _sz((.30, .22), (.42, .12), (.24, .10), (.18, .08))),
    'DL04': ('Magazine page', _sz((.46, .34), (.30, .24), (.36, .12), (.22, .16), (.20, .10), (.14, .08))),
    'DL05': ('Photo collage', _sz((.38, .34), (.30, .28), (.26, .24), (.22, .20), (.18, .16))),
    'DL06': ('Mobile UI',     _sz((.72, .14), (.52, .20), (.34, .14), (.24, .12), (.20, .10))),
    'DL07': ('Packaging',     _sz((.40, .26), (.34, .18), (.28, .14), (.20, .12), (.16, .10))),
    'DL08': ('Book cover',    _sz((.56, .26), (.40, .16), (.26, .12), (.18, .10))),
}


def layout_problem(code, weights=None):
    name, sizes = LAYOUT_PROBLEMS[code]
    n = len(sizes)
    return Problem(lambda X: -layout_score(X, sizes, weights),
                   np.zeros(2 * n), np.ones(2 * n), 2 * n, code, batch=True)


def large_layout_sizes(n, rng_seed=20260726):
    """Element sizes for the scalability study: a magazine-style grid whose
    total area is held at ~50% of the canvas so the density term stays
    comparable with DL01-DL08."""
    rng = np.random.default_rng(rng_seed)
    ar = rng.uniform(0.6, 1.8, n)
    base = np.sqrt(0.5 / n)
    scale = rng.uniform(0.75, 1.35, n)
    return np.column_stack([base * scale * np.sqrt(ar),
                            base * scale / np.sqrt(ar)])


def large_layout_problem(n, weights=None, seed=20260726):
    sizes = large_layout_sizes(n, seed)
    return Problem(lambda X: -layout_score(X, sizes, weights),
                   np.zeros(2 * n), np.ones(2 * n), 2 * n, f'DL-N{n}', batch=True)
