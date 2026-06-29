#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""migrate_db01_v2.py — db01 venues.csv 薄缓存化一次性迁移 (Light 库重构 P0)

按 docs/analysis/db-upgrade 定稿的 6 条全局原则 + db01 库级决策，对 venues.csv 做结构化升级：
  1. 锚点规整：把散落 risk_note 的 OpenAlex 源 URL / ISSN 统一为标准子串 `oa_id=S...; issn=XXXX-XXXX`，
     供 venue_signal.py 精确匹配与全库 batch 复查。
  2. domain_scope 打标(G2)：CCF 档→中国CS，CAS分区(无CCF)→中国语境，纯国际SCI→通用。
  3. IF 口径机读标记(G3/G5)：真 JCR(LetPub journalid)→ `if_kind=jcr`；付费墙+代理值→ `if_kind=proxy`；
     N/A→ `if_kind=na`。让消费方机器区分权威快照 vs 代理值，不再靠人读中文。
  4. 不补造任何数据：缺 ISSN / 真 JCR 的保持原状，标 last_checked 让运行时实时查或人工核(G1)。

铁律(db01 README R4/R8)：用 csv 模块正确读写；改后物理行数==逻辑行数==输入；列数恒 19。
幂等：重复跑不重复追加子串(先检测已有 oa_id=/domain_scope=/if_kind= 再决定是否加)。

用法：
    python migrate_db01_v2.py --dry-run    # 只报告将改什么，不写盘
    python migrate_db01_v2.py --apply      # 写盘(原文件备份为 .bak)
    python migrate_db01_v2.py --selftest   # 内置 fixture 自测，不读真实库
"""
from __future__ import annotations
import argparse
import csv
import re
import sys

CSV_PATH = "databases/db01-venues-templates/venues.csv"
HEADER_LEN = 19
ISSN_RE = re.compile(r"\b\d{4}-\d{3}[\dxX]\b")
OA_RE = re.compile(r"S\d{6,}")


def extract_oa_id(risk_note: str) -> str | None:
    """从 risk_note 抽 OpenAlex 源 id（已有 oa_id= 优先，否则从 OpenAlex源=URL 抽）。"""
    m = re.search(r"oa_id=(S\d{6,})", risk_note)
    if m:
        return m.group(1)
    m = re.search(r"openalex\.org/(S\d{6,})", risk_note)
    if m:
        return m.group(1)
    m = OA_RE.search(risk_note)
    return m.group(0) if m else None


def extract_issn(indexing: str, risk_note: str) -> str | None:
    """优先已有 issn= 子串，否则从 risk_note/indexing 抽首个 ISSN 形态。"""
    m = re.search(r"issn=(\d{4}-\d{3}[\dxX])", risk_note, re.I)
    if m:
        return m.group(1)
    for blob in (risk_note, indexing):
        m = ISSN_RE.search(blob or "")
        if m:
            return m.group(0)
    return None


def decide_domain_scope(row: dict) -> str:
    """G2 偏科隔离：判定 domain_scope 取值。"""
    ccf = (row.get("ccf_level") or "").strip()
    cas = (row.get("cas_quartile") or "").strip()
    has_ccf = ccf not in ("", "N/A", "未列入") and "待核" not in ccf
    has_cas = "区" in cas
    if has_ccf:
        return "中国CS"          # CCF 是中国计算机专属评价体系
    if has_cas:
        return "中国语境"        # 中科院分区，主要对投中国体系用户有意义
    return "通用"                # 纯国际 SCI / 会议


def decide_if_kind(impact_factor: str) -> str:
    """G3/G5 IF 口径机读标记。"""
    v = impact_factor or ""
    if v.startswith("N/A"):
        return "na"
    # 真 JCR：带 LetPub journalid 且非"免费源不可得"
    if "journalid=" in v and "不可得" not in v:
        return "jcr"
    return "proxy"               # 付费墙+OpenAlex 代理值，或纯代理值


def append_subfield(risk_note: str, key: str, value: str) -> str:
    """幂等追加 `key=value` 子串到 risk_note（已有同 key 则跳过）。分号分隔。"""
    if re.search(rf"(^|[;；]\s*){re.escape(key)}=", risk_note):
        return risk_note
    sep = "" if risk_note.endswith((";", "；")) or not risk_note else "; "
    return f"{risk_note}{sep}{key}={value}"


def migrate_row(row: dict) -> tuple[dict, list[str]]:
    """对单行做 4 项处置，返回 (新行, 变更说明列表)。"""
    changes = []
    rn = row.get("risk_note") or ""

    # 1. 锚点规整
    oa = extract_oa_id(rn)
    if oa and "oa_id=" not in rn:
        rn = append_subfield(rn, "oa_id", oa)
        changes.append(f"+oa_id={oa}")
    issn = extract_issn(row.get("indexing") or "", rn)
    if issn and not re.search(r"issn=", rn, re.I):
        rn = append_subfield(rn, "issn", issn)
        changes.append(f"+issn={issn}")
    if not oa and not issn:
        changes.append("⚠无锚点(缺oa_id+issn,需联网补)")

    # 2. domain_scope
    ds = decide_domain_scope(row)
    if "domain_scope=" not in rn:
        rn = append_subfield(rn, "domain_scope", ds)
        changes.append(f"+domain_scope={ds}")

    # 3. if_kind
    kind = decide_if_kind(row.get("impact_factor") or "")
    if "if_kind=" not in rn:
        rn = append_subfield(rn, "if_kind", kind)
        changes.append(f"+if_kind={kind}")

    row["risk_note"] = rn
    return row, changes


def run(rows: list[dict]) -> tuple[list[dict], dict]:
    stats = {"oa": 0, "issn": 0, "no_anchor": 0, "ds": {}, "if": {}}
    out = []
    for row in rows:
        new, ch = migrate_row(row)
        for c in ch:
            if c.startswith("+oa_id"):
                stats["oa"] += 1
            elif c.startswith("+issn"):
                stats["issn"] += 1
            elif "无锚点" in c:
                stats["no_anchor"] += 1
            elif c.startswith("+domain_scope"):
                k = c.split("=", 1)[1]
                stats["ds"][k] = stats["ds"].get(k, 0) + 1
            elif c.startswith("+if_kind"):
                k = c.split("=", 1)[1]
                stats["if"][k] = stats["if"].get(k, 0) + 1
        out.append(new)
    return out, stats


def load(path: str) -> tuple[list[str], list[dict]]:
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)
    assert len(fieldnames) == HEADER_LEN, f"表头列数 {len(fieldnames)} != {HEADER_LEN}"
    return fieldnames, rows


def save(path: str, fieldnames: list[str], rows: list[dict]) -> None:
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def _selftest() -> int:
    fixture = [
        {"venue_name": "TPAMI", "indexing": "SCIE", "impact_factor": "18.6(JCR2024,来源LetPub journalid=3411,2025-2026版)",
         "ccf_level": "A", "cas_quartile": "1区",
         "risk_note": "OpenAlex源=https://openalex.org/S4210123; CCF等级=A"},
        {"venue_name": "Nature", "indexing": "SCIE; ISSN 0028-0836", "impact_factor": "IF=免费源不可得(付费墙,Clarivate JCR);OpenAlex 2yr均被引=16.80作替代",
         "ccf_level": "N/A", "cas_quartile": "1区", "risk_note": "顶刊"},
        {"venue_name": "SomeConf", "indexing": "EI", "impact_factor": "N/A(会议)",
         "ccf_level": "N/A", "cas_quartile": "N/A", "risk_note": "无 ISSN 无 oa"},
    ]
    out, stats = run([dict(r) for r in fixture])
    # TPAMI: 真JCR, CCF→中国CS, 有oa
    assert "if_kind=jcr" in out[0]["risk_note"], out[0]["risk_note"]
    assert "domain_scope=中国CS" in out[0]["risk_note"], out[0]["risk_note"]
    assert "oa_id=S4210123" in out[0]["risk_note"], out[0]["risk_note"]
    # Nature: 代理值, 无CCF有CAS→中国语境, 有issn
    assert "if_kind=proxy" in out[1]["risk_note"], out[1]["risk_note"]
    assert "domain_scope=中国语境" in out[1]["risk_note"], out[1]["risk_note"]
    assert "issn=0028-0836" in out[1]["risk_note"], out[1]["risk_note"]
    # SomeConf: na, 无CCF无CAS→通用, 无锚点
    assert "if_kind=na" in out[2]["risk_note"], out[2]["risk_note"]
    assert "domain_scope=通用" in out[2]["risk_note"], out[2]["risk_note"]
    assert stats["no_anchor"] == 1, stats
    # 幂等：再跑一次不重复加
    out2, _ = run(out)
    assert out2[0]["risk_note"].count("if_kind=") == 1, "幂等失败"
    assert out2[0]["risk_note"].count("domain_scope=") == 1, "幂等失败"
    print("[selftest] PASS migrate_db01_v2（锚点/domain_scope/if_kind/幂等/无锚点检测）")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description="db01 venues.csv 薄缓存化迁移")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--path", default=CSV_PATH)
    args = ap.parse_args()

    if args.selftest:
        sys.exit(_selftest())

    fieldnames, rows = load(args.path)
    n_in = len(rows)
    orig = [dict(r) for r in rows]          # 迁移前快照(run 会原地改 rows)，供备份
    out, stats = run(rows)
    assert len(out) == n_in, f"行数变化 {n_in}->{len(out)}"

    print(f"输入数据行: {n_in}")
    print(f"规整 oa_id: {stats['oa']} 行  规整 issn: {stats['issn']} 行  无锚点(需联网补): {stats['no_anchor']} 行")
    print(f"domain_scope 分布: {stats['ds']}")
    print(f"if_kind 分布: {stats['if']}")

    if args.apply:
        save(args.path + ".bak", fieldnames, orig)   # 备份迁移前快照
        save(args.path, fieldnames, out)
        # 校验回读
        fn2, rows2 = load(args.path)
        assert len(rows2) == n_in, f"写后行数 {len(rows2)} != {n_in}"
        assert len(fn2) == HEADER_LEN
        print(f"[apply] 已写盘，备份 {args.path}.bak；回读校验 行数={len(rows2)} 列数={len(fn2)} OK")
    else:
        print("[dry-run] 未写盘。加 --apply 落盘。")


if __name__ == "__main__":
    main()
