# -*- coding: utf-8 -*-
"""Slide-XML builder that reuses the AirTAC training template package
(slideMaster2 chalkboard background, 微软雅黑, gold/cream design tokens).

Everything is emitted as native PowerPoint shapes so the result stays fully
editable, exactly like the two source decks.
"""
from xml.sax.saxutils import escape

EMU = 914400                     # per inch
W_IN, H_IN = 13.3333, 7.5        # canvas

# ---------------------------------------------------------------- tokens
GOLD      = 'F5D349'   # big headings
GOLD2     = 'F5C842'   # scenario title / badge stroke
WHITE     = 'FFFFFF'
CREAM     = 'FFF7E8'   # card body fill
INK       = '1E1E1E'   # text on cream
INK2      = '1A1A1A'
GREEN     = '2C6B53'
GREEN2    = '2E7D32'
ORANGE    = 'E55E24'
AMBER     = 'E67E22'
RED       = 'C02F2B'
RED2      = 'C00000'
BLUE      = '2E75B6'
PURPLE    = '6A4C93'
TEAL      = '11828C'
SLATE     = '4A5568'
YELLOW    = 'FFFF00'
ACCENTS   = [GREEN, ORANGE, BLUE, RED, PURPLE, TEAL]

FONT = '微软雅黑'


def _e(v):                       # inches -> EMU
    return int(round(v * EMU))


def _sz(pt):                     # points -> OOXML hundredths
    return int(round(pt * 100))


def esc(t):
    return escape(str(t))


# ---------------------------------------------------------------- metrics
# 微软雅黑 single-line advance is ~1.34 em; PowerPoint's spcPct scales that.
LH = 1.34
PT_MIN = 18                      # hard floor requested by the client
PT_MAX = 30                      # never grow a body run past this


def _wide(ch):
    o = ord(ch)
    return (0x1100 <= o <= 0x115F or 0x2E80 <= o <= 0xA4CF or
            0xAC00 <= o <= 0xD7A3 or 0xF900 <= o <= 0xFAFF or
            0xFE30 <= o <= 0xFE6F or 0xFF00 <= o <= 0xFF60 or
            0xFFE0 <= o <= 0xFFE6 or 0x3000 <= o <= 0x303F)


def _em(s):
    """Text advance in em units."""
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
    for para in str(s).split('\n'):
        if not para:
            n += 1
            continue
        n += max(1, int(_em(para) / avail_em - 1e-9) + 1)
    return n


def need_height(txt, pt, avail_in, line_pct=100, space=0, npara=1):
    """Height in inches the text needs — the single model used by both the
    autofit and the linter, so they can never disagree."""
    n = text_lines(txt, pt, avail_in)
    return (n * pt * LH * (line_pct / 100.0) / 72.0
            + max(0, npara - 1) * space / 72.0)


# ---------------------------------------------------------------- unwrap
# 「连贯的文字不需要断行」— drop breaks the author inserted in the middle of a
# running sentence, keep the ones that carry structure.
_TERM = set('。！？；：…”’」』》】）)')
_LEAD = set('①②③④⑤⑥⑦⑧⑨⑩◆▸●○·—－※→⇒【〔「『《（(“')
_LEADW = ('特点', '代价', '处理方式', '效果', '结果', '风险', '正确', '错误',
          '标准', '要求', '结论', '对策', '做法', '例：', '如：', '注：', '——')


def _joinable(a, b):
    a, b = a.rstrip(), b.lstrip('　 ')
    if not a or not b:
        return False
    if a[-1] in _TERM or b[0] in _LEAD or b.startswith(_LEADW):
        return False
    # 「正常：…」「双峰：…」 — a labelled item starts its own line
    return '：' not in b[:6] and ':' not in b[:6]


def unwrap(s):
    segs = str(s).split('\n')
    out = [segs[0]]
    for seg in segs[1:]:
        if _joinable(out[-1], seg):
            out[-1] = out[-1].rstrip() + seg.lstrip('　 ')
        else:
            out.append(seg)
    return '\n'.join(out)


def unwrap_paras(lines):
    """Same rule applied across paragraphs of a text box."""
    out = []
    for para in lines:
        if out and para and out[-1]:
            a = ''.join(r['t'] for r in out[-1])
            b = ''.join(r['t'] for r in para)
            if _joinable(a, b):
                head = dict(para[0]); head['t'] = head['t'].lstrip('　 ')
                out[-1] = out[-1] + [head] + list(para[1:])
                continue
        out.append(list(para))
    return out


# ---------------------------------------------------------------- runs
# Author sizes are written on a compact scale; SCALE lifts every one of them
# to at least the 18pt floor the client asked for.
SCALE = {11: 18, 12: 18, 13: 18, 14: 18, 15: 18, 16: 19, 17: 20,
         20: 22, 22: 24, 24: 25, 25: 26, 26: 28, 34: 34, 40: 40}


def run(text, pt, color=INK, bold=True, italic=False, keep_breaks=False):
    """One <a:r>. A literal \\n becomes a soft break unless the rule above
    decides it was a hand break inside a running sentence."""
    t = str(text) if keep_breaks else unwrap(text)
    return {'t': t, 'sz': max(PT_MIN, SCALE.get(pt, pt)), 'c': color,
            'b': bold, 'i': italic}


def _scaled(lines, mult):
    if mult == 1.0:
        return lines
    out = []
    for para in lines:
        out.append([dict(r, sz=max(PT_MIN, round(r['sz'] * mult * 2) / 2.0))
                    for r in para])
    return out


MIN_LINE_PCT = 82                # how tight leading may get to avoid overflow


def autofit(lines, avail_w, avail_h, line_pct=100, space=0,
            max_pt=PT_MAX, max_line_pct=132, grow=True):
    """Pick the largest uniform scale (and then the largest line spacing) that
    still fits the box — 「字体可以大一点，行间距可以大一点…也不要溢出」.
    Never drops any run below PT_MIN; tightens leading only as a last resort."""
    if not lines or avail_w <= 0.05 or avail_h <= 0.05:
        return lines, line_pct, space
    sizes = [r['sz'] for p in lines for r in p]
    if not sizes:
        return lines, line_pct, space
    base_min, base_max = min(sizes), max(sizes)
    txt = '\n'.join(''.join(r['t'] for r in p) for p in lines)
    npara = len(lines)

    def fits(mult, lp, sp):
        return need_height(txt, base_max * mult, avail_w, lp, sp,
                           npara) <= avail_h

    lo = min(1.0, max(PT_MIN / base_min, 0.80))
    hi = max(1.0, min(max_pt / base_max, 1.60)) if grow else 1.0
    step = max(0.5 / base_min, 0.01)

    if not fits(lo, line_pct, space):
        # the box is genuinely tight: give back leading before giving back size
        for sp in (space, 0):
            lp = line_pct
            while lp >= MIN_LINE_PCT:
                if fits(lo, lp, sp):
                    return _scaled(lines, lo), lp, sp
                lp -= 2
        return _scaled(lines, lo), MIN_LINE_PCT, 0

    best, m = lo, lo
    while m <= hi + 1e-9:
        if not fits(m, line_pct, space):
            break
        best, m = m, m + step
    lines = _scaled(lines, best)

    lp = line_pct
    if text_lines(txt, base_max * best, avail_w) > 1:
        while lp + 2 <= max_line_pct and fits(best, lp + 2, space):
            lp += 2
    return lines, lp, space


def _run_xml(r):
    """A run. A literal \\n is emitted as <a:br/> — PowerPoint ignores raw
    newlines inside <a:t>, so they must become real soft breaks."""
    props = f'lang="zh-CN" altLang="en-US" sz="{_sz(r["sz"])}"'
    if r['b']:
        props += ' b="1"'
    if r.get('i'):
        props += ' i="1"'
    rpr = (f'<a:rPr {props} dirty="0">'
           f'<a:solidFill><a:srgbClr val="{r["c"]}"/></a:solidFill>'
           f'<a:latin typeface="{FONT}" panose="020B0503020204020204" charset="-122"/>'
           f'<a:ea typeface="{FONT}" panose="020B0503020204020204" charset="-122"/>'
           f'<a:cs typeface="{FONT}" panose="020B0503020204020204" charset="-122"/>'
           f'</a:rPr>')
    out = []
    for k, seg in enumerate(str(r['t']).split('\n')):
        if k:
            out.append(f'<a:br>{rpr}</a:br>')
        if seg == '':
            continue
        sp = ' xml:space="preserve"' if seg != seg.strip() else ''
        out.append(f'<a:r>{rpr}<a:t{sp}>{esc(seg)}</a:t></a:r>')
    return ''.join(out)


def _para_xml(runs, align='l', space_before=0, line_pct=100, indent=0, hang=0):
    pr = f'<a:pPr algn="{align}"'
    if indent:
        pr += f' marL="{_e(indent)}"'
        if hang:
            pr += f' indent="-{_e(hang)}"'
    pr += '>'
    if line_pct != 100:
        pr += f'<a:lnSpc><a:spcPct val="{line_pct * 1000}"/></a:lnSpc>'
    if space_before:
        pr += f'<a:spcBef><a:spcPts val="{int(space_before * 100)}"/></a:spcBef>'
    pr += '<a:buNone/></a:pPr>'
    return '<a:p>' + pr + ''.join(_run_xml(r) for r in runs) + '</a:p>'


# ---------------------------------------------------------------- shapes
class Deck:
    def __init__(self):
        self.slides = []            # list of (xml_body, shape_records)

    def add(self, slide):
        self.slides.append(slide)
        return slide


class Slide:
    """Accumulates shapes; `.xml()` renders the whole <p:sld>."""

    def __init__(self, name=''):
        self._sp = []
        self._id = 1
        self._gid = 0
        self._cur_grp = None
        self.name = name
        self.records = []           # (label, x, y, w, h, kind, text, pt, ...)
        self.notes_text = []        # speaker notes paragraphs
        self.pictures = []          # (rIdImg*, absolute source path)

    class _G:
        def __init__(self, sl):
            self.sl = sl
        def __enter__(self):
            self.sl._gid += 1
            self.sl._cur_grp = self.sl._gid
            return self.sl
        def __exit__(self, *a):
            self.sl._cur_grp = None

    def group(self):
        """Shapes added inside `with sl.group():` reflow as one unit."""
        return Slide._G(self)

    # ---- low level -------------------------------------------------
    def _next(self, label):
        self._id += 1
        return self._id, f'{label} {self._id}'

    def _spPr(self, x, y, w, h, geom='rect', fill=None, line=None, lw=1.5,
              radius=None, alpha=None, dash=None):
        s = f'<a:xfrm><a:off x="{_e(x)}" y="{_e(y)}"/><a:ext cx="{_e(w)}" cy="{_e(h)}"/></a:xfrm>'
        if geom == 'roundRect' and radius is not None:
            adj = int(radius * 100000)
            s += f'<a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val {adj}"/></a:avLst></a:prstGeom>'
        else:
            s += f'<a:prstGeom prst="{geom}"><a:avLst/></a:prstGeom>'
        if fill:
            if alpha is not None:
                s += f'<a:solidFill><a:srgbClr val="{fill}"><a:alpha val="{int(alpha*1000)}"/></a:srgbClr></a:solidFill>'
            else:
                s += f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>'
        else:
            s += '<a:noFill/>'
        if line:
            d = f'<a:prstDash val="{dash}"/>' if dash else ''
            s += (f'<a:ln w="{int(lw*12700)}" cap="flat" cmpd="sng" algn="ctr">'
                  f'<a:solidFill><a:srgbClr val="{line}"/></a:solidFill>{d}</a:ln>')
        else:
            s += '<a:ln><a:noFill/></a:ln>'
        return f'<p:spPr>{s}</p:spPr>'

    def shape(self, x, y, w, h, geom='rect', fill=None, line=None, lw=1.5,
              radius=None, paras=None, anchor='ctr', label='Shape',
              lIns=0.10, rIns=0.10, tIns=0.05, bIns=0.05, alpha=None,
              dash=None, wrap=True, text_for_lint=None, pt_for_lint=None,
              line_pct_for_lint=100, space_for_lint=0, npara_for_lint=1,
              pt_is_final=False):
        sid, nm = self._next(label)
        body = paras or [_para_xml([run('', 12, WHITE)])]
        tf = (f'<p:txBody><a:bodyPr wrap="{"square" if wrap else "none"}" '
              f'lIns="{_e(lIns)}" tIns="{_e(tIns)}" rIns="{_e(rIns)}" bIns="{_e(bIns)}" '
              f'rtlCol="0" anchor="{anchor}"><a:noAutofit/></a:bodyPr>'
              f'<a:lstStyle/>{"".join(body)}</p:txBody>')
        self._sp.append({
            'y': y, 'h': h, 'kind': 'sp',
            'head': f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="{nm}"/>'
                    f'<p:cNvSpPr/><p:nvPr/></p:nvSpPr>',
            'geo': dict(x=x, w=w, geom=geom, fill=fill, line=line, lw=lw,
                        radius=radius, alpha=alpha, dash=dash),
            'tail': tf + '</p:sp>', 'g': self._cur_grp})
        if text_for_lint is not None:
            # content files quote author sizes; SCALE is what actually ships
            if not pt_is_final:
                pt_for_lint = max(PT_MIN, SCALE.get(pt_for_lint,
                                                    pt_for_lint or 12))
            self.records.append([nm, x, y, w, h, geom, text_for_lint,
                                 pt_for_lint, lIns + rIns,
                                 line_pct_for_lint, space_for_lint,
                                 npara_for_lint, tIns + bIns, True])
        else:
            self.records.append([nm, x, y, w, h, geom, '', 0, 0, 100, 0, 1, 0,
                                 bool(fill or line)])
        self._sp[-1]['rec'] = len(self.records) - 1
        return self

    def textbox(self, x, y, w, h, lines, anchor='t', align='l', label='Text',
                line_pct=100, space=0, lIns=0.08, rIns=0.08, tIns=0.05,
                bIns=0.05, fit=True, max_pt=PT_MAX, max_line_pct=132):
        """A text box whose type size is decided at render time, so a
        grow-to-fit pass can resize the box first."""
        sid, nm = self._next(label)
        self._sp.append({
            'y': y, 'h': h, 'kind': 'txt',
            'head': f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="{nm}"/>'
                    f'<p:cNvSpPr/><p:nvPr/></p:nvSpPr>',
            'geo': dict(x=x, w=w, geom='rect', fill=None, line=None, lw=1.5,
                        radius=None, alpha=None, dash=None),
            'txt': dict(lines=lines, anchor=anchor, align=align,
                        line_pct=line_pct, space=space, lIns=lIns, rIns=rIns,
                        tIns=tIns, bIns=bIns, fit=fit, max_pt=max_pt,
                        max_line_pct=max_line_pct),
            'tail': '', 'g': self._cur_grp})
        self.records.append([nm, x, y, w, h, 'rect', '', PT_MIN,
                             lIns + rIns, line_pct, space, len(lines),
                             tIns + bIns, True])
        self._sp[-1]['rec'] = len(self.records) - 1
        return self

    def _finalize(self):
        """Resolve every deferred text box against its current geometry."""
        for r in self._sp:
            if r['kind'] != 'txt':
                continue
            t = r['txt']
            lines, lp, sp = t['lines'], t['line_pct'], t['space']
            if t['fit']:
                lines, lp, sp = autofit(
                    lines, r['geo']['w'] - t['lIns'] - t['rIns'],
                    r['h'] - t['tIns'] - t['bIns'], t['line_pct'], t['space'],
                    t['max_pt'], t['max_line_pct'])
            paras = [_para_xml(rs, align=t['align'], line_pct=lp,
                               space_before=(sp if i else 0))
                     for i, rs in enumerate(lines)]
            r['tail'] = (
                f'<p:txBody><a:bodyPr wrap="square" lIns="{_e(t["lIns"])}" '
                f'tIns="{_e(t["tIns"])}" rIns="{_e(t["rIns"])}" '
                f'bIns="{_e(t["bIns"])}" rtlCol="0" anchor="{t["anchor"]}">'
                f'<a:noAutofit/></a:bodyPr><a:lstStyle/>'
                f'{"".join(paras)}</p:txBody></p:sp>')
            rec = self.records[r['rec']]
            rec[2], rec[4] = r['y'], r['h']
            rec[6] = '\n'.join(''.join(x['t'] for x in rs) for rs in lines)
            rec[7] = max((x['sz'] for rs in lines for x in rs), default=PT_MIN)
            rec[9], rec[10], rec[11] = lp, sp, len(lines)
        return self

    def picture(self, src_path, x, y, w, h, label='Art'):
        """A generated illustration. `src_path` is an absolute path on disk;
        the packager copies it into ppt/media and wires the relationship."""
        sid, nm = self._next(label)
        rid = f'rIdImg{len(self.pictures) + 1}'
        self.pictures.append((rid, src_path))
        self._sp.append({'y': y, 'h': h, 'kind': 'pic', 'fixed': True,
            'head': f'<p:pic><p:nvPicPr><p:cNvPr id="{sid}" name="{nm}"/>'
                    f'<p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr>'
                    f'<p:nvPr/></p:nvPicPr>'
                    f'<p:blipFill><a:blip r:embed="{rid}"/>'
                    f'<a:stretch><a:fillRect/></a:stretch></p:blipFill><p:spPr>',
            'xy': (x, w, h),
            'tail': '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
                    '</p:spPr></p:pic>'})
        self.records.append([nm, x, y, w, h, 'pic', '', 0, 0, 100, 0, 1, 0, True])
        return self

    # ---- speaker notes ---------------------------------------------
    def notes(self, *paragraphs):
        """备注 — content that belongs to the trainer, not to the screen."""
        self.notes_text = [p for p in paragraphs if p]
        return self

    def line(self, x, y, w, h, color=WHITE, lw=1.0, alpha=None, dash=None):
        sid, nm = self._next('Connector')
        fl = (f'<a:solidFill><a:srgbClr val="{color}">'
              + (f'<a:alpha val="{int(alpha*1000)}"/>' if alpha is not None else '')
              + '</a:srgbClr></a:solidFill>')
        d = f'<a:prstDash val="{dash}"/>' if dash else ''
        self._sp.append({'y': y, 'h': h, 'kind': 'cxn', 'fixed': True,
            'head': f'<p:cxnSp><p:nvCxnSpPr><p:cNvPr id="{sid}" name="{nm}"/>'
                    f'<p:cNvCxnSpPr/><p:nvPr/></p:nvCxnSpPr><p:spPr>',
            'xy': (x, w, h),
            'tail': f'<a:prstGeom prst="line"><a:avLst/></a:prstGeom>'
                    f'<a:ln w="{int(lw*12700)}" cap="flat">{fl}{d}</a:ln></p:spPr></p:cxnSp>'})
        return self

    def arrow(self, x, y, w, color=WHITE, lw=2.0):
        sid, nm = self._next('Arrow')
        self._sp.append({'y': y, 'h': 0, 'kind': 'cxn',
            'head': f'<p:cxnSp><p:nvCxnSpPr><p:cNvPr id="{sid}" name="{nm}"/>'
                    f'<p:cNvCxnSpPr/><p:nvPr/></p:nvCxnSpPr><p:spPr>',
            'xy': (x, w, 0),
            'tail': f'<a:prstGeom prst="straightConnector1"><a:avLst/></a:prstGeom>'
                    f'<a:ln w="{int(lw*12700)}" cap="flat">'
                    f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
                    f'<a:tailEnd type="triangle" w="med" len="med"/></a:ln></p:spPr></p:cxnSp>'})
        return self

    def _render(self, r):
        if r['kind'] == 'txt':
            g = r['geo']
            return (r['head'] + self._spPr(g['x'], r['y'], g['w'], r['h'])
                    + r['tail'])
        if r['kind'] == 'pic':
            x, w, h = r['xy']
            return (r['head'] +
                    f'<a:xfrm><a:off x="{_e(x)}" y="{_e(r["y"])}"/>'
                    f'<a:ext cx="{_e(w)}" cy="{_e(h)}"/></a:xfrm>' + r['tail'])
        if r['kind'] == 'cxn':
            x, w, h = r['xy']
            return (r['head'] +
                    f'<a:xfrm><a:off x="{_e(x)}" y="{_e(r["y"])}"/>'
                    f'<a:ext cx="{_e(w)}" cy="{_e(h)}"/></a:xfrm>' + r['tail'])
        g = r['geo']
        return (r['head'] + self._spPr(g['x'], r['y'], g['w'], r['h'],
                                       g['geom'], g['fill'], g['line'], g['lw'],
                                       g['radius'], g['alpha'], g['dash'])
                + r['tail'])

    def reflow(self, top=2.14, bottom=7.16, gap=0.085, enabled=False):
        if not enabled:
            return self
        """Compact content vertically: units (atomic groups or single shapes)
        are collected into rows by top-alignment, rows are flowed top-down."""
        idx = [i for i, r in enumerate(self._sp)
               if r['y'] >= 2.02 and not r.get('fixed')]
        if not idx:
            return self
        units = {}                       # key -> [top, bottom, [idx...]]
        for i in idx:
            r = self._sp[i]
            key = ('g', r.get('g')) if r.get('g') else ('s', i)
            u = units.setdefault(key, [r['y'], r['y'] + r['h'], []])
            u[0] = min(u[0], r['y'])
            u[1] = max(u[1], r['y'] + r['h'])
            u[2].append(i)
        rows = []
        for u in sorted(units.values(), key=lambda v: v[0]):
            for rw in rows:
                if abs(rw[0] - u[0]) < 0.22:
                    rw[0] = min(rw[0], u[0]); rw[1] = max(rw[1], u[1])
                    rw[2].extend(u[2]); break
            else:
                rows.append([u[0], u[1], list(u[2])])
        rows.sort(key=lambda r: r[0])
        shift = top - rows[0][0]
        prev_bottom = None
        for rw in rows:
            y0 = rw[0] + shift
            if prev_bottom is not None and y0 < prev_bottom + gap:
                shift += (prev_bottom + gap) - y0
                y0 = rw[0] + shift
            for i in rw[2]:
                self._sp[i]['y'] += shift
                if 'rec' in self._sp[i]:
                    self.records[self._sp[i]['rec']][2] += shift
                    self.records[self._sp[i]['rec']][4] = self._sp[i]['h']
            prev_bottom = rw[1] + shift
        return self

    def xml(self):
        self._finalize()
        return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
                '<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
                'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
                'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
                '<p:cSld><p:spTree><p:nvGrpSpPr>'
                '<p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
                '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
                '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
                + ''.join(self._render(r) for r in self._sp) +
                '</p:spTree></p:cSld><p:clrMapOvr><a:overrideClrMapping '
                'bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" '
                'accent2="accent2" accent3="accent3" accent4="accent4" '
                'accent5="accent5" accent6="accent6" hlink="hlink" '
                'folHlink="folHlink"/></p:clrMapOvr></p:sld>')


# ---------------------------------------------------------------- text helper
def text(sl, x, y, w, h, lines, anchor='t', align='l', label='Text',
         line_pct=100, space=0, lIns=0.08, rIns=0.08, tIns=0.05, bIns=0.05,
         fit=True, unwrap_paragraphs=True, max_pt=PT_MAX, max_line_pct=132):
    """lines: list of list-of-run (each inner list = one paragraph).
    By default the text is unwrapped (no hand breaks mid-sentence) and then
    grown to fill the box without overflowing."""
    if unwrap_paragraphs:
        lines = unwrap_paras(lines)
    return sl.textbox(x, y, w, h, lines, anchor=anchor, align=align,
                      label=label, line_pct=line_pct, space=space,
                      lIns=lIns, rIns=rIns, tIns=tIns, bIns=bIns, fit=fit,
                      max_pt=max_pt, max_line_pct=max_line_pct)


def label_paras(lines, align='ctr', avail_w=1.0, avail_h=1.0, line_pct=100,
                max_pt=PT_MAX, fit=True):
    """Autofit helper for the label text that lives directly on a filled
    shape (card headers, nav chips, bars). Returns (paras, pt, line_pct)."""
    if fit:
        lines, line_pct, _ = autofit(lines, avail_w, avail_h, line_pct, 0,
                                     max_pt, max(line_pct, 100))
    pt = max((r['sz'] for rs in lines for r in rs), default=12)
    flat = '\n'.join(''.join(r['t'] for r in rs) for rs in lines)
    return ([_para_xml(rs, align=align, line_pct=line_pct) for rs in lines],
            pt, line_pct, flat, len(lines))
