# cec2017-py by Duncan Tilley (MIT licence), vendored so that the revision
# experiments run against a faithful CEC2017 implementation.
# Source: https://github.com/tilleyd/cec2017-py
from . import basic
from . import simple
from . import hybrid
from . import composition
from . import transforms
from . import utils

all_functions = [
    simple.f1, simple.f2, simple.f3, simple.f4, simple.f5,
    simple.f6, simple.f7, simple.f8, simple.f9, simple.f10,
    hybrid.f11, hybrid.f12, hybrid.f13, hybrid.f14, hybrid.f15,
    hybrid.f16, hybrid.f17, hybrid.f18, hybrid.f19, hybrid.f20,
    composition.f21, composition.f22, composition.f23, composition.f24,
    composition.f25, composition.f26, composition.f27, composition.f28,
    composition.f29, composition.f30,
]
