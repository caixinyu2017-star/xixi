# -*- coding: utf-8 -*-
"""Paper 9 display equations in OMML (Word's native equation format)."""
from mdpi_builder import mr, msub, msup, mfrac, msum, mdelim, mdelim2, omath


def sp():
    return mr(' ')


def op(o):
    return sp() + mr(o, upright=True) + sp()


def num(t):
    return mr(t, upright=True)


def brack(b):
    return mdelim(b, left='[', right=']')


def brace(b):
    return mdelim(b, left='{', right='')


def prod(lo, hi, body):
    return (f'<m:nary><m:naryPr><m:chr m:val="&#8719;"/><m:limLoc m:val="undOvr"/>'
            f'<m:supHide m:val="0"/><m:subHide m:val="0"/></m:naryPr>'
            f'<m:sub>{lo}</m:sub><m:sup>{hi}</m:sup><m:e>{body}</m:e></m:nary>')


# (1) CES production over the two kinds of entry-tier graduate
EQ1 = omath(
    msub(mr('Y'), mr('t')) + op('=') +
    msup(brack(msum(mr('j=1'), mr('2'),
                    msup(mdelim(msub(mr('A'), mr('jt')) + msub(mr('E'), mr('jt'))),
                         mr('ρ')))),
         mfrac(num('1'), mr('ρ'))) + mr(',') + sp() + sp() +
    mr('ρ') + op('=') + mfrac(mr('σ') + mr('−') + num('1'), mr('σ'))
)

# (2) marginal product of an entry-tier worker
EQ2 = omath(
    msub(mr('p'), mr('jt')) + op('=') +
    mfrac(mr('∂') + msub(mr('Y'), mr('t')),
          mr('∂') + msub(mr('E'), mr('jt'))) + op('=') +
    msup(msub(mr('A'), mr('jt')), mr('ρ')) +
    msup(msub(mr('Y'), mr('t')), num('1') + mr('−') + mr('ρ')) +
    msup(msub(mr('E'), mr('jt')), mr('ρ') + mr('−') + num('1'))
)

# (3) matching, tightness and the two rates
EQ3 = omath(
    msub(mr('m'), mr('jt')) + op('=') +
    mr('μ') + msup(msub(mr('S'), mr('jt')), mr('α')) +
    msup(msub(mr('V'), mr('jt')), num('1') + mr('−') + mr('α')) + mr(',') + sp() + sp() +
    msub(mr('θ'), mr('jt')) + op('=') +
    mfrac(msub(mr('V'), mr('jt')), msub(mr('S'), mr('jt'))) + mr(',') + sp() + sp() +
    msub(mr('f'), mr('jt')) + op('=') +
    mr('μ') + msup(msub(mr('θ'), mr('jt')), num('1') + mr('−') + mr('α'))
)

# (4) match surplus
EQ4 = omath(
    msub(mr('Σ'), mr('jt')) + op('=') +
    mfrac(msub(mr('p'), mr('jt')) + mr('−') + mr('b'),
          mr('r') + mr('+') + mr('δ') + mr('+') + mr('γ') + mr('+') +
          mr('η') + msub(mr('f'), mr('jt')))
)

# (5) free entry
EQ5 = omath(
    mfrac(mr('κ'), mr('q') + mdelim(msub(mr('θ'), mr('jt')))) + op('=') +
    mdelim(num('1') + mr('−') + mr('η')) + msub(mr('Σ'), mr('jt')) + mr(',') + sp() + sp() +
    mr('q') + mdelim(mr('θ')) + op('=') + mr('μ') + msup(mr('θ'), mr('−') + mr('α'))
)

# (6) wage and the value of entering the field
EQ6 = omath(
    msub(mr('w'), mr('jt')) + op('=') + mr('b') + mr('+') + mr('η') +
    msub(mr('Σ'), mr('jt')) + mdelim(mr('r') + mr('+') + mr('δ') + mr('+') + mr('γ') +
                                     mr('+') + msub(mr('f'), mr('jt'))) + mr(',') +
    sp() + sp() +
    msub(mr('W'), mr('jt')) + op('=') +
    mfrac(mr('b') + mr('+') + msub(mr('f'), mr('jt')) + mr('η') + msub(mr('Σ'), mr('jt')),
          mr('r'))
)

# (7) stock transitions
EQ7 = omath(
    msub(mr('E'), mr('j,t+1')) + op('=') +
    brack(msub(mr('E'), mr('jt')) + mdelim(num('1') + mr('−') + mr('d')) + mr('+') +
          msub(mr('U'), mr('jt')) + msub(mr('F'), mr('jt'))) +
    mdelim(num('1') + mr('−') + mr('g'))
)

# (8) searcher transitions and the graduating cohort
EQ8 = omath(
    msub(mr('U'), mr('j,t+1')) + op('=') +
    brack(msub(mr('U'), mr('jt')) + mdelim(num('1') + mr('−') + msub(mr('F'), mr('jt'))) +
          mr('+') + msub(mr('E'), mr('jt')) + mr('d')) +
    mdelim(num('1') + mr('−') + mr('g')) + mr('+') + msub(mr('G'), mr('j,t+1'))
)

# (9) the pipeline: the graduating cohort was chosen D years earlier
EQ9 = omath(
    msub(mr('G'), mr('1t')) + op('=') + msub(mr('s'), mr('t−D')) + msub(mr('N'), mr('t−D'))
    + mr(',') + sp() + sp() +
    msub(mr('G'), mr('2t')) + op('=') +
    mdelim(num('1') + mr('−') + msub(mr('s'), mr('t−D'))) + msub(mr('N'), mr('t−D'))
)

# (10) the differential entrants decide on
EQ10 = omath(
    msub(mr('x'), mr('t')) + op('=') +
    mr('r') + mdelim(msub(mr('W'), mr('1t')) + mr('−') + msub(mr('W'), mr('2t'))) +
    mr('+') + mr('a')
)

# (11) the field choice
EQ11 = omath(
    msub(mr('s'), mr('t')) + op('=') +
    mfrac(num('1'),
          num('1') + mr('+') + mr('exp', upright=True) +
          mdelim(mr('−') + mr('β') + msup(msub(mr('x'), mr('t')), mr('e'))))
)


# (12) the two forecasting rules
EQ12 = omath(
    msup(msub(mr('x'), mr('1,t+D')), mr('e')) + op('=') + mr('x̄') + mr(',') +
    sp() + sp() + sp() +
    msup(msub(mr('x'), mr('2,t+D')), mr('e')) + op('=') +
    msub(mr('x'), mr('t−1')) + mr('+') + mr('φ') +
    mdelim(msub(mr('x'), mr('t−1')) + mr('−') + msub(mr('x'), mr('t−2')))
)

# (13) fitness and the weights on the rules
EQ13 = omath(
    msub(mr('n'), mr('ht')) + op('=') +
    mfrac(mr('exp', upright=True) + mdelim(mr('ψ') + msub(mr('π'), mr('h,t−1'))),
          msum(mr('k=1'), mr('2'),
               mr('exp', upright=True) +
               mdelim(mr('ψ') + msub(mr('π'), mr('k,t−1'))))) + mr(',') + sp() + sp() +
    msub(mr('π'), mr('ht')) + op('=') +
    mr('−') + msup(mdelim(msub(mr('x'), mr('t')) + mr('−') +
                          msup(msub(mr('x'), mr('ht')), mr('e'))), num('2')) +
    mr('−') + msub(mr('c'), mr('h'))
)

# (14) the population forecast
EQ14 = omath(
    msup(msub(mr('x'), mr('t')), mr('e')) + op('=') +
    msum(mr('h=1'), mr('2'),
         msub(mr('n'), mr('ht')) + msup(msub(mr('x'), mr('h,t+D')), mr('e')))
)

# (15) the loop gain and the stability condition
EQ15 = omath(
    mr('Γ') + op('=') +
    mfrac(mr('d') + msub(mr('s'), mr('t')), mr('d') + msub(mr('s'), mr('t−D')))
    + mr(',') + sp() + sp() +
    mdelim(mr('λ')) + op('=') +
    msup(mdelim(mr('Γ'), left='|', right='|'), mfrac(num('1'), mr('D'))) + mr(',') +
    sp() + sp() + mr('T') + op('=') + num('2') + mr('D')
)

# (16) the cost of adjustment
EQ16 = omath(
    mr('L') + op('=') +
    msum(mr('t=0'), mr('∞'),
         msup(mdelim(num('1') + mr('+') + mr('r'), left='(', right=')'),
              mr('−') + mr('t')) +
         mfrac(msup(mr('Y'), mr('*')) + mr('−') + msub(mr('Y'), mr('t')),
               msup(mr('Y'), mr('*')))) +
    mr(' ') + mr('÷') + mr(' ') +
    msum(mr('t=0'), mr('∞'),
         msup(mdelim(num('1') + mr('+') + mr('r'), left='(', right=')'),
              mr('−') + mr('t')))
)

EQS = {'eq%d' % i: e for i, e in enumerate(
    [EQ1, EQ2, EQ3, EQ4, EQ5, EQ6, EQ7, EQ8, EQ9, EQ10, EQ11, EQ12, EQ13, EQ14,
     EQ15, EQ16], start=1)}
