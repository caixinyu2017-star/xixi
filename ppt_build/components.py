# -*- coding: utf-8 -*-
"""Reusable page furniture matching the two source decks."""
from deckkit import (Slide, text, run, _para_xml, esc,
                     GOLD, GOLD2, WHITE, CREAM, INK, GREEN, GREEN2, ORANGE,
                     AMBER, RED, RED2, BLUE, YELLOW, ACCENTS, FONT, W_IN, H_IN)

# ---- fixed geometry lifted from the source decks (inches) ----
TITLE_Y, TITLE_H = 0.00, 0.67
RULE1_Y = 0.66
NAV_Y, NAV_H = 0.72, 0.47
RULE2_Y = 1.24
VRULE_X = 1.99
SIDE_X, SIDE_W, SIDE_H = 0.04, 1.85, 0.72
SIDE_Y = [2.15, 3.54, 4.87]
CX, CW = 2.11, 11.17          # content column
CY = 1.40                     # content top
CBOT = 7.14                   # content bottom limit


def chrome(sl, course, sections, active_sec, sidebar, active_side):
    """Title bar + section chips + sidebar chips + rules."""
    text(sl, 0.30, TITLE_Y, 12.7, TITLE_H, [[run(course, 26, WHITE)]],
         anchor='ctr', label='标题')
    sl.line(0.03, RULE1_Y, 13.27, 0, WHITE, 1.0)

    xs = [(0.91, 3.30), (4.61, 3.77), (8.69, 3.18)]
    for i, (label, (x, w)) in enumerate(zip(sections, xs)):
        on = (i == active_sec)
        sl.shape(x, NAV_Y, w, NAV_H, 'flowChartAlternateProcess',
                 YELLOW if on else WHITE, YELLOW if on else None, 2.0,
                 paras=[_para_xml([run(label, 15, RED2 if on else '000000')],
                                  align='ctr')],
                 anchor='ctr', label='Nav', text_for_lint=label, pt_for_lint=15)
    sl.line(0.04, RULE2_Y, 13.27, 0, WHITE, 1.0)
    sl.line(VRULE_X, 1.29, 0, 6.10, WHITE, 1.0)

    for i, label in enumerate(sidebar[:3]):
        on = (i == active_side)
        parts = label.split('\n')
        paras = [_para_xml([run(p, 13, RED2 if on else '000000')], align='ctr')
                 for p in parts]
        sl.shape(SIDE_X, SIDE_Y[i], SIDE_W, SIDE_H, 'flowChartAlternateProcess',
                 YELLOW if on else WHITE, YELLOW if on else None, 2.0,
                 paras=paras, anchor='ctr', label='Side',
                 text_for_lint=max(parts, key=len), pt_for_lint=13)
    return sl


def heading(sl, gold, white=None, x=CX, y=CY, w=CW):
    """Big gold headline + optional white sub-line. Returns next free y."""
    text(sl, x, y - 0.06, w, 0.48, [[run(gold, 25, GOLD)]], anchor='ctr', label='H1')
    if white:
        text(sl, x, y + 0.42, w, 0.34, [[run(white, 16, WHITE)]],
             anchor='ctr', label='H2')
        return y + 0.82
    return y + 0.52


def _fit(lines, pt, avail_w, line_pct=100, space=0):
    """Height in inches that `lines` needs — same metric the linter uses."""
    from lint import text_lines
    from deckkit import SCALE
    pt = SCALE.get(pt, pt)
    n = sum(text_lines(''.join(r['t'] for r in ln) if isinstance(ln, list) else ln,
                       pt, avail_w) for ln in lines)
    lh = 1.0 + 0.34 * (line_pct / 100.0)
    return n * pt * lh / 72.0 + max(0, len(lines) - 1) * space / 72.0


def card(sl, x, y, w, h, header, body, accent=GREEN, hpt=15, bpt=14,
         head_h=0.36, body_align='l', line_pct=100, space=3):
    """Cream rounded card with a solid accent header bar.
    Grows taller than `h` when the body needs it."""
    body_h = h - head_h - 0.10
    with sl.group():
        sl.shape(x, y, w, h, 'roundRect', CREAM, accent, 1.25, radius=0.06)
        sl.shape(x, y, w, head_h, 'rect', accent, None,
                 paras=[_para_xml([run(header, hpt, WHITE)], align='ctr')],
                 anchor='ctr', label='CardHead',
                 text_for_lint=header, pt_for_lint=hpt)
        if body:
            lines = body if isinstance(body[0], list) else [[run(b, bpt, INK)] for b in body]
            text(sl, x + 0.12, y + head_h + 0.04, w - 0.24, body_h,
                 lines, anchor='t', align=body_align, label='CardBody',
                 line_pct=line_pct, space=space)
    return sl


def stat(sl, x, y, w, h, big, label, accent=ORANGE, bigpt=34, labpt=13):
    """Large number callout on a cream tile."""
    with sl.group():
        sl.shape(x, y, w, h, 'roundRect', CREAM, accent, 1.25, radius=0.10)
        text(sl, x, y + 0.06, w, h * 0.56, [[run(big, bigpt, accent)]],
             anchor='ctr', align='ctr', label='StatBig')
        text(sl, x + 0.06, y + h * 0.58, w - 0.12, h * 0.40 - 0.06,
             [[run(label, labpt, INK)]], anchor='ctr', align='ctr', label='StatLab')
    return sl


def chip(sl, x, y, w, h, label, fill=AMBER, stroke=GOLD2, pt=14, color=WHITE):
    sl.shape(x, y, w, h, 'roundRect', fill, stroke, 1.5, radius=0.22,
             paras=[_para_xml([run(label, pt, color)], align='ctr')],
             anchor='ctr', label='Chip', text_for_lint=label, pt_for_lint=pt)
    return sl


def flow(sl, y, items, h=0.95, x0=CX, total=CW, accent=GREEN, pt=14, subpt=11):
    """Horizontal step chain: items = [(title, sub), ...] with arrows between."""
    n = len(items)
    gap = 0.30
    bw = (total - gap * (n - 1)) / n
    for i, (t, s) in enumerate(items):
        x = x0 + i * (bw + gap)
        acc = accent if isinstance(accent, str) else accent[i % len(accent)]
        with sl.group():
            sl.shape(x, y, bw, h, 'roundRect', CREAM, acc, 1.25, radius=0.12)
            sl.shape(x, y, bw, 0.34, 'rect', acc, None,
                     paras=[_para_xml([run(t, pt, WHITE)], align='ctr')],
                     anchor='ctr', label='FlowHead', text_for_lint=t, pt_for_lint=pt)
            if s:
                text(sl, x + 0.06, y + 0.38, bw - 0.12, h - 0.44,
                     [[run(s, subpt, INK)]], anchor='ctr', align='ctr',
                     label='FlowBody', line_pct=92)
        if i < n - 1:
            sl.arrow(x + bw + 0.04, y + h / 2, gap - 0.08, WHITE, 2.0)
    return sl


def bullets(sl, x, y, w, h, items, pt=14, color=WHITE, marker='◆',
            mcolor=GOLD, space=7, line_pct=100):
    """Marker + text rows inside one text box."""
    lines = []
    for it in items:
        if isinstance(it, tuple):
            lines.append([run(marker + ' ', pt, mcolor),
                          run(it[0], pt, GOLD), run(it[1], pt, color)])
        else:
            lines.append([run(marker + ' ', pt, mcolor), run(it, pt, color)])
    return text(sl, x, y, w, h, lines, anchor='t', label='Bullets',
                space=space, line_pct=line_pct)


def banner(sl, y, label, body, h=0.62, x=CX, w=CW, fill=AMBER, pt=14):
    """Full-width amber takeaway bar: bold label then body."""
    with sl.group():
        sl.shape(x, y, w, h, 'roundRect', fill, GOLD2, 1.5, radius=0.16)
        text(sl, x + 0.18, y, w - 0.36, h,
             [[run(label, pt, '2B1400'), run(body, pt, WHITE)]],
             anchor='ctr', label='Banner')
    return sl


def note(sl, y, body, h=0.52, x=CX, w=CW, pt=13, color=GOLD):
    text(sl, x, y, w, h, [[run(body, pt, color)]], anchor='ctr',
         align='ctr', label='Note')
    return sl


# ---------------------------------------------------------------- scenario
def scenario(sl, course, sections, active_sec, sidebar, active_side,
             idx, title, situation, ask, common, better):
    """情境 page — same geometry as the source decks' 情境1..6."""
    chrome(sl, course, sections, active_sec, sidebar, active_side)
    chip(sl, CX, 1.42, 1.50, 0.50, f'情境 {idx}', AMBER, GOLD2, 15)
    text(sl, 3.70, 1.40, 9.58, 0.54, [[run(title, 17, GOLD2)]],
         anchor='ctr', label='ScTitle')

    assert len(situation) <= 6, f'情境正文最多6行，实{len(situation)}'
    assert len(better) <= 5, f'反常识做法最多5行，实{len(better)}'

    sl.shape(CX, 2.02, CW, 2.22, 'rect', WHITE, GREEN2, 1.5)
    sl.shape(CX, 2.02, CW, 0.38, 'rect', GREEN2, None,
             paras=[_para_xml([run('现  场  情  境', 14, WHITE)], align='ctr')],
             anchor='ctr', label='ScHead', text_for_lint='现场情境', pt_for_lint=14)
    text(sl, CX + 0.16, 2.44, CW - 0.32, 1.74,
         [[run(p, 12, '1A1A1A')] for p in situation],
         anchor='t', label='ScBody', space=3, line_pct=102)

    sl.shape(CX, 4.34, CW, 0.44, 'roundRect', GREEN, GOLD2, 1.25, radius=0.20,
             paras=[_para_xml([run('讨 论', 13, GOLD2), run('　' + ask, 13, WHITE)])],
             anchor='ctr', label='ScAsk', lIns=0.18,
             text_for_lint='讨论 ' + ask, pt_for_lint=13)

    sl.shape(CX, 4.86, CW, 0.48, 'roundRect', '3A3A3A', '9A9A9A', 1.25,
             radius=0.16,
             paras=[_para_xml([run('普遍做法　', 13, 'FFC9A0'), run(common, 13, WHITE)])],
             anchor='ctr', label='ScCommon', lIns=0.18,
             text_for_lint='普遍做法 ' + common, pt_for_lint=13)

    sl.shape(CX, 5.42, CW, 1.72, 'roundRect', AMBER, GOLD2, 1.75, radius=0.12)
    text(sl, CX + 0.18, 5.46, CW - 0.36, 1.64,
         [[run('反常识做法  ▸  ', 14, '2B1400'), run(better[0], 14, WHITE)]] +
         [[run(b, 13, WHITE)] for b in better[1:]],
         anchor='ctr', label='ScBetter', space=4, line_pct=104)
    return sl


# ---------------------------------------------------------------- team task
def team_task(sl, badge, title, situation, tasks, scoring, intro=False):
    """Opening / closing team-task page (no nav chrome, like source slide 49)."""
    chip(sl, 0.40, 0.46, 1.85, 0.56, badge, AMBER, GOLD2, 15)
    text(sl, 2.40, 0.44, 10.55, 0.60, [[run(title, 20, GOLD)]],
         anchor='ctr', label='TTTitle')

    sit_h = 0.52 + 0.30 * len(situation)
    sl.shape(0.40, 1.20, 12.55, sit_h, 'rect', WHITE, GREEN2, 1.5)
    sl.shape(0.40, 1.20, 1.30, sit_h, 'rect', GREEN2, None,
             paras=[_para_xml([run('情  境', 14, WHITE)], align='ctr')],
             anchor='ctr', label='TTSitHead', text_for_lint='情境', pt_for_lint=14)
    text(sl, 1.86, 1.26, 10.95, sit_h - 0.12,
         [[run(p, 13, '1A1A1A')] for p in situation],
         anchor='ctr', label='TTSit', space=5, line_pct=105)

    ty = 1.20 + sit_h + 0.22
    th = 7.10 - ty
    sl.shape(0.40, ty, 12.55, th, 'rect', CREAM, AMBER, 1.75)
    sl.shape(0.40, ty, 12.55, 0.46, 'rect', AMBER, None,
             paras=[_para_xml([run('团  队  任  务', 15, WHITE)], align='ctr')],
             anchor='ctr', label='TTHead', text_for_lint='团队任务', pt_for_lint=15)

    body_y = ty + 0.52
    lines = [[run(t[0], 14, RED if intro else GREEN),
              run('　' + t[1], 14, INK)] if isinstance(t, tuple)
             else [[run(t, 14, INK)]][0] for t in tasks]
    text(sl, 0.62, body_y, 12.10, th - 0.52 - 0.46, lines,
         anchor='t', label='TTTasks', space=7, line_pct=104)

    sl.shape(0.40, ty + th - 0.44, 12.55, 0.44, 'rect', AMBER, None,
             paras=[_para_xml([run('产　出　', 13, '2B1400'), run(scoring, 13, WHITE)])],
             anchor='ctr', label='TTScore', lIns=0.22,
             text_for_lint='产出 ' + scoring, pt_for_lint=13)
    return sl


# ---------------------------------------------------------------- cover
def cover(sl, title, subtitle, bullets_, presenter):
    sl.shape(1.10, 1.30, 11.13, 1.55, 'roundRect', None, GOLD, 2.5, radius=0.08)
    text(sl, 1.30, 1.42, 10.73, 0.86, [[run(title, 40, GOLD)]],
         anchor='ctr', align='ctr', label='CoverTitle')
    text(sl, 1.30, 2.26, 10.73, 0.48, [[run(subtitle, 17, WHITE)]],
         anchor='ctr', align='ctr', label='CoverSub')
    n = len(bullets_)
    gap, w = 0.28, (11.13 - 0.28 * (n - 1)) / n
    for i, (h, s) in enumerate(bullets_):
        x = 1.10 + i * (w + gap)
        sl.shape(x, 3.28, w, 1.72, 'roundRect', CREAM, ACCENTS[i % 6], 1.5, radius=0.10)
        sl.shape(x, 3.28, w, 0.40, 'rect', ACCENTS[i % 6], None,
                 paras=[_para_xml([run(h, 15, WHITE)], align='ctr')],
                 anchor='ctr', label='CovHead', text_for_lint=h, pt_for_lint=15)
        text(sl, x + 0.10, 3.74, w - 0.20, 1.20, [[run(s, 13, INK)]],
             anchor='ctr', align='ctr', label='CovBody', line_pct=104)
    text(sl, 1.10, 5.36, 11.13, 0.42, [[run(presenter, 14, WHITE)]],
         anchor='ctr', align='ctr', label='CoverBy')
    text(sl, 1.10, 5.82, 11.13, 0.40,
         [[run('亚德客企业内训 ｜ 车间班组长 · 职能骨干　|　全日 6 小时', 13, GOLD)]],
         anchor='ctr', align='ctr', label='CoverFoot')
    return sl
