#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_access_level.py — 数据访问分级守门，防止高敏数据误流入公开产物。

每份数据/派生材料在数据卡里声明一个 access_level：
  raw            含 PII / 未脱敏的原始数据
  redacted       已脱敏 / 去标识
  verified_only  已核验可公开的派生数据 / 聚合统计

下游环节（sink）按"是否公开"分级。校验规则：数据只能流向**不低于**其
要求的 sink——raw 不得进入任何公开 sink，redacted 公开前需先升级到
verified_only。这不是加密，是流向守门：把"这份数据能去哪"变成可校验的
规则，而非靠记忆。

诚实原则：脚本只按声明的 access_level 判定，不猜测数据是否真的脱敏干净——
真实脱敏是否到位仍需人工与 a10 research-ethics 复核。脚本拦的是"声明级别
与目标 sink 不匹配"这类机械错误。

用法：
  # 单点校验：这个级别的数据能流向这个 sink 吗？
  python check_access_level.py --level raw --sink paper
  # 批量校验一个清单（JSON: [{name, level, sink}]）
  python check_access_level.py --manifest flows.json --out report.json
  # 自测
  python check_access_level.py --selftest
"""
from __future__ import annotations

import argparse
import json
import sys

# sink 公开程度：数字越大越公开。
SINK_EXPOSURE = {
    "internal-analysis": 0,   # 内部分析、跑实验
    "internal-report": 1,     # 内部报告 / 给导师看
    "paper": 2,               # 论文正文 / 表格 / 附录
    "figure": 2,              # 公开图表
    "public-repo": 3,         # 公开代码仓库样例数据
    "public-release": 3,      # 数据集公开发布
}

# 每个 access_level 允许流向的最高公开度（含）。
LEVEL_MAX_EXPOSURE = {
    "raw": 0,            # 只能内部分析，绝不公开
    "redacted": 1,       # 可到内部报告；再公开需升级
    "verified_only": 3,  # 可进入任何公开产物
}

LEVELS = list(LEVEL_MAX_EXPOSURE)


def check(level: str, sink: str) -> dict:
    """返回单条流向的判定。三态：pass / blocked / unknown。"""
    if level not in LEVEL_MAX_EXPOSURE:
        return {"status": "unknown", "level": level, "sink": sink,
                "reason": f"未知 access_level：{level}（应为 {LEVELS}）"}
    if sink not in SINK_EXPOSURE:
        return {"status": "unknown", "level": level, "sink": sink,
                "reason": f"未知 sink：{sink}（应为 {list(SINK_EXPOSURE)}）"}
    allowed = LEVEL_MAX_EXPOSURE[level]
    want = SINK_EXPOSURE[sink]
    if want <= allowed:
        return {"status": "pass", "level": level, "sink": sink,
                "reason": f"{level} 可流向 {sink}"}
    fix = "先脱敏升级到 redacted/verified_only" if level == "raw" else "公开前先核验升级到 verified_only"
    return {"status": "blocked", "level": level, "sink": sink,
            "reason": f"{level} 不得流向公开度更高的 {sink}——{fix}"}


def check_manifest(flows: list) -> dict:
    results = [check(f.get("level", ""), f.get("sink", "")) for f in flows]
    for f, r in zip(flows, results):
        r["name"] = f.get("name", "")
    blocked = [r for r in results if r["status"] == "blocked"]
    unknown = [r for r in results if r["status"] == "unknown"]
    return {
        "total": len(results),
        "blocked": len(blocked),
        "unknown": len(unknown),
        "passed": len(results) - len(blocked) - len(unknown),
        "results": results,
        # 有任何 blocked → 整体 FAIL（守门阻断）；只有 unknown → 需人工
        "verdict": "FAIL" if blocked else ("REVIEW" if unknown else "PASS"),
    }


def selftest() -> int:
    cases = [
        ("raw", "internal-analysis", "pass"),
        ("raw", "paper", "blocked"),
        ("raw", "public-repo", "blocked"),
        ("redacted", "internal-report", "pass"),
        ("redacted", "paper", "blocked"),
        ("verified_only", "public-release", "pass"),
        ("verified_only", "paper", "pass"),
        ("bogus", "paper", "unknown"),
        ("raw", "nowhere", "unknown"),
    ]
    ok = True
    for level, sink, expect in cases:
        got = check(level, sink)["status"]
        flag = "OK" if got == expect else "FAIL"
        if got != expect:
            ok = False
        print(f"  [{flag}] {level:>13} -> {sink:<18} expect={expect:<8} got={got}")
    print("[selftest]", "ALL PASS" if ok else "SOME FAILED")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="数据访问分级守门")
    ap.add_argument("--level", help="access_level: raw/redacted/verified_only")
    ap.add_argument("--sink", help="下游环节，见 SINK_EXPOSURE")
    ap.add_argument("--manifest", help="JSON 流向清单 [{name, level, sink}]")
    ap.add_argument("--out", help="把报告写到该 JSON 路径")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    if args.manifest:
        with open(args.manifest, encoding="utf-8") as f:
            flows = json.load(f)
        report = check_manifest(flows)
    elif args.level and args.sink:
        report = check(args.level, args.sink)
    else:
        ap.error("需要 --level+--sink，或 --manifest，或 --selftest")
        return 2

    out = json.dumps(report, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out)
    print(out)
    # blocked / FAIL 时返回非零，便于在 pipeline 里当闸门
    verdict = report.get("verdict") or report.get("status")
    return 1 if verdict in ("FAIL", "blocked") else 0


if __name__ == "__main__":
    sys.exit(main())
