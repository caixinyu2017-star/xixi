#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""calibration.py — 可选 calibration mode（三分类，反映真实回 m03 循环）。

喂入一批"已知结局"的 idea，用本技能判决与真实结局做对照，校准严格度。

⚠ 旧版二分类把"有条件通过"当"不通过"计为负例——但真实闭环里有条件通过是**回 m03 迭代**
（最终常被接收），不是拒稿。把"需修订"与"被拒"混为一谈会**高估 FNR**、误导调参。
本版改三分类：

  结局/判决三类：
    accept   ← 真实"直接接收" / 判决"通过"
    revise   ← 真实"修订后接收(major/minor revision then accept)" / 判决"有条件通过(含重大)"
    reject   ← 真实"被拒/撤回" / 判决"不通过"

  关键校准指标（在"是否最终会进入发表轨道"的意义下）：
    - strict_FNR：真实最终被接收(accept+revise)却judged 为 reject 的比例 → 评审过严，误杀
    - FPR       ：真实被拒(reject)却 judged 为 accept 的比例 → 评审过松/谄媚，放行坏 idea
    - revise_match：真实 revise 且 judged revise 的占比 → "需修订"识别准确度（旧版完全测不到）
  另给三分类混淆矩阵与逐类 precision/recall。

借 academic-paper-reviewer 的 calibration 模式。无外部依赖，自带合成数据自测。
"""
from __future__ import annotations
from dataclasses import dataclass

# 判决文本 → 三类
_VERDICT_TO_CLASS = {
    "通过": "accept",
    "有条件通过": "revise",
    "有条件通过（重大）": "revise",
    "不通过": "reject",
}
CLASSES = ("accept", "revise", "reject")


def verdict_class(decision: str) -> str:
    """把判决文本归一到三类；未知文本保守归 reject。"""
    return _VERDICT_TO_CLASS.get((decision or "").strip(), "reject")


@dataclass
class CalibItem:
    idea_id: str
    actual_outcome: str      # 已知结局三类之一: accept / revise / reject
    decision: str            # 本技能判决文本


def _on_track(cls: str) -> bool:
    """是否在'最终会进入发表轨道'(accept 或 revise-then-accept)。reject 不在。"""
    return cls in ("accept", "revise")


def confusion3(items: list) -> dict:
    """3x3 混淆矩阵：mat[actual][pred] = 计数。"""
    mat = {a: {p: 0 for p in CLASSES} for a in CLASSES}
    for it in items:
        actual = it.actual_outcome.strip()
        if actual not in CLASSES:
            raise ValueError(f"actual_outcome 必须是 {CLASSES} 之一: {actual!r}")
        pred = verdict_class(it.decision)
        mat[actual][pred] += 1
    return mat


def metrics(items: list) -> dict:
    mat = confusion3(items)
    n = len(items)

    def safe(a, b):
        return round(a / b, 3) if b else None

    # strict_FNR：真实 on-track(accept+revise) 却被 judged reject
    ontrack_total = sum(mat[a][p] for a in ("accept", "revise") for p in CLASSES)
    ontrack_killed = sum(mat[a]["reject"] for a in ("accept", "revise"))
    # FPR：真实 reject 却被 judged accept（放行坏 idea，最严重）
    reject_total = sum(mat["reject"][p] for p in CLASSES)
    reject_passed = mat["reject"]["accept"]
    # revise 识别
    revise_total = sum(mat["revise"][p] for p in CLASSES)
    revise_hit = mat["revise"]["revise"]
    # 逐类 precision/recall
    per_class = {}
    for c in CLASSES:
        tp = mat[c][c]
        col = sum(mat[a][c] for a in CLASSES)   # 所有被 judged 为 c 的
        row = sum(mat[c][p] for p in CLASSES)   # 所有真实为 c 的
        per_class[c] = {"precision": safe(tp, col), "recall": safe(tp, row)}
    diag = sum(mat[c][c] for c in CLASSES)
    return {
        "confusion3": mat,
        "n": n,
        "strict_FNR": safe(ontrack_killed, ontrack_total),  # 误杀最终会发表的
        "FPR": safe(reject_passed, reject_total),           # 放行真被拒的
        "revise_match": safe(revise_hit, revise_total),     # 需修订识别准确度
        "accuracy3": safe(diag, n),                         # 三类全对角占比
        "per_class": per_class,
    }


def interpret(m: dict) -> str:
    msgs = []
    if m["strict_FNR"] is not None and m["strict_FNR"] > 0.4:
        msgs.append(f"strict_FNR={m['strict_FNR']} 偏高: 评审过严, 把最终会被接收的 idea 误判为不通过, "
                    f"检查否决项是否过激、通过线(pass_line)是否过高")
    if m["FPR"] is not None and m["FPR"] > 0.3:
        msgs.append(f"FPR={m['FPR']} 偏高: 评审过松/谄媚, 把真被拒 idea 放行为通过, "
                    f"收紧 pass_line 与反谄媚 concession 配额")
    if m["revise_match"] is not None and m["revise_match"] < 0.5:
        msgs.append(f"revise_match={m['revise_match']} 偏低: '需修订'识别不准, "
                    f"检查 cond_line/cond_major_line 区间是否需调整")
    if not msgs:
        msgs.append("strict_FNR/FPR/revise_match 均在可接受范围, 严格度大致校准")
    return " | ".join(msgs)


def _selftest():
    # 合成 9 个已知结局 idea（三类各覆盖）
    items = [
        CalibItem("a1", "accept", "通过"),               # accept→accept 对
        CalibItem("a2", "accept", "通过"),               # 对
        CalibItem("a3", "accept", "不通过"),              # 误杀(strict_FNR)
        CalibItem("r1", "revise", "有条件通过"),          # revise 命中
        CalibItem("r2", "revise", "有条件通过（重大）"),   # revise 命中
        CalibItem("r3", "revise", "不通过"),              # 误杀(strict_FNR：revise 也是 on-track)
        CalibItem("x1", "reject", "不通过"),              # reject 对
        CalibItem("x2", "reject", "不通过"),              # 对
        CalibItem("x3", "reject", "通过"),                # 放行坏idea(FPR)
    ]
    m = metrics(items)
    print("confusion3:")
    for a in CLASSES:
        print(f"  actual={a}: {m['confusion3'][a]}")
    print("strict_FNR:", m["strict_FNR"], "FPR:", m["FPR"],
          "revise_match:", m["revise_match"], "accuracy3:", m["accuracy3"])
    print("interpret:", interpret(m))

    # on-track 总数 = accept(3)+revise(3)=6；被误杀(judged reject)=a3,r3=2 → strict_FNR=2/6
    assert m["strict_FNR"] == round(2 / 6, 3), m["strict_FNR"]
    # reject 总数=3；被放行(judged accept)=x3=1 → FPR=1/3
    assert m["FPR"] == round(1 / 3, 3), m["FPR"]
    # revise 总数=3；命中(judged revise)=r1,r2=2 → 2/3
    assert m["revise_match"] == round(2 / 3, 3), m["revise_match"]
    # 对角=a1,a2,r1,r2,x1,x2=6 → accuracy3=6/9
    assert m["accuracy3"] == round(6 / 9, 3), m["accuracy3"]

    # 关键回归断言：旧二分类会把 r1/r2(有条件通过) 误计为"漏放"，三分类不应如此
    # r1/r2 是 revise→revise 正确命中，不进 strict_FNR 分子
    assert m["confusion3"]["revise"]["revise"] == 2

    # 未知判决文本保守归 reject
    assert verdict_class("莫名其妙") == "reject"
    # 非法 actual_outcome 报错
    try:
        metrics([CalibItem("bad", "maybe", "通过")])
        raise AssertionError("should raise on bad actual_outcome")
    except ValueError:
        print("[guard] illegal actual_outcome ... OK")

    # 空输入不崩
    m0 = metrics([])
    assert m0["strict_FNR"] is None and m0["n"] == 0
    print("\nALL SELFTESTS PASSED")


if __name__ == "__main__":
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if len(sys.argv) > 2 or (len(sys.argv) == 2 and sys.argv[1] != "--selftest"):
        raise SystemExit(f"usage: python {sys.argv[0]} [--selftest]")
    _selftest()
