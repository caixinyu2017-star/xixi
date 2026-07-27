"""Best solutions for the two illustrative figures.

Figure 12 shows the optimized palettes and the harmonic template that best
fits the MSSBOA palette; Figure 15 shows representative layouts.  Both need an
actual decision vector, which the statistical runs do not keep, so the best of
a small set of seeded repetitions is recomputed here with the same algorithms
and the same budget as run_all.py.
"""
import json
import os
import sys
import zlib

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results')

from design_problems import (color_problem, layout_problem,       # noqa: E402
                             LAYOUT_PROBLEMS, best_template)
from run_all import MAIN, MAIN_ORDER, POP, DESIGN_FES             # noqa: E402

REPS = 8
LAYOUT_CODES = ('DL01', 'DL04', 'DL06')


def _seed(*p):
    return int(zlib.crc32('|'.join(map(str, p)).encode()) % (2 ** 32))


def main():
    out = {}
    for algo in MAIN_ORDER:
        prob = color_problem(7)
        best = (-np.inf, None)
        for r in range(REPS):
            bf, bx, _ = MAIN[algo](prob, DESIGN_FES, POP,
                                   np.random.default_rng(_seed('c', algo, r)))
            if -bf > best[0]:
                best = (-float(bf), np.asarray(bx, float))
        t, a = best_template(best[1], 7)
        out[f'color|{algo}|7'] = {'score': best[0],
                                  'palette': best[1].reshape(7, 3).tolist(),
                                  'template': t, 'alpha': a}
        print(f'  colour  {algo:7s} {best[0] * 100:6.2f}%  template {t} @ {a:.0f}deg',
              flush=True)

    for algo in ('MSSBOA', 'SBOA'):
        for code in LAYOUT_CODES:
            prob = layout_problem(code)
            best = (-np.inf, None)
            for r in range(REPS):
                bf, bx, _ = MAIN[algo](prob, DESIGN_FES, POP,
                                       np.random.default_rng(_seed('l', algo, code, r)))
                if -bf > best[0]:
                    best = (-float(bf), np.asarray(bx, float))
            out[f'layout|{algo}|{code}'] = {'score': best[0],
                                            'x': best[1].tolist()}
            print(f'  layout  {algo:7s} {code} {best[0] * 100:6.2f}', flush=True)

    json.dump(out, open(os.path.join(RES, 'design_best.json'), 'w'))
    print('wrote design_best.json')


if __name__ == '__main__':
    main()
