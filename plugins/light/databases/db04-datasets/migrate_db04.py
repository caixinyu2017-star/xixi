#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""migrate_db04.py — db04 数据集卡薄缓存化一次性迁移 (Light 库重构 P0)

按 docs/analysis/db-upgrade 定稿原则 + db04 库级决策，对 8 个 cards_*.md 的 YAML 卡做结构化升级。
db04 卡受 CI 锁死 16 字段（check_databases.py SCHEMAS），**不能加新字段**——故沿用 db01 哲学，
把锚点/口径/偏科标记塞进现有字段值的尾部子串（key=value，分号分隔），不破 16 字段 schema。

机械处置（本脚本，可幂等重跑）：
  1. citation 字段尾部追加 `; last_checked=<日期>; <锚点>`：
     - paper_url 是 openalex.org/W-id → 锚点 `oa_id=W...`（可 OpenAlex 实时查被引）
     - paper_url 是 doi.org/... → 锚点 `doi=...`（可 Crossref 实时查）
     - 无论文 → 锚点 `src=community`（无被引实时源，被引数若有为静态）
     last_checked 取 citation 原有的 (YYYY-MM-DD)，无则用占位标记需核。
  2. known_issues 字段尾部追加 `; domain_scope=<方向>`（G2 偏科隔离，从 domain 字段映射）。

语义处置（不在本脚本，交 workflow agent）：bias_risk/known_issues 的"通用警示 vs 偏科判断"细分。

行级正则替换（不重新序列化 YAML，保原格式/注释/引号）。幂等：已有 last_checked=/domain_scope= 则跳过。

用法：
    python migrate_db04.py --dry-run     # 报告将改什么
    python migrate_db04.py --apply       # 写盘(每文件备份 .bak)
    python migrate_db04.py --selftest    # fixture 自测
"""
from __future__ import annotations
import argparse
import glob
import re
import sys

CARDS_GLOB = "databases/db04-datasets/cards_*.md"

# domain 关键词 → domain_scope 偏科边界（G2）。匹配 domain 字段文本，首个命中为准。
DOMAIN_SCOPE_RULES = [
    ("奶山羊", "精准畜牧-奶山羊"),
    ("山羊", "精准畜牧-小反刍"),
    ("家畜", "精准畜牧"),
    ("绵羊", "精准畜牧"),
    ("奶牛", "精准畜牧"),
    ("猪", "精准畜牧"),
    ("动物", "动物视觉"),
    ("野生动物", "动物视觉"),
    ("哺乳动物", "动物视觉"),
    ("自动驾驶", "自动驾驶-特定地域"),
    ("多模态", "多模态CV"),
    ("视觉-语言", "多模态CV"),
    ("视频", "视频理解"),
    ("姿态", "CV-姿态"),
    ("计算机视觉", "通用CV"),
    ("NLP", "通用NLP"),
    ("大模型", "通用NLP"),
    ("语音", "语音"),
    ("图 /", "图学习"),
    ("引文网络", "图学习"),
    ("时序", "时序"),
    ("电力", "时序-能源"),
    ("金融", "金融-特定市场"),
    ("经济", "经济"),
    ("生物", "生物医学"),
    ("医", "生物医学"),
    ("化学", "化学-材料"),
    ("材料", "化学-材料"),
    ("物理", "物理科学"),
    ("表格", "通用表格"),
]


def map_domain_scope(domain: str) -> str:
    for kw, scope in DOMAIN_SCOPE_RULES:
        if kw in domain:
            return scope
    return "通用"


def _has_subfield(value: str, key: str) -> bool:
    return bool(re.search(rf"(^|[;；]\s*){re.escape(key)}=", value))


def _strip_quotes(v: str) -> tuple[str, str, str]:
    """拆出 (前引号, 内容, 后引号+行尾注释)。处理 YAML 值的引号包裹。"""
    m = re.match(r'^(\s*")(.*)("(?:\s*#.*)?)\s*$', v)
    if m:
        return m.group(1), m.group(2), m.group(3)
    return "", v.rstrip(), ""


def make_citation_anchor(block: str) -> str:
    """从同卡 paper_url 决定 citation 锚点子串。"""
    mp = re.search(r"paper_url:\s*\"?(\S+)", block)
    pu = mp.group(1) if mp else ""
    mw = re.search(r"openalex\.org/(W\d+)", pu)
    if mw:
        return f"oa_id={mw.group(1)}"
    md = re.search(r"(10\.\d{4,}/[^\s\";]+)", pu)
    if md:
        return f"doi={md.group(1)}"
    return "src=community"


def migrate_block(block: str) -> tuple[str, list[str]]:
    """对单卡文本块做 citation/known_issues 子串追加。返回 (新块, 变更列表)。

    安全边界：仅处理"单行标量"的 citation/known_issues。块标量(`citation: |`/`>`，值为下方
    多行缩进)结构异质(多条文献、cited:/doi: 混排)，正则不可靠，跳过留 workflow agent 按语义处理。
    """
    changes = []
    domain_m = re.search(r"^\s*domain:\s*\"?(.+?)\"?\s*$", block, re.M)
    domain = domain_m.group(1) if domain_m else ""
    scope = map_domain_scope(domain)

    # 1. citation 追加 last_checked + 锚点（跳过块标量）
    def fix_citation(m):
        raw = m.group(2)
        if raw.lstrip().startswith(("|", ">")):
            return m.group(0)  # 块标量(多行,异质)跳过留 workflow agent，不计入变更
        head, content, tail = _strip_quotes(raw)
        if _has_subfield(content, "last_checked") and (
                _has_subfield(content, "oa_id") or _has_subfield(content, "doi")
                or _has_subfield(content, "src")):
            return m.group(0)  # 已迁移
        add = []
        if not _has_subfield(content, "last_checked"):
            dm = re.search(r"\((20\d\d-\d\d-\d\d)\)", content)
            add.append(f"last_checked={dm.group(1) if dm else '待核'}")
        anchor = make_citation_anchor(block)
        akey = anchor.split("=", 1)[0]
        if not _has_subfield(content, akey):
            add.append(anchor)
        if not add:
            return m.group(0)
        sep = "" if content.rstrip().endswith((";", "；")) else "; "
        new_content = f"{content.rstrip()}{sep}{'; '.join(add)}"
        changes.append("citation+" + "+".join(a.split("=")[0] for a in add))
        return f"{m.group(1)}{head}{new_content}{tail}"

    block2 = re.sub(r"(^\s*citation:\s*)(.+)$", fix_citation, block, count=1, flags=re.M)

    # 2. known_issues 追加 domain_scope（跳过块标量）
    def fix_known(m):
        raw = m.group(2)
        if raw.lstrip().startswith(("|", ">")):
            return m.group(0)
        head, content, tail = _strip_quotes(raw)
        if _has_subfield(content, "domain_scope"):
            return m.group(0)
        sep = "" if content.rstrip().endswith((";", "；")) else "; "
        new_content = f"{content.rstrip()}{sep}domain_scope={scope}"
        changes.append(f"known_issues+domain_scope={scope}")
        return f"{m.group(1)}{head}{new_content}{tail}"

    block3 = re.sub(r"(^\s*known_issues:\s*)(.+)$", fix_known, block2, count=1, flags=re.M)
    return block3, changes


def migrate_text(txt: str) -> tuple[str, list[str]]:
    """切分卡块逐块迁移，重组。以 '- dataset_name:' 为卡边界。"""
    parts = re.split(r"(?=^\s*-\s*dataset_name:)", txt, flags=re.M)
    out, all_changes = [], []
    for p in parts:
        if "dataset_name:" in p and "citation:" in p:
            np, ch = migrate_block(p)
            out.append(np)
            all_changes.extend(ch)
        else:
            out.append(p)
    return "".join(out), all_changes


def _selftest() -> int:
    fixture = '''- dataset_name: "TestA"
  domain: "奶山羊 / 行为识别"
  paper_url: "https://openalex.org/W123456"
  citation: "Zhang et al., 2024. OpenAlex 被引 12 (2026-06-06)"
  known_issues: "标签噪声; 已饱和"
  bias_risk: "单一牧场"
'''
    out, ch = migrate_text(fixture)
    assert "last_checked=2026-06-06" in out, out
    assert "oa_id=W123456" in out, out
    assert "domain_scope=精准畜牧-奶山羊" in out, out
    # 幂等
    out2, ch2 = migrate_text(out)
    assert out2.count("last_checked=") == 1, "citation 幂等失败"
    assert out2.count("domain_scope=") == 1, "known_issues 幂等失败"
    assert ch2 == [], f"幂等应无变更: {ch2}"

    # DOI 锚点
    fix2 = '''- dataset_name: "TestB"
  domain: "生物医学 / 影像"
  paper_url: "https://doi.org/10.1038/s41597-022-01899-x"
  citation: "Lee et al., 2022. 被引 88"
  known_issues: "类别不均衡"
'''
    o2, _ = migrate_text(fix2)
    assert "doi=10.1038/s41597-022-01899-x" in o2, o2
    assert "last_checked=待核" in o2, o2  # 无日期
    assert "domain_scope=生物医学" in o2, o2

    # 无论文 → community
    fix3 = '''- dataset_name: "TestC"
  domain: "通用表格"
  paper_url: "无官方发布论文(Kaggle 社区数据集)"
  citation: "社区数据集, 无被引"
  known_issues: "无标准划分"
'''
    o3, _ = migrate_text(fix3)
    assert "src=community" in o3, o3
    assert "domain_scope=通用表格" in o3, o3
    print("[selftest] PASS migrate_db04（oa_id/doi/community 锚点 + last_checked + domain_scope + 幂等）")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description="db04 数据集卡薄缓存化迁移")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(_selftest())

    files = sorted(glob.glob(CARDS_GLOB))
    total_changes = {}
    for f in files:
        txt = open(f, encoding="utf-8").read()
        new, changes = migrate_text(txt)
        if changes:
            total_changes[f] = len(changes)
        if args.apply and new != txt:
            with open(f + ".bak", "w", encoding="utf-8") as bf:
                bf.write(txt)
            with open(f, "w", encoding="utf-8") as wf:
                wf.write(new)

    print("各文件变更子串数:")
    for f, n in total_changes.items():
        print(f"  {f.split('/')[-1]}: {n}")
    print(f"合计 {sum(total_changes.values())} 处子串追加，覆盖 {len(total_changes)} 文件")
    print("[apply] 已写盘(每文件 .bak 备份)" if args.apply else "[dry-run] 未写盘")


if __name__ == "__main__":
    main()
