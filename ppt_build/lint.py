# -*- coding: utf-8 -*-
"""Geometric layout linter — stands in for visual QA, since LibreOffice
cannot load PPTX in this environment.

Checks: out-of-bounds, slide-edge margins, and text overflow estimated from
CJK/ASCII glyph widths.
"""
from deckkit import W_IN, H_IN

MARGIN = 0.03          # allowed bleed past the canvas
MIN_EDGE = 0.02        # min distance from slide edge for text shapes


def _wide(ch):
    o = ord(ch)
    return (0x1100 <= o <= 0x115F or 0x2E80 <= o <= 0xA4CF or
            0xAC00 <= o <= 0xD7A3 or 0xF900 <= o <= 0xFAFF or
            0xFE30 <= o <= 0xFE6F or 0xFF00 <= o <= 0xFF60 or
            0xFFE0 <= o <= 0xFFE6 or 0x3000 <= o <= 0x303F)


def _em(s):
    """Text advance in em units for the given string."""
    t = 0.0
    for ch in s:
        if ch == '\n':
            continue
        t += 1.0 if _wide(ch) else (0.30 if ch == ' ' else 0.55)
    return t


def text_lines(s, pt, avail_in):
    """How many wrapped lines this string needs in a box `avail_in` wide."""
    avail_em = max(avail_in * 72.0 / pt, 0.5)
    n = 0
    for para in s.split('\n'):
        if not para:
            n += 1
            continue
        n += max(1, int(_em(para) / avail_em - 1e-9) + 1)
    return n


def check(slides, names=None, verbose=True):
    issues = []
    for i, sl in enumerate(slides, 1):
        nm = (names or {}).get(i, '')
        for (label, x, y, w, h, geom, txt, pt, pad) in sl.records:
            if x < -MARGIN or y < -MARGIN or x + w > W_IN + MARGIN or y + h > H_IN + MARGIN:
                issues.append((i, nm, label, 'OUT-OF-BOUNDS',
                               f'x={x:.2f} y={y:.2f} w={w:.2f} h={h:.2f}'))
            if txt:
                if x < MIN_EDGE or x + w > W_IN - MIN_EDGE:
                    issues.append((i, nm, label, 'EDGE', f'x={x:.2f} x2={x+w:.2f}'))
                avail = w - pad
                if avail <= 0.05:
                    issues.append((i, nm, label, 'NO-WIDTH', f'w={w:.2f} pad={pad:.2f}'))
                    continue
                n = text_lines(txt, pt, avail)
                need = n * pt * 1.34 / 72.0
                if need > h * 1.06 + 0.005:
                    issues.append((i, nm, label, 'OVERFLOW',
                                   f'{n}行×{pt}pt 需{need:.2f}" 实{h:.2f}" '
                                   f'「{txt[:34].replace(chr(10), "/")}」'))
        # overlap between cards / flow tiles / banners on the same slide
        boxes = [r for r in sl.records
                 if r[5] == 'roundRect' and r[3] > 1.2 and r[4] > 0.35]
        for a in range(len(boxes)):
            for b in range(a + 1, len(boxes)):
                _, ax, ay, aw, ah, *_ = boxes[a]
                _, bx, by, bw, bh, *_ = boxes[b]
                ox = min(ax + aw, bx + bw) - max(ax, bx)
                oy = min(ay + ah, by + bh) - max(ay, by)
                if ox > 0.02 and oy > 0.02:
                    issues.append((i, nm, boxes[a][0], 'OVERLAP',
                                   f'{boxes[b][0]} 重叠 {ox:.2f}"×{oy:.2f}"'))
    if verbose:
        if not issues:
            print(f'LINT OK — {len(slides)} 页，无越界 / 无溢出')
        else:
            print(f'LINT: {len(issues)} 处问题')
            for it in issues[:70]:
                print('  p%-3d %-22s %-11s %-13s %s' % it)
    return issues
