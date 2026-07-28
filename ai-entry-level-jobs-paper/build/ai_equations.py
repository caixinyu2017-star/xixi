# -*- coding: utf-8 -*-
"""Display equations of the job-ladder model, written as native Word OMML."""
import os
import sys

_YSTS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "..", "..",
                                     "zhejiang-youth-systems-paper", "build"))
if _YSTS not in sys.path:
    sys.path.insert(0, _YSTS)

from mdpi_builder import mr, msub, msup, mfrac, mdelim, omath   # noqa: E402


def _sp():
    return mr(' ')


def _op(op):
    return _sp() + mr(op, upright=True) + _sp()


def _up(t):
    return mr(t, upright=True)


def _dot(base):
    return ('<m:acc><m:accPr><m:chr m:val="̇"/></m:accPr>'
            f'<m:e>{base}</m:e></m:acc>')


def _bar(base):
    return ('<m:bar><m:barPr><m:pos m:val="top"/></m:barPr>'
            f'<m:e>{base}</m:e></m:bar>')


def _fn(name, arg):
    return _up(name) + mdelim(arg)


def _prime(base):
    return base + mr('′', upright=True)


def msubsup_N():
    """The Nash-bargained entry wage, w_j^N."""
    return ('<m:sSubSup><m:sSubSupPr/><m:e>' + mr('w') + '</m:e>'
            '<m:sub>' + mr('j') + '</m:sub>'
            '<m:sup>' + mr('N', upright=True) + '</m:sup></m:sSubSup>')


# short-hands ---------------------------------------------------------------
r_ = mr('r')
w_ = mr('ω')
dj = msub(mr('δ'), mr('j'))
ds = msub(mr('δ'), mr('s'))
ph = mr('φ')
pi_ = mr('π')
m_ = mr('m')
eta = mr('η')
beta = mr('β')
uj, ej, us, es = (msub(mr('u'), mr('j')), msub(mr('e'), mr('j')),
                  msub(mr('u'), mr('s')), msub(mr('e'), mr('s')))
fj, fs = msub(mr('f'), mr('j')), msub(mr('f'), mr('s'))
qj, qs = msub(mr('q'), mr('j')), msub(mr('q'), mr('s'))
thj, ths = msub(mr('θ'), mr('j')), msub(mr('θ'), mr('s'))
Fj, Fs = msub(mr('F'), mr('j')), msub(mr('F'), mr('s'))
Xj, Xs = msub(mr('X'), mr('j')), msub(mr('X'), mr('s'))
Jj, Js = msub(mr('J'), mr('j')), msub(mr('J'), mr('s'))
Wj, Ws = msub(mr('W'), mr('j')), msub(mr('W'), mr('s'))
Uj, Us = msub(mr('U'), mr('j')), msub(mr('U'), mr('s'))
wj, ws = msub(mr('w'), mr('j')), msub(mr('w'), mr('s'))
cj, cs = msub(mr('c'), mr('j')), msub(mr('c'), mr('s'))
vj, vs = msub(mr('v'), mr('j')), msub(mr('v'), mr('s'))
Sj = msub(mr('S'), mr('j'))
lam_uj = msub(mr('λ'), msub(mr('u'), mr('j')))
lam_ej = msub(mr('λ'), msub(mr('e'), mr('j')))
lam_us = msub(mr('λ'), msub(mr('u'), mr('s')))
lam_es = msub(mr('λ'), msub(mr('e'), mr('s')))
sw = msub(mr('s'), mr('w'))
sm = msub(mr('s'), mr('m'))
sv = msub(mr('s'), mr('v'))
svs = msub(mr('s'), mr('vs'))
ta = msub(mr('t'), mr('a'))
pa = msub(mr('p'), mr('a'))
Aa = mr('A')

ONE = mr('1')


# (1) matching function ------------------------------------------------------
EQ1 = omath(
    msub(mr('M'), mr('i')) + mdelim(msub(mr('u'), mr('i')) + mr(', ') +
                                    msub(mr('v'), mr('i'))) + _op('=') +
    msub(mr('μ'), mr('i')) + _sp() + msup(msub(mr('u'), mr('i')), eta) + _sp() +
    msup(msub(mr('v'), mr('i')), ONE + _op('−') + eta) + mr(', ') + _sp() +
    msub(mr('θ'), mr('i')) + _op('=') +
    mfrac(msub(mr('v'), mr('i')), msub(mr('u'), mr('i'))) + mr(', ') + _sp() +
    mr('i') + _op('∈') + mdelim(mr('j') + mr(', ') + mr('s'), '{', '}'))

# (2) transition rates -------------------------------------------------------
EQ2 = omath(
    msub(mr('f'), mr('i')) + _op('=') + msub(mr('μ'), mr('i')) + _sp() +
    msup(msub(mr('θ'), mr('i')), ONE + _op('−') + eta) + mr(', ') + _sp() +
    _sp() + msub(mr('q'), mr('i')) + _op('=') + msub(mr('μ'), mr('i')) + _sp() +
    msup(msub(mr('θ'), mr('i')), _op('−') + eta) + mr(', ') + _sp() + _sp() +
    msub(mr('f'), mr('i')) + _op('=') + msub(mr('θ'), mr('i')) + _sp() +
    msub(mr('q'), mr('i')))

# (3)-(4) stocks -------------------------------------------------------------
EQ3 = omath(
    _dot(uj) + _op('=') + w_ + _op('+') + dj + _sp() + ej + _op('−') +
    mdelim(fj + _op('+') + w_) + uj + mr(', ') + _sp() + _sp() +
    _dot(ej) + _op('=') + fj + _sp() + uj + _op('−') +
    mdelim(dj + _op('+') + pi_ + _op('+') + w_) + ej)

EQ4 = omath(
    _dot(us) + _op('=') + ds + _sp() + es + _op('−') +
    mdelim(fs + _op('+') + w_) + us + mr(', ') + _sp() + _sp() +
    _dot(es) + _op('=') + pi_ + _sp() + ej + _op('+') + fs + _sp() + us +
    _op('−') + mdelim(ds + _op('+') + w_) + es)

# (5) promotion technology ---------------------------------------------------
EQ5 = omath(
    _fn('π', m_) + _op('=') + _bar(pi_) + _sp() + msup(m_, mr('ψ')) + mr(', ') +
    _sp() + _sp() + mr('0') + _op('<') + mr('ψ') + _op('<') + ONE)

# (6) task bundles -----------------------------------------------------------
EQ6 = omath(
    Xj + _op('=') + ej + _op('+') + mr('χ') + Aa + mr(', ') + _sp() + _sp() +
    Xs + _op('=') + es + _op('−') + m_ + _sp() + ej)

# (7) production -------------------------------------------------------------
EQ7 = omath(
    mr('Y') + _op('=') + mr('Z') + _sp() +
    msup(mdelim(mr('α') + _sp() + msup(Xj, mr('ρ')) + _op('+') +
                mdelim(ONE + _op('−') + mr('α')) + msup(Xs, mr('ρ')), '[', ']'),
         mfrac(mr('s'), mr('ρ'))))

# (8) marginal products ------------------------------------------------------
EQ8 = omath(
    Fj + _op('=') + mfrac(mr('∂Y'), mr('∂') + Xj) + mr(', ') + _sp() + _sp() +
    Fs + _op('=') + mfrac(mr('∂Y'), mr('∂') + Xs))

# (9) demand for AI ----------------------------------------------------------
EQ9 = omath(
    mr('χ') + _sp() + Fj + _op('=') + pa + mdelim(ONE + _op('+') + ta))

# (10) senior firm value -----------------------------------------------------
EQ10 = omath(
    mdelim(r_ + _op('+') + ds + _op('+') + w_ + _op('+') + ph) + Js + _op('=') +
    Fs + _op('−') + ws)

# (11) senior worker values --------------------------------------------------
EQ11 = omath(
    mdelim(r_ + _op('+') + ds + _op('+') + w_ + _op('+') + fs) +
    mdelim(Ws + _op('−') + Us) + _op('=') + ws + _op('−') + mr('b'))

# (12) junior firm value -----------------------------------------------------
EQ12 = omath(
    mdelim(r_ + _op('+') + dj + _op('+') + w_ + _op('+') + pi_) + Jj +
    _op('=') + Fj + _op('−') + mdelim(ONE + _op('−') + sw) + wj + _op('−') +
    mdelim(ONE + _op('−') + sm) + m_ + _sp() + Fs + _op('+') + pi_ + _sp() + Js)

# (13) junior worker values --------------------------------------------------
EQ13 = omath(
    mdelim(r_ + _op('+') + w_ + _op('+') + pi_ + _op('+') + dj) + Wj +
    _op('=') + wj + _op('+') + pi_ + _sp() + Ws + _op('+') + dj + _sp() + Uj +
    mr(', ') + _sp() + _sp() +
    mdelim(r_ + _op('+') + w_) + Uj + _op('=') + mr('b') + _op('+') + fj +
    mdelim(Wj + _op('−') + Uj))

# (14) Nash bargaining -------------------------------------------------------
EQ14 = omath(
    msub(mr('w'), mr('i')) + _op('=') + _up('arg max') + _sp() +
    msup(mdelim(msub(mr('W'), mr('i')) + _op('−') + msub(mr('U'), mr('i'))),
         beta) + _sp() + msup(msub(mr('J'), mr('i')), ONE + _op('−') + beta) +
    mr(', ') + _sp() + _sp() +
    beta + _sp() + msub(mr('J'), mr('i')) + _op('=') +
    mdelim(ONE + _op('−') + beta) +
    mdelim(msub(mr('W'), mr('i')) + _op('−') + msub(mr('U'), mr('i'))))

# (15) free entry ------------------------------------------------------------
EQ15 = omath(
    mfrac(cj + mdelim(ONE + _op('−') + sv), qj) + _op('=') + Jj + mr(', ') +
    _sp() + _sp() + mfrac(cs + mdelim(ONE + _op('−') + svs), qs) + _op('=') + Js)

# (16) mentoring first-order condition, non-contractible ---------------------
EQ16 = omath(
    _prime(pi_) + mdelim(m_) + mdelim(Js + _op('−') + Jj) + _op('=') +
    mdelim(ONE + _op('−') + sm) + Fs)

# (17) mentoring first-order condition, contractible benchmark ---------------
EQ17 = omath(
    _prime(pi_) + mdelim(m_) +
    mdelim(Js + _op('+') + Ws + _op('−') + Uj + _op('−') + Sj) + _op('=') +
    mdelim(ONE + _op('−') + sm) + Fs)

# (18) planner's objective ---------------------------------------------------
EQ18 = omath(
    _up('max') + _sp() +
    '<m:nary><m:naryPr><m:chr m:val="∫"/><m:limLoc m:val="subSup"/>'
    '<m:subHide m:val="0"/><m:supHide m:val="1"/></m:naryPr>'
    f'<m:sub>{mr("0")}</m:sub><m:sup/><m:e>' +
    msup(_up('e'), _op('−') + r_ + mr('t')) +
    mdelim(mr('Y') + _op('−') + cj + vj + _op('−') + cs + vs + _op('−') +
           pa + Aa + _op('+') + mr('b') + mdelim(uj + _op('+') + us), '[', ']') +
    _up('d') + mr('t') + '</m:e></m:nary>')

# (19) planner costates, unemployment ---------------------------------------
EQ19 = omath(
    mdelim(r_ + _op('+') + w_) + lam_uj + _op('=') + mr('b') + _op('+') + eta +
    _sp() + fj + mdelim(lam_ej + _op('−') + lam_uj) + mr(', ') + _sp() + _sp() +
    mdelim(r_ + _op('+') + w_) + lam_us + _op('=') + mr('b') + _op('+') + eta +
    _sp() + fs + mdelim(lam_es + _op('−') + lam_us))

# (20) planner costates, employment -----------------------------------------
EQ20 = omath(
    mdelim(r_ + _op('+') + dj + _op('+') + pi_ + _op('+') + w_) + lam_ej +
    _op('=') + Fj + _op('−') + m_ + Fs + _op('+') + dj + lam_uj + _op('+') +
    pi_ + lam_es + mr(', ') + _sp() + _sp() +
    mdelim(r_ + _op('+') + ds + _op('+') + w_) + lam_es + _op('=') + Fs +
    _op('+') + ds + lam_us)

# (21) planner optimality ----------------------------------------------------
EQ21 = omath(
    mdelim(ONE + _op('−') + eta) + msub(mr('q'), mr('i')) +
    mdelim(msub(mr('λ'), msub(mr('e'), mr('i'))) + _op('−') +
           msub(mr('λ'), msub(mr('u'), mr('i')))) + _op('=') +
    msub(mr('c'), mr('i')) + mr(', ') + _sp() + _sp() +
    _prime(pi_) + mdelim(m_) + mdelim(lam_es + _op('−') + lam_ej) + _op('=') + Fs)

# (22) the two wedges --------------------------------------------------------
EQ23 = omath(
    mfrac(_up('private return'), _up('social return')) + _op('=') +
    '<m:groupChr><m:groupChrPr><m:chr m:val="⏟"/><m:pos m:val="bot"/>'
    '<m:vertJc m:val="top"/></m:groupChrPr><m:e>' +
    mdelim(ONE + _op('−') + beta) +
    '</m:e></m:groupChr>' + _sp() +
    '<m:groupChr><m:groupChrPr><m:chr m:val="⏟"/><m:pos m:val="bot"/>'
    '<m:vertJc m:val="top"/></m:groupChrPr><m:e>' +
    mfrac(r_ + _op('+') + ds + _op('+') + w_,
          r_ + _op('+') + ds + _op('+') + w_ + _op('+') + ph) +
    '</m:e></m:groupChr>')

# (23) estimation criterion --------------------------------------------------
EQ22 = omath(
    _up('min') + _sp() +
    '<m:nary><m:naryPr><m:chr m:val="∑"/><m:limLoc m:val="subSup"/>'
    '</m:naryPr><m:sub>' + mr('k') + _op('=') + ONE +
    '</m:sub><m:sup>' + mr('9') + '</m:sup><m:e>' +
    msub(mr('ϖ'), mr('k')) +
    msup(mdelim(mfrac(msub(mr('m'), mr('k')) + mdelim(mr('Θ')),
                      _bar(msub(mr('m'), mr('k')))) + _op('−') + ONE),
         mr('2')) + '</m:e></m:nary>')

# (24) marginal value of public funds ---------------------------------------
EQ24 = omath(
    _up('MVPF') + _op('=') + mfrac(mr('Δ') + mr('𝒲') + _op('+') + mr('G'),
                                   mr('G')) + _op('=') + ONE + _op('+') +
    mfrac(mr('Δ') + mr('𝒲'), mr('G')))

# (25) real rigidity of the entry wage ---------------------------------------
EQ25 = omath(
    wj + _op('=') +
    msup(msubsup_N(), ONE + _op('−') + msub(mr('γ'), mr('w'))) + _sp() +
    msup(_bar(wj), msub(mr('γ'), mr('w'))) + mr(', ') + _sp() + _sp() +
    mr('0') + _op('≤') + msub(mr('γ'), mr('w')) + _op('≤') + ONE)

EQUATIONS = {
    'eq1': EQ1, 'eq2': EQ2, 'eq3': EQ3, 'eq4': EQ4, 'eq5': EQ5, 'eq6': EQ6,
    'eq7': EQ7, 'eq8': EQ8, 'eq9': EQ9, 'eq10': EQ10, 'eq11': EQ11,
    'eq12': EQ12, 'eq13': EQ13, 'eq14': EQ14, 'eq15': EQ15, 'eq16': EQ16,
    'eq17': EQ17, 'eq18': EQ18, 'eq19': EQ19, 'eq20': EQ20, 'eq21': EQ21,
    'eq22': EQ22, 'eq23': EQ23, 'eq24': EQ24, 'eq25': EQ25,
}
