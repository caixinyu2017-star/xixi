# -*- coding: utf-8 -*-
"""逐一核对论文正文中出现的每一个数字是否与估计结果文件一致。

把 results/*.json 中的全部数值（含以字符串形式存放的系数与 t 值）及若干直接
派生量展开为允许集合，再从论文 Markdown 中抽取全部数字逐一比对，输出无法在
允许集合中找到对应值的"孤儿数字"，供人工复核。
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NUMTOK = re.compile(r"-?\d+(?:\.\d+)?")


def walk(obj, out):
    if isinstance(obj, dict):
        for v in obj.values():
            walk(v, out)
    elif isinstance(obj, list):
        for v in obj:
            walk(v, out)
    elif isinstance(obj, bool):
        pass
    elif isinstance(obj, (int, float)):
        out.append(float(obj))
    elif isinstance(obj, str):
        for t in NUMTOK.findall(obj):
            try:
                out.append(float(t))
            except ValueError:
                pass


def fmts(x):
    s, ax = set(), abs(x)
    for nd in range(0, 5):
        s.add(f"{ax:.{nd}f}")
    s.add(f"{ax:g}")
    return {t.rstrip(".") for t in s}


def allowed_set(paths, extra):
    vals = []
    for p in paths:
        walk(json.load(open(p, encoding="utf-8")), vals)
    derived = list(vals) + [v * 100 for v in vals] + list(extra)
    out = set()
    for v in derived:
        out |= fmts(v)
    return out


GENERIC = {
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13",
    "14", "15", "16", "17", "18", "19", "20", "25", "30", "34", "40", "50",
    "75", "90", "95", "99", "100", "200", "278", "300", "360", "500", "1000",
    "2006", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017",
    "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025",
    "1.96", "0.01", "0.05", "0.10", "1002", "6487", "249.2", "49", "224",
    "314001", "1179", "1984",
    # Hansen(1999) 门槛值置信区间的 LR 临界值 c(α)=−2ln(1−√(1−α))，α=0.05 时为 7.35
    "7.35",
}


def csv_values(paths):
    """把作图用 CSV 中的全部数值一并纳入允许集合。"""
    out = []
    for p in paths:
        f = os.path.join(ROOT, "results", p)
        if not os.path.exists(f):
            continue
        for line in open(f, encoding="utf-8").read().split("\n")[1:]:
            for t in NUMTOK.findall(line):
                try:
                    out.append(float(t))
                except ValueError:
                    pass
    return out


def turning_points(obj, out):
    """凡同一层级同时给出一次项与二次项系数处，补入其隐含的拐点 −b1/(2b2)。"""
    if isinstance(obj, dict):
        pair = None
        for k1, k2 in (("x", "x2"), ("ai_std", "ai_sq")):
            if isinstance(obj.get(k1), dict) and isinstance(obj.get(k2), dict):
                pair = (obj[k1], obj[k2])
        if pair:
            def _val(dd):
                if isinstance(dd.get("b"), (int, float)):
                    return float(dd["b"])          # 未取整的原始系数
                return float(NUMTOK.findall(str(dd.get("coef")))[0])

            try:
                b1, b2 = _val(pair[0]), _val(pair[1])
                if b2 != 0:
                    out.append(-b1 / (2 * b2))
            except (IndexError, ValueError, TypeError):
                pass
        for v in obj.values():
            turning_points(v, out)
    elif isinstance(obj, list):
        for v in obj:
            turning_points(v, out)


def region_gaps():
    """论文1 正文引用的东中西部差距为分区域趋势值之差，此处逐年补入。"""
    f = os.path.join(ROOT, "results", "p1_trend_region.csv")
    if not os.path.exists(f):
        return []
    rows = [ln.split(",") for ln in
            open(f, encoding="utf-8").read().strip().split("\n")]
    head, body = rows[0], rows[1:]
    iy, ir, iv = head.index("year"), head.index("region"), head.index("yqe")
    by = {}
    for r in body:
        by.setdefault(r[iy], {})[r[ir]] = float(r[iv])
    out = []
    for yr, d in by.items():
        ks = sorted(d)
        for i in range(len(ks)):
            for j in range(len(ks)):
                if i != j:
                    out.append(d[ks[i]] - d[ks[j]])
    return out


def check(name, jsons, extra, csvs=()):
    derived = list(extra) + csv_values(csvs)
    for j in jsons:
        tp = []
        turning_points(json.load(open(os.path.join(ROOT, "results", j),
                                      encoding="utf-8")), tp)
        derived += tp
    allow = allowed_set([os.path.join(ROOT, "results", j) for j in jsons],
                        derived)
    allow |= GENERIC
    text = open(os.path.join(HERE, f"{name}.md"), encoding="utf-8").read()
    text = re.sub(r"\$\$.*?\$\$", " ", text, flags=re.S)
    text = re.sub(r"\$[^$]*\$", " ", text)
    text = re.sub(r"\[@[^\]]+\]", " ", text)
    text = re.sub(r"表\d+|图\d+|式\(\d+-\d+\)|假设\d+|第（\d+）列|（\d+）", " ", text)
    text = re.sub(r"\(\d+-\d+\)", " ", text)
    text = re.sub(r"p\d_fig\d\.png", " ", text)
    text = re.sub(r"^#+ [\d.]+", " ", text, flags=re.M)
    nums = NUMTOK.findall(text)
    orphans = [t for t in nums
               if t.lstrip("-") not in allow
               and t.lstrip("-").rstrip("0").rstrip(".") not in allow]
    print(f"=== {name}：共 {len(nums)} 个数字，未匹配 {len(orphans)} 个")
    for o in sorted(set(orphans)):
        print("   ", o, "×", orphans.count(o))
    return len(orphans)


CASES = [
    ("paper1", ["p1_results.json"],
     [0.2631 * 0.1149, 0.2631 * 0.1149 / 0.4812 * 100] + region_gaps(),
     ["p1_trend.csv", "p1_trend_region.csv", "p1_threshold_ssr.csv"]),
    ("paper2", ["p2_results.json"],
     [33.4179 / 2],
     ["p2_trend.csv"]),
]

bad = sum(check(*c) for c in CASES)
sys.exit(1 if bad else 0)
