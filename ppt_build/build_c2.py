# -*- coding: utf-8 -*-
"""《问题分析与解决》 — 60 页。

改版要点（客户第二轮意见）：
  1. 全篇正文最小 18pt，连贯的句子不再人工断行；
  2. 顶部课程名居中，第一/二/三节导航框加宽到单行；
  3. 情境 1~6 的「反常识做法」移到备注，屏幕上的三块放大铺满；
  4. 理论/知识页改用 gpt-image-2 生成的示意图，铺满除框架外的内容区；
  5. 出图前用 lint 逐页核对：不溢出、不遮挡。
"""
import os

import course2_a, course2_b, course2_c          # noqa: F401
from course2_a import S, COURSE, SEC
from course2_c import EXTRA
from deckkit import Slide
from components import chrome, artwork
from lint import check
from fixup import fit_all
from pack import build

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = '/home/user/xixi/管理技能课-问题分析与解决.pptx'

# 理论 / 知识传授页：内容区整块换成生成的示意图（框架保留）
ART = {
    5:  'p5_gap.fit.png',        # 问题 = 应有状态 − 现实状态
    7:  'p7_sangen.fit.png',     # 三现主义
    8:  'p8_w5h2.fit.png',       # 5W2H
    11: 'p11_iceberg.fit.png',   # 症状 / 问题 / 真因
    13: 'p13_pareto.fit.png',    # 柏拉图
    18: 'p18_strata.fit.png',    # 层别法
    22: 'p22_fivewhy.fit.png',   # 5Why
    24: 'p24_fishbone.fit.png',  # 鱼骨图 5M1E
    28: 'p28_threecond.fit.png',  # 真因三条件
    33: 'p33_fourlevel.fit.png',  # 对策四层次
    34: 'p34_pokayoke.fit.png',  # 防错法
    38: 'p38_sdca.fit.png',      # SDCA 标准化
}


def assemble():
    slides = S[:49] + EXTRA + [S[49]]     # 结课任务 must stay last
    assert len(slides) == 60, len(slides)
    swapped, missing = [], []
    for n, name in sorted(ART.items()):
        path = os.path.join(HERE, 'art', name)
        if not os.path.exists(path):
            missing.append(n)
            continue
        old = slides[n - 1]
        sec, side, sidebar = old.chrome_args
        s = Slide()
        chrome(s, COURSE, SEC, sec, sidebar, side)
        artwork(s, path)
        s.notes_text = list(getattr(old, 'notes_text', []))   # keep 讲法与段子
        slides[n - 1] = s
        swapped.append(n)
    if swapped:
        print('示意图页：', swapped)
    if missing:
        print('仍用原生图形的页（尚无成图）：', missing)
    return fit_all(slides)


if __name__ == '__main__':
    slides = assemble()
    issues = check(slides)
    assert not issues, f'{len(issues)} 处布局问题'
    notes = sum(1 for s in slides if getattr(s, 'notes_text', None))
    print(build(slides, OUT, title='问题分析与解决｜亚德客企业内训'),
          len(slides), '页，备注', notes, '页')
