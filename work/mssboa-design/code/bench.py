"""CEC2017 problem wrapper and the function-class map used in the revision."""
import sys
import os

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from framework import Problem                                    # noqa: E402
from cec2017 import all_functions                                # noqa: E402

# F2 is excluded from the suite (unstable behaviour), leaving 29 functions.
CEC2017_IDS = [i for i in range(1, 31) if i != 2]

# Function classes of the CEC2017 suite - used for the loss-distribution
# analysis requested by Reviewer 1 (comment 4).
FUNCTION_CLASS = {}
for _i in CEC2017_IDS:
    if _i in (1, 3):
        FUNCTION_CLASS[_i] = 'Unimodal'
    elif 4 <= _i <= 10:
        FUNCTION_CLASS[_i] = 'Multimodal'
    elif 11 <= _i <= 20:
        FUNCTION_CLASS[_i] = 'Hybrid'
    else:
        FUNCTION_CLASS[_i] = 'Composition'

CLASS_ORDER = ['Unimodal', 'Multimodal', 'Hybrid', 'Composition']


def cec2017_problem(fid, dim):
    """Return a minimization Problem for CEC2017 function `fid` in `dim` D.

    The underlying implementation is vectorized over rows, so the problem is
    declared as batched and whole populations are evaluated in one call.
    """
    fn = all_functions[fid - 1]

    def fobj(X):
        return np.asarray(fn(np.atleast_2d(X)), dtype=float)

    return Problem(fobj, -100.0, 100.0, dim, f'F{fid}', batch=True)
