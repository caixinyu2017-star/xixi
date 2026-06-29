#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sample_size_check.py — "数据规模是否足够"的可操作经验预警（data-engineering 四问之一）。

data-engineering 的"数据先行四问"里"规模是否足够"最量化、却原本最空泛（无任何阈值/判据）。
本脚本据**公开经验法则**给出规模预警，把这一问从口头变可计算。纯标准库零依赖。

⚠ 诚实声明：这些是**经验阈值（rules of thumb），不是统计功效分析（power analysis）**。
真正的样本量该由效应量 + 显著性 + 功效定（用 statsmodels/G*Power 等做 power analysis，
本仓 code_assets/stats_tests.py 若含 power 函数应优先用）。本脚本只做"低于经验下限就预警"的
粗筛，绝不替代正式样本量论证；阈值依据逐条标注，可调。

经验阈值依据（均为领域常见 rule of thumb，非定论）：
- 分类每类最小样本：≥ 50/类 偏紧、≥ 100/类 较稳（小样本类别学不动、CV 不稳）
- 回归样本/特征比（EPV 思想）：每个特征 ≥ 10~20 样本，低于 10 易过拟合
- 检测/分割每类实例数：每类 ≥ 数百实例起步（COCO 量级远高），≥ 50 仅够 demo
- 二分类正例数（EPV，Peduzzi 1996 经典）：逻辑回归每自变量 ≥ 10 个正例

用法：
  python sample_size_check.py --task clf --n 1200 --classes 3 --features 20
  python sample_size_check.py --task reg --n 200 --features 30
  python sample_size_check.py --task detection --n 5000 --classes 4
  python sample_size_check.py --selftest
"""
from __future__ import annotations
import argparse
import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# 经验阈值（可调；依据见 docstring）
CLF_PER_CLASS_TIGHT = 50      # 分类每类最小（偏紧下限）
CLF_PER_CLASS_OK = 100        # 分类每类较稳
REG_EPV_MIN = 10              # 回归/逻辑回归每特征(或每正例)最小样本
REG_EPV_OK = 20               # 较稳
DET_PER_CLASS_MIN = 50        # 检测每类实例 demo 下限
DET_PER_CLASS_OK = 300        # 检测每类较像样起步


def check(task: str, n: int, classes: int = 0, features: int = 0,
          positives: int = 0, per_class_counts: list | None = None) -> dict:
    """据经验阈值给规模预警。返回 {level, findings, advice}。level: ok/warn/insufficient。"""
    findings = []
    level = "ok"

    def bump(new):
        nonlocal level
        order = {"ok": 0, "warn": 1, "insufficient": 2}
        if order[new] > order[level]:
            level = new

    if task == "clf":
        k = max(1, classes)
        avg_per_class = n / k
        # 若给了各类真实计数，按最小类判（更严谨）
        min_class = min(per_class_counts) if per_class_counts else avg_per_class
        basis = "最小类实际样本" if per_class_counts else "样本/类数均摊"
        if min_class < CLF_PER_CLASS_TIGHT:
            bump("insufficient")
            findings.append(f"[insufficient] {basis}={min_class:.0f} < {CLF_PER_CLASS_TIGHT}/类经验下限"
                            f"——小类学不动、CV 不稳，考虑合并类/补采/重采样")
        elif min_class < CLF_PER_CLASS_OK:
            bump("warn")
            findings.append(f"[warn] {basis}={min_class:.0f}，介于 {CLF_PER_CLASS_TIGHT}~{CLF_PER_CLASS_OK}/类，"
                            f"偏紧——交叉验证方差会大，慎报单点指标")
        if features and n / max(1, features) < REG_EPV_MIN:
            bump("warn")
            findings.append(f"[warn] 样本/特征比={n/features:.1f} < {REG_EPV_MIN}，高维易过拟合，考虑降维/正则")

    elif task == "reg":
        if features:
            epv = n / max(1, features)
            if epv < REG_EPV_MIN:
                bump("insufficient")
                findings.append(f"[insufficient] 样本/特征比={epv:.1f} < {REG_EPV_MIN}（EPV 经验下限）"
                                f"——严重过拟合风险，须降特征或大幅补样本")
            elif epv < REG_EPV_OK:
                bump("warn")
                findings.append(f"[warn] 样本/特征比={epv:.1f}，介于 {REG_EPV_MIN}~{REG_EPV_OK}，偏紧——优先正则/特征筛选")
        else:
            findings.append("[info] 未给 --features，无法算样本/特征比；回归规模主要看 EPV")

    elif task == "detection":
        k = max(1, classes)
        per = (min(per_class_counts) if per_class_counts else n / k)
        basis = "最小类实例数" if per_class_counts else "实例/类数均摊"
        if per < DET_PER_CLASS_MIN:
            bump("insufficient")
            findings.append(f"[insufficient] {basis}={per:.0f} < {DET_PER_CLASS_MIN}/类"
                            f"——仅够 demo，远不足训练稳健检测器（COCO 量级每类数千+）")
        elif per < DET_PER_CLASS_OK:
            bump("warn")
            findings.append(f"[warn] {basis}={per:.0f}，介于 {DET_PER_CLASS_MIN}~{DET_PER_CLASS_OK}/类，"
                            f"偏少——稀有类召回会差，考虑针对性补采/增强(只增训练折)")

    else:
        raise ValueError(f"task 须是 clf/reg/detection 之一：{task!r}")

    # 二分类 EPV（若给了正例数）
    if positives and features:
        epv_pos = positives / max(1, features)
        if epv_pos < REG_EPV_MIN:
            bump("warn" if level != "insufficient" else "insufficient")
            findings.append(f"[warn] 正例 EPV={epv_pos:.1f}（正例数/特征数）< {REG_EPV_MIN}"
                            f"（Peduzzi 1996 逻辑回归经验）——系数不稳，减特征或补正例")

    if not findings:
        findings.append("[ok] 各项规模在经验阈值之上（仍建议正式 power analysis 论证主结论）")
    advice = ("这是经验粗筛非 power analysis。主结论的样本量须用效应量+显著性+功效正式论证"
              "（statsmodels/G*Power 或 code_assets/stats_tests.py 的 power 函数）。阈值可调，见脚本顶部。")
    return {"task": task, "n": n, "classes": classes, "features": features,
            "level": level, "findings": findings, "advice": advice}


def render(rep: dict) -> str:
    icon = {"ok": "✅", "warn": "⚠️", "insufficient": "🛑"}[rep["level"]]
    lines = [f"# 数据规模充足性预警 {icon} {rep['level'].upper()}",
             f"- task={rep['task']} n={rep['n']} classes={rep['classes']} features={rep['features']}", ""]
    lines += [f"- {x}" for x in rep["findings"]]
    lines += ["", f"> {rep['advice']}"]
    return "\n".join(lines)


def _selftest() -> int:
    print("### sample_size_check 离线自测", file=sys.stderr)
    # 分类：每类够 → ok
    assert check("clf", n=600, classes=3, features=10)["level"] == "ok"
    # 分类：每类 30 < 50 → insufficient
    assert check("clf", n=90, classes=3)["level"] == "insufficient"
    # 分类：给各类真实计数，最小类 20 → insufficient（按最小类不按均摊）
    r = check("clf", n=1000, classes=3, per_class_counts=[960, 20, 20])
    assert r["level"] == "insufficient" and "最小类" in r["findings"][0], r
    # 回归：样本/特征比 5 < 10 → insufficient
    assert check("reg", n=150, features=30)["level"] == "insufficient"
    # 回归：比 15 → warn
    assert check("reg", n=300, features=20)["level"] == "warn"
    # 检测：每类 30 < 50 → insufficient
    assert check("detection", n=120, classes=4)["level"] == "insufficient"
    # 检测：每类 200 → warn
    assert check("detection", n=800, classes=4)["level"] == "warn"
    # 正例 EPV
    r2 = check("clf", n=2000, classes=2, features=50, positives=200)
    assert any("正例 EPV" in f for f in r2["findings"]), r2
    # 非法 task
    try:
        check("bad", n=10)
        raise AssertionError("应报错")
    except ValueError:
        pass
    # 渲染含诚实声明
    md = render(check("reg", n=150, features=30))
    assert "power analysis" in md and "经验" in md, md
    print("[selftest] PASS sample_size_check offline")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="数据规模充足性经验预警（四问之规模）")
    ap.add_argument("--task", choices=["clf", "reg", "detection"])
    ap.add_argument("--n", type=int, help="总样本数")
    ap.add_argument("--classes", type=int, default=0, help="类别数（clf/detection）")
    ap.add_argument("--features", type=int, default=0, help="特征数")
    ap.add_argument("--positives", type=int, default=0, help="二分类正例数（算 EPV）")
    ap.add_argument("--per-class", default="", help="各类实际计数，逗号分隔（按最小类判，更严谨）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest or not (args.task and args.n):
        return _selftest()

    pcc = [int(x) for x in args.per_class.split(",") if x.strip()] if args.per_class else None
    rep = check(args.task, args.n, args.classes, args.features, args.positives, pcc)
    print(json.dumps(rep, ensure_ascii=False, indent=2) if args.json else render(rep))
    return 0


if __name__ == "__main__":
    sys.exit(main())
