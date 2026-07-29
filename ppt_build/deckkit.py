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


# ---------------------------------------------------------------- runs
# Author sizes are written on a compact scale; SCALE lifts every one of them
# into the 16–24pt band the client asked for.
SCALE = {11: 16, 12: 16, 13: 16, 14: 17, 15: 18, 16: 19, 17: 20,
         20: 21, 22: 23, 24: 24, 25: 25, 26: 26, 34: 32, 40: 38}


def run(text, pt, color=INK, bold=True, italic=False):
    """One <a:r>. `text` may contain \n only via separate paragraphs."""
    return {'t': str(text), 'sz': SCALE.get(pt, pt), 'c': color,
            'b': bold, 'i': italic}


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
        self.records = []           # (label, x, y, w, h, kind, text, pt)

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
              dash=None, wrap=True, text_for_lint=None, pt_for_lint=None):
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
            self.records.append([nm, x, y, w, h, geom, text_for_lint,
                                 pt_for_lint or 12, lIns + rIns])
        else:
            self.records.append([nm, x, y, w, h, geom, '', 0, 0])
        self._sp[-1]['rec'] = len(self.records) - 1
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
         line_pct=100, space=0, lIns=0.08, rIns=0.08):
    """lines: list of list-of-run (each inner list = one paragraph)."""
    paras = [_para_xml(rs, align=align, line_pct=line_pct,
                       space_before=(space if i else 0))
             for i, rs in enumerate(lines)]
    flat = '\n'.join(''.join(r['t'] for r in rs) for rs in lines)
    pt = max((r['sz'] for rs in lines for r in rs), default=12)
    return sl.shape(x, y, w, h, 'rect', None, None, paras=paras, anchor=anchor,
                    label=label, lIns=lIns, rIns=rIns,
                    text_for_lint=flat, pt_for_lint=pt)
