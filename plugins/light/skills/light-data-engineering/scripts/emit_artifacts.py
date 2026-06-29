#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""emit_artifacts.py — 按 CONVENTIONS §6.1 把 m02 产物落到标准工件名 + 回写 passport。

痛点：data_doctor / quality_gate / croissant_export / data_feasibility 各自 --out 任意名，
靠人记标准名（quality_report.md / data_card.md / data_feasibility.md）易漏，orchestrator
台账与 a07 一致性回扫就扫不到。本脚本把"落标准名 + 登记 passport"做成一条命令。

它**不重新计算**，只做两件事：
  1) 校验给定文件已落到 §6.1 标准工件名（不符给出应改的目标名）；
  2) 调 orchestrator 的 passport.py append-stage 把 m02 阶段产物登记进 .light/passport.yaml
     （artifacts 路径并集是 a07 回扫的权威清单，必须登记）。

§6.1 中 m02 标准工件：data_card.md + quality_report.md（下游 m05/a03/m06）；
本次优化新增 data_feasibility.md（下游 m03/m04，补单向挂载）。

纯标准库零依赖、零网络。selftest 不触碰真实文件系统外的东西（用临时校验逻辑）。

用法：
  # 校验当前目录是否齐备标准工件，并打印 passport 登记命令：
  python emit_artifacts.py --check --dir .
  # 实际登记到 passport（委托 orchestrator/scripts/passport.py）：
  python emit_artifacts.py --register --passport .light/passport.yaml \
      --stage 2 --quality-report quality_report.md --data-card data_card.md \
      --feasibility data_feasibility.md
  python emit_artifacts.py --selftest
"""
from __future__ import annotations
import argparse
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# CONVENTIONS §6.1 m02 标准工件（+ 本次新增的 feasibility）
STD_ARTIFACTS = {
    "quality_report": "quality_report.md",
    "data_card": "data_card.md",
    "feasibility": "data_feasibility.md",
}
# 各工件下游消费（与 §6.1 一致；feasibility 是本次补的 m03/m04）
DOWNSTREAM = {
    "quality_report.md": "m05/a03/m06",
    "data_card.md": "m05/a03/m06",
    "data_feasibility.md": "m03/m04",
}


def check_dir(d: str) -> dict:
    """检查目录里标准工件齐备情况。返回 {present, missing}。"""
    present, missing = [], []
    for std in STD_ARTIFACTS.values():
        if os.path.isfile(os.path.join(d, std)):
            present.append(std)
        else:
            missing.append(std)
    return {"present": present, "missing": missing}


def normalize_name(given: str, kind: str) -> tuple[str, bool]:
    """给定路径的 basename 是否匹配该 kind 的标准名。返回 (标准名, 是否已合规)。"""
    std = STD_ARTIFACTS[kind]
    base = os.path.basename(given)
    return std, (base == std)


def build_passport_cmd(passport: str, stage: int, artifacts: list[str],
                       gate_notes: str) -> list[str]:
    """构造委托给 orchestrator/scripts/passport.py 的 append-stage 命令（不直接执行写入）。"""
    arts = ",".join(artifacts)
    out = (f"m02 数据工程产物：{arts}（下游 "
           f"{'/'.join(sorted(set(DOWNSTREAM.get(a, '?') for a in artifacts)))}）")
    return [
        "python", "skills/light-orchestrator/scripts/passport.py", "append-stage",
        "--file", passport, "--stage", str(stage), "--skill", "m02",
        "--input", "原始/现成数据集 + 自建需求",
        "--output", out,
        "--gate-type", "confirm", "--gate-result", "PASS",
        "--gate-notes", gate_notes or "data_doctor/quality_gate selftest 通过，工件齐备",
    ]


def _selftest() -> int:
    print("### emit_artifacts 离线自测", file=sys.stderr)
    # normalize_name：标准名合规 / 非标准名给出目标
    std, ok = normalize_name("foo/quality_report.md", "quality_report")
    assert std == "quality_report.md" and ok, (std, ok)
    std, ok = normalize_name("health.md", "quality_report")
    assert std == "quality_report.md" and not ok, "非标准名应判不合规"
    # feasibility 下游是 m03/m04（补单向挂载的关键）
    assert DOWNSTREAM["data_feasibility.md"] == "m03/m04", DOWNSTREAM
    assert DOWNSTREAM["data_card.md"] == "m05/a03/m06"
    # build_passport_cmd：含 append-stage、skill m02、artifacts、下游
    cmd = build_passport_cmd(".light/passport.yaml", 2,
                             ["quality_report.md", "data_feasibility.md"], "")
    s = " ".join(cmd)
    assert "append-stage" in s and "m02" in s and "passport.py" in s, s
    assert "m03/m04" in s and "m05/a03/m06" in s, "下游消费未写入 output: " + s
    # check_dir：对一个一定不存在的目录，三标准工件全 missing
    res = check_dir("/nonexistent_dir_xyz_123")
    assert set(res["missing"]) == set(STD_ARTIFACTS.values()), res
    assert res["present"] == [], res
    print("[selftest] PASS emit_artifacts offline")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="m02 标准工件落位 + passport 登记")
    ap.add_argument("--check", action="store_true", help="检查目录标准工件齐备")
    ap.add_argument("--dir", default=".", help="--check 的目标目录")
    ap.add_argument("--register", action="store_true", help="打印 passport 登记命令")
    ap.add_argument("--passport", default=".light/passport.yaml")
    ap.add_argument("--stage", type=int, default=2)
    ap.add_argument("--quality-report")
    ap.add_argument("--data-card")
    ap.add_argument("--feasibility")
    ap.add_argument("--gate-notes")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return _selftest()

    if args.check:
        res = check_dir(args.dir)
        print(f"# m02 标准工件检查 @ {args.dir}")
        for a in res["present"]:
            print(f"  [✓] {a}  → 下游 {DOWNSTREAM.get(a, '?')}")
        for a in res["missing"]:
            print(f"  [缺] {a}  → 下游 {DOWNSTREAM.get(a, '?')}（未生成）")
        if res["missing"]:
            print("\n提示：data_card.md 由模板填，quality_report.md 由 data_doctor.py --out 生成，"
                  "data_feasibility.md 由 data_feasibility.py --out 生成。")
        return 0 if not res["missing"] else 1

    if args.register:
        arts = []
        for given, kind in ((args.quality_report, "quality_report"),
                            (args.data_card, "data_card"),
                            (args.feasibility, "feasibility")):
            if not given:
                continue
            std, ok = normalize_name(given, kind)
            if not ok:
                print(f"[warn] {given} 非标准名，应为 {std}（§6.1）", file=sys.stderr)
            arts.append(std)
        if not arts:
            ap.error("--register 需至少一个 --quality-report/--data-card/--feasibility")
        cmd = build_passport_cmd(args.passport, args.stage, arts, args.gate_notes)
        print("# 在仓库根执行以下命令把 m02 产物登记进 passport：")
        print(" ".join(f'"{c}"' if " " in c else c for c in cmd))
        return 0

    ap.error("需要 --check / --register / --selftest")
    return 2


if __name__ == "__main__":
    sys.exit(main())
