# -*- coding: utf-8 -*-
"""Display equations of the YSTS model, written as native Word OMML."""
from mdpi_builder import mr, msub, msup, mfrac, msum, mdelim, omath


def _sp():
    return mr(' ')


def _op(op):
    return _sp() + mr(op, upright=True) + _sp()


def _dot(base):
    return f'<m:acc><m:accPr><m:chr m:val="̇"/></m:accPr><m:e>{base}</m:e></m:acc>'


def _up(t):
    return mr(t, upright=True)


def _fn(name, arg):
    """Upright function name applied to a parenthesised argument."""
    return _up(name) + mdelim(arg)


L = 'Λ'          # logistic link
EXP = 'exp'

# (1) logistic digital-economy intensity ------------------------------------
EQ1 = omath(
    _fn('Ψ', mr('t')) + _op('=') +
    mfrac(msub(mr('Ψ'), _up('max')),
          mr('1') + _op('+') +
          mdelim(mfrac(msub(mr('Ψ'), _up('max')), msub(mr('Ψ'), mr('0'))) +
                 _op('−') + mr('1')) +
          _sp() + msup(_up(EXP), mdelim(_op('−') + msub(mr('r'), mr('Ψ')) + mr('t'),
                                        left='', right=''))))

# (2) employer skill threshold ----------------------------------------------
EQ2 = omath(
    _fn('θ', mr('t')) + _op('=') + msub(mr('θ'), mr('0')) + _op('+') + mr('κ') +
    mdelim(_fn('Ψ', mr('t')) + _op('−') + msub(mr('Ψ'), mr('0'))) + _op('+') +
    msub(mr('κ'), mr('2')) + _sp() +
    mfrac(_fn('U', mr('t')), _fn('M', mr('t')) + _op('+') + _fn('U', mr('t')))
)

# (3) skill-threshold gap ----------------------------------------------------
EQ3 = omath(
    _fn('x', mr('t')) + _op('=') + _fn('H', mr('t')) + _op('−') + _fn('θ', mr('t'))
)

# (4) meeting function and market tightness ---------------------------------
EQ4 = omath(
    _fn('m', mr('t')) + _op('=') + mr('μ') + _sp() +
    msup(_fn('S', mr('t')), mr('α')) + _sp() +
    msup(_fn('V', mr('t')), mr('1') + _op('−') + mr('α')) + mr(',') + _sp() + _sp() +
    _fn('ϑ', mr('t')) + _op('=') + mfrac(_fn('V', mr('t')), _fn('S', mr('t')))
)

# (5) screening, acceptance and match quality --------------------------------
EQ5 = omath(
    msub(mr('p'), mr('s')) + _op('=') + _fn(L, msub(mr('β'), mr('s')) + mr('x')) +
    mr(',') + _sp() + _sp() +
    msub(mr('p'), mr('a')) + _op('=') +
    _fn(L, msub(mr('β'), mr('a')) + mdelim(mr('q') + _op('−') + mr('A'))) +
    mr(',') + _sp() + _sp() +
    mr('σ') + _op('=') +
    _fn(L, msub(mr('σ'), mr('0')) + _op('+') + msub(mr('β'), mr('σ')) + mr('x'))
)

# (6) offer quality ----------------------------------------------------------
EQ6 = omath(
    _fn('q', mr('t')) + _op('=') + msub(mr('q'), mr('0')) + _op('+') +
    msub(mr('γ'), mr('q')) + _sp() + _up('ln') +
    mdelim(mr('1') + _op('+') + _fn('ϑ', mr('t')))
)

# (7) hiring rate with a smooth capacity limit -------------------------------
EQ7 = omath(
    _fn('h', mr('t')) + _op('=') +
    _up('smin') + mdelim(mr('m') + _sp() + msub(mr('p'), mr('s')) + _sp() +
                         msub(mr('p'), mr('a')) + mr(', ') +
                         mfrac(mr('S'), msub(mr('d'), _up('min')))) +
    mr(',') + _sp() + _sp() +
    _up('smin') + mdelim(mr('a') + mr(', ') + mr('b')) + _op('=') +
    mfrac(mr('a') + mr('b'), mr('a') + _op('+') + mr('b'))
)

# (8) values of searching and queueing, with probability weighting -----------
EQ8 = omath(
    msub(mr('W'), mr('S')) + _op('=') + msub(mr('p'), mr('s')) + _sp() +
    msub(mr('p'), mr('a')) + _sp() + mr('q') + mr(',') + _sp() + _sp() +
    msub(mr('W'), mr('Q')) + _op('=') + mr('Π') + _sp() +
    _fn('w', msub(mr('π'), mr('e'))) + mr(',') + _sp() + _sp() +
    _fn('w', mr('π')) + _op('=') +
    msup(_up(EXP), mdelim(_op('−') +
                          msup(mdelim(_op('−') + _up('ln') + _sp() + mr('π')),
                               mr('ε')), left='', right=''))
)

# (9) queue entry and discouraged return -------------------------------------
EQ9 = omath(
    msub(mr('f'), mr('SQ')) + _op('=') + mr('ν') + _sp() + mr('S') + _sp() +
    _fn(L, msub(mr('β'), mr('c')) +
        mfrac(msub(mr('W'), mr('Q')) + _op('−') + msub(mr('W'), mr('S')),
              msub(mr('W'), mr('Q')) + _op('+') + msub(mr('W'), mr('S')))) +
    mr(',') + _sp() + _sp() +
    msub(mr('f'), mr('QS')) + _op('=') + msub(mr('ν'), mr('r')) + _sp() + mr('Q') +
    mdelim(mr('1') + _op('−') + _fn(L, mr('·')), left='[', right=']')
)

# (10) searcher stock --------------------------------------------------------
EQ10 = omath(
    _dot(mr('S')) + _op('=') + _fn('Φ', mr('t')) + _op('+') +
    msub(mr('f'), mr('QS')) + _op('+') + msub(mr('δ'), mr('M')) + mr('M') + _op('+') +
    msub(mr('δ'), mr('U')) + mr('U') + _op('−') + mr('h') + _op('−') +
    msub(mr('f'), mr('SQ')) + _op('−') + mr('ω') + mr('S')
)

# (11) queue stock -----------------------------------------------------------
EQ11 = omath(
    _dot(mr('Q')) + _op('=') + msub(mr('f'), mr('SQ')) + _op('−') +
    msub(mr('f'), mr('QS')) + _op('−') + msub(mr('f'), mr('QM')) + _op('−') +
    mr('ω') + mr('Q') + mr(',') + _sp() + _sp() +
    msub(mr('f'), mr('QM')) + _op('=') +
    _up('smin') + mdelim(mr('Ξ') + mr(', ') + mr('Q')) + mr(',') + _sp() + _sp() +
    msub(mr('π'), mr('e')) + _op('=') + mfrac(msub(mr('f'), mr('QM')), mr('Q'))
)

# (12) employment stocks -----------------------------------------------------
EQ12 = omath(
    _dot(mr('M')) + _op('=') + mr('h') + mr('σ') + _op('+') +
    msub(mr('f'), mr('QM')) + _op('−') +
    mdelim(msub(mr('δ'), mr('M')) + _op('+') + mr('ω')) + mr('M') +
    mr(',') + _sp() + _sp() +
    _dot(mr('U')) + _op('=') + mr('h') + mdelim(mr('1') + _op('−') + mr('σ')) +
    _op('−') + mdelim(msub(mr('δ'), mr('U')) + _op('+') + mr('ω')) + mr('U')
)

# (13) employability capital -------------------------------------------------
EQ13 = omath(
    _dot(mr('H')) + _op('=') +
    mfrac(_fn('Φ', mr('t')) + mdelim(msub(mr('h'), _up('new')) + _op('−') + mr('H')) +
          _op('−') + msub(mr('f'), mr('QS')) +
          mdelim(mr('1') + _op('−') + mr('χ')) + mr('H'), mr('S')) +
    _op('−') + msub(mr('δ'), mr('H')) + mr('H') + _op('+') + mr('τ') +
    mdelim(msub(mr('h'), _up('max')) + _op('−') + mr('H'))
)

# (14) aspiration ------------------------------------------------------------
EQ14 = omath(
    _dot(mr('A')) + _op('=') + mr('λ') +
    mdelim(msup(mr('A'), mr('∗')) + _op('−') + mr('A')) + mr(',') + _sp() + _sp() +
    msup(mr('A'), mr('∗')) + _op('=') + mr('ζ') + msub(mr('A'), _up('anch')) +
    _op('+') + mdelim(mr('1') + _op('−') + mr('ζ')) + mr('q') +
    msub(mr('p'), mr('s'))
)

# (15) outcome indicators ----------------------------------------------------
EQ15 = omath(
    _up('NER') + _op('=') + mfrac(mr('S') + _op('+') + mr('Q'),
                                  mr('S') + _op('+') + mr('Q') + _op('+') + mr('M') +
                                  _op('+') + mr('U')) + mr(',') + _sp() + _sp() +
    _up('MM') + _op('=') + mfrac(mr('U'), mr('M') + _op('+') + mr('U')) +
    mr(',') + _sp() + _sp() +
    mr('D') + _op('=') + mfrac(mr('S') + _op('+') + mr('Q'),
                               mr('h') + mr('σ') + _op('+') + msub(mr('f'), mr('QM')))
)

# (16) fixed point, Jacobian and relaxation times -----------------------------
EQ16 = omath(
    _fn('f', msup(mr('y'), mr('∗')) + mr('; ') + mr('t')) + _op('=') + mr('0') +
    mr(',') + _sp() + _sp() +
    _fn('J', mr('t')) + _op('=') +
    msub(mfrac(mr('∂') + mr('f'), mr('∂') + mr('y')), msup(mr('y'), mr('∗'))) +
    mr(',') + _sp() + _sp() +
    msub(mr('τ'), mr('i')) + _op('=') +
    _op('−') + mfrac(mr('1'), _up('Re') + _sp() + msub(mr('λ'), mr('i')))
)

# (17) Sobol indices ---------------------------------------------------------
EQ17 = omath(
    msub(mr('S'), mr('i')) + _op('=') +
    mfrac(_up('Var') + mdelim(_up('E') +
                              mdelim(mr('Y') + mr(' | ') + msub(mr('X'), mr('i')),
                                     left='[', right=']')),
          _up('Var') + mdelim(mr('Y'))) + mr(',') + _sp() + _sp() +
    msub(mr('S'), mr('Ti')) + _op('=') +
    mfrac(_up('E') + mdelim(_up('Var') +
                            mdelim(mr('Y') + mr(' | ') + msub(mr('X'), mr('∼i')),
                                   left='[', right=']')),
          _up('Var') + mdelim(mr('Y')))
)

# (18) Saltelli estimators ---------------------------------------------------
_A = msup(mr('Y'), mr('A'))
_B = msup(mr('Y'), mr('B'))
_ABi = msubsup = (f'<m:sSubSup><m:sSubSupPr/><m:e>{mr("Y")}</m:e>'
                  f'<m:sub>{mr("i")}</m:sub><m:sup>{mr("AB")}</m:sup></m:sSubSup>')
EQ18 = omath(
    msub(mr('Ŝ'), mr('i')) + _op('=') +
    mfrac(mfrac(mr('1'), mr('N')) + msum(mr('n=1'), mr('N'),
                                         mdelim(_A + mdelim(_ABi + _op('−') + _B))),
          msup(mr('s'), mr('2'))) + mr(',') + _sp() + _sp() +
    msub(mr('Ŝ'), mr('Ti')) + _op('=') +
    mfrac(mfrac(mr('1'), mr('2N')) + msum(mr('n=1'), mr('N'),
                                          msup(mdelim(_B + _op('−') + _ABi), mr('2'))),
          msup(mr('s'), mr('2')))
)

# (19) logistic meta-model of trap risk --------------------------------------
EQ19 = omath(
    _up('Pr') + mdelim(msub(mr('T'), mr('j')) + _op('=') + mr('1') + mr(' | ') +
                       msub(mr('z'), mr('j'))) + _op('=') +
    _fn(L, msub(mr('γ'), mr('0')) + _op('+') +
        msum(mr('k=1'), mr('K'), msub(mr('γ'), mr('k')) + msub(mr('z'), mr('jk'))))
)

# (20) policy effort in prior standard deviations ----------------------------
EQ20 = omath(
    msubsup2 := (f'<m:sSubSup><m:sSubSupPr/><m:e>{mr("p")}</m:e>'
                 f'<m:sub>{mr("k")}</m:sub><m:sup>{mr("pol")}</m:sup></m:sSubSup>') +
    _op('=') + msub(mr('p'), mr('k')) + _op('±') + mr('e') + _sp() +
    msub(mr('s'), mr('k')) + mr(',') + _sp() + _sp() +
    msub(mr('s'), mr('k')) + _op('=') +
    mfrac(msub(mr('b'), mr('k')) + _op('−') + msub(mr('a'), mr('k')),
          msup(mr('12'), mr('1/2')))
)

EQUATIONS = {f'eq{i}': e for i, e in enumerate(
    [EQ1, EQ2, EQ3, EQ4, EQ5, EQ6, EQ7, EQ8, EQ9, EQ10, EQ11, EQ12, EQ13, EQ14,
     EQ15, EQ16, EQ17, EQ18, EQ19, EQ20], start=1)}
