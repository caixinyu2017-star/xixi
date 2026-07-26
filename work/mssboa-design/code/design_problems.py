"""Visual-design optimization problems used in Section 5.

Problem 1 - aesthetic colour-harmony palette generation      (Eqs. 15-19)
Problem 2 - graphic-layout aesthetics optimization           (Eqs. 20-22)

Both are written as *minimization* problems (the optimizer minimizes -f) so
that they plug into the same runner as the CEC2017 benchmarks.

Colour space
------------
Colours live in HSV.  HSV is used because Matsuda's harmonic templates are
defined as angular sectors on the hue wheel, so hue must be an explicit,
cyclic coordinate; saturation supplies the perceptual weight of a hue (a
desaturated colour carries almost no hue information) and value supplies the
tonal contrast term.  Perceptual distances that the objective needs - the
lightness spread - are evaluated after converting to CIE L*a*b*, which is
approximately perceptually uniform.

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


def hue_arc(h1, h2):
    """Geodesic (arc-length) distance on the cyclic hue wheel.        (Eq. 15)"""
    d = np.abs(h1 - h2) % 360.0
    return np.minimum(d, 360.0 - d)


def _dist_to_template(h, sectors, alpha):
    """Arc distance from hue h to the nearest sector of template T(alpha).

    Zero when h falls inside a sector.
    """
    best = np.full(np.shape(h), 180.0)
    for off, width in sectors:
        centre = (off + alpha) % 360.0
        d = hue_arc(h, centre) - width / 2.0
        best = np.minimum(best, np.maximum(d, 0.0))
    return best


def disharmony(hues, sats, n_alpha=72):
    """Saturation-weighted disharmony energy of a palette.            (Eq. 16)

    E(P) = min_{m in M, alpha} sum_i  d(h_i, T_m(alpha)) * s_i
    M is the set of seven chromatic templates; alpha is sampled on a grid of
    n_alpha rotations (5-degree resolution by default).
    """
    alphas = np.linspace(0.0, 360.0, n_alpha, endpoint=False)
    hues = np.asarray(hues, float)
    sats = np.asarray(sats, float)
    best_e, best_key = np.inf, None
    for name, sectors in HARMONIC_TEMPLATES.items():
        # (n_alpha, K) distance of every hue to the template at every rotation
        d = np.full((len(alphas), hues.size), 180.0)
        for off, width in sectors:
            centre = (off + alphas) % 360.0
            dd = hue_arc(hues[None, :], centre[:, None]) - width / 2.0
            d = np.minimum(d, np.maximum(dd, 0.0))
        e = d @ sats
        j = int(np.argmin(e))
        if e[j] < best_e:
            best_e, best_key = float(e[j]), (name, float(alphas[j]))
    return best_e, best_key


def harmony_term(hues, sats):
    """Disharmony energy mapped to a harmony score in [0, 1].         (Eq. 17)

    HAR = 1 - E(P) / E_max,   E_max = 180 K  (every hue maximally misplaced
    at full saturation).
    """
    e, key = disharmony(hues, sats)
    return 1.0 - e / (180.0 * len(hues)), key


def diversity_term(hues, sats, vals):
    """Hue-diversity term.                                            (Eq. 18)

    DIV = (2 / (K (K-1))) * sum_{i<j} d(h_i, h_j) / 180
    i.e. the mean normalized pairwise arc distance; it is 0 for a monochrome
    palette and 1 when every pair of hues is complementary.
    """
    K = len(hues)
    if K < 2:
        return 0.0
    tot, cnt = 0.0, 0
    for i in range(K):
        for j in range(i + 1, K):
            tot += hue_arc(hues[i], hues[j]) / 180.0
            cnt += 1
    return tot / cnt


def contrast_term(vals):
    """Tonal-contrast term: rewards a usable lightness spread.

    CON = min(1, (max V - min V) / 0.6)
    A palette needs roughly 60% of the value range to remain legible when it
    is used for text on background; more spread than that is not rewarded.
    """
    return float(min(1.0, (np.max(vals) - np.min(vals)) / 0.6))


W_COLOR = dict(har=0.60, div=0.25, con=0.15)


def palette_score(x, K, weights=None):
    """Aesthetic objective of a K-colour palette.                     (Eq. 19)

    x = (h_1, s_1, v_1, ..., h_K, s_K, v_K), h in [0,360), s, v in [0.2, 1].
    f = w_har HAR + w_div DIV + w_con CON,  w_har + w_div + w_con = 1.
    """
    w = dict(W_COLOR if weights is None else weights)
    p = np.asarray(x, float).reshape(K, 3)
    hues = p[:, 0] % 360.0
    sats = np.clip(p[:, 1], 0.0, 1.0)
    vals = np.clip(p[:, 2], 0.0, 1.0)
    har, _ = harmony_term(hues, sats)
    return (w['har'] * har + w['div'] * diversity_term(hues, sats, vals)
            + w['con'] * contrast_term(vals))


def color_problem(K, weights=None):
    lb = np.tile([0.0, 0.2, 0.15], K)
    ub = np.tile([360.0, 1.0, 1.0], K)
    return Problem(lambda x: -palette_score(x, K, weights), lb, ub, 3 * K,
                   f'COLOR-K{K}')


def hsv_to_rgb(h, s, v):
    h = float(h) % 360.0
    c = v * s
    xx = c * (1 - abs((h / 60.0) % 2 - 1))
    m = v - c
    i = int(h // 60) % 6
    r, g, b = [(c, xx, 0), (xx, c, 0), (0, c, xx),
               (0, xx, c), (xx, 0, c), (c, 0, xx)][i]
    return (r + m, g + m, b + m)


# ------------------------------------------------------------------- layouts
#  Ngo, D.C.L.; Teo, L.S.; Byrne, J.G.  Modelling interface aesthetics.
#  Inf. Sci. 2003, 152, 25-46.
W_LAYOUT = dict(BM=0.30, OV=0.22, AL=0.18, SY=0.15, DEN=0.15)
PENALTY = 2.0


def _rects(x, sizes):
    """Decode the decision vector into axis-aligned rectangles.

    x holds the normalized centres (cx_1, cy_1, ..., cx_n, cy_n) in [0,1]^2n;
    sizes holds the fixed (w_i, h_i) of every element in canvas units.
    """
    c = np.asarray(x, float).reshape(-1, 2)
    w = sizes[:, 0]
    h = sizes[:, 1]
    x0 = c[:, 0] - w / 2.0
    y0 = c[:, 1] - h / 2.0
    return np.column_stack([x0, y0, x0 + w, y0 + h])


def balance_measure(R, areas):
    """Visual balance.                                                (Eq. 20)

    BM = 1 - (|BM_v| + |BM_h|) / 2
    BM_v = (w_L - w_R) / max(|w_L|, |w_R|),  w_side = sum_j a_j d_j
    where d_j is the distance from the centre of element j to the vertical
    (resp. horizontal) axis of the canvas; the same for BM_h.
    """
    cx = (R[:, 0] + R[:, 2]) / 2.0
    cy = (R[:, 1] + R[:, 3]) / 2.0
    out = []
    for c, _ in ((cx, 'v'), (cy, 'h')):
        d = c - 0.5
        left = float(np.sum(areas[d < 0] * np.abs(d[d < 0])))
        right = float(np.sum(areas[d >= 0] * np.abs(d[d >= 0])))
        m = max(abs(left), abs(right))
        out.append(0.0 if m < 1e-12 else (left - right) / m)
    return 1.0 - (abs(out[0]) + abs(out[1])) / 2.0


def overlap_measure(R, areas):
    """Non-overlap degree.                                            (Eq. 21)

    OV = 1 - sum_{i<j} area(R_i ^ R_j) / sum_i a_i
    clipped to [0, 1]; it is 1 for a layout with no overlapping elements.
    """
    dx = (np.minimum(R[:, None, 2], R[None, :, 2])
          - np.maximum(R[:, None, 0], R[None, :, 0])).clip(min=0.0)
    dy = (np.minimum(R[:, None, 3], R[None, :, 3])
          - np.maximum(R[:, None, 1], R[None, :, 1])).clip(min=0.0)
    inter = float(np.triu(dx * dy, 1).sum())
    return float(np.clip(1.0 - inter / float(np.sum(areas)), 0.0, 1.0))


def alignment_measure(R, tol=0.02):
    """Alignment: fraction of element pairs sharing an alignment guide.

    AL = (number of aligned pairs) / (number of pairs); a pair counts as
    aligned when any of their left, right, centre-x, top, bottom or centre-y
    coordinates coincide within tol.
    """
    n = len(R)
    if n < 2:
        return 1.0
    gx = np.column_stack([R[:, 0], R[:, 2], (R[:, 0] + R[:, 2]) / 2.0])
    gy = np.column_stack([R[:, 1], R[:, 3], (R[:, 1] + R[:, 3]) / 2.0])
    ok = np.zeros((n, n), dtype=bool)
    for g in (gx, gy):
        # |g[i,a] - g[j,b]| < tol for any guide pair (a, b)
        d = np.abs(g[:, None, :, None] - g[None, :, None, :])
        ok |= (d < tol).any(axis=(2, 3))
    iu = np.triu_indices(n, 1)
    return float(ok[iu].mean())


def symmetry_measure(R, areas):
    """Symmetry about the vertical and horizontal axes of the canvas.

    SY = 1 - (|S_v| + |S_h|) / 2 with S computed from the area-weighted
    first and second moments of the elements on either side of each axis,
    normalized as in Ngo et al.
    """
    cx = (R[:, 0] + R[:, 2]) / 2.0
    cy = (R[:, 1] + R[:, 3]) / 2.0
    w = R[:, 2] - R[:, 0]
    h = R[:, 3] - R[:, 1]
    res = []
    for c, other, ext in ((cx, cy, w), (cy, cx, h)):
        d = c - 0.5
        neg, pos = d < 0, d >= 0
        vals = []
        for m in (neg, pos):
            if not np.any(m):
                vals.append(np.zeros(3))
                continue
            vals.append(np.array([
                float(np.sum(areas[m] * np.abs(d[m]))),
                float(np.sum(areas[m] * np.abs(other[m] - 0.5))),
                float(np.sum(areas[m] * ext[m])),
            ]))
        a, b = vals
        den = np.maximum(np.abs(a), np.abs(b))
        den[den < 1e-12] = 1.0
        res.append(float(np.mean(np.abs(a - b) / den)))
    return 1.0 - (res[0] + res[1]) / 2.0


def density_measure(R, areas, ideal=0.5):
    """White-space / density term.

    DEN = 1 - |rho - rho*| / max(rho*, 1 - rho*)
    where rho is the fraction of the canvas covered by the union of the
    elements and rho* = 0.5 is the ideal coverage reported by Ngo et al.
    """
    rho = float(np.sum(areas))
    return float(np.clip(1.0 - abs(rho - ideal) / max(ideal, 1 - ideal), 0.0, 1.0))


def out_of_canvas(R):
    """Total area of the elements falling outside the unit canvas."""
    ox = np.maximum(0.0, -R[:, 0]) + np.maximum(0.0, R[:, 2] - 1.0)
    oy = np.maximum(0.0, -R[:, 1]) + np.maximum(0.0, R[:, 3] - 1.0)
    hh = R[:, 3] - R[:, 1]
    ww = R[:, 2] - R[:, 0]
    return float(np.sum(ox * hh + oy * ww))


def layout_score(x, sizes, weights=None, penalty=PENALTY):
    """Overall layout aesthetic objective.                            (Eq. 22)

    f = w_BM BM + w_OV OV + w_AL AL + w_SY SY + w_DEN DEN - lambda P_out
    """
    w = dict(W_LAYOUT if weights is None else weights)
    R = _rects(x, sizes)
    areas = (R[:, 2] - R[:, 0]) * (R[:, 3] - R[:, 1])
    f = (w['BM'] * balance_measure(R, areas)
         + w['OV'] * overlap_measure(R, areas)
         + w['AL'] * alignment_measure(R)
         + w['SY'] * symmetry_measure(R, areas)
         + w['DEN'] * density_measure(R, areas))
    return f - penalty * out_of_canvas(R)


# ------------------------------------------------------- the eight problems
def _sz(*pairs):
    return np.array(pairs, dtype=float)


LAYOUT_PROBLEMS = {
    # code:      (name,            element sizes as (w, h) fractions of canvas)
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
    return Problem(lambda x: -layout_score(x, sizes, weights),
                   np.zeros(2 * n), np.ones(2 * n), 2 * n, code)


def large_layout_sizes(n, rng_seed=20260726):
    """Element sizes for the scalability study (Reviewer 1, comment 12).

    A magazine-style grid of n elements whose total area is held at ~50% of
    the canvas so that the density term stays comparable with DL01-DL08.
    """
    rng = np.random.default_rng(rng_seed)
    ar = rng.uniform(0.6, 1.8, n)                  # aspect ratios
    base = np.sqrt(0.5 / n)
    scale = rng.uniform(0.75, 1.35, n)
    w = base * scale * np.sqrt(ar)
    h = base * scale / np.sqrt(ar)
    return np.column_stack([w, h])


def large_layout_problem(n, weights=None, seed=20260726):
    sizes = large_layout_sizes(n, seed)
    return Problem(lambda x: -layout_score(x, sizes, weights),
                   np.zeros(2 * n), np.ones(2 * n), 2 * n, f'DL-N{n}')
