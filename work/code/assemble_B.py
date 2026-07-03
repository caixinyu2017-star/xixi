"""Assemble paper B into the final Word document."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content_paperB as C
from content_paperA import set_refs, resolve_refs
import make_results_B
from build_docx import PaperBuilder
from refs_data import REFS_ALL

OUT = '/home/user/xixi/work/out'
os.makedirs(OUT, exist_ok=True)
TEMPLATE = '/home/user/xixi/work/src/paper2_biomimetics_template.docx'
WORKDIR = '/tmp/claude-0/-home-user-xixi/57c8ca26-c69e-525b-bff7-40b46ed7b46f/scratchpad/bwB'


def main():
    st = make_results_B.main()
    set_refs(REFS_ALL)
    body = C.blocks(st) + C.blocks_experiments(st)
    body += [{'pagebreak': True}] + st['appendix']
    resolved, reflist = resolve_refs(body)
    resolved.append({'refs': reflist})

    b = PaperBuilder(TEMPLATE, WORKDIR)
    b.set_front_matter('Article', C.TITLE, C.AUTHORS, C.AFFILIATIONS,
                       C.abstract(st), C.KEYWORDS)
    b.build(resolved)
    out = f'{OUT}/MSBKA_Biomimetics.docx'
    b.save(out)
    print('saved', out, '| refs used:', len(reflist))


if __name__ == '__main__':
    main()
