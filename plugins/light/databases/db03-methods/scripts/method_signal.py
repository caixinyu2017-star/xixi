#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""method_signal.py — db03 方法卡易变字段实时校验 (Light / db03 库重构)

读 db03 卡 representative_papers 的内联锚点(doi:/cited:/checked:)与 implementation_repo，
实时校验易变字段，对比本地快照产 diff：
  1. 被引数      ← OpenAlex /works/doi:{DOI} cited_by_count（representative_papers 的 doi: 锚点）
  2. 仓库存活    ← GitHub /repos/{org}/{repo} HTTP 状态（implementation_repo 的 org/repo）

与 venue_signal.py / dataset_signal.py 同构（母本），诚实约定一致：
- 礼貌池邮箱经 --mailto 或环境变量 OPENALEX_MAILTO；不传匿名查(不伪造邮箱)。
- OpenAlex key/限流口径见 m01 references「OpenAlex 接入真相源」，本脚本不复写数字。
- 任一信号失败 → status="unavailable"+reason，不编数、不崩。
- 无网/无 key → 返回本地 cited 快照 + stale 警告(标 checked 距今)，不阻断下游(G3)。
- 冲突默认信在线；若在线 vs 快照差异>50% 提示可能是 OpenAlex 记录合并/拆分，标注供人工核
  (db03 已知 arXiv vs 正式版被引分散问题)。
- GitHub 未鉴权 60 req/h，176 卡全量刷需分批或 token；本脚本单卡查，批量由调用方控速。

用法：
    python scripts/method_signal.py --doi 10.1109/cvpr.2016.90 --mailto you@x.edu
    python scripts/method_signal.py --repo facebookresearch/maml
    python scripts/method_signal.py --rp-line "ResNet | 2016 | cited:221133 | doi:10.1109/cvpr.2016.90 | checked:2026-06-06"
    python scripts/method_signal.py --selftest
"""
from __future__ import annotations
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_MAILTO = os.environ.get("OPENALEX_MAILTO", "").strip()
TIMEOUT = 30
OA = "https://api.openalex.org"
GH = "https://api.github.com"
_MAILTO = DEFAULT_MAILTO


def _user_agent() -> str:
    return "Light-method-signal/1.0" + (f" (mailto:{_MAILTO})" if _MAILTO else "")


def http_fetch(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": _user_agent(),
                                               "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8", "replace"))


def _add_mailto(params: dict) -> str:
    p = dict(params)
    if _MAILTO:
        p.setdefault("mailto", _MAILTO)
    return urllib.parse.urlencode(p)


def parse_rp_line(line: str) -> dict:
    """从 representative_papers 条目抽锚点：doi:/cited:/checked:/年份。"""
    out = {}
    m = re.search(r"doi:([^\s|\"]+)", line)
    if m:
        out["doi"] = m.group(1)
    m = re.search(r"cited:(\d+)", line)
    if m:
        out["cited_snapshot"] = int(m.group(1))
    m = re.search(r"checked:([^\s|\"]+)", line)
    if m:
        out["checked"] = m.group(1)
    return out


def signal_citation(doi: str, snapshot: int | None, fetch) -> dict:
    """被引实时查 OpenAlex by DOI，与快照对比(冲突信在线 + 差异>50% 提示合并/拆分)。"""
    if not doi:
        return {"status": "unavailable", "reason": "无 doi 锚点"}
    try:
        url = f"{OA}/works/doi:{urllib.parse.quote(doi)}?" + _add_mailto(
            {"select": "id,cited_by_count,publication_year"})
        data = fetch(url)
        live = data.get("cited_by_count")
        out = {"status": "ok", "cited_by_count_live": live,
               "cited_snapshot": snapshot,
               "publication_year": data.get("publication_year"),
               "source": f"OpenAlex doi:{doi}(实时)，冲突信在线"}
        if snapshot and live and snapshot > 0:
            ratio = abs(live - snapshot) / snapshot
            if ratio > 0.5:
                out["anomaly"] = (f"在线值({live})与快照({snapshot})差异>{int(ratio*100)}%，"
                                  "可能 OpenAlex 记录合并/拆分(arXiv vs 正式版)，人工核")
        return out
    except Exception as e:  # noqa: BLE001
        return {"status": "unavailable", "reason": f"OpenAlex 失败:{e.__class__.__name__}",
                "cited_snapshot": snapshot, "note": "降级用本地快照，标 stale"}


def signal_repo_alive(repo: str, fetch) -> dict:
    """仓库存活 GitHub /repos/{org}/{repo}。"""
    if not repo or "/" not in repo:
        return {"status": "unavailable", "reason": "无 org/repo"}
    try:
        data = fetch(f"{GH}/repos/{repo}")
        return {"status": "ok", "repo": repo, "alive": True,
                "archived": data.get("archived", False),
                "pushed_at": data.get("pushed_at")}
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"status": "ok", "repo": repo, "alive": False, "http": 404,
                    "note": "仓库失效(404)，换镜像或标弃用"}
        return {"status": "unavailable", "reason": f"GitHub HTTP {e.code}"}
    except Exception as e:  # noqa: BLE001
        return {"status": "unavailable", "reason": f"GitHub 失败:{e.__class__.__name__}"}


def assemble(rp_line: str, doi: str, repo: str, fetch) -> dict:
    anchors = parse_rp_line(rp_line) if rp_line else {}
    use_doi = doi or anchors.get("doi", "")
    snap = anchors.get("cited_snapshot")
    return {
        "anchors": anchors,
        "signals": {
            "citation": signal_citation(use_doi, snap, fetch),
            "repo_alive": signal_repo_alive(repo, fetch) if repo
            else {"status": "unavailable", "reason": "未提供 --repo"},
        },
        "freshness": {"local_checked": anchors.get("checked"),
                      "note": "无网回退本地 cited 快照并标 stale；冲突默认信在线"},
    }


class _MockFetcher:
    def __call__(self, url: str) -> dict:
        if "/works/doi:" in url:
            return {"id": "https://openalex.org/W1", "cited_by_count": 221500,
                    "publication_year": 2016}
        if "/repos/" in url:
            return {"archived": False, "pushed_at": "2025-01-01T00:00:00Z"}
        raise RuntimeError(f"mock 未覆盖:{url}")


def _selftest() -> int:
    fetch = _MockFetcher()
    a = parse_rp_line("ResNet | 2016 | cited:221133 | doi:10.1109/cvpr.2016.90 | checked:2026-06-06")
    assert a == {"doi": "10.1109/cvpr.2016.90", "cited_snapshot": 221133,
                 "checked": "2026-06-06"}, a
    rep = assemble("ResNet | 2016 | cited:221133 | doi:10.1109/cvpr.2016.90 | checked:2026-06-06",
                   "", "facebookresearch/maml", fetch)
    assert rep["signals"]["citation"]["status"] == "ok"
    assert rep["signals"]["citation"]["cited_by_count_live"] == 221500
    assert rep["signals"]["citation"]["cited_snapshot"] == 221133  # 信在线但留快照对比
    assert rep["signals"]["repo_alive"]["alive"] is True
    assert rep["freshness"]["local_checked"] == "2026-06-06"

    # 差异>50% 异常提示
    rep2 = assemble("X | 2020 | cited:1000 | doi:10.1/x", "", "", fetch)
    assert "anomaly" in rep2["signals"]["citation"], rep2["signals"]["citation"]

    # 无 doi + 无 repo → 双 unavailable，不崩
    rep3 = assemble("无锚点条目 | 2020", "", "", fetch)
    assert rep3["signals"]["citation"]["status"] == "unavailable"
    assert rep3["signals"]["repo_alive"]["status"] == "unavailable"

    # OpenAlex 失败 → 降级留快照
    def boom(url):
        raise urllib.error.URLError("offline")
    rep4 = assemble("X | cited:50 | doi:10.2/y", "", "", boom)
    assert rep4["signals"]["citation"]["status"] == "unavailable"
    assert rep4["signals"]["citation"]["cited_snapshot"] == 50
    print("[selftest] PASS method_signal（被引/仓库存活 + 锚点解析 + 差异提示 + 降级 + 信在线）")
    return 0


def main() -> None:
    global _MAILTO
    ap = argparse.ArgumentParser(description="db03 方法卡易变字段实时校验")
    ap.add_argument("--doi", default="")
    ap.add_argument("--rp-line", default="", help="representative_papers 条目(自动解析锚点)")
    ap.add_argument("--repo", default="", help="GitHub org/repo")
    ap.add_argument("--mailto", default="")
    ap.add_argument("--json-out", default="")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        sys.exit(_selftest())
    if args.mailto:
        _MAILTO = args.mailto.strip()
    if not args.doi and not args.rp_line and not args.repo:
        ap.error("至少提供 --doi/--rp-line/--repo 之一(或 --selftest)")
    report = assemble(args.rp_line, args.doi, args.repo, http_fetch)
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.json_out:
        open(args.json_out, "w", encoding="utf-8").write(text)
    print(text)


if __name__ == "__main__":
    main()
