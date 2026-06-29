#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""croissant_export.py — 把数据卡字段导出为 Croissant JSON-LD（借 mlcommons/croissant）。

data_card_template.md 是人读 Markdown；本脚本据其关键字段额外产一份 **机器可读的 Croissant
JSON-LD**（MLCommons 标准，HF/Kaggle/OpenML 已采用），便于数据集发布后被自动索引，而不止人读。
纯标准库零依赖。

⚠ 诚实：本脚本产出的是**最小可用骨架**，覆盖 Croissant 核心字段（name/description/license/
url/citation + RecordSet 字段字典）；完整 Croissant（distribution 校验和、复杂 RecordSet
join、fileObject hash 等）须用 mlcommons/croissant 官方库校验。字段缺失如实留空不臆造。

用法：
  python croissant_export.py --in card_fields.json --out dataset.croissant.json
  python croissant_export.py --selftest
"""
from __future__ import annotations
import argparse
import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# 数据卡 data_type → Croissant/schema.org 粗映射（仅提示，不强约束）
_CROISSANT_CTX = {
    "@language": "en",
    "@vocab": "https://schema.org/",
    "cr": "http://mlcommons.org/croissant/",
    "data": {"@id": "cr:data", "@type": "@json"},
    "dataType": {"@id": "cr:dataType", "@type": "@vocab"},
    "field": "cr:field",
    "recordSet": "cr:recordSet",
}

# 数据卡字段类型 → Croissant dataType（schema.org / croissant 词表）
_DTYPE_MAP = {
    "int": "sc:Integer", "integer": "sc:Integer",
    "float": "sc:Float", "numeric": "sc:Float",
    "string": "sc:Text", "text": "sc:Text",
    "bool": "sc:Boolean", "boolean": "sc:Boolean",
    "datetime": "sc:DateTime", "date": "sc:Date",
}


def to_croissant(card: dict) -> dict:
    """card: 数据卡关键字段 dict。返回 Croissant JSON-LD（最小骨架）。"""
    name = card.get("dataset_name") or "unnamed-dataset"
    fields = []
    for col in card.get("columns", []) or []:
        cdt = _DTYPE_MAP.get((col.get("type") or "").lower(), "sc:Text")
        f = {
            "@type": "cr:Field",
            "@id": f"{name}/{col.get('name','field')}",
            "name": col.get("name", "field"),
            "description": col.get("meaning", "") or col.get("description", ""),
            "dataType": cdt,
        }
        if col.get("unit"):
            f["unitText"] = col["unit"]
        fields.append(f)

    cr = {
        "@context": _CROISSANT_CTX,
        "@type": "sc:Dataset",
        "conformsTo": "http://mlcommons.org/croissant/1.0",
        "name": name,
        "description": card.get("description", "") or card.get("motivation", ""),
        "version": str(card.get("version", "")) or "1.0.0",
        "license": card.get("license", "") or "unknown",
        "url": card.get("download_url", "") or card.get("paper_url", ""),
    }
    if card.get("doi"):
        cr["identifier"] = card["doi"]
    if card.get("citation") or card.get("paper_url"):
        cr["citation"] = card.get("citation") or card.get("paper_url")
    if card.get("keywords"):
        cr["keywords"] = card["keywords"]
    # RecordSet（字段字典）——有列定义才产
    if fields:
        cr["recordSet"] = [{
            "@type": "cr:RecordSet",
            "@id": f"{name}/records",
            "name": f"{name}_records",
            "field": fields,
        }]
    # 诚实标注未覆盖的部分
    cr["_light_note"] = ("最小 Croissant 骨架（Light croissant_export 生成）；distribution 校验和/"
                         "fileObject hash/复杂 RecordSet join 须用 mlcommons/croissant 官方库补全与校验。")
    return cr


def validate_minimal(cr: dict) -> list:
    """最小完整性检查：缺核心字段给警告（不臆造默认值）。返回警告列表。"""
    warns = []
    for key in ("name", "description", "license", "url"):
        if not cr.get(key) or cr.get(key) in ("unknown", ""):
            warns.append(f"缺/空字段 '{key}'——发布前应补（HF/Kaggle 索引会用到）")
    if cr.get("license") == "unknown":
        warns.append("license=unknown：开源发布前必须明确许可，否则他人无法合法使用")
    if "recordSet" not in cr:
        warns.append("无 recordSet（字段字典）：建议补 columns 让数据集字段机器可读")
    return warns


def _selftest() -> int:
    print("### croissant_export 离线自测", file=sys.stderr)
    card = {
        "dataset_name": "dairygoat-behavior",
        "description": "Sensor + video features for dairy goat estrus behavior.",
        "version": "1.2.0", "license": "CC-BY-4.0",
        "download_url": "https://example.org/dairygoat",
        "doi": "10.0000/dg.1", "keywords": ["animal", "behavior"],
        "columns": [
            {"name": "accel_x", "type": "float", "unit": "m/s^2", "meaning": "X 轴加速度"},
            {"name": "behavior", "type": "string", "meaning": "行为类别"},
            {"name": "goat_id", "type": "int", "meaning": "羊只 ID"},
        ],
    }
    cr = to_croissant(card)
    # 结构正确
    assert cr["@type"] == "sc:Dataset" and cr["name"] == "dairygoat-behavior", cr
    assert cr["conformsTo"].endswith("1.0") and cr["license"] == "CC-BY-4.0", cr
    assert cr["identifier"] == "10.0000/dg.1", cr
    # RecordSet + 字段类型映射
    rs = cr["recordSet"][0]["field"]
    accel = next(f for f in rs if f["name"] == "accel_x")
    assert accel["dataType"] == "sc:Float" and accel["unitText"] == "m/s^2", accel
    beh = next(f for f in rs if f["name"] == "behavior")
    assert beh["dataType"] == "sc:Text", beh
    # 可 JSON 序列化
    json.dumps(cr, ensure_ascii=False)

    # 缺字段告警（不臆造）
    warns = validate_minimal(to_croissant({"dataset_name": "x", "columns": []}))
    assert any("license" in w for w in warns) and any("recordSet" in w for w in warns), warns
    print("[selftest] PASS croissant_export offline")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="数据卡字段 → Croissant JSON-LD（机器可读数据卡）")
    ap.add_argument("--in", dest="infile", help="数据卡关键字段 JSON")
    ap.add_argument("--out", help="输出 .croissant.json 路径")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest or not args.infile:
        return _selftest()
    with open(args.infile, encoding="utf-8") as f:
        card = json.load(f)
    cr = to_croissant(card)
    warns = validate_minimal(cr)
    for w in warns:
        print(f"[warn] {w}", file=sys.stderr)
    out = json.dumps(cr, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"Croissant JSON-LD 已写入 {args.out}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
