#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sycophancy_guard.py — 反谄媚硬协议的可计算部分。

实现 references/contract.md B 节:
  - 反驳应答 1-5 评分制的统计
  - concession-rate (给 4/5 的让步比例) 计算与 >50% 报警
  - 禁连续让步检查 (同一作者连续两条都 >=4 且第二条无新证据 -> 违规)
  - 让步必须挂证据 (4/5 无 evidence -> 强制降为 3)

无外部依赖, 自带 __main__ 自测。
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Rebuttal:
    text: str
    score: int          # 1-5, 见 contract.md 表
    has_new_evidence: bool = False   # 是否挂了新证据/新检索


def normalize(rebuttals: list) -> list:
    """让步(4/5)必须挂证据, 否则强制降为3。返回(归一化后score, 备注)。"""
    out = []
    for r in rebuttals:
        s, note = r.score, ""
        if s not in (1, 2, 3, 4, 5):
            raise ValueError(f"score must be 1-5, got {s}")
        if s >= 4 and not r.has_new_evidence:
            s, note = 3, "让步无新证据->强制降为3"
        out.append((s, note))
    return out


def concession_rate(norm_scores: list) -> float:
    if not norm_scores:
        return 0.0
    concessions = sum(1 for s in norm_scores if s >= 4)
    return round(concessions / len(norm_scores) * 100, 1)


def check_consecutive(norm_scores: list) -> list:
    """禁连续让步: 相邻两条都>=4 即违规(归一化后仍>=4说明都挂了证据,
    但协议仍禁止连续让步,需第二条独立证明)。返回 (索引i, 提示) 列表。"""
    flags = []
    for i in range(1, len(norm_scores)):
        if norm_scores[i] >= 4 and norm_scores[i - 1] >= 4:
            flags.append((i, f"连续让步 @反驳#{i}#{i+1} -> 需第二条独立新证据,否则按<=3"))
    return flags


def apply_autonomous_downgrade(scores: list) -> tuple:
    """自主模式下，连续让步的第二条自动降到 3（不依赖人工复核，否则在 agent 里形同虚设）。
    返回 (降级后 scores, 降级动作列表)。"""
    out = list(scores)
    actions = []
    for i in range(1, len(out)):
        if out[i] >= 4 and out[i - 1] >= 4:
            actions.append(f"自主降级:反驳#{i+1} 因连续让步从 {out[i]} 自动降为 3")
            out[i] = 3
    return out, actions


def audit(rebuttals: list, autonomous: bool = False) -> dict:
    """concession 审计。autonomous=True 时连续让步自动降级（不留人工复核口子）。
    小 N(<4) 用绝对让步计数门限补百分比阈值的脆弱（2 条里 1 条让步=50% 不触发百分比报警但可疑）。"""
    norm = normalize(rebuttals)
    scores = [s for s, _ in norm]
    consec = check_consecutive(scores)
    auto_actions = []
    if autonomous:
        scores, auto_actions = apply_autonomous_downgrade(scores)
    rate = concession_rate(scores)
    n = len(scores)
    n_concede = sum(1 for s in scores if s >= 4)
    # 报警：百分比>50%（大 N）OR 小 N 绝对门限（N<4 且让步≥1，百分比阈值在小 N 下不可靠）
    pct_alert = rate > 50.0
    small_n_alert = (n < 4 and n_concede >= 1)
    alert = pct_alert or small_n_alert
    if pct_alert:
        msg = f"⚠ SYCOPHANCY-ALERT: concession-rate={rate}%（>50%）"
    elif small_n_alert:
        msg = f"⚠ SYCOPHANCY-ALERT: 小样本(N={n})下有 {n_concede} 条让步——百分比阈值在小 N 不可靠，按绝对门限报警，人工复核每条让步证据是否扎实"
    else:
        msg = ""
    return {
        "normalized": norm,
        "concession_rate": rate,
        "n_rebuttals": n,
        "n_concessions": n_concede,
        "sycophancy_alert": alert,
        "alert_reason": ("pct>50%" if pct_alert else ("small_n_abs" if small_n_alert else "none")),
        "alert_msg": msg,
        "consecutive_flags": [f for _, f in consec],
        "autonomous_downgrades": auto_actions,
    }


def _selftest():
    # 案例1: worked example 两条反驳 (A=2 重述, B=5 新证据)。
    # 旧逻辑 rate=50% 不报警——但小 N(N=2) 下 1 条让步即可疑，新增小 N 绝对门限应报警。
    rs = [Rebuttal("数据私有所以算首次", 2),
          Rebuttal("补了ISIC公开集+4.1% p<0.01", 5, has_new_evidence=True)]
    a = audit(rs)
    print(f"[1] rate={a['concession_rate']}% alert={a['sycophancy_alert']} reason={a['alert_reason']}")
    assert a["concession_rate"] == 50.0
    assert a["sycophancy_alert"] and a["alert_reason"] == "small_n_abs", a  # 小 N 门限触发

    # 案例2: 谄媚 - 4条里3条让步且都挂证据 -> rate 75% 报警(百分比)
    rs2 = [Rebuttal("e1", 5, True), Rebuttal("e2", 5, True),
           Rebuttal("e3", 3), Rebuttal("e4", 4, True)]
    a2 = audit(rs2)
    print(f"[2] rate={a2['concession_rate']}% -> {a2['alert_msg']}")
    assert a2["sycophancy_alert"] and a2["concession_rate"] == 75.0 and a2["alert_reason"] == "pct>50%"
    assert a2["consecutive_flags"], "应检测到连续让步"

    # 案例2b: 自主模式 - 连续让步(e1,e2)第二条自动降级为3,不留人工口子
    a2b = audit(rs2, autonomous=True)
    print(f"[2b] autonomous downgrades={a2b['autonomous_downgrades']} rate={a2b['concession_rate']}%")
    assert a2b["autonomous_downgrades"], "自主模式应有降级动作"
    assert a2b["concession_rate"] < a2["concession_rate"], "降级后让步率应下降"

    # 案例3: 让步无证据 -> 强制降为3, 不计入concession
    rs3 = [Rebuttal("空口让步", 5, has_new_evidence=False),
           Rebuttal("普通澄清", 3)]
    a3 = audit(rs3)
    print(f"[3] normalized={a3['normalized']} rate={a3['concession_rate']}%")
    assert a3["concession_rate"] == 0.0, a3
    assert "强制降为3" in a3["normalized"][0][1]
    assert not a3["sycophancy_alert"], "无让步不应报警(N<4 但 n_concede=0)"

    # 案例4: 范围校验
    try:
        normalize([Rebuttal("bad", 6)])
        raise AssertionError("should raise")
    except ValueError:
        print("[4] score range guard ... OK")

    # 案例5: 大 N 低让步率不报警(5条1让步=20%)
    rs5 = [Rebuttal("x", 2)] * 4 + [Rebuttal("y", 5, True)]
    a5 = audit(rs5)
    assert not a5["sycophancy_alert"] and a5["alert_reason"] == "none", a5

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
