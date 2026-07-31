#!/usr/bin/env python3
"""Generate all framework diagrams via the gpt-image-2 endpoint, in parallel."""
import base64
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import requests

API = "https://chedankj.com/v1/images/generations"
KEY = os.environ["CHEDANKJ_API_KEY"]
OUT = sys.argv[2] if len(sys.argv) > 2 else "images"
os.makedirs(OUT, exist_ok=True)

with open(sys.argv[1], encoding="utf-8") as fh:
    specs = json.load(fh)

only = set(sys.argv[3].split(",")) if len(sys.argv) > 3 else None


def run(spec):
    name = spec["name"]
    if only and name not in only:
        return name, "skipped"
    dest = os.path.join(OUT, name + ".png")
    for attempt in range(1, 4):
        try:
            r = requests.post(
                API,
                headers={"Authorization": f"Bearer {KEY}",
                         "Content-Type": "application/json"},
                json={"model": "gpt-image-2",
                      "prompt": spec["prompt"],
                      "size": spec.get("size", "1536x1024")},
                timeout=600,
            )
            if r.status_code != 200:
                raise RuntimeError(f"HTTP {r.status_code}: {r.text[:200]}")
            payload = r.json()["data"][0]
            if "b64_json" in payload:
                blob = base64.b64decode(payload["b64_json"])
            else:
                blob = requests.get(payload["url"], timeout=300).content
            with open(dest, "wb") as fh:
                fh.write(blob)
            return name, f"ok {len(blob)//1024}KB (attempt {attempt})"
        except Exception as exc:  # noqa: BLE001
            if attempt == 3:
                return name, f"FAILED {exc}"
            time.sleep(4 * attempt)
    return name, "FAILED"


with ThreadPoolExecutor(max_workers=5) as pool:
    for name, status in pool.map(run, specs):
        print(f"{name}: {status}", flush=True)
print("DONE", flush=True)
