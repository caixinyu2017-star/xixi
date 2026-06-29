#!/usr/bin/env python3
"""contrast_lint.py — WCAG 2.1 contrast checker for design tokens / CSS vars.

Parses hex colors out of a design-token JSON or a CSS/`@theme` block, then for
each declared foreground/background pairing (or, lacking explicit pairings, all
two-color combinations) computes the WCAG relative-luminance contrast ratio and
判 PASS/FAIL against the thresholds in references/visual-a11y-rules.md:

  normal body text (< 18pt / < 14pt bold)   >= 4.5:1
  large text       (>= 18pt / >= 14pt bold) >= 3:1
  UI component / graphic (borders, icons)    >= 3:1
  decorative / disabled                      no requirement (not checked)

Contrast math (WCAG 2.1):
  L = 0.2126*R + 0.7152*G + 0.0722*B, each channel linearized:
      c_srgb = c/255; c_lin = c_srgb/12.92 if c_srgb<=0.03928
               else ((c_srgb+0.055)/1.055)**2.4
  ratio = (L_light + 0.05) / (L_dark + 0.05)

Input forms (pure stdlib, no deps):
  - JSON: either a flat {"name": "#rrggbb", ...} map, a DTCG-style token tree
    with {"$value": "#rrggbb"} leaves, or a {"pairs": [{"fg","bg","role"?}]}
    list to check only specific pairings.
  - CSS:  any text containing `--name: #rrggbb;` / `color: #rgb;` declarations;
    all distinct hex colors are extracted and checked pairwise.

Usage:
  python contrast_lint.py <tokens.json|styles.css>   # exit 1 on any FAIL
  python contrast_lint.py - --css                    # stdin as CSS
  python contrast_lint.py - --json                   # stdin as JSON
  python contrast_lint.py --selftest                 # offline synthetic tests
  python contrast_lint.py                            # (no args) == --selftest
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass

# Thresholds straight from references/visual-a11y-rules.md (WCAG 2.1 AA).
TH_BODY = 4.5   # normal body text
TH_LARGE = 3.0  # large text (>=18pt / >=14pt bold)
TH_UI = 3.0     # UI components / graphics

_HEX_RE = re.compile(r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b")
# captures `--token-name: #hex` or `prop: #hex` with the identifier before it
_NAMED_HEX_RE = re.compile(
    r"(--[\w-]+|[\w-]+)\s*:\s*(#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6}))\b"
)


def _expand_hex(h: str) -> str:
    """Normalize #rgb / #rrggbb (with or without leading #) to 6-digit lower hex."""
    h = h.lstrip("#").lower()
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    if len(h) != 6 or any(c not in "0123456789abcdef" for c in h):
        raise ValueError(f"not a hex color: {h!r}")
    return h


def _channel_lin(c8: int) -> float:
    cs = c8 / 255.0
    return cs / 12.92 if cs <= 0.03928 else ((cs + 0.055) / 1.055) ** 2.4


def relative_luminance(hex6: str) -> float:
    h = _expand_hex(hex6)
    r, g, b = (int(h[i : i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _channel_lin(r) + 0.7152 * _channel_lin(g) + 0.0722 * _channel_lin(b)


def contrast_ratio(fg: str, bg: str) -> float:
    l1, l2 = relative_luminance(fg), relative_luminance(bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


@dataclass
class Pair:
    fg: str
    bg: str
    role: str = "body"  # body | large | ui
    fg_name: str = ""
    bg_name: str = ""


@dataclass
class Result:
    pair: Pair
    ratio: float
    threshold: float
    passed: bool

    def line(self) -> str:
        tag = "PASS" if self.passed else "FAIL"
        a = self.pair.fg_name or self.pair.fg
        b = self.pair.bg_name or self.pair.bg
        return (
            f"[{tag}] {self.pair.role:5s} {a} on {b}: "
            f"{self.ratio:.2f}:1 (need {self.threshold}:1)"
        )


_THRESHOLD = {"body": TH_BODY, "large": TH_LARGE, "ui": TH_UI}


def check_pairs(pairs: list[Pair]) -> list[Result]:
    out: list[Result] = []
    for p in pairs:
        th = _THRESHOLD.get(p.role, TH_BODY)
        r = contrast_ratio(p.fg, p.bg)
        out.append(Result(p, r, th, r >= th))
    return out


def render(results: list[Result]) -> str:
    if not results:
        return "no color pairs to check"
    lines = [r.line() for r in results]
    n_pass = sum(1 for r in results if r.passed)
    lines.append(f"--- {n_pass}/{len(results)} pairs pass WCAG AA ---")
    return "\n".join(lines)


# ---- extraction ---------------------------------------------------------

def _walk_json_colors(obj, prefix: str, acc: dict[str, str]) -> None:
    """Collect {name: hex} from a flat map or a DTCG ($value) token tree."""
    if isinstance(obj, dict):
        # DTCG leaf: {"$value": "#hex", ...}
        val = obj.get("$value")
        if isinstance(val, str) and _HEX_RE.fullmatch(val.strip()):
            acc[prefix or "color"] = _expand_hex(val.strip())
            return
        for k, v in obj.items():
            if k.startswith("$"):
                continue
            child = f"{prefix}.{k}" if prefix else k
            if isinstance(v, str) and _HEX_RE.fullmatch(v.strip()):
                acc[child] = _expand_hex(v.strip())
            else:
                _walk_json_colors(v, child, acc)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            _walk_json_colors(v, f"{prefix}[{i}]", acc)


def pairs_from_json(text: str) -> list[Pair]:
    data = json.loads(text)
    # explicit pairings take priority
    if isinstance(data, dict) and isinstance(data.get("pairs"), list):
        pairs: list[Pair] = []
        for item in data["pairs"]:
            pairs.append(
                Pair(
                    fg=_expand_hex(item["fg"]),
                    bg=_expand_hex(item["bg"]),
                    role=item.get("role", "body"),
                    fg_name=item.get("fg_name", item["fg"]),
                    bg_name=item.get("bg_name", item["bg"]),
                )
            )
        return pairs
    colors: dict[str, str] = {}
    _walk_json_colors(data, "", colors)
    return _all_combinations(colors)


def pairs_from_css(text: str) -> list[Pair]:
    colors: dict[str, str] = {}
    for name, hexv in _NAMED_HEX_RE.findall(text):
        try:
            colors[name] = _expand_hex(hexv)
        except ValueError:
            continue
    if not colors:  # fall back to any bare hex occurrences
        for m in _HEX_RE.finditer(text):
            h = _expand_hex(m.group(0))
            colors.setdefault(f"#{h}", h)
    return _all_combinations(colors)


def _all_combinations(colors: dict[str, str]) -> list[Pair]:
    items = list(colors.items())
    pairs: list[Pair] = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            n1, h1 = items[i]
            n2, h2 = items[j]
            if h1 == h2:
                continue
            pairs.append(Pair(fg=h1, bg=h2, role="body", fg_name=n1, bg_name=n2))
    return pairs


# ---- selftest -----------------------------------------------------------

def _approx(a: float, b: float, eps: float = 0.02) -> bool:
    return abs(a - b) <= eps


def _selftest() -> None:
    # Known WCAG reference values.
    assert _approx(contrast_ratio("#000000", "#ffffff"), 21.0), "black/white = 21:1"
    assert _approx(contrast_ratio("#ffffff", "#ffffff"), 1.0), "same color = 1:1"
    # #767676 on white is the canonical 4.5:1 boundary gray.
    assert _approx(contrast_ratio("#767676", "#ffffff"), 4.54, 0.1), "boundary gray"
    # #777 short-hex expands and parses.
    assert _approx(contrast_ratio("#fff", "#000"), 21.0), "short hex expands"

    print("=== JSON tokens (mixed pass/fail) ===")
    tok = json.dumps(
        {
            "color": {
                "ink": {"$value": "#1a1a1a"},
                "bg": {"$value": "#ffffff"},
                "muted": {"$value": "#cfcfcf"},  # low-contrast vs white
            }
        }
    )
    res = check_pairs(pairs_from_json(tok))
    print(render(res))
    # ink-on-bg should PASS body; muted-on-bg should FAIL body.
    by = {(r.pair.fg_name, r.pair.bg_name): r for r in res}
    assert any(r.passed for r in res), "at least one strong pair passes"
    assert any(not r.passed for r in res), "the muted/bg pair must fail"

    print("\n=== explicit pairs with roles ===")
    pj = json.dumps(
        {
            "pairs": [
                {"fg": "#1a1a1a", "bg": "#ffffff", "role": "body"},
                {"fg": "#949494", "bg": "#ffffff", "role": "body"},   # ~3.0 -> FAIL body
                {"fg": "#949494", "bg": "#ffffff", "role": "large"},  # ~3.0 -> PASS large
            ]
        }
    )
    rp = check_pairs(pairs_from_json(pj))
    print(render(rp))
    assert rp[0].passed, "dark ink on white passes body"
    assert not rp[1].passed, "mid-gray fails body 4.5:1"
    assert rp[2].passed, "same gray passes large 3:1"

    print("\n=== CSS variables ===")
    css = ":root{--fg:#222;--bg:#fff;--faint:#ddd;}\n.btn{color:#222;background:#fff}"
    rc = check_pairs(pairs_from_css(css))
    print(render(rc))
    assert any(not r.passed for r in rc), "faint/light pair fails"

    print("\nself-test OK")


def _run_file(path: str, mode: str | None) -> int:
    if path == "-":
        text = sys.stdin.read()
    else:
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            text = fh.read()
    if mode == "css" or (mode is None and path.lower().endswith(".css")):
        pairs = pairs_from_css(text)
    elif mode == "json" or (mode is None and path.lower().endswith(".json")):
        pairs = pairs_from_json(text)
    else:
        # sniff: JSON if it parses, else CSS
        try:
            pairs = pairs_from_json(text)
        except Exception:
            pairs = pairs_from_css(text)
    results = check_pairs(pairs)
    print(render(results))
    return 0 if all(r.passed for r in results) else 1


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] == "--selftest":
        _selftest()
    else:
        mode = None
        if "--css" in args:
            mode = "css"
        if "--json" in args:
            mode = "json"
        path = next((a for a in args if not a.startswith("--")), "-")
        raise SystemExit(_run_file(path, mode))
