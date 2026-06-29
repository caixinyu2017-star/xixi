#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""card_gate.py — 立项卡交接门禁（把"自报不被采信"做成可机检，交 m04 前拦下残卡）。

idea-generation 的 idea_card 字段与 m04 rubric 对齐，但原本"无空字段/最近邻≥3/撞车自评"
全靠人填完自检——本脚本把它变成**可机检门禁**：解析填好的 idea_card.md，校验交 m04 前必须满足的
硬条件，不满足拒绝交接（退出码 1），让残卡进不了下游严审。

校验项（对齐模板 (m04 复核) 锚点）：
  1. 必填字段非空：标题/一句话机制/新颖性主张/与最近邻差异/数据可行性（不能留模板占位或空白）
  2. 最近邻 ≥3 篇且带检索留痕（表格至少 3 行有内容，不是空 | | |）
  3. 新颖性主张已归档到三档之一（①新②增量③复现）
  4. 撞车自评已选档（①/②/③ 三选一，不能悬空）
  5. 无"应该/大概/should/probably"等模糊词支撑 (m04 复核) 字段（违反卡内"勿写应该/大概"约定）

诚实：只校验**可机检的结构完整性**，不判 idea 好不好（那是 m04 的事）。校验通过≠idea 通过，
只表示"卡填齐了、够格送审"。垃圾进垃圾出——填的内容真不真仍由 m04 对抗式复核。

用法：
  python card_gate.py --in idea_card.md
  python card_gate.py --in idea_candidates.md   # 多卡（按 "# 立项卡" 分割）逐张校验
  python card_gate.py --selftest
"""
from __future__ import annotations
import argparse
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

VAGUE_WORDS = ["应该", "大概", "可能差不多", "should ", "probably ", "maybe "]
# 敷衍填充：非空但无实质信息的占位式作答（审查实测：最近邻填"无"、差异填"更好"、
# 数据填"有数据" 能骗过纯非空校验）。这类词单独成行/成段即视为敷衍，拦下。
_PERFUNCTORY = {"无", "没有", "没", "n/a", "na", "none", "-", "暂无", "待定", "tbd",
                "更好", "更强", "更优", "有数据", "有", "够用", "足够", "可以", "能",
                "差不多", "类似", "见上", "同上", "略"}
# 最近邻文献/留痕列里的敷衍占位（填了"无/没有"冒充已检索）
_NBR_PERFUNCTORY = {"无", "没有", "没", "n/a", "na", "none", "-", "—", "待定", "tbd", "略", "见上"}
# 模板占位/空白判定：{{...}}、纯空、纯破折号
_PLACEHOLDER = re.compile(r"^\s*(\{\{.*\}\}|[-—_\s]*|例\s.*|\.\.\.)?\s*$")


def _is_perfunctory(v: str) -> bool:
    """非空但实质为敷衍占位：整段去标点后命中敷衍词集，或过短（<5 字且无数字/英文实词）。"""
    core = re.sub(r"`\(m04[^`]*\)`|\(m04[^)]*\)", "", v)  # 去复核标记
    core = re.sub(r"[\s。，、；：.,;:!！?？*>\-—_]+", "", core).lower().strip()
    if not core:
        return False  # 空交给 _is_empty 判，这里只管"非空但敷衍"
    if core in _PERFUNCTORY:
        return True
    # 极短且不含任何数字或长英文词（数字/术语通常代表实质内容）
    if len(core) < 5 and not re.search(r"\d|[a-z]{4,}", core):
        return True
    return False


def _section(card: str, header_kw: str) -> str:
    """取某 ## 小节正文（到下一个 ## 或卡尾）。header_kw 为标题关键词。"""
    lines = card.splitlines()
    out, capturing = [], False
    for ln in lines:
        if ln.startswith("##"):
            capturing = header_kw in ln
            continue
        if capturing:
            out.append(ln)
    return "\n".join(out).strip()


def _table_field(card: str, field_kw: str) -> str:
    """取 | **字段** | 值 | 形式的字段值。field_kw 命中字段名即返回该行的值列。"""
    for ln in card.splitlines():
        if ln.strip().startswith("|") and field_kw in ln:
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) >= 2:
                return cells[-1]  # 值列（去掉可能的 (m04 复核) 标记后取末列）
    return ""


def _is_empty(v: str) -> bool:
    v = re.sub(r"`\(m04[^`]*\)`|\(m04[^)]*\)", "", v).strip()  # 去掉复核标记
    return bool(_PLACEHOLDER.match(v))


def gate_card(card: str) -> dict:
    """对单张卡做门禁校验。返回 {idea_id, passed, errors, warnings}。"""
    errors, warnings = [], []
    mid = re.search(r"立项卡\s*[·\.]\s*(\S+)", card)
    idea_id = mid.group(1) if mid else "?"

    # 1) 必填表字段非空 + 非敷衍
    for kw, name in [("标题", "标题"), ("一句话机制", "一句话机制"),
                     ("新颖性主张", "新颖性主张")]:
        v = _table_field(card, kw)
        if _is_empty(v):
            errors.append(f"字段「{name}」为空或仍是模板占位")
        elif _is_perfunctory(v):
            errors.append(f"字段「{name}」是敷衍占位（如'无/更好/有'），无实质内容——m04 无法复核")

    # 2) 必填小节非空 + 非敷衍
    for kw, name in [("与最近邻的差异", "与最近邻的差异"), ("数据可行性", "数据可行性")]:
        sec = _section(card, kw)
        # 去掉小节里的说明引文(> 开头)与表头，看是否有实质内容
        body = "\n".join(l for l in sec.splitlines()
                         if l.strip() and not l.strip().startswith(">")
                         and not l.strip().startswith("|"))
        # 数据可行性是 bullet 列表，检查是否还是模板空占位（点名数据集等）
        filled = [l for l in sec.splitlines()
                  if l.strip().startswith("-") and not _is_empty(l.split("：", 1)[-1] if "：" in l else l)]
        if not body.strip() and not filled:
            errors.append(f"小节「{name}」无实质内容（仍是模板）")
        else:
            # 非敷衍校验：把小节正文(去 bullet 前缀/字段名)的实质串拿来判
            substantive = []
            for l in (body.splitlines() + filled):
                seg = l.split("：", 1)[-1] if "：" in l else l.lstrip("-* ")
                if seg.strip():
                    substantive.append(seg.strip())
            joined = " ".join(substantive)
            if substantive and all(_is_perfunctory(s) for s in substantive):
                errors.append(f"小节「{name}」全是敷衍占位（如'更好/有数据'）——m04 数据支撑维度会封顶记红旗")

    # 3) 新颖性主张归档三档
    nov = _table_field(card, "新颖性主张")
    if not _is_empty(nov) and not re.search(r"[①②③123]|新现象|增量|复现|新方法|新理论", nov):
        errors.append("新颖性主张未归档到三档之一（①新/②增量/③复现）")

    # 4) 最近邻 ≥3 篇带留痕：数三行表格里有内容的（文献/留痕列填"无"等敷衍不算数）
    nbr_sec = _section(card, "最近邻")
    rows = [l for l in nbr_sec.splitlines() if re.match(r"^\s*\|\s*\d", l)]
    filled_rows, perfunctory_rows = 0, 0
    for r in rows:
        cells = [c.strip() for c in r.strip().strip("|").split("|")]
        # cells: [#, 文献, 检索留痕, 是否等价]；文献列与留痕列都要有内容且非敷衍
        if len(cells) >= 3 and cells[1] and cells[2] and not _PLACEHOLDER.match(cells[1]):
            lit_bad = cells[1].lower() in _NBR_PERFUNCTORY
            trace_bad = cells[2].lower() in _NBR_PERFUNCTORY
            if lit_bad or trace_bad:
                perfunctory_rows += 1  # 填了"无/没有"冒充已检索
            else:
                filled_rows += 1
    if filled_rows < 3:
        extra = (f"（其中 {perfunctory_rows} 行用'无/没有'等敷衍冒充检索，不计数——"
                 "撞车检查最忌填'无'假装查过）" if perfunctory_rows else "")
        errors.append(f"最近邻工作仅 {filled_rows} 篇有内容+留痕（核心撞车要求 ≥3，一票否决项）{extra}")

    # 5) 撞车自评选档
    if "撞车自评" in card:
        seg = card[card.find("撞车自评"):card.find("撞车自评") + 200]
        if not re.search(r"[①②③]|选[一①②③]|实质等价|实质扩展|无命中", seg):
            warnings.append("撞车自评疑似未明确选档（①实质等价/②有扩展/③无命中）")

    # 6) 模糊词支撑复核字段
    for w in VAGUE_WORDS:
        if w in nov or w in _table_field(card, "一句话机制"):
            warnings.append(f"复核字段含模糊词「{w.strip()}」——m04 会要求换成可核查证据")

    return {"idea_id": idea_id, "passed": len(errors) == 0,
            "errors": errors, "warnings": warnings}


def gate_text(text: str) -> list:
    """文本可能含多张卡（idea_candidates.md），按 "# 立项卡" 分割逐张校验。
    只保留**真正以 '# 立项卡' 开头**的段（文件头引言/注释段不算卡，避免误判）。"""
    parts = re.split(r"(?=^#\s*立项卡)", text, flags=re.M)
    cards = [p for p in parts if re.match(r"^#\s*立项卡", p.strip())]
    if not cards:
        # 无标准"# 立项卡"标题时，整体当一张（单卡裸文件）
        cards = [text]
    return [gate_card(c) for c in cards]


_GOOD = """# 立项卡 · I-01
| **标题** | 时序对比学习做奶山羊发情早期识别 |
| **一句话机制** | 用自监督时序对比学习从加速度序列学发情前驱模式，无需密集标注 |
| **新颖性主张** `(m04 复核)` | ②增量：把已知对比学习框架系统化扩展到畜牧时序早期预警，明说是扩展 |

## 最近邻工作（≥3 篇，带检索留痕）
| # | 文献 | 检索留痕 | 是否等价 |
|---|---|---|---|
| 1 | Smith 2023 goat estrus CNN / 10.1/a | "estrus accelerometer"×OpenAlex HTTP200 命中12 | 否，他用监督CNN |
| 2 | Lee 2022 contrastive TS / 10.1/b | "contrastive time series"×S2 HTTP200 命中30 | 否，非畜牧 |
| 3 | Wang 2021 livestock behavior / 10.1/c | "livestock behavior self-supervised"×OpenAlex 命中8 | 否，无早期预警 |
- 撞车自评：③ 无命中且阴性证据充分 → 正常。

## 与最近邻的差异 `(m04 复核)`
相对 Smith 2023 不需密集标注；相对 Lee 2022 引入畜牧领域先验；预期早期识别提前量 +6h。

## 数据可行性 `(m04 复核 · 数据支撑维度)`
- 数据集：自采 dairygoat-sensor（对齐 db04），3000 段。
- 规模：3000 段 × 40 羊。
- 标注方式：已有兽医标注。
"""

_BAD = """# 立项卡 · I-02
| **标题** | {{标题}} |
| **一句话机制** | 应该能用深度学习提升性能 |
| **新颖性主张** `(m04 复核)` | 很新 |

## 最近邻工作（≥3 篇，带检索留痕）
| # | 文献 | 检索留痕 | 是否等价 |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

## 与最近邻的差异 `(m04 复核)`

## 数据可行性 `(m04 复核 · 数据支撑维度)`
- 数据集：
"""

# 敷衍但非空：审查实测能骗过纯非空校验的卡——最近邻填"无"、差异填"更好"、数据填"有数据"
_PERFUNCTORY_CARD = """# 立项卡 · I-03
| **标题** | 深度学习做某任务 |
| **一句话机制** | 用神经网络从数据学习特征做分类 |
| **新颖性主张** `(m04 复核)` | ①新方法 |

## 最近邻工作（≥3 篇，带检索留痕）
| # | 文献 | 检索留痕 | 是否等价 |
|---|---|---|---|
| 1 | 无 | 无 | 无 |
| 2 | 无 | 无 | 无 |
| 3 | 无 | 无 | 无 |

## 与最近邻的差异 `(m04 复核)`
更好。

## 数据可行性 `(m04 复核 · 数据支撑维度)`
- 数据集：有数据。
"""


def _selftest() -> int:
    print("### card_gate 离线自测", file=sys.stderr)
    good = gate_card(_GOOD)
    assert good["passed"], f"合格卡不应被拦: {good['errors']}"
    assert good["idea_id"] == "I-01", good

    bad = gate_card(_BAD)
    assert not bad["passed"], "残卡应被拦"
    errs = " ".join(bad["errors"])
    assert "标题" in errs, errs                    # 模板占位
    assert "最近邻" in errs, errs                  # 空表 <3
    assert any("数据可行性" in e or "与最近邻" in e for e in bad["errors"]), bad["errors"]
    # 模糊词告警（"应该"在一句话机制；"很新"未归档三档）
    assert any("新颖性主张未归档" in e for e in bad["errors"]), bad["errors"]
    assert any("模糊词" in w for w in bad["warnings"]), bad["warnings"]

    # 多卡分割
    multi = gate_text(_GOOD + "\n" + _BAD)
    assert len(multi) == 2 and multi[0]["passed"] and not multi[1]["passed"], multi

    # 敷衍但非空卡：必须被拦（审查实测过去能骗过纯非空校验）
    perf = gate_card(_PERFUNCTORY_CARD)
    assert not perf["passed"], f"敷衍卡应被拦: {perf}"
    perf_errs = " ".join(perf["errors"])
    assert "最近邻" in perf_errs and "敷衍冒充" in perf_errs, perf["errors"]  # 填"无"冒充检索被识破
    assert any("与最近邻的差异" in e for e in perf["errors"]), perf["errors"]  # "更好"敷衍
    assert any("数据可行性" in e for e in perf["errors"]), perf["errors"]      # "有数据"敷衍
    # 合格卡仍不被敷衍校验误伤
    assert gate_card(_GOOD)["passed"], "加敷衍校验后合格卡被误伤"
    print("[selftest] PASS card_gate offline")
    return 0


def render(results: list) -> str:
    lines = ["# 立项卡门禁报告", ""]
    n_pass = sum(1 for r in results if r["passed"])
    lines.append(f"{n_pass}/{len(results)} 张卡通过门禁（够格交 m04）。门禁只校验结构完整性，不判 idea 优劣。")
    lines.append("")
    for r in results:
        mark = "✅ 通过" if r["passed"] else "🛑 拦截"
        lines.append(f"## {r['idea_id']} — {mark}")
        for e in r["errors"]:
            lines.append(f"- [拦截] {e}")
        for w in r["warnings"]:
            lines.append(f"- [警示] {w}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="立项卡交接门禁（交 m04 前校验结构完整性）")
    ap.add_argument("--in", dest="infile", help="idea_card.md 或 idea_candidates.md")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest or not args.infile:
        return _selftest()
    with open(args.infile, encoding="utf-8") as f:
        results = gate_text(f.read())
    print(render(results))
    return 0 if all(r["passed"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
