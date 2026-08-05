#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 1—2 步：数据审计 + 描述性测算。全部结果写入 results.json 供绘图与正文引用。"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from case_data import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results.json')
res = {}

print('=' * 66)
print('第 1 步  数据审计')
print('=' * 66)
print(f'观测单位：单一企业（浙江嘉兴数字城市实验室有限公司）')
print(f'数据性质：案例稿自述数据，非抽样调查数据；不存在样本量与统计推断')
print(f'治理提效观测环节数：{len(GOVERNANCE_EFFICIENCY)}')
print(f'人才规模观测点数：{len(HEADCOUNT)}（稿件仅给出三个时点，无逐年数据）')
print(f'资质记录阶段数：{len(QUALIFICATION)}，覆盖 {QUALIFICATION[0]["年份"]}—{QUALIFICATION[-1]["年份"]}')
print(f'垂直解决方案领域数：{len(SOLUTIONS)}')
print()
print('口径冲突（必须先报告）：')
for i, x in enumerate(INCONSISTENCIES, 1):
    print(f'  [{i}] {x["指标"]}')
    print(f'      A: {x["表述A"]}  （{x["出处A"]}）')
    print(f'      B: {x["表述B"]}  （{x["出处B"]}）')
    print(f'      处置: {x["处置"]}')
res['inconsistencies'] = INCONSISTENCIES

print()
print('=' * 66)
print('第 2 步  描述性测算')
print('=' * 66)

# --- 2.1 治理提效 ---
print('\n[2.1] 关键业务环节时耗压缩')
print(f'  工作日折算假设：1 个工作日 = {HOURS_PER_WORKDAY} 小时')
eff = []
for r in GOVERNANCE_EFFICIENCY:
    b, a = r['before_min'], r['after_min']
    comp = (b - a) / b                 # 时耗压缩率
    mult = b / a                       # 效率提升倍数
    saved = b - a
    eff.append({**{k: r[k] for k in ('环节', '传统方式', '数字化方式',
                                     'before_raw', 'after_raw', 'before_min',
                                     'after_min', 'source')},
                '压缩率': round(comp, 4), '提升倍数': round(mult, 2), '节省分钟': saved})
    print(f'  {r["环节"]}: {r["before_raw"]}({b} 分钟) -> {r["after_raw"]}({a} 分钟)  '
          f'压缩率 {comp:.2%}  效率提升 {mult:.1f} 倍  单次节省 {saved} 分钟')
avg_comp = sum(e['压缩率'] for e in eff) / len(eff)
print(f'  两环节平均时耗压缩率：{avg_comp:.2%}')
res['efficiency'] = eff
res['efficiency_avg_compression'] = round(avg_comp, 4)
res['hours_per_workday'] = HOURS_PER_WORKDAY

# --- 2.2 人才规模 ---
print('\n[2.2] 人才规模与研发结构')
n0, n1, n2 = [h['人数'] for h in HEADCOUNT]
growth_total = (n2 - n0) / n0
growth_p1 = (n1 - n0) / n0
growth_p2 = (n2 - n1) / n1
rd = n2 * RD_SHARE
print(f'  成立初期 {n0} 人 -> 扩充期 {n1} 人 -> 调研时点 {n2} 人')
print(f'  阶段一增幅 {growth_p1:.1%}；阶段二增幅 {growth_p2:.1%}；累计增幅 {growth_total:.1%}（{n2/n0:.0f} 倍）')
print(f'  研发技术人员约 {rd:.0f} 人（{RD_SHARE:.0%} 下界）；{RD_SHARE_NOTE}')
res['headcount'] = {'points': HEADCOUNT, 'rd_share': RD_SHARE, 'rd_headcount_lower': int(rd),
                    'growth_total': round(growth_total, 4),
                    'growth_p1': round(growth_p1, 4), 'growth_p2': round(growth_p2, 4),
                    'multiple': round(n2 / n0, 2), 'rd_share_note': RD_SHARE_NOTE}

# --- 2.3 资质累计 ---
print('\n[2.3] 资质认证累计进阶')
cum, running = [], 0
for q in QUALIFICATION:
    running += len(q['资质'])
    cum.append({'阶段': q['阶段'], '年份': q['年份'], '当期新增': len(q['资质']),
                '累计': running, '能力维度': q['能力维度'], '资质': q['资质']})
    print(f'  {q["年份"]} {q["阶段"]}: 新增 {len(q["资质"])} 项，累计 {running} 项 —— {q["能力维度"]}')
res['qualification'] = cum
res['qualification_total'] = running

# --- 2.4 产品结构 ---
print('\n[2.4] 解决方案与产品结构')
from collections import Counter
c = Counter(s['属性'] for s in SOLUTIONS)
for k, v in c.most_common():
    print(f'  {k}: {v} 个领域，占 {v/len(SOLUTIONS):.1%}')
liv_n = PRODUCT_TOTAL * PRODUCT_LIVELIHOOD_SHARE
print(f'  数字化产品共 {PRODUCT_TOTAL} 个，民生类占比 {PRODUCT_LIVELIHOOD_SHARE:.0%}，约 {liv_n:.0f} 个')
res['solutions'] = {'by_attribute': dict(c), 'domains': SOLUTIONS,
                    'product_total': PRODUCT_TOTAL,
                    'livelihood_share': PRODUCT_LIVELIHOOD_SHARE,
                    'livelihood_count': int(liv_n)}

json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'\n结果已写入 {OUT}')
