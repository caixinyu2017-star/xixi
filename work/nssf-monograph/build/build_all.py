# -*- coding: utf-8 -*-
"""总装：chapters/*.md -> 书稿docx"""
import os, glob, json
from md2docx import build

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, 'chapters')

META = {
    'project': '国家社科基金后期资助项目',
    'category': '申　报　成　果',
    'title': '全国统一大市场建设与“内卷式”竞争治理研究',
    'subtitle': '——基于“市场分割—内卷竞争—统一红利”的理论与实证',
    'author': '蔡鑫宇　著',
}

ORDER = ['00_preface.md', '00b_abstract.md',
         '01.md', '02.md', '03.md', '04.md', '05.md', '06.md',
         '07.md', '08.md', '09.md', '10.md', '11.md', '12.md']

if __name__ == '__main__':
    files = [os.path.join(CH, f) for f in ORDER if os.path.exists(os.path.join(CH, f))]
    missing = [f for f in ORDER if not os.path.exists(os.path.join(CH, f))]
    if missing:
        print('缺章节文件：', missing)
    out = os.path.join(ROOT, 'output', '全国统一大市场建设与内卷式竞争治理研究（书稿）.docx')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    stats, used, unused = build(files, out, os.path.join(ROOT, 'plan', 'refs_db.json'), META)
    print(json.dumps(stats, ensure_ascii=False, indent=1))
    print('输出：', out)
