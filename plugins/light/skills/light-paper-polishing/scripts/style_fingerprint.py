#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""style_fingerprint.py — 从用户过往文稿提取文风指纹，供润色时校准。

通用润色容易把每个人的文字都改成同一种"标准学术腔"。文风校准的目的相反：
先从用户**已发表/已认可**的文稿里量出 ta 的个人文风指纹，润色时往这个
指纹靠，保留作者声音，而不是抹平成模板。

提取的是**可量化、风格中性**的特征（不评判好坏，只刻画习惯）：
  - 句长：均值 / 中位数 / 分布（长短句节奏）
  - 段长：每段平均句数
  - 被动语态比例（英文）
  - 第一人称使用（we/I/our vs 全程无人称）
  - 连接词偏好（however/moreover/thus… 各自频次）
  - 标点习惯（分号、破折号、括号的使用密度）
  - 高频实义词（去停用词后，作者偏爱的表达）

对比模式：把一段**待润色稿**的指纹和**参考指纹**并排，标出偏离最大的维度，
提示润色该往哪调（如"你过往中位句长 22 词，这段 38 词，偏离你的习惯→建议断句"）。

诚实原则：指纹只是统计画像，不是文风的全部；它能提示"这段不像你平时的写法"，
但"改成什么样更好"仍是作者与审稿人的判断。脚本不自动改写。

用法：
  # 建指纹（喂一个或多个过往文稿，纯文本）
  python style_fingerprint.py --build past1.txt past2.txt --out my_style.json
  # 对比：待润色稿 vs 参考指纹
  python style_fingerprint.py --compare draft.txt --ref my_style.json
  python style_fingerprint.py --selftest
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from statistics import mean, median

STOPWORDS = set("the a an and or but of to in on for with as by is are was were be "
                "this that these those it its we our i you they he she them his her "
                "from at which who whose whom not no can will would should could may "
                "have has had do does did been being than then so such".split())

CONNECTORS = ["however", "moreover", "furthermore", "thus", "therefore", "hence",
              "nevertheless", "nonetheless", "consequently", "additionally",
              "meanwhile", "whereas", "although", "though", "yet", "besides"]

PASSIVE = re.compile(r"\b(is|are|was|were|be|been|being)\s+\w+(ed|en)\b", re.I)
FIRST_PERSON = re.compile(r"\b(we|our|us|i|my|ours)\b", re.I)


def split_sentences(text: str):
    parts = re.split(r"(?<=[.!?。！？])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str):
    return re.findall(r"[A-Za-z一-鿿]+", text.lower())


def fingerprint(text: str) -> dict:
    sents = split_sentences(text)
    paras = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    sent_lens = [len(words(s)) for s in sents] or [0]
    toks = words(text)
    n_tok = len(toks) or 1
    conn = {c: len(re.findall(rf"\b{c}\b", text, re.I)) for c in CONNECTORS}
    conn = {k: v for k, v in conn.items() if v > 0}
    content = [w for w in toks if w not in STOPWORDS and len(w) > 2]
    freq: dict = {}
    for w in content:
        freq[w] = freq.get(w, 0) + 1
    top = sorted(freq.items(), key=lambda x: -x[1])[:15]
    return {
        "n_sentences": len(sents),
        "sent_len_mean": round(mean(sent_lens), 1),
        "sent_len_median": round(median(sent_lens), 1),
        "sent_len_max": max(sent_lens),
        "sentences_per_para": round(len(sents) / max(len(paras), 1), 1),
        "passive_ratio": round(len(PASSIVE.findall(text)) / max(len(sents), 1), 3),
        "first_person_per_1k": round(len(FIRST_PERSON.findall(text)) / n_tok * 1000, 1),
        "semicolons_per_1k": round(text.count(";") / n_tok * 1000, 1),
        "dashes_per_1k": round((text.count("—") + text.count(" - ")) / n_tok * 1000, 1),
        "parens_per_1k": round(text.count("(") / n_tok * 1000, 1),
        "connectors": conn,
        "top_content_words": [w for w, _ in top],
    }


def merge_fingerprints(fps: list) -> dict:
    """多篇文稿合并为一个参考指纹（数值取均值，词表取并集高频）。"""
    if len(fps) == 1:
        return fps[0]
    num_keys = ["sent_len_mean", "sent_len_median", "sentences_per_para",
                "passive_ratio", "first_person_per_1k", "semicolons_per_1k",
                "dashes_per_1k", "parens_per_1k"]
    merged = {k: round(mean(f[k] for f in fps), 2) for k in num_keys}
    merged["sent_len_max"] = max(f["sent_len_max"] for f in fps)
    merged["n_sentences"] = sum(f["n_sentences"] for f in fps)
    allconn: dict = {}
    for f in fps:
        for k, v in f["connectors"].items():
            allconn[k] = allconn.get(k, 0) + v
    merged["connectors"] = allconn
    allwords: dict = {}
    for f in fps:
        for w in f["top_content_words"]:
            allwords[w] = allwords.get(w, 0) + 1
    merged["top_content_words"] = sorted(allwords, key=lambda w: -allwords[w])[:15]
    return merged


def compare(draft_fp: dict, ref: dict) -> list:
    """标出待润色稿偏离参考指纹最大的维度，给校准提示。"""
    notes = []
    sl, rl = draft_fp["sent_len_median"], ref.get("sent_len_median", sl_default := 0)
    if rl and abs(sl - rl) >= 6:
        d = "偏长，建议断句" if sl > rl else "偏短，可适当合并"
        notes.append(f"中位句长 {sl}（你的习惯 {rl}）→ {d}")
    pr, rpr = draft_fp["passive_ratio"], ref.get("passive_ratio", 0)
    if abs(pr - rpr) >= 0.15:
        d = "被动偏多" if pr > rpr else "被动偏少"
        notes.append(f"被动比例 {pr}（你的习惯 {rpr}）→ {d}")
    fp1, rfp1 = draft_fp["first_person_per_1k"], ref.get("first_person_per_1k", 0)
    if abs(fp1 - rfp1) >= 5:
        d = "第一人称偏多" if fp1 > rfp1 else "第一人称偏少（你平时更常用 we/our）"
        notes.append(f"第一人称频次 {fp1}/千词（你的习惯 {rfp1}）→ {d}")
    draft_conn = set(draft_fp["connectors"])
    ref_conn = set(ref.get("connectors", {}))
    alien = draft_conn - ref_conn
    if alien:
        notes.append(f"出现你过往很少用的连接词：{sorted(alien)}（可换成你惯用的：{sorted(ref_conn)[:5]}）")
    if not notes:
        notes.append("这段文风与你过往指纹基本一致，无明显偏离。")
    return notes


def selftest() -> int:
    past = ("We propose a method. We evaluate it on three datasets. "
            "Our results show clear gains. We discuss limitations openly.\n\n"
            "The approach is simple. It works well. We release the code.")
    draft = ("It is worth noting that the proposed methodology, which was "
             "comprehensively evaluated across a multitude of diverse experimental "
             "settings and configurations, was subsequently demonstrated to be "
             "effective; moreover, the results were analyzed thoroughly.")
    fp_past = fingerprint(past)
    fp_draft = fingerprint(draft)
    print("[过往指纹] 中位句长=%s 被动比=%s 第一人称/千词=%s" % (
        fp_past["sent_len_median"], fp_past["passive_ratio"], fp_past["first_person_per_1k"]))
    print("[待润色稿] 中位句长=%s 被动比=%s" % (
        fp_draft["sent_len_median"], fp_draft["passive_ratio"]))
    print("[校准提示]")
    for n in compare(fp_draft, fp_past):
        print("  -", n)
    # 校验：长难句草稿应至少被提示句长偏离
    ok = any("句长" in n for n in compare(fp_draft, fp_past))
    print("[selftest]", "OK" if ok else "FAIL")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="文风指纹提取与校准")
    ap.add_argument("--build", nargs="+", help="过往文稿文件，建参考指纹")
    ap.add_argument("--compare", help="待润色稿文件")
    ap.add_argument("--ref", help="参考指纹 JSON")
    ap.add_argument("--out", help="指纹输出路径")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    if args.build:
        fps = []
        for path in args.build:
            with open(path, encoding="utf-8") as f:
                fps.append(fingerprint(f.read()))
        ref = merge_fingerprints(fps)
        out = json.dumps(ref, ensure_ascii=False, indent=2)
        if args.out:
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(out)
        print(out)
        return 0

    if args.compare and args.ref:
        with open(args.compare, encoding="utf-8") as f:
            draft_fp = fingerprint(f.read())
        with open(args.ref, encoding="utf-8") as f:
            ref = json.load(f)
        for n in compare(draft_fp, ref):
            print("  -", n)
        return 0

    ap.error("需要 --build，或 --compare+--ref，或 --selftest")
    return 2


if __name__ == "__main__":
    sys.exit(main())
