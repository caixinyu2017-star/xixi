#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""plan_lint.py — 实验矩阵四要素齐全性检查 (Light / light-research-plan)

检查实验矩阵 Markdown 表每个实验行是否齐备四要素，缺一即提示：
  1. 假设      ← "对应假设" 列非空且形如 H1/H2…
  2. 变量      ← "数据集" 与 "baseline" 列均非空（自变量/控制变量的最小落地）
  3. 指标      ← "指标" 列非空
  4. 停止条件  ← "完成判定" 列非空（用什么结果回答该假设、达到判定门槛）

对应 EXP-Bench 四要素与 SKILL「实验设计」纪律：设计与结论最易跑偏。
纯离线、只读、不产文件；--selftest 用内置样例自测。

用法：
    python scripts/plan_lint.py --file experiments/experiment_matrix.md
    python scripts/plan_lint.py --selftest
退出码：0 全齐 / 1 有缺项或无法解析（可接 CI）。
"""
from __future__ import annotations
import argparse
import re
import sys

# 列名 → 要素的别名映射（容忍模板措辞差异）
COL_ALIASES = {
    "hypothesis": ("对应假设", "假设"),
    "dataset": ("数据集", "data", "数据"),
    "baseline": ("baseline", "基线", "对照"),
    "metric": ("指标", "metric", "评价指标"),
    "stop": ("完成判定", "停止条件", "判定", "成功标准"),
}
# 占位符（模板未填）视为缺项
PLACEHOLDER_RE = re.compile(r"^\s*(\{\{.*\}\}|[-—–]|n/?a|tbd|待定|待填|\.\.\.|…)?\s*$", re.I)
# 实验行 ID 形态：EXP-01 / ABL-02 / SEN-01 / GEN/ROB 等
EXP_ID_RE = re.compile(r"^[A-Z]{2,4}-?\d+$")
HYP_RE = re.compile(r"\bH\d+\b")
# 可量化阈值：含数字、不等号、p 值、百分比等——停止条件应可量化而非纯定性
QUANT_RE = re.compile(r"\d|[<>≥≤=]|p\s*[<>=]|%|百分", re.I)
# 纯定性词（停止条件只写这些 = 不可验收）
QUALITATIVE_ONLY = ("效果好", "有提升", "更优", "表现好", "可行", "成功", "提高", "改善",
                    "better", "improve", "good", "works")


def _is_blank(cell: str) -> bool:
    return bool(PLACEHOLDER_RE.match(cell or ""))


def _norm(s: str) -> str:
    return (s or "").strip().lower()


def parse_tables(text: str) -> list[list[list[str]]]:
    """把 Markdown 里所有管线表解析为 [表][行][单元格]。"""
    tables, cur = [], []
    for line in text.splitlines():
        if line.strip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            cur.append(cells)
        else:
            if cur:
                tables.append(cur)
                cur = []
    if cur:
        tables.append(cur)
    return tables


def _is_separator(row: list[str]) -> bool:
    return all(re.fullmatch(r":?-{2,}:?", c.strip() or "") for c in row if c.strip() != "") \
        and any("-" in c for c in row)


def find_experiment_table(tables: list[list[list[str]]]) -> tuple[list[str], list[list[str]]] | None:
    """找含"对应假设/假设"列且有实验 ID 行的表，返回 (表头, 数据行)。"""
    for tbl in tables:
        if len(tbl) < 2:
            continue
        header = tbl[0]
        norm_header = [_norm(h) for h in header]
        has_hyp = any(any(a in nh for a in (_norm(x) for x in COL_ALIASES["hypothesis"]))
                      for nh in norm_header)
        if not has_hyp:
            continue
        rows = [r for r in tbl[1:] if not _is_separator(r)]
        # 至少一行首列像实验 ID
        if any(EXP_ID_RE.match((r[0] or "").strip()) for r in rows if r):
            return header, rows
    return None


def _col_index(header: list[str], element: str) -> int | None:
    for i, h in enumerate(header):
        nh = _norm(h)
        if any(_norm(alias) in nh for alias in COL_ALIASES[element]):
            return i
    return None


def lint(text: str) -> dict:
    tables = parse_tables(text)
    found = find_experiment_table(tables)
    if not found:
        return {"ok": False, "error": "未找到实验矩阵表（需含「对应假设」列且有 EXP-/ABL- 等实验行）"}
    header, rows = found
    idx = {el: _col_index(header, el) for el in COL_ALIASES}
    missing_cols = [el for el, i in idx.items() if i is None]
    findings = []
    warnings = []           # 语义弱校验（不翻 ok 退出码，但提示"绿了可能仍错"）
    hyp_to_exps = {}        # 假设 → 该假设下的实验 ID 列表（覆盖度检查）
    checked = 0
    for r in rows:
        if not r or not EXP_ID_RE.match((r[0] or "").strip()):
            continue
        checked += 1
        exp_id = r[0].strip()
        gaps = []
        # 假设
        i = idx["hypothesis"]
        hyp_val = r[i] if (i is not None and i < len(r)) else ""
        if i is None or i >= len(r) or _is_blank(r[i]) or not HYP_RE.search(r[i]):
            gaps.append("假设(对应假设列空或非 H#)")
        else:
            for h in HYP_RE.findall(hyp_val):
                hyp_to_exps.setdefault(h, []).append(exp_id)
        # 变量：数据集 + baseline 都要有
        for el, label in (("dataset", "数据集"), ("baseline", "baseline")):
            j = idx[el]
            if j is None or j >= len(r) or _is_blank(r[j]):
                gaps.append(f"变量({label}空)")
        # 指标
        k = idx["metric"]
        metric_val = r[k] if (k is not None and k < len(r)) else ""
        if k is None or k >= len(r) or _is_blank(r[k]):
            gaps.append("指标(空)")
        # 停止条件
        m = idx["stop"]
        stop_val = r[m] if (m is not None and m < len(r)) else ""
        if m is None or m >= len(r) or _is_blank(r[m]):
            gaps.append("停止条件(完成判定空)")
        else:
            # 语义弱校验1：停止条件应可量化（含数字/不等号/p值），纯定性词给 warning
            if not QUANT_RE.search(stop_val):
                warnings.append(f"{exp_id}: 完成判定「{stop_val[:30]}」无可量化阈值（数字/不等号/p值），"
                                f"难以客观验收——EXP-Bench 最忌结论判定不可量化")
            elif any(q in stop_val.lower() for q in QUALITATIVE_ONLY) and not QUANT_RE.search(stop_val):
                warnings.append(f"{exp_id}: 完成判定含定性词且无量化门槛")
            # 语义弱校验2：完成判定是否提到了该行的指标（判定与指标对齐）
            if metric_val and not _is_blank(metric_val):
                # 提取指标关键 token：字母(数字)混合名(F1/R2/top-1/acc/mAP)或中文词，含短名
                mtokens = re.findall(r"[A-Za-z]+[\-\d]*|[一-鿿]{2,}", metric_val.lower())
                mtokens = [t for t in mtokens if len(t) >= 2 or any(ch.isdigit() for ch in t)]
                if mtokens and not any(t in stop_val.lower() for t in mtokens):
                    warnings.append(f"{exp_id}: 完成判定未提及指标「{metric_val[:20]}」关键词，"
                                    f"判定与指标可能脱节（绿了但判定对错存疑）")
        if gaps:
            findings.append({"exp_id": exp_id, "gaps": gaps})

    # 语义弱校验3：假设-实验覆盖度——每个假设最好有 ≥1 主实验(EXP) + ≥1 消融(ABL)
    coverage_warnings = []
    for h, exps in sorted(hyp_to_exps.items()):
        prefixes = {re.match(r"^[A-Z]+", e).group(0) for e in exps if re.match(r"^[A-Z]+", e)}
        if "ABL" not in prefixes:
            coverage_warnings.append(f"假设 {h} 无消融实验(ABL-)，仅靠 {sorted(set(exps))} 验证——"
                                     f"缺消融难归因增益来自创新点本身")
    warnings.extend(coverage_warnings)

    # 严谨性评分卡（借 ARA Rigor Reviewer）：把"齐全/语义/覆盖"汇成 0-100 严谨度，分项可审计。
    # 经验扣分制（非真值，可调）：每个硬缺项行扣 15、每条语义 warning 扣 5，封底 0。
    rigor = 100
    rigor -= 15 * len(findings)
    rigor -= 5 * len(warnings)
    rigor = max(0, rigor)
    rigor_breakdown = {
        "form_complete": len(findings) == 0,              # 四要素齐全
        "quantifiable_verdicts": not any("无可量化阈值" in w for w in warnings),
        "verdict_metric_aligned": not any("脱节" in w for w in warnings),
        "ablation_coverage": not any("消融" in w for w in warnings),
        "n_hard_gaps": len(findings),
        "n_semantic_warnings": len(warnings),
    }

    return {"ok": len(findings) == 0 and not missing_cols,
            "rigor_score": rigor, "rigor_breakdown": rigor_breakdown,
            "checked_rows": checked, "missing_columns": missing_cols,
            "findings": findings, "warnings": warnings,
            "hypotheses": {h: sorted(set(e)) for h, e in hyp_to_exps.items()}}


def _print_report(rep: dict) -> None:
    if rep.get("error"):
        print(f"[plan_lint] 解析失败: {rep['error']}")
        return
    print(f"[plan_lint] 检查 {rep['checked_rows']} 个实验行")
    if rep["missing_columns"]:
        print(f"  ⚠ 表头缺列: {', '.join(rep['missing_columns'])}（无法核对对应要素）")
    if rep["findings"]:
        for f in rep["findings"]:
            print(f"  ✗ {f['exp_id']}: 缺 {', '.join(f['gaps'])}")
    else:
        print("  ✓ 所有实验行四要素齐全（假设/变量/指标/停止条件）")
    # 语义弱校验（warning：不影响退出码，但提示"形式齐全≠语义正确"）
    if rep.get("warnings"):
        print(f"  —— 语义弱校验 {len(rep['warnings'])} 条 warning（形式齐全≠语义正确，人工核） ——")
        for w in rep["warnings"]:
            print(f"  ⚠ {w}")
    # 严谨性评分卡（借 ARA Rigor Reviewer）
    if "rigor_score" in rep:
        b = rep["rigor_breakdown"]
        print(f"  —— 严谨性评分 {rep['rigor_score']}/100（经验扣分制，可审计；非真值） ——")
        print(f"     四要素齐全={b['form_complete']} 判定可量化={b['quantifiable_verdicts']} "
              f"判定指标对齐={b['verdict_metric_aligned']} 有消融覆盖={b['ablation_coverage']}")


def _selftest() -> int:
    good = """
# 实验矩阵

| 实验ID | 对应假设 | 数据集(db04) | baseline(db03) | 指标 | 随机种子 | 状态 | 完成判定 |
|--------|----------|--------------|----------------|------|----------|------|----------|
| EXP-01 | H1 | ImageNet | ResNet50 | top-1 | 0,1,2 | 未开始 | top-1 > baseline 且 p<0.05 |
"""
    rep = lint(good)
    assert rep["ok"], rep
    assert rep["checked_rows"] == 1 and not rep["findings"], rep

    bad = """
| 实验ID | 对应假设 | 数据集(db04) | baseline(db03) | 指标 | 状态 | 完成判定 |
|--------|----------|--------------|----------------|------|------|----------|
| EXP-01 | H1 | ImageNet | ResNet50 | top-1 | 未开始 | top-1 > baseline 且 p<0.05 |
| EXP-02 | {{假设}} | {{数据集}} | ResNet50 | top-1 | 未开始 | {{判定门槛}} |
| ABL-01 | H2 | CIFAR | 移除X | acc | 未开始 | — |
"""
    rep2 = lint(bad)
    assert not rep2["ok"], rep2
    assert rep2["checked_rows"] == 3, rep2
    ids = {f["exp_id"] for f in rep2["findings"]}
    assert ids == {"EXP-02", "ABL-01"}, rep2
    exp02 = next(f for f in rep2["findings"] if f["exp_id"] == "EXP-02")
    assert any("假设" in g for g in exp02["gaps"]), exp02
    assert any("数据集" in g for g in exp02["gaps"]), exp02
    assert any("停止条件" in g for g in exp02["gaps"]), exp02
    abl = next(f for f in rep2["findings"] if f["exp_id"] == "ABL-01")
    assert any("停止条件" in g for g in abl["gaps"]), abl

    # 无实验表 → 报错而非崩
    rep3 = lint("# 没有表格\n普通文字。")
    assert not rep3["ok"] and rep3.get("error"), rep3

    # 语义弱校验：完成判定不可量化 + 判定与指标脱节 + 假设无消融
    sem = """
| 实验ID | 对应假设 | 数据集 | baseline | 指标 | 完成判定 |
|--------|----------|--------|----------|------|----------|
| EXP-01 | H1 | ImageNet | ResNet50 | top-1 acc | 效果比 baseline 好 |
| EXP-02 | H2 | CIFAR | VGG | F1 | top-1 > 0.9 |
"""
    rs = lint(sem)
    # 四要素齐全(形式) → ok=True，但应有语义 warning
    assert rs["ok"], rs
    wtext = " ".join(rs["warnings"])
    # EXP-01 完成判定"效果比baseline好"无量化阈值
    assert any("EXP-01" in w and "无可量化阈值" in w for w in rs["warnings"]), rs["warnings"]
    # EXP-02 指标是 F1 但判定写 top-1（脱节）
    assert any("EXP-02" in w and "脱节" in w for w in rs["warnings"]), rs["warnings"]
    # H1/H2 都无 ABL 消融 → 覆盖度 warning
    assert any("H1" in w and "消融" in w for w in rs["warnings"]), rs["warnings"]

    # 有消融时不报覆盖度 warning
    with_abl = """
| 实验ID | 对应假设 | 数据集 | baseline | 指标 | 完成判定 |
|--------|----------|--------|----------|------|----------|
| EXP-01 | H1 | ImageNet | ResNet50 | top-1 | top-1 > baseline 且 p<0.05 |
| ABL-01 | H1 | ImageNet | 移除X | top-1 | top-1 下降 > 2% 证明X有效 |
"""
    rab = lint(with_abl)
    assert not any("消融" in w for w in rab["warnings"]), rab["warnings"]

    # 严谨性评分卡：齐全+对齐+有消融 → 高分；缺项/多 warning → 低分
    assert rab["rigor_score"] >= 90, rab["rigor_score"]          # with_abl 干净
    assert rab["rigor_breakdown"]["ablation_coverage"], rab
    assert rs["rigor_score"] < rab["rigor_score"], (rs["rigor_score"], rab["rigor_score"])  # sem 有 warning 应更低
    assert rep2["rigor_score"] < 100, rep2["rigor_score"]        # bad 有硬缺项

    print("[selftest] PASS plan_lint（齐全/缺项/无表 + 语义弱校验 + 覆盖度 + 严谨性评分）")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description="实验矩阵四要素齐全性检查")
    ap.add_argument("--file", help="实验矩阵 Markdown 路径")
    ap.add_argument("--selftest", action="store_true", help="离线样例自测")
    args = ap.parse_args()
    if args.selftest:
        sys.exit(_selftest())
    if not args.file:
        ap.error("需 --file <实验矩阵.md> 或 --selftest")
    with open(args.file, encoding="utf-8") as f:
        rep = lint(f.read())
    _print_report(rep)
    sys.exit(0 if rep["ok"] else 1)


if __name__ == "__main__":
    main()
