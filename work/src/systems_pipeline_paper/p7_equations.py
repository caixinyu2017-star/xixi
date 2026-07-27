# -*- coding: utf-8 -*-
"""Paper 7 display equations in OMML (Word's native equation format)."""
from mdpi_builder import mr, msub, msup, mfrac, mdelim, omath


def sp():
    return mr(' ')


def op(o):
    return sp() + mr(o, upright=True) + sp()


def num(t):
    return mr(t, upright=True)


def d(v, wrt='t'):
    """derivative d v / d t"""
    return mfrac(num('d') + mr(v), num('d') + mr(wrt))


def brace(body):
    return mdelim(body, left='{', right='}')


def brack(body):
    return mdelim(body, left='[', right=']')


# ---------------------------------------------------------------- Study 1
# (1) JSH_i = alpha_0 + alpha_1 ATA_i + gamma' x_i + eps_i
EQ1 = omath(
    msub(mr('JSH'), mr('i')) + op('=') + msub(mr('α'), num('0')) + op('+') +
    msub(mr('α'), num('1')) + msub(mr('ATA'), mr('i')) + op('+') +
    msup(mr('γ'), mr('′')) + msub(mr('x'), mr('i')) + op('+') +
    msub(mr('ε'), mr('i'))
)

# (2) ln TTP_i = b0 + b1 ln(MEN_i/m*) + b2 ATA_i + b3 (ATA_i SAL_i) + g'x + e
EQ2 = omath(
    num('ln') + sp() + msub(mr('TTP'), mr('i')) + op('=') +
    msub(mr('β'), num('0')) + op('+') + msub(mr('β'), num('1')) + sp() +
    num('ln') + mdelim(mfrac(msub(mr('MEN'), mr('i')), msup(mr('m'), mr('∗')))) +
    op('+') + msub(mr('β'), num('2')) + msub(mr('ATA'), mr('i')) + op('+') +
    msub(mr('β'), num('3')) + mdelim(msub(mr('ATA'), mr('i')) + sp() +
                                     msub(mr('SAL'), mr('i'))) +
    op('+') + msup(mr('γ'), mr('′')) + msub(mr('x'), mr('i')) + op('+') +
    msub(mr('ε'), mr('i'))
)

# (3) partial ln TTP / partial ATA = b2 + b3 SAL
EQ3 = omath(
    mfrac(mr('∂') + sp() + num('ln') + sp() + mr('TTP'),
          mr('∂') + sp() + mr('ATA')) + op('=') +
    msub(mr('β'), num('2')) + op('+') + msub(mr('β'), num('3')) + sp() + mr('SAL')
)

# ---------------------------------------------------------------- Study 2
# (4) dA/dt = c A (1 - A/A_max)
EQ4 = omath(
    d('A') + op('=') + mr('c') + sp() + mr('A') +
    mdelim(num('1') + op('−') + mfrac(mr('A'), msub(mr('A'), mr('max'))))
)

# (5) J* = j0 D(t) (1 - phi A)(1 + w W)
EQ5 = omath(
    msup(mr('J'), mr('∗')) + op('=') + msub(mr('j'), num('0')) + sp() +
    mr('D') + mdelim(mr('t')) + mdelim(num('1') + op('−') + mr('φ') + mr('A')) +
    mdelim(num('1') + op('+') + mr('w') + mr('W'))
)

# (6) H = min{ (J*-J)/tauH + rho + J/tauJ , P/tauM }
EQ6 = omath(
    mr('H') + op('=') + num('min') + sp() +
    brace(mfrac(msup(mr('J'), mr('∗')) + op('−') + mr('J'),
                msub(mr('τ'), mr('H'))) + op('+') + mr('ρ') + op('+') +
          mfrac(mr('J'), msub(mr('τ'), mr('J'))) + mr(', ', upright=True) +
          mfrac(mr('P'), msub(mr('τ'), mr('M'))))
)

# (7) dP/dt = G + b J/tauJ - H - P/tauP
EQ7 = omath(
    d('P') + op('=') + mr('G') + op('+') + mr('b') + sp() +
    mfrac(mr('J'), msub(mr('τ'), mr('J'))) + op('−') + mr('H') + op('−') +
    mfrac(mr('P'), msub(mr('τ'), mr('P')))
)

# (8) dJ/dt = H - rho - J/tauJ,  rho = J/tau
EQ8 = omath(
    d('J') + op('=') + mr('H') + op('−') + mr('ρ') + op('−') +
    mfrac(mr('J'), msub(mr('τ'), mr('J'))) + mr(',    ', upright=True) +
    mr('ρ') + op('=') + mfrac(mr('J'), mr('τ'))
)

# (9) dS/dt = rho - S/tauS
EQ9 = omath(
    d('S') + op('=') + mr('ρ') + op('−') + mfrac(mr('S'), msub(mr('τ'), mr('S')))
)

# (10) dQ/dt = G + b J/tauJ - (H + P/tauP) K - delta Q,  K = Q/P
EQ10 = omath(
    d('Q') + op('=') + mr('G') + op('+') + mr('b') + sp() +
    mfrac(mr('J'), msub(mr('τ'), mr('J'))) + op('−') +
    mdelim(mr('H') + op('+') + mfrac(mr('P'), msub(mr('τ'), mr('P')))) + mr('K') +
    op('−') + mr('δ') + mr('Q') + mr(',    ', upright=True) + mr('K') + op('=') +
    mfrac(mr('Q'), mr('P'))
)

# (11) M = max{ rho_m S , (1-u*)S - max(0, L - u* S) },  m = min(m* J, M)/J
EQ11 = omath(
    mr('M') + op('=') + num('max') + sp() +
    brace(msub(mr('r'), mr('m')) + mr('S') + mr(', ', upright=True) +
          mdelim(num('1') + op('−') + msup(mr('u'), mr('∗'))) + mr('S') + op('−') +
          num('max') + mdelim(num('0') + mr(', ', upright=True) + mr('L') + op('−') +
                              msup(mr('u'), mr('∗')) + mr('S'))) +
    mr(',    ', upright=True) + mr('m') + op('=') +
    mfrac(num('min') + mdelim(msup(mr('m'), mr('∗')) + mr('J') +
                              mr(', ', upright=True) + mr('M')), mr('J'))
)

# (12) tau = tau0 / (Lm Le Lk)
EQ12 = omath(
    mr('τ') + op('=') + mfrac(msub(mr('τ'), num('0')),
                              msub(mr('L'), mr('m')) + sp() +
                              msub(mr('L'), mr('e')) + sp() +
                              msub(mr('L'), mr('k')))
)

# (13) Lm = ((m+mf)/(m*+mf))^a ; Le = 1 - (theta - lambda) A ; Lk = K^cq
EQ13 = omath(
    msub(mr('L'), mr('m')) + op('=') +
    msup(mdelim(mfrac(mr('m') + op('+') + msub(mr('m'), mr('f')),
                      msup(mr('m'), mr('∗')) + op('+') + msub(mr('m'), mr('f')))),
         mr('a')) + mr(',    ', upright=True) +
    msub(mr('L'), mr('e')) + op('=') + num('1') + op('−') +
    mdelim(mr('θ') + op('−') + mr('λ')) + mr('A') + mr(',    ', upright=True) +
    msub(mr('L'), mr('k')) + op('=') + msup(mr('K'), mr('κ'))
)

# (14) Y = piJ J + q A R + piS (S - V - M)
EQ14 = omath(
    mr('Y') + op('=') + msub(mr('π'), mr('J')) + mr('J') + op('+') + mr('q') +
    sp() + mr('A') + sp() + mr('R') + op('+') + msub(mr('π'), mr('S')) +
    mdelim(mr('S') + op('−') + mr('V') + op('−') + mr('M'))
)

# (15) dW/dt = (w~ - W)/tauW ,  w~ = (Sdes - S)/Sdes
EQ15 = omath(
    d('W') + op('=') + mfrac(mr('ω') + op('−') + mr('W'), msub(mr('τ'), mr('W'))) +
    mr(',    ', upright=True) + mr('ω') + op('=') +
    mfrac(msub(mr('S'), mr('des')) + op('−') + mr('S'), msub(mr('S'), mr('des')))
)

EQUATIONS_P7 = {
    'eq1': EQ1, 'eq2': EQ2, 'eq3': EQ3, 'eq4': EQ4, 'eq5': EQ5,
    'eq6': EQ6, 'eq7': EQ7, 'eq8': EQ8, 'eq9': EQ9, 'eq10': EQ10,
    'eq11': EQ11, 'eq12': EQ12, 'eq13': EQ13, 'eq14': EQ14, 'eq15': EQ15,
}
