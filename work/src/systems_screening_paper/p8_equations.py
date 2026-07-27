# -*- coding: utf-8 -*-
"""Paper 8 display equations in OMML (Word's native equation format)."""
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
    return mdelim(b, left='{', right='}')


def prod(sub, sup, body):
    return ('<m:nary><m:naryPr><m:chr m:val="∏"/><m:limLoc m:val="subSup"/>'
            '</m:naryPr>'
            f'<m:sub>{sub}</m:sub><m:sup>{sup}</m:sup><m:e>{body}</m:e></m:nary>')


def integral(body):
    return ('<m:nary><m:naryPr><m:chr m:val="∫"/><m:limLoc m:val="subSup"/>'
            '<m:subHide m:val="1"/><m:supHide m:val="1"/></m:naryPr>'
            f'<m:sub></m:sub><m:sup></m:sup><m:e>{body}</m:e></m:nary>')


# (1) U_nsj = beta_n' x_sj + eps_nsj
EQ1 = omath(
    msub(mr('U'), mr('nsj')) + op('=') +
    msup(msub(mr('β'), mr('n')), mr('′')) + msub(mr('x'), mr('sj')) + op('+') +
    msub(mr('ε'), mr('nsj'))
)

# (2) V_nsj = b1 AI + b2 PE + b3 AI*PE + b4 T70 + b5 T90 + b6 EL + b7 RF
#             + b8 IN + b9 (w - wbar)
EQ2 = omath(
    msub(mr('V'), mr('nsj')) + op('=') +
    msub(mr('β'), mr('1n')) + msub(mr('AI'), mr('sj')) + op('+') +
    msub(mr('β'), mr('2n')) + msub(mr('PE'), mr('sj')) + op('+') +
    msub(mr('β'), mr('3n')) + msub(mr('AI'), mr('sj')) + msub(mr('PE'), mr('sj')) +
    op('+') + msup(mr('γ'), mr('′')) + msub(mr('q'), mr('sj')) + op('+') +
    msub(mr('β'), mr('wn')) + mdelim(msub(mr('w'), mr('sj')) + op('−') +
                                     mr('w̄'))
)

# (3) conditional logit probability
EQ3 = omath(
    msub(mr('P'), mr('nsj')) + op('=') +
    mfrac(mr('exp', upright=True) + mdelim(msub(mr('V'), mr('nsj'))),
          msum(mr('m∈') + msub(mr('C'), mr('s')), '',
               mr('exp', upright=True) + mdelim(msub(mr('V'), mr('nsm')))))
)

# (4) mixed logit sequence probability
EQ4 = omath(
    msub(mr('L'), mr('n')) + mdelim(mr('θ')) + op('=') +
    integral(prod(mr('s=1'), mr('S'), msub(mr('P'), mr('ns')) +
                  mdelim(mr('β'))) + sp() + mr('f') +
             mdelim2(mr('β'), mr('θ')) + sp() +
             mr('d') + mr('β'))
)

# (5) simulated log-likelihood
EQ5 = omath(
    mr('SLL') + mdelim(mr('θ')) + op('=') +
    msum(mr('n=1'), mr('N'),
         mr('ln', upright=True) + sp() +
         brack(mfrac(num('1'), mr('R')) + sp() +
               msum(mr('r=1'), mr('R'),
                    prod(mr('s=1'), mr('S'),
                         msub(mr('P'), mr('ns')) +
                         mdelim(msub(mr('β'), mr('r'))))))) +
    mr(',    ', upright=True) + msub(mr('β'), mr('r')) + op('=') +
    mr('b') + op('+') + mr('diag', upright=True) + mdelim(mr('σ')) +
    msub(mr('η'), mr('r'))
)

# (6) marginal rate of substitution in salary units
EQ6 = omath(
    msub(mr('MRS'), mr('k')) + op('=') +
    op('−') + mfrac(msub(mr('β'), mr('k')), msub(mr('β'), mr('w')))
)

# (7) disclosure penalty with and without process evidence
EQ7 = omath(
    msub(mr('Δ'), mr('0')) + op('=') + msub(mr('β'), num('1')) +
    mr(',    ', upright=True) +
    msub(mr('Δ'), mr('1')) + op('=') + msub(mr('β'), num('1')) + op('+') +
    msub(mr('β'), num('3'))
)

# (8) latent class probability
EQ8 = omath(
    msub(mr('P'), mr('n')) + op('=') +
    msum(mr('c=1'), mr('C'), msub(mr('π'), mr('c')) + sp() +
         prod(mr('s=1'), mr('S'),
              msub(mr('P'), mr('ns')) + mdelim(msub(mr('β'), mr('c')))))
)

# (9) membership model
EQ9 = omath(
    msub(mr('π'), mr('nc')) + op('=') +
    mfrac(mr('exp', upright=True) + mdelim(msup(msub(mr('γ'), mr('c')), mr('′')) +
                                           msub(mr('z'), mr('n'))),
          msum(mr('h=1'), mr('C'),
               mr('exp', upright=True) +
               mdelim(msup(msub(mr('γ'), mr('h')), mr('′')) +
                      msub(mr('z'), mr('n')))))
)

# (10) entropy R-squared
EQ10 = omath(
    msub(mr('E'), mr('C')) + op('=') + num('1') + op('−') +
    mfrac(op('−') + msum(mr('n=1'), mr('N'),
                         msum(mr('c=1'), mr('C'),
                              msub(mr('h'), mr('nc')) + sp() +
                              mr('ln', upright=True) + sp() +
                              msub(mr('h'), mr('nc')))),
          mr('N') + sp() + mr('ln', upright=True) + sp() + mr('C'))
)

# (11) randomised-architecture outcome model
EQ11 = omath(
    msub(mr('y'), mr('n')) + op('=') + mr('α') + op('+') +
    msub(mr('δ'), num('1')) + msup(msub(mr('D'), mr('n')), mr('cred')) + op('+') +
    msub(mr('δ'), num('2')) + msup(msub(mr('D'), mr('n')), mr('evid')) + op('+') +
    msup(mr('λ'), mr('′')) + msub(mr('z'), mr('n')) + op('+') + msub(mr('u'), mr('n'))
)

EQUATIONS_P8 = {
    'eq1': EQ1, 'eq2': EQ2, 'eq3': EQ3, 'eq4': EQ4, 'eq5': EQ5, 'eq6': EQ6,
    'eq7': EQ7, 'eq8': EQ8, 'eq9': EQ9, 'eq10': EQ10, 'eq11': EQ11,
}
