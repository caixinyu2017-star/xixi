# -*- coding: utf-8 -*-
"""《价值 & 开发》 — 60 页，亚德客营业部人员 / 中层管理者，全日 6 小时。

课纲来自客户提供的《价值&开发》教学计划（四讲：理解 / 评估 / 开发 / 落地），
理论一笔带过，重心放在可以当天动手的口径与动作；公司与行业事实来自公开检索
（见 PR 说明），凡查不到的一律不写死数字。

  · 6 页情境模拟问答，反常识做法放在备注，讨论后再揭示；
  · 第 2 页开场团队任务（说困境）、第 60 页结课团队任务（综合情境分析）；
  · 正文 18~24pt，行列用 vspan / hspan 精确等分，lint 带覆盖率检查确保不留大片空白；
  · 备注里穿插短段子，用于换气。
"""
import os

import course3_a, course3_b, course3_c          # noqa: F401
from course3_a import S, COURSE, SEC
from deckkit import Slide
from components import chrome, artwork
from lint import check
from fixup import fit_all
from pack import build

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = '/home/user/xixi/管理技能课-价值与开发.pptx'

# 模型页：内容区整块换成生成的示意图（框架保留，其余 52 页全部是原生可编辑形状）
ART = {
    9:  'v9_iceberg.fit.png',    # 冰山模型
    16: 'v16_flow.fit.png',      # 价值流四台阶
    21: 'v21_funnel.fit.png',    # 销售漏斗与过程指标
    26: 'v26_ninebox.fit.png',   # 九宫格
    36: 'v36_702010.fit.png',    # 70-20-10
    37: 'v37_ojt.fit.png',       # OJT 四台阶
    42: 'v42_tco.fit.png',       # 四个算账锚点
    52: 'v52_grow.fit.png',      # GROW
}


def assemble(use_art=True):
    slides = list(S)
    assert len(slides) == 60, len(slides)
    swapped, missing = [], []
    if use_art:
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
            s.notes_text = list(getattr(old, 'notes_text', []))  # keep 讲法与段子
            slides[n - 1] = s
            swapped.append(n)
        if swapped:
            print('示意图页：', swapped)
        if missing:
            print('仍用原生图形的页（尚无成图）：', missing)
    return fit_all(slides)


if __name__ == '__main__':
    import sys
    use_art = '--no-art' not in sys.argv
    slides = assemble(use_art)
    issues = check(slides, coverage=True)
    assert not issues, f'{len(issues)} 处布局问题'
    notes = sum(1 for s in slides if getattr(s, 'notes_text', None))
    print(build(slides, OUT, title='价值 & 开发｜亚德客企业内训'),
          len(slides), '页，备注', notes, '页')
