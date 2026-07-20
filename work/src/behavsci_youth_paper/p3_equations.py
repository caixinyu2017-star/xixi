# -*- coding: utf-8 -*-
"""Display equations (OMML) for paper 3."""
from bs_builder import mr, msub, msup, mfrac, msum, mdelim, macc, omath

def _sub(a, b):
    return msub(mr(a), mr(b))

EQUATIONS_P3 = {}

# (1) LLM composite: S̄_i = (1/(M R)) Σ_{m=1}^{M} Σ_{r=1}^{R} S_{i m r}
EQUATIONS_P3['composite'] = omath(
    msub(macc(mr('S')), mr('i')) + mr('=', upright=True)
    + mfrac(mr('1'), mr('MR'))
    + msum(mr('m') + mr('=', upright=True) + mr('1'), mr('M'),
           msum(mr('r') + mr('=', upright=True) + mr('1'), mr('R'),
                msub(mr('S'), mr('imr')))))

# (2) ICC(2,1) = (MS_R − MS_E) / (MS_R + (k−1)MS_E + (k/n)(MS_C − MS_E))
_msr = _sub('MS', 'R'); _mse = _sub('MS', 'E'); _msc = _sub('MS', 'C')
EQUATIONS_P3['icc'] = omath(
    mr('ICC', upright=True) + mdelim(mr('2,1', upright=True))
    + mr('=', upright=True)
    + mfrac(_msr + mr('−') + _mse,
            _msr + mr('+') + mdelim(mr('k') + mr('−') + mr('1')) + _mse
            + mr('+') + mfrac(mr('k'), mr('n'))
            + mdelim(_msc + mr('−') + _mse)))

# (3) hierarchical model: Y_i = β0 + B1' D_i + B2' Q_i + γ S̄_i + ε_i
EQUATIONS_P3['hier'] = omath(
    _sub('Y', 'i') + mr('=', upright=True) + _sub('β', '0')
    + mr('+') + msup(msub(mr('B'), mr('1')), mr('⊤'))
    + msub(mr('D'), mr('i'))
    + mr('+') + msup(msub(mr('B'), mr('2')), mr('⊤'))
    + msub(mr('Q'), mr('i'))
    + mr('+') + mr('γ') + msub(macc(mr('S')), mr('i'))
    + mr('+') + _sub('ε', 'i'))

# (4) silhouette: s(i) = (b(i) − a(i)) / max{a(i), b(i)}
EQUATIONS_P3['sil'] = omath(
    mr('s') + mdelim(mr('i')) + mr('=', upright=True)
    + mfrac(mr('b') + mdelim(mr('i')) + mr('−') + mr('a') + mdelim(mr('i')),
            mr('max', upright=True) + mdelim(mr('a') + mdelim(mr('i')) + mr(',', upright=True)
                                             + mr('b') + mdelim(mr('i')), left='{', right='}')))
