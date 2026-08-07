# -*- coding: utf-8 -*-
"""Grow-to-fit pass.

The client asked for 18pt minimum type that also fills its box. Raising the
floor makes a handful of hand-laid boxes too short. Rather than trimming the
copy, this pass finds every text box that still overflows and pushes its
bottom edge down into whatever vertical space is provably free underneath —
taking the whole card (panel + header + body) with it, so nothing is ever
covered up. Boxes with nothing free below them are left for a manual fix and
reported by the linter.
"""
from deckkit import need_height

CBOT = 7.34          # bottom of the design content area
GAP = 0.06           # breathing room kept between a grown box and its neighbour
MAX_GROW = 1.40


def _span(r):
    if r['kind'] in ('cxn', 'pic'):
        x, w, _ = r['xy']
    else:
        x, w = r['geo']['x'], r['geo']['w']
    return x, x + w


def _unit(sl, r):
    """Every shape that must move together with `r` (its card)."""
    if r.get('g'):
        return [s for s in sl._sp if s.get('g') == r['g']]
    return [r]


def _container_bottom(sl, unit):
    """A text box drawn inside a panel may not grow past that panel, or it
    would spill over the frame it belongs to."""
    if len(unit) != 1 or unit[0]['kind'] != 'txt':
        return None
    r = unit[0]
    x0, x1 = _span(r)
    bot, best = r['y'] + r['h'], None
    for s in sl._sp:
        if s is r or s['kind'] not in ('sp',):
            continue
        sx0, sx1 = _span(s)
        if (sx0 <= x0 + 0.02 and sx1 >= x1 - 0.02 and
                s['y'] <= r['y'] + 0.02 and s['y'] + s['h'] >= bot - 0.05):
            b = s['y'] + s['h']
            best = b if best is None else min(best, b)
    return best


def _free_below(sl, unit, cbot):
    bot = max(s['y'] + s['h'] for s in unit)
    x0 = min(_span(s)[0] for s in unit)
    x1 = max(_span(s)[1] for s in unit)
    free = cbot - bot
    cb = _container_bottom(sl, unit)
    if cb is not None:
        free = min(free, cb - bot)
    for s in sl._sp:
        if s in unit or s['kind'] == 'cxn':
            continue
        sx0, sx1 = _span(s)
        if min(x1, sx1) - max(x0, sx0) <= 0.05:
            continue
        if s['y'] >= bot - 0.02:
            free = min(free, s['y'] - bot)
    return free


def _grow(sl, unit, amount):
    bot = max(s['y'] + s['h'] for s in unit)
    for s in unit:
        if s['y'] + s['h'] >= bot - 0.04:
            s['h'] += amount
            if s.get('rec') is not None:
                sl.records[s['rec']][4] = s['h']


def _deficits(sl):
    out = []
    for r in sl._sp:
        if r['kind'] != 'txt':
            continue
        t, rec = r['txt'], sl.records[r['rec']]
        need = need_height(rec[6], rec[7], r['geo']['w'] - t['lIns'] - t['rIns'],
                           rec[9], rec[10], rec[11])
        room = r['h'] - t['tIns'] - t['bIns']
        if need > room + 0.012:
            out.append((r, need - room))
    return out


def fit_slide(sl, cbot=CBOT, rounds=5):
    sl._finalize()
    for _ in range(rounds):
        todo = _deficits(sl)
        if not todo:
            return sl
        moved = False
        for r, d in todo:
            unit = _unit(sl, r)
            grow = min(d + 0.04, _free_below(sl, unit, cbot) - GAP, MAX_GROW)
            if grow > 0.01:
                _grow(sl, unit, grow)
                moved = True
        sl._finalize()
        if not moved:
            break
    return sl


def fit_all(slides, cbot=CBOT):
    for sl in slides:
        fit_slide(sl, cbot)
    return slides
