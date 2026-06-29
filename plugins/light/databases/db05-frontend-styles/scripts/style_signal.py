#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""style_signal.py — db05 前端工具易变事实实时校验 (Light / db05 库重构)

db05 是"视觉范式 + token SSOT"库；工具的 license/version/链接是会变的 B 事实，
不当认证事实写死，本地存快照 + last_checked，真值由本脚本实时查、冲突信在线。

两条信号（都复用 venue_signal.py 的 urllib GET + 优雅降级 + mock selftest 范式）：
  1. npm 系工具 license + 最新版本 ← https://registry.npmjs.org/<pkg>
     顶层 .license(SPDX) / .dist-tags.latest / .versions[latest].license
  2. 画廊 / SaaS / Figma / 定价层（无 license API）← 只做 HTTP 存活探测(状态码)
     + 存 source_pointer 指向官方 LICENSE/pricing 页；定价值不抓，标 待核查。

诚实约定（与 venue_signal/method_signal/paper_signal 一致）：
- 查询失败 → status="unavailable"+reason，不编值、不崩。
- 无网/查不到 → 返回本地 cached_license + 标 stale + last_checked + 提示"投产前以官方 LICENSE 为准"。
- 冲突默认信在线：在线 license 与缓存不一致时信在线，回写缓存 + 刷新 last_checked。
- Pro/定价层无开放 API → 不抓值，恒标 待核查 + source_pointer 指向官方 pricing 页。
- 本环境 WebFetch 被拦，脚本走 urllib(registry.npmjs.org 已实测可达)，不依赖 WebFetch。

用法：
    python scripts/style_signal.py --npm @radix-ui/react-dialog
    python scripts/style_signal.py --url https://www.awwwards.com/ --alive-only
    python scripts/style_signal.py --npm echarts --cached-license Apache-2.0
    python scripts/style_signal.py --selftest
"""
from __future__ import annotations
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

TIMEOUT = 30
NPM = "https://registry.npmjs.org"


def http_fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "Light-style-signal/1.0",
                                               "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8", "replace"))


def http_status(url: str) -> int:
    """GET 取 HTTP 状态码(存活探测)；网络异常抛出由调用方降级。"""
    req = urllib.request.Request(url, headers={"User-Agent": "Light-style-signal/1.0"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.getcode()


def _extract_license(data: dict):
    """从 npm registry JSON 抽 SPDX license：顶层 .license 优先，回退 latest 版本的 .license。"""
    lic = data.get("license")
    if isinstance(lic, dict):  # 旧式 {type, url}
        lic = lic.get("type")
    if not lic:
        latest = (data.get("dist-tags") or {}).get("latest")
        versions = data.get("versions") or {}
        if latest and latest in versions:
            vlic = versions[latest].get("license")
            lic = vlic.get("type") if isinstance(vlic, dict) else vlic
    return lic


def signal_npm(pkg: str, cached_license, fetch) -> dict:
    """npm 包 license + 最新版本实时查，冲突信在线。"""
    if not pkg:
        return {"status": "unavailable", "reason": "无 npm 包名"}
    try:
        data = fetch(f"{NPM}/{urllib.parse.quote(pkg, safe='@/')}")
        latest = (data.get("dist-tags") or {}).get("latest")
        live_license = _extract_license(data)
        if not live_license:
            return {"status": "unavailable", "reason": "registry 无 license 字段(非标准SPDX?)",
                    "cached_license": cached_license, "latest_version": latest,
                    "note": "降级用快照，标 待核查；投产前以官方 LICENSE 为准"}
        out = {"status": "ok", "pkg": pkg, "license_live": live_license,
               "latest_version": latest, "cached_license": cached_license,
               "source_pointer": f"{NPM}/{pkg}", "source": "registry.npmjs.org(实时)，冲突信在线"}
        if cached_license and cached_license != live_license:
            out["conflict"] = (f"快照({cached_license}) ≠ 在线({live_license})，"
                               "信在线、回写缓存 + 刷新 last_checked")
        return out
    except Exception as e:  # noqa: BLE001
        return {"status": "unavailable", "reason": f"registry 失败:{e.__class__.__name__}",
                "cached_license": cached_license,
                "note": "无网降级用快照，标 stale；投产前以官方 LICENSE 为准"}


def signal_url_alive(url: str, fetch_status) -> dict:
    """画廊/SaaS/Figma 链接存活探测(无 license API,只看状态码)。"""
    if not url:
        return {"status": "unavailable", "reason": "无 url"}
    try:
        code = fetch_status(url)
        return {"status": "ok", "url": url, "http": code, "alive": 200 <= code < 400,
                "note": "仅存活探测；license/定价以官方页为准(无 API,人工核)"}
    except urllib.error.HTTPError as e:
        return {"status": "ok", "url": url, "http": e.code, "alive": False,
                "note": f"HTTP {e.code}，可能失效或反爬，warn-only 不阻断"}
    except Exception as e:  # noqa: BLE001
        return {"status": "unavailable", "reason": f"探测失败:{e.__class__.__name__}",
                "note": "无网降级，沿用 check_freshness.py 月度复查"}


def assemble(pkg: str, url: str, cached_license, fetch_json, fetch_status) -> dict:
    sig = {}
    if pkg:
        sig["npm"] = signal_npm(pkg, cached_license, fetch_json)
    if url:
        sig["url_alive"] = signal_url_alive(url, fetch_status)
    if not sig:
        sig["npm"] = {"status": "unavailable", "reason": "未提供 --npm/--url"}
    return {
        "signals": sig,
        "freshness": {"note": "无网回退快照并标 stale；冲突默认信在线；"
                              "Pro/定价层无 API 恒标 待核查 指向官方 pricing 页"},
    }


class _MockJson:
    def __call__(self, url: str) -> dict:
        if "/echarts" in url:
            return {"license": "Apache-2.0", "dist-tags": {"latest": "5.5.0"},
                    "versions": {"5.5.0": {"license": "Apache-2.0"}}}
        if "react-dialog" in url:  # 顶层无 license，回退版本
            return {"dist-tags": {"latest": "1.1.1"},
                    "versions": {"1.1.1": {"license": "MIT"}}}
        if "/nolicense" in url:
            return {"dist-tags": {"latest": "0.1.0"}, "versions": {"0.1.0": {}}}
        raise RuntimeError(f"mock 未覆盖:{url}")


class _MockStatus:
    def __call__(self, url: str) -> int:
        if "dead" in url:
            raise urllib.error.HTTPError(url, 404, "Not Found", {}, None)
        return 200


def _selftest() -> int:
    fj, fs = _MockJson(), _MockStatus()
    # 顶层 license 命中 + 冲突信在线
    r = signal_npm("echarts", "MIT", fj)  # 快照 MIT 与在线 Apache-2.0 冲突
    assert r["status"] == "ok" and r["license_live"] == "Apache-2.0", r
    assert r["latest_version"] == "5.5.0"
    assert "conflict" in r, "应提示快照与在线冲突"
    # 顶层无 license → 回退 latest 版本 license
    r2 = signal_npm("@radix-ui/react-dialog", None, fj)
    assert r2["license_live"] == "MIT", r2
    # registry 有包但完全无 license → unavailable 标待核查，不编
    r3 = signal_npm("nolicense", "ISC", fj)
    assert r3["status"] == "unavailable" and r3["cached_license"] == "ISC", r3
    # URL 存活
    a = signal_url_alive("https://www.awwwards.com/", fs)
    assert a["status"] == "ok" and a["alive"] is True, a
    # URL 失效 404 → warn-only 不崩
    a2 = signal_url_alive("https://dead.example/", fs)
    assert a2["alive"] is False and a2["http"] == 404, a2
    # 无网降级留快照
    def boom_json(url):
        raise urllib.error.URLError("offline")
    r4 = signal_npm("echarts", "Apache-2.0", boom_json)
    assert r4["status"] == "unavailable" and r4["cached_license"] == "Apache-2.0", r4
    # assemble 双信号
    rep = assemble("echarts", "https://www.awwwards.com/", "Apache-2.0", fj, fs)
    assert rep["signals"]["npm"]["status"] == "ok"
    assert rep["signals"]["url_alive"]["alive"] is True
    print("[selftest] PASS style_signal（npm license+版本/回退/冲突信在线/存活探测/无网降级/不编值）")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description="db05 前端工具 license/版本/存活实时校验")
    ap.add_argument("--npm", default="", help="npm 包名(查 license + 最新版本)")
    ap.add_argument("--url", default="", help="画廊/SaaS 链接(存活探测)")
    ap.add_argument("--cached-license", default="", help="本地快照 license(冲突时对比)")
    ap.add_argument("--alive-only", action="store_true", help="仅 URL 存活探测")
    ap.add_argument("--json-out", default="")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        sys.exit(_selftest())
    if not args.npm and not args.url:
        ap.error("至少提供 --npm 或 --url 之一(或 --selftest)")
    report = assemble(args.npm if not args.alive_only else "", args.url,
                      args.cached_license or None, http_fetch_json, http_status)
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.json_out:
        open(args.json_out, "w", encoding="utf-8").write(text)
    print(text)


if __name__ == "__main__":
    main()
