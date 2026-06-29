#!/usr/bin/env python3
"""Validate Light database markdown files.

CI scope:
- every fenced ```yaml/```yml block under databases/ must parse as YAML;
- database card-bearing files must contain non-empty list[dict] YAML blocks;
- db03–db08 real cards must satisfy their README-declared required fields;
- template blocks with all required fields left blank are allowed and skipped;
- duplicate YAML keys are rejected instead of silently overwritten;
- db03 method_name, db04 dataset_name, db05 project_type, db06 scenario, db07 figure_type and db08 material_type must be unique within each database;
- db09 project_card.md must carry all 14 CONVENTIONS §3 project-card fields and its
  decision_log/version_history/terminology siblings must exist (R8.4);
- every local .md link in a database README must point to an existing file.
"""
from __future__ import annotations

import io
import pathlib
import re
import sys

import yaml
from yaml.constructor import ConstructorError
from yaml.nodes import MappingNode

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[2]
DATABASES = ROOT / "databases"

errors: list[str] = []
yaml_blocks = 0
readme_links = 0
schema_checked_cards = 0
template_cards = 0
project_checked_cards = 0
duplicate_name_index: dict[tuple[str, str], list[str]] = {}

SCHEMAS: dict[str, list[str]] = {
    "db03-methods": "method_name, task_type, input_data, output_result, core_assumption, advantages, limitations, common_baselines, evaluation_metrics, suitable_datasets, implementation_repo, representative_papers, possible_innovation_points, maturity".split(", "),
    "db04-datasets": "dataset_name, domain, task, data_type, size, format, license, download_url, paper_url, citation, leaderboard_url, known_issues, bias_risk, privacy_risk, preprocessing_steps, recommended_splits".split(", "),
    "db05-frontend-styles": "project_type, style_tag, layout_type, color_palette, font_style, component_pattern, interaction_pattern, animation_type, screenshot_reference, implementation_notes, suitable_project_scene".split(", "),
    "db06-ppt-styles": "scenario, theme_style, page_type, layout_structure, color_palette, font_pairing, visual_hierarchy, chart_style, icon_style, transition_style, speaker_notes_style, reuse_template_notes".split(", "),
    "db07-figures": "figure_type, paper_source, research_field, purpose, data_required, layout, color_scheme, annotation_style, caption_style, possible_code_tool, replication_notes, where_to_place_in_paper".split(", "),
    "db08-ip-materials": "material_type, required_sections, official_requirement, writing_style, common_mistakes, checklist, sample_structure, legal_risk, reuse_scope, final_review_needed".split(", "),
}

NAME_FIELDS = {
    "db03-methods": "method_name",
    "db04-datasets": "dataset_name",
    "db05-frontend-styles": "project_type",
    "db06-ppt-styles": "scenario",
    "db07-figures": "figure_type",
    "db08-ip-materials": "material_type",
}

UNIQUE_NAME_FIELDS = {
    "db03-methods": "method_name",
    "db04-datasets": "dataset_name",
    "db05-frontend-styles": "project_type",
    "db06-ppt-styles": "scenario",
    "db07-figures": "figure_type",
    "db08-ip-materials": "material_type",
}

# CONVENTIONS §3 项目卡 14 字段（真相源）。project_card.md 的 yaml 块须全含且非空。
DB09_CARD_FIELDS = "project_name, goal, current_stage, confirmed_idea, data_status, method_status, experiment_status, paper_status, ppt_status, code_status, risk_list, next_actions, decision_log, version_history".split(", ")


class UniqueKeyLoader(yaml.SafeLoader):
    """SafeLoader variant that rejects duplicate keys instead of overwriting."""


def construct_unique_mapping(loader: UniqueKeyLoader, node: MappingNode, deep: bool = False):
    seen = set()
    for key_node, _ in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in seen:
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        seen.add(key)
    return yaml.SafeLoader.construct_mapping(loader, node, deep=deep)


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    construct_unique_mapping,
)


YAML_FENCE_RE = re.compile(
    r"^[ \t]{0,3}```[ \t]*(?:ya?ml)(?:[ \t].*)?[ \t]*\n(.*?)\n^[ \t]{0,3}```[ \t]*$",
    flags=re.S | re.I | re.M,
)


def is_card_file(path: pathlib.Path) -> bool:
    name = path.name.lower()
    return name.startswith("cards") or name.endswith("_cards.md")


def is_schema_card_file(path: pathlib.Path) -> bool:
    """Files whose fenced YAML blocks are database cards and must satisfy schema checks."""
    db_key = db_key_for(path)
    if is_card_file(path):
        return True
    return db_key in {"db05-frontend-styles", "db06-ppt-styles", "db07-figures"} and path.name == "resources_real.md"


def db_key_for(path: pathlib.Path) -> str | None:
    try:
        rel = path.relative_to(DATABASES)
    except ValueError:
        return None
    return rel.parts[0] if rel.parts else None


def is_blank(value) -> bool:
    if value is None:
        return True
    if isinstance(value, str) and not value.strip():
        return True
    if isinstance(value, (list, dict, tuple, set)) and len(value) == 0:
        return True
    return False


def is_template_card(item: dict, fields: list[str]) -> bool:
    """A README seed/template block has required keys and every value blank."""
    return set(fields).issubset(item) and all(is_blank(value) for value in item.values())


def is_allowed_template_block(path: pathlib.Path, block_index: int) -> bool:
    """Only the first YAML block in seed card files is allowed to be blank template."""
    return block_index == 1 and path.name in {
        "method_cards.md",
        "dataset_cards.md",
        "design_cards.md",
        "slide_cards.md",
        "figure_cards.md",
        "material_cards.md",
    }


def readme_schema_fields(db_key: str) -> list[str] | None:
    """Read the explicit whole-line comma-separated schema from a db README."""
    readme = DATABASES / db_key / "README.md"
    if not readme.exists():
        return None
    for line in readme.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"\s*`([^`]+,[^`]+)`\s*", line)
        if match:
            return [field.strip() for field in match.group(1).split(",")]
    return None


def card_label(db_key: str, item: dict, fallback: str) -> str:
    name_field = NAME_FIELDS.get(db_key)
    if name_field:
        value = item.get(name_field)
        if value:
            return str(value)
    return fallback


def record_unique_name(db_key: str, item: dict, location: str) -> None:
    """Collect exact card names for databases where duplicate names fail CI."""
    name_field = UNIQUE_NAME_FIELDS.get(db_key)
    if not name_field:
        return
    value = item.get(name_field)
    if is_blank(value):
        return
    key = (db_key, str(value).strip())
    duplicate_name_index.setdefault(key, []).append(location)


if not DATABASES.exists():
    errors.append("databases/: missing directory")
else:
    for db_key, expected_fields in sorted(SCHEMAS.items()):
        actual_fields = readme_schema_fields(db_key)
        if actual_fields is None:
            errors.append(f"databases/{db_key}/README.md: missing schema backtick line")
        elif actual_fields != expected_fields:
            errors.append(
                f"databases/{db_key}/README.md: schema differs from check_databases.py; "
                f"README={actual_fields!r}, checker={expected_fields!r}"
            )

    for md in sorted(DATABASES.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        rel = md.relative_to(ROOT)
        db_key = db_key_for(md)
        schema = SCHEMAS.get(db_key or "")
        blocks = list(YAML_FENCE_RE.finditer(text))
        schema_card_file = is_schema_card_file(md)
        if schema_card_file and not blocks:
            errors.append(f"{rel}: card-bearing file has no fenced YAML blocks")
        for idx, match in enumerate(blocks, start=1):
            block = match.group(1)
            yaml_blocks += 1
            try:
                data = yaml.load(block, Loader=UniqueKeyLoader)
            except Exception as exc:  # noqa: BLE001 - report parser detail in CI
                errors.append(f"{rel}: yaml block #{idx} does not parse: {exc}")
                continue
            if not schema_card_file:
                continue
            if not isinstance(data, list) or not data:
                errors.append(f"{rel}: yaml block #{idx} must be a non-empty list")
                continue
            if not all(isinstance(item, dict) for item in data):
                errors.append(f"{rel}: yaml block #{idx} must contain only mappings")
                continue
            if not schema:
                continue
            for item_idx, item in enumerate(data, start=1):
                fallback = f"block {idx} item {item_idx}"
                if is_template_card(item, schema) and is_allowed_template_block(md, idx):
                    template_cards += 1
                    continue
                schema_checked_cards += 1
                missing = [field for field in schema if field not in item or is_blank(item.get(field))]
                if missing:
                    label = card_label(db_key or "", item, fallback)
                    errors.append(f"{rel}: {fallback} ({label}) missing required fields: {', '.join(missing)}")
                record_unique_name(db_key or "", item, f"{rel}: {fallback}")

    for (db_key, name), locations in sorted(duplicate_name_index.items()):
        if len(locations) > 1:
            joined = "; ".join(locations)
            name_field = UNIQUE_NAME_FIELDS[db_key]
            errors.append(f"databases/{db_key}: duplicate {name_field} {name!r}: {joined}")

    # --- R8.4 db09 项目卡 schema：CONVENTIONS §3 项目卡 14 字段为真相源 ---
    db09_root = DATABASES / "db09-projects" / "projects"
    if db09_root.exists():
        for card in sorted(db09_root.glob("*/project_card.md")):
            project_checked_cards += 1
            rel = card.relative_to(ROOT)
            text = card.read_text(encoding="utf-8")
            blocks = list(YAML_FENCE_RE.finditer(text))
            if not blocks:
                errors.append(f"{rel}: project_card.md 缺 ```yaml 字段块")
                continue
            try:
                data = yaml.load(blocks[0].group(1), Loader=UniqueKeyLoader)
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{rel}: project_card yaml 不能解析: {exc}")
                continue
            if not isinstance(data, dict):
                errors.append(f"{rel}: project_card yaml 块必须是字段映射")
                continue
            missing = [f for f in DB09_CARD_FIELDS if f not in data or is_blank(data.get(f))]
            if missing:
                errors.append(f"{rel}: 项目卡缺字段: {', '.join(missing)}")
            # 四件套同目录文件齐全（decision_log/version_history/terminology）
            for sibling in ("decision_log.md", "version_history.md", "terminology.md"):
                if not (card.parent / sibling).exists():
                    errors.append(f"{rel.parent}: 缺配套文件 {sibling}")

    for readme in sorted(DATABASES.glob("db*/README.md")):
        text = readme.read_text(encoding="utf-8")
        base = readme.parent
        rel_readme = readme.relative_to(ROOT)
        for target in re.findall(r"\]\(([^)]+)\)", text):
            if re.match(r"^[a-z]+://", target):
                continue
            if target.startswith("#"):
                continue
            clean = target.split("#", 1)[0].split("?", 1)[0]
            if not clean.endswith(".md"):
                continue
            readme_links += 1
            path = (base / clean).resolve()
            try:
                path.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"{rel_readme}: link escapes repo: {target}")
                continue
            if not path.exists():
                errors.append(f"{rel_readme}: missing linked file {target}")

print(
    "数据库 Markdown: "
    f"yaml_blocks={yaml_blocks}, readme_md_links={readme_links}, "
    f"schema_checked_cards={schema_checked_cards}, template_cards={template_cards}, "
    f"db09_project_cards={project_checked_cards}"
)
if errors:
    print("\n数据库校验失败:")
    for err in errors:
        print(f"  ✗ {err}")
    sys.exit(1)
print("✓ 数据库 YAML、schema 与 README 链接合规")
