"""Build native Word equations (OMML) for the revised manuscript.

Every mathematical expression added during the revision must be a Word
equation-editor object, not styled text.  This module builds OMML fragments
programmatically and inserts them into a paragraph, either inline or as a
centred display equation.

The 129 OMML equations already present in the submitted file are left
untouched; this only supplies the new ones.
"""
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn

_NS = nsdecls('m', 'w')


# --------------------------------------------------------------- primitives
def _esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;')
            .replace('>', '&gt;'))


def r(text, italic=True):
    """A math run.  Variables are italic, operators and digits upright."""
    pr = '' if italic else '<m:rPr><m:sty m:val="p"/></m:rPr>'
    return f'<m:r>{pr}<m:t xml:space="preserve">{_esc(text)}</m:t></m:r>'


def op(text):
    """An upright operator or punctuation run."""
    return r(text, italic=False)


def num(text):
    return r(text, italic=False)


def sub(base, s):
    return f'<m:sSub><m:e>{base}</m:e><m:sub>{s}</m:sub></m:sSub>'


def sup(base, s):
    return f'<m:sSup><m:e>{base}</m:e><m:sup>{s}</m:sup></m:sSup>'


def subsup(base, sb, sp):
    return (f'<m:sSubSup><m:e>{base}</m:e><m:sub>{sb}</m:sub>'
            f'<m:sup>{sp}</m:sup></m:sSubSup>')


def frac(n, d):
    return f'<m:f><m:num>{n}</m:num><m:den>{d}</m:den></m:f>'


def delim(inner, beg='(', end=')'):
    return (f'<m:d><m:dPr><m:begChr m:val="{beg}"/><m:endChr m:val="{end}"/>'
            f'<m:ctrlPr/></m:dPr><m:e>{inner}</m:e></m:d>')


def abs_(inner):
    return delim(inner, '|', '|')


def rad(inner, degree=None):
    if degree is None:
        return (f'<m:rad><m:radPr><m:degHide m:val="1"/><m:ctrlPr/></m:radPr>'
                f'<m:deg/><m:e>{inner}</m:e></m:rad>')
    return (f'<m:rad><m:radPr><m:ctrlPr/></m:radPr><m:deg>{degree}</m:deg>'
            f'<m:e>{inner}</m:e></m:rad>')


def nary(chr_, lower, upper, body):
    """Big operator (sum, product) with limits."""
    return (f'<m:nary><m:naryPr><m:chr m:val="{chr_}"/>'
            f'<m:limLoc m:val="undOvr"/><m:ctrlPr/></m:naryPr>'
            f'<m:sub>{lower}</m:sub><m:sup>{upper}</m:sup>'
            f'<m:e>{body}</m:e></m:nary>')


def func(name, arg):
    """A named function such as min or max applied to an argument."""
    return (f'<m:func><m:funcPr><m:ctrlPr/></m:funcPr>'
            f'<m:fName>{op(name)}</m:fName><m:e>{arg}</m:e></m:func>')


def joined(*parts):
    return ''.join(parts)


# ----------------------------------------------------------------- insertion
def inline(paragraph, omml_body, before=None):
    """Append an inline equation to `paragraph` (or insert before an element)."""
    el = parse_xml(f'<m:oMath {_NS}>{omml_body}</m:oMath>')
    if before is not None:
        before.addprevious(el)
    else:
        paragraph._p.append(el)
    return el


def display(paragraph, omml_body):
    """Turn `paragraph` into a centred display equation."""
    el = parse_xml(f'<m:oMathPara {_NS}>'
                   f'<m:oMathParaPr><m:jc m:val="center"/></m:oMathParaPr>'
                   f'<m:oMath>{omml_body}</m:oMath></m:oMathPara>')
    paragraph._p.append(el)
    return el


def para_with_math(paragraph, pieces, color=None):
    """Fill a paragraph with alternating text and equations.

    `pieces` is a sequence of strings (plain text) and ('math', omml) tuples,
    so a sentence can carry real Word equations inside it.
    """
    from docx_edit import COLORS
    for p in pieces:
        if isinstance(p, tuple) and p and p[0] == 'math':
            inline(paragraph, p[1])
        else:
            run = paragraph.add_run(str(p))
            if color:
                run.font.color.rgb = COLORS[color]
    return paragraph


# =========================================================================
#  The equations added by this revision
# =========================================================================
_x, _o, _k, _h = r('x'), r('o'), r('k'), r('h')
_j = r('j')
XJ = sub(_x, _j)
OJ = sub(_o, _j)
XSTAR = sup(sub(_x, _j), op('*'))
HSTAR = sup(_h, op('*'))
LBJ = sub(r('lb'), _j)
UBJ = sub(r('ub'), _j)


def eq_similar_triangles():
    """h / h* = (x_j - o_j) / (o_j - x*_j) = k"""
    return joined(frac(_h, HSTAR), op(' = '),
                  frac(joined(XJ, op(' − '), OJ),
                       joined(OJ, op(' − '), XSTAR)),
                  op(' = '), _k)


def eq_lens_solved():
    """x*_j = o_j + (o_j - x_j) / k"""
    return joined(XSTAR, op(' = '), OJ, op(' + '),
                  frac(joined(OJ, op(' − '), XJ), _k))


def eq_midpoint():
    """o_j = (lb_j + ub_j) / 2"""
    return joined(OJ, op(' = '), frac(joined(LBJ, op(' + '), UBJ), num('2')))


def eq_contraction():
    """|x*_j - o_j| = |x_j - o_j| / k"""
    return joined(abs_(joined(XSTAR, op(' − '), OJ)), op(' = '),
                  frac(abs_(joined(XJ, op(' − '), OJ)), _k))


def eq_k_schedule():
    """k(t) = (1 + (t/T)^nu)^mu"""
    t, T = r('t'), r('T')
    nu, mu = r('ν'), r('μ')
    return joined(_k, delim(t), op(' = '),
                  sup(delim(joined(num('1'), op(' + '),
                                   sup(delim(frac(t, T)), nu))), mu))


def eq_obl_special():
    """k = 1  =>  x*_j = lb_j + ub_j - x_j"""
    return joined(_k, op(' = '), num('1'), op('  ⇒  '), XSTAR, op(' = '),
                  LBJ, op(' + '), UBJ, op(' − '), XJ)


def eq_diversity():
    """DIV = 2 / (K(K-1)) * sum_{i<j} d(h_i, h_j) / 180"""
    K, i, d, h = r('K'), r('i'), r('d'), r('h')
    body = frac(joined(d, delim(joined(sub(h, i), op(', '), sub(h, _j)))),
                num('180'))
    return joined(op('DIV'), op(' = '),
                  frac(num('2'), joined(K, delim(joined(K, op(' − '), num('1'))))),
                  nary('∑', joined(i, op(' < '), _j), '', body))


def eq_contrast():
    """CON = min(1, (max_i v_i - min_i v_i) / 0.6)"""
    v, i = r('v'), r('i')
    inner = frac(joined(sub(op('max'), i), sub(v, i), op(' − '),
                        sub(op('min'), i), sub(v, i)), num('0.6'))
    return joined(op('CON'), op(' = '),
                  func('min', delim(joined(num('1'), op(', '), inner))))


def eq_palette_objective():
    """f(P) = w_har HAR(P) + w_div DIV(P) + w_con CON(P)"""
    f, P, w = r('f'), r('P'), r('w')
    return joined(f, delim(P), op(' = '), sub(w, op('har')), op(' HAR'), delim(P),
                  op(' + '), sub(w, op('div')), op(' DIV'), delim(P),
                  op(' + '), sub(w, op('con')), op(' CON'), delim(P))


def eq_acgm_weights():
    """lambda_1 = 1 - t^2/T^2,  lambda_2 = t^2/T^2"""
    lam, t, T = r('λ'), r('t'), r('T')
    t2 = sup(t, num('2'))
    T2 = sup(T, num('2'))
    return joined(sub(lam, num('1')), op(' = '), num('1'), op(' − '),
                  frac(t2, T2), op(',   '),
                  sub(lam, num('2')), op(' = '), frac(t2, T2))


def eq_lobl_subset():
    """N_min = 0.2 N"""
    N = r('N')
    return joined(sub(N, op('min')), op(' = '), num('0.2'), N)


def eq_kT():
    """k(T) = 2^mu"""
    T, mu = r('T'), r('μ')
    return joined(_k, delim(T), op(' = '), sup(num('2'), mu))
