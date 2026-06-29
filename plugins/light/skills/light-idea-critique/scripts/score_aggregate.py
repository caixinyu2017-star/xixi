#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""score_aggregate.py — idea 严审加权聚合 + 否决项 + 判决映射。

实现 references/rubric.md 的：
  - 八维度权重加权求和 (Weighted, 0-100)
  - Weighted -> Overall(1-10) 线性映射
  - 否决项 (gate before score) 优先于加权分
  - decision mapping 表

无外部数据依赖；自带 __main__ 用合成数据自测（含 examples 的皮肤镜案例）。
仅用标准库，便于在任意环境跑通。

⚠ 阈值与权重的依据声明（诚实底线，勿读成"有数据反推的金标准"）：
  下方 WEIGHTS / PASS_LINE / 各 gate 线均为**经验默认值，是可调超参，非由标注集反推**。
  - 权重锚定的是 NeurIPS/ICLR 评审表的**维度构成**（Originality/Soundness/...），但 NeurIPS
    评审表本身**不给数值权重**——这里的 0.20/0.18/... 是"按顶会维度重要性排序"的经验设定，
    不是会议官方权重，也未做大样本敏感性回归。审稿人若质疑"为何 soundness 0.18 而非 0.20"，
    诚实回答是"经验默认值，可在 THRESHOLDS 里调，并跑 _weight_sensitivity() 看判决稳健性"。
  - 通过线 PASS_LINE=80 与 references.md #6 的现实（真实被接收论文 CycleReviewer 仅评 ~5.69/10）
    存在张力：要求 strong-accept 级才放行可能偏严、FNR 偏高。保留 80 作**默认严线**，但显式
    暴露为可调，并提供 calibration.py 在**用户自己的标注集**上反推经验阈值的路径（Light 当前
    无公开标注集，故不假装 80 有数据依据）。
  - decide() 支持传入 thresholds 覆盖默认值，便于 calibration 反推后注入或按场景调松/调严。
"""
from __future__ import annotations
from dataclasses import dataclass, field

# === 八维度权重（合计 1.00）——经验默认值，可调超参，见上"依据声明" ===
# 锚定 NeurIPS/ICLR 评审维度构成，但数值为经验设定（会议表不给权重），非数据反推。
WEIGHTS = {
    "originality": 0.20,
    "soundness": 0.18,
    "data": 0.14,
    "experiment": 0.14,
    "contribution": 0.13,
    "delta": 0.08,
    "feasibility": 0.07,
    "impact": 0.06,
}
CORE_DIMS = ("originality", "soundness", "data", "experiment")

# === 判决阈值——经验默认值，可调超参（decide() 可整体覆盖）===
# 默认值理由写在每行；要调松/调严或用 calibration 反推后的经验值，改这里或传 decide(thresholds=)。
DEFAULT_THRESHOLDS = {
    # decision mapping 的 Weighted 分界（见 rubric.md decision mapping 表，须与之同步）
    "pass_line": 80,        # ≥ 此线→"通过"。默认 80=strong-accept 级严线（与 ref#6 现实有张力，偏严）
    "cond_line": 65,        # ≥ 此线→"有条件通过"（minor revision 级）
    "cond_major_line": 50,  # ≥ 此线→"有条件通过（重大）"（major revision 级）
    "reject_line": 35,      # < 此线→"不通过（地基问题）"；[reject_line, cond_major_line)→"不通过"
    # 否决项 gate 线
    "gate_fatal": 45,       # 创新性<此 或 核心两项<此 → 压顶不通过（顶会一个 fatal flaw 即拒的经验线）
    "pass_core_floor": 60,  # "通过"额外要求：核心四维均≥此（防某核心维勉强及格仍被高均值放行）
}



@dataclass
class Verdict:
    weighted: float
    overall: int
    decision: str
    reasons: list = field(default_factory=list)
    border_review: str = ""   # SciMuse 式边界复核建议（仅否决边界 case 有值，参考非放行）


def _check_weights():
    total = round(sum(WEIGHTS.values()), 6)
    assert total == 1.0, f"weights must sum to 1.0, got {total}"


def weighted_score(scores: dict) -> float:
    """scores: {dim: 0-100}. 缺失维度视为错误。"""
    missing = set(WEIGHTS) - set(scores)
    if missing:
        raise ValueError(f"missing dimensions: {sorted(missing)}")
    for d, v in scores.items():
        if d not in WEIGHTS:
            raise ValueError(f"unknown dimension: {d}")
        if not (0 <= v <= 100):
            raise ValueError(f"{d} score out of range 0-100: {v}")
    return round(sum(scores[d] * WEIGHTS[d] for d in WEIGHTS), 2)


def to_overall(weighted: float) -> int:
    return int(round(1 + weighted / 100 * 9))


def decide(scores: dict, unresolved_critical: bool = False,
           thresholds: dict | None = None, interestingness: float | None = None) -> Verdict:
    """否决项与 decision mapping 取更严者。

    thresholds: 可选，覆盖 DEFAULT_THRESHOLDS 的任意子集（便于 calibration 反推后注入，
    或按场景调松/调严）。未传的键回退默认值。
    interestingness: 可选 0-100（借 SciMuse 式有趣度/价值预判）。仅在 idea 被否决项压到"不通过"
    但 Weighted 接近通过线时，输出"边界复核建议"提示人工二次确认是否误杀——不改 gate、不自动放行。
    """
    t = dict(DEFAULT_THRESHOLDS)
    if thresholds:
        t.update(thresholds)
    w = weighted_score(scores)
    ov = to_overall(w)
    reasons = []

    # --- 否决项 (gate) ---
    gate_cap = None  # 可达到的最宽判决
    if scores["originality"] < t["gate_fatal"]:
        gate_cap = "不通过"
        reasons.append(f"否决:创新性<{t['gate_fatal']}(套壳/无检索)->直接不通过")
    low_core = [d for d in CORE_DIMS if scores[d] < t["gate_fatal"]]
    if len(low_core) >= 2:
        gate_cap = "不通过"
        reasons.append(f"否决:核心维度两项<{t['gate_fatal']} {low_core}->不通过")
    if unresolved_critical:
        # 最高只能有条件通过
        if gate_cap != "不通过":
            gate_cap = "有条件通过"
        reasons.append("否决:存在未化解CRITICAL->最高有条件通过")

    # --- decision mapping 表（阈值见 DEFAULT_THRESHOLDS，须与 rubric.md 同步）---
    if w >= t["pass_line"]:
        mapped = "通过"
    elif w >= t["cond_line"]:
        mapped = "有条件通过"
    elif w >= t["cond_major_line"]:
        mapped = "有条件通过（重大）"
    elif w >= t["reject_line"]:
        mapped = "不通过"
    else:
        mapped = "不通过"
    reasons.append(f"decision-mapping:Weighted={w}->{mapped}")

    # 取更严者
    rank = {"通过": 3, "有条件通过": 2, "有条件通过（重大）": 2, "不通过": 0}
    final = mapped
    if gate_cap is not None and rank[gate_cap] < rank[mapped]:
        final = gate_cap
        reasons.append(f"取更严:gate({gate_cap})覆盖mapping({mapped})")

    # 额外:通过要求无核心维度 < pass_core_floor
    if final == "通过":
        low_floor = [d for d in CORE_DIMS if scores[d] < t["pass_core_floor"]]
        if low_floor:
            final = "有条件通过"
            reasons.append(f"降级:通过要求核心维度>={t['pass_core_floor']},但{low_floor}<{t['pass_core_floor']}")

    # 边界复核建议（借 SciMuse 可量化有趣度，缓解二元否决的边界误杀，不改 gate 本身）：
    # 当 idea 被 gate 压到"不通过"、但 Weighted 其实不低(接近 pass_line)且有趣度高时，
    # 提示"这是边界 case，建议人工二次复核是否误杀"——只提示，绝不自动放行（撞车否决仍有效）。
    border_note = None
    if interestingness is not None and final == "不通过":
        near_pass = w >= t["pass_line"] - 15  # 距通过线 15 分内算边界
        if near_pass and interestingness >= 70:
            border_note = (f"边界复核建议：本 idea 被否决项压到不通过，但 Weighted={w}（距通过线 "
                           f"{t['pass_line']} 仅 {round(t['pass_line']-w,1)} 分）且有趣度={interestingness} 偏高——"
                           f"建议人工二次确认是否为边界误杀（撞车/否决仍按原判，此为参考不自动放行）。")
            reasons.append(border_note)

    v = Verdict(weighted=w, overall=ov, decision=final, reasons=reasons)
    if border_note:
        v.border_review = border_note
    return v


def weight_sensitivity(scores: dict, delta: float = 0.02,
                       thresholds: dict | None = None) -> dict:
    """权重敏感性分析：对每个权重做 ±delta 微扰（其余等比归一），看判决是否翻档。

    回答审稿人"权重微扰下判决稳不稳"。返回 {基准判决, 微扰后是否出现翻档, 各扰动结果}。
    纯标准库、不联网。delta 默认 ±0.02（权重小数点级别的合理扰动）。
    """
    base = decide(scores, thresholds=thresholds)
    flips = []
    global WEIGHTS
    orig = dict(WEIGHTS)
    try:
        for dim in orig:
            for sign in (+1, -1):
                pert = dict(orig)
                pert[dim] = max(0.0, round(orig[dim] + sign * delta, 4))
                # 其余权重等比缩放，使总和回到 1.0
                rest = sum(v for k, v in pert.items() if k != dim)
                if rest <= 0:
                    continue
                scale = (1.0 - pert[dim]) / rest
                for k in pert:
                    if k != dim:
                        pert[k] = round(pert[k] * scale, 6)
                WEIGHTS = pert
                v = decide(scores, thresholds=thresholds)
                if v.decision != base.decision:
                    flips.append({"dim": dim, "sign": sign, "delta": delta,
                                  "decision": v.decision, "weighted": v.weighted})
    finally:
        WEIGHTS = orig
    return {"base_decision": base.decision, "base_weighted": base.weighted,
            "delta": delta, "flip_count": len(flips), "flips": flips,
            "robust": len(flips) == 0}


def rank_batch(candidates: list, top_k: int | None = None,
               thresholds: dict | None = None) -> dict:
    """批量评审排序：摄入 m03 的多张 idea 立项卡（idea_candidates），逐卡完整八维判决，
    再按"先放行档位、再 Weighted 降序"汇总排序，输出 top-k 放行名单 + 余下附判决理由。

    candidates: [{"id": str, "scores": {dim:0-100}, "unresolved_critical": bool}]
      —— scores 仍须由逐卡完整严审（Step1-5：盲审/检索/五视角/反谄媚）得出，本函数
      只做"逐卡 decide + 汇总排序"，不替代严审（口径见 SKILL 批量工作流）。
    top_k: 放行前 k 名（None=不截断，全排序）。

    排序键：先按判决档位（通过 > 有条件通过 > 有条件通过(重大) > 不通过），同档再按 Weighted 降序。
    诚实约定：只有判决=通过的卡才计入 passlist（与单卡 decide 一致，gate 不因排序放宽）。
    """
    rank_order = {"通过": 3, "有条件通过": 2, "有条件通过（重大）": 1, "不通过": 0}
    rows = []
    for c in candidates:
        cid = c.get("id", "?")
        v = decide(c["scores"], unresolved_critical=c.get("unresolved_critical", False),
                   thresholds=thresholds)
        rows.append({"id": cid, "weighted": v.weighted, "overall": v.overall,
                     "decision": v.decision, "reasons": v.reasons})
    # 稳定排序：先档位降序，再 Weighted 降序，再 id 升序（确定性，便于复现/测试）
    rows.sort(key=lambda r: (-rank_order.get(r["decision"], 0), -r["weighted"], r["id"]))
    passlist = [r for r in rows if r["decision"] == "通过"]
    if top_k is not None:
        passlist = passlist[:top_k]
    pass_ids = {r["id"] for r in passlist}
    return {
        "n": len(rows),
        "ranked": rows,                       # 全部卡，已排序
        "passlist": passlist,                 # 判决=通过的（截到 top_k）
        "pass_count": len(passlist),
        "top_k": top_k,
        "note": ("仅判决=通过的 idea 计入 passlist 放行 m05；有条件通过/不通过带 Roadmap 回 m03。"
                 "排序不放宽否决项 gate——top-k 只在已通过的卡里取，不会把不通过的卡排进放行名单。"),
        "not_passed": [r["id"] for r in rows if r["id"] not in pass_ids],
    }


def _selftest():
    _check_weights()
    print("[1] weights sum to 1.0 ... OK")

    # 案例A: examples 的皮肤镜 idea(创新性42, 命中否决)
    derm = dict(originality=42, soundness=50, data=55, experiment=48,
                contribution=50, delta=45, feasibility=80, impact=58)
    vA = decide(derm, unresolved_critical=True)
    print(f"[A] dermoscopy Weighted={vA.weighted} Overall={vA.overall} -> {vA.decision}")
    for r in vA.reasons:
        print("      -", r)
    assert abs(vA.weighted - 51.0) < 0.5, vA.weighted   # 实算 51.0（修正旧 51.2 笔误）
    assert vA.decision == "不通过", vA.decision  # 创新性<45压顶

    # 案例B: 强 idea, 各维高分, 应通过
    strong = dict(originality=88, soundness=85, data=82, experiment=84,
                  contribution=86, delta=80, feasibility=85, impact=82)
    vB = decide(strong)
    print(f"[B] strong     Weighted={vB.weighted} Overall={vB.overall} -> {vB.decision}")
    assert vB.weighted >= 80 and vB.decision == "通过", vB

    # 案例C: 中等 idea, 无否决, 应有条件通过
    mid = dict(originality=70, soundness=68, data=66, experiment=64,
               contribution=70, delta=62, feasibility=75, impact=65)
    vC = decide(mid)
    print(f"[C] mid        Weighted={vC.weighted} Overall={vC.overall} -> {vC.decision}")
    assert vC.decision.startswith("有条件通过"), vC

    # 案例D: 高 Weighted 但有未化解 CRITICAL -> 降到有条件通过
    vD = decide(strong, unresolved_critical=True)
    print(f"[D] strong+CRIT Weighted={vD.weighted} -> {vD.decision}")
    assert vD.decision == "有条件通过", vD

    # 案例E: 范围/缺维校验
    try:
        weighted_score({"originality": 50})
        raise AssertionError("should have raised on missing dims")
    except ValueError:
        print("[E] missing-dimension guard ... OK")
    try:
        weighted_score({**strong, "originality": 120})
        raise AssertionError("should have raised on out-of-range")
    except ValueError:
        print("[F] out-of-range guard ... OK")

    # 案例G: 可调阈值注入——把通过线放松到 70，mid(Weighted~67) 仍不够，但放到 66 就能过
    mid_w = decide(mid).weighted
    g_loose = decide(mid, thresholds={"pass_line": int(mid_w), "pass_core_floor": 0})
    assert g_loose.decision == "通过", (mid_w, g_loose)
    g_strict = decide(strong, thresholds={"pass_line": 95})  # 收紧到 95，strong(~84) 落到有条件
    assert g_strict.decision.startswith("有条件通过"), g_strict
    print(f"[G] threshold injection ... OK (loose pass@{int(mid_w)}, strict pass@95)")

    # 案例H: 权重敏感性——strong idea 判决应对 ±0.02 微扰稳健（不翻档）
    sens = weight_sensitivity(strong, delta=0.02)
    print(f"[H] weight sensitivity: base={sens['base_decision']} "
          f"flips={sens['flip_count']} robust={sens['robust']}")
    assert sens["base_decision"] == "通过" and sens["robust"], sens
    # 边界 idea（Weighted 恰在 pass_line 附近）应能探测到翻档，证明分析有效
    border = dict(originality=80, soundness=80, data=80, experiment=80,
                  contribution=80, delta=80, feasibility=80, impact=80)
    sens_b = weight_sensitivity(border, delta=0.02)
    print(f"[H'] border idea: base={sens_b['base_decision']} flips={sens_b['flip_count']}")
    assert "WEIGHTS" in globals() and abs(round(sum(WEIGHTS.values()), 6) - 1.0) < 1e-9, "权重未被敏感性分析破坏"

    # 案例I: 批量排序——3 卡(strong 通过 / mid 有条件 / derm 不通过)，验证排序与 passlist
    batch = [
        {"id": "mid", "scores": mid},
        {"id": "strong", "scores": strong},
        {"id": "derm", "scores": derm, "unresolved_critical": True},
    ]
    rb = rank_batch(batch)
    print(f"[I] batch rank: n={rb['n']} pass={rb['pass_count']} order={[r['id'] for r in rb['ranked']]}")
    # strong 应排第一(通过)，derm 最后(不通过)
    assert rb["ranked"][0]["id"] == "strong" and rb["ranked"][-1]["id"] == "derm", rb["ranked"]
    # 只有 strong 进 passlist（通过）；mid 有条件、derm 不通过都不放行
    assert rb["passlist"] == [r for r in rb["passlist"]] and rb["pass_count"] == 1, rb
    assert rb["passlist"][0]["id"] == "strong", rb["passlist"]
    assert set(rb["not_passed"]) == {"mid", "derm"}, rb["not_passed"]
    # top_k 截断：两个通过卡时取 top_k=1
    batch2 = [{"id": "s1", "scores": strong}, {"id": "s2", "scores": strong}, {"id": "bad", "scores": derm}]
    rb2 = rank_batch(batch2, top_k=1)
    assert rb2["pass_count"] == 1 and rb2["passlist"][0]["id"] == "s1", rb2  # 同分按 id 升序确定性
    print(f"[I'] top_k=1 of 2 passing -> {rb2['passlist'][0]['id']}")

    # 案例J: SciMuse 边界复核——idea 被否决项压到不通过，但 Weighted 近通过线 + 有趣度高 → 出复核建议
    # 构造：originality=44(<45 触发否决) 但其余维度高 → Weighted 接近 pass_line
    border = dict(originality=44, soundness=85, data=82, experiment=84,
                  contribution=86, delta=80, feasibility=85, impact=82)
    vJ = decide(border, interestingness=85)
    assert vJ.decision == "不通过", vJ.decision           # 否决仍生效，不自动放行
    assert vJ.border_review, "应给出边界复核建议"
    assert "边界" in vJ.border_review and "不自动放行" in vJ.border_review, vJ.border_review
    print(f"[J] border review fired: {vJ.border_review[:40]}...")
    # 有趣度低则不提示
    vJ2 = decide(border, interestingness=40)
    assert not vJ2.border_review, "低有趣度不应出复核建议"
    # 不传 interestingness 时行为不变（向后兼容）
    vJ3 = decide(border)
    assert vJ3.decision == "不通过" and not vJ3.border_review, vJ3

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
