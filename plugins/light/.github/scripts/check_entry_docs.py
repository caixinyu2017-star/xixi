#!/usr/bin/env python3
"""Validate Light entry-point docs and routing examples.

This gate protects the public/agent-facing entry layer:
- README zh/en must reflect the real 28 skills and 17/11 split;
- ROUTER.md must cover every manual/always-on skill via its m/a code;
- MODE_REGISTRY.md must report the actual mode table count;
- README.md and README.en.md must stay structurally isomorphic: same number of
  level-2 (##) headings, in the same order, with the same leading emoji/marker on
  each (heading text itself may differ zh/en) (R8.3 中英结构 gate);
- ROUTER_EXAMPLES.md must contain machine-readable examples whose expected
  skill codes exist in ROUTER.md, and must cover every one of the 28 skill
  codes plus light-orchestrator (28/28 必覆盖, R8.1 起从 7 个收紧到全集);
- out-of-scope skill names must not reappear in entry docs.
"""
from __future__ import annotations

import io
import pathlib
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[2]
SKILLS = ROOT / "skills"
ENTRY_DOCS = [
    "README.md",
    "README.en.md",
    "ROUTER.md",
    "ROUTER_EXAMPLES.md",
    "MODE_REGISTRY.md",
    "CONVENTIONS.md",
    "WHATS_INCLUDED.md",
]
FORBIDDEN_SKILL_NAMES = {"light-software", "light-miniprogram", "light-novel"}

MANUAL = {
    "m01": "light-literature-search",
    "m02": "light-data-engineering",
    "m03": "light-idea-generation",
    "m04": "light-idea-critique",
    "m05": "light-research-plan",
    "m06": "light-result-analysis",
    "m07": "light-paper-drafting",
    "m08": "light-paper-polishing",
    "m09": "light-figure-planning",
    "m10": "light-citation",
    "m11": "light-figure-drawing",
    "m12": "light-typesetting",
    "m13": "light-venue-matching",
    "m14": "light-review-rebuttal",
    "m15": "light-ip-application",
    "m16": "light-slides",
    "m17": "light-competition",
}
ALWAYS_ON = {
    "a01": "light-file-reading",
    "a02": "light-memory-pm",
    "a03": "light-backend-coding",
    "a04": "light-system-design",
    "a05": "light-frontend-design",
    "a06": "light-project-structure",
    "a07": "light-consistency",
    "a08": "light-self-review",
    "a09": "light-tool-selection",
    "a10": "light-research-ethics",
    "light-orchestrator": "light-orchestrator",
}
ALL_CODES = set(MANUAL) | set(ALWAYS_ON)
ALL_SKILLS_BY_CODE = MANUAL | ALWAYS_ON

errors: list[str] = []


def read(name: str) -> str:
    path = ROOT / name
    if not path.exists():
        errors.append(f"missing entry doc: {name}")
        return ""
    return path.read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def parse_mode_rows(markdown: str) -> list[str]:
    rows: list[str] = []
    in_mode_table = False
    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            in_mode_table = False
        if stripped == "| mode | 产出 | 触发场景 |":
            in_mode_table = True
            continue
        if in_mode_table:
            if not stripped.startswith("|"):
                in_mode_table = False
                continue
            if re.fullmatch(r"\|[-:| ]+\|", stripped):
                continue
            cells = [cell.strip() for cell in stripped.strip("|").split("|")]
            if len(cells) >= 3 and cells[0]:
                rows.append(cells[0])
    return rows


def parse_router_codes(router: str) -> set[str]:
    codes = set(re.findall(r"\b(?:m\d{2}|a\d{2})\b", router))
    if "light-orchestrator" in router:
        codes.add("light-orchestrator")
    return codes


def parse_router_examples(markdown: str) -> list[tuple[int, str, list[str]]]:
    rows: list[tuple[int, str, list[str]]] = []
    for lineno, line in enumerate(markdown.splitlines(), 1):
        stripped = line.strip()
        if not stripped.startswith("|") or "`" not in stripped:
            continue
        if re.fullmatch(r"\|[-:| ]+\|", stripped) or "用户输入" in stripped:
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 3:
            continue
        utterance = cells[0].strip("`")
        expected_cell = cells[1]
        expected = re.findall(r"`([^`]+)`", expected_cell)
        if expected:
            rows.append((lineno, utterance, expected))
    return rows


# Leading-marker regex: capture any non-word/non-CJK prefix (emoji, symbols) on a
# heading so README zh/en structure can be compared without matching translated text.
_HEADING_MARKER_RE = re.compile(r"^([^\w一-鿿]*)", re.UNICODE)


def parse_heading_markers(markdown: str) -> list[str]:
    """Return the ordered leading-marker (emoji/symbol prefix) of every ## heading."""
    markers: list[str] = []
    for line in markdown.splitlines():
        if line.startswith("## "):
            title = line[3:].strip()
            marker = _HEADING_MARKER_RE.match(title).group(1).strip()
            markers.append(marker)
    return markers


skill_dirs = sorted(path.parent.name for path in SKILLS.glob("light-*/SKILL.md"))
require(len(skill_dirs) == 28, f"expected 28 light skills, found {len(skill_dirs)}")
require(set(skill_dirs) == set(ALL_SKILLS_BY_CODE.values()), "manual/always-on registry does not match skills/light-* dirs")

texts = {name: read(name) for name in ENTRY_DOCS}

for name, text in texts.items():
    for forbidden in FORBIDDEN_SKILL_NAMES:
        if forbidden in text:
            errors.append(f"{name}: forbidden out-of-scope skill mention: {forbidden}")

for name in ("README.md", "README.en.md"):
    text = texts[name]
    require("28" in text, f"{name}: missing 28-skill count")
    require("17" in text, f"{name}: missing 17 manual skill count")
    require("11" in text, f"{name}: missing 11 always-on skill count")
    require("9" in text, f"{name}: missing 9 knowledge-base count")
    missing = [skill for skill in skill_dirs if skill not in text]
    if missing:
        errors.append(f"{name}: missing skill links/mentions: {', '.join(missing)}")

# R8.3 README 中英结构同构 gate：## 标题数量、顺序、前导 emoji/标记一致（文本不要求逐字）
zh_markers = parse_heading_markers(texts["README.md"])
en_markers = parse_heading_markers(texts["README.en.md"])
if len(zh_markers) != len(en_markers):
    errors.append(
        f"README 结构不同步: README.md 有 {len(zh_markers)} 个 ## 标题, "
        f"README.en.md 有 {len(en_markers)} 个 (数量须一致)"
    )
else:
    for idx, (zh_marker, en_marker) in enumerate(zip(zh_markers, en_markers), 1):
        if zh_marker != en_marker:
            errors.append(
                f"README 结构不同步: 第 {idx} 个 ## 标题前导标记不一致 "
                f"(README.md={zh_marker!r} vs README.en.md={en_marker!r})"
            )

router = texts["ROUTER.md"]
router_codes = parse_router_codes(router)
missing_router_codes = sorted(ALL_CODES - router_codes)
if missing_router_codes:
    errors.append(f"ROUTER.md: missing route codes: {', '.join(missing_router_codes)}")

mode_text = texts["MODE_REGISTRY.md"]
mode_rows = parse_mode_rows(mode_text)
reported_match = re.search(r"合计\s*(\d+)\s*个\s*mode", mode_text)
if not reported_match:
    errors.append("MODE_REGISTRY.md: missing reported total mode count phrase")
else:
    reported = int(reported_match.group(1))
    if reported != len(mode_rows):
        errors.append(f"MODE_REGISTRY.md: reported {reported} modes, parsed {len(mode_rows)} table rows")

examples = parse_router_examples(texts["ROUTER_EXAMPLES.md"])
require(len(examples) >= 30, f"ROUTER_EXAMPLES.md: expected >=30 examples, found {len(examples)}")
seen_utterances: set[str] = set()
covered_codes: set[str] = set()
for lineno, utterance, expected in examples:
    if utterance in seen_utterances:
        errors.append(f"ROUTER_EXAMPLES.md:{lineno}: duplicate utterance: {utterance}")
    seen_utterances.add(utterance)
    for code in expected:
        if code not in ALL_CODES:
            errors.append(f"ROUTER_EXAMPLES.md:{lineno}: unknown expected route code: {code}")
        covered_codes.add(code)

for required_code in sorted(ALL_CODES):
    if required_code not in covered_codes:
        errors.append(f"ROUTER_EXAMPLES.md: examples do not cover required route {required_code}")

print(
    "入口文档: "
    f"skills={len(skill_dirs)}, manual={len(MANUAL)}, always_on={len(ALWAYS_ON)}, "
    f"modes={len(mode_rows)}, route_examples={len(examples)}, "
    f"readme_h2={len(zh_markers)}/{len(en_markers)}"
)

if errors:
    print("\n入口文档校验失败:")
    for error in errors:
        print(f"  ✗ {error}")
    sys.exit(1)

print("✓ README/ROUTER/MODE_REGISTRY/ROUTER_EXAMPLES 入口一致性通过")
