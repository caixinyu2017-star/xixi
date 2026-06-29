#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rebuttal_budget.py — 会议 rebuttal 字数/页数预算检查（纯标准库，离线）。

会议 rebuttal 常有硬性 1 页或字数上限（ICLR/NeurIPS 等），超限直接被截断或拒收。
本脚本对 response letter / rebuttal 文本做预算核对：词数、字符数、估算页数，
对照所选会议预设上限给 PASS/WARN/FAIL。中英混排分别计词（英文按空白切，中文按字符）。

用法:
    python rebuttal_budget.py rebuttal.md --venue iclr
    python rebuttal_budget.py rebuttal.md --max-words 1000
    cat rebuttal.md | python rebuttal_budget.py --venue neurips
    python rebuttal_budget.py --selftest        # 离线自检，不读外部文件

预设上限仅为常见档位的工程近似，**以目标会议当年征稿/返修说明为准**（量纲逐年变）。
"""
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

import argparse  # noqa: E402
import re  # noqa: E402
import unicodedata  # noqa: E402

# 常见会议 rebuttal 预算近似。这些会多按**字符/页数**限(非词数)，故主用 max_chars；
# 数值为工程近似(注明依据)，**必须以目标会议当年征稿/OpenReview 框为准**(逐年变)。
VENUE_LIMITS = {
    # ICLR/NeurIPS 用 OpenReview 评论框，常见单条回复字符上限近 ~5000（Markdown 框计字符）
    "iclr": {"max_words": 0, "max_chars": 5000,
             "note": "ICLR OpenReview 单条 review 回复常 ~5000 字符上限（按 Markdown 框计字符，非词数）；以当年为准"},
    "neurips": {"max_words": 0, "max_chars": 6000,
                "note": "NeurIPS 近年单条回复字符框 ~6000，或单页 PDF；以 OpenReview 当年框为准"},
    # CVPR 限 1 页 PDF（含图表），换算成纯文本词数上限近似 ~1000 词（留图表空间）
    "cvpr": {"max_words": 1000, "max_chars": 0,
             "note": "CVPR rebuttal 限 1 页 PDF（含图表），~1000 词是留图表空间的纯文本近似；以官方模板为准"},
    "generic-1page": {"max_words": 650, "max_chars": 0,
                      "note": "1 页 ~650 词工程近似（单栏 11pt）"},
    "generic-5000char": {"max_words": 0, "max_chars": 5000,
                         "note": "OpenReview 式 5000 字符框工程近似"},
}

# 1 页纯文本词数近似（单栏，去掉图表）。仅用于估页，不作硬判。
WORDS_PER_PAGE = 650


def count_words(text):
    """中英混排计词：英文/数字按空白切分的 token；中日韩表意字符逐字计。"""
    cjk = 0
    for ch in text:
        if _is_cjk(ch):
            cjk += 1
    # 去掉 CJK 后按空白切，得拉丁词数
    latin_text = "".join(" " if _is_cjk(ch) else ch for ch in text)
    latin = len([t for t in re.split(r"\s+", latin_text) if t.strip()])
    return latin + cjk, latin, cjk


def _is_cjk(ch):
    try:
        name = unicodedata.name(ch)
    except ValueError:
        return False
    return "CJK" in name or "HIRAGANA" in name or "KATAKANA" in name


def strip_markup(text):
    """粗去 markdown 噪声（代码块/行内码/链接 URL/标题井号），让计词更接近正文。"""
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"`[^`]*`", " ", text)
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)  # 链接保留锚文本
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.MULTILINE)
    return text


def assess(text, limits, strip=True):
    """limits: venue 限制 dict（含 max_words / max_chars / note），或直接传 {"max_words": N}。"""
    if isinstance(limits, int):   # 向后兼容：旧调用传 max_words 整数
        limits = {"max_words": limits}
    max_words = limits.get("max_words", 0)
    body = strip_markup(text) if strip else text
    total, latin, cjk = count_words(body)
    pages = total / WORDS_PER_PAGE
    result = {
        "words_total": total, "words_latin": latin, "words_cjk": cjk,
        "chars": len(body), "est_pages": round(pages, 2), "max_words": max_words,
        "max_chars": limits.get("max_chars", 0),
    }
    max_chars = limits.get("max_chars", 0)
    chars = result["chars"]
    # 优先按 venue 实际口径判定：有 max_chars 用字符、有 max_words 用词数（两者皆设时各判、取更严）
    verdicts = []
    if max_chars and max_chars > 0:
        if chars > max_chars:
            verdicts.append(("FAIL", f"超字符上限 {chars - max_chars}（{chars}/{max_chars} 字符）"))
        elif chars > max_chars * 0.9:
            verdicts.append(("WARN", f"逼近字符上限（{chars}/{max_chars}，余 {max_chars - chars}）"))
        else:
            verdicts.append(("PASS", f"在字符预算内（{chars}/{max_chars}）"))
    if max_words and max_words > 0:
        if total > max_words:
            verdicts.append(("FAIL", f"超限 {total - max_words} 词（{total}/{max_words}）"))
        elif total > max_words * 0.9:
            verdicts.append(("WARN", f"逼近上限（{total}/{max_words}，余 {max_words - total} 词）"))
        else:
            verdicts.append(("PASS", f"在预算内（{total}/{max_words}）"))
    if verdicts:
        # 取最严判定（FAIL>WARN>PASS）
        rank = {"FAIL": 2, "WARN": 1, "PASS": 0}
        verdicts.sort(key=lambda v: -rank[v[0]])
        result["verdict"] = verdicts[0][0]
        result["msg"] = "；".join(m for _, m in verdicts)
    else:
        result["verdict"] = "INFO"
        result["msg"] = (f"该 venue 未设词数/字符上限；估算 {result['est_pages']} 页"
                         f"（{total} 词 / {chars} 字符）——以目标会议当年征稿框为准")
    return result


def _render(r, venue_note=None):
    cap = ""
    if r.get("max_chars"):
        cap = f" / 上限 {r['max_chars']} 字符"
    elif r.get("max_words"):
        cap = f" / 上限 {r['max_words']} 词"
    lines = [
        f"[{r['verdict']}] {r['msg']}",
        f"  词数: {r['words_total']}（拉丁 {r['words_latin']} + CJK {r['words_cjk']}）",
        f"  字符: {r['chars']}{cap}    估算页数: {r['est_pages']}",
    ]
    if venue_note:
        lines.append(f"  注: {venue_note}")
    return "\n".join(lines)


def _selftest():
    # 1) 英文短文本在 generic-1page 预算内 -> PASS
    r = assess("This is a short rebuttal. " * 10, 650)
    assert r["verdict"] == "PASS", r
    # 2) 超长 -> FAIL
    r2 = assess("word " * 800, 650)
    assert r2["verdict"] == "FAIL", r2
    assert r2["words_total"] == 800, r2
    # 3) 逼近上限 -> WARN
    r3 = assess("word " * 600, 650)
    assert r3["verdict"] == "WARN", r3
    # 4) 中英混排计词：5 个中文字 + 2 英文词
    n, lat, cjk = count_words("方法学有效 good work")
    assert cjk == 5 and lat == 2, (n, lat, cjk)
    # 5) markdown 去噪：代码块与链接不灌水
    body = strip_markup("see [paper](http://x.com/very/long/url) ```code block ignored```")
    assert "http" not in body and "code block" not in body, body
    # 6) 无上限 -> INFO + 估页
    r6 = assess("word " * 1300, 0)
    assert r6["verdict"] == "INFO" and r6["est_pages"] == 2.0, r6

    # 7) RR-1 venue 预设填真值后真能判 PASS/FAIL（原来三会 max_words=0 永远 INFO，承诺形同虚设）
    # ICLR 用 max_chars=5000：短文本 PASS、超长 FAIL
    short = assess("Thanks for the review. We address each point below. " * 5, VENUE_LIMITS["iclr"])
    assert short["verdict"] == "PASS", short          # 不再永远 INFO
    longtext = assess("x" * 6000, VENUE_LIMITS["iclr"])
    assert longtext["verdict"] == "FAIL", longtext     # 超 5000 字符 → FAIL（承诺真生效）
    # CVPR 用 max_words=1000：超词 FAIL
    cvpr_over = assess("word " * 1200, VENUE_LIMITS["cvpr"])
    assert cvpr_over["verdict"] == "FAIL", cvpr_over
    # NeurIPS 字符框
    nips = assess("ok " * 100, VENUE_LIMITS["neurips"])
    assert nips["verdict"] in ("PASS", "WARN"), nips
    # 字符与词数双限时取更严
    both = assess("word " * 700, {"max_words": 650, "max_chars": 99999})
    assert both["verdict"] == "FAIL", both             # 词数超 → 取更严的 FAIL
    print("[selftest] PASS rebuttal_budget（计词/预算判定/中英混排/markdown去噪/估页/venue字符限）")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="会议 rebuttal 字数/页数预算检查")
    ap.add_argument("file", nargs="?", help="rebuttal 文本文件（缺省读 stdin）")
    ap.add_argument("--venue", choices=sorted(VENUE_LIMITS), help="按预设会议取上限")
    ap.add_argument("--max-words", type=int, default=None, help="自定义词数上限（覆盖 --venue）")
    ap.add_argument("--max-chars", type=int, default=None, help="自定义字符上限（OpenReview 框常用，覆盖 --venue）")
    ap.add_argument("--no-strip", action="store_true", help="不去 markdown 噪声，按原文计")
    ap.add_argument("--selftest", action="store_true", help="离线自检")
    args = ap.parse_args(argv)

    if args.selftest:
        return _selftest()

    note = None
    if args.venue:
        limits = dict(VENUE_LIMITS[args.venue])
        note = limits.get("note")
    else:
        limits = {"max_words": 0, "max_chars": 0}
    # 自定义上限覆盖 venue 预设
    if args.max_words is not None:
        limits["max_words"] = args.max_words
    if args.max_chars is not None:
        limits["max_chars"] = args.max_chars

    if args.file:
        with open(args.file, encoding="utf-8") as f:
            text = f.read()
    else:
        text = sys.stdin.read()
    if not text.strip():
        ap.error("输入为空（给文件或从 stdin 喂文本）")

    r = assess(text, limits, strip=not args.no_strip)
    print(_render(r, note))
    return 1 if r["verdict"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
