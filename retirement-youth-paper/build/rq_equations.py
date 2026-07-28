# -*- coding: utf-8 -*-
"""Display equations of the rationing model, written as native Word OMML."""
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


def _sub2(base, sub, sup):
    return ('<m:sSubSup><m:sSubSupPr/><m:e>' + base + '</m:e>'
            '<m:sub>' + sub + '</m:sub><m:sup>' + sup + '</m:sup></m:sSubSup>')


# short-hands ---------------------------------------------------------------
r_ = mr('r')
gam = mr('γ')
rho = mr('ρ')
eta = mr('η')
beta = mr('β')
dQ = msub(mr('δ'), mr('Q'))
dM = msub(mr('δ'), mr('M'))
lamQ = msub(mr('λ'), mr('Q'))
muy = msub(mr('μ'), mr('y'))
th = mr('θ')
uq, um, eq_, em = (msub(mr('u'), mr('q')), msub(mr('u'), mr('m')),
                   msub(mr('e'), mr('q')), msub(mr('e'), mr('m')))
Um, Eq, Em = msub(mr('U'), mr('m')), msub(mr('E'), mr('q')), msub(mr('E'), mr('m'))
fy, fp = msub(mr('f'), mr('y')), msub(mr('f'), mr('p'))
Jy, Jp = msub(mr('J'), mr('y')), msub(mr('J'), mr('p'))
Vy, Vp = msub(mr('V'), mr('y')), msub(mr('V'), mr('p'))
Dy, Dp = msub(mr('Δ'), mr('y')), msub(mr('Δ'), mr('p'))
wy, wp, wQ = msub(mr('w'), mr('y')), msub(mr('w'), mr('p')), msub(mr('w'), mr('Q'))
Wqy = _sub2(mr('W'), mr('q'), mr('y'))
Wqp = _sub2(mr('W'), mr('q'), mr('p'))
Nb = _bar(mr('N'))
vQ, vM = msub(mr('v'), mr('Q')), msub(mr('v'), mr('M'))
cM = msub(mr('c'), mr('M'))
pM, pQ = msub(mr('p'), mr('M')), msub(mr('p'), mr('Q'))
b_ = mr('b')
kap = msub(mr('κ'), mr('q'))
Ty = msub(mr('T'), mr('y'))
a0 = msub(mr('a'), mr('0'))
Se = msub(mr('S'), mr('e'))
sv = msub(mr('s'), mr('v'))
sN = msub(mr('s'), mr('N'))
tq = msub(mr('τ'), mr('q'))
ONE = mr('1')


# (1) age structure ----------------------------------------------------------
EQ1 = omath(
    gam + _op('=') + mfrac(ONE, Ty) + mr(', ') + _sp() + _sp() +
    rho + _op('=') + mfrac(ONE, mr('R') + _op('−') + a0 + _op('−') + Ty))

# (2) matching ---------------------------------------------------------------
EQ2 = omath(
    mr('M') + mdelim(Se + mr(', ') + vM) + _op('=') + msup(Se, eta) + _sp() +
    msup(vM, ONE + _op('−') + eta) + mr(', ') + _sp() + _sp() +
    th + _op('=') + mfrac(vM, Se) + mr(', ') + _sp() + _sp() +
    Se + _op('=') + muy + um + _op('+') + Um)

# (3) hazards ----------------------------------------------------------------
EQ3 = omath(
    fp + _op('=') + msup(th, ONE + _op('−') + eta) + mr(', ') + _sp() + _sp() +
    fy + _op('=') + muy + _sp() + msup(th, ONE + _op('−') + eta) + mr(', ') +
    _sp() + _sp() + mr('q') + mdelim(th) + _op('=') + msup(th, _op('−') + eta))

# (4) young stocks -----------------------------------------------------------
EQ4 = omath(
    _dot(uq) + _op('=') + msub(mr('a'), mr('q')) + msub(mr('I'), mr('y')) +
    _op('−') + mdelim(lamQ + _op('+') + gam) + uq + mr(', ') + _sp() + _sp() +
    _dot(um) + _op('=') + mdelim(ONE + _op('−') + msub(mr('a'), mr('q'))) +
    msub(mr('I'), mr('y')) + _op('−') + mdelim(fy + _op('+') + gam) + um)

EQ5 = omath(
    _dot(eq_) + _op('=') + lamQ + uq + _op('−') + mdelim(dQ + _op('+') + gam) +
    eq_ + mr(', ') + _sp() + _sp() +
    _dot(em) + _op('=') + fy + um + _op('−') + mdelim(dM + _op('+') + gam) + em)

# (6) prime stocks -----------------------------------------------------------
EQ6 = omath(
    _dot(Um) + _op('=') + gam + mdelim(uq + _op('+') + um) + _op('+') + dQ +
    Eq + _op('+') + dM + Em + _op('−') + mdelim(fp + _op('+') + rho) + Um)

EQ7 = omath(
    _dot(Eq) + _op('=') + gam + eq_ + _op('−') + mdelim(dQ + _op('+') + rho) +
    Eq + mr(', ') + _sp() + _sp() +
    _dot(Em) + _op('=') + gam + em + _op('+') + fp + Um + _op('−') +
    mdelim(dM + _op('+') + rho) + Em)

# (8) the establishment constraint and the vacancy flow it implies -----------
EQ8 = omath(
    eq_ + _op('+') + Eq + _op('=') + Nb + mdelim(ONE + _op('+') + sN) +
    mr(', ') + _sp() + _sp() + vQ + _op('=') + dQ + Nb + _op('+') + rho + Eq +
    _op('=') + mdelim(dQ + _op('+') + gam) + eq_)

# (9) the queue hazard -------------------------------------------------------
EQ9 = omath(
    lamQ + _op('=') + mfrac(vQ, uq) + _op('=') +
    mfrac(mdelim(dQ + _op('+') + gam) + Nb + mdelim(dQ + _op('+') + rho),
          uq + mdelim(dQ + _op('+') + rho + _op('+') + gam)))

# (10) market match values ---------------------------------------------------
EQ10 = omath(
    mdelim(r_ + _op('+') + dM + _op('+') + rho) + Jp + _op('=') + pM + _op('−') +
    wp + mr(', ') + _sp() + _sp() +
    mdelim(r_ + _op('+') + dM + _op('+') + gam) + Jy + _op('=') + pM +
    _op('−') + wy + _op('+') + gam + Jp)

# (11) worker surpluses ------------------------------------------------------
EQ11 = omath(
    mdelim(r_ + _op('+') + dM + _op('+') + fp + _op('+') + rho) + Dp + _op('=') +
    wp + _op('−') + b_ + mr(', ') + _sp() + _sp() +
    mdelim(r_ + _op('+') + dM + _op('+') + fy + _op('+') + gam) + Dy +
    _op('=') + wy + _op('−') + b_ + _op('+') + gam + Dp)

# (12) Nash bargaining -------------------------------------------------------
EQ12 = omath(
    beta + _sp() + msub(mr('J'), mr('i')) + _op('=') +
    mdelim(ONE + _op('−') + beta) + msub(mr('Δ'), mr('i')) + mr(', ') + _sp() +
    _sp() + mr('i') + _op('∈') + mdelim(mr('y') + mr(', ') + mr('p'), '{', '}'))

# (13) search values ---------------------------------------------------------
EQ13 = omath(
    mdelim(r_ + _op('+') + rho) + Vp + _op('=') + b_ + _op('+') + fp + Dp +
    mr(', ') + _sp() + _sp() +
    mdelim(r_ + _op('+') + gam) + Vy + _op('=') + b_ + _op('+') + fy + Dy +
    _op('+') + gam + Vp)

# (14) the value of a rationed job -------------------------------------------
EQ14 = omath(
    mdelim(r_ + _op('+') + dQ + _op('+') + rho) + Wqp + _op('=') +
    wQ + mdelim(ONE + _op('−') + tq) + _op('+') + dQ + Vp + mr(', ') + _sp() +
    _sp() + mdelim(r_ + _op('+') + dQ + _op('+') + gam) + Wqy + _op('=') +
    wQ + mdelim(ONE + _op('−') + tq) + _op('+') + dQ + Vy + _op('+') + gam + Wqp)

# (15) the Harris-Todaro indifference condition ------------------------------
EQ15 = omath(
    mdelim(r_ + _op('+') + gam) + Vy + _op('=') + kap + b_ + _op('+') + lamQ +
    mdelim(Wqy + _op('−') + Vy) + _op('+') + gam + Vp)

# (16) the queue length it implies -------------------------------------------
EQ16 = omath(
    lamQ + _op('=') +
    mfrac(mdelim(r_ + _op('+') + gam) + Vy + _op('−') + kap + b_ + _op('−') +
          gam + Vp, Wqy + _op('−') + Vy) + mr(', ') + _sp() + _sp() +
    uq + _op('=') + mfrac(vQ, lamQ))

# (17) free entry ------------------------------------------------------------
EQ17 = omath(
    mfrac(cM + mdelim(ONE + _op('−') + sv), mr('q') + mdelim(th)) + _op('=') +
    msub(mr('ω'), mr('y')) + Jy + _op('+') +
    mdelim(ONE + _op('−') + msub(mr('ω'), mr('y'))) + Jp + mr(', ') + _sp() +
    _sp() + msub(mr('ω'), mr('y')) + _op('=') + mfrac(muy + um, Se))

# (18) output and welfare ----------------------------------------------------
EQ18 = omath(
    mr('Y') + _op('=') + pQ + Nb + mdelim(ONE + _op('+') + sN) + _op('+') + pM +
    mdelim(em + _op('+') + Em))

EQ19 = omath(
    mr('𝒲') + _op('=') + mr('Y') + _op('−') + cM + vM + _op('+') + b_ +
    mdelim(um + _op('+') + Um) + _op('+') + kap + b_ + uq)

# (20) the output forgone by the queue ---------------------------------------
EQ20 = omath(
    _up('L') + _op('=') + uq + mdelim(pM + _op('−') + kap + b_))

# (21) the crowding-out coefficient ------------------------------------------
EQ21 = omath(
    mr('Ξ') + _op('=') +
    mfrac(mr('Δ') + mdelim(eq_ + _op('+') + em),
          mr('Δ') + mdelim(Eq + _op('+') + Em)))

# (22) estimation criterion --------------------------------------------------
EQ22 = omath(
    '<m:nary><m:naryPr><m:chr m:val="∑"/><m:limLoc m:val="subSup"/>'
    '</m:naryPr><m:sub>' + mr('k') + _op('=') + ONE +
    '</m:sub><m:sup>' + mr('6') + '</m:sup><m:e>' +
    msup(mdelim(_up('ln') + _sp() + msub(mr('m'), mr('k')) + mdelim(mr('Θ')) +
                _op('−') + _up('ln') + _sp() + _bar(msub(mr('m'), mr('k')))),
         mr('2')) + '</m:e></m:nary>' + _op('=') + mr('0'))

# (23) marginal value of public funds ----------------------------------------
EQ23 = omath(
    _up('MVPF') + _op('=') + ONE + _op('+') +
    mfrac(mr('Δ') + mr('𝒲'), mr('G')))

# (24) break-even screening value --------------------------------------------
EQ24 = omath(
    msup(mr('ξ'), mr('*')) + _op('=') +
    mfrac(uq + mdelim(pM + _op('−') + kap + b_), pQ + Nb))

EQUATIONS = {'eq%d' % i: e for i, e in enumerate(
    [EQ1, EQ2, EQ3, EQ4, EQ5, EQ6, EQ7, EQ8, EQ9, EQ10, EQ11, EQ12, EQ13,
     EQ14, EQ15, EQ16, EQ17, EQ18, EQ19, EQ20, EQ21, EQ22, EQ23, EQ24],
    start=1)}
