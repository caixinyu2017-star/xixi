#!/usr/bin/env python3
"""ai_tell_lint.py — mechanically flag the "AI-generated" tells.

Scans HTML/JSX/CSS source text for the blacklisted patterns from the skill's
AI-tell section. Each finding reports file position + the offending snippet so
it can be verified and fixed. Pure stdlib. Self-tests under __main__.

Blacklist (all machine-detectable):
  T1 scroll cue        : "scroll down", "scroll to explore", a bouncing
                         chevron/mouse hint near the hero.
  T2 section-numbering : eyebrow text like "01 /", "02.", "(01)" used as a
                         decorative section counter.
  T3 version footer    : "v1.0.0", "Made with", "Powered by <generic>" style
                         filler footers. The bare vX.Y.Z form is only a tell in
                         a footer/page-footer context (a changelog/release-notes
                         body legitimately lists versions, so we don't flag those).
  T4 em-dash           : the literal em-dash character used as ENGLISH prose
                         punctuation (a notorious LLM tell). Only flagged inside
                         HTML text nodes (not CSS/JS/comments/strings) and not
                         when adjacent to CJK characters, because the Chinese
                         破折号 is legitimate prose. Suggests en-dash/comma/rewrite.

Usage:
  python ai_tell_lint.py <file>     # lint a real file, exit 1 if tells found
  python ai_tell_lint.py -          # read source from stdin
  python ai_tell_lint.py --selftest # synthetic DIRTY/CLEAN tests
  python ai_tell_lint.py            # (no args) == --selftest
"""
from __future__ import annotations
import re
import sys
from dataclasses import dataclass
from html.parser import HTMLParser


@dataclass
class Finding:
    rule: str
    line: int
    snippet: str


# T1 scroll cues
_SCROLL = re.compile(
    r"(scroll\s*(down|to\s*explore|for\s*more)|scroll-(cue|hint|indicator)|"
    r"\bbounc\w*\s+(chevron|arrow|mouse))",
    re.I,
)
# T2 decorative section numbering used as eyebrow ("01 /", "02.", "(03)")
_SECNUM = re.compile(r"""(data-role=["']eyebrow["'][^>]*>\s*\(?0?\d{1,2}\s*[./)])""", re.I)
_SECNUM_TEXT = re.compile(r">\s*\(?0\d\s*[./)]\s*<")
# T3a "made with"/"powered by" filler — a tell anywhere it appears.
_MADEWITH = re.compile(r"(made\s+with\s+(love|❤|claude|ai|v0)|powered\s+by\s+\w+)", re.I)
# T3b bare semver — only a tell in a footer context (see _VersionScanner).
_VERSION = re.compile(r"v\d+\.\d+\.\d+", re.I)
# footer-context signal on a raw line (covers <footer>, data-role="footer", 页脚)
_FOOTER_HINT = re.compile(r"(<footer\b|data-role=[\"']?(footer|page-?footer)|页\s*脚)", re.I)
_EMDASH = "—"  # em-dash character

# Unicode ranges that count as CJK (Chinese 破折号 context is legitimate prose).
_CJK = re.compile(
    r"[　-〿㐀-䶿一-鿿豈-﫿＀-￯]"
)


def _is_cjk(ch: str) -> bool:
    return bool(ch) and bool(_CJK.match(ch))


class _ProseScanner(HTMLParser):
    """Walks HTML and flags em-dash only inside real text nodes (skipping
    <script>/<style>/comments) and only when it is NOT adjacent to a CJK
    character — i.e. English em-dash usage, the LLM tell."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.findings: list[Finding] = []
        self._skip_depth = 0  # inside <script>/<style>

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._skip_depth += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data: str):
        if self._skip_depth:
            return
        if _EMDASH not in data:
            return
        line = self.getpos()[0]
        for i, ch in enumerate(data):
            if ch != _EMDASH:
                continue
            prev_ch = data[i - 1] if i > 0 else ""
            next_ch = data[i + 1] if i + 1 < len(data) else ""
            # legitimate Chinese 破折号: adjacent to CJK on either side → skip
            if _is_cjk(prev_ch) or _is_cjk(next_ch):
                continue
            snip = data.strip()[:80] or "—"
            self.findings.append(Finding("T4 em-dash", line, snip))
            break  # one finding per text node is enough


def lint(text: str) -> list[Finding]:
    findings: list[Finding] = []
    # Line-based rules: T1, T2, T3a (made-with), T3b (version in footer line).
    for i, line in enumerate(text.splitlines(), 1):
        for rule, rx in (
            ("T1 scroll-cue", _SCROLL),
            ("T2 section-numbering eyebrow", _SECNUM),
            ("T2 section-numbering eyebrow", _SECNUM_TEXT),
            ("T3 version/made-with footer", _MADEWITH),
        ):
            m = rx.search(line)
            if m:
                findings.append(Finding(rule, i, line.strip()[:80]))
        # bare semver only counts as a tell when the line is footer context
        if _VERSION.search(line) and _FOOTER_HINT.search(line):
            findings.append(
                Finding("T3 version/made-with footer", i, line.strip()[:80])
            )

    # Parser-based rule: T4 em-dash in English prose text nodes only.
    scanner = _ProseScanner()
    try:
        scanner.feed(text)
        scanner.close()
    except Exception:
        pass  # malformed markup: skip the prose pass rather than crash the lint
    findings.extend(scanner.findings)
    findings.sort(key=lambda f: (f.line, f.rule))
    return findings


def render(findings: list[Finding]) -> str:
    if not findings:
        return "CLEAN: no AI-tells found."
    return "\n".join(f"L{f.line} [{f.rule}] {f.snippet}" for f in findings)


_DIRTY = """
<section data-layout="hero">
  <span data-role="eyebrow">01 / Intro</span>
  <h1>Hi</h1>
  <a class="scroll-cue">Scroll down to explore</a>
</section>
<p>We move fast — then we ship.</p>
<footer>Made with love · v1.2.3 · Powered by Acme</footer>
"""

_CLEAN = """
<section data-layout="hero">
  <span data-role="eyebrow">New release</span>
  <h1>Hi</h1>
</section>
<p>We move fast, then we ship.</p>
<footer>(c) 2026 Acme. All rights reserved.</footer>
"""

# These previously caused FALSE POSITIVES and must now stay CLEAN:
#  - Chinese 破折号 in legitimate prose (T4 must not fire on CJK-adjacent em-dash)
#  - em-dash inside a CSS/JS comment or string (T4 only scans HTML text nodes)
#  - a bare vX.Y.Z in a changelog/release-notes body, NOT a footer (T3 needs
#    footer context for the bare semver form)
_CLEAN_TRICKY = """
<section data-layout="content">
  <p data-role="body">奶山羊发情行为识别——一个跨学科的研究课题，需要细致标注。</p>
  <h2>更新日志</h2>
  <ul><li>v2.1.0 新增夜间识别</li><li>v2.0.3 修复漏检</li></ul>
</section>
<style>/* layout — keep the grid tidy */ .x{gap:8px}</style>
<script>const label = "range a—b means inclusive"; // note — keep simple</script>
"""

def _selftest() -> None:
    print("=== DIRTY (expect findings T1-T4) ===")
    d = lint(_DIRTY)
    print(render(d))
    rules = {f.rule[:2] for f in d}
    for needle in ("T1", "T2", "T3", "T4"):
        assert needle in rules, f"{needle} should be flagged in DIRTY"

    print("\n=== CLEAN (expect none) ===")
    c = lint(_CLEAN)
    print(render(c))
    assert not c, "CLEAN doc should have zero findings"

    print("\n=== CLEAN_TRICKY (no false positives) ===")
    t = lint(_CLEAN_TRICKY)
    print(render(t))
    assert not t, (
        "CLEAN_TRICKY must stay clean: CJK 破折号, comment/string em-dash, and "
        "changelog semver are all legitimate, not AI-tells"
    )

    print("\nself-test OK")


def _run_file(path: str) -> int:
    """Lint a real file (or '-' for stdin). Exit 1 if any AI-tell is found."""
    if path == "-":
        text = sys.stdin.read()
    else:
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            text = fh.read()
    findings = lint(text)
    print(render(findings))
    return 1 if findings else 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] == "--selftest":
        _selftest()
    else:
        raise SystemExit(_run_file(args[0]))
