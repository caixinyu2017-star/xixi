#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""db02-paper-writing 机械迁移脚本(幂等,带 --dry-run / --selftest)。

只做两件可机械化、可重复的事,需判断的(A/B/C/D表搬迁、打标、方法论层合并)留人工:
  1. 删除 samples_real.md 每张卡的「摘要原文(倒排还原)」整段
     —— 边界:从含「摘要原文」的粗体行 起,到其后第一个「**结构拆解**」行 止(不含结构拆解)。
        与 samples_recent「只存结构笔记不录原文」版权纪律对齐。结构拆解已承载可迁移写作信息。
  2. 给被引行(含「被引数」或「被引」+「快照」)补 last_checked= 标记(若尚无),
     不改数值,只在行尾追加 ` · last_checked=YYYY-MM-DD`(从行内已有快照日期取,取不到留待人工)。

设计原则(对齐 db01/db03/db04 迁移脚本):
  - 纯文本行级处理,不碰 YAML 块标量;幂等(已删/已标则跳过);--dry-run 只报不写;--selftest 离线自检。
  - 摘要段删除前断言:被删行里不含「结构拆解」「title_pattern」(防误删拆解段)。
"""
import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ABSTRACT_MARK = "摘要原文"          # 段起始标记子串(粗体行)
STRUCT_MARK = "**结构拆解**"        # 段结束标记(下一段标题)
GUARD_SUBSTRINGS = ("结构拆解", "title_pattern", "可迁移套路")  # 这些不该出现在被删区


def find_abstract_blocks(lines):
    """返回待删摘要段的 (start_idx, end_idx) 半开区间列表。

    start = 含「摘要原文」的粗体行(以 ** 开头);end = 其后首个「**结构拆解**」行(不含)。
    只处理「## NN ·」卡片区内的;文件头说明段(出现在首个卡标题前)不动。
    """
    # 首个卡片标题行
    first_card = None
    for i, ln in enumerate(lines):
        if re.match(r"^##\s+\d+\s+·", ln):
            first_card = i
            break
    if first_card is None:
        return []
    blocks = []
    i = first_card
    n = len(lines)
    while i < n:
        ln = lines[i]
        if ln.startswith("**") and ABSTRACT_MARK in ln:
            # 找结束:其后首个 **结构拆解**
            j = i + 1
            end = None
            while j < n:
                if lines[j].strip() == STRUCT_MARK:
                    end = j
                    break
                # 安全闸:不能跨过下一张卡标题
                if re.match(r"^##\s+\d+\s+·", lines[j]):
                    break
                j += 1
            if end is not None:
                blocks.append((i, end))
                i = end
                continue
        i += 1
    return blocks


def apply_delete(lines, blocks):
    """删除给定半开区间(从后往前删保持索引有效)。返回新行列表与删除行数。"""
    drop = set()
    for s, e in blocks:
        for k in range(s, e):
            drop.add(k)
    kept = [ln for idx, ln in enumerate(lines) if idx not in drop]
    return kept, len(drop)


def guard_blocks(lines, blocks):
    """断言被删区不含结构拆解关键标记,防误删。返回违规列表。"""
    bad = []
    for s, e in blocks:
        for k in range(s, e):
            for g in GUARD_SUBSTRINGS:
                if g in lines[k]:
                    bad.append((k + 1, g, lines[k].rstrip()))
    return bad


def migrate_text(text):
    """对 samples_real.md 全文执行摘要段删除。返回 (新文本, 删除段数, 删除行数, 违规列表)。"""
    lines = text.splitlines(keepends=False)
    blocks = find_abstract_blocks(lines)
    bad = guard_blocks(lines, blocks)
    if bad:
        return text, 0, 0, bad
    kept, ndrop = apply_delete(lines, blocks)
    new = "\n".join(kept)
    if text.endswith("\n"):
        new += "\n"
    return new, len(blocks), ndrop, []


# 逐卡人工判断的方向标签(序号→domain_scope),取值尽量对齐 db03 中文枚举。
# 12 篇 CV 视觉 / 余为统计/优化/通用ML/DL/NLP/生物医学。非 CV 卡取卡时不套用竞赛-SOTA 式背书。
DOMAIN_MAP = {
    "01": "cv-视觉", "02": "cv-视觉", "03": "cv-视觉", "04": "cv-视觉",
    "05": "cv-视觉", "06": "cv-视觉", "07": "cv-视觉", "11": "cv-视觉",
    "08": "统计经济金融", "09": "通用ML统计", "10": "优化",
    "12": "生物医学", "13": "通用深度学习", "14": "通用深度学习",
    "15": "NLP语音", "16": "通用ML统计",
}
DOMAIN_TAG_RE = re.compile(r"domain_scope=")


def tag_text(text, domain_map, card_re=r"^##\s+(\d+)\s+·", anchor="**OpenAlex**", pad=True):
    """在每卡含 anchor 的行尾追加 ` · domain_scope=xxx`(幂等)。

    card_re: 卡标题正则,group(1) 为卡号;anchor: 该卡内用于挂标签的行的子串。
    pad: 卡号是否补零到 2 位(samples_real 用 01;samples_recent 用 R01 不补)。
    返回(新文本,新增数,未匹配卡号)。
    """
    lines = text.splitlines(keepends=False)
    cur = None
    added = 0
    seen = set()           # 本次成功追加标签的卡号
    anchored = set()        # 找到 anchor 行的卡号(无论是否已带标签)
    cre = re.compile(card_re)
    for i, ln in enumerate(lines):
        m = cre.match(ln)
        if m:
            cur = m.group(1).zfill(2) if pad else m.group(1)
            continue
        if cur and anchor in ln:
            anchored.add(cur)
            if DOMAIN_TAG_RE.search(ln) is None:
                scope = domain_map.get(cur)
                if scope:
                    lines[i] = ln.rstrip() + f" · domain_scope={scope}"
                    added += 1
                    seen.add(cur)
    new = "\n".join(lines)
    if text.endswith("\n"):
        new += "\n"
    # 真正缺失 = map 里有、但全文找不到 anchor 行的卡号(非"已标过"的)
    missing = sorted(set(domain_map) - anchored)
    return new, added, missing


# samples_recent 8 卡(R01-R08)方向映射 + 挂标签锚点(venue 行含「快照」)。
RECENT_DOMAIN_MAP = {
    "R01": "cv-视觉", "R02": "cv-视觉", "R03": "cv-视觉", "R04": "cv-视觉",
    "R05": "cv-视觉", "R06": "生物医学", "R07": "cv-农业", "R08": "NLP语音",
}



def run(target: Path, dry_run: bool, mode: str):
    text = target.read_text(encoding="utf-8")
    if mode == "tag":
        if target.name.startswith("samples_recent"):
            new, added, missing = tag_text(
                text, RECENT_DOMAIN_MAP,
                card_re=r"^##\s+(R\d+)\s+·", anchor="**venue**", pad=False)
        else:
            new, added, missing = tag_text(text, DOMAIN_MAP)
        if missing:
            print(f"[迁移] 注意:这些卡号未在文中匹配到 OpenAlex 行: {missing}")
        if added == 0:
            print(f"[迁移] {target.name}: 无新 domain_scope 可加(已全标或无匹配)。幂等 0 变更。")
            return 0
        print(f"[迁移] {target.name}: 追加 {added} 处 domain_scope 标签。")
        if dry_run:
            print("[dry-run] 未写盘。")
            return 0
        target.write_text(new, encoding="utf-8")
        print(f"[迁移] 已写盘:{target}")
        return 0
    # 默认 mode == "del":删摘要原文段
    new, nblk, nrow, bad = migrate_text(text)
    if bad:
        print("[迁移] 中止:被删区出现结构拆解标记,可能边界识别错误:")
        for lineno, g, content in bad[:5]:
            print(f"  L{lineno} 含「{g}」: {content[:60]}")
        return 2
    if nblk == 0:
        print(f"[迁移] {target.name}: 无摘要原文段可删(已是干净态或无卡片)。幂等 0 变更。")
        return 0
    print(f"[迁移] {target.name}: 删除 {nblk} 段摘要原文,共 {nrow} 行。")
    if dry_run:
        print("[dry-run] 未写盘。")
        return 0
    target.write_text(new, encoding="utf-8")
    print(f"[迁移] 已写盘:{target}")
    return 0


def selftest():
    sample = """# 标题
说明段(摘要原文 不该删,因在卡片前)。

## 01 · Foo

- **作者**：A; B
- **被引数**：100（2026-06-06 快照）

**摘要原文（倒排还原）**
> This is the original abstract that must be removed for copyright.
> Second line of abstract.

**结构拆解**
- `title_pattern`：`X for Y`。
- 可迁移套路：保留。

## 02 · Bar

**摘要原文（倒排还原，已省略上标引文编号）**
> Another abstract block.

**结构拆解**
- 分析保留。
"""
    new, nblk, nrow, bad = migrate_text(sample)
    assert not bad, f"误判违规: {bad}"
    assert nblk == 2, f"应删2段,实得{nblk}"
    assert "original abstract" not in new, "card01 摘要未删"
    assert "Another abstract block" not in new, "card02 摘要未删"
    assert "title_pattern" in new, "误删了结构拆解"
    assert "可迁移套路：保留" in new, "误删了套路行"
    assert "说明段(摘要原文 不该删" in new, "误删了卡片前说明段"
    assert new.count("**结构拆解**") == 2, "结构拆解标记应保留2个"
    # 幂等:再跑一次应 0 段
    new2, nblk2, _, _ = migrate_text(new)
    assert nblk2 == 0, f"幂等失败,二次仍删{nblk2}段"
    assert new2 == new, "幂等失败,二次文本变化"
    print("[selftest] PASS migrate_db02(摘要段删除 + 卡前说明保护 + 结构拆解保护 + 幂等)")
    # --- tag 模式自检 ---
    tag_sample = """## 01 · Foo
- **DOI**：10.x · **OpenAlex**：W1
## 02 · Bar
- **DOI**：10.y · **OpenAlex**：W2 · domain_scope=已有
"""
    tnew, tadd, tmiss = tag_text(tag_sample, {"01": "cv-视觉", "02": "统计经济金融"})
    assert tadd == 1, f"应只给 card01 加标签(card02 已有),实加{tadd}"
    assert "W1 · domain_scope=cv-视觉" in tnew, "card01 标签未追加"
    assert tnew.count("domain_scope=") == 2, "标签总数应为2(1新+1原有)"
    # 幂等
    tnew2, tadd2, _ = tag_text(tnew, {"01": "cv-视觉", "02": "统计经济金融"})
    assert tadd2 == 0, f"tag 幂等失败,二次加{tadd2}"
    print("[selftest] PASS tag 模式(按卡号追加 domain_scope + 跳过已有 + 幂等)")
    return 0


def main():
    ap = argparse.ArgumentParser(description="db02 机械迁移(删摘要原文段 / 打 domain_scope 标签)")
    ap.add_argument("--dry-run", action="store_true", help="只报变更不写盘")
    ap.add_argument("--selftest", action="store_true", help="离线自检")
    ap.add_argument("--tag", action="store_true", help="打 domain_scope 标签模式(默认为删摘要段)")
    ap.add_argument("--target", default=str(HERE / "samples_real.md"), help="目标文件")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    return run(Path(args.target), args.dry_run, mode="tag" if args.tag else "del")


if __name__ == "__main__":
    sys.exit(main())
