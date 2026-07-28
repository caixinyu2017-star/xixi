# -*- coding: utf-8 -*-
"""Generate Figures 1 and 2 with the gpt-image-2 model, for comparison.

Image models render dense mathematical labelling unreliably, so each output is
inspected before it is allowed anywhere near the manuscript.
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
    'gold, muted brick red, teal green, medium grey. Serif labels, generous '
    'white space, boxes aligned on a strict grid, arrows must never cross a '
    'box and never overlap a label. All text in English, spelled exactly as '
    'given, no other text anywhere in the image.'
)

PROMPTS = {
    'fig1_v1': (
        'A worker-flow diagram of a two-tier career ladder, drawn as two '
        'horizontal rows on a strict grid. '
        'Upper row, two boxes side by side: "Entry-level jobseekers" on the '
        'left and "Entry-level employed" on the right, joined by a pair of '
        'opposite horizontal arrows, the upper one labelled "hiring" and the '
        'lower one labelled "separation". '
        'Lower row, directly beneath, two boxes: "Experienced jobseekers" and '
        '"Experienced employed", joined by the same pair of opposite '
        'horizontal arrows labelled "hiring" and "separation". '
        'One thick vertical arrow runs from "Entry-level employed" straight '
        'down to "Experienced employed", labelled "promotion". '
        'On the far left a small oval labelled "New entrants" has one '
        'horizontal arrow into "Entry-level jobseekers". '
        'A short horizontal arrow leaves "Experienced employed" to the right '
        'and ends at a small label "poached by rival firms". '
        'A single line of text at the bottom reads "Promotion is the only '
        'source of experienced workers". '
        + COMMON),

    'fig1_v2': (
        'A production-technology diagram, left to right in three columns on a '
        'strict grid. '
        'Column one, three boxes stacked vertically: "Experienced labour" at '
        'the top, "Entry-level labour" in the middle, "Artificial '
        'intelligence" at the bottom. '
        'Column two, two boxes: "Entry-level tasks" aligned with the middle '
        'of the figure and "Experienced tasks" below it. '
        'Column three, one box: "Output". '
        'Horizontal arrows: from "Entry-level labour" to "Entry-level '
        'tasks"; from "Artificial intelligence" to "Entry-level tasks", '
        'labelled "substitutes"; from "Experienced labour" to "Experienced '
        'tasks". Both task boxes have a horizontal arrow into "Output". '
        'Separately, above column two, a box labelled "Mentoring" receives a '
        'vertical arrow down from "Experienced labour" labelled "diverts '
        'senior time" and sends one horizontal arrow right into a box '
        'labelled "Promotion hazard". '
        'A single line of text at the bottom reads "Artificial intelligence '
        'raises task output but not the promotion hazard". '
        + COMMON),

    'fig2_v1': (
        'A two-column stacked-bar comparison, drawn as a clean academic '
        'schematic rather than a chart. '
        'On the left a tall column of two stacked rectangles under the '
        'heading "SOCIAL RETURN": the lower rectangle, in muted navy, is '
        'labelled "current task output"; the upper rectangle, in teal, is '
        'taller and labelled "value of creating an experienced worker". '
        'On the right, aligned to the same baseline, a second column under '
        'the heading "PRIVATE RETURN" with four stacked rectangles: the same '
        'navy "current task output" at the bottom, identical in height to the '
        'left column; above it a shorter solid teal rectangle labelled '
        '"firm keeps"; above that a hatched teal rectangle labelled "lost to '
        'hold-up"; and at the top a hatched gold rectangle labelled "lost to '
        'poaching". The two columns reach the same total height. '
        'Between the columns, two small caption boxes with one horizontal '
        'arrow each pointing right at the rectangle it explains: the lower '
        'box reads "hold-up", the upper box reads "poaching". '
        'To the left of the left column, two short vertical brace labels: '
        '"AI substitutes for this" beside the lower rectangle and "AI cannot '
        'substitute for this" beside the upper one. '
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
    for k in (sys.argv[1:] or list(PROMPTS)):
        generate(k)
