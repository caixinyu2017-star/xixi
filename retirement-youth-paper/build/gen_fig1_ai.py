# -*- coding: utf-8 -*-
"""Generate Figure 1 (model structure) with the gpt-image-2 model.

Three variants are requested so that the cleanest one can be selected; image
models garble dense mathematical labelling, so the output is inspected before
it is allowed into the manuscript.
"""
import base64
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, '..', 'figs_ai'))

COMMON = (
    'Style requirements, follow exactly: a figure for an academic economics '
    'journal, pure white background, flat minimal vector style, thin-stroke '
    'rounded rectangles with white or very pale fill, thin solid arrows with '
    'small triangular heads, every connector strictly horizontal or vertical '
    'or a right-angle elbow, no curved or diagonal lines, no icons, no '
    'pictograms, no people, no clip art, no shadows, no gradients, no 3D, no '
    'background texture. Restrained academic palette only: dark navy, muted '
    'gold, muted brick red, medium grey. Serif labels, generous white space, '
    'boxes aligned on a strict grid, arrows must never cross a box and never '
    'overlap a label. All text in English, spelled exactly as given, no other '
    'text anywhere in the image.'
)

PROMPTS = {
    'fig1_v1': (
        'A worker-flow diagram of a two-sector labour market, drawn as two '
        'horizontal bands. The upper band is labelled YOUNG and the lower '
        'band is labelled PRIME-AGE. '
        'Upper band, four boxes left to right in one row: "Queueing", '
        '"Rationed job", "Open search", "Market job". '
        'Lower band, three boxes: "Rationed job", "Open search", '
        '"Market job", each aligned directly below its counterpart above. '
        'Horizontal arrows within the upper band: from "Queueing" to '
        '"Rationed job", and a pair of opposite horizontal arrows between '
        '"Open search" and "Market job". The same pair of opposite arrows in '
        'the lower band. Vertical downward arrows connect each upper box to '
        'the box directly below it, and these vertical arrows are dashed. '
        'On the far left a small oval labelled "Entrants" has two arrows into '
        '"Queueing" and "Open search". On the far right a small oval labelled '
        '"Retirement" receives one arrow from each lower-band job box. '
        'A single box below everything, spanning the width, reads '
        '"Establishment headcount fixed by administrative rule". '
        + COMMON),

    'fig1_v2': (
        'A two-sector labour-market stock-and-flow diagram on a strict grid, '
        'three columns and two rows. '
        'Row one is titled YOUNG, row two is titled PRIME-AGE, the titles set '
        'small and left-aligned above each row. '
        'Column one holds the box "Not employed", column two holds the box '
        '"Rationed sector job", column three holds the box "Market sector '
        'job". Six boxes in total, identical size, evenly spaced. '
        'Solid horizontal arrows run from column one to column two and from '
        'column one to column three in both rows, and a return arrow runs '
        'from column three back to column one in both rows. '
        'Dashed vertical arrows run from each box in row one down to the box '
        'directly beneath it in row two, labelled "ageing". '
        'A dashed arrow leaves each row-two box to the right towards a small '
        'label "retirement". '
        'A separate narrow box sits between the two rows in column two, '
        'reading "Vacancies = separations + retirements", with a short '
        'vertical arrow up into the row-one rationed job box. '
        + COMMON),

    'fig1_v3': (
        'A clean academic schematic of worker flows, arranged as a left-to-'
        'right pipeline with a branch. '
        'On the left a single box "Labour market entrants". Two arrows leave '
        'it: the upper arrow goes to a box "Examination queue", the lower '
        'arrow goes to a box "Open job search". '
        'From "Examination queue" one arrow goes right to a box "Rationed '
        'sector employment". From "Open job search" one arrow goes right to a '
        'box "Market sector employment", with a return arrow back. '
        'Both employment boxes have a dashed arrow going right to a final box '
        '"Retirement". '
        'Above the "Rationed sector employment" box, a smaller box reads '
        '"Fixed headcount", joined by a short vertical line. '
        'Below the "Market sector employment" box, a smaller box reads "Free '
        'entry", joined by a short vertical line. '
        'The two branches are visually separated: the rationed branch is '
        'drawn in muted gold, the market branch in dark navy. '
        + COMMON),
}


def generate(key, model='gpt-image-2'):
    api_key = os.environ.get('CHEDANKJ_API_KEY') or os.environ.get('OPENAI_API_KEY')
    if not api_key:
        sys.exit('no API key in the environment')
    os.makedirs(OUT, exist_ok=True)
    body = json.dumps({'model': model, 'prompt': PROMPTS[key],
                       'size': '1536x1024', 'quality': 'high'}).encode()
    base = os.environ.get('OPENAI_BASE_URL', 'https://www.chedankj.com').rstrip('/')
    req = urllib.request.Request(
        f'{base}/v1/images/generations', data=body,
        headers={'Authorization': f'Bearer {api_key}',
                 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            data = json.load(r)
        b64 = data['data'][0].get('b64_json')
        if b64 is None:
            with urllib.request.urlopen(data['data'][0]['url'], timeout=600) as r2:
                img = r2.read()
        else:
            img = base64.b64decode(b64)
        path = os.path.join(OUT, key + '.png')
        with open(path, 'wb') as f:
            f.write(img)
        print('ok %s -> %s (%d KB)' % (key, path, len(img) // 1024), flush=True)
    except Exception as e:                                    # noqa: BLE001
        msg = getattr(e, 'read', lambda: b'')()
        print('FAIL %s: %s %s' % (key, e, msg[:300]), file=sys.stderr, flush=True)


if __name__ == '__main__':
    keys = sys.argv[1:] or list(PROMPTS)
    for k in keys:
        generate(k)
