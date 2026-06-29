#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""polish.py — LanguageTool-backed grammar/style polish for academic text.

Pipeline:
  1. Read text (--text / --file / stdin).
  2. Chunk on sentence/paragraph boundaries so each chunk stays under the
     anonymous LanguageTool size cap (default 18000 chars, cap is ~20000).
  3. POST each chunk to https://api.languagetool.org/v2/check (level=picky).
  4. Map every match back to an absolute line/column in the ORIGINAL text and
     emit structured findings {line, col, rule, issue, suggestion, context}.
  5. If the endpoint is unreachable / non-200, degrade gracefully to a small
     set of local regex rules so the script still produces findings offline.

Honesty: the endpoint is curl-tested in SKILL.md / references.md (HTTP 200,
2026-06-06). This script reuses that exact endpoint and records the HTTP code
it actually receives at runtime in the JSON output under "_meta".

Usage:
  python polish.py --text "This sentence have a error."
  python polish.py --file paper.txt --language en-US --level picky
  echo "..." | python polish.py --json
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
import argparse
import json
import re
import time
import urllib.parse
import urllib.request
import urllib.error

LT_ENDPOINT = "https://api.languagetool.org/v2/check"
MAX_CHUNK = 18000          # stay safely under anonymous ~20k char cap
TIMEOUT = 30
# 匿名端点限流 ~20 req/min + 75KB/min；chunk 间隔 sleep 控速，429 指数退避重试。
CHUNK_SLEEP = 3.2          # 秒：~20 req/min 的安全间隔
MAX_RETRY = 3              # 429/5xx 重试次数


def split_chunks(text, max_chunk=MAX_CHUNK):
    """Split text into <=max_chunk pieces on paragraph/sentence boundaries.

    Returns list of (offset_in_original, chunk_text) so matches can be mapped
    back to absolute positions.
    """
    if len(text) <= max_chunk:
        return [(0, text)]
    chunks = []
    # prefer paragraph boundaries, fall back to sentence, then hard cut
    pieces = re.split(r"(\n\s*\n)", text)
    buf, buf_start, cursor = "", 0, 0
    for piece in pieces:
        if len(buf) + len(piece) > max_chunk and buf:
            chunks.append((buf_start, buf))
            buf, buf_start = "", cursor
        buf += piece
        cursor += len(piece)
    if buf:
        chunks.append((buf_start, buf))
    # any chunk still too big -> hard split
    final = []
    for off, ch in chunks:
        while len(ch) > max_chunk:
            final.append((off, ch[:max_chunk]))
            ch = ch[max_chunk:]
            off += max_chunk
        if ch:
            final.append((off, ch))
    return final


def offset_to_linecol(text, offset):
    prefix = text[:offset]
    line = prefix.count("\n") + 1
    col = offset - (prefix.rfind("\n") + 1) + 1
    return line, col


def check_chunk(chunk, language, level, mother_tongue, _sleep=time.sleep):
    """POST one chunk to LanguageTool with 429/5xx 指数退避重试。返回 (http_code, matches_list)。"""
    data = {"text": chunk, "language": language, "level": level}
    if mother_tongue:
        data["motherTongue"] = mother_tongue
    body = urllib.parse.urlencode(data).encode("utf-8")
    last_code = None
    for attempt in range(MAX_RETRY):
        req = urllib.request.Request(
            LT_ENDPOINT, data=body,
            headers={"Content-Type": "application/x-www-form-urlencoded",
                     "Accept": "application/json",
                     "User-Agent": "light-paper-polishing/1.0"},
        )
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return resp.getcode(), json.loads(resp.read().decode("utf-8")).get("matches", [])
        except urllib.error.HTTPError as e:
            last_code = e.code
            if e.code in (429, 500, 502, 503) and attempt < MAX_RETRY - 1:
                _sleep(2 ** attempt * 2)   # 指数退避 2s,4s,8s
                continue
            return e.code, None
        except Exception:  # network down, DNS, timeout, SSL...
            return None, None
    return last_code, None


# ---- offline fallback rules (no network) ----
LOCAL_RULES = [
    (r"\b(\w+)\s+\1\b", "DUP_WORD", "Repeated word.", None),
    (r"\bthis\s+(results|datas|analyses)\b", "AGREEMENT", "Possible number disagreement.", None),
    (r"\ba\s+([aeiouAEIOU]\w+)", "A_VS_AN", "Use 'an' before a vowel sound.", "an \\1"),
    (r"\s+([,.;:])", "SPACE_BEFORE_PUNCT", "No space before punctuation.", "\\1"),
    (r"\b(dont|cant|wont|isnt|arent|doesnt)\b", "MISSING_APOSTROPHE", "Missing apostrophe.", None),
    (r"  +", "DOUBLE_SPACE", "Multiple consecutive spaces.", " "),
]


def local_check(text):
    findings = []
    for pat, rid, msg, repl in LOCAL_RULES:
        for m in re.finditer(pat, text):
            line, col = offset_to_linecol(text, m.start())
            suggestion = None
            if repl is not None:
                try:
                    suggestion = re.sub(pat, repl, m.group(0))
                except re.error:
                    suggestion = None
            findings.append({
                "line": line, "col": col, "rule": rid,
                "issue": msg, "suggestion": suggestion,
                "context": text[max(0, m.start() - 25):m.end() + 25].replace("\n", " "),
                "source": "local",
            })
    return findings


def run(text, language, level, mother_tongue, _sleep=time.sleep, max_chunk=MAX_CHUNK):
    chunks = split_chunks(text, max_chunk=max_chunk)
    findings = []
    http_codes = []
    n_online, n_fallback = 0, 0
    for i, (off, chunk) in enumerate(chunks):
        if i > 0:
            _sleep(CHUNK_SLEEP)   # 控速，避开 ~20 req/min 限流
        code, matches = check_chunk(chunk, language, level, mother_tongue, _sleep=_sleep)
        http_codes.append(code)
        if code == 200 and matches is not None:
            n_online += 1
            for m in matches:
                abs_off = off + m["offset"]
                line, col = offset_to_linecol(text, abs_off)
                reps = [r["value"] for r in m.get("replacements", [])][:3]
                findings.append({
                    "line": line, "col": col,
                    "rule": m.get("rule", {}).get("id", ""),
                    "issue": m.get("message", ""),
                    "suggestion": "; ".join(reps) if reps else None,
                    "context": m.get("context", {}).get("text", ""),
                    "source": "languagetool",
                })
        else:
            # 仅该 chunk 降级本地规则（其余 chunk 的 LanguageTool 结果保留，不全篇丢弃）
            n_fallback += 1
            for f in local_check(chunk):
                f["line"], f["col"] = offset_to_linecol(text, off + _chunk_local_off(chunk, f))
                findings.append(f)
    findings.sort(key=lambda f: (f["line"], f["col"]))
    if n_online and n_fallback:
        mode = "mixed(部分chunk降级本地)"
    elif n_online:
        mode = "languagetool"
    else:
        mode = "local-fallback"
    return {
        "_meta": {
            "endpoint": LT_ENDPOINT,
            "http_codes": http_codes,
            "mode": mode,
            "n_chunks": len(chunks),
            "n_chunks_online": n_online,
            "n_chunks_fallback": n_fallback,
            "n_findings": len(findings),
        },
        "findings": findings,
    }


def _chunk_local_off(chunk, finding):
    """local_check 的 finding 已带 chunk 内 line/col，但我们需要它的 chunk 内绝对 offset 来重映射。
    重新按 context 在 chunk 里定位（local_check 的 context 是命中点±25 字符，足够定位）。"""
    # local_check 内部已算好 chunk 内 line/col；这里把它转回 chunk 内 offset
    lines = chunk.splitlines(keepends=True)
    li = finding["line"] - 1
    off = sum(len(l) for l in lines[:li]) + (finding["col"] - 1)
    return off



def _selftest() -> int:
    sample = "This sentence have a error.  The approach was used used and dont fail ."
    findings = local_check(sample)
    rules = {f["rule"] for f in findings}
    assert "DUP_WORD" in rules, rules
    assert "DOUBLE_SPACE" in rules or "SPACE_BEFORE_PUNCT" in rules, rules
    chunks = split_chunks(sample, max_chunk=12)
    assert len(chunks) > 1, chunks
    line, col = offset_to_linecol("a\nbc", 3)
    assert (line, col) == (2, 2), (line, col)

    # PP-4 每 chunk 独立降级：mock check_chunk —— chunk0 返回 200、其余 429 → 仅该 chunk 降级
    big = ("Para zero is clean.\n\n" + "x" * 30 + "\n\n"
           "Para two has used used dup and dont apostrophe.")
    calls = {"i": 0}

    def fake_check(chunk, lang, lvl, mt, _sleep=None):
        calls["i"] += 1
        return (200, []) if calls["i"] == 1 else (429, None)
    g = globals()
    orig = g["check_chunk"]
    try:
        g["check_chunk"] = fake_check
        res = run(big, "en-US", "picky", "zh-CN", _sleep=lambda s: None, max_chunk=25)
    finally:
        g["check_chunk"] = orig
    meta = res["_meta"]
    assert meta["n_chunks_online"] >= 1 and meta["n_chunks_fallback"] >= 1, meta
    assert meta["mode"].startswith("mixed"), meta
    assert res["findings"], "降级 chunk 的本地 findings 应保留"

    # check_chunk 429 退避重试：mock 一直 429，应重试 MAX_RETRY 次后返回 429
    retry = {"n": 0}

    def always_429(req, timeout=None):
        retry["n"] += 1
        raise urllib.error.HTTPError(LT_ENDPOINT, 429, "rate", {}, None)
    orig_open = urllib.request.urlopen
    try:
        urllib.request.urlopen = always_429
        code, m = check_chunk("x", "en-US", "picky", "zh-CN", _sleep=lambda s: None)
    finally:
        urllib.request.urlopen = orig_open
    assert code == 429 and m is None and retry["n"] == MAX_RETRY, (code, retry["n"])

    print(f"[selftest] PASS polish local={len(findings)} chunks={len(chunks)} +per-chunk-fallback+retry")
    return 0


def main():
    ap = argparse.ArgumentParser(description="LanguageTool-backed academic polish.")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--text")
    g.add_argument("--file")
    ap.add_argument("--language", default="en-US")
    ap.add_argument("--level", default="picky", choices=["default", "picky"])
    ap.add_argument("--mother-tongue", default="zh-CN")
    ap.add_argument("--json", action="store_true", help="emit raw JSON")
    ap.add_argument("--selftest", action="store_true", help="run offline local-rule self-test")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(_selftest())

    if args.text is not None:
        text = args.text
    elif args.file:
        with open(args.file, encoding="utf-8") as f:
            text = f.read()
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        # self-test when no input (so the script always runs)
        text = ("This sentence have a error.  In conclusion, the results "
                "is significant and a unique approach was used used.")
        print("[self-test: no input given, using built-in sample]\n", file=sys.stderr)

    result = run(text, args.language, args.level, args.mother_tongue)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    meta = result["_meta"]
    print(f"mode={meta['mode']}  http={meta['http_codes']}  "
          f"chunks={meta['n_chunks']}  findings={meta['n_findings']}")
    for f in result["findings"]:
        sug = f["suggestion"] or "—"
        print(f"  L{f['line']}:C{f['col']} [{f['rule']}] {f['issue']}")
        print(f"      → {sug}   ({f['source']})")


if __name__ == "__main__":
    main()
