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


def check(slides, names=None, verbose=True, limit=80):
    issues = []
    for i, sl in enumerate(slides, 1):
        nm = (names or {}).get(i, '')
        for rec in sl.records:
            (label, x, y, w, h, geom, txt, pt, pad,
             line_pct, space, npara, tbpad) = rec
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
