#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""passport.py — 产物台账（.light/passport.yaml）的读写与校验工具。

把 passport 从"手填 YAML"变成"工具调用 + schema 校验"，堵两类机械错误：
必填字段缺失、stage 序号乱序、gate.result 枚举非法。schema 对齐
references/passport.md，并新增 per-stage `revision_rounds`（返修轮次计数，
跨会话续跑时从台账读已用轮次而非重置，防返修配额刷新，见 X-2）。

YAML 依赖策略：优先 stdlib。解析时先 try-import PyYAML；装了就用，没装
就退回内置最小块式 YAML 解析器（支持本工具自身 emit 的子集：标量、块
映射、块序列、行内 [..] / {..}）。写出始终用内置 emitter，输出确定、稳定。

诚实原则：脚本只校验结构（字段在不在、序号顺不顺、枚举合不合法），
不判断 input/output 文字内容是否属实——内容真实性仍靠 a08/a10 闸门与人工。

子命令：
  init             新建台账（--project --pipeline [--created]）
  append-stage     追加一条阶段记录（字段见 --help）
  get-current-stage 读 current_stage 并打印阶段摘要
  validate         全量 schema 校验，FAIL 返回非零
  --selftest       离线合成样例自测，自清理无残留

用法示例：
  python passport.py init --project demo --pipeline A --out .light/passport.yaml
  python passport.py append-stage --file .light/passport.yaml \\
      --stage 1 --skill m01 --input "数据集+目标" --output "文献12篇" \\
      --artifacts docs/lit.md --gate-type confirm --gate-result PASS
  python passport.py get-current-stage --file .light/passport.yaml
  python passport.py validate --file .light/passport.yaml
  python passport.py --selftest
"""
from __future__ import annotations

import argparse
import datetime
import io
import os
import sys
import tempfile

# ---- schema 常量（对齐 references/passport.md）-----------------------------
GATE_TYPES = {"confirm", "decision"}
# 确认点结果枚举：PASS / FAIL / WARN / 以及 FAIL→PASS（返修后过）。
GATE_RESULTS = {"PASS", "FAIL", "WARN", "FAIL->PASS", "FAIL→PASS"}
TOP_REQUIRED = ["project", "pipeline", "created", "updated", "current_stage"]
STAGE_REQUIRED = ["stage", "skill", "input", "output"]
# 同一阶段最多 2 轮整体返修（见 references/checkpoints.md）。
MAX_REVISION_ROUNDS = 2


def now_minute() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")


# ===========================================================================
# 最小 YAML 解析器（块式子集）+ try-import PyYAML 降级
# ===========================================================================
def parse_yaml(text: str) -> dict:
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(text)
        return data if isinstance(data, dict) else {}
    except ImportError:
        return _mini_parse(text)


def _scalar(tok: str):
    """把一个标量 token 解析成 Python 值。"""
    s = tok.strip()
    if s == "" or s == "~" or s == "null":
        return None
    if len(s) >= 2 and s[0] in "\"'" and s[-1] == s[0]:
        return s[1:-1]
    if s in ("true", "True"):
        return True
    if s in ("false", "False"):
        return False
    try:
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        pass
    return s


def _flow(tok: str):
    """解析行内 [..] 或 {..}；只支持一层（够本 schema 用）。"""
    s = tok.strip()
    if s.startswith("[") and s.endswith("]"):
        body = s[1:-1].strip()
        if not body:
            return []
        return [_scalar(x) for x in _split_top(body)]
    if s.startswith("{") and s.endswith("}"):
        body = s[1:-1].strip()
        out = {}
        if not body:
            return out
        for pair in _split_top(body):
            if ":" not in pair:
                continue
            k, v = pair.split(":", 1)
            out[k.strip()] = _scalar(v)
        return out
    return _scalar(s)


def _split_top(body: str) -> list:
    """按逗号切分，但跳过引号内与括号内的逗号。"""
    parts, depth, q, cur = [], 0, "", ""
    for ch in body:
        if q:
            cur += ch
            if ch == q:
                q = ""
            continue
        if ch in "\"'":
            q = ch
            cur += ch
        elif ch in "[{":
            depth += 1
            cur += ch
        elif ch in "]}":
            depth -= 1
            cur += ch
        elif ch == "," and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    if cur.strip():
        parts.append(cur)
    return parts


def _mini_parse(text: str):
    lines = []
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        lines.append((indent, raw.strip()))
    val, _ = _parse_block(lines, 0, 0)
    return val if isinstance(val, dict) else {}


def _parse_block(lines, idx, indent):
    """解析同一缩进层级的块；返回 (value, next_idx)。"""
    if idx >= len(lines):
        return None, idx
    if lines[idx][1].startswith("- "):
        return _parse_seq(lines, idx, indent)
    return _parse_map(lines, idx, indent)


def _parse_seq(lines, idx, indent):
    seq = []
    while idx < len(lines):
        ci, content = lines[idx]
        if ci < indent or not content.startswith("- "):
            break
        if ci > indent:
            break
        rest = content[2:].strip()
        # 把 "- " 之后内容当作该项首行，构造一个伪缩进块
        item_lines = [(indent + 2, rest)]
        j = idx + 1
        while j < len(lines) and lines[j][0] > indent:
            item_lines.append(lines[j])
            j += 1
        if ":" in rest and not rest.startswith(("[", "{")):
            val, _ = _parse_map(item_lines, 0, indent + 2)
        elif item_lines[0][1].startswith("- "):
            val, _ = _parse_seq(item_lines, 0, indent + 2)
        else:
            val = _flow(rest)
        seq.append(val)
        idx = j
    return seq, idx


def _parse_map(lines, idx, indent):
    mp = {}
    while idx < len(lines):
        ci, content = lines[idx]
        if ci != indent or content.startswith("- "):
            break
        if ":" not in content:
            break
        key, _, after = content.partition(":")
        key = key.strip()
        after = after.strip()
        if after:
            mp[key] = _flow(after)
            idx += 1
        else:
            # 嵌套块：下一更深缩进
            child = []
            j = idx + 1
            while j < len(lines) and lines[j][0] > indent:
                child.append(lines[j])
                j += 1
            if child:
                child_indent = child[0][0]
                val, _ = _parse_block(child, 0, child_indent)
                mp[key] = val
            else:
                mp[key] = None
            idx = j
    return mp, idx


# ===========================================================================
# YAML 输出（内置 emitter，输出稳定确定）
# ===========================================================================
def _emit_scalar(v) -> str:
    if v is None:
        return "~"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    s = str(v)
    # 含特殊字符或可能被误解析时加引号
    if s == "" or any(c in s for c in ":#[]{}\n") or s.strip() != s:
        return '"' + s.replace('"', '\\"') + '"'
    return s


def _emit_flow_list(seq) -> str:
    return "[" + ", ".join(_emit_scalar(x) for x in seq) + "]"


def _emit_flow_map(mp) -> str:
    return "{" + ", ".join(f"{k}: {_emit_scalar(v)}" for k, v in mp.items()) + "}"


def emit_yaml(data: dict) -> str:
    """把 passport dict 写成稳定的块式 YAML。"""
    buf = io.StringIO()
    for key in ("project", "pipeline", "created", "updated", "current_stage"):
        if key in data:
            buf.write(f"{key}: {_emit_scalar(data[key])}\n")
    stages = data.get("stages") or []
    buf.write("stages:\n")
    for st in stages:
        buf.write(_emit_stage(st))
    kl = data.get("known_limitations")
    if kl:
        buf.write("known_limitations:\n")
        for item in kl:
            buf.write(f"  - {_emit_scalar(item)}\n")
    return buf.getvalue()


# stage 内字段输出顺序（缺失字段跳过）
_STAGE_ORDER = ["stage", "round", "revision_rounds", "skill",
                "input", "output", "artifacts", "gate", "gaps"]


def _emit_stage(st: dict) -> str:
    buf = io.StringIO()
    first = True
    for k in _STAGE_ORDER:
        if k not in st:
            continue
        v = st[k]
        prefix = "  - " if first else "    "
        first = False
        if k == "artifacts" and isinstance(v, list):
            buf.write(f"{prefix}{k}: {_emit_flow_list(v)}\n")
        elif k == "gate" and isinstance(v, dict):
            buf.write(f"{prefix}{k}: {_emit_flow_map(v)}\n")
        elif k == "gaps" and isinstance(v, list):
            buf.write(f"{prefix}{k}: {_emit_flow_list(v)}\n")
        else:
            buf.write(f"{prefix}{k}: {_emit_scalar(v)}\n")
    # 任何不在顺序表里的额外键也输出，保证读写往返不丢字段
    for k, v in st.items():
        if k in _STAGE_ORDER:
            continue
        prefix = "  - " if first else "    "
        first = False
        if isinstance(v, list):
            buf.write(f"{prefix}{k}: {_emit_flow_list(v)}\n")
        elif isinstance(v, dict):
            buf.write(f"{prefix}{k}: {_emit_flow_map(v)}\n")
        else:
            buf.write(f"{prefix}{k}: {_emit_scalar(v)}\n")
    return buf.getvalue()


# ===========================================================================
# 读写文件
# ===========================================================================
def load(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return parse_yaml(f.read())


def save(path: str, data: dict) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(emit_yaml(data))


# ===========================================================================
# schema 校验
# ===========================================================================
def validate(data: dict) -> dict:
    """全量校验，返回 {verdict, errors, warnings}。"""
    errors, warnings = [], []

    for k in TOP_REQUIRED:
        if k not in data or data[k] in (None, ""):
            errors.append(f"顶层缺必填字段：{k}")

    stages = data.get("stages")
    if not isinstance(stages, list):
        errors.append("stages 必须是序列")
        stages = []

    seen_nums = []
    for i, st in enumerate(stages):
        if not isinstance(st, dict):
            errors.append(f"stages[{i}] 不是映射")
            continue
        tag = f"stage[{st.get('stage', '?')}]"
        for k in STAGE_REQUIRED:
            if k not in st or st[k] in (None, ""):
                errors.append(f"{tag} 缺必填字段：{k}")
        num = st.get("stage")
        if isinstance(num, int):
            seen_nums.append(num)
        else:
            errors.append(f"{tag} 的 stage 必须是整数序号")
        # gate 校验
        gate = st.get("gate")
        if isinstance(gate, dict):
            gt = gate.get("type")
            if gt not in GATE_TYPES:
                errors.append(f"{tag} gate.type 非法：{gt}（应为 {sorted(GATE_TYPES)}）")
            if gt == "confirm":
                res = gate.get("result")
                if res not in GATE_RESULTS:
                    errors.append(f"{tag} gate.result 非法：{res}"
                                  f"（应为 {sorted(GATE_RESULTS)}）")
            elif gt == "decision":
                if not gate.get("choice"):
                    errors.append(f"{tag} 决策点 gate 缺 choice")
                if gate.get("by") != "user":
                    warnings.append(f"{tag} 决策点 gate.by 建议为 user")
        elif gate is not None:
            errors.append(f"{tag} gate 必须是映射")
        # revision_rounds 校验（X-2）
        rr = st.get("revision_rounds")
        if rr is not None:
            if not isinstance(rr, int) or rr < 0:
                errors.append(f"{tag} revision_rounds 必须是非负整数")
            elif rr > MAX_REVISION_ROUNDS:
                warnings.append(f"{tag} revision_rounds={rr} 已超 {MAX_REVISION_ROUNDS} 轮"
                                f"返修上限，超出部分应转为 known_limitations 如实记录")

    # stage 序号单调递增校验
    if seen_nums != sorted(seen_nums):
        errors.append(f"stage 序号未按升序排列：{seen_nums}")
    if len(seen_nums) != len(set(seen_nums)):
        errors.append(f"stage 序号有重复：{seen_nums}")

    # current_stage 应等于最后一条 stage
    cs = data.get("current_stage")
    if isinstance(cs, int) and seen_nums and cs != max(seen_nums):
        warnings.append(f"current_stage={cs} 与最大 stage 序号 {max(seen_nums)} 不一致")

    verdict = "FAIL" if errors else ("WARN" if warnings else "PASS")
    return {"verdict": verdict, "errors": errors, "warnings": warnings}


def revision_rounds_used(data: dict, stage_num: int) -> int:
    """断点恢复后查某阶段已用返修轮次（X-2 防配额跨会话刷新）。"""
    for st in data.get("stages") or []:
        if isinstance(st, dict) and st.get("stage") == stage_num:
            rr = st.get("revision_rounds")
            return rr if isinstance(rr, int) else 0
    return 0


# ===========================================================================
# 子命令实现
# ===========================================================================
def cmd_init(args) -> int:
    if os.path.exists(args.out) and not args.force:
        print(f"[init] 已存在：{args.out}（续跑场景，勿覆盖；要重建加 --force）",
              file=sys.stderr)
        return 1
    created = args.created or now_minute()
    data = {
        "project": args.project,
        "pipeline": args.pipeline,
        "created": created,
        "updated": created,
        "current_stage": 0,
        "stages": [],
    }
    save(args.out, data)
    print(f"[init] 已建台账：{args.out}（project={args.project} pipeline={args.pipeline}）")
    return 0


def _kv_list(pairs):
    """把 ['k=v', ...] 解析成有序 dict。"""
    out = {}
    for p in pairs or []:
        if "=" not in p:
            continue
        k, v = p.split("=", 1)
        out[k.strip()] = _scalar(v)
    return out


def cmd_append_stage(args) -> int:
    data = load(args.file)
    stage = {
        "stage": args.stage,
        "skill": args.skill,
        "input": args.input,
        "output": args.output,
    }
    if args.round is not None:
        stage["round"] = args.round
    if args.revision_rounds is not None:
        stage["revision_rounds"] = args.revision_rounds
    if args.artifacts:
        stage["artifacts"] = list(args.artifacts)
    gate = {}
    if args.gate_type:
        gate["type"] = args.gate_type
        if args.gate_type == "confirm" and args.gate_result:
            gate["result"] = args.gate_result
        if args.gate_type == "decision":
            if args.gate_choice:
                gate["choice"] = args.gate_choice
            gate["by"] = "user"
        if args.gate_notes:
            gate["notes"] = args.gate_notes
    extra = _kv_list(args.gate_kv)
    gate.update(extra)
    if gate:
        stage["gate"] = gate
    if args.gaps:
        stage["gaps"] = list(args.gaps)

    if not isinstance(data.get("stages"), list):
        data["stages"] = []
    data["stages"].append(stage)
    data["current_stage"] = args.stage
    data["updated"] = now_minute()

    rep = validate(data)
    if rep["verdict"] == "FAIL":
        for e in rep["errors"]:
            print(f"  [ERR] {e}", file=sys.stderr)
        print("[append-stage] 校验未过，未写入。", file=sys.stderr)
        return 1
    save(args.file, data)
    for w in rep["warnings"]:
        print(f"  [WARN] {w}", file=sys.stderr)
    print(f"[append-stage] 已追加 stage={args.stage} skill={args.skill}，"
          f"current_stage→{args.stage}")
    return 0


def cmd_get_current_stage(args) -> int:
    data = load(args.file)
    cs = data.get("current_stage")
    print(f"current_stage: {cs}")
    stages = data.get("stages") or []
    cur = None
    for st in stages:
        if isinstance(st, dict) and st.get("stage") == cs:
            cur = st
    if cur:
        print(f"  skill : {cur.get('skill')}")
        print(f"  output: {cur.get('output')}")
        gate = cur.get("gate") or {}
        print(f"  gate  : {gate}")
        rr = cur.get("revision_rounds")
        if rr is not None:
            print(f"  revision_rounds: {rr}/{MAX_REVISION_ROUNDS}（续跑时从此读，勿重置）")
    else:
        print("  （无匹配阶段记录，可能尚未追加任何 stage）")
    return 0


def cmd_validate(args) -> int:
    data = load(args.file)
    rep = validate(data)
    for e in rep["errors"]:
        print(f"  [ERR]  {e}")
    for w in rep["warnings"]:
        print(f"  [WARN] {w}")
    print(f"[validate] verdict={rep['verdict']}")
    return 1 if rep["verdict"] == "FAIL" else 0


# ===========================================================================
# 离线自测（合成样例，自清理无残留）
# ===========================================================================
class _NS:
    """轻量 argparse.Namespace 替身，供 selftest 直接调子命令。"""
    def __init__(self, **kw):
        self.__dict__.update(kw)


def _mk_append(path, **kw):
    return _NS(
        file=path,
        stage=kw["stage"], skill=kw["skill"],
        input=kw.get("input", "in"), output=kw.get("output", "out"),
        round=kw.get("round"), revision_rounds=kw.get("revision_rounds"),
        artifacts=kw.get("artifacts"),
        gate_type=kw.get("gate_type"), gate_result=kw.get("gate_result"),
        gate_choice=kw.get("gate_choice"), gate_notes=kw.get("gate_notes"),
        gate_kv=kw.get("gate_kv"), gaps=kw.get("gaps"),
    )


def selftest() -> int:
    ok = True
    tmp = tempfile.mkdtemp(prefix="passport_selftest_")
    path = os.path.join(tmp, "passport.yaml")
    try:
        # 1. init
        rc = cmd_init(_NS(out=path, force=False, project="demo",
                          pipeline="A", created="2026-06-08T09:00"))
        ok &= (rc == 0 and os.path.exists(path))
        print(f"  [{'OK' if rc == 0 else 'FAIL'}] init")

        # 2. 合法 confirm 阶段
        rc = cmd_append_stage(_mk_append(path, stage=1, skill="m01",
                              artifacts=["docs/lit.md"],
                              gate_type="confirm", gate_result="PASS"))
        ok &= (rc == 0)
        print(f"  [{'OK' if rc == 0 else 'FAIL'}] append confirm/PASS")

        # 3. 决策点 + 返修轮次
        rc = cmd_append_stage(_mk_append(path, stage=4, skill="m04", round=2,
                              revision_rounds=1, gate_type="decision",
                              gate_choice="微调放行"))
        ok &= (rc == 0)
        print(f"  [{'OK' if rc == 0 else 'FAIL'}] append decision + revision_rounds")

        # 4. FAIL->PASS 诚信门 + GAP
        rc = cmd_append_stage(_mk_append(path, stage=8, skill="m07",
                              revision_rounds=1, gate_type="confirm",
                              gate_result="FAIL->PASS",
                              gate_notes="2 处幻觉引用已删",
                              gaps=["[RESULT GAP] 待补敏感性分析"]))
        ok &= (rc == 0)
        print(f"  [{'OK' if rc == 0 else 'FAIL'}] append FAIL->PASS + gaps")

        # 5. 读写往返一致：重新 load 再 validate
        data = load(path)
        rep = validate(data)
        good = rep["verdict"] in ("PASS", "WARN")
        ok &= good
        print(f"  [{'OK' if good else 'FAIL'}] round-trip validate "
              f"verdict={rep['verdict']}")

        # 6. revision_rounds_used 读取（X-2 防刷新核心 API）
        used = revision_rounds_used(data, 8)
        ok &= (used == 1)
        print(f"  [{'OK' if used == 1 else 'FAIL'}] revision_rounds_used(8)={used}")

        # 7. 非法 gate.result 枚举被拦
        bad = {"project": "p", "pipeline": "A", "created": "x", "updated": "x",
               "current_stage": 1,
               "stages": [{"stage": 1, "skill": "m1", "input": "i", "output": "o",
                           "gate": {"type": "confirm", "result": "GREAT"}}]}
        rep = validate(bad)
        hit = any("gate.result" in e for e in rep["errors"])
        good = rep["verdict"] == "FAIL" and hit
        ok &= good
        print(f"  [{'OK' if good else 'FAIL'}] reject illegal gate.result")

        # 8. stage 乱序被拦
        bad2 = {"project": "p", "pipeline": "A", "created": "x", "updated": "x",
                "current_stage": 3,
                "stages": [{"stage": 3, "skill": "m1", "input": "i", "output": "o"},
                           {"stage": 2, "skill": "m2", "input": "i", "output": "o"}]}
        rep = validate(bad2)
        hit = any("升序" in e for e in rep["errors"])
        good = rep["verdict"] == "FAIL" and hit
        ok &= good
        print(f"  [{'OK' if good else 'FAIL'}] reject out-of-order stage")

        # 9. 缺必填字段被拦
        bad3 = {"project": "p", "pipeline": "A", "created": "x", "updated": "x",
                "current_stage": 1,
                "stages": [{"stage": 1, "skill": "m1", "output": "o"}]}
        rep = validate(bad3)
        hit = any("input" in e for e in rep["errors"])
        good = rep["verdict"] == "FAIL" and hit
        ok &= good
        print(f"  [{'OK' if good else 'FAIL'}] reject missing required field")
    finally:
        for f in os.listdir(tmp):
            os.remove(os.path.join(tmp, f))
        os.rmdir(tmp)
        print(f"  [cleanup] removed {tmp} exists={os.path.exists(tmp)}")

    print("[selftest]", "ALL PASS" if ok else "SOME FAILED")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="产物台账 passport.yaml 读写与校验")
    ap.add_argument("--selftest", action="store_true", help="离线合成样例自测")
    sub = ap.add_subparsers(dest="cmd")

    p = sub.add_parser("init", help="新建台账")
    p.add_argument("--project", required=True)
    p.add_argument("--pipeline", required=True)
    p.add_argument("--created", help="首次启动时间，默认当前分钟")
    p.add_argument("--out", default=".light/passport.yaml")
    p.add_argument("--force", action="store_true", help="允许覆盖已存在台账")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("append-stage", help="追加一条阶段记录")
    p.add_argument("--file", default=".light/passport.yaml")
    p.add_argument("--stage", type=int, required=True)
    p.add_argument("--skill", required=True)
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--round", type=int, help="回环阶段第几轮（m03⇄m04）")
    p.add_argument("--revision-rounds", type=int, dest="revision_rounds",
                   help="本阶段已用整体返修轮次（X-2，续跑勿重置）")
    p.add_argument("--artifacts", nargs="*", help="产物路径，相对项目根")
    p.add_argument("--gate-type", choices=sorted(GATE_TYPES))
    p.add_argument("--gate-result", help="confirm 结果：PASS/FAIL/WARN/FAIL->PASS")
    p.add_argument("--gate-choice", help="decision 用户所选分支")
    p.add_argument("--gate-notes", help="闸门备注，FAIL->PASS 须写原因")
    p.add_argument("--gate-kv", nargs="*", help="额外 gate 字段 k=v")
    p.add_argument("--gaps", nargs="*", help="本阶段 GAP 留痕")
    p.set_defaults(func=cmd_append_stage)

    p = sub.add_parser("get-current-stage", help="读 current_stage 摘要")
    p.add_argument("--file", default=".light/passport.yaml")
    p.set_defaults(func=cmd_get_current_stage)

    p = sub.add_parser("validate", help="全量 schema 校验")
    p.add_argument("--file", default=".light/passport.yaml")
    p.set_defaults(func=cmd_validate)

    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not args.cmd:
        ap.error("需要子命令（init/append-stage/get-current-stage/validate）或 --selftest")
        return 2
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
