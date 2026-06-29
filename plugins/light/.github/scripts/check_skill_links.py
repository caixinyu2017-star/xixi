#!/usr/bin/env python3
"""Validate internal file references inside Light skills.

CI scope:
- scan every skills/light-*/SKILL.md for concrete backtick paths under
  references/, templates/, examples/, assets/, and scripts/;
- scan SKILL.md, references.md, references/*.md, templates/*.md, and examples/*.md
  for explicit Markdown/HTML local links that resolve into those internal paths;
- validate optional SKILL.md frontmatter linked_files entries when present;
- reject path traversal for protected internal references;
- install-reachability (R8.8): any concrete ``../``-relative reference in a SKILL.md
  that points at a repo-level file/dir must have its top-level target present in the
  installer manifest (databases / code_assets / shared top-level docs), so the path
  still resolves after installing into ~/.claude/skills or ~/.agents/skills. Pure
  textual mentions (no relative path), e.g. orchestrator "见 CONVENTIONS §5", are allowed;
- skip generic directory mentions, globs, placeholders, and selftest-generated
  example output directories so the gate catches real drift without blocking on
  documentation examples.
"""
from __future__ import annotations

import io
import pathlib
import re
import sys
import urllib.parse
from collections import Counter
from typing import Iterable

import yaml

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[2]
SKILLS = ROOT / "skills"
TARGET_DIRS = {"references", "templates", "examples", "assets", "scripts"}
TARGET_ROOT_FILES = {"references.md"}
EXPECTED_SKILLS = 28

# R8.8 安装清单：install.sh 把这些仓库级 sibling 链进 ~/.../skills/ 旁边，
# 技能用 ../../<这些> 的相对路径装后才可达。databases/code_assets 是目录、其余是顶层文档。
# 解析自 install.sh 以免硬编码漂移（解析失败则退回这份内置默认）。
DEFAULT_INSTALL_MANIFEST = {"databases", "code_assets", "CONVENTIONS.md", "ROUTER.md", "ROUTER_EXAMPLES.md", "MODE_REGISTRY.md"}
# 相对仓库根的引用：``../`` 开头、最终落到仓库内某文件/目录的具体路径 token。
RELATIVE_REPO_RE = re.compile(r"(?<![\w./-])((?:\.\./)+[A-Za-z0-9_][A-Za-z0-9_./-]*)")

# Standard Markdown links/images and simple HTML href/src attributes.
MARKDOWN_LINK_RE = re.compile(r"!??\[[^\]\n]*(?:\][^\[\]\n]*)*\]\(([^)\n]+)\)")
HTML_ATTR_RE = re.compile(r'''\b(?:href|src)=["']([^"']+)["']''', re.IGNORECASE)
CODE_SPAN_RE = re.compile(r"`([^`\n]+)`")

# Concrete path-like tokens inside backticks. This intentionally starts at a
# protected internal directory/root file, so arbitrary function names, commands,
# URLs, and db paths are ignored.
INTERNAL_PATH_RE = re.compile(
    r"(?<![\w./-])"
    r"((?:references\.md|(?:references|templates|examples|assets|scripts)/[^\s`'\"),，。；;：:）\]}]+))"
)

GENERIC_DIR_MENTIONS = {f"{name}/" for name in TARGET_DIRS} | TARGET_DIRS
PLACEHOLDER_MARKERS = ("*", "{", "}", "<", ">", "xxx", "...", "…")
DYNAMIC_EXAMPLE_MARKERS = ("/_export_demo", "figure-export", "examples/example_out")

errors: list[str] = []
warnings: list[str] = []
checked_paths: list[tuple[str, str, str]] = []
skipped_reasons: Counter[str] = Counter()
install_refs_checked = 0


def split_frontmatter(text: str) -> tuple[str, str]:
    """Return (frontmatter_yaml, body) for a Markdown document."""
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[4:end], text[end + 5 :]
    return "", text


def load_install_manifest() -> set[str]:
    """Parse install.sh for the repo-level sibling targets it links next to skills/.

    Looks for ``safe_link_dir "$parent/databases" ...`` style sibling dirs and the
    ``for doc in CONVENTIONS.md ROUTER.md ... ; do`` shared-doc loop. Falls back to
    DEFAULT_INSTALL_MANIFEST if install.sh is missing or unparseable.
    """
    install_sh = ROOT / "install.sh"
    if not install_sh.exists():
        return set(DEFAULT_INSTALL_MANIFEST)
    text = install_sh.read_text(encoding="utf-8", errors="ignore")
    manifest: set[str] = set()
    for m in re.finditer(r'safe_link_dir\s+"\$parent/([A-Za-z0-9_.-]+)"', text):
        manifest.add(m.group(1))
    doc_loop = re.search(r"for\s+doc\s+in\s+([A-Za-z0-9_.\s-]+?);\s*do", text)
    if doc_loop:
        manifest.update(tok for tok in doc_loop.group(1).split() if tok)
    return manifest or set(DEFAULT_INSTALL_MANIFEST)


INSTALL_MANIFEST = load_install_manifest()


def strip_local_target(raw: str) -> str | None:
    """Normalize a raw link/token into a local path string, or None."""
    candidate = raw.strip().strip("<>")
    if not candidate or candidate.startswith("#"):
        return None
    if re.match(r"^[a-z][a-z0-9+.-]*:", candidate.lower()):
        return None

    # Markdown permits an optional title after whitespace: (path.md "title").
    candidate = candidate.split()[0]
    candidate = candidate.split("#", 1)[0].split("?", 1)[0]
    candidate = urllib.parse.unquote(candidate).replace("\\", "/")
    candidate = candidate.strip().strip("'\".,，。；;:：)）]】")
    if candidate.startswith("./"):
        candidate = candidate[2:]
    if not candidate or candidate.startswith("#"):
        return None
    return candidate


def raw_looks_protected(candidate: str) -> bool:
    """Return True when the raw path syntactically targets protected internals."""
    normalized = candidate.lstrip("/")
    if normalized.startswith("./"):
        normalized = normalized[2:]
    first = normalized.split("/", 1)[0]
    return normalized in TARGET_ROOT_FILES or first in TARGET_DIRS


def should_skip(candidate: str) -> str | None:
    """Return a skip reason for non-concrete/documentation-only path mentions."""
    normalized = candidate.rstrip("/")
    if candidate in GENERIC_DIR_MENTIONS or normalized in TARGET_DIRS:
        return "generic-dir"
    if any(marker in candidate for marker in PLACEHOLDER_MARKERS):
        return "placeholder-or-glob"
    if any(marker in candidate for marker in DYNAMIC_EXAMPLE_MARKERS):
        return "generated-example-output"
    return None


def allowed_roots(skill_dir: pathlib.Path) -> list[pathlib.Path]:
    """Return allowed internal roots for one skill."""
    roots = [skill_dir / name for name in TARGET_DIRS]
    roots.extend(skill_dir / name for name in TARGET_ROOT_FILES)
    return [root.resolve() for root in roots]


def is_within_or_equal(path: pathlib.Path, root: pathlib.Path) -> bool:
    """Return True if path is root or below root."""
    try:
        return path == root or path.is_relative_to(root)
    except AttributeError:  # pragma: no cover - Python <3.9 compatibility
        try:
            path.relative_to(root)
            return True
        except ValueError:
            return path == root


def is_allowed_internal_path(skill_dir: pathlib.Path, resolved: pathlib.Path) -> bool:
    """Return True when a resolved path stays inside protected skill internals."""
    return any(is_within_or_equal(resolved, root) for root in allowed_roots(skill_dir))


def resolve_candidate(skill_dir: pathlib.Path, doc: pathlib.Path, candidate: str, source: str) -> pathlib.Path:
    """Resolve candidate relative to the place where that syntax is normally written."""
    if candidate.startswith("/"):
        return (ROOT / candidate.lstrip("/")).resolve()
    # Markdown/HTML links are relative to their source document.
    if source in {"markdown link", "html attr"}:
        return (doc.parent / candidate).resolve()
    # Backtick asset paths and frontmatter linked_files are skill-root relative.
    return (skill_dir / candidate).resolve()


def display_candidate(skill_dir: pathlib.Path, resolved: pathlib.Path, raw_candidate: str) -> str:
    """Return a stable human-readable path for reports."""
    try:
        return resolved.relative_to(skill_dir.resolve()).as_posix()
    except ValueError:
        return raw_candidate


def skill_docs(skill_dir: pathlib.Path) -> list[pathlib.Path]:
    """Markdown docs whose explicit local Markdown/HTML links should be checked."""
    docs = [skill_dir / "SKILL.md", skill_dir / "references.md"]
    for subdir in ("references", "templates", "examples"):
        docs.extend(sorted((skill_dir / subdir).glob("*.md")))
    return [doc for doc in docs if doc.exists()]


def add_candidate(
    *,
    skill_dir: pathlib.Path,
    doc: pathlib.Path,
    raw: str,
    source: str,
    seen: set[tuple[str, str, str]],
) -> None:
    candidate = strip_local_target(raw)
    if not candidate:
        return
    if source not in {"markdown link", "html attr"} and candidate.startswith("/"):
        skipped_reasons["absolute-or-api-path"] += 1
        return
    skip_reason = should_skip(candidate)
    if skip_reason:
        skipped_reasons[skip_reason] += 1
        return

    protected_syntax = raw_looks_protected(candidate)
    resolved = resolve_candidate(skill_dir, doc, candidate, source)
    inside_allowed_root = is_allowed_internal_path(skill_dir, resolved)

    if source in {"markdown link", "html attr"}:
        # Markdown links can be written as relative siblings, e.g.
        # references/pipelines.md -> [checkpoints.md](checkpoints.md).
        # Check them when the resolved target is one of this skill's protected
        # internal paths. If a link syntactically claims a protected path but
        # resolves outside the allowed roots, fail closed instead of silently
        # accepting a traversal such as references/../SKILL.md.
        if not inside_allowed_root:
            if protected_syntax:
                rel_doc = doc.relative_to(ROOT).as_posix()
                errors.append(
                    f"{rel_doc}: {source} escapes protected skill internals: {candidate}"
                )
            return
    else:
        if not protected_syntax:
            return
        if not inside_allowed_root:
            rel_doc = doc.relative_to(ROOT).as_posix()
            errors.append(f"{rel_doc}: {source} escapes protected skill internals: {candidate}")
            return

    reported_candidate = display_candidate(skill_dir, resolved, candidate)
    key = (doc.relative_to(ROOT).as_posix(), reported_candidate, source)
    if key in seen:
        return
    seen.add(key)

    checked_paths.append((key[0], reported_candidate, source))
    if not resolved.exists():
        errors.append(f"{key[0]}: {source} points to missing internal path: {reported_candidate}")


def iter_code_span_path_tokens(text: str) -> Iterable[str]:
    """Yield concrete-looking internal paths from Markdown code spans."""
    for span_match in CODE_SPAN_RE.finditer(text):
        span = span_match.group(1)
        for path_match in INTERNAL_PATH_RE.finditer(span.replace("\\", "/")):
            yield path_match.group(1)
        # Also handle a code span that is exactly a protected path.
        yield span


def check_frontmatter_linked_files(skill_dir: pathlib.Path, seen: set[tuple[str, str, str]]) -> None:
    skill_file = skill_dir / "SKILL.md"
    frontmatter, _body = split_frontmatter(skill_file.read_text(encoding="utf-8", errors="ignore"))
    if not frontmatter:
        return
    try:
        data = yaml.safe_load(frontmatter) or {}
    except Exception as exc:  # noqa: BLE001 - CI diagnostic
        warnings.append(f"{skill_file.relative_to(ROOT).as_posix()}: frontmatter parse skipped: {exc}")
        return
    linked_files = data.get("linked_files")
    if not linked_files:
        return
    if not isinstance(linked_files, dict):
        errors.append(f"{skill_file.relative_to(ROOT).as_posix()}: linked_files must be a mapping")
        return
    for group, values in linked_files.items():
        if group not in TARGET_DIRS and group not in TARGET_ROOT_FILES:
            continue
        if isinstance(values, str):
            values = [values]
        if not isinstance(values, list):
            errors.append(f"{skill_file.relative_to(ROOT).as_posix()}: linked_files.{group} must be a list/string")
            continue
        for value in values:
            if not isinstance(value, str):
                errors.append(f"{skill_file.relative_to(ROOT).as_posix()}: linked_files.{group} contains non-string value")
                continue
            add_candidate(
                skill_dir=skill_dir,
                doc=skill_file,
                raw=value,
                source="frontmatter linked_files",
                seen=seen,
            )


def check_install_reachability(skill_dir: pathlib.Path, seen: set[str]) -> None:
    """R8.8: concrete ../-relative repo references in SKILL.md must be install-reachable.

    For each backtick token like ``../../code_assets/stats_tests.py`` or
    ``../../databases/db09-projects/...``: strip the leading ``../`` segments, take the
    first remaining top-level segment, and require it to be in the installer manifest
    (so the path still resolves after install). Also require the target to exist in the
    repo today. Placeholder/glob tokens are skipped.
    """
    global install_refs_checked
    skill_file = skill_dir / "SKILL.md"
    text = skill_file.read_text(encoding="utf-8", errors="ignore")
    rel_doc = skill_file.relative_to(ROOT).as_posix()
    for span_match in CODE_SPAN_RE.finditer(text):
        span = span_match.group(1).replace("\\", "/")
        for m in RELATIVE_REPO_RE.finditer(span):
            token = m.group(1).rstrip("/")
            # 占位/通配/模板片段不算具体引用
            if any(marker in token for marker in PLACEHOLDER_MARKERS):
                continue
            remainder = re.sub(r"^(?:\.\./)+", "", token)
            if not remainder:
                continue
            top = remainder.split("/", 1)[0]
            dedupe_key = f"{rel_doc}::{token}"
            if dedupe_key in seen:
                continue
            seen.add(dedupe_key)
            install_refs_checked += 1
            if top not in INSTALL_MANIFEST:
                errors.append(
                    f"{rel_doc}: 相对引用 {token!r} 的顶层目标 {top!r} 不在安装清单 "
                    f"{sorted(INSTALL_MANIFEST)}，装到 ~/.claude/skills 后将断链"
                    f"（改纯文字提及，或把 {top!r} 加入 install.sh/ps1 的 sibling 链接）"
                )
                continue
            # 安装清单内的目标，还须在仓库里真实存在（去掉占位后定位）
            clean = remainder.split("#", 1)[0].split("?", 1)[0]
            target = (ROOT / clean)
            if not target.exists():
                errors.append(f"{rel_doc}: 相对引用 {token!r} 在仓库内不存在: {clean}")


skill_dirs = sorted(path.parent for path in SKILLS.glob("light-*/SKILL.md"))
if len(skill_dirs) != EXPECTED_SKILLS:
    errors.append(f"expected {EXPECTED_SKILLS} Light skills, found {len(skill_dirs)}")
doc_count = 0
seen_candidates: set[tuple[str, str, str]] = set()
for skill_dir in skill_dirs:
    docs = skill_docs(skill_dir)
    doc_count += len(docs)
    for doc in docs:
        text = doc.read_text(encoding="utf-8", errors="ignore")
        for regex, source in ((MARKDOWN_LINK_RE, "markdown link"), (HTML_ATTR_RE, "html attr")):
            for match in regex.finditer(text):
                add_candidate(
                    skill_dir=skill_dir,
                    doc=doc,
                    raw=match.group(1),
                    source=source,
                    seen=seen_candidates,
                )
        # In SKILL.md, backtick paths are user-facing asset references and should
        # stay concrete. In research notes, backtick paths often describe third-
        # party repositories, so only explicit Markdown/HTML links are checked.
        if doc.name == "SKILL.md":
            for token in iter_code_span_path_tokens(text):
                add_candidate(
                    skill_dir=skill_dir,
                    doc=doc,
                    raw=token,
                    source="code span path",
                    seen=seen_candidates,
                )
    check_frontmatter_linked_files(skill_dir, seen_candidates)

install_seen: set[str] = set()
for skill_dir in skill_dirs:
    check_install_reachability(skill_dir, install_seen)

print(
    "技能内部链接: "
    f"skills={len(skill_dirs)}, docs={doc_count}, checked_paths={len(checked_paths)}, "
    f"install_refs={install_refs_checked}, skipped={sum(skipped_reasons.values())}"
)
if skipped_reasons:
    skipped = ", ".join(f"{reason}={count}" for reason, count in sorted(skipped_reasons.items()))
    print(f"跳过说明性路径: {skipped}")

if warnings:
    print("\n技能内部链接警告:")
    for warning in warnings:
        print(f"  ! {warning}")

if errors:
    print("\n技能内部链接校验失败:")
    for error in errors:
        print(f"  ✗ {error}")
    sys.exit(1)

print("✓ 技能内部 references/templates/examples/assets/scripts 链接均可解析到现有文件")
