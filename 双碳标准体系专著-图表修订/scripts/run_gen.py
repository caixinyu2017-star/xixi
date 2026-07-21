# -*- coding: utf-8 -*-
"""批量调用 chedankj.com gpt-image-2 生成图片（curl 绕过 Cloudflare UA 过滤）。
用法: python3 run_gen.py [key1 key2 ...]   # 无参数=全部
输出: gen/out/<key>.png
"""
import json, os, subprocess, sys, base64, concurrent.futures as cf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figspec import FIGS

GEN = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(GEN, "out")
os.makedirs(OUT, exist_ok=True)
KEY = os.environ["CHEDANKJ_API_KEY"]

def gen_one(fig):
    k = fig["key"]
    req = {"model": "gpt-image-2", "prompt": fig["prompt"], "size": fig["size"], "n": 1}
    reqf = os.path.join(OUT, k + ".req.json")
    respf = os.path.join(OUT, k + ".resp.json")
    with open(reqf, "w") as f:
        json.dump(req, f, ensure_ascii=False)
    for attempt in range(3):
        r = subprocess.run([
            "curl", "-sS", "-m", "900", "-X", "POST",
            "https://chedankj.com/v1/images/generations",
            "-H", f"Authorization: Bearer {KEY}",
            "-H", "Content-Type: application/json",
            "--data", "@" + reqf, "-o", respf])
        if r.returncode != 0:
            continue
        try:
            resp = json.load(open(respf))
            b64 = resp["data"][0]["b64_json"]
            png = os.path.join(OUT, k + ".png")
            with open(png, "wb") as f:
                f.write(base64.b64decode(b64))
            return k, "OK", attempt
        except Exception as e:
            err = open(respf, errors="replace").read()[:200] if os.path.exists(respf) else str(e)
            print(f"[{k}] attempt {attempt}: {err}", flush=True)
    return k, "FAIL", 99

if __name__ == "__main__":
    keys = sys.argv[1:]
    figs = [f for f in FIGS if not keys or f["key"] in keys]
    print(f"generating {len(figs)} figures ...", flush=True)
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        for k, st, att in ex.map(gen_one, figs):
            print(k, st, f"(attempt {att})", flush=True)
    print("done")
