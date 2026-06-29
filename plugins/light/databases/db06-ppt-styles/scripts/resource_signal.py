#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""resource_signal.py — db06 PPT 资源易变事实实时校验 (Light / db06 库重构)

db06 是「版式/叙事方法卡 + 薄事实缓存」库；资源表的 GitHub 星标 / 许可 / 链接存活
是会变的 B 事实，不当认证事实写死，本地存快照 + last_checked，真值由本脚本实时查、冲突信在线。

三类信号（复用 venue_signal/style_signal 的 urllib GET + 优雅降级 + mock selftest 范式）：
  1. GitHub 仓库星标 + 许可 ← GET https://api.github.com/repos/{owner}/{repo}
     取 .stargazers_count 与 .license.spdx_id
  2. PyPI 包许可 ← GET https://pypi.org/pypi/{pkg}/json 取 .info.license / classifiers
  3. 链接存活 ← GET 取 HTTP 状态码（403=反爬非失效，要标注；000/异常=降级）

诚实约定（与 venue_signal/style_signal 一致）：
- 查询失败 → status="unavailable"+reason，不编值、不崩。
- 许可是合规红线(metropolis=CC-BY-SA-4.0 必须可追溯)：本地存快照、冲突信在线并回写、无网回退快照标 stale。
- 星标是纯参考值：本地存快照值 + last_checked，冲突信在线。
- light-slides 多在无网/沙箱跑 python-pptx：默认可用本地快照(标 as-of)，不强制联网、不阻断出稿。
- GitHub 未认证 60 req/h，db06 仅 ~6 个开源仓单轮够用；更高频再标待核实限流。

用法：
    python scripts/resource_signal.py --github hakimel/reveal.js
    python scripts/resource_signal.py --pypi python-pptx
    python scripts/resource_signal.py --url https://gamma.app/ --cached-http 000
    python scripts/resource_signal.py --selftest
"""
from __future__ import annotations
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

TIMEOUT = 30
GH = "https://api.github.com"
PYPI = "https://pypi.org/pypi"


def http_fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "Light-resource-signal/1.0",
                                               "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8", "replace"))


def http_status(url: str) -> int:
    req = urllib.request.Request(url, headers={"User-Agent": "Light-resource-signal/1.0"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.getcode()


def signal_github(repo: str, cached_stars, cached_license, fetch) -> dict:
    """GitHub 仓库星标 + 许可实时查，冲突信在线。repo 形如 owner/name。"""
    if not repo or "/" not in repo:
        return {"status": "unavailable", "reason": "无 owner/repo"}
    try:
        data = fetch(f"{GH}/repos/{repo}")
        stars = data.get("stargazers_count")
        lic = (data.get("license") or {}).get("spdx_id")
        out = {"status": "ok", "repo": repo, "stars_live": stars, "license_live": lic,
               "stars_snapshot": cached_stars, "license_snapshot": cached_license,
               "source_pointer": f"{GH}/repos/{repo}", "source": "GitHub API(实时)，冲突信在线"}
        if cached_license and lic and cached_license != lic:
            out["license_conflict"] = (f"许可快照({cached_license}) ≠ 在线({lic})，"
                                       "合规红线、信在线、回写 + 刷新 last_checked")
        return out
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"status": "ok", "repo": repo, "alive": False, "http": 404,
                    "note": "仓库失效(404)，换镜像或标弃用"}
        return {"status": "unavailable", "reason": f"GitHub HTTP {e.code}",
                "stars_snapshot": cached_stars, "license_snapshot": cached_license}
    except Exception as e:  # noqa: BLE001
        return {"status": "unavailable", "reason": f"GitHub 失败:{e.__class__.__name__}",
                "stars_snapshot": cached_stars, "license_snapshot": cached_license,
                "note": "无网降级用快照，标 stale；合规以官方 LICENSE 为准"}


def signal_pypi(pkg: str, cached_license, fetch) -> dict:
    """PyPI 包许可实时查(.info.license 优先，回退 classifiers 的 License:: 项)。"""
    if not pkg:
        return {"status": "unavailable", "reason": "无 pypi 包名"}
    try:
        data = fetch(f"{PYPI}/{urllib.parse.quote(pkg)}/json")
        info = data.get("info") or {}
        lic = (info.get("license") or "").strip()
        if not lic:
            for c in info.get("classifiers", []):
                if c.startswith("License ::"):
                    lic = c.split("::")[-1].strip()
                    break
        if not lic:
            return {"status": "unavailable", "reason": "PyPI 无 license 字段",
                    "license_snapshot": cached_license, "note": "降级用快照，标待核查"}
        out = {"status": "ok", "pkg": pkg, "license_live": lic,
               "license_snapshot": cached_license,
               "source_pointer": f"{PYPI}/{pkg}/json", "source": "PyPI API(实时)，冲突信在线"}
        if cached_license and cached_license not in lic and lic not in cached_license:
            out["license_conflict"] = f"快照({cached_license}) ≠ 在线({lic})，信在线"
        return out
    except Exception as e:  # noqa: BLE001
        return {"status": "unavailable", "reason": f"PyPI 失败:{e.__class__.__name__}",
                "license_snapshot": cached_license, "note": "无网降级用快照，标 stale"}


def signal_url_alive(url: str, cached_http, fetch_status) -> dict:
    """链接存活探测；403=反爬非失效要标注。"""
    if not url:
        return {"status": "unavailable", "reason": "无 url"}
    try:
        code = fetch_status(url)
        return {"status": "ok", "url": url, "http": code, "alive": 200 <= code < 400,
                "http_snapshot": cached_http}
    except urllib.error.HTTPError as e:
        note = "403=反爬非失效，浏览器可访问" if e.code == 403 else f"HTTP {e.code}"
        return {"status": "ok", "url": url, "http": e.code, "alive": e.code == 403,
                "http_snapshot": cached_http, "note": note}
    except Exception as e:  # noqa: BLE001
        return {"status": "unavailable", "reason": f"探测失败:{e.__class__.__name__}",
                "http_snapshot": cached_http, "note": "无网降级，沿用月度复查"}


def assemble(repo, pypi, url, cached_stars, cached_license, cached_http,
             fetch_json, fetch_status) -> dict:
    sig = {}
    if repo:
        sig["github"] = signal_github(repo, cached_stars, cached_license, fetch_json)
    if pypi:
        sig["pypi"] = signal_pypi(pypi, cached_license, fetch_json)
    if url:
        sig["url_alive"] = signal_url_alive(url, cached_http, fetch_status)
    if not sig:
        sig["github"] = {"status": "unavailable", "reason": "未提供 --github/--pypi/--url"}
    return {"signals": sig,
            "freshness": {"note": "无网回退快照并标 stale；冲突默认信在线；"
                                  "许可为合规红线、以官方 LICENSE 为准；不强制联网、不阻断出稿"}}


class _MockJson:
    def __call__(self, url: str) -> dict:
        if "/repos/" in url:
            return {"stargazers_count": 72000, "license": {"spdx_id": "MIT"}}
        if "python-pptx" in url:
            return {"info": {"license": "MIT", "classifiers": ["License :: OSI Approved :: MIT License"]}}
        if "/nolic/json" in url:
            return {"info": {"license": "", "classifiers": []}}
        raise RuntimeError(f"mock 未覆盖:{url}")


class _MockStatus:
    def __call__(self, url: str) -> int:
        if "gamma" in url:
            raise urllib.error.URLError("connection blocked")  # 000 类
        if "canva" in url:
            raise urllib.error.HTTPError(url, 403, "Forbidden", {}, None)
        return 200


def _selftest() -> int:
    fj, fs = _MockJson(), _MockStatus()
    # GitHub 星标+许可，许可快照与在线一致
    r = signal_github("hakimel/reveal.js", 71600, "MIT", fj)
    assert r["status"] == "ok" and r["stars_live"] == 72000 and r["license_live"] == "MIT", r
    assert "license_conflict" not in r
    # 许可冲突(快照 Apache-2.0 ≠ 在线 MIT)→ 信在线 + 提示
    r2 = signal_github("x/y", 100, "Apache-2.0", fj)
    assert "license_conflict" in r2, r2
    # PyPI 许可
    p = signal_pypi("python-pptx", "MIT", fj)
    assert p["status"] == "ok" and p["license_live"] == "MIT", p
    # PyPI 无 license → 待核查不编
    p2 = signal_pypi("nolic", "BSD", fj)
    assert p2["status"] == "unavailable" and p2["license_snapshot"] == "BSD", p2
    # URL 403 反爬 → alive=True + 标注
    a = signal_url_alive("https://canva.com/", 403, fs)
    assert a["http"] == 403 and a["alive"] is True and "反爬" in a["note"], a
    # URL 000 连接拦截 → unavailable 降级
    a2 = signal_url_alive("https://gamma.app/", "000", fs)
    assert a2["status"] == "unavailable" and a2["http_snapshot"] == "000", a2
    # 无网 GitHub → 回退快照
    def boom(url):
        raise urllib.error.URLError("offline")
    r3 = signal_github("a/b", 500, "MIT", boom)
    assert r3["status"] == "unavailable" and r3["stars_snapshot"] == 500, r3
    # assemble 三信号
    rep = assemble("hakimel/reveal.js", "python-pptx", "https://canva.com/",
                   71600, "MIT", 403, fj, fs)
    assert rep["signals"]["github"]["status"] == "ok"
    assert rep["signals"]["pypi"]["license_live"] == "MIT"
    assert rep["signals"]["url_alive"]["http"] == 403
    print("[selftest] PASS resource_signal（GitHub星标+许可/PyPI许可/存活403/冲突信在线/无网降级/不编值）")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description="db06 PPT 资源 星标/许可/存活 实时校验")
    ap.add_argument("--github", default="", help="owner/repo")
    ap.add_argument("--pypi", default="", help="PyPI 包名")
    ap.add_argument("--url", default="", help="链接存活探测")
    ap.add_argument("--cached-stars", type=int, default=None)
    ap.add_argument("--cached-license", default="")
    ap.add_argument("--cached-http", default="")
    ap.add_argument("--json-out", default="")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        sys.exit(_selftest())
    if not args.github and not args.pypi and not args.url:
        ap.error("至少提供 --github/--pypi/--url 之一(或 --selftest)")
    report = assemble(args.github, args.pypi, args.url, args.cached_stars,
                      args.cached_license or None, args.cached_http or None,
                      http_fetch_json, http_status)
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.json_out:
        open(args.json_out, "w", encoding="utf-8").write(text)
    print(text)


if __name__ == "__main__":
    main()
