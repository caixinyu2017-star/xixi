#!/usr/bin/env python3
"""draft_lint.py — 论文草稿诚信门机检器（人判优先，机检兜底）。

检查项：
  1. 残留缺口标记：[MATERIAL GAP] / [RESULT GAP] / TODO（终稿门必须为 0）。
  2. 必备声明小节缺失：按**行首 markdown 标题**校验 Data Availability / Ethics / CRediT /
     Conflicts / Funding / AI Use（不再用全文子串，避免正文散句误判为"已有该 section"）。
  3. 高危结果句无显著性：SOTA/outperform/最优 等措辞与 p值/CI/±std 在**同句或相邻句窗口**
     共现才算通过（不再要求严格同行，治长段落/相邻句的误报）。
  4. 引用台账：抽取 DOI/arXiv（跳过 ``` 代码围栏与引用块，避免示例代码里的内容假阳），
     输出待 curl 核查清单。
  5. --claims：抽取候选事实句（含数字/比较/SOTA 措辞），播种 claim 台账（templates/claim_passport.md）。

用法：
  python draft_lint.py <draft.md> [--final] [--json] [--claims]
  python draft_lint.py --selftest

退出码：0 通过；1 发现需返工项；2 用法错误。
"""
import json
import re
import sys

GAP_PAT = re.compile(r"\[(?:MATERIAL GAP|RESULT GAP)\b[^\]]*\]|(?<![\w/])TODO\b")
DOI_PAT = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+")
ARXIV_PAT = re.compile(r"arXiv:\d{4}\.\d{4,5}", re.IGNORECASE)
HYPE_PAT = re.compile(r"\b(?:state[- ]of[- ]the[- ]art|SOTA|outperform\w*|best[- ]ever|超越|最优|优于)\b", re.IGNORECASE)
SIG_PAT = re.compile(r"p\s*[<=>]\s*0?\.\d+|95%\s*CI|±\s*\d|std", re.IGNORECASE)
# 候选事实句：含数字+百分号/指标提升/比较措辞 → 可能是需登记 claim 的事实陈述
CLAIM_HINT_PAT = re.compile(
    r"\d+(?:\.\d+)?\s*%|\bby\s+\d|提升|提高|降低|达到|improv\w*|reduc\w*|achiev\w*|"
    r"state[- ]of[- ]the[- ]art|SOTA|outperform\w*|优于|超越", re.IGNORECASE)

REQUIRED_SECTIONS = {
    "Data Availability": r"data\s+availability|数据可用",
    "Ethics": r"ethics|伦理",
    "CRediT": r"credit|author\s+contribution|作者贡献",
    "Conflicts of Interest": r"conflict|competing\s+interest|利益冲突",
    "Funding": r"funding|资助|基金",
    "AI Use Disclosure": r"ai\s+use|generative\s+ai|\bllm\b|ai\s+使用|生成式",
}


def _strip_code_fences(text):
    """剥除 ``` 围栏代码块（整段置空保留行号），避免示例代码里的 DOI/TODO/SOTA 假阳。"""
    out, in_fence = [], False
    for ln in text.splitlines():
        if ln.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append("")        # 围栏行本身置空，保留行号对齐
            continue
        out.append("" if in_fence else ln)
    return out


def _split_sentences(text):
    """粗切句（中英）：按 。！？.!? 和换行切，返回句列表。用于同句/相邻句共现判定。"""
    # 先把代码块剥掉再切句
    clean = "\n".join(_strip_code_fences(text))
    parts = re.split(r"(?<=[。！？.!?])\s+|\n+", clean)
    return [p.strip() for p in parts if p.strip()]


def _section_titles(text):
    """抽行首 markdown 标题（# / ## …）的文本，用于校验真有该 section 而非全文子串。"""
    titles = []
    for ln in _strip_code_fences(text):
        m = re.match(r"^#{1,6}\s+(.*)", ln)
        if m:
            titles.append(m.group(1).strip().lower())
    return titles


def lint(text, final=False, want_claims=False):
    findings = []
    code_stripped = _strip_code_fences(text)   # 行级、保留行号
    lines = code_stripped

    # 1. 残留缺口标记（跳过代码块后）
    gaps = [(i + 1, m.group(0)) for i, ln in enumerate(lines) for m in GAP_PAT.finditer(ln)]
    if gaps:
        sev = "FAIL" if final else "WARN"
        findings.append((sev, f"残留缺口标记 {len(gaps)} 处" + (" — 终稿门要求清零" if final else " — 初稿可暂留")))
        for ln_no, tok in gaps[:20]:
            findings.append(("  ", f"L{ln_no}: {tok}"))

    # 2. 必备声明：按行首 markdown 标题校验（不再全文子串）
    titles = _section_titles(text)
    title_blob = " | ".join(titles)
    missing = [name for name, pat in REQUIRED_SECTIONS.items() if not re.search(pat, title_blob, re.I)]
    if missing:
        findings.append(("WARN", "缺必备声明小节(按标题校验): " + ", ".join(missing)))

    # 3. 高危结果句缺显著性：SOTA 措辞与显著性在同句或相邻句窗口共现才算通过
    sents = _split_sentences(text)
    for i, s in enumerate(sents):
        if HYPE_PAT.search(s):
            window = " ".join(sents[max(0, i - 1):i + 2])  # 前一句+本句+后一句
            if not SIG_PAT.search(window):
                findings.append(("WARN", f"夸大/SOTA 措辞但邻近无显著性(p/CI/±std): {s[:70]}"))

    # 4. 引用台账（代码块已剥）
    clean_text = "\n".join(code_stripped)
    dois = sorted(set(DOI_PAT.findall(clean_text)))
    arxivs = sorted(set(ARXIV_PAT.findall(clean_text)))
    if dois or arxivs:
        findings.append(("INFO", f"引用待核: {len(dois)} DOI + {len(arxivs)} arXiv（需 curl 实测记 HTTP 码）"))
        for d in dois[:20]:
            findings.append(("  ", f'curl -sI -H "Accept: application/vnd.citationstyles.csl+json" https://doi.org/{d}'))
        for a in arxivs[:20]:
            aid = a.split(":", 1)[1]
            findings.append(("  ", f"curl -sI https://arxiv.org/abs/{aid}"))

    # 5. 候选事实句抽取（播种 claim 台账）
    claims = []
    if want_claims:
        for s in sents:
            if CLAIM_HINT_PAT.search(s) and not GAP_PAT.search(s):
                claims.append(s[:160])
        if claims:
            findings.append(("INFO", f"候选事实句 {len(claims)} 条（登记到 templates/claim_passport.md 逐条核查）"))
            for c in claims[:20]:
                findings.append(("  ", f"claim? {c}"))

    failed = any(sev == "FAIL" for sev, _ in findings)
    result = {
        "findings": findings, "failed": failed,
        "n_gaps": len(gaps), "missing_sections": missing,
        "n_doi": len(dois), "n_arxiv": len(arxivs),
        "candidate_claims": claims,
    }
    return findings, failed, result


def _selftest():
    bad = """# Title
We achieve state-of-the-art results, outperforming all baselines.
Tail accuracy improves by [RESULT GAP: 待实验].
Prior work [MATERIAL GAP: 需引用] showed something.
See doi 10.1109/CVPR.2016.90 and arXiv:1512.03385 for ResNet.
TODO: add ablation.
"""
    good = """# Title
We improve tail accuracy by 4.2 points (p<0.001, ±0.3 std) over the baseline.
## Data Availability
Synthetic data; code at anonymous repo.
## Ethics Statement
No human or animal subjects.
## CRediT Author Contributions
A.B.: all.
## Conflicts of Interest
None.
## Funding
No specific grant.
## AI Use Disclosure
LLM used for language editing; authors verified all content.
"""
    print("=== selftest: BAD draft (初稿门) ===")
    f1, fail1, r1 = lint(bad, final=False)
    for sev, msg in f1:
        print(f"[{sev}] {msg}")
    print(f"final-mode fail? {lint(bad, final=True)[1]}")

    print("\n=== selftest: GOOD draft (终稿门) ===")
    f2, fail2, r2 = lint(good, final=True)
    for sev, msg in f2:
        print(f"[{sev}] {msg}")

    # 断言：bad 在终稿门必失败；good 在终稿门不因 GAP 失败且无缺失声明
    assert lint(bad, final=True)[1] is True, "BAD 应在终稿门 FAIL"
    assert fail2 is False, "GOOD 不应有 FAIL 级问题"
    assert not any("缺必备声明" in m for _, m in f2), "GOOD 不应缺声明"
    assert any("引用待核" in m for _, m in f1), "BAD 应抽出引用待核"
    assert any("无显著性" in m for _, m in f1), "BAD 应标出无显著性的 SOTA 句"

    # 新增断言1：相邻句共现——SOTA 句与 p 值分处相邻句应判通过（不误报）
    adjacent = ("We achieve state-of-the-art results.\n"
                "The improvement is significant (p<0.001, ±0.2 std).")
    fa, _, _ = lint(adjacent)
    assert not any("无显著性" in m for _, m in fa), "相邻句有显著性不应误报"

    # 新增断言2：代码块里的 TODO/DOI/SOTA 不应被当真命中
    fenced = ("# Title\n```python\n# TODO: refactor\nx = 'state-of-the-art'\n"
              "# see 10.1109/CVPR.2016.90\n```\nReal text with no issues.\n"
              "## Data Availability\nx\n## Ethics\nx\n## CRediT\nx\n## Conflicts of Interest\nx\n"
              "## Funding\nx\n## AI Use Disclosure\nx\n")
    ff, _, rf = lint(fenced, final=True)
    assert rf["n_gaps"] == 0, f"代码块里的 TODO 不应计入 gap: {rf['n_gaps']}"
    assert rf["n_doi"] == 0, f"代码块里的 DOI 不应抽取: {rf['n_doi']}"
    assert not any("无显著性" in m for _, m in ff), "代码块里的 SOTA 字符串不应触发"

    # 新增断言3：必备声明按标题校验——正文散句含 'ethics' 但无标题 → 仍报缺失
    body_only = "# Title\nWe discuss ethics and funding informally in this paragraph.\n"
    fb, _, rb = lint(body_only, final=True)
    assert "Ethics" in rb["missing_sections"], "正文散句不应算作有 Ethics section"
    assert "Funding" in rb["missing_sections"], "正文散句不应算作有 Funding section"

    # 新增断言4：--claims 抽候选事实句
    fc, _, rc = lint("We improve accuracy by 4.2% over baseline.\nThe sky is blue.",
                     want_claims=True)
    assert rc["candidate_claims"], "应抽出含数字提升的候选事实句"
    assert any("4.2%" in c for c in rc["candidate_claims"]), rc["candidate_claims"]

    print("\nALL SELFTEST ASSERTIONS PASSED")


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        _selftest()
        return 0
    if len(argv) < 2:
        print(__doc__)
        return 2
    final = "--final" in argv
    as_json = "--json" in argv
    want_claims = "--claims" in argv
    path = [a for a in argv[1:] if not a.startswith("--")][0]
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    findings, failed, result = lint(text, final=final, want_claims=want_claims)
    if as_json:
        print(json.dumps({"failed": result["failed"], "n_gaps": result["n_gaps"],
                          "missing_sections": result["missing_sections"],
                          "n_doi": result["n_doi"], "n_arxiv": result["n_arxiv"],
                          "n_candidate_claims": len(result["candidate_claims"]),
                          "findings": [{"sev": s.strip(), "msg": m} for s, m in findings]},
                         ensure_ascii=False, indent=2))
    else:
        for sev, msg in findings:
            print(f"[{sev}] {msg}")
        print("\n==> " + ("FAIL: 有需返工项" if failed else "PASS: 无 FAIL 级问题（WARN 仍需人判）"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
