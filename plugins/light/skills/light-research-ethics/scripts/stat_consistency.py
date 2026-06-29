#!/usr/bin/env python3
"""Statistical consistency quick-checks for fabrication screening
(light-research-ethics asset, stdlib only).

Covers two high-frequency integrity signals:

1. GRIM / granularity test (Brown & Heathers 2017):
   For an integer sample size n and a reported mean M of integer-valued items,
   the mean can only land on the grid {k/n : k integer}. If no integer k rounds
   to the reported M at its stated decimal places, the mean is *impossible* given
   n -> 🛑 (likely typo, wrong n, or fabrication). Also flags reported decimal
   precision that exceeds what n can resolve (granularity = step/n).

2. p-value vs degrees-of-freedom consistency:
   Recompute the two-tailed p-value implied by a reported t (with df) or the
   upper-tail p implied by a reported F (with df1, df2) using a pure-stdlib
   regularized incomplete beta function, and compare to the reported p. A gross
   mismatch (orders of magnitude, or sign/threshold disagreement) is flagged as a
   signal that the test statistic and its df / p do not cohere.

HONEST LIMITS:
- GRIM/granularity only applies to means of INTEGER items (Likert counts, item
  sums, whole-number tallies). It is meaningless for continuous measurements.
- The p-value check is a magnitude sanity check, not an exact replication of the
  authors' software; rounding of the reported statistic/p is expected. Only a
  GROSS discrepancy is flagged. A flag is a "needs human review" signal, never a
  verdict of misconduct.

Usage:
    python stat_consistency.py grim --n 28 --mean 3.45
    python stat_consistency.py grim --n 28 --mean 3.45 --items 2
    python stat_consistency.py pcheck --t 2.10 --df 25 --p 0.045
    python stat_consistency.py pcheck --F 4.50 --df1 2 --df2 40 --p 0.017
    python stat_consistency.py --selftest
    python stat_consistency.py grim --n 28 --mean 3.45 --json
"""
import sys
import math
import json
import argparse

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")


# --------------------------------------------------------------------------
# Regularized incomplete beta function I_x(a,b)  (Numerical Recipes betai)
# Pure stdlib; used for t- and F-distribution tail probabilities.
# --------------------------------------------------------------------------
def _betacf(a, b, x):
    """Continued fraction for the incomplete beta function (Lentz's method)."""
    MAXIT = 300
    EPS = 3.0e-12
    FPMIN = 1.0e-300
    qab = a + b
    qap = a + 1.0
    qam = a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < FPMIN:
        d = FPMIN
    d = 1.0 / d
    h = d
    for m in range(1, MAXIT + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN:
            d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN:
            c = FPMIN
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN:
            d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN:
            c = FPMIN
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < EPS:
            break
    return h


def betai(a, b, x):
    """Regularized incomplete beta function I_x(a, b), 0 <= x <= 1."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    lbeta = (math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
             + a * math.log(x) + b * math.log(1.0 - x))
    front = math.exp(lbeta)
    if x < (a + 1.0) / (a + b + 2.0):
        return front * _betacf(a, b, x) / a
    return 1.0 - front * _betacf(b, a, 1.0 - x) / b


def t_two_tailed_p(t, df):
    """Two-tailed p-value for Student's t statistic with df degrees of freedom."""
    if df <= 0:
        raise ValueError("df must be > 0")
    t = abs(float(t))
    x = df / (df + t * t)
    return betai(df / 2.0, 0.5, x)


def f_upper_p(f, df1, df2):
    """Upper-tail p-value P(F > f) for an F statistic with (df1, df2)."""
    if df1 <= 0 or df2 <= 0:
        raise ValueError("df1 and df2 must be > 0")
    f = float(f)
    if f <= 0:
        return 1.0
    x = df2 / (df2 + df1 * f)
    return betai(df2 / 2.0, df1 / 2.0, x)


# --------------------------------------------------------------------------
# GRIM / granularity test
# --------------------------------------------------------------------------
def _reported_decimals(mean_str):
    """Number of decimal places in the reported mean string (e.g. '3.45' -> 2)."""
    s = str(mean_str).strip()
    if "." not in s:
        return 0
    return len(s.split(".", 1)[1])


def grim_check(n, mean_str, items=1):
    """GRIM test for a mean of integer-valued items.

    n      : integer sample size (per reported group)
    mean_str: the reported mean, AS A STRING, to preserve decimal places
    items  : number of integer items summed into each score (default 1).
             The mean grid step is 1/(n*items).

    Returns a dict with consistent (bool) + diagnostics. A mean is GRIM-consistent
    if some integer total T yields T/(n*items) that rounds to the reported mean at
    its reported decimal precision.
    """
    n = int(n)
    items = int(items)
    if n <= 0 or items <= 0:
        raise ValueError("n and items must be positive integers")
    reported = float(mean_str)
    decimals = _reported_decimals(mean_str)
    grid = n * items  # number of possible distinct sums per unit step
    # Candidate integer total nearest to reported*grid, plus neighbours.
    approx_total = reported * grid
    consistent = False
    best = None
    for t in (math.floor(approx_total) - 1, math.floor(approx_total),
              math.ceil(approx_total), math.ceil(approx_total) + 1):
        if t < 0:
            continue
        candidate = t / grid
        rounded = round(candidate, decimals)
        if best is None or abs(candidate - reported) < abs(best[1] - reported):
            best = (t, candidate, rounded)
        if abs(rounded - reported) < 10 ** (-(decimals + 6)):
            consistent = True
    # Granularity: smallest distinguishable step in the mean.
    granularity = 1.0 / grid
    # If reported precision is finer than granularity can ever resolve, the
    # extra digits are not meaningful (soft warning, not impossible by itself).
    over_precise = (10 ** (-decimals)) < granularity / 2.0
    return {
        "test": "grim",
        "n": n,
        "items": items,
        "reported_mean": reported,
        "decimals": decimals,
        "grid_step": granularity,
        "nearest_total": best[0] if best else None,
        "nearest_possible_mean": round(best[1], decimals + 4) if best else None,
        "consistent": consistent,
        "over_precise": over_precise,
        "status": "CONSISTENT" if consistent else "IMPOSSIBLE",
    }


# --------------------------------------------------------------------------
# p-value vs df consistency
# --------------------------------------------------------------------------
def pcheck(reported_p, t=None, df=None, F=None, df1=None, df2=None,
           gross_ratio=3.0):
    """Compare a reported p-value with the p implied by the reported statistic.

    Provide either (t, df) or (F, df1, df2). gross_ratio: factor beyond which the
    reported and recomputed p are deemed grossly inconsistent (default 3x).
    """
    if t is not None and df is not None:
        computed = t_two_tailed_p(t, df)
        stat_desc = "t=%g, df=%g (two-tailed)" % (float(t), float(df))
    elif F is not None and df1 is not None and df2 is not None:
        computed = f_upper_p(F, df1, df2)
        stat_desc = "F=%g, df1=%g, df2=%g (upper tail)" % (
            float(F), float(df1), float(df2))
    else:
        raise ValueError("provide (t, df) or (F, df1, df2)")
    reported_p = float(reported_p)
    # Compare on a ratio basis, guarding tiny values.
    lo = min(reported_p, computed)
    hi = max(reported_p, computed)
    ratio = (hi / lo) if lo > 1e-12 else float("inf")
    # Threshold disagreement: do they fall on the same side of .05 / .01?
    crosses = []
    for thr in (0.05, 0.01, 0.001):
        if (reported_p <= thr) != (computed <= thr):
            crosses.append(thr)
    gross = ratio > gross_ratio or bool(crosses)
    return {
        "test": "pcheck",
        "statistic": stat_desc,
        "reported_p": reported_p,
        "computed_p": computed,
        "ratio": ratio,
        "significance_crosses": crosses,
        "consistent": not gross,
        "status": "MISMATCH" if gross else "CONSISTENT",
    }


# --------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------
def _emit(result, as_json):
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    if result["test"] == "grim":
        icon = "✅" if result["consistent"] else "🛑"
        print("%s GRIM %s" % (icon, result["status"]))
        print("   n=%d  items=%d  reported mean=%s  (%d dp)"
              % (result["n"], result["items"], result["reported_mean"],
                 result["decimals"]))
        print("   grid step = 1/(n*items) = %.6g" % result["grid_step"])
        print("   nearest possible mean = %s (from integer total %s)"
              % (result["nearest_possible_mean"], result["nearest_total"]))
        if not result["consistent"]:
            print("   -> reported mean is IMPOSSIBLE for this n: no integer sum")
            print("      of integer items divides to it. Check n, the mean, or")
            print("      whether items are truly integer-valued. ⚠ human review.")
        if result["over_precise"]:
            print("   ⚠ reported decimals are finer than n can resolve "
                  "(over-precise).")
    else:
        icon = "✅" if result["consistent"] else "🛑"
        print("%s p-value %s" % (icon, result["status"]))
        print("   %s" % result["statistic"])
        print("   reported p = %.6g   recomputed p = %.6g"
              % (result["reported_p"], result["computed_p"]))
        print("   ratio = %.3g" % result["ratio"])
        if result["significance_crosses"]:
            print("   -> reported & recomputed p fall on OPPOSITE sides of: %s"
                  % ", ".join(str(t) for t in result["significance_crosses"]))
        if not result["consistent"]:
            print("   -> statistic, df and p do not cohere. ⚠ magnitude sanity")
            print("      check only (rounding expected); confirm with the paper's")
            print("      exact values before any conclusion.")


# --------------------------------------------------------------------------
# Self-test (offline, no I/O, no residue)
# --------------------------------------------------------------------------
def _selftest():
    fails = []

    # betai is a CDF building block: I_0=0, I_1=1, symmetry I_x(a,b)=1-I_{1-x}(b,a)
    assert abs(betai(2, 3, 0.0) - 0.0) < 1e-12
    assert abs(betai(2, 3, 1.0) - 1.0) < 1e-12
    assert abs(betai(2.5, 1.5, 0.4) - (1 - betai(1.5, 2.5, 0.6))) < 1e-9

    # t with large df approximates the normal: |t|=1.96 two-tailed ~ 0.05
    p = t_two_tailed_p(1.96, 100000)
    assert abs(p - 0.05) < 2e-3, "t->normal tail wrong: %r" % p
    # t=0 -> p=1
    assert abs(t_two_tailed_p(0.0, 10) - 1.0) < 1e-9

    # Known F relation: P(F>f) with df1=1 equals two-tailed t with sqrt(f).
    f, df2 = 4.0, 30
    assert abs(f_upper_p(f, 1, df2) - t_two_tailed_p(math.sqrt(f), df2)) < 1e-7

    # GRIM impossible case: classic example, n=28 mean 3.45 (1-item Likert)
    # is NOT achievable; nearest grid means are 96/28=3.428.., 97/28=3.464..
    r = grim_check(28, "3.45")
    assert not r["consistent"], "n=28 mean 3.45 should be GRIM-impossible"
    assert r["status"] == "IMPOSSIBLE"

    # GRIM consistent case: 97/28 = 3.4642857 rounds to 3.46.
    r2 = grim_check(28, "3.46")
    assert r2["consistent"], "n=28 mean 3.46 should be GRIM-consistent"

    # Whole-number mean is always consistent (total = mean*n is integer).
    assert grim_check(40, "3")["consistent"]

    # Larger n makes more means reachable: n=100 mean 3.45 is fine.
    assert grim_check(100, "3.45")["consistent"]

    # items>1 widens the grid: n=28, 2 items -> step 1/56, 3.45 now reachable.
    assert grim_check(28, "3.45", items=2)["consistent"]

    # pcheck consistent: t=2.10, df=25 gives p ~ 0.046, reported 0.045 -> OK.
    pc = pcheck(0.045, t=2.10, df=25)
    assert pc["consistent"], "t=2.10/df=25/p=.045 should cohere: %r" % pc

    # pcheck mismatch: t=2.10, df=25 cannot give p=0.0001 (off by orders).
    pc2 = pcheck(0.0001, t=2.10, df=25)
    assert not pc2["consistent"], "gross p mismatch should flag"

    # pcheck threshold crossing: real p>.05 but reported as significant.
    pc3 = pcheck(0.04, t=1.50, df=20)  # true two-tailed p ~ 0.149
    assert not pc3["consistent"] and 0.05 in pc3["significance_crosses"]

    # F pcheck consistent: F=4.50, df1=2, df2=40 -> p ~ 0.017.
    pc4 = pcheck(0.017, F=4.50, df1=2, df2=40)
    assert pc4["consistent"], "F=4.50 path should cohere: %r" % pc4

    print("[selftest] betai/t/F tail functions PASS")
    print("[selftest] GRIM impossible(n=28,3.45) & consistent(3.46) PASS")
    print("[selftest] GRIM items>1 widening & large-n PASS")
    print("[selftest] pcheck cohere / gross-ratio / threshold-cross / F PASS")
    print("[selftest] all assertions PASS")
    return 0 if not fails else 1


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(
        description="Statistical consistency quick-checks (GRIM + p/df), stdlib only")
    ap.add_argument("--selftest", action="store_true", help="offline self-test")
    sub = ap.add_subparsers(dest="cmd")

    g = sub.add_parser("grim", help="GRIM / granularity test on a reported mean")
    g.add_argument("--n", required=True, type=int, help="integer sample size")
    g.add_argument("--mean", required=True,
                   help="reported mean AS WRITTEN (keep decimals, e.g. 3.45)")
    g.add_argument("--items", type=int, default=1,
                   help="number of integer items summed per score (default 1)")
    g.add_argument("--json", action="store_true")

    p = sub.add_parser("pcheck", help="p-value vs df consistency")
    p.add_argument("--p", required=True, type=float, help="reported p-value")
    p.add_argument("--t", type=float, help="reported t statistic")
    p.add_argument("--df", type=float, help="df for t")
    p.add_argument("--F", type=float, help="reported F statistic")
    p.add_argument("--df1", type=float, help="numerator df for F")
    p.add_argument("--df2", type=float, help="denominator df for F")
    p.add_argument("--gross-ratio", type=float, default=3.0,
                   help="ratio beyond which p is deemed grossly inconsistent")
    p.add_argument("--json", action="store_true")

    args = ap.parse_args()
    if args.selftest:
        return _selftest()
    if args.cmd == "grim":
        return _emit(grim_check(args.n, args.mean, args.items), args.json)
    if args.cmd == "pcheck":
        if args.t is not None and args.df is not None:
            res = pcheck(args.p, t=args.t, df=args.df, gross_ratio=args.gross_ratio)
        elif args.F is not None and args.df1 is not None and args.df2 is not None:
            res = pcheck(args.p, F=args.F, df1=args.df1, df2=args.df2,
                         gross_ratio=args.gross_ratio)
        else:
            p.error("provide either --t and --df, or --F, --df1 and --df2")
        return _emit(res, args.json)
    ap.error("choose a subcommand: grim | pcheck  (or --selftest)")


if __name__ == "__main__":
    sys.exit(main())
