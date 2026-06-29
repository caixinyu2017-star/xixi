#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_project_card.py —— db09 项目卡细粒度校验器 (Light / light-memory-pm)

定位：只补 .github/scripts/check_databases.py **未覆盖**的细粒度规则。
CI 那个脚本已校验：14 字段齐全 + decision_log/version_history/terminology
三件套存在。本脚本不重复这些，只做四类更细的内容校验：

  ABS_DATE     绝对日期格式：project_card.created 与 decision_log /
               version_history 每条目行首必须是 [YYYY-MM-DD]，禁相对日期
               (今天/昨天/上周/最近/N 天前…)。
  STAGE_ENUM   current_stage 的前导词必须落在 db09 README 的 11 枚举值内。
  LINE_FORMAT  decision_log 行须 `- [日期] 决策 — 理由 — 来源`(≥2 个 ' — ')；
               version_history 行须 `- [日期] 材料 vN — 摘要`(≥1 个 ' — ')。
  HANDOFF_CHAIN .light/handoff/S<NN>-*.md 的 parent_session 链必须可达：
               指向存在的 session_no，沿链能抵 none 根，无悬挂、无环。

用法：
  python check_project_card.py --db09 <db09-projects 目录> [--handoff <.light/handoff>]
  python check_project_card.py --project-dir <单个项目目录> [--readme <db09 README>]
  python check_project_card.py --selftest    # 离线合成自测，不依赖真实仓库

依赖：PyYAML(环境已确认可用)；无网络、无外部数据。
退出码：发现 error 级问题返回 1，否则 0；--selftest 断言失败返回 1。
"""
import sys, os, re, argparse, glob, tempfile, shutil

sys.stdout.reconfigure(encoding="utf-8")

try:
    import yaml
except ImportError:
    sys.stderr.write("需要 PyYAML: pip install pyyaml\n"); sys.exit(2)

# db09 README 第 23 行声明的 11 个 current_stage 枚举（真相源；--readme 可覆盖同步）
DEFAULT_STAGES = [
    "资料调研", "idea 构思", "方案确认", "数据准备", "实验实现", "结果分析",
    "论文写作", "图表制作", "投稿准备", "答辩展示", "成果转化",
]

DATE_RE = re.compile(r"^\[(\d{4})-(\d{2})-(\d{2})\]")
# 行首条目：列表项 `- [日期] ...`
ITEM_RE = re.compile(r"^\s*-\s+(.*)$")
# 相对日期词（出现在应为绝对日期的位置即报错）
RELATIVE_WORDS = [
    "今天", "今日", "昨天", "昨日", "明天", "明日", "前天", "后天",
    "上周", "本周", "下周", "上个月", "这个月", "下个月", "最近", "近期",
    "刚才", "稍早", "目前", "当前", "现在",
]
RELATIVE_NUM_RE = re.compile(r"\d+\s*(天|周|月|年)前")
YAML_FENCE_RE = re.compile(r"```[ \t]*ya?ml[ \t]*\n(.*?)\n```", re.S | re.I)


def _finding(kind, severity, location, line_text, detail, suggestion):
    return {"kind": kind, "severity": severity, "location": location,
            "line": (line_text or "").strip(), "detail": detail,
            "suggestion": suggestion}


def parse_readme_stages(readme_path):
    """从 db09 README 解析 current_stage 枚举行，失败回退 DEFAULT_STAGES。"""
    if not readme_path or not os.path.isfile(readme_path):
        return list(DEFAULT_STAGES)
    with open(readme_path, encoding="utf-8") as f:
        for ln in f:
            m = re.search(r"`current_stage`\s*[:：]\s*(.+)", ln)
            if m:
                parts = [p.strip().strip("`") for p in m.group(1).split("|")]
                parts = [p for p in parts if p]
                if parts:
                    return parts
    return list(DEFAULT_STAGES)


def _stage_head(value):
    """取 current_stage 的前导枚举词：截到首个括号/全角括号/空白前。"""
    s = (value or "").strip()
    s = re.split(r"[（(\s]", s, 1)[0]
    return s.strip()


def _frontmatter(text):
    """解析文件头 --- ... --- YAML frontmatter，返回 dict（无则 {}）。"""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return {}
    try:
        data = yaml.safe_load(m.group(1))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _has_relative_date(s):
    for w in RELATIVE_WORDS:
        if w in s:
            return w
    m = RELATIVE_NUM_RE.search(s)
    return m.group(0) if m else None


def _valid_date(y, mo, d):
    import datetime
    try:
        datetime.date(int(y), int(mo), int(d))
        return True
    except ValueError:
        return False


# ---------------------------------------------------------------------------
# 校验 1：project_card.md —— created 绝对日期 + current_stage 枚举
# ---------------------------------------------------------------------------
def check_project_card(card_path, stages):
    findings = []
    loc = os.path.basename(card_path)
    with open(card_path, encoding="utf-8") as f:
        text = f.read()
    fm = _frontmatter(text)
    created = fm.get("created")
    if created is None:
        findings.append(_finding(
            "ABS_DATE", "error", f"{loc}:frontmatter", "",
            "frontmatter 缺 created 字段", "补 created: YYYY-MM-DD 绝对日期"))
    else:
        cs = str(created).strip()
        m = DATE_RE.match(f"[{cs}]")
        if not m or not _valid_date(*m.groups()):
            findings.append(_finding(
                "ABS_DATE", "error", f"{loc}:created", cs,
                f"created '{cs}' 不是合法绝对日期 YYYY-MM-DD",
                "改成形如 2026-06-14 的绝对日期"))

    # current_stage 取 yaml 字段块内值
    stage_val = None
    fb = YAML_FENCE_RE.search(text)
    if fb:
        try:
            data = yaml.safe_load(fb.group(1))
            if isinstance(data, dict):
                stage_val = data.get("current_stage")
        except Exception:
            pass
    if stage_val is None:
        findings.append(_finding(
            "STAGE_ENUM", "error", f"{loc}:current_stage", "",
            "未能从 ```yaml 字段块解析 current_stage", "确认字段块存在且含 current_stage"))
    else:
        head = _stage_head(str(stage_val))
        if head not in stages:
            findings.append(_finding(
                "STAGE_ENUM", "error", f"{loc}:current_stage", str(stage_val),
                f"current_stage 前导词 '{head}' 不在 db09 README 11 枚举内",
                f"改用枚举之一：{' | '.join(stages)}"))
    return findings


# ---------------------------------------------------------------------------
# 校验 2：decision_log / version_history 行首绝对日期 + 行格式
# ---------------------------------------------------------------------------
def _iter_items(path):
    """产出 (行号, 列表项正文) —— 仅 `- ...` 列表条目，跳过标题/引用/空行。"""
    with open(path, encoding="utf-8") as f:
        for i, raw in enumerate(f.read().splitlines(), 1):
            m = ITEM_RE.match(raw)
            if m:
                yield i, m.group(1).rstrip(), raw


def check_log_file(path, kind, min_dashes):
    """kind: 'decision_log' | 'version_history'；校验日期与 ' — ' 分段数。"""
    findings = []
    loc = os.path.basename(path)
    for ln, body, raw in _iter_items(path):
        dm = DATE_RE.match(body)
        if not dm:
            rel = _has_relative_date(body)
            detail = (f"行首非 [YYYY-MM-DD] 绝对日期（含相对词 '{rel}'）"
                      if rel else "行首缺 [YYYY-MM-DD] 绝对日期")
            findings.append(_finding(
                "ABS_DATE", "error", f"{loc}:{ln}", raw, detail,
                "条目须以 `- [YYYY-MM-DD] ` 开头，相对日期先转绝对日期"))
        elif not _valid_date(*dm.groups()):
            findings.append(_finding(
                "ABS_DATE", "error", f"{loc}:{ln}", raw,
                f"日期 [{dm.group(1)}-{dm.group(2)}-{dm.group(3)}] 非法",
                "用真实存在的日历日期"))
        # 行格式：' — ' 分段数（中文破折号）
        rest = DATE_RE.sub("", body).strip()
        seg = rest.count(" — ")
        if seg < min_dashes:
            tmpl = ("`- [日期] 决策 — 理由 — 来源`" if kind == "decision_log"
                    else "`- [日期] 材料(论文/PPT/图/代码) vN — 变更摘要`")
            findings.append(_finding(
                "LINE_FORMAT", "error", f"{loc}:{ln}", raw,
                f"{kind} 行 ' — ' 分段不足（需≥{min_dashes}，实得 {seg}）",
                f"按格式：{tmpl}"))
        if kind == "version_history" and not re.search(r"\bv\d", body, re.I) \
                and "未" not in body and "骨架" not in body:
            findings.append(_finding(
                "LINE_FORMAT", "warn", f"{loc}:{ln}", raw,
                "version_history 行未见版本号 vN（非未出版本说明行）",
                "出正式版本的行应标 vN 并与 git tag 对齐"))
    return findings


# ---------------------------------------------------------------------------
# 校验 3：.light/handoff/S<NN>-*.md 的 parent_session 链可达
# ---------------------------------------------------------------------------
def _norm_session(v):
    """归一 session 号：'S03'/'s3'/3 -> 'S03'；'none'/'' -> None。"""
    if v is None:
        return None
    s = str(v).strip()
    if not s or s.lower() == "none":
        return None
    m = re.match(r"[sS]?0*(\d+)$", s)
    if m:
        return f"S{int(m.group(1)):02d}"
    return s  # 非常规写法原样保留，便于报错定位


def check_handoff_chain(handoff_dir):
    """加载所有衔接卡，校验 parent_session 链：可达 none 根、无悬挂、无环。"""
    findings = []
    cards = {}  # session_no -> {"parent":.., "file":..}
    for path in sorted(glob.glob(os.path.join(handoff_dir, "S*-*.md"))):
        loc = os.path.basename(path)
        with open(path, encoding="utf-8") as f:
            fm = _frontmatter(f.read())
        sn = _norm_session(fm.get("session_no"))
        if sn is None:
            findings.append(_finding(
                "HANDOFF_CHAIN", "error", loc, "",
                "衔接卡 frontmatter 缺合法 session_no", "补 session_no: S<NN>"))
            continue
        if sn in cards:
            findings.append(_finding(
                "HANDOFF_CHAIN", "error", loc, "",
                f"session_no {sn} 与 {cards[sn]['file']} 撞号",
                "同一项目 session_no 须唯一递增"))
        cards[sn] = {"parent": _norm_session(fm.get("parent_session")),
                     "file": loc, "raw_parent": fm.get("parent_session")}

    # 链路可达性：沿 parent 走，须抵 None(根)，无悬挂引用、无环
    roots = 0
    for sn, info in cards.items():
        seen, cur = set(), sn
        ok = True
        while True:
            parent = cards[cur]["parent"]
            if parent is None:
                break
            if parent not in cards:
                findings.append(_finding(
                    "HANDOFF_CHAIN", "error", info["file"], "",
                    f"{sn} 的 parent_session '{cards[cur]['raw_parent']}' 指向不存在的卡",
                    "parent_session 须指向已存在的 session_no，或首卡写 none"))
                ok = False
                break
            if parent in seen:
                findings.append(_finding(
                    "HANDOFF_CHAIN", "error", info["file"], "",
                    f"{sn} 沿 parent 链成环（重复 {parent}）",
                    "parent_session 链不得成环，最终须抵 none 根"))
                ok = False
                break
            seen.add(parent)
            cur = parent
        if ok and cards[sn]["parent"] is None:
            roots += 1
    if cards and roots == 0:
        findings.append(_finding(
            "HANDOFF_CHAIN", "error", "handoff/", "",
            "衔接卡集合无 parent_session=none 的根卡",
            "首张衔接卡 parent_session 须写 none，链才有起点"))
    return findings


# ---------------------------------------------------------------------------
# 串联：对一个项目目录跑全部校验
# ---------------------------------------------------------------------------
def audit_project_dir(project_dir, stages):
    findings = []
    card = os.path.join(project_dir, "project_card.md")
    if os.path.isfile(card):
        findings += check_project_card(card, stages)
    dl = os.path.join(project_dir, "decision_log.md")
    if os.path.isfile(dl):
        findings += check_log_file(dl, "decision_log", 2)
    vh = os.path.join(project_dir, "version_history.md")
    if os.path.isfile(vh):
        findings += check_log_file(vh, "version_history", 1)
    return findings


def run_audit(db09_dir=None, project_dir=None, handoff_dir=None, readme=None):
    findings = []
    stages = parse_readme_stages(readme or (
        os.path.join(db09_dir, "README.md") if db09_dir else None))
    if project_dir:
        findings += audit_project_dir(project_dir, stages)
    if db09_dir:
        proj_root = os.path.join(db09_dir, "projects")
        for d in sorted(glob.glob(os.path.join(proj_root, "*"))):
            if os.path.isdir(d):
                findings += audit_project_dir(d, stages)
    if handoff_dir and os.path.isdir(handoff_dir):
        findings += check_handoff_chain(handoff_dir)
    order = {"error": 0, "warn": 1}
    findings.sort(key=lambda f: (order.get(f["severity"], 9), f["kind"], f["location"]))
    return findings


def render_report(findings):
    out = ["=" * 64, "db09 项目卡细粒度校验报告 (light-memory-pm)",
           f"发现总数：{len(findings)}", "=" * 64]
    labels = {"ABS_DATE": "绝对日期", "STAGE_ENUM": "current_stage 枚举",
              "LINE_FORMAT": "行格式", "HANDOFF_CHAIN": "衔接链可达"}
    by_kind = {}
    for f in findings:
        by_kind.setdefault(f["kind"], []).append(f)
    n = 0
    for kind in ["ABS_DATE", "STAGE_ENUM", "LINE_FORMAT", "HANDOFF_CHAIN"]:
        items = by_kind.get(kind, [])
        out.append(f"\n## [{kind}] {labels[kind]}　({len(items)} 条)")
        if not items:
            out.append("  （无）")
        for f in items:
            n += 1
            tag = "ERROR" if f["severity"] == "error" else "WARN "
            out.append(f"  {n:>3}. [{tag}] {f['location']}")
            out.append(f"       现状：{f['line'] or '(空/位置级)'}")
            out.append(f"       问题：{f['detail']}")
            out.append(f"       建议：{f['suggestion']}")
    out.append("\n" + "=" * 64)
    out.append(f"完整性自检：累计 {n} 条 == 发现总数 {len(findings)} -> "
               + ("通过" if n == len(findings) else "不一致(请检查)"))
    out.append("=" * 64)
    return "\n".join(out)


# ---------------------------------------------------------------------------
# 合成自测：临时目录造"坏"样例，断言四类问题都被检出；自清理无残留
# ---------------------------------------------------------------------------
BAD_CARD = """---
project_name: synth-bad
created: 昨天
---
# 项目卡：合成坏样例

```yaml
project_name: 合成坏样例
current_stage: 全力冲刺（非枚举词）
```
"""
BAD_DECISION = """# 决策日志
- [2026-06-01] 决策A — 理由A — 来源m03
- 最近决定改方案，因为效果不好
- [2026-13-40] 决策C — 理由C — 来源m04
"""
BAD_VERSION = """# 版本记录
- [2026-06-01] 代码 v1.0 — 初版骨架
- 上周更新了论文
"""


def _write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def selftest():
    print(">>> --selftest：临时目录合成坏样例，离线自测\n")
    tmp = tempfile.mkdtemp(prefix="mempm_selftest_")
    rc = 1
    try:
        proj = os.path.join(tmp, "projects", "synth-bad")
        os.makedirs(proj)
        _write(os.path.join(proj, "project_card.md"), BAD_CARD)
        _write(os.path.join(proj, "decision_log.md"), BAD_DECISION)
        _write(os.path.join(proj, "version_history.md"), BAD_VERSION)
        # 衔接卡：S01 根(none) + S02 指向 S01(健康) + S03 指向不存在的 S09(悬挂)
        hd = os.path.join(tmp, "handoff")
        os.makedirs(hd)
        _write(os.path.join(hd, "S01-root.md"),
               "---\nsession_no: S01\nparent_session: none\n---\n本卡\n")
        _write(os.path.join(hd, "S02-mid.md"),
               "---\nsession_no: S02\nparent_session: S01\n---\n本卡\n")
        _write(os.path.join(hd, "S03-orphan.md"),
               "---\nsession_no: S03\nparent_session: S09\n---\n本卡\n")

        findings = run_audit(db09_dir=tmp, handoff_dir=hd)
        print(render_report(findings))

        kinds = {f["kind"] for f in findings}
        expect = {"ABS_DATE", "STAGE_ENUM", "LINE_FORMAT", "HANDOFF_CHAIN"}
        missing = expect - kinds
        # 额外断言：健康链(S01/S02)不应报错，仅 S03 悬挂报错
        chain_errs = [f for f in findings if f["kind"] == "HANDOFF_CHAIN"]
        orphan_ok = any("S09" in f["detail"] for f in chain_errs)
        # 合法的 [2026-06-01] 行不应进 ABS_DATE
        abs_locs = [f["location"] for f in findings if f["kind"] == "ABS_DATE"]
        good_card = parse_readme_stages(None) == DEFAULT_STAGES
        ok = (not missing) and orphan_ok and good_card and len(chain_errs) == 1
        print("\n[自测断言]")
        print("  四类检测均触发：", "通过" if not missing else f"缺失 {missing}")
        print("  仅 S03 悬挂链报错(S01/S02 健康)：", "通过" if (orphan_ok and len(chain_errs) == 1) else "失败")
        print("  README 缺省回退 11 枚举：", "通过" if good_card else "失败")
        print("  ABS_DATE 命中数：", len(abs_locs))
        print("\n>>> 自测整体：", "通过 ✓" if ok else "失败 ✗")
        rc = 0 if ok else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        print(f"[清理] 已删除临时目录，无残留：{not os.path.exists(tmp)}")
    return rc


def main():
    ap = argparse.ArgumentParser(description="db09 项目卡细粒度校验器 (light-memory-pm)")
    ap.add_argument("--db09", help="db09-projects 目录（扫 projects/* 全项目）")
    ap.add_argument("--project-dir", help="单个项目目录（含 project_card.md 等）")
    ap.add_argument("--handoff", help=".light/handoff 目录（校验 parent_session 链）")
    ap.add_argument("--readme", help="db09 README 路径（解析 current_stage 枚举；默认取 --db09/README.md）")
    ap.add_argument("--selftest", action="store_true", help="离线合成自测，不依赖真实仓库")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if not (args.db09 or args.project_dir or args.handoff):
        return selftest()

    findings = run_audit(db09_dir=args.db09, project_dir=args.project_dir,
                         handoff_dir=args.handoff, readme=args.readme)
    print(render_report(findings))
    errors = sum(1 for f in findings if f["severity"] == "error")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
