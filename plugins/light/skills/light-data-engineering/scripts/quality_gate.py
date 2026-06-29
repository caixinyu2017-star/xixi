"""quality_gate.py — validate a CSV against a YAML rule file. Pass/fail report.

Pure pandas + PyYAML. No heavy external dependency (no Great Expectations /
Frictionless needed) so it runs anywhere. Reproducible data gate for pipelines.

Rule file (YAML) shape:
    dataset:
      min_rows: 100
      max_rows: 1000000
      no_duplicate_rows: true
    columns:
      age:
        dtype: int          # int | float | numeric | string | bool | datetime
        required: true       # column must exist
        non_null: true       # no missing values
        min: 0
        max: 120
      status:
        enum: [active, churned, paused]
      email:
        regex: "^[^@]+@[^@]+\\.[^@]+$"
      user_id:
        unique: true

Exit code 0 = all pass, 1 = any failure (CI-friendly).

Usage:
    python quality_gate.py --csv data.csv --rules rules.yaml [--out report.md]
    python quality_gate.py --selftest
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
import argparse
import io
import re
import numpy as np
import pandas as pd
import yaml


def _is_dtype(series, want):
    s = series.dropna()
    if want == "numeric":
        return pd.api.types.is_numeric_dtype(series)
    if want == "int":
        if pd.api.types.is_integer_dtype(series):
            return True
        if pd.api.types.is_float_dtype(series):       # allow whole-valued floats
            return bool(np.all(np.equal(np.mod(s.values, 1), 0))) if len(s) else True
        return False
    if want == "float":
        return pd.api.types.is_float_dtype(series)
    if want == "bool":
        return pd.api.types.is_bool_dtype(series)
    if want == "datetime":
        if pd.api.types.is_datetime64_any_dtype(series):
            return True
        try:
            pd.to_datetime(s, errors="raise")
            return True
        except Exception:
            return False
    if want == "string":
        return pd.api.types.is_object_dtype(series) or \
            isinstance(series.dtype, pd.CategoricalDtype) or \
            pd.api.types.is_string_dtype(series)
    return True  # unknown type spec -> don't fail on it


def validate(df, rules):
    """Return (results, all_passed). Each result: dict(check, target, status, detail, severity).

    规则可带 severity: error(默认，FAIL 即一票否决退出码1) 或 warn(仅警示不影响退出码)。
    dataset 级用 rules['dataset']['severity']，列级用每列 spec 的 'severity'，未给则 error。
    """
    results = []

    def add(check, target, ok, detail="", severity="error"):
        results.append({"check": check, "target": target,
                        "status": "PASS" if ok else "FAIL", "detail": detail,
                        "severity": severity})
        return ok

    ds = rules.get("dataset", {}) or {}
    ds_sev = ds.get("severity", "error")
    n = len(df)
    if "min_rows" in ds:
        add("min_rows", "<dataset>", n >= ds["min_rows"],
            f"{n} rows (need >= {ds['min_rows']})", ds_sev)
    if "max_rows" in ds:
        add("max_rows", "<dataset>", n <= ds["max_rows"],
            f"{n} rows (need <= {ds['max_rows']})", ds_sev)
    if ds.get("no_duplicate_rows"):
        d = int(df.duplicated().sum())
        add("no_duplicate_rows", "<dataset>", d == 0, f"{d} duplicate rows", ds_sev)

    cols = rules.get("columns", {}) or {}
    for col, spec in cols.items():
        spec = spec or {}
        sev = spec.get("severity", "error")
        present = col in df.columns
        if spec.get("required"):
            add("required", col, present, "missing column" if not present else "present", sev)
        if not present:
            continue
        s = df[col]

        if "dtype" in spec:
            ok = _is_dtype(s, spec["dtype"])
            add("dtype", col, ok, f"want {spec['dtype']}, got {s.dtype}", sev)
        if spec.get("non_null"):
            nn = int(s.isna().sum())
            add("non_null", col, nn == 0, f"{nn} nulls", sev)
        if spec.get("unique"):
            dup = int(s.duplicated().sum())
            add("unique", col, dup == 0, f"{dup} duplicate values", sev)
        if "min" in spec:
            sv = pd.to_numeric(s, errors="coerce")
            bad = int((sv < spec["min"]).sum())
            add("min", col, bad == 0, f"{bad} values < {spec['min']}", sev)
        if "max" in spec:
            sv = pd.to_numeric(s, errors="coerce")
            bad = int((sv > spec["max"]).sum())
            add("max", col, bad == 0, f"{bad} values > {spec['max']}", sev)
        if "enum" in spec:
            allowed = set(spec["enum"])
            bad_vals = set(s.dropna().unique()) - allowed
            add("enum", col, len(bad_vals) == 0,
                f"unexpected: {sorted(map(str, bad_vals))[:10]}" if bad_vals else "ok", sev)
        if "regex" in spec:
            pat = re.compile(spec["regex"])
            # match_mode: search(默认,部分匹配) | fullmatch(整串匹配,email 等用此更严)
            mode = spec.get("regex_mode", "search")
            matcher = (pat.fullmatch if mode == "fullmatch" else pat.search)
            nonmatch = int(s.dropna().astype(str).apply(
                lambda v: matcher(v) is None).sum())
            add("regex", col, nonmatch == 0,
                f"{nonmatch} non-matching values (mode={mode})", sev)

    # 退出码只看 error 级失败；warn 级失败仅警示
    error_fails = [r for r in results if r["status"] == "FAIL" and r["severity"] == "error"]
    all_passed = len(error_fails) == 0
    return results, all_passed


def render(results, all_passed):
    L = ["# Data Quality Gate Report", ""]
    n_pass = sum(r["status"] == "PASS" for r in results)
    warn_fails = sum(1 for r in results if r["status"] == "FAIL" and r.get("severity") == "warn")
    err_fails = sum(1 for r in results if r["status"] == "FAIL" and r.get("severity", "error") == "error")
    L.append(f"**Result: {'PASS' if all_passed else 'FAIL'}**  "
             f"({n_pass}/{len(results)} checks passed; error-fails={err_fails}, warn-fails={warn_fails})")
    L.append("> 退出码只由 error 级失败决定；warn 级失败仅警示不阻断。")
    L.append("")
    L.append("| check | target | severity | status | detail |")
    L.append("| --- | --- | --- | --- | --- |")
    for r in results:
        sev = r.get("severity", "error")
        mark = "PASS" if r["status"] == "PASS" else ("**FAIL**" if sev == "error" else "_warn_")
        L.append(f"| {r['check']} | `{r['target']}` | {sev} | {mark} | {r['detail']} |")
    L.append("")
    return "\n".join(L)


SYNTH_RULES = {
    "dataset": {"min_rows": 5, "no_duplicate_rows": True},
    "columns": {
        "age": {"dtype": "int", "required": True, "non_null": True, "min": 0, "max": 120},
        "status": {"enum": ["active", "churned"]},
        "email": {"regex": r"^[^@]+@[^@]+\.[^@]+$"},
        "user_id": {"unique": True, "required": True},
        "missing_col": {"required": True},
    },
}


def make_synth_bad():
    return pd.DataFrame({
        "age": [25, 40, 200, -3, 33, 33],        # 200>max, -3<min
        "status": ["active", "churned", "frozen", "active", "active", "active"],  # frozen not in enum
        "email": ["a@b.com", "bad", "c@d.org", "e@f.io", "g@h.co", "g@h.co"],     # 'bad' fails regex
        "user_id": [1, 2, 3, 4, 5, 5],           # dup id
    })  # also: no 'missing_col', and row [33,active,g@h.co,5]... duplicates handled by id


def make_synth_good():
    return pd.DataFrame({
        "age": [25, 40, 30, 33, 50],
        "status": ["active", "churned", "active", "active", "churned"],
        "email": ["a@b.com", "c@d.org", "e@f.io", "g@h.co", "i@j.net"],
        "user_id": [1, 2, 3, 4, 5],
        "missing_col": [1, 2, 3, 4, 5],
    })


def main():
    ap = argparse.ArgumentParser(description="Validate CSV against YAML rules")
    ap.add_argument("--csv")
    ap.add_argument("--rules")
    ap.add_argument("--out")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        bad = make_synth_bad()
        res, ok = validate(bad, SYNTH_RULES)
        print(render(res, ok))
        fails = {(r["check"], r["target"]) for r in res if r["status"] == "FAIL"}
        for expected in [("max", "age"), ("min", "age"), ("enum", "status"),
                         ("regex", "email"), ("unique", "user_id"),
                         ("required", "missing_col")]:
            assert expected in fails, f"gate missed {expected}"
        assert not ok, "bad data should not pass"
        good, gok = make_synth_good(), None
        gres, gok = validate(make_synth_good(), SYNTH_RULES)
        assert gok, "clean data should pass: " + \
            str([r for r in gres if r["status"] == "FAIL"])

        # severity：warn 级失败不应翻总体（退出码只看 error 级）
        warn_rules = {"columns": {"age": {"max": 30, "severity": "warn"}}}  # 多数 age>30 会 fail 但 warn
        wres, wok = validate(make_synth_good(), warn_rules)
        assert any(r["status"] == "FAIL" and r["severity"] == "warn" for r in wres), wres
        assert wok is True, "warn 级失败不应让 all_passed 翻 False"
        # 同样的检查若是 error 级则应翻 False
        err_rules = {"columns": {"age": {"max": 30}}}  # 默认 error
        _, eok = validate(make_synth_good(), err_rules)
        assert eok is False, "error 级失败应让 all_passed=False"
        # regex_mode=fullmatch 比 search 更严：带尾随垃圾的串在 fullmatch 下应失败
        rmode = {"columns": {"email": {"regex": r"\S+@\S+\.\S+", "regex_mode": "fullmatch"}}}
        df_loose = pd.DataFrame({"email": ["a@b.com junk", "ok@x.io"]})
        rres, _ = validate(df_loose, rmode)
        assert any(r["check"] == "regex" and r["status"] == "FAIL" for r in rres), rres
        # 同串在 search 模式下会"放过"（部分匹配 ok@x.io 那段）→ 证明 fullmatch 更严
        rmode_s = {"columns": {"email": {"regex": r"\S+@\S+\.\S+", "regex_mode": "search"}}}
        rres_s, _ = validate(df_loose, rmode_s)
        assert all(r["status"] == "PASS" for r in rres_s if r["check"] == "regex"), rres_s

        print("[selftest] PASS — every rule fired on bad data; clean data passed; severity/fullmatch OK.")
        return

    if not (args.csv and args.rules):
        ap.error("provide --csv and --rules, or --selftest")
    df = pd.read_csv(args.csv)
    with io.open(args.rules, encoding="utf-8") as fh:
        rules = yaml.safe_load(fh)
    res, ok = validate(df, rules)
    report = render(res, ok)
    if args.out:
        with io.open(args.out, "w", encoding="utf-8") as fh:
            fh.write(report)
        print(f"Wrote report to {args.out}", file=sys.stderr)
    else:
        print(report)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
