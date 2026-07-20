# -*- coding: utf-8 -*-
"""Paper 2 display equations in OMML."""
from mdpi_builder import mr, msub, msup, mfrac, msum, mdelim, omath

def _sp():
    return mr(' ')

def _op(op):
    return _sp() + mr(op, upright=True) + _sp()

def _acc_bar(base):
    return f'<m:acc><m:accPr><m:chr m:val="̄"/></m:accPr><m:e>{base}</m:e></m:acc>'

# (1) (Y_1i, Y_2i) = α + β X_ki + ε_i
EQ1 = omath(
    mdelim(msub(mr('Y'), mr('1i')) + mr(', ', upright=True) + msub(mr('Y'), mr('2i'))) +
    _op('=') + mr('α') + _op('+') + mr('β') + msub(mr('X'), mr('ki')) +
    _op('+') + msub(mr('ε'), mr('i'))
)

# (2) z_ij = (x_ij − x̄_j) / s_j
EQ2 = omath(
    msub(mr('z'), mr('ij')) + _op('=') +
    mfrac(msub(mr('x'), mr('ij')) + _op('−') + msub(_acc_bar(mr('x')), mr('j')),
          msub(mr('s'), mr('j')))
)

# (3) X = ΛF + ε
EQ3 = omath(
    mr('X') + _op('=') + mr('Λ') + mr('F') + _op('+') + mr('ε')
)

# (4) Y_i = β_0 + β_1 FACT_{EDL,i} + ε_i
EQ4 = omath(
    msub(mr('Y'), mr('i')) + _op('=') + msub(mr('β'), mr('0')) + _op('+') +
    msub(mr('β'), mr('1')) + _sp() + msub(mr('FACT', upright=True), mr('EDL,i')) +
    _op('+') + msub(mr('ε'), mr('i'))
)

# (5) W = Σ_{k=1}^{K} Σ_{i∈C_k} ‖ z_i − μ_k ‖²
_norm = mdelim(msub(mr('z'), mr('i')) + _op('−') + msub(mr('μ'), mr('k')),
               left='‖', right='‖')
EQ5 = omath(
    mr('W') + _op('=') +
    msum(mr('k=1'), mr('K'),
         msum(mr('i∈') + msub(mr('C'), mr('k')), '',
              msup(_norm, mr('2'))))
)

EQUATIONS_P2 = {'eq1': EQ1, 'eq2': EQ2, 'eq3': EQ3, 'eq4': EQ4, 'eq5': EQ5}
