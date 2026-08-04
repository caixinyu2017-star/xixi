"""A small LaTeX-subset -> OMML converter built on omml.py primitives.

Supports: Greek letters, sub/superscripts (_{} ^{}), \\frac, \\sqrt[n]{}, \\hat, \\bar,
\\text{}, \\sum_{}^{} (n-ary), \\ln \\log \\exp, operators (\\times \\cdot \\leq \\geq
\\neq \\approx \\pm \\prime \\in \\sim), delimiters via \\left( \\right) or plain ( ) [ ] | .
Produces a list of OMML elements suitable for omml.omath(...) or omml.add_numbered_equation.
"""
import re
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

GREEK = {
    'alpha': 'α', 'beta': 'β', 'gamma': 'γ', 'delta': 'δ', 'epsilon': 'ε',
    'varepsilon': 'ε', 'zeta': 'ζ', 'eta': 'η', 'theta': 'θ', 'vartheta': 'ϑ',
    'iota': 'ι', 'kappa': 'κ', 'lambda': 'λ', 'mu': 'μ', 'nu': 'ν', 'xi': 'ξ',
    'pi': 'π', 'rho': 'ρ', 'sigma': 'σ', 'tau': 'τ', 'upsilon': 'υ', 'phi': 'φ',
    'varphi': 'φ', 'chi': 'χ', 'psi': 'ψ', 'omega': 'ω',
    'Gamma': 'Γ', 'Delta': 'Δ', 'Theta': 'Θ', 'Lambda': 'Λ', 'Xi': 'Ξ',
    'Pi': 'Π', 'Sigma': 'Σ', 'Phi': 'Φ', 'Psi': 'Ψ', 'Omega': 'Ω',
}
OPS = {
    'times': '×', 'cdot': '·', 'leq': '≤', 'le': '≤', 'geq': '≥', 'ge': '≥',
    'neq': '≠', 'approx': '≈', 'pm': '±', 'prime': '′', 'in': '∈', 'sim': '∼',
    'rightarrow': '→', 'to': '→', 'cdots': '⋯', 'ldots': '…', 'infty': '∞',
    'partial': '∂', 'nabla': '∇', 'circ': '∘', 'ast': '∗', 'perp': '⊥',
}
FUNCS = {'ln', 'log', 'exp', 'max', 'min', 'sin', 'cos', 'tan', 'Cov', 'Var', 'Corr', 'Prob'}


def _m(tag):
    return OxmlElement('m:' + tag)


def _run(text, upright=False):
    r = _m('r')
    if upright:
        rpr = _m('rPr'); s = _m('sty'); s.set(qn('m:val'), 'p'); rpr.append(s); r.append(rpr)
    t = _m('t'); t.set(qn('xml:space'), 'preserve'); t.text = text; r.append(t)
    return r


def _slot(tag, kids):
    n = _m(tag)
    for k in kids:
        n.append(k)
    return n


class Tok:
    def __init__(self, s):
        self.s = s
        self.i = 0
        self.n = len(s)

    def peek(self):
        return self.s[self.i] if self.i < self.n else ''

    def getc(self):
        c = self.s[self.i]; self.i += 1; return c

    def read_command(self):
        # backslash already consumed
        m = re.match(r'[A-Za-z]+', self.s[self.i:])
        if m:
            name = m.group(0); self.i += len(name); return name
        else:
            c = self.getc(); return c  # escaped symbol like \{ \_ \%

    def read_group(self):
        # expects current char '{'
        assert self.getc() == '{'
        depth = 1; start = self.i
        while self.i < self.n and depth > 0:
            c = self.s[self.i]
            if c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0:
                    break
            self.i += 1
        inner = self.s[start:self.i]
        self.getc()  # consume '}'
        return inner


def _atom(t):
    """Read a single atom (no sub/sup handling): returns list of OMML elems."""
    c = t.peek()
    if c == '\\':
        t.getc()
        name = t.read_command()
        if name == 'frac':
            num = parse(t.read_group()); den = parse(t.read_group())
            f = _m('f'); f.append(_slot('num', num)); f.append(_slot('den', den)); return [f]
        if name == 'dfrac':
            num = parse(t.read_group()); den = parse(t.read_group())
            f = _m('f'); f.append(_slot('num', num)); f.append(_slot('den', den)); return [f]
        if name == 'sqrt':
            deg = None
            if t.peek() == '[':
                t.getc(); start = t.i
                while t.peek() != ']':
                    t.getc()
                degtxt = t.s[start:t.i]; t.getc(); deg = parse(degtxt)
            rad = parse(t.read_group())
            r = _m('rad'); pr = _m('radPr'); dh = _m('degHide')
            dh.set(qn('m:val'), '1' if deg is None else '0'); pr.append(dh); r.append(pr)
            r.append(_slot('deg', deg or [])); r.append(_slot('e', rad)); return [r]
        if name in ('big', 'Big', 'bigg', 'Bigg', 'bigl', 'Bigl', 'bigr', 'Bigr'):
            return []
        if name in (',', ';', ':', '!', 'quad', 'qquad', 'thinspace'):
            return [_run(' ' if name in (',', ';', ':') else '  ')]
        if name in ('hat', 'bar', 'tilde', 'vec', 'dot', 'overline',
                    'widehat', 'widetilde'):
            base = parse(t.read_group())
            chr_map = {'hat': '̂', 'bar': '̅', 'overline': '̅', 'tilde': '̃',
                       'vec': '⃗', 'dot': '̇', 'widehat': '̂', 'widetilde': '̃'}
            if name in ('bar', 'overline'):
                b = _m('bar'); pr = _m('barPr'); pos = _m('pos'); pos.set(qn('m:val'), 'top')
                pr.append(pos); b.append(pr); b.append(_slot('e', base)); return [b]
            a = _m('acc'); pr = _m('accPr'); ch = _m('chr'); ch.set(qn('m:val'), chr_map[name])
            pr.append(ch); a.append(pr); a.append(_slot('e', base)); return [a]
        if name == 'text' or name == 'mathrm' or name == 'operatorname':
            inner = t.read_group(); return [_run(inner, upright=True)]
        if name == 'sum' or name == 'prod' or name == 'int':
            chrmap = {'sum': '∑', 'prod': '∏', 'int': '∫'}
            sub = sup = None
            while t.peek() in ('_', '^'):
                which = t.getc()
                grp = t.read_group() if t.peek() == '{' else t.getc()
                if which == '_':
                    sub = parse(grp)
                else:
                    sup = parse(grp)
            nary = _m('nary'); pr = _m('naryPr')
            ch = _m('chr'); ch.set(qn('m:val'), chrmap[name]); pr.append(ch)
            ll = _m('limLoc'); ll.set(qn('m:val'), 'subSup'); pr.append(ll)
            if sub is None:
                sh = _m('subHide'); sh.set(qn('m:val'), '1'); pr.append(sh)
            if sup is None:
                sph = _m('supHide'); sph.set(qn('m:val'), '1'); pr.append(sph)
            # a braced group immediately after the limits bounds the operand;
            # otherwise the remainder of the stream is taken
            while t.peek() == ' ':
                t.getc()
            if t.peek() == '{':
                operand = parse(t.read_group())
            else:
                operand_text = t.s[t.i:]
                t.i = t.n
                operand = parse(operand_text) if operand_text.strip() else []
            nary.append(pr)
            nary.append(_slot('sub', sub or []))
            nary.append(_slot('sup', sup or []))
            nary.append(_slot('e', operand))
            return [nary]
        if name == 'left':
            # read delimiter char
            lc = t.getc()
            # read until matching \right
            depth = 1; buf = ''
            while t.i < t.n:
                if t.s[t.i:t.i+6] == '\\left ' or t.s[t.i:t.i+5] == '\\left':
                    pass
                if t.s[t.i:t.i+6] == '\\right':
                    t.i += 6; rc = t.getc(); depth -= 1
                    if depth == 0:
                        break
                    else:
                        buf += '\\right' + rc; continue
                if t.s[t.i:t.i+5] == '\\left':
                    depth += 1; buf += t.s[t.i:t.i+5]; t.i += 5; continue
                buf += t.s[t.i]; t.i += 1
            inner = parse(buf)
            lc = '' if lc == '.' else lc
            rc = '' if rc == '.' else rc
            d = _m('d'); pr = _m('dPr')
            bc = _m('begChr'); bc.set(qn('m:val'), lc); pr.append(bc)
            ec = _m('endChr'); ec.set(qn('m:val'), rc); pr.append(ec)
            d.append(pr); d.append(_slot('e', inner)); return [d]
        if name in GREEK:
            return [_run(GREEK[name])]
        if name in OPS:
            return [_run(OPS[name], upright=True)]
        if name in FUNCS:
            return [_run(name, upright=True)]
        if name == ',' or name == ';' or name == ' ' or name == '!' or name == 'quad' or name == 'qquad':
            return [_run(' ')]
        # unknown command: render literally without backslash
        return [_run(name)]
    if c == '{':
        return parse(t.read_group())
    if c == '(' or c == ')' or c == '[' or c == ']' or c == '|':
        t.getc(); return [_run(c, upright=True)]
    # default: accumulate a multi-letter identifier so names like YEMP are one run
    if c.isalpha():
        j = t.i
        while j < t.n and t.s[j].isalnum():
            j += 1
        word = t.s[t.i:j]
        t.i = j
        # Avoid collisions with LibreOffice-Math reserved keywords (rendering only;
        # Word treats the run identically). Split into two runs so the bare token is hidden.
        _LO_KW = {'size', 'color', 'font', 'left', 'right', 'sqrt', 'sum', 'int', 'prod',
                  'times', 'over', 'sup', 'sub', 'lim', 'abs', 'func', 'matrix', 'stack',
                  'bold', 'italic', 'align', 'phantom', 'binom', 'nroot', 'widevec', 'lint'}
        if len(word) > 1 and word.lower() in _LO_KW:
            return [_run(word[0]), _run(word[1:])]
        return [_run(word)]
    if c.isdigit():
        j = t.i
        while j < t.n and (t.s[j].isdigit() or t.s[j] == '.'):
            j += 1
        num = t.s[t.i:j]
        t.i = j
        return [_run(num, upright=True)]
    t.getc()
    if c.isspace():
        return [_run(' ')]
    if c in '+-=<>/.,:;':
        return [_run(c, upright=(c in '+-=<>/'))]
    return [_run(c)]


def parse(s):
    """Parse a LaTeX-subset string into a list of OMML elements."""
    t = Tok(s)
    out = []
    while t.i < t.n:
        c = t.peek()
        if c == '^' or c == '_':
            # attach to previous atom
            base = out.pop() if out else _run('')
            sub = None; sup = None
            while t.peek() in ('_', '^'):
                which = t.getc()
                if t.peek() == '{':
                    grp = t.read_group()
                elif t.peek() == '\\':
                    # command as script
                    save = t.i; t.getc(); nm = t.read_command()
                    grp = '\\' + nm
                else:
                    grp = t.getc()
                if which == '_':
                    sub = parse(grp)
                else:
                    sup = parse(grp)
            if sub is not None and sup is not None:
                node = _m('sSubSup'); node.append(_slot('e', [base]))
                node.append(_slot('sub', sub)); node.append(_slot('sup', sup))
            elif sub is not None:
                node = _m('sSub'); node.append(_slot('e', [base])); node.append(_slot('sub', sub))
            else:
                node = _m('sSup'); node.append(_slot('e', [base])); node.append(_slot('sup', sup))
            out.append(node)
        else:
            out.extend(_atom(t))
    return out


def L(s):
    """Public: LaTeX subset -> list of OMML elements."""
    return parse(s)
