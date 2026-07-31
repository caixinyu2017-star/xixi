# -*- coding: utf-8 -*-
"""Cross-check every number that appears in the manuscript against p9_results.json."""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, 'p9_results.json')))


def flat(o, p=''):
    out = {}
    if isinstance(o, dict):
        for k, v in o.items():
            out.update(flat(v, p + '/' + k))
    elif isinstance(o, list):
        if o and isinstance(o[0], (int, float)):
            out[p] = o
        else:
            for i, v in enumerate(o):
                out.update(flat(v, p + '/%d' % i))
    else:
        out[p] = o
    return out


F = flat(R)
NUMS = {k: v for k, v in F.items() if isinstance(v, (int, float))}


def near(x, tol=5e-3):
    """Every stored value the manuscript figure could plausibly be rounded from."""
    hits = []
    for k, v in NUMS.items():
        if v is None:
            continue
        for cand in (v, 100.0 * v, abs(v)):
            if abs(cand) < 1e-12 and abs(x) < 1e-12:
                hits.append(k); break
            if abs(cand) > 1e-12 and abs(cand - x) <= tol * max(1.0, abs(x)):
                hits.append(k); break
    return hits


if __name__ == '__main__':
    import p9_content_a as A
    import p9_content_b as B
    text = []
    for mod in (A, B):
        for name in dir(mod):
            v = getattr(mod, name)
            if isinstance(v, (list, tuple, str)):
                text.append(str(v))
    blob = ' '.join(text)
    blob = re.sub(r'\{\{[^}]*\}\}', ' ', blob)
    blob = re.sub(r'⟪[^⟫]*⟫', ' ', blob)
    found = re.findall(r'(?<![\w.])(\d+\.\d+)(?![\w])', blob)
    miss = []
    for f in sorted(set(found)):
        x = float(f)
        if x in (1.0, 2.0, 0.5, 4.0, 3.0, 5.0):
            continue
        if not near(x):
            miss.append(f)
    print('distinct decimals in text: %d' % len(set(found)))
    print('unmatched: %d' % len(miss))
    for m in miss:
        print('   ', m)
