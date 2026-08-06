# -*- coding: utf-8 -*-
"""Reusable page furniture matching the two source decks."""
from deckkit import (Slide, text, run, _para_xml, esc, label_paras,
                     GOLD, GOLD2, WHITE, CREAM, INK, GREEN, GREEN2, ORANGE,
                     AMBER, RED, RED2, BLUE, YELLOW, ACCENTS, FONT, W_IN, H_IN,
                     need_height, PT_MIN)

# ---- fixed geometry lifted from the source decks (inches) ----
TITLE_Y, TITLE_H = 0.00, 0.67
RULE1_Y = 0.66
NAV_Y, NAV_H = 0.72, 0.47
RULE2_Y = 1.24
VRULE_X = 1.99
SIDE_X, SIDE_W, SIDE_H = 0.04, 1.85, 0.78
SIDE_Y = [2.14, 3.52, 4.90]
CX, CW = 2.11, 11.17          # content column
CY = 1.40                     # content top
CBOT = 7.14                   # content bottom limit

# ---- content area available to a generated illustration -------------
ART_X, ART_Y = 2.06, 1.30
ART_W, ART_H = 11.22, 6.04

# nav chips: wide enough that 第一节 / 第二节 / 第三节 each sit on one line
NAV_XS = [(0.16, 4.45), (4.75, 4.14), (9.03, 4.14)]


def chrome(sl, course, sections, active_sec, sidebar, active_side):
    """Title bar + section chips + sidebar chips + rules."""
    text(sl, 0.10, TITLE_Y, W_IN - 0.20, TITLE_H, [[run(course, 26, WHITE)]],
         anchor='ctr', align='ctr', label='标题',
         tIns=0.03, bIns=0.03, max_pt=28)
    sl.line(0.03, RULE1_Y, 13.27, 0, WHITE, 1.0)

    for i, (label, (x, w)) in enumerate(zip(sections, NAV_XS)):
        on = (i == active_sec)
        paras, pt, lp, flat, npara = label_paras(
            [[run(label, 15, RED2 if on else '000000')]],
            avail_w=w - 0.12, avail_h=NAV_H - 0.06, max_pt=20)
        sl.shape(x, NAV_Y, w, NAV_H, 'flowChartAlternateProcess',
                 YELLOW if on else WHITE, YELLOW if on else None, 2.0,
                 paras=paras, anchor='ctr', label='Nav',
                 lIns=0.06, rIns=0.06, tIns=0.03, bIns=0.03,
                 text_for_lint=flat, pt_for_lint=pt, pt_is_final=True,
                 npara_for_lint=npara)
    sl.line(0.04, RULE2_Y, 13.27, 0, WHITE, 1.0)
    sl.line(VRULE_X, 1.29, 0, 6.10, WHITE, 1.0)

    for i, label in enumerate(sidebar[:3]):
        on = (i == active_side)
        parts = label.split('\n')
        paras, pt, lp, flat, npara = label_paras(
            [[run(p, 13, RED2 if on else '000000', keep_breaks=True)]
             for p in parts],
            avail_w=SIDE_W - 0.12, avail_h=SIDE_H - 0.06, max_pt=19)
        sl.shape(SIDE_X, SIDE_Y[i], SIDE_W, SIDE_H, 'flowChartAlternateProcess',
                 YELLOW if on else WHITE, YELLOW if on else None, 2.0,
                 paras=paras, anchor='ctr', label='Side',
                 lIns=0.06, rIns=0.06, tIns=0.03, bIns=0.03,
                 text_for_lint=flat, pt_for_lint=pt, pt_is_final=True,
                 npara_for_lint=npara)
    return sl


def heading(sl, gold, white=None, x=CX, y=CY, w=CW):
    """Big gold headline + optional white sub-line. Returns next free y."""
    text(sl, x, 1.30, w, 0.54, [[run(gold, 25, GOLD)]], anchor='ctr',
         label='H1', tIns=0.02, bIns=0.02, max_pt=28)
    if white:
        text(sl, x, 1.84, w, 0.40, [[run(white, 16, WHITE)]],
             anchor='ctr', label='H2', tIns=0.02, bIns=0.02, max_pt=21)
        return 2.26
    return 1.86


def _fit(lines, pt, avail_w, line_pct=100, space=0):
    """Height in inches that `lines` needs — same metric the linter uses."""
    from deckkit import SCALE
    pt = max(PT_MIN, SCALE.get(pt, pt))
    txt = '\n'.join(''.join(r['t'] for r in ln) if isinstance(ln, list) else str(ln)
                    for ln in lines)
    return need_height(txt, pt, avail_w, line_pct, space, len(lines))


def card(sl, x, y, w, h, header, body, accent=GREEN, hpt=15, bpt=14,
         head_h=0.40, body_align='l', line_pct=100, space=3, max_pt=26):
    """Cream rounded card with a solid accent header bar."""
    body_h = h - head_h - 0.05
    with sl.group():
        sl.shape(x, y, w, h, 'roundRect', CREAM, accent, 1.25, radius=0.06)
        paras, pt, lp, flat, npara = label_paras(
            [[run(header, hpt, WHITE)]],
            avail_w=w - 0.20, avail_h=head_h - 0.04, max_pt=22)
        sl.shape(x, y, w, head_h, 'rect', accent, None, paras=paras,
                 anchor='ctr', label='CardHead', lIns=0.10, rIns=0.10,
                 tIns=0.02, bIns=0.02,
                 text_for_lint=flat, pt_for_lint=pt, pt_is_final=True,
                 npara_for_lint=npara)
        if body:
            lines = body if isinstance(body[0], list) else [[run(b, bpt, INK)] for b in body]
            text(sl, x + 0.10, y + head_h + 0.02, w - 0.20, body_h,
                 lines, anchor='t', align=body_align, label='CardBody',
                 line_pct=line_pct, space=space, max_pt=max_pt,
                 lIns=0.06, rIns=0.06, tIns=0.02, bIns=0.02)
    return sl


def stat(sl, x, y, w, h, big, label, accent=ORANGE, bigpt=34, labpt=13):
    """Large number callout on a cream tile."""
    with sl.group():
        sl.shape(x, y, w, h, 'roundRect', CREAM, accent, 1.25, radius=0.10)
        text(sl, x, y + 0.05, w, h * 0.54, [[run(big, bigpt, accent)]],
             anchor='ctr', align='ctr', label='StatBig', max_pt=46,
             tIns=0.02, bIns=0.02)
        text(sl, x + 0.06, y + h * 0.56, w - 0.12, h * 0.42 - 0.05,
             [[run(label, labpt, INK)]], anchor='ctr', align='ctr',
             label='StatLab', max_pt=22, line_pct=96)
    return sl


def chip(sl, x, y, w, h, label, fill=AMBER, stroke=GOLD2, pt=14, color=WHITE,
         max_pt=22):
    paras, spt, lp, flat, npara = label_paras(
        [[run(label, pt, color)]], avail_w=w - 0.16, avail_h=h - 0.06,
        max_pt=max_pt)
    sl.shape(x, y, w, h, 'roundRect', fill, stroke, 1.5, radius=0.22,
             paras=paras, anchor='ctr', label='Chip',
             lIns=0.08, rIns=0.08, tIns=0.03, bIns=0.03,
             text_for_lint=flat, pt_for_lint=spt, pt_is_final=True,
             npara_for_lint=npara)
    return sl


def flow(sl, y, items, h=0.95, x0=CX, total=CW, accent=GREEN, pt=14, subpt=11,
         head_h=0.42):
    """Horizontal step chain: items = [(title, sub), ...] with arrows between."""
    n = len(items)
    gap = 0.30
    bw = (total - gap * (n - 1)) / n
    for i, (t, s) in enumerate(items):
        x = x0 + i * (bw + gap)
        acc = accent if isinstance(accent, str) else accent[i % len(accent)]
        with sl.group():
            sl.shape(x, y, bw, h, 'roundRect', CREAM, acc, 1.25, radius=0.12)
            paras, hp, lp, flat, npara = label_paras(
                [[run(t, pt, WHITE)]], avail_w=bw - 0.16,
                avail_h=head_h - 0.04, max_pt=22)
            sl.shape(x, y, bw, head_h, 'rect', acc, None, paras=paras,
                     anchor='ctr', label='FlowHead', lIns=0.08, rIns=0.08,
                     tIns=0.02, bIns=0.02,
                     text_for_lint=flat, pt_for_lint=hp, pt_is_final=True,
                 npara_for_lint=npara)
            if s:
                text(sl, x + 0.05, y + head_h + 0.02, bw - 0.10,
                     h - head_h - 0.05, [[run(s, subpt, INK)]], anchor='ctr',
                     align='ctr', label='FlowBody', line_pct=96, max_pt=21,
                     tIns=0.02, bIns=0.02)
        if i < n - 1:
            sl.arrow(x + bw + 0.04, y + h / 2, gap - 0.08, WHITE, 2.0)
    return sl


def bullets(sl, x, y, w, h, items, pt=14, color=WHITE, marker='◆',
            mcolor=GOLD, space=7, line_pct=100, max_pt=24):
    """Marker + text rows inside one text box."""
    lines = []
    for it in items:
        if isinstance(it, tuple):
            lines.append([run(marker + ' ', pt, mcolor),
                          run(it[0], pt, GOLD), run(it[1], pt, color)])
        else:
            lines.append([run(marker + ' ', pt, mcolor), run(it, pt, color)])
    return text(sl, x, y, w, h, lines, anchor='t', label='Bullets',
                space=space, line_pct=line_pct, max_pt=max_pt)


def banner(sl, y, label, body, h=0.66, x=CX, w=CW, fill=AMBER, pt=14,
           max_pt=23):
    """Full-width amber takeaway bar: bold label then body."""
    with sl.group():
        sl.shape(x, y, w, h, 'roundRect', fill, GOLD2, 1.5, radius=0.16)
        text(sl, x + 0.16, y, w - 0.32, h,
             [[run(label, pt, '2B1400'), run(body, pt, WHITE)]],
             anchor='ctr', label='Banner', max_pt=max_pt, tIns=0.03, bIns=0.03)
    return sl


def note(sl, y, body, h=0.52, x=CX, w=CW, pt=13, color=GOLD, max_pt=22):
    text(sl, x, y, w, h, [[run(body, pt, color)]], anchor='ctr',
         align='ctr', label='Note', max_pt=max_pt)
    return sl


def bar(sl, x, y, w, h, lead, lead_color, body, fill, stroke, pt=13,
        radius=0.16, label='Bar', max_pt=22, geom='roundRect', lw=1.25):
    """One-line accent bar: coloured lead-in word then white body."""
    lines = [[run(lead, pt, lead_color), run(body, pt, WHITE)]]
    paras, spt, lp, flat, npara = label_paras(
        lines, align='l', avail_w=w - 0.34, avail_h=h - 0.08, max_pt=max_pt)
    sl.shape(x, y, w, h, geom, fill, stroke, lw, radius=radius, paras=paras,
             anchor='ctr', label=label, lIns=0.18, rIns=0.16,
             tIns=0.04, bIns=0.04, text_for_lint=flat, pt_for_lint=spt, pt_is_final=True,
             line_pct_for_lint=lp, npara_for_lint=npara)
    return sl


# ---------------------------------------------------------------- scenario
# 反常识做法 now lives in the speaker notes, so the three on-screen blocks
# stretch across the whole content area.
SC_BADGE = (CX, 1.36, 1.66, 0.56)
SC_TITLE = (3.92, 1.34, 9.36, 0.60)
SC_SIT = (CX, 2.02, CW, 3.42)
SC_ASK = (CX, 5.54, CW, 0.70)
SC_COMMON = (CX, 6.32, CW, 0.82)


def scenario(sl, course, sections, active_sec, sidebar, active_side,
             idx, title, situation, ask, common, better):
    """情境 page — 现场情境 / 讨论 / 普遍做法 fill the screen;
    反常识做法 goes to 备注 so the trainer reveals it after the discussion."""
    chrome(sl, course, sections, active_sec, sidebar, active_side)
    chip(sl, *SC_BADGE, f'情境 {idx}', AMBER, GOLD2, 15, max_pt=22)
    text(sl, *SC_TITLE, [[run(title, 17, GOLD2)]], anchor='ctr',
         label='ScTitle', tIns=0.03, bIns=0.03, max_pt=24)

    x, y, w, h = SC_SIT
    head_h = 0.46
    sl.shape(x, y, w, h, 'rect', WHITE, GREEN2, 1.5)
    paras, hp, lp, flat, npara = label_paras(
        [[run('现  场  情  境', 14, WHITE)]], avail_w=w - 0.24,
        avail_h=head_h - 0.04, max_pt=22)
    sl.shape(x, y, w, head_h, 'rect', GREEN2, None, paras=paras, anchor='ctr',
             label='ScHead', lIns=0.12, rIns=0.12, tIns=0.02, bIns=0.02,
             text_for_lint=flat, pt_for_lint=hp, pt_is_final=True,
                 npara_for_lint=npara)
    text(sl, x + 0.16, y + head_h + 0.04, w - 0.32, h - head_h - 0.10,
         [[run(p, 12, '1A1A1A')] for p in situation],
         anchor='t', label='ScBody', space=4, line_pct=104, max_pt=24)

    bar(sl, *SC_ASK, '讨 论　', GOLD2, ask, GREEN, GOLD2, pt=13, radius=0.20,
        label='ScAsk', max_pt=23)
    bar(sl, *SC_COMMON, '普遍做法　', 'FFC9A0', common, '3A3A3A', '9A9A9A',
        pt=13, radius=0.16, label='ScCommon', max_pt=22)

    sl.notes('【反常识做法 · 讲师用，讨论后再揭示】',
             *[b if isinstance(b, str) else str(b) for b in better],
             '',
             '带法建议：先让各组讲完「普遍做法」，把它写到白板上，再逐条对照上面的反常识观点；'
             '不要一上来就给答案，学员自己推翻自己的结论，记忆才留得住。')
    return sl


# ---------------------------------------------------------------- team task
def team_task(sl, badge, title, situation, tasks, scoring, intro=False,
              bottom=7.30):
    """Opening / closing team-task page (no nav chrome, like source slide 49).
    The 情境 panel is sized from what the text actually needs, so everything
    left over goes to the task list."""
    from deckkit import unwrap_paras
    chip(sl, 0.40, 0.42, 2.00, 0.60, badge, AMBER, GOLD2, 15, max_pt=23)
    text(sl, 2.56, 0.40, 10.40, 0.64, [[run(title, 20, GOLD)]],
         anchor='ctr', label='TTTitle', tIns=0.03, bIns=0.03, max_pt=26)

    sit_lines = unwrap_paras([[run(p, 13, '1A1A1A')] for p in situation])
    sit_txt = '\n'.join(''.join(r['t'] for r in ln) for ln in sit_lines)
    sit_h = need_height(sit_txt, PT_MIN, 10.83, 104, 5, len(sit_lines)) + 0.16
    sit_h = max(1.05, min(sit_h, 2.70))
    sl.shape(0.40, 1.16, 12.55, sit_h, 'rect', WHITE, GREEN2, 1.5)
    paras, hp, lp, flat, npara = label_paras(
        [[run('情  境', 14, WHITE)]], avail_w=1.30 - 0.16,
        avail_h=sit_h - 0.06, max_pt=22)
    sl.shape(0.40, 1.16, 1.30, sit_h, 'rect', GREEN2, None, paras=paras,
             anchor='ctr', label='TTSitHead', lIns=0.08, rIns=0.08,
             text_for_lint=flat, pt_for_lint=hp, pt_is_final=True,
                 npara_for_lint=npara)
    text(sl, 1.84, 1.20, 10.99, sit_h - 0.08,
         [[run(p, 13, '1A1A1A')] for p in situation],
         anchor='ctr', label='TTSit', space=5, line_pct=104, max_pt=23)

    ty = 1.16 + sit_h + 0.18
    th = bottom - ty
    head_h, foot_h = 0.50, 0.52
    sl.shape(0.40, ty, 12.55, th, 'rect', CREAM, AMBER, 1.75)
    paras, hp, lp, flat, npara = label_paras(
        [[run('团  队  任  务', 15, WHITE)]], avail_w=12.55 - 0.24,
        avail_h=head_h - 0.04, max_pt=23)
    sl.shape(0.40, ty, 12.55, head_h, 'rect', AMBER, None, paras=paras,
             anchor='ctr', label='TTHead', lIns=0.12, rIns=0.12,
             tIns=0.02, bIns=0.02,
             text_for_lint=flat, pt_for_lint=hp, pt_is_final=True,
                 npara_for_lint=npara)

    body_y = ty + head_h + 0.04
    lines = [[run(t[0], 14, RED if intro else GREEN),
              run('　' + t[1], 14, INK)] if isinstance(t, tuple)
             else [run(t, 14, INK)] for t in tasks]
    text(sl, 0.60, body_y, 12.15, th - head_h - foot_h - 0.08, lines,
         anchor='t', label='TTTasks', space=6, line_pct=104, max_pt=24)

    bar(sl, 0.40, ty + th - foot_h, 12.55, foot_h, '产　出　', '2B1400',
        scoring, AMBER, None, pt=13, geom='rect', label='TTScore', max_pt=22)
    return sl


# ---------------------------------------------------------------- cover
def cover(sl, title, subtitle, bullets_, presenter):
    sl.shape(1.10, 1.24, 11.13, 1.66, 'roundRect', None, GOLD, 2.5, radius=0.08)
    text(sl, 1.30, 1.34, 10.73, 0.94, [[run(title, 40, GOLD)]],
         anchor='ctr', align='ctr', label='CoverTitle', tIns=0.03, bIns=0.03,
         max_pt=44)
    text(sl, 1.30, 2.28, 10.73, 0.54, [[run(subtitle, 17, WHITE)]],
         anchor='ctr', align='ctr', label='CoverSub', max_pt=23)
    n = len(bullets_)
    gap, w = 0.28, (11.13 - 0.28 * (n - 1)) / n
    for i, (h, s) in enumerate(bullets_):
        x = 1.10 + i * (w + gap)
        sl.shape(x, 3.22, w, 1.86, 'roundRect', CREAM, ACCENTS[i % 6], 1.5, radius=0.10)
        paras, hp, lp, flat, npara = label_paras(
            [[run(h, 15, WHITE)]], avail_w=w - 0.16, avail_h=0.42, max_pt=22)
        sl.shape(x, 3.22, w, 0.46, 'rect', ACCENTS[i % 6], None, paras=paras,
                 anchor='ctr', label='CovHead', lIns=0.08, rIns=0.08,
                 tIns=0.02, bIns=0.02,
                 text_for_lint=flat, pt_for_lint=hp, pt_is_final=True,
                 npara_for_lint=npara)
        text(sl, x + 0.08, 3.70, w - 0.16, 1.32, [[run(s, 13, INK)]],
             anchor='ctr', align='ctr', label='CovBody', line_pct=104,
             max_pt=22)
    text(sl, 1.10, 5.34, 11.13, 0.50, [[run(presenter, 14, WHITE)]],
         anchor='ctr', align='ctr', label='CoverBy', max_pt=22)
    text(sl, 1.10, 5.92, 11.13, 0.48,
         [[run('亚德客企业内训 ｜ 车间班组长 · 职能骨干　|　全日 6 小时', 13, GOLD)]],
         anchor='ctr', align='ctr', label='CoverFoot', max_pt=21)
    return sl


# ---------------------------------------------------------------- artwork
def artwork(sl, path_rel, x=ART_X, y=ART_Y, w=ART_W, h=ART_H):
    """Drop a generated illustration into the content area (chrome excluded)."""
    sl.picture(path_rel, x, y, w, h)
    return sl
