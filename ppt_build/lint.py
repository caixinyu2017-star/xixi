# -*- coding: utf-8 -*-
"""Geometric layout linter — stands in for visual QA, since LibreOffice
cannot load PPTX in this environment.

Checks: out-of-bounds, slide-edge margins, text overflow and occlusion.
The height model is imported from deckkit so the autofit and the linter can
never disagree about what fits.
"""
from deckkit import W_IN, H_IN, PT_MIN, need_height, text_lines, _em, _wide  # noqa: F401

CBOT = 7.36            # bottom of the design content area
MARGIN = 0.03          # allowed bleed past the canvas
MIN_EDGE = 0.02        # min distance from slide edge for text shapes
SLACK = 0.012          # rounding tolerance, inches


def check(slides, names=None, verbose=True, limit=80, coverage=False,
          min_fill=0.80, max_hole=0.62):
    issues = []
    for i, sl in enumerate(slides, 1):
        nm = (names or {}).get(i, '')
        sl._finalize()          # deferred text boxes must be resolved first,
        for rec in sl.records:  # otherwise their records are still placeholders
            (label, x, y, w, h, geom, txt, pt, pad,
             line_pct, space, npara, tbpad) = rec[:13]
            if x < -MARGIN or y < -MARGIN or x + w > W_IN + MARGIN or y + h > H_IN + MARGIN:
                issues.append((i, nm, label, 'OUT-OF-BOUNDS',
                               f'x={x:.2f} y={y:.2f} w={w:.2f} h={h:.2f}'))
            elif y + h > CBOT + 0.06:
                issues.append((i, nm, label, 'BELOW-AREA',
                               f'底边 {y + h:.2f}" > {CBOT:.2f}"'))
            if not txt:
                continue
            if pt < PT_MIN - 0.01:
                issues.append((i, nm, label, 'TOO-SMALL',
                               f'{pt}pt < {PT_MIN}pt 「{txt[:24]}」'))
            if x < MIN_EDGE or x + w > W_IN - MIN_EDGE:
                issues.append((i, nm, label, 'EDGE', f'x={x:.2f} x2={x+w:.2f}'))
            avail = w - pad
            if avail <= 0.05:
                issues.append((i, nm, label, 'NO-WIDTH', f'w={w:.2f} pad={pad:.2f}'))
                continue
            need = need_height(txt, pt, avail, line_pct, space, npara)
            room = h - tbpad
            if need > room + SLACK:
                n = text_lines(txt, pt, avail)
                issues.append((i, nm, label, 'OVERFLOW',
                               f'{n}行×{pt}pt 需{need:.2f}" 容{room:.2f}" '
                               f'「{txt[:30].replace(chr(10), "/")}」'))
        issues.extend(_occlusion(sl, i, nm))
        if coverage:
            issues.extend(_coverage(sl, i, nm, min_fill, max_hole))
    if verbose:
        if not issues:
            print(f'LINT OK — {len(slides)} 页：无越界 / 无溢出 / 无遮挡 / 字号 ≥ {PT_MIN}pt')
        else:
            kinds = {}
            for it in issues:
                kinds[it[3]] = kinds.get(it[3], 0) + 1
            print(f'LINT: {len(issues)} 处问题 {kinds}')
            for it in issues[:limit]:
                print('  p%-3d %-20s %-11s %-13s %s' % it)
    return issues


def _occlusion(sl, i, nm):
    """Filled panels must not sit on top of one another. Text boxes drawn
    inside their own panel are fine, so only opaque panels are compared."""
    out = []
    panels = [r for r in sl.records
              if r[5] in ('roundRect', 'rect', 'flowChartAlternateProcess')
              and r[3] > 1.0 and r[4] > 0.30]
    for a in range(len(panels)):
        for b in range(a + 1, len(panels)):
            _, ax, ay, aw, ah, *_ = panels[a]
            _, bx, by, bw, bh, *_ = panels[b]
            ox = min(ax + aw, bx + bw) - max(ax, bx)
            oy = min(ay + ah, by + bh) - max(ay, by)
            if ox <= 0.02 or oy <= 0.02:
                continue
            # a header bar sitting on the top edge of its own card is by design
            inside = (bx >= ax - 0.01 and bx + bw <= ax + aw + 0.01 and
                      by >= ay - 0.01 and by + bh <= ay + ah + 0.01)
            if inside:
                continue
            out.append((i, nm, panels[a][0], 'OVERLAP',
                        f'{panels[b][0]} 重叠 {ox:.2f}"×{oy:.2f}"'))
    return out


# ------------------------------------------------------------------ coverage
# 「边框不要留有大部分空白，整体内容部分也不要有大部分留白」——
# 把内容区栅格化，统计被形状盖住的比例，并找出最高的一条空白横带。
NAV_BOTTOM = 1.28          # content starts below the section-chip rule
FULL_TOP = 0.34            # pages without chrome (cover / team task)
CONTENT_L, CONTENT_R = 2.06, 13.28
FULL_L, FULL_R = 0.34, 12.99


def _content_rect(sl):
    has_nav = any(r[0].startswith('Nav') for r in sl.records)
    if has_nav:
        return CONTENT_L, NAV_BOTTOM, CONTENT_R, CBOT
    return FULL_L, FULL_TOP, FULL_R, CBOT


def _coverage(sl, i, nm, min_fill, max_hole, nx=112, ny=64):
    x0, y0, x1, y1 = _content_rect(sl)
    cw, ch = (x1 - x0) / nx, (y1 - y0) / ny
    rows = [[False] * nx for _ in range(ny)]
    for r in sl.records:
        _, sx, sy, sw, sh, geom, txt = r[:7]
        if sw <= 0.02 or sh <= 0.02 or not r[13]:
            continue                      # zero-size, or an unfilled helper box
        ca = max(0, int((sx - x0) / cw)); cb = min(nx, int((sx + sw - x0) / cw) + 1)
        ra = max(0, int((sy - y0) / ch)); rb = min(ny, int((sy + sh - y0) / ch) + 1)
        for rr in range(ra, rb):
            row = rows[rr]
            for cc in range(ca, cb):
                row[cc] = True
    filled = sum(sum(r) for r in rows)
    frac = filled / float(nx * ny)
    out = []
    if frac < min_fill:
        out.append((i, nm, '内容区', 'SPARSE', f'覆盖率 {frac*100:.0f}% < {min_fill*100:.0f}%'))
    # tallest run of near-empty rows
    run_len = best = 0
    for r in rows:
        if sum(r) < nx * 0.12:
            run_len += 1
            best = max(best, run_len)
        else:
            run_len = 0
    hole = best * ch
    if hole > max_hole:
        out.append((i, nm, '内容区', 'HOLE', f'空白横带 {hole:.2f}" > {max_hole:.2f}"'))
    return out
