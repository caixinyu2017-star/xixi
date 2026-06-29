#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""validate_plan_card.py — 图表规划卡的契约校验（把 m11 的打回前移到规划阶段）。

解析一张/一批图表规划卡（templates/figure_plan_card.md 的填充实例），校验规划层字段
是否与执行层 m11(light-figure-drawing) 的 figure_export.py 约束对齐，**在规划阶段就拦下
会被 m11 打回的卡**，而不是画完才发现栏宽键不存在：

  1. target_journal 必须命中 figure_export.py JOURNAL_SPECS 的键（nature/science/cell/...）
     或为 custom；custom 必须带 custom_width_mm（且为正数，禁臆测——须注明来源 db01/实测）。
  2. column 必须是该刊在 JOURNAL_SPECS 实有的档位（如 full 仅 science/mdpi、onehalf 仅
     plos/elsevier）；custom 时 column 省略。
  3. figure_id 必须形如 F<数字>/T<数字>，批量校验时须唯一（与 m07 论文占位 [图位 F1] 对齐）。
  4. source_card 必填（命中的 db07 canonical 来源，或 new_canonical_candidate 标记）。

诚实约定：
- 校验"键是否存在 / 字段是否齐全 / 是否唯一"这类**可机检**的契约，不替你判断图好不好看。
- 优先从 figure_export.py 动态读 JOURNAL_SPECS（单一真相源，杜绝栏宽键漂移）；导入不到时
  回退到内置快照（标 [SNAPSHOT]，提示可能与执行层漂移，须以 figure_export.py 为准）。
- 解析失败/字段缺失如实报，不脑补默认值。

用法：
  python validate_plan_card.py card.md                # 校验单卡
  python validate_plan_card.py F1.md F2.md T1.md      # 批量（含 figure_id 唯一性）
  python validate_plan_card.py --selftest
"""
from __future__ import annotations
import argparse
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# 执行层约束的内置快照（仅当 figure_export.py 导入失败时回退；正常以 figure_export 为单一真相源）。
# 与 figure_export.py JOURNAL_SPECS 的 *_mm 键对齐（2026-06 快照）。
_SPECS_SNAPSHOT = {
    "nature": ["single", "double"],
    "science": ["single", "double", "full"],
    "cell": ["single", "double"],
    "plos": ["single", "onehalf", "double"],
    "ieee": ["single", "double"],
    "elsevier": ["single", "double", "onehalf"],
    "mdpi": ["single", "full"],
}


def load_journal_columns() -> tuple[dict, bool]:
    """返回 ({journal: [valid columns]}, is_live)。优先从 figure_export.py 动态读。"""
    here = os.path.dirname(os.path.abspath(__file__))
    fe_dir = os.path.normpath(os.path.join(here, "..", "..",
                                           "light-figure-drawing", "scripts"))
    if fe_dir not in sys.path:
        sys.path.insert(0, fe_dir)
    try:
        import figure_export as fe  # type: ignore
        specs = {}
        for jname, spec in fe.JOURNAL_SPECS.items():
            specs[jname] = [k[:-3] for k in spec if k.endswith("_mm")]
        return specs, True
    except Exception:  # noqa: BLE001 — 导入不到回退快照
        return dict(_SPECS_SNAPSHOT), False


# ---- 规划卡解析 -------------------------------------------------------------

# 卡里字段以 markdown 表格行 `| **field** | value |` 或标题 `# 图表规划卡 · F1` 承载。
_FIELD_RE = re.compile(r"^\|\s*\*{0,2}([A-Za-z_]+)\*{0,2}\s*\|\s*(.*?)\s*\|\s*$")
_TITLE_RE = re.compile(r"^#\s*图表规划卡.*?[·:]\s*`?([FT]\d+)`?", re.I)
_FIGID_RE = re.compile(r"^[FT]\d+$")


def _clean_value(v: str) -> str:
    """去掉 markdown 强调/反引号/模板占位，取裸值首段（到第一个分隔符前）。"""
    v = v.replace("**", "").replace("`", "").strip()
    # 模板未填（{{...}}）视为空
    if v.startswith("{{") and v.endswith("}}"):
        return ""
    return v


def parse_card(text: str) -> dict:
    """从规划卡 markdown 抽出待校验字段。缺失字段不脑补，留空。"""
    fields: dict[str, str] = {}
    for line in text.splitlines():
        mt = _TITLE_RE.match(line.strip())
        if mt and "figure_id" not in fields:
            fields["figure_id"] = mt.group(1).strip()
        m = _FIELD_RE.match(line)
        if m:
            key = m.group(1).strip().lower()
            val = _clean_value(m.group(2))
            # 表头行（field/value 这种）跳过
            if key in ("field", "字段") or not val:
                if key not in fields:
                    fields.setdefault(key, val)
                continue
            fields[key] = val
    # custom_width_mm 取首个数字
    if "custom_width_mm" in fields:
        mnum = re.search(r"[\d.]+", fields["custom_width_mm"])
        fields["custom_width_mm"] = mnum.group(0) if mnum else ""
    return fields


def validate_card(fields: dict, journal_cols: dict) -> list:
    """对单卡字段做契约校验，返回 errors 列表（空=通过）。"""
    errors = []
    fid = fields.get("figure_id", "")
    if not fid:
        errors.append("figure_id 缺失（须形如 F1/T1，与 m07 占位对齐）")
    elif not _FIGID_RE.match(fid):
        errors.append(f"figure_id 格式非法: {fid!r}（须 F<数字> 或 T<数字>）")

    tj = (fields.get("target_journal") or "").lower()
    col = (fields.get("column") or "").lower()
    cwm = fields.get("custom_width_mm", "")

    if not tj:
        errors.append("target_journal 缺失（须为 JOURNAL_SPECS 键或 custom）")
    elif tj == "custom":
        if not cwm:
            errors.append("target_journal=custom 必须带 custom_width_mm（数据须有来源，禁臆测）")
        else:
            try:
                if float(cwm) <= 0:
                    errors.append(f"custom_width_mm 须为正数: {cwm!r}")
            except ValueError:
                errors.append(f"custom_width_mm 非数字: {cwm!r}")
    elif tj not in journal_cols:
        errors.append(f"target_journal={tj!r} 不在 JOURNAL_SPECS: "
                      f"{sorted(journal_cols)} 或 custom")
    else:
        # 刊有效，校验 column 档位
        valid_cols = journal_cols[tj]
        if not col:
            errors.append(f"column 缺失（{tj} 可选: {valid_cols}）")
        elif col == "custom":
            if not cwm:
                errors.append("column=custom 须带 custom_width_mm")
        elif col not in valid_cols:
            errors.append(f"column={col!r} 非 {tj} 实有档位: {valid_cols}")

    if not fields.get("source_card"):
        errors.append("source_card 必填（db07 canonical 来源，或 new_canonical_candidate 标记）")
    return errors


def validate_files(paths: list, journal_cols: dict) -> dict:
    """批量校验多张卡，含 figure_id 跨卡唯一性。"""
    cards = []
    seen_ids: dict[str, list] = {}
    for p in paths:
        try:
            with open(p, encoding="utf-8") as f:
                text = f.read()
        except OSError as e:
            cards.append({"path": p, "errors": [f"读取失败: {e}"], "fields": {}})
            continue
        fields = parse_card(text)
        errs = validate_card(fields, journal_cols)
        fid = fields.get("figure_id", "")
        if fid:
            seen_ids.setdefault(fid, []).append(p)
        cards.append({"path": p, "errors": errs, "fields": fields})
    # figure_id 唯一性（批量时）
    for fid, where in seen_ids.items():
        if len(where) > 1:
            for c in cards:
                if c["fields"].get("figure_id") == fid:
                    c["errors"].append(f"figure_id={fid} 跨卡重复（出现在 {len(where)} 张卡，须唯一）")
    n_bad = sum(1 for c in cards if c["errors"])
    return {"n": len(cards), "n_pass": len(cards) - n_bad, "n_fail": n_bad, "cards": cards}


def _selftest() -> int:
    print("### validate_plan_card 离线自测", file=sys.stderr)
    cols, live = load_journal_columns()
    print(f"[specs] {'LIVE from figure_export' if live else '[SNAPSHOT] 回退内置'}: {sorted(cols)}")
    assert "nature" in cols and "single" in cols["nature"], cols
    assert "full" in cols.get("science", []) and "full" not in cols.get("nature", []), cols

    # 1) 合法卡通过
    good = ("# 图表规划卡 · `F1`\n"
            "| **figure_id** | `F1` |\n"
            "| **target_journal** | `nature` |\n"
            "| **column** | `double` |\n"
            "| **source_card** | databases/db07-figures/resources_real.md::bar_grouped |\n")
    f = parse_card(good)
    assert f["figure_id"] == "F1" and f["target_journal"] == "nature", f
    assert validate_card(f, cols) == [], validate_card(f, cols)

    # 2) column 非该刊档位（nature 无 full）
    bad_col = parse_card(good.replace("`double`", "`full`"))
    errs = validate_card(bad_col, cols)
    assert any("非 nature 实有档位" in e for e in errs), errs

    # 3) 未知刊
    bad_j = parse_card(good.replace("`nature`", "`naturee`"))
    assert any("不在 JOURNAL_SPECS" in e for e in validate_card(bad_j, cols)), bad_j

    # 4) custom 缺 width
    cust = parse_card("# 图表规划卡 · `F2`\n| **figure_id** | `F2` |\n"
                      "| **target_journal** | `custom` |\n"
                      "| **source_card** | x |\n")
    assert any("custom_width_mm" in e for e in validate_card(cust, cols)), cust
    cust2 = parse_card("# 图表规划卡 · `F3`\n| **figure_id** | `F3` |\n"
                       "| **target_journal** | `custom` |\n"
                       "| **custom_width_mm** | 120 mm（来源 db01 卡） |\n"
                       "| **source_card** | x |\n")
    assert validate_card(cust2, cols) == [], validate_card(cust2, cols)

    # 5) source_card 缺失
    no_src = parse_card("# 图表规划卡 · `F4`\n| **figure_id** | `F4` |\n"
                        "| **target_journal** | `ieee` |\n| **column** | `single` |\n")
    assert any("source_card" in e for e in validate_card(no_src, cols)), no_src

    # 6) figure_id 格式非法
    bad_id = parse_card("| **figure_id** | fig1 |\n| **target_journal** | `ieee` |\n"
                        "| **column** | `single` |\n| **source_card** | x |\n")
    assert any("figure_id 格式非法" in e for e in validate_card(bad_id, cols)), bad_id

    # 7) 模板占位未填视为空
    tmpl = parse_card("| **figure_id** | {{figure_id}} |\n")
    assert tmpl.get("figure_id", "") == "", tmpl

    print("[selftest] PASS validate_plan_card offline")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="图表规划卡契约校验（对齐 m11 执行层约束）")
    ap.add_argument("cards", nargs="*", help="规划卡 .md 路径（可多张，含 figure_id 唯一性）")
    ap.add_argument("--selftest", action="store_true", help="run offline synthetic self-test")
    args = ap.parse_args()

    if args.selftest:
        return _selftest()
    if not args.cards:
        ap.error("请提供至少一张规划卡 .md，或 --selftest")

    cols, live = load_journal_columns()
    if not live:
        print("[SNAPSHOT] 未能从 figure_export.py 动态读 JOURNAL_SPECS，用内置快照；"
              "以执行层为准。", file=sys.stderr)
    result = validate_files(args.cards, cols)
    for c in result["cards"]:
        fid = c["fields"].get("figure_id", "?")
        if c["errors"]:
            print(f"✗ {c['path']} ({fid}): {len(c['errors'])} 个问题")
            for e in c["errors"]:
                print(f"    - {e}")
        else:
            print(f"✓ {c['path']} ({fid}): 契约校验通过")
    print(f"\n[SUMMARY] {result['n_pass']}/{result['n']} 通过, {result['n_fail']} 需修正")
    return 1 if result["n_fail"] else 0


if __name__ == "__main__":
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] == "--selftest"):
        sys.exit(_selftest())
    sys.exit(main())
