#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""er_diagram.py — 表结构定义(YAML/JSON) → Mermaid erDiagram 文本 (Light / light-system-design)

输入一个描述实体表与关系的 YAML 或 JSON，输出可粘进 Markdown / mermaid.live 的
`erDiagram` 文本。纯离线、无第三方硬依赖（YAML 缺 PyYAML 时回退 JSON）。

输入 schema（YAML 示例）：
    entities:
      User:
        columns:
          - {name: id, type: int, key: PK}
          - {name: email, type: varchar, key: UK}
          - {name: name, type: varchar}
      Post:
        columns:
          - {name: id, type: int, key: PK}
          - {name: user_id, type: int, key: FK}
          - {name: title, type: varchar}
    relationships:
      - {from: User, to: Post, type: one-to-many, label: writes}

关系基数 type 取值（映射到 Mermaid 关系符号，默认实体均为 identifying "--"）：
    one-to-one   -> ||--||
    one-to-many  -> ||--o{
    many-to-one  -> }o--||
    many-to-many -> }o--o{
    zero-or-one  -> ||--o|
列 key 取值：PK(主键) / FK(外键) / UK(唯一)，渲染进列行的 Mermaid key 标记。

用法：
    python er_diagram.py --in schema.yaml
    python er_diagram.py --in schema.json --out er.mmd
    python er_diagram.py --in schema.yaml --strict   # 关系端点必须已定义实体，否则报错
    python er_diagram.py --selftest
"""
from __future__ import annotations
import argparse
import json
import sys

# 关系基数 -> Mermaid 关系符号（左实体 .. 右实体）
CARD = {
    "one-to-one": "||--||",
    "one-to-many": "||--o{",
    "many-to-one": "}o--||",
    "many-to-many": "}o--o{",
    "zero-or-one": "||--o|",
    "zero-or-many": "|o--o{",
}
# 列 key -> Mermaid 列 key 标记
KEYMAP = {"PK": "PK", "FK": "FK", "UK": "UK"}


def load_spec(text: str, prefer_yaml: bool = True) -> dict:
    """解析 YAML 或 JSON 文本为 dict。无 PyYAML 时回退尝试 JSON。"""
    text = text.strip()
    if prefer_yaml:
        try:
            import yaml  # type: ignore
            return yaml.safe_load(text) or {}
        except ImportError:
            pass  # 回退 JSON
    return json.loads(text)


def _sanitize(name: str) -> str:
    """Mermaid 实体/类型名只允许字母数字下划线，其余替换。"""
    out = "".join(c if (c.isalnum() or c == "_") else "_" for c in str(name))
    return out or "_"


def _col_line(col: dict) -> str:
    """渲染一列为 Mermaid: `type name KEY "comment"`。"""
    ctype = _sanitize(col.get("type", "string"))
    cname = _sanitize(col.get("name", "col"))
    parts = [f"    {ctype} {cname}"]
    key = col.get("key")
    if key:
        for k in str(key).replace("/", ",").split(","):
            k = k.strip().upper()
            if k in KEYMAP:
                parts.append(KEYMAP[k])
    comment = col.get("comment")
    line = " ".join(parts)
    if comment:
        line += f' "{comment}"'
    return line


def build_mermaid(spec: dict, strict: bool = False) -> str:
    """把表结构 spec 渲染为 erDiagram 文本。

    strict=True 时校验：每条关系的 from/to 都必须在 entities 中已定义，否则 raise
    ValueError（防把实体名写错却静默漏画该表）。默认 False 以兼容"先写关系、实体
    后补"的草稿用法——此时未定义的实体不报错，但也不会被渲染成块。
    """
    if not isinstance(spec, dict):
        raise ValueError("spec 顶层必须是对象/字典")
    entities = spec.get("entities") or {}
    rels = spec.get("relationships") or []
    if not entities:
        raise ValueError("spec 缺 entities（至少一个实体表）")

    lines = ["erDiagram"]
    # 已定义实体的 sanitized 名集合，供 strict 校验关系端点引用
    known = {_sanitize(e) for e in entities}
    for r in rels:
        a = _sanitize(r.get("from", ""))
        b = _sanitize(r.get("to", ""))
        if not a or not b:
            raise ValueError(f"关系缺 from/to: {r}")
        rtype = (r.get("type") or "one-to-many").lower()
        if rtype not in CARD:
            raise ValueError(f"未知关系基数 '{rtype}'，可选: {list(CARD)}")
        if strict:
            missing = [x for x in (a, b) if x not in known]
            if missing:
                raise ValueError(
                    f"关系引用了未在 entities 定义的实体 {missing}: {r}"
                    "（去掉 --strict 可放行先写关系后补实体的草稿）"
                )
        label = _sanitize(r.get("label", "rel")) or "rel"
        lines.append(f"    {a} {CARD[rtype]} {b} : {label}")

    # 实体列块
    for ename, edef in entities.items():
        en = _sanitize(ename)
        cols = (edef or {}).get("columns") or []
        lines.append(f"    {en} {{")
        for col in cols:
            lines.append(_col_line(col))
        lines.append("    }")
    return "\n".join(lines)


def _selftest() -> int:
    spec = {
        "entities": {
            "User": {"columns": [
                {"name": "id", "type": "int", "key": "PK"},
                {"name": "email", "type": "varchar", "key": "UK"},
                {"name": "name", "type": "varchar"},
            ]},
            "Post": {"columns": [
                {"name": "id", "type": "int", "key": "PK"},
                {"name": "user_id", "type": "int", "key": "FK"},
                {"name": "title", "type": "varchar", "comment": "标题"},
            ]},
        },
        "relationships": [
            {"from": "User", "to": "Post", "type": "one-to-many", "label": "writes"},
        ],
    }
    out = build_mermaid(spec)
    assert out.startswith("erDiagram"), out
    assert "User ||--o{ Post : writes" in out, out
    assert "int id PK" in out, out
    assert "varchar email UK" in out, out
    assert 'varchar title "标题"' in out, out
    assert sum(1 for ln in out.splitlines() if ln.strip().endswith("{")) == 2, out  # 两个实体块

    # JSON 文本解析路径
    spec2 = load_spec(json.dumps(spec), prefer_yaml=False)
    assert build_mermaid(spec2) == out, "JSON 解析结果应与 dict 一致"

    # YAML 文本解析路径（有 PyYAML 才验，缺则跳过不算失败）
    try:
        import yaml  # noqa: F401
        ytext = (
            "entities:\n"
            "  A:\n"
            "    columns:\n"
            "      - {name: id, type: int, key: PK}\n"
            "relationships:\n"
            "  - {from: A, to: A, type: one-to-one, label: self}\n"
        )
        m = build_mermaid(load_spec(ytext))
        assert "A ||--|| A : self" in m, m
        print("[selftest] YAML path OK")
    except ImportError:
        print("[selftest] PyYAML 缺失，跳过 YAML 解析路径（JSON 路径已验）")

    # 错误输入应抛而非崩
    for bad in ({}, {"entities": {}}, {"entities": {"X": {}},
                 "relationships": [{"from": "X", "to": "Y", "type": "weird"}]}):
        try:
            build_mermaid(bad)
            raise AssertionError(f"应对错误输入抛异常: {bad}")
        except ValueError:
            pass

    # --strict：关系端点引用未定义实体应抛 ValueError
    dangling = {
        "entities": {"User": {"columns": [{"name": "id", "type": "int", "key": "PK"}]}},
        "relationships": [{"from": "User", "to": "Ghost", "type": "one-to-many"}],
    }
    try:
        build_mermaid(dangling, strict=True)
        raise AssertionError("strict 模式应对未定义实体 Ghost 抛异常")
    except ValueError:
        pass
    # 非 strict（默认）应放行草稿：不抛，且不渲染未定义实体块
    draft = build_mermaid(dangling)
    assert "User ||--o{ Ghost" in draft, draft
    assert sum(1 for ln in draft.splitlines() if ln.strip().endswith("{")) == 1, draft
    # strict 下端点都已定义则正常渲染
    ok = build_mermaid(spec, strict=True)
    assert ok == out, "strict 对合法 spec 应与非 strict 输出一致"
    print("[selftest] strict 校验 OK")

    print("[selftest] PASS er_diagram")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description="表结构定义(YAML/JSON) → Mermaid erDiagram")
    ap.add_argument("--in", dest="infile", help="输入 YAML/JSON 路径")
    ap.add_argument("--out", dest="outfile", default="", help="输出 .mmd 路径（默认打印到 stdout）")
    ap.add_argument("--strict", action="store_true",
                    help="校验关系 from/to 必须是已定义实体，否则报错")
    ap.add_argument("--selftest", action="store_true", help="离线样例自测")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(_selftest())
    if not args.infile:
        ap.error("需 --in <schema.yaml|schema.json> 或 --selftest")

    with open(args.infile, encoding="utf-8") as f:
        text = f.read()
    prefer_yaml = not args.infile.lower().endswith(".json")
    spec = load_spec(text, prefer_yaml=prefer_yaml)
    mermaid = build_mermaid(spec, strict=args.strict)
    if args.outfile:
        with open(args.outfile, "w", encoding="utf-8") as f:
            f.write(mermaid + "\n")
        print(f"wrote {args.outfile}")
    else:
        print(mermaid)


if __name__ == "__main__":
    main()
