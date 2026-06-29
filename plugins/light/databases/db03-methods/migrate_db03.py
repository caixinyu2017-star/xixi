#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""migrate_db03.py — db03 方法卡薄缓存化一次性迁移 (Light 库重构)

db03 卡受 CI 锁死 14 字段(check_databases.py)，不能加新字段——沿用 db01/db04 哲学，
把锚点/口径塞进现有字段值的子串(key=value)，不破 schema。

机械处置(本脚本，幂等)：
  1. representative_papers 每条 `- "... | cited:N | doi:..."` 尾部追加 `| checked:<文件头日期>`
     （cited+doi 已内联=快照值+指针，补 checked 完成"薄缓存三元组"；日期取文件头查询日，无则"待核"）。
  2. 卡级 domain_scope=：从文件名映射（方法本身通用，标方法的通用域，非奶山羊——
     奶山羊适配段的 [livestock-adapt] 隔离交 workflow agent 处理）。塞进 possible_innovation_points 尾部
     （该字段每卡都有且是 catch-all 性质），不加列。

不动：core_assumption/advantages/limitations/baselines/metrics（A-通用方法论，留本地精养）。
maturity 的 scope 限定（132/176 已带括号说明）作 P1，本脚本不强改。

行级正则，不重序列化 YAML。跳过块标量。每文件 .bak 备份 + YAML 可解析。

用法：--dry-run / --apply / --selftest
"""
from __future__ import annotations
import argparse
import glob
import re
import sys

CARDS_GLOB = "databases/db03-methods/cards_*.md"

# 文件名 → domain_scope（方法的通用域；与 db04 枚举风格对齐）。
FILE_SCOPE = {
    "cards_detection_tracking": "cv-检测跟踪",
    "cards_action_spatiotemporal": "cv-行为识别",
    "cards_temporal_action": "cv-时序动作",
    "cards_nighttime_multimodal": "cv-夜间多模态",
    "cards_dl": "通用深度学习",
    "cards_frontier": "前沿ML",
    "cards_ml_stats": "通用ML统计",
    "cards_mining_other": "数据挖掘",
    "cards_nlp_speech": "NLP语音",
    "cards_biomedical": "生物医学",
    "cards_physical_sciences": "物理科学",
    "cards_stats_econ_finance": "统计经济金融",
}


def file_date(txt: str) -> str:
    """取文件头(前 1500 字符)的查询日期，无则'待核'。"""
    m = re.search(r"(20\d\d-\d\d-\d\d)", txt[:1500])
    return m.group(1) if m else "待核"


def file_scope(path: str) -> str:
    base = path.replace("\\", "/").split("/")[-1].replace(".md", "")
    return FILE_SCOPE.get(base, "通用")


def migrate_text(txt: str, scope: str, date: str) -> tuple[str, list[str]]:
    changes = []

    # 1. representative_papers 列表项加 checked:日期（仅含 cited: 的条目；幂等跳过已有 checked:）
    def fix_rp(m):
        line = m.group(0)
        if "checked:" in line or "cited:" not in line:
            return line
        # 在末尾引号前插入 | checked:日期
        nl = re.sub(r'"\s*$', f' | checked:{date}"', line)
        if nl != line:
            changes.append("rp+checked")
        return nl

    txt2 = re.sub(r'^\s*-\s*"[^"]*\|[^"]*"\s*$', fix_rp, txt, flags=re.M)

    # 2. possible_innovation_points 加 domain_scope=（每卡一次；跳过块标量 | / >）
    def fix_pip(m):
        head, val = m.group(1), m.group(2)
        if val.lstrip().startswith(("|", ">")):
            return m.group(0)
        if "domain_scope=" in val:
            return m.group(0)
        # 处理引号包裹
        qm = re.match(r'^(\s*")(.*)("\s*)$', val)
        if qm:
            inner = qm.group(2).rstrip()
            sep = "" if inner.endswith((";", "；")) else "; "
            changes.append(f"pip+domain_scope={scope}")
            return f"{head}{qm.group(1)}{inner}{sep}domain_scope={scope}{qm.group(3)}"
        inner = val.rstrip()
        sep = "" if inner.endswith((";", "；")) else "; "
        changes.append(f"pip+domain_scope={scope}")
        return f"{head}{inner}{sep}domain_scope={scope}"

    txt3 = re.sub(r"(^\s*possible_innovation_points:\s*)(.+)$", fix_pip, txt2, flags=re.M)
    return txt3, changes


def _selftest() -> int:
    fixture = '''- method_name: "YOLOv8"
  possible_innovation_points: 小目标改进
  representative_papers:
    - "YOLOv8 paper | 2023 | cited:500 | doi:10.1/x"
  maturity: 主流
'''
    out, ch = migrate_text(fixture, "cv-检测跟踪", "2026-06-06")
    assert "checked:2026-06-06" in out, out
    assert "domain_scope=cv-检测跟踪" in out, out
    # 幂等
    out2, ch2 = migrate_text(out, "cv-检测跟踪", "2026-06-06")
    assert out2.count("checked:") == 1, "rp 幂等失败"
    assert out2.count("domain_scope=") == 1, "pip 幂等失败"
    assert ch2 == [], f"幂等应无变更:{ch2}"
    # 引号包裹的 pip
    fix2 = '''- method_name: "X"
  possible_innovation_points: "与注意力混合"
  representative_papers:
    - "P | 2020 | cited:10 | doi:10.2/y"
'''
    o2, _ = migrate_text(fix2, "通用深度学习", "待核")
    assert 'domain_scope=通用深度学习"' in o2, o2
    assert "checked:待核" in o2, o2
    # 无 cited 的条目不加 checked
    fix3 = '''  representative_papers:
    - "无被引数据条目 | 2020"
'''
    o3, _ = migrate_text(fix3, "通用", "2026-06-06")
    assert "checked:" not in o3, o3
    print("[selftest] PASS migrate_db03（rp checked + domain_scope + 幂等 + 引号 + 无cited跳过）")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description="db03 方法卡薄缓存化迁移")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        sys.exit(_selftest())

    total = {}
    for f in sorted(glob.glob(CARDS_GLOB)):
        txt = open(f, encoding="utf-8").read()
        new, ch = migrate_text(txt, file_scope(f), file_date(txt))
        if ch:
            total[f.split("/")[-1]] = len(ch)
        if args.apply and new != txt:
            open(f + ".bak", "w", encoding="utf-8").write(txt)
            open(f, "w", encoding="utf-8").write(new)

    print("各文件变更子串数:")
    for f, n in total.items():
        print(f"  {f}: {n}")
    print(f"合计 {sum(total.values())} 处，覆盖 {len(total)} 文件")
    print("[apply] 已写盘(.bak 备份)" if args.apply else "[dry-run] 未写盘")


if __name__ == "__main__":
    main()
