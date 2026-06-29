#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
version_tag_reconcile.py —— version_history 与 git tag 对齐核对 (Light / light-memory-pm)

落地 SKILL.md/README 反复强调却零执行的纪律：「论文/PPT/代码出新版→追加
version_history 并打 `git tag -a`，二者必须对齐」。本脚本解析 db09 项目的
version_history.md 中各行的版本号 vN，与 git tag 列表比对，列出两类失配：

  TAG_NO_RECORD   有 git tag，但 version_history 里找不到对应版本记录
                  （打了 tag 忘了写记录）。
  RECORD_NO_TAG   version_history 记了某个 vN 版本，但没有对应 git tag
                  （写了记录忘了 `git tag -a`，破坏可复现）。

诚实边界：
- 「未出正式版本」类说明行（含 v0/骨架态/草稿态/未定稿/未开始）不算正式版本，
  不要求有 tag，跳过比对，避免对尚未发版的项目误报。
- 版本号按规范化比较：`v1`、`v1.0`、`v1.0.0`、`paper-v1.0` 归一到 (材料?, 主.次.修)。
  tag 前缀（paper-/code-/ppt-/fig-）若存在则参与材料维度匹配，否则只比版本号。

用法：
  # 真实项目：从 git 读 tag（在仓库内运行）
  python version_tag_reconcile.py --version-history <path> --git-dir <repo>
  # 注入式 tag 列表（不调 git，便于离线/CI）
  python version_tag_reconcile.py --version-history <path> --tags v1.0.0 v1.1.0
  python version_tag_reconcile.py --selftest    # 离线合成自测，注入 tag，不调 git

依赖：标准库（git 调用可选）；--selftest 不触网、不调 git、自清理无残留。
退出码：发现失配返回 1，否则 0；--selftest 断言失败返回 1。
"""
import sys, os, re, argparse, subprocess, tempfile, shutil

sys.stdout.reconfigure(encoding="utf-8")

ITEM_RE = re.compile(r"^\s*-\s+(.*)$")
# 版本号：可带材料前缀(paper/code/ppt/fig/figure/slides)，主.次.修任意省略
VER_RE = re.compile(
    r"\b(?:(paper|code|ppt|fig|figure|slides)[-_])?[vV](\d+)(?:\.(\d+))?(?:\.(\d+))?\b")
# 「未出正式版本」标志词：这些行的 vN 不要求有 tag
PRERELEASE_WORDS = ["骨架", "草稿", "未定稿", "未开始", "未出", "占位", "WIP", "draft"]

PREFIX_ALIAS = {"figure": "fig", "slides": "ppt"}


def _norm_material(prefix):
    if not prefix:
        return None
    p = prefix.lower()
    return PREFIX_ALIAS.get(p, p)


def _norm_version(major, minor, patch):
    """归一版本号为 (主, 次, 修) 整数三元组，缺省补 0。"""
    return (int(major), int(minor or 0), int(patch or 0))


def parse_version_history(path):
    """解析 version_history.md，返回正式版本记录列表 [{material, ver, line, lineno}]。

    跳过「未出正式版本」说明行（含 PRERELEASE_WORDS），它们不要求 tag。
    """
    records = []
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    for i, raw in enumerate(lines, 1):
        m = ITEM_RE.match(raw)
        if not m:
            continue
        body = m.group(1)
        if any(w in body for w in PRERELEASE_WORDS):
            continue  # 未发版说明行，不参与对齐
        for vm in VER_RE.finditer(body):
            mat = _norm_material(vm.group(1))
            ver = _norm_version(vm.group(2), vm.group(3), vm.group(4))
            records.append({"material": mat, "ver": ver,
                            "line": raw.strip(), "lineno": i})
    return records


def parse_tags(tag_list):
    """解析 git tag 名列表，返回 [{material, ver, tag}]；非版本 tag 跳过。"""
    out = []
    for t in tag_list:
        t = t.strip()
        if not t:
            continue
        vm = VER_RE.search(t)
        if not vm:
            continue
        out.append({"material": _norm_material(vm.group(1)),
                    "ver": _norm_version(vm.group(2), vm.group(3), vm.group(4)),
                    "tag": t})
    return out


def git_tags(repo_dir):
    """从 git 读 tag 列表；失败抛异常（由调用方处理）。"""
    res = subprocess.run(["git", "-C", repo_dir, "tag", "--list"],
                         capture_output=True, text=True, check=True)
    return [ln for ln in res.stdout.splitlines() if ln.strip()]


def _ver_str(v):
    return f"v{v[0]}.{v[1]}.{v[2]}"


def _key(material, ver):
    """对齐键：材料维度只在两侧都标了前缀时才参与；否则只比版本号。"""
    return (material, ver)


def reconcile(records, tags):
    """比对记录与 tag，返回 {tag_no_record:[...], record_no_tag:[...], matched:[...]}。

    匹配策略（两段）：
      1) 严格：material + ver 都相等。
      2) 宽松回退：当一侧 material 为 None（记录/ tag 没标前缀）时，
         只要版本号相等即视为匹配，不因前缀缺失误报。
    """
    rec_left = list(records)
    tag_left = list(tags)
    matched = []

    def _try_match(strict):
        i = 0
        while i < len(rec_left):
            r = rec_left[i]
            hit = None
            for t in tag_left:
                if r["ver"] != t["ver"]:
                    continue
                if strict:
                    if r["material"] == t["material"]:
                        hit = t; break
                else:
                    if r["material"] is None or t["material"] is None \
                            or r["material"] == t["material"]:
                        hit = t; break
            if hit:
                matched.append((r, hit))
                tag_left.remove(hit)
                rec_left.pop(i)
            else:
                i += 1

    _try_match(strict=True)
    _try_match(strict=False)

    return {
        "matched": matched,
        "record_no_tag": rec_left,   # 有记录无 tag
        "tag_no_record": tag_left,   # 有 tag 无记录
    }


def render_report(result, vh_path):
    out = ["=" * 64, "version_history ↔ git tag 对齐核对 (light-memory-pm)",
           f"version_history：{os.path.basename(vh_path)}",
           f"匹配 {len(result['matched'])} 组　"
           f"有记录无 tag {len(result['record_no_tag'])} 条　"
           f"有 tag 无记录 {len(result['tag_no_record'])} 条", "=" * 64]

    out.append(f"\n## [RECORD_NO_TAG] 有版本记录但无 git tag　({len(result['record_no_tag'])} 条)")
    if not result["record_no_tag"]:
        out.append("  （无）")
    for r in result["record_no_tag"]:
        mat = f"{r['material']}-" if r["material"] else ""
        out.append(f"  - {os.path.basename(vh_path)}:{r['lineno']}  记录 {mat}{_ver_str(r['ver'])}")
        out.append(f"      现状：{r['line']}")
        out.append(f"      建议：补 `git tag -a {mat}{_ver_str(r['ver'])} -m ...` 并 `git push --tags`")

    out.append(f"\n## [TAG_NO_RECORD] 有 git tag 但无版本记录　({len(result['tag_no_record'])} 条)")
    if not result["tag_no_record"]:
        out.append("  （无）")
    for t in result["tag_no_record"]:
        out.append(f"  - tag {t['tag']}（{_ver_str(t['ver'])}）")
        out.append(f"      建议：在 version_history.md 补 `- [日期] 材料 {_ver_str(t['ver'])} — 变更摘要`")

    out.append(f"\n## [MATCHED] 已对齐　({len(result['matched'])} 组)")
    if not result["matched"]:
        out.append("  （无）")
    for r, t in result["matched"]:
        out.append(f"  - {_ver_str(r['ver'])}  记录行 {r['lineno']}  ↔  tag {t['tag']}")

    out.append("\n" + "=" * 64)
    total = (len(result["matched"]) + len(result["record_no_tag"])
             + len(result["tag_no_record"]))
    out.append(f"完整性自检：matched+两类失配 = {total}")
    out.append("=" * 64)
    return "\n".join(out)


# ---------------------------------------------------------------------------
# 合成自测：临时 version_history + 注入式 tag 列表（不调 git），断言两类失配
# ---------------------------------------------------------------------------
SYNTH_VH = """# 版本记录 (合成自测)

- [2026-06-01] 代码 v1.0.0 — 初版，已打 tag（应 MATCHED）
- [2026-06-05] 论文 paper-v1.0 — 投稿稿，已打 tag（应 MATCHED）
- [2026-06-10] 代码 v1.1.0 — 加了跟踪模块，忘了打 tag（应 RECORD_NO_TAG）
- [2026-06-12] 代码 骨架态（未打 tag）v0 — 未发版说明行，应被跳过
"""
# 注入 tag：v1.0.0(配代码记录) / paper-v1.0(配论文记录) / code-v2.0.0(无对应记录)
SYNTH_TAGS = ["v1.0.0", "paper-v1.0", "code-v2.0.0", "not-a-version-tag"]


def selftest():
    print(">>> --selftest：临时 version_history + 注入式 tag，离线自测（不调 git）\n")
    tmp = tempfile.mkdtemp(prefix="vtr_selftest_")
    rc = 1
    try:
        vh = os.path.join(tmp, "version_history.md")
        with open(vh, "w", encoding="utf-8") as f:
            f.write(SYNTH_VH)

        records = parse_version_history(vh)
        tags = parse_tags(SYNTH_TAGS)
        result = reconcile(records, tags)
        print(render_report(result, vh))

        # 断言：
        #  - 骨架态 v0 行被跳过 -> records 仅 3 条
        #  - matched 2 组（v1.0.0、paper-v1.0）
        #  - record_no_tag 1 条（v1.1.0）
        #  - tag_no_record 1 条（code-v2.0.0；not-a-version-tag 被忽略）
        a_records = len(records) == 3
        a_matched = len(result["matched"]) == 2
        a_rnt = len(result["record_no_tag"]) == 1 and result["record_no_tag"][0]["ver"] == (1, 1, 0)
        a_tnr = len(result["tag_no_record"]) == 1 and result["tag_no_record"][0]["ver"] == (2, 0, 0)
        ok = a_records and a_matched and a_rnt and a_tnr
        print("\n[自测断言]")
        print("  骨架态行被跳过(records=3)：", "通过" if a_records else f"失败({len(records)})")
        print("  已对齐 2 组(v1.0.0/paper-v1.0)：", "通过" if a_matched else "失败")
        print("  有记录无 tag = v1.1.0：", "通过" if a_rnt else "失败")
        print("  有 tag 无记录 = code-v2.0.0：", "通过" if a_tnr else "失败")
        print("\n>>> 自测整体：", "通过 ✓" if ok else "失败 ✗")
        rc = 0 if ok else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        print(f"[清理] 已删除临时目录，无残留：{not os.path.exists(tmp)}")
    return rc


def main():
    ap = argparse.ArgumentParser(
        description="version_history ↔ git tag 对齐核对 (light-memory-pm)")
    ap.add_argument("--version-history", help="version_history.md 路径")
    ap.add_argument("--git-dir", help="git 仓库目录（从中读 tag 列表）")
    ap.add_argument("--tags", nargs="*", help="注入式 tag 列表（不调 git，便于离线/CI）")
    ap.add_argument("--selftest", action="store_true", help="离线合成自测，注入 tag，不调 git")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if not args.version_history:
        return selftest()
    if not os.path.isfile(args.version_history):
        sys.stderr.write(f"找不到 version_history：{args.version_history}\n"); return 2

    if args.tags is not None:
        tag_list = args.tags
    elif args.git_dir:
        try:
            tag_list = git_tags(args.git_dir)
        except Exception as e:
            sys.stderr.write(f"读 git tag 失败：{e}\n"); return 2
    else:
        sys.stderr.write("需提供 --tags 或 --git-dir 之一\n"); return 2

    records = parse_version_history(args.version_history)
    tags = parse_tags(tag_list)
    result = reconcile(records, tags)
    print(render_report(result, args.version_history))
    mismatch = len(result["record_no_tag"]) + len(result["tag_no_record"])
    return 1 if mismatch else 0


if __name__ == "__main__":
    sys.exit(main())
