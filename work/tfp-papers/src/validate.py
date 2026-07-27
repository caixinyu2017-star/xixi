# -*- coding: utf-8 -*-
"""逐一核对论文正文中出现的每一个数字是否与估计结果文件一致。

做法：把 results/*.json 中的所有数值（及若干由其直接派生的量，如百分比、
比值、总效应）展开为一个允许集合，再从论文 Markdown 中抽取全部数字逐一比对，
输出无法在允许集合中找到对应值的"孤儿数字"，供人工复核。
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def walk(obj, out):
    if isinstance(obj, dict):
        for v in obj.values():
            walk(v, out)
    elif isinstance(obj, list):
        for v in obj:
            walk(v, out)
    elif isinstance(obj, (int, float)) and not isinstance(obj, bool):
        out.append(float(obj))


def fmts(x):
    """一个数值在正文中可能出现的书写形式。"""
    s = set()
    ax = abs(x)
    for nd in range(0, 5):
        s.add(f"{ax:.{nd}f}")
    s.add(f"{ax:g}")
    return {t.rstrip(".") for t in s}


def allowed_set(paths, extra):
    vals = []
    for p in paths:
        walk(json.load(open(p, encoding="utf-8")), vals)
    derived = list(vals)
    for v in vals:                       # 百分比形式
        derived.append(v * 100)
    derived.extend(extra)
    out = set()
    for v in derived:
        out |= fmts(v)
    return out


# 与统计结果无关的数字：年份、编号、样本结构、政策背景等
GENERIC = {
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13",
    "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25",
    "30", "40", "50", "100", "200", "283", "390", "400", "500", "800", "2000",
    "1982", "1984", "2010", "2011", "2012", "2013", "2014", "2015", "2016",
    "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025",
    "1.96", "0.05", "0.06", "0.01", "0.10", "0.25", "15.4", "5.5", "1002",
    "6487", "062.9", "224", "924.24", "224.0", "7.35", "0.5", "95", "99", "90",
}

NUM = re.compile(r"−?\d+(?:\.\d+)?")

CASES = [
    ("paper3", ["p3_results.json"],
     [0.0318 / 1.0482 * 100, (0.0322 - 0.0318) / 0.0318 * 100,
      0.0440 / 1.0638 * 100, 0.0479 / 1.0638 * 100]),
    ("paper4", ["p4_results.json"],
     [0.0266 / 0.0153, 0.0109 / 0.0265 * 100,
      (-0.0156 - 0.0187) / (1 - 0.2274), (-0.0173 - 0.0191) / (1 - 0.3238),
      (-0.0118 - 0.0122) / (1 - 0.2968), 23.59, 61.28, 15.13]),
]

bad_total = 0
for name, jsons, extra in CASES:
    allow = allowed_set([os.path.join(ROOT, "results", j) for j in jsons], extra)
    allow |= GENERIC
    text = open(os.path.join(HERE, f"{name}.md"), encoding="utf-8").read()
    # 剔除公式、图表编号与引文键，避免误报
    text = re.sub(r"\$\$.*?\$\$", " ", text, flags=re.S)
    text = re.sub(r"\$[^$]*\$", " ", text)
    text = re.sub(r"\[@[^\]]+\]", " ", text)
    text = re.sub(r"表\d+|图\d+|式（\d+）|假设\d+|第（\d+）列|（\d+）", " ", text)
    text = re.sub(r"p\d_fig\d\.png", " ", text)
    text = re.sub(r"^#+ [\d.]+", " ", text, flags=re.M)
    nums = NUM.findall(text)
    orphans = []
    for tok in nums:
        t = tok.lstrip("−")
        if t in allow or t.rstrip("0").rstrip(".") in allow:
            continue
        orphans.append(tok)
    print(f"=== {name}：共 {len(nums)} 个数字，未匹配 {len(orphans)} 个")
    for o in sorted(set(orphans)):
        print("   ", o, "×", orphans.count(o))
    bad_total += len(orphans)

sys.exit(1 if bad_total else 0)
