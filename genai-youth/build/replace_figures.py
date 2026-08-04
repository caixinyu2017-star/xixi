# -*- coding: utf-8 -*-
"""Replace figure images inside an existing .docx without touching anything else.

The manuscript the author edits by hand must not be regenerated, or those edits
are lost.  This script opens the author's file, swaps the bytes of the media
parts that hold the data figures, and rewrites the drawing extents so each
picture keeps its printed width with the new aspect ratio.  Every other part of
the package is copied through byte for byte.

Usage:  python3 replace_figures.py IN.docx OUT.docx
"""
from __future__ import annotations

import re
import shutil
import sys
import zipfile

from PIL import Image

EMU_PER_CM = 360000

# media part -> (replacement image, printed width in cm)
# the mapping is established by matching the byte size of the part already in
# the package against the figure files, so it does not depend on part numbering
REPLACEMENTS = [
    ('fig3_event_study.png', 11.5),
    ('fig4_psm_balance.png', 11.5),
    ('fig5_marginal_effect.png', 11.5),
    ('fig6_heterogeneity.png', 11.5),
    ('fig7_placebo.png', 11.5),
]

FIG_DIR = '../figures/'


def size_of(path):
    with Image.open(path) as im:
        return im.size


def build_map(zin, old_sizes):
    """Match each media part to a replacement by the byte size recorded earlier."""
    out = {}
    for item in zin.infolist():
        if not item.filename.startswith('word/media/'):
            continue
        for fname, width in REPLACEMENTS:
            if old_sizes.get(fname) == item.file_size:
                out[item.filename] = (fname, width)
    return out


def main(src, dst, old_sizes):
    zin = zipfile.ZipFile(src)
    mapping = build_map(zin, old_sizes)
    if len(mapping) != len(REPLACEMENTS):
        missing = {f for f, _ in REPLACEMENTS} - {v[0] for v in mapping.values()}
        raise SystemExit(f'could not locate media parts for: {sorted(missing)}')

    # new extents, in EMU, at the recorded printed width
    extents = {}
    for part, (fname, width_cm) in mapping.items():
        w_px, h_px = size_of(FIG_DIR + fname)
        cx = int(round(width_cm * EMU_PER_CM))
        cy = int(round(cx * h_px / w_px))
        extents[part] = (cx, cy)
        print(f'{part:22s} <- {fname:26s} {w_px}x{h_px}  ->  {cx} x {cy} EMU')

    doc = zin.read('word/document.xml').decode('utf8')
    rels = zin.read('word/_rels/document.xml.rels').decode('utf8')

    # relationship id -> media part
    rid_of = {}
    for m in re.finditer(r'<Relationship Id="([^"]+)"[^>]*Target="(media/[^"]+)"', rels):
        rid_of['word/' + m.group(2)] = m.group(1)

    n_fixed = 0
    for part, (cx, cy) in extents.items():
        rid = rid_of.get(part)
        if rid is None:
            raise SystemExit(f'no relationship found for {part}')
        # the <wp:inline> block that embeds this relationship
        pat = re.compile(r'<wp:inline\b.*?r:embed="%s".*?</wp:inline>' % re.escape(rid),
                         re.S)
        m = pat.search(doc)
        if m is None:
            raise SystemExit(f'no inline drawing found for {rid} ({part})')
        block = m.group(0)
        new = re.sub(r'(<wp:extent\s+cx=")\d+("\s+cy=")\d+(")',
                     lambda g: f'{g.group(1)}{cx}{g.group(2)}{cy}{g.group(3)}', block)
        new = re.sub(r'(<a:ext\s+cx=")\d+("\s+cy=")\d+(")',
                     lambda g: f'{g.group(1)}{cx}{g.group(2)}{cy}{g.group(3)}', new)
        doc = doc[:m.start()] + new + doc[m.end():]
        n_fixed += 1
    print(f'rewrote {n_fixed} drawing extents')

    with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if item.filename in mapping:
                with open(FIG_DIR + mapping[item.filename][0], 'rb') as f:
                    zout.writestr(item, f.read())
            elif item.filename == 'word/document.xml':
                zout.writestr(item, doc.encode('utf8'))
            else:
                zout.writestr(item, zin.read(item.filename))
    zin.close()
    print('wrote', dst)


if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    # byte sizes of the figures as they stand in the author's file, recorded
    # before the images were regenerated
    old = {
        'fig3_event_study.png': 156523,
        'fig4_psm_balance.png': 162891,
        'fig5_marginal_effect.png': 164637,
        'fig6_heterogeneity.png': 170040,
        'fig7_placebo.png': 121324,
    }
    main(src, dst, old)
