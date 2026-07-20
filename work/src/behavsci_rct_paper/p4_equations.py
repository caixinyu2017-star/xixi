# -*- coding: utf-8 -*-
"""Display equations (OMML) for paper 4 (RCT)."""
from bs_builder import mr, msub, msup, mfrac, mdelim, macc, omath

def _sub(a, b):
    return msub(mr(a), mr(b))

EQUATIONS_P4 = {}

# (1) LMM: Y_it = b0 + b1 G_i + b2 W4_t + b3 W8_t + b4 G x W4 + b5 G x W8 + u_i + e_it
EQUATIONS_P4['lmm'] = omath(
    msub(mr('Y'), mr('it')) + mr('=', upright=True) + _sub('β', '0')
    + mr('+') + _sub('β', '1') + msub(mr('G'), mr('i'))
    + mr('+') + _sub('β', '2') + msub(mr('W4', upright=True), mr('t'))
    + mr('+') + _sub('β', '3') + msub(mr('W8', upright=True), mr('t'))
    + mr('+') + _sub('β', '4') + mdelim(msub(mr('G'), mr('i')) + mr('×', upright=True) + msub(mr('W4', upright=True), mr('t')))
    + mr('+') + _sub('β', '5') + mdelim(msub(mr('G'), mr('i')) + mr('×', upright=True) + msub(mr('W8', upright=True), mr('t')))
    + mr('+') + _sub('u', 'i') + mr('+') + msub(mr('ε'), mr('it')))

# (2) adjusted effect size: d = J * b_G / SD_baseline
EQUATIONS_P4['dsize'] = omath(
    mr('d') + mr('=', upright=True) + mr('J', upright=True) + mr('·', upright=True)
    + mfrac(msup(msub(mr('β'), mr('G')), mr('adj')),
            msub(mr('SD'), mr('baseline'))))

# (3) indirect effect: ab, with c = c' + ab
EQUATIONS_P4['med'] = omath(
    msub(mr('θ'), mr('indirect')) + mr('=', upright=True)
    + mr('a') + mr('·', upright=True) + mr('b')
    + mr(',', upright=True) + mr('  c') + mr('=', upright=True)
    + mr('c') + mr('′') + mr('+') + mr('a') + mr('·', upright=True) + mr('b'))

# (4) dose-response: dY_i = g0 + g1 S_i + g2 Y_i0 + e_i
EQUATIONS_P4['dose'] = omath(
    mr('Δ') + msub(mr('Y'), mr('i')) + mr('=', upright=True) + _sub('γ', '0')
    + mr('+') + _sub('γ', '1') + msub(mr('S'), mr('i'))
    + mr('+') + _sub('γ', '2') + msub(mr('Y'), mr('i0'))
    + mr('+') + _sub('ε', 'i'))
