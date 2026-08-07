# -*- coding: utf-8 -*-
"""Match a generated PNG to the slide's content rectangle without distorting it.

The gateway decides its own output aspect, so the picture rarely lands exactly
on the 11.22 x 6.04 inch content area. Rather than stretching the artwork —
which visibly widens Chinese glyphs — this pads the short axis by replicating
the edge pixels. Every one of these posters carries full-width colour bands at
the top and bottom, so edge replication extends those bands seamlessly and the
padding is invisible.
"""
import os
from PIL import Image

TARGET = 11.22 / 6.04
TOL = 0.025            # below this the residual stretch is imperceptible


def fit(src, dst=None, target=TARGET, tol=TOL):
    dst = dst or src
    im = Image.open(src).convert('RGB')
    w, h = im.size
    ratio = w / h
    if abs(ratio - target) / target <= tol:
        if dst != src:
            im.save(dst)
        return dst, (w, h), False

    if ratio < target:                       # too tall → widen
        nw, nh = int(round(h * target)), h
        pad = nw - w
        left, right = pad // 2, pad - pad // 2
        out = Image.new('RGB', (nw, nh))
        if left:
            out.paste(im.crop((0, 0, 1, h)).resize((left, h)), (0, 0))
        out.paste(im, (left, 0))
        if right:
            out.paste(im.crop((w - 1, 0, w, h)).resize((right, h)), (left + w, 0))
    else:                                    # too wide → heighten
        nw, nh = w, int(round(w / target))
        pad = nh - h
        top, bot = pad // 2, pad - pad // 2
        out = Image.new('RGB', (nw, nh))
        if top:
            out.paste(im.crop((0, 0, w, 1)).resize((w, top)), (0, 0))
        out.paste(im, (0, top))
        if bot:
            out.paste(im.crop((0, h - 1, w, h)).resize((w, bot)), (0, top + h))
    out.save(dst)
    return dst, (nw, nh), True


def fit_dir(d, target=TARGET):
    out = {}
    for n in sorted(os.listdir(d)):
        if n.endswith('.png') and not n.endswith('.fit.png'):
            src = os.path.join(d, n)
            out[n] = fit(src, src.replace('.png', '.fit.png'), target)
    return out


if __name__ == '__main__':
    for n, (p, size, padded) in fit_dir('art').items():
        print(f'{n:24s} {size[0]}x{size[1]} {"padded" if padded else "as-is"}')
