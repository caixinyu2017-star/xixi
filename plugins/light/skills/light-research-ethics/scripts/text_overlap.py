#!/usr/bin/env python3
"""Offline self-plagiarism / duplicate-text screen (light-research-ethics asset).

Compares ONE target file against a set of comparison files (your own older
papers, course reports, or one specific source text) entirely offline, using
only the Python standard library. Finds the longest verbatim contiguous run of
words shared between the two texts (difflib.SequenceMatcher), reports the
overall overlap ratio, and counts runs that exceed the red-flag threshold.

This maps the risk_checklist red flag "连续 >40 词逐字相同" to a runnable tool.

HONEST LIMITS: this only compares text YOU supply. It does NOT include
Turnitin's journal/web/student corpora. Use it for self-plagiarism and
duplicate-text screening only. Do NOT report its numbers as a "plagiarism rate"
or "similarity %". A clean result means "no overlap found within the supplied
corpus", NOT a guarantee that the text is original.

Usage:
    python text_overlap.py paper.txt old_paper.txt
    python text_overlap.py paper.txt "corpus/*.txt" --min-run 40 --exclude-refs
    python text_overlap.py paper.txt old.txt --json
    python text_overlap.py --selftest
"""
import sys
import os
import re
import glob
import json
import argparse
import difflib

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

# References / bibliography headings — content after these is dropped with
# --exclude-refs so the shared bibliography does not inflate overlap.
REF_HEADING = re.compile(
    r"^\s*(?:#+\s*|\d+[.\s]+)?"
    r"(references|bibliography|works cited|literature cited|"
    r"参考文献|引用文献|参考资料)\s*$",
    re.IGNORECASE,
)
WORD_RE = re.compile(r"\w+", re.UNICODE)


def strip_refs(text):
    """Drop everything from the first References/参考文献 heading onward."""
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        if REF_HEADING.match(ln):
            return "\n".join(lines[:i])
    return text


def tokenize(text):
    """Return (norm_words, originals, line_nos). Word-level, normalized:
    lowercase + punctuation dropped (\\w+) + whitespace collapsed implicitly."""
    norm, orig, lines = [], [], []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for m in WORD_RE.finditer(line):
            tok = m.group(0)
            norm.append(tok.lower())
            orig.append(tok)
            lines.append(lineno)
    return norm, orig, lines


def analyze(a_words, b_words, min_run):
    """Compare two normalized word lists. Return dict with longest run (as
    a/b index spans + length), count of runs >= min_run, and overlap ratios."""
    sm = difflib.SequenceMatcher(a=a_words, b=b_words, autojunk=False)
    blocks = [bl for bl in sm.get_matching_blocks() if bl.size > 0]
    longest = max(blocks, key=lambda bl: bl.size, default=None)
    flagged = [bl for bl in blocks if bl.size >= min_run]
    matched_a = sum(bl.size for bl in blocks)
    word_overlap = matched_a / len(a_words) if a_words else 0.0
    sa, sb = set(a_words), set(b_words)
    union = len(sa | sb)
    jaccard = len(sa & sb) / union if union else 0.0
    return {"blocks": blocks, "longest": longest, "flagged": flagged,
            "word_overlap": word_overlap, "jaccard": jaccard,
            "matched_words": matched_a}


def load_words(path, exclude_refs):
    text = open(path, encoding="utf-8", errors="replace").read()
    if exclude_refs:
        text = strip_refs(text)
    return tokenize(text)


def compare_file(target, t_norm, t_orig, t_lines, other, min_run, exclude_refs):
    """Compare target (pre-tokenized) against one comparison file."""
    o_norm, o_orig, o_lines = load_words(other, exclude_refs)
    res = analyze(t_norm, o_norm, min_run)
    lg = res["longest"]
    rec = {"file": other, "word_overlap": res["word_overlap"],
           "jaccard": res["jaccard"], "flagged_runs": len(res["flagged"]),
           "longest_run_words": lg.size if lg else 0}
    if lg and lg.size > 0:
        snippet = " ".join(t_orig[lg.a:lg.a + lg.size])
        rec["longest_snippet"] = snippet
        rec["target_line"] = t_lines[lg.a]
        rec["compare_line"] = o_lines[lg.b]
    rec["over_threshold"] = bool(lg and lg.size >= min_run)
    return rec


def expand_inputs(patterns):
    out = []
    for p in patterns:
        hits = glob.glob(p)
        out.extend(hits if hits else [p])
    return list(dict.fromkeys(out))  # dedup, keep order


def run(args):
    if not os.path.isfile(args.target):
        sys.stderr.write("error: target not found: %s\n" % args.target)
        return 2
    t_norm, t_orig, t_lines = load_words(args.target, args.exclude_refs)
    others = [f for f in expand_inputs(args.compare)
              if os.path.isfile(f) and os.path.abspath(f) != os.path.abspath(args.target)]
    if not others:
        sys.stderr.write("error: no comparison files resolved\n")
        return 2
    records = [compare_file(args.target, t_norm, t_orig, t_lines, o,
                            args.min_run, args.exclude_refs) for o in others]
    records.sort(key=lambda r: r["longest_run_words"], reverse=True)
    if args.json:
        print(json.dumps({"target": args.target, "min_run": args.min_run,
                           "results": records}, ensure_ascii=False, indent=2))
    else:
        _print_markdown(args, records)
    return 0


def _print_markdown(args, records):
    print("# 离线自查重 — target: %s\n" % args.target)
    print("> 阈值 min-run=%d 词；exclude-refs=%s。" % (args.min_run, args.exclude_refs))
    print("| 对比文件 | 最长逐字重合(词) | 超阈片段数 | 词重合率 | Jaccard |")
    print("|---|---|---|---|---|")
    for r in records:
        mark = "🛑" if r["over_threshold"] else ("⚠️" if r["longest_run_words"] else "✅")
        print("| %s | %s %d | %d | %.1f%% | %.1f%% |" % (
            os.path.basename(r["file"]), mark, r["longest_run_words"],
            r["flagged_runs"], r["word_overlap"] * 100, r["jaccard"] * 100))
    flagged = [r for r in records if r["over_threshold"]]
    if flagged:
        print("\n## 🛑 超红旗阈值片段（连续 >=%d 词逐字相同）" % args.min_run)
        for r in flagged:
            print("\n- **%s** ↔ target L%d / 对比 L%d，%d 词：" % (
                os.path.basename(r["file"]), r["target_line"],
                r["compare_line"], r["longest_run_words"]))
            snip = r["longest_snippet"]
            print("  > %s" % (snip[:300] + (" …" if len(snip) > 300 else "")))
    print("\n**%d 个对比文件命中红旗阈值。**" % len(flagged))
    print("\n> 诚实限制：仅比对所给语料，不含 Turnitin 的期刊/网页/学生库。"
          "结果只用于自我抄袭与重复文本筛查，不得对外宣称\"抄袭率/相似度%\"。"
          "清结果仅代表\"在所给语料内未见重合\"，不保证无抄袭。")


def _selftest():
    target = ("Climate change is driven by greenhouse gas emissions from human "
              "activity and this long verbatim passage repeats word for word in "
              "both documents to trigger the red flag threshold during testing. "
              "\n\nReferences\n"
              "Smith J. 2020. A unique bibliography entry only in the target file.")
    other = ("In an unrelated opening sentence we discuss something else. "
             "Climate change is driven by greenhouse gas emissions from human "
             "activity and this long verbatim passage repeats word for word in "
             "both documents to trigger the red flag threshold during testing. "
             "\n\nReferences\n"
             "Jones P. 1999. A totally different bibliography entry here.")
    min_run = 20
    # exclude-refs ON: bibliographies differ, so they must not be matched.
    t = tokenize(strip_refs(target))
    o = tokenize(strip_refs(other))
    res = analyze(t[0], o[0], min_run)
    lg = res["longest"]
    assert lg and lg.size >= min_run, "should locate run >= min_run"
    snippet = " ".join(t[1][lg.a:lg.a + lg.size]).lower()
    assert "climate change" in snippet, "longest run should be the shared passage"
    assert "bibliography" not in snippet, "refs must be excluded from match"
    assert all("smith" not in w and "jones" not in w for w in t[0]), \
        "strip_refs should drop bibliography content"
    # exclude-refs OFF baseline: full text still tokenizes the refs.
    full = tokenize(target)
    assert any(w == "smith" for w in full[0]), "without strip_refs refs remain"
    print("[selftest] longest run = %d words: \"%s…\"" % (lg.size, snippet[:50]))
    print("[selftest] word_overlap=%.1f%% jaccard=%.1f%%"
          % (res["word_overlap"] * 100, res["jaccard"] * 100))
    print("[selftest] exclude-refs drops bibliography PASS")
    print("[selftest] all assertions PASS")
    return 0


def main():
    ap = argparse.ArgumentParser(
        description="Offline self-plagiarism / duplicate-text screen (stdlib only)")
    ap.add_argument("target", nargs="?", help="target file to check")
    ap.add_argument("compare", nargs="*", help="comparison files or globs")
    ap.add_argument("--min-run", type=int, default=40,
                    help="red-flag threshold in words (default 40, per risk_checklist)")
    ap.add_argument("--exclude-refs", action="store_true",
                    help="drop content after References/参考文献 heading")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of markdown")
    ap.add_argument("--selftest", action="store_true", help="offline self-test")
    args = ap.parse_args()
    if args.selftest:
        return _selftest()
    if not args.target or not args.compare:
        ap.error("provide a target file and at least one comparison file/glob (or --selftest)")
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
