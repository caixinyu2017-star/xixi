"""Recompute only the extraction-noise sweep and patch summary.json.

The resampling noise channel and the extended eta grid affect no other
part of the experimental programme (extraction_noise is only invoked
for eta > 0), so the remaining entries of summary.json stay valid.
"""
import json
import os
import time

import numpy as np

import run_all as R

T0 = time.time()
TAB = R.TAB
with open(os.path.join(TAB, "summary.json"), encoding="utf-8") as fh:
    S = json.load(fh)

noise = []
for eta in R.ETAS:
    vals = {k: [] for k in ("RAMT", "MLP-Acc", "Logit-Acc+DA", "FCFS")}
    for s in range(1, 7):
        r = R.one_seed(s, eta=eta)
        for k in vals:
            vals[k].append(r["metrics"][k]["yield100"])
    noise.append(dict(
        eta=eta,
        ramt=float(np.mean(vals["RAMT"])),
        ramt_sd=float(np.std(vals["RAMT"])),
        mlp=float(np.mean(vals["MLP-Acc"])),
        mlp_sd=float(np.std(vals["MLP-Acc"])),
        logit=float(np.mean(vals["Logit-Acc+DA"])),
        logit_sd=float(np.std(vals["Logit-Acc+DA"])),
        fcfs=float(np.mean(vals["FCFS"])),
        fcfs_sd=float(np.std(vals["FCFS"]))))
    print("[%7.1fs] eta %.1f: RAMT %.2f MLP %.2f Logit %.2f FCFS %.2f"
          % (time.time() - T0, eta, noise[-1]["ramt"], noise[-1]["mlp"],
             noise[-1]["logit"], noise[-1]["fcfs"]), flush=True)

S["noise"] = noise
S["meta"]["etas"] = R.ETAS
S["meta"]["runtime_s"] = float(S["meta"]["runtime_s"]) + round(
    time.time() - T0, 1)
with open(os.path.join(TAB, "summary.json"), "w", encoding="utf-8") as fh:
    json.dump(S, fh, indent=1, default=float)
print("summary.json patched in %.1f s" % (time.time() - T0))
