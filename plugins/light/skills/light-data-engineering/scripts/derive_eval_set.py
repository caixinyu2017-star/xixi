#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""derive_eval_set.py — 据 m05 派生数据规格，从基础集生成鲁棒性/泛化/敏感性评测集。

m05(research-plan) 的实验矩阵里，鲁棒性/泛化/敏感性维度需要"派生评测集"：
在基础数据上做受控变换（加噪/缺失/跨域子集/扫参），用来测 ROB/GEN/SEN。
SKILL「回边」节说这些回 m02 构建——本脚本把这条回边从"口头规格"变成
"规格 JSON → 可执行变换 → 派生集 + dataset_card 字段"，回填 db04。

变换类型（transform）：
  noise    给数值列加高斯噪声        params: cols(可选), scale(相对std倍数)
  missing  随机置缺失(MCAR)          params: cols(可选), rate(缺失比例)
  subset   跨域子集(按列值筛)        params: col, values(保留的取值列表)
  scale    数值列乘以因子(扫参用)     params: cols(可选), factor

铁律（与 SKILL 防泄漏一致）：
- 派生**只动特征、不碰标签**（除非显式 target_safe=false）；不改变与目标的因果。
- 加噪/缺失只为评测鲁棒性，**仅作用于评测集**，不回流训练折。
- 固定 seed，记录到 dataset_card，保证可复现。

纯 numpy/pandas，零网络。规格见 examples/derive_spec.example.json。

用法：
  python derive_eval_set.py --base data.csv --spec derive_spec.json --outdir derived/
  python derive_eval_set.py --selftest
"""
from __future__ import annotations
import argparse
import io
import json
import os
import sys
import numpy as np
import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

VALID = {"noise", "missing", "subset", "scale"}


def _num_cols(df, cols):
    num = df.select_dtypes(include=[np.number]).columns.tolist()
    if cols:
        return [c for c in cols if c in num]
    return num


def apply_transform(df: pd.DataFrame, t: dict, target: str | None,
                    seed: int) -> pd.DataFrame:
    """据单条变换规格返回派生 DataFrame（不原地改）。"""
    kind = t.get("transform")
    if kind not in VALID:
        raise ValueError(f"未知 transform：{kind}（应为 {sorted(VALID)}）")
    rng = np.random.default_rng(seed)
    out = df.copy()
    p = t.get("params", {}) or {}
    target_safe = t.get("target_safe", True)
    cols = p.get("cols")
    # 默认保护标签列
    protect = {target} if (target and target_safe) else set()

    if kind == "noise":
        scale = float(p.get("scale", 0.1))
        for c in _num_cols(out, cols):
            if c in protect:
                continue
            std = float(out[c].std(ddof=0)) or 1.0
            out[c] = out[c] + rng.normal(0, scale * std, len(out))
    elif kind == "missing":
        rate = float(p.get("rate", 0.1))
        for c in (cols or [c for c in out.columns if c not in protect]):
            if c in protect or c not in out.columns:
                continue
            mask = rng.uniform(size=len(out)) < rate
            out.loc[mask, c] = np.nan
    elif kind == "subset":
        col = p.get("col")
        vals = p.get("values")
        if not col or col not in out.columns or vals is None:
            raise ValueError("subset 需 params.col 与 params.values")
        out = out[out[col].astype(str).isin([str(v) for v in vals])].reset_index(drop=True)
    elif kind == "scale":
        factor = float(p.get("factor", 1.0))
        for c in _num_cols(out, cols):
            if c in protect:
                continue
            out[c] = out[c] * factor
    return out


def build_card_fields(name: str, base_name: str, t: dict, n_rows: int,
                      seed: int) -> dict:
    """为派生集生成 dataset_card 关键字段（对齐 db04 schema），回填用。"""
    return {
        "dataset_name": name,
        "domain": "derived-eval",
        "task": t.get("eval_dim", "robustness"),
        "data_type": "tabular",
        "size": f"{n_rows} rows",
        "format": "csv",
        "license": "inherits-from-base",
        "download_url": "",
        "paper_url": "",
        "citation": f"derived from {base_name}",
        "leaderboard_url": "",
        "known_issues": f"派生集：{t.get('transform')} 变换；仅用于评测，不可回流训练",
        "bias_risk": "继承自基础集",
        "privacy_risk": "继承自基础集 access_level",
        "preprocessing_steps": f"transform={t.get('transform')} params={t.get('params', {})} seed={seed}",
        "recommended_splits": "评测集不再划分；与基础集同 split 锚点(SPLIT-01/02, LEAK-01)",
    }


def derive_all(df: pd.DataFrame, spec: dict) -> list[dict]:
    """据完整规格生成所有派生集。返回 [{name, df, card}]。"""
    base_name = spec.get("base_name", "base")
    target = spec.get("target")
    seed = int(spec.get("seed", 0))
    results = []
    for i, t in enumerate(spec.get("transforms", [])):
        name = t.get("name") or f"{base_name}_{t.get('transform')}_{i}"
        derived = apply_transform(df, t, target, seed + i)
        card = build_card_fields(name, base_name, t, len(derived), seed + i)
        results.append({"name": name, "df": derived, "card": card,
                        "transform": t.get("transform")})
    return results


def _selftest() -> int:
    print("### derive_eval_set 离线自测", file=sys.stderr)
    rng = np.random.default_rng(0)
    n = 200
    base = pd.DataFrame({
        "f1": rng.normal(0, 1, n),
        "f2": rng.normal(10, 2, n),
        "domain": rng.choice(["A", "B", "C"], n),
        "label": rng.integers(0, 2, n),
    })
    spec = {
        "base_name": "demo", "target": "label", "seed": 0,
        "transforms": [
            {"name": "demo_noise", "transform": "noise", "eval_dim": "robustness",
             "params": {"scale": 0.5}},
            {"name": "demo_missing", "transform": "missing",
             "params": {"rate": 0.3, "cols": ["f1"]}},
            {"name": "demo_subset", "transform": "subset",
             "params": {"col": "domain", "values": ["A"]}},
            {"name": "demo_scale", "transform": "scale", "params": {"factor": 2.0}},
        ],
    }
    res = derive_all(base, spec)
    by = {r["name"]: r for r in res}
    # noise：f1 改变但 label 不动（target_safe 默认 True）
    assert not np.allclose(by["demo_noise"]["df"]["f1"], base["f1"]), "noise 未改特征"
    assert (by["demo_noise"]["df"]["label"] == base["label"]).all(), "noise 误改了标签"
    # missing：f1 出现 NaN，且 rate 约 0.3，label 无 NaN
    miss_rate = by["demo_missing"]["df"]["f1"].isna().mean()
    assert 0.15 < miss_rate < 0.45, f"missing rate 异常: {miss_rate}"
    assert by["demo_missing"]["df"]["label"].isna().sum() == 0, "missing 误伤标签"
    # subset：只剩 domain==A
    assert set(by["demo_subset"]["df"]["domain"].unique()) == {"A"}, "subset 筛选错"
    assert len(by["demo_subset"]["df"]) < n, "subset 未缩小"
    # scale：f2 翻倍，label 不变
    assert np.allclose(by["demo_scale"]["df"]["f2"], base["f2"] * 2), "scale 未生效"
    assert (by["demo_scale"]["df"]["label"] == base["label"]).all(), "scale 误改标签"
    # card 字段对齐 db04（16 字段齐全）
    card = by["demo_noise"]["card"]
    for k in ("dataset_name", "domain", "task", "data_type", "size", "format",
              "license", "preprocessing_steps", "recommended_splits", "known_issues"):
        assert k in card, f"card 缺字段 {k}"
    assert "seed=" in card["preprocessing_steps"], "card 未记 seed（可复现性）"
    # 未知 transform 报错
    try:
        apply_transform(base, {"transform": "bogus"}, "label", 0)
        raise AssertionError("应报错")
    except ValueError:
        pass
    # 可复现：同 seed 两次结果一致
    r2 = derive_all(base, spec)
    assert np.allclose(r2[0]["df"]["f1"], by["demo_noise"]["df"]["f1"]), "同seed不可复现"
    print("[selftest] PASS derive_eval_set offline")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="据 m05 派生规格生成评测集 + dataset_card 字段")
    ap.add_argument("--base", help="基础数据 CSV")
    ap.add_argument("--spec", help="派生规格 JSON（见 examples/derive_spec.example.json）")
    ap.add_argument("--outdir", help="输出目录（派生 CSV + *_card_fields.json）")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest or not (args.base and args.spec):
        return _selftest()

    df = pd.read_csv(args.base)
    with io.open(args.spec, encoding="utf-8") as fh:
        spec = json.load(fh)
    res = derive_all(df, spec)
    outdir = args.outdir or "."
    os.makedirs(outdir, exist_ok=True)
    for r in res:
        csv_path = os.path.join(outdir, f"{r['name']}.csv")
        card_path = os.path.join(outdir, f"{r['name']}_card_fields.json")
        r["df"].to_csv(csv_path, index=False)
        with io.open(card_path, "w", encoding="utf-8") as fh:
            json.dump(r["card"], fh, ensure_ascii=False, indent=2)
        print(f"[{r['transform']}] {csv_path} ({len(r['df'])} rows) + {card_path}",
              file=sys.stderr)
    print(f"生成 {len(res)} 个派生评测集到 {outdir}/；card_fields 可喂 croissant_export.py 回填 db04。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
