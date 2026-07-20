# -*- coding: utf-8 -*-
"""Display equations in OMML (Word native equation editor format)."""
from mdpi_builder import mr, msub, mfrac, omath, mdelim

def _acc_tilde(base):
    return f'<m:acc><m:accPr><m:chr m:val="̃"/></m:accPr><m:e>{base}</m:e></m:acc>'

def _sp():
    return mr(' ')

def _eq_op(op='='):
    return _sp() + mr(op, upright=True) + _sp()

def _plus():
    return _sp() + mr('+', upright=True) + _sp()

def _times():
    return _sp() + mr('×', upright=True) + _sp()

def _prime(sym):
    # symbol with prime superscript, e.g. γ′
    return mr(sym + '′')

# (1) YEMP_{i,t} = Emp30_{i,t} / Emp_{i,t}
EQ1 = omath(
    msub(mr('YEMP'), mr('i,t')) + _eq_op() +
    mfrac(msub(mr('Emp30', upright=True), mr('i,t')),
          msub(mr('Emp', upright=True), mr('i,t')))
)

# (2) II_{m,t} = ROBOT_{m,t} / L_{m,2010}
EQ2 = omath(
    msub(mr('II'), mr('m,t')) + _eq_op() +
    mfrac(msub(mr('ROBOT', upright=True), mr('m,t')),
          msub(mr('L'), mr('m,2010')))
)

# (3) ω_{i,m} = RS_{i,m,2011} / ~RS_{m,2011}
EQ3 = omath(
    msub(mr('ω'), mr('i,m')) + _eq_op() +
    mfrac(msub(mr('RS', upright=True), mr('i,m,2011')),
          msub(_acc_tilde(mr('RS', upright=True)), mr('m,2011')))
)

# (4) II_{i,t} = ω_{i,m} × II_{m,t}
EQ4 = omath(
    msub(mr('II'), mr('i,t')) + _eq_op() +
    msub(mr('ω'), mr('i,m')) + _times() +
    msub(mr('II'), mr('m,t'))
)

def _controls_tail(coef_sym):
    """+ SYM′ Controls_{i,t} + μ_i + λ_t + ε_{i,t}"""
    return (_plus() + _prime(coef_sym) + _sp() +
            msub(mr('Controls'), mr('i,t')) +
            _plus() + msub(mr('μ'), mr('i')) +
            _plus() + msub(mr('λ'), mr('t')) +
            _plus() + msub(mr('ε'), mr('i,t')))

# (5) Y_{i,t} = α + β_1 II_{i,t−1} + γ′Controls + μ_i + λ_t + ε_{i,t}
EQ5 = omath(
    msub(mr('Y'), mr('i,t')) + _eq_op() + mr('α') +
    _plus() + msub(mr('β'), mr('1')) + _sp() + msub(mr('II'), mr('i,t−1')) +
    _controls_tail('γ')
)

# (6) M_{i,t} = α + δ_1 II_{i,t−1} + θ′Controls + μ_i + λ_t + ε_{i,t}
EQ6 = omath(
    msub(mr('M'), mr('i,t')) + _eq_op() + mr('α') +
    _plus() + msub(mr('δ'), mr('1')) + _sp() + msub(mr('II'), mr('i,t−1')) +
    _controls_tail('θ')
)

# (7) Y_{i,t} = α + φ_1 M_{i,t} + φ_2 II_{i,t−1} + κ′Controls + μ_i + λ_t + ε_{i,t}
EQ7 = omath(
    msub(mr('Y'), mr('i,t')) + _eq_op() + mr('α') +
    _plus() + msub(mr('φ'), mr('1')) + _sp() + msub(mr('M'), mr('i,t')) +
    _plus() + msub(mr('φ'), mr('2')) + _sp() + msub(mr('II'), mr('i,t−1')) +
    _controls_tail('κ')
)

# (8) Y = α + η1 II + η2 Mod + η3 II×Mod + ϑ′Controls + μ + λ + ε
# kept compact (no delimiters) so the equation stays within the text column
EQ8 = omath(
    msub(mr('Y'), mr('i,t')) + _eq_op() + mr('α') +
    _plus() + msub(mr('η'), mr('1')) + _sp() + msub(mr('II'), mr('i,t−1')) +
    _plus() + msub(mr('η'), mr('2')) + _sp() + msub(mr('Mod'), mr('i,t')) +
    _plus() + msub(mr('η'), mr('3')) + _sp() +
    msub(mr('II'), mr('i,t−1')) + mr('×', upright=True) + msub(mr('Mod'), mr('i,t')) +
    _controls_tail('ϑ')
)

EQUATIONS = {'eq1': EQ1, 'eq2': EQ2, 'eq3': EQ3, 'eq4': EQ4,
             'eq5': EQ5, 'eq6': EQ6, 'eq7': EQ7, 'eq8': EQ8}
