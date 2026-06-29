"""explain_shap.py - SHAP model interpretability with publication-grade export (Light m06).

Fills the one capability the skill names in its checklist ("可解释性证据: SHAP
beeswarm/bar/waterfall") but had no script for. Computes Shapley values and exports
three figures at dpi=300 (PDF/SVG/PNG), reusing make_figs' house style:
  * beeswarm - global feature effect + direction (per-sample dots, colored by value)
  * bar      - mean(|SHAP|) global importance ranking
  * waterfall- single-sample additive decomposition (base value -> prediction)

Explainer dispatch (fast path first, model-agnostic fallback last):
  1. shap.TreeExplainer   - explicit fast path for tree ensembles (RF/GBM/XGB/LGBM)
  2. shap.Explainer       - unified entry; auto-picks Tree/Linear/etc. for the model
  3. shap.KernelExplainer - model-agnostic fallback; background set is SUBSAMPLED
     (shap.sample, ~100 rows) because it is expensive (see caveat 3 below).

shap is an OPTIONAL dependency: if it is not importable the script degrades
gracefully (prints a skip notice, exits 0) exactly like leakage_overfit_check.py
does for deepchecks. It is never a hard requirement.

Usage as library: from explain_shap import explain; explain(model, X, outdir=...).
Run standalone:  python explain_shap.py
  -> synthetic make_classification + RandomForest self-test; writes 3 figures if
     shap is installed, else prints a skip notice and exits cleanly.

Three caveats baked into how this is used (do not ignore them):
  1. Correlated features DILUTE attribution: Shapley credit is split across mutually
     correlated features, so an important feature can look weak if a proxy co-varies
     with it. Read importances together with the correlation matrix, not in isolation.
  2. SHAP is NOT causal: values explain what THE MODEL relies on, not real-world cause.
     "Feature pushes prediction up" != "feature causes the outcome." Never cite SHAP
     as causal evidence.
  3. KernelExplainer is EXPENSIVE: roughly O(n_samples * n_background * 2^...-approx)
     model calls. Always subsample the background (shap.sample / shap.kmeans, ~100
     rows here) and explain a modest slice of rows, or runtime explodes.
"""
import os
import sys

import numpy as np

import matplotlib
matplotlib.use("Agg")  # headless-safe, must precede pyplot import
import matplotlib.pyplot as plt

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# Reuse make_figs' house style (viridis, constrained_layout, dpi300, save_all).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from make_figs import save_all  # noqa: E402  (applies rcParams house style on import)
except Exception:  # pragma: no cover - make_figs always ships beside this file
    def save_all(fig, path_noext, formats=("png", "pdf", "svg")):
        out = []
        for fmt in formats:
            p = f"{path_noext}.{fmt}"
            fig.savefig(p, dpi=300, bbox_inches="tight")
            out.append(p)
        return out


def _shap_available():
    """True iff shap is importable. Optional dependency, mirrors deepchecks handling."""
    try:
        import shap  # noqa: F401
        return True
    except Exception:
        return False


def _build_explainer(model, X, background_size=100, seed=0):
    """Pick a SHAP explainer: TreeExplainer fast path -> Explainer auto -> Kernel fallback.

    Returns (explainer, kind). The background set for the model-agnostic fallback is
    SUBSAMPLED to `background_size` rows (shap.sample, kmeans if available) because
    KernelExplainer cost scales with background size (caveat 3 in the module docstring).
    """
    import shap
    X = np.asarray(X, float) if not hasattr(X, "iloc") else X

    # 1) explicit fast path for tree ensembles
    try:
        expl = shap.TreeExplainer(model)
        return expl, "TreeExplainer"
    except Exception:
        pass

    # 2) unified entry: shap.Explainer auto-selects Tree/Linear/etc.
    try:
        expl = shap.Explainer(model, X)
        return expl, "Explainer(auto)"
    except Exception:
        pass

    # 3) model-agnostic fallback (expensive) -> subsample background
    n = X.shape[0]
    bg_n = min(background_size, n)
    try:
        background = shap.kmeans(X, min(bg_n, 50))
    except Exception:
        background = shap.sample(X, bg_n, random_state=seed)
    predict = getattr(model, "predict_proba", None) or model.predict
    expl = shap.KernelExplainer(predict, background)
    return expl, "KernelExplainer(fallback)"


def _shap_values(explainer, X, kind):
    """Compute SHAP values. Returns a modern shap.Explanation when possible.

    Newer shap (callable explainers) return an Explanation; KernelExplainer returns
    a raw array (or list per class). We normalize to a single-output Explanation so
    the plot helpers below stay simple.
    """
    import shap

    # Callable API (shap.Explainer / TreeExplainer in recent versions)
    try:
        exp = explainer(X)
        return _select_class(exp)
    except Exception:
        pass

    # Legacy KernelExplainer.shap_values -> wrap into an Explanation
    raw = explainer.shap_values(X)
    base = getattr(explainer, "expected_value", 0.0)
    if isinstance(raw, list):  # one array per class -> take last (positive) class
        vals = np.asarray(raw[-1])
        base = np.asarray(base)[-1] if np.ndim(base) else base
    else:
        vals = np.asarray(raw)
    feat = X.values if hasattr(X, "values") else np.asarray(X)
    names = list(X.columns) if hasattr(X, "columns") else None
    return shap.Explanation(values=vals, base_values=base, data=feat, feature_names=names)


def _select_class(exp):
    """If an Explanation carries a class axis (..., n_classes), keep the last class."""
    try:
        if exp.values.ndim == 3:
            return exp[..., -1]
    except Exception:
        pass
    return exp


def _save_shap_plot(plot_fn, path_noext):
    """The SHAP export trap, handled once.

    SHAP plot functions draw onto the current pyplot figure and (by default) call
    plt.show(), which discards the figure under a headless Agg backend. So: call with
    show=False, grab plt.gcf(), then save it ourselves via make_figs.save_all at
    dpi=300 / bbox_inches='tight' to PDF+SVG+PNG. Always close to avoid leaking figs.
    """
    plt.close("all")
    plot_fn()                 # plot_fn must pass show=False internally
    fig = plt.gcf()
    paths = save_all(fig, path_noext)
    plt.close(fig)
    return paths


def explain(model, X, outdir=None, prefix="shap", sample_idx=0,
            max_display=12, background_size=100, seed=0):
    """Compute SHAP values for `model` on `X` and export beeswarm + bar + waterfall.

    Returns a dict with the chosen explainer kind and the written figure paths, or a
    skip record if shap is not installed. Never raises on a missing shap.
    """
    if not _shap_available():
        msg = ("shap not installed -> skipping SHAP interpretability "
               "(optional dependency; pip install shap to enable). No figures written.")
        print(f"[skip] {msg}")
        return {"available": False, "skipped": True, "note": msg, "figures": []}

    import shap
    outdir = outdir or os.path.dirname(os.path.abspath(__file__))
    os.makedirs(outdir, exist_ok=True)

    explainer, kind = _build_explainer(model, X, background_size=background_size, seed=seed)
    exp = _shap_values(explainer, X, kind)
    figures = {}
    figures["beeswarm"] = _save_shap_plot(
        lambda: shap.plots.beeswarm(exp, max_display=max_display, show=False),
        os.path.join(outdir, f"{prefix}_beeswarm"))
    figures["bar"] = _save_shap_plot(
        lambda: shap.plots.bar(exp, max_display=max_display, show=False),
        os.path.join(outdir, f"{prefix}_bar"))
    figures["waterfall"] = _save_shap_plot(
        lambda: shap.plots.waterfall(exp[sample_idx], max_display=max_display, show=False),
        os.path.join(outdir, f"{prefix}_waterfall"))
    return {"available": True, "skipped": False, "explainer": kind,
            "n_samples": int(exp.values.shape[0]), "figures": figures}


def _synth_model(seed=0):
    """Synthetic classification data + a fitted RandomForest (the TreeExplainer path)."""
    import pandas as pd
    from sklearn.datasets import make_classification
    from sklearn.ensemble import RandomForestClassifier
    X, y = make_classification(n_samples=300, n_features=8, n_informative=4,
                               n_redundant=2, random_state=seed)
    cols = [f"f{i}" for i in range(X.shape[1])]
    Xdf = pd.DataFrame(X, columns=cols)
    model = RandomForestClassifier(n_estimators=80, random_state=seed).fit(Xdf, y)
    return model, Xdf



def _selftest() -> int:
    import tempfile
    with tempfile.TemporaryDirectory(prefix="light_explain_shap_") as tmp:
        if not _shap_available():
            res = explain(None, None, outdir=tmp)
            assert res["skipped"] is True and res["available"] is False, res
        else:
            model, X = _synth_model(seed=1)
            res = explain(model, X.iloc[:30], outdir=tmp, prefix="selftest_shap", max_display=6)
            assert res["available"] is True and res["figures"], res
            for paths in res["figures"].values():
                for path in paths:
                    assert os.path.exists(path) and os.path.getsize(path) > 0, path
    print("[selftest] PASS explain_shap")
    return 0


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] != "--selftest":
            raise SystemExit("usage: python explain_shap.py [--selftest]")
        raise SystemExit(_selftest())
    here = os.path.dirname(os.path.abspath(__file__))
    if not _shap_available():
        explain(None, None, outdir=here)  # prints the skip notice, returns cleanly
        print("DONE (shap absent: degraded gracefully, no figures expected)")
        return

    print("[demo] synthetic make_classification + RandomForest -> SHAP")
    model, X = _synth_model()
    # explain a modest slice to keep any KernelExplainer fallback cheap (caveat 3)
    res = explain(model, X.iloc[:100], outdir=here, prefix="demo_shap")
    print(f"explainer: {res['explainer']}  (n_samples={res['n_samples']})")
    for name, paths in res["figures"].items():
        for p in paths:
            print(f"  wrote [{name}] {p}")
    print("DONE")


if __name__ == "__main__":
    main()
