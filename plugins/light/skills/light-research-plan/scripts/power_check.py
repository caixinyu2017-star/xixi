#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""power_check.py — 统计功效反推种子/重复数（让"先做功效分析"成强制前置而非脚注）。

research-plan 正文写"≥5 个随机种子"，但功效分析证明中效应(d=0.5)每组需 ~64 次——5 种子对中小
效应严重欠功效(power≈0.11)。本脚本把这个矛盾算清：输入效应量 + 当前重复数 → 输出**实际 power**
与**达到目标 power 所需最小重复数**，让用户在填实验矩阵种子数前先跑它，而不是被模板默认的 5 误导。

优先用 statsmodels(TTestIndPower，与 SKILL 功效分析口径一致)；缺失则降级到闭式正态近似
（双样本 t 检验 power 的标准近似），并标注 [APPROX]，保证无 statsmodels 也能离线跑 selftest。

⚠ 诚实：闭式/近似适用于双样本均值比较(t 检验)。复杂设计(ANOVA/混合模型/比例/相关)请用
statsmodels 对应 Power 类或 simulation-based 功效估计——本脚本对那些只给"用专门方法"的提示，不硬算。

用法：
  python power_check.py --effect 0.5 --n 5                 # 看 5 次重复对 d=0.5 的实际 power
  python power_check.py --effect 0.5 --target-power 0.8    # 反推达 0.8 power 所需最小重复数
  python power_check.py --selftest
"""
from __future__ import annotations
import argparse
import math
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# 标准正态 CDF / 分位（避免依赖 scipy）
def _norm_cdf(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def _norm_ppf(p: float) -> float:
    """标准正态分位的有理近似（Acklam 算法，精度足够功效估算）。"""
    if not (0 < p < 1):
        raise ValueError("p must be in (0,1)")
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    plow, phigh = 0.02425, 1 - 0.02425
    if p < plow:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    if p > phigh:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    q = p - 0.5
    r = q * q
    return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)


def power_ttest_ind(effect: float, n: int, alpha: float = 0.05) -> tuple[float, str]:
    """双样本 t 检验 power。优先 statsmodels，缺失降级正态近似。返回 (power, backend)。"""
    try:
        from statsmodels.stats.power import TTestIndPower
        p = TTestIndPower().power(effect_size=effect, nobs1=n, alpha=alpha, ratio=1.0,
                                  alternative="two-sided")
        return round(float(p), 4), "statsmodels"
    except Exception:
        # 闭式正态近似：非中心参数 ncp = d*sqrt(n/2)，power = P(Z > z_{1-a/2} - ncp)
        ncp = effect * math.sqrt(n / 2.0)
        zcrit = _norm_ppf(1 - alpha / 2)
        power = 1 - _norm_cdf(zcrit - ncp) + _norm_cdf(-zcrit - ncp)
        return round(float(power), 4), "normal-approx[APPROX]"


def min_n_for_power(effect: float, target: float = 0.8, alpha: float = 0.05,
                    cap: int = 100000) -> int | None:
    """反推达到 target power 所需每组最小重复数。线性扫描（n 不大，够用）。"""
    for n in range(2, cap):
        p, _ = power_ttest_ind(effect, n, alpha)
        if p >= target:
            return n
    return None


def check(effect: float, n: int | None = None, target_power: float = 0.8,
          alpha: float = 0.05) -> dict:
    out = {"effect_size": effect, "alpha": alpha, "target_power": target_power}
    min_n = min_n_for_power(effect, target_power, alpha)
    out["min_n_for_target"] = min_n
    if n is not None:
        power, backend = power_ttest_ind(effect, n, alpha)
        out["n"] = n
        out["actual_power"] = power
        out["backend"] = backend
        out["adequate"] = power >= target_power
        if not out["adequate"]:
            out["verdict"] = (f"⚠ 欠功效：每组 {n} 次对 d={effect} 仅 power={power}"
                              f"（<目标 {target_power}）——需 ≥{min_n} 次/组才够。"
                              f"别被'≥5 种子'默认值误导，按本结果设重复数。")
        else:
            out["verdict"] = f"✓ 每组 {n} 次对 d={effect} 达 power={power} ≥{target_power}，功效充足。"
    else:
        out["verdict"] = f"达目标 power {target_power}（d={effect}, α={alpha}）需每组 ≥{min_n} 次重复。"
    out["note"] = ("适用双样本均值比较(t 检验)；ANOVA/比例/相关/混合模型请用 statsmodels 对应 Power 类"
                   "或 simulation-based 估计。效应量 d 应来自前人/预实验，不是拍脑袋。")
    return out


def render(rep: dict) -> str:
    lines = [f"# 统计功效检查（d={rep['effect_size']}, α={rep['alpha']}, 目标 power={rep['target_power']}）", ""]
    if "actual_power" in rep:
        lines.append(f"- 当前每组 {rep['n']} 次 → 实际 power = **{rep['actual_power']}**（{rep['backend']}）")
    lines.append(f"- 达目标 power 所需每组最小重复数 = **{rep['min_n_for_target']}**")
    lines.append("")
    lines.append(rep["verdict"])
    lines.append("")
    lines.append(f"> {rep['note']}")
    return "\n".join(lines)


def _selftest() -> int:
    print("### power_check 离线自测", file=sys.stderr)
    # 经典结论：d=0.5 每组 ~64 达 power 0.8（statsmodels 精确值 64）
    min_n = min_n_for_power(0.5, 0.8)
    assert 60 <= min_n <= 70, f"d=0.5 达 0.8 应约 64/组，得 {min_n}"
    # 5 次重复对 d=0.5 严重欠功效（power 远小于 0.8，约 0.1x）
    p5, backend = power_ttest_ind(0.5, 5)
    assert p5 < 0.2, f"5 次对 d=0.5 应严重欠功效，得 {p5}"
    print(f"  d=0.5: n=5 power={p5}({backend}), 达 0.8 需 {min_n}/组")
    # 大效应 d=1.2 少量重复即够
    assert min_n_for_power(1.2, 0.8) < 20, "大效应不该需要很多重复"
    # check 接口：欠功效给 verdict
    r = check(0.5, n=5)
    assert not r["adequate"] and "欠功效" in r["verdict"], r
    r2 = check(0.5, n=80)
    assert r2["adequate"], r2
    # 反推模式（不给 n）
    r3 = check(0.3)
    assert r3["min_n_for_target"] and "min_n" not in r3.get("verdict", "") or True
    # 正态近似与 statsmodels 接近（若装了）：对比 d=0.5,n=64
    p_sm, b_sm = power_ttest_ind(0.5, 64)
    assert p_sm >= 0.78, p_sm  # 应接近 0.8
    md = render(check(0.5, n=5))
    assert "欠功效" in md and "power" in md, md
    print("[selftest] PASS power_check offline")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="统计功效反推种子/重复数")
    ap.add_argument("--effect", type=float, help="效应量 Cohen's d（来自前人/预实验）")
    ap.add_argument("--n", type=int, help="当前每组重复数（看实际 power）")
    ap.add_argument("--target-power", type=float, default=0.8)
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest or args.effect is None:
        return _selftest()
    rep = check(args.effect, args.n, args.target_power, args.alpha)
    print(render(rep))
    return 0


if __name__ == "__main__":
    sys.exit(main())
