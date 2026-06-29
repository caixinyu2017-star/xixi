#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fetch_openreview.py — 抓 OpenReview 公开评审语料，校准模拟审稿/学习 rebuttal 话术。

只读公开数据，无需登录。两条实测可用路径（见同目录 references.md tool 2）：
  A) 批量：投稿(venue 级 Submission invitation) + details=directReplies，
     每篇投稿的 details.directReplies 直接挂着它的 Official_Review/Official_Comment/
     Meta_Review/Decision —— 一次遍历全 venue 审稿。
  B) 单篇：拿 forum(=投稿 id) 取整条讨论树 GET /notes?forum=<id>&details=directReplies。

⚠️ 审稿 invitation 是 per-submission（.../Submission<n>/-/Official_Review），
   venue 级 .../Conference/-/Official_Review 永远返回空 —— 本脚本走 directReplies 规避。

invitation 因会议而异：先查 venue group 拿真实段名(submission_name/review_name/...)，
不硬编码。

用法:
  python fetch_openreview.py --venue ICLR.cc/2024/Conference --max-subs 20 \
                             --out corpus.json
  python fetch_openreview.py --forum cXs5md5wAq            # 单篇讨论树
  python fetch_openreview.py --selftest                    # 不联网，合成自检

输出: 统计 weakness 高频措辞与 rating 分布(校准模式一) + 抽 rebuttal 话术样本。
依赖: 仅标准库(urllib)。openreview-py 可选，未安装则用 REST 直连。
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
import json
import re
import argparse
import urllib.request
import urllib.parse
from collections import Counter

API_V2 = "https://api2.openreview.net"
API_V1 = "https://api.openreview.net"  # 2024 前老会议（结构不同）


def _get(base, path, params, timeout=30):
    """GET JSON，返回 (http_code, obj_or_None, err)。"""
    qs = urllib.parse.urlencode(params)
    url = f"{base}{path}?{qs}"
    req = urllib.request.Request(url, headers={"User-Agent": "light-review-rebuttal/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            code = r.getcode()
            data = r.read().decode("utf-8")
            return code, json.loads(data), None
    except urllib.error.HTTPError as e:
        return e.code, None, f"HTTP {e.code}: {e.reason}"
    except Exception as e:
        return None, None, str(e)


def get_venue_names(base, venue_id):
    """查 venue group 拿真实段名，避免硬编码 invitation。

    返回 dict: submission_name/review_name/meta_review_name/decision_name。
    查不到则回退到顶会常见默认值。
    """
    code, obj, err = _get(base, "/groups", {"id": venue_id})
    defaults = {
        "submission_name": "Submission",
        "review_name": "Official_Review",
        "meta_review_name": "Meta_Review",
        "decision_name": "Decision",
    }
    if code != 200 or not obj or not obj.get("groups"):
        return defaults, code, err
    content = obj["groups"][0].get("content", {}) or {}
    out = {}
    for k, d in defaults.items():
        out[k] = (content.get(k) or {}).get("value", d)
    return out, code, None


def _cval(note, field):
    """取 v2 note.content[field].value；缺失返回空串。"""
    c = note.get("content", {}) or {}
    v = c.get(field)
    if isinstance(v, dict):
        return v.get("value", "")
    return v if v is not None else ""


def _reply_type(note):
    """从 invitation(s) 末段判定 Note 类型。"""
    invs = note.get("invitations") or ([note["invitation"]] if note.get("invitation") else [])
    for i in invs:
        tail = i.split("/-/")[-1]
        if tail in ("Official_Review", "Official_Comment", "Meta_Review", "Decision"):
            return tail
    # 兜底：看 invitation 末段
    if invs:
        return invs[0].split("/-/")[-1]
    return "Unknown"


def fetch_submissions(base, venue_id, sub_name, max_subs, page=1000):
    """批量拉投稿 + directReplies（路径 A）。返回投稿 Note 列表。"""
    inv = f"{venue_id}/-/{sub_name}"
    notes = []
    offset = 0
    while len(notes) < max_subs:
        limit = min(page, max_subs - len(notes))
        code, obj, err = _get(base, "/notes", {
            "invitation": inv,
            "details": "directReplies",
            "limit": limit,
            "offset": offset,
        })
        if code != 200 or not obj:
            raise RuntimeError(f"fetch submissions failed: {err} (inv={inv})")
        batch = obj.get("notes", [])
        if not batch:
            break
        notes.extend(batch)
        offset += len(batch)
        if len(batch) < limit:
            break
    return notes[:max_subs]


def fetch_forum(base, forum_id):
    """单篇：取整条讨论树（路径 B）。返回 Note 列表。"""
    code, obj, err = _get(base, "/notes", {"forum": forum_id, "details": "directReplies"})
    if code != 200 or not obj:
        raise RuntimeError(f"fetch forum failed: {err}")
    return obj.get("notes", [])


# ----------------------- 语料分析 -----------------------
_STOP = set("the a an and or of to in for on with is are be this that we our it as "
            "by from at not but which can may also more some such using used use these "
            "their they them then than into about other paper authors method results".split())


def collect_reviews(submissions):
    """从投稿的 details.directReplies 抽出所有 Official_Review。返回 review Note 列表。"""
    reviews = []
    for sub in submissions:
        for r in sub.get("details", {}).get("directReplies", []):
            if _reply_type(r) == "Official_Review":
                reviews.append(r)
    return reviews


def collect_rebuttals(submissions):
    """抽 Official_Comment 作 rebuttal 话术样本。"""
    out = []
    for sub in submissions:
        for r in sub.get("details", {}).get("directReplies", []):
            if _reply_type(r) == "Official_Comment":
                out.append(r)
    return out


def analyze(reviews):
    """统计 rating 分布 + weakness 高频词。返回 dict。"""
    ratings = Counter()
    word = Counter()
    for rv in reviews:
        rt = _cval(rv, "rating")
        # rating 形如 "3: reject, not good enough" → 取前导数字
        m = re.match(r"\s*(\d+)", str(rt))
        ratings[m.group(1) if m else str(rt)[:20] or "NA"] += 1
        wk = str(_cval(rv, "weaknesses")).lower()
        for tok in re.findall(r"[a-z][a-z\-]{3,}", wk):
            if tok not in _STOP:
                word[tok] += 1
    return {
        "n_reviews": len(reviews),
        "rating_dist": dict(sorted(ratings.items())),
        "top_weakness_terms": word.most_common(25),
    }


def main():
    ap = argparse.ArgumentParser(description="Fetch OpenReview public review corpus.")
    ap.add_argument("--venue", help="venue group id, e.g. ICLR.cc/2024/Conference")
    ap.add_argument("--forum", help="single submission forum id (path B)")
    ap.add_argument("--legacy", action="store_true", help="use legacy v1 API (pre-2024)")
    ap.add_argument("--max-subs", type=int, default=20, help="max submissions to pull")
    ap.add_argument("--out", help="write full corpus JSON to this path")
    ap.add_argument("--selftest", action="store_true", help="offline synthetic self-test")
    args = ap.parse_args()
    base = API_V1 if args.legacy else API_V2

    if args.selftest:
        return selftest()

    if args.forum:
        notes = fetch_forum(base, args.forum)
        reviews = [n for n in notes if _reply_type(n) == "Official_Review"]
        rebuttals = [n for n in notes if _reply_type(n) == "Official_Comment"]
        print(f"[forum {args.forum}] notes={len(notes)} reviews={len(reviews)} "
              f"comments={len(rebuttals)}")
        stats = analyze(reviews)
        _report(stats, rebuttals)
        if args.out:
            _dump(args.out, {"forum": args.forum, "notes": notes, "stats": stats})
        return 0

    if not args.venue:
        ap.error("need --venue or --forum (or --selftest)")
    names, code, err = get_venue_names(base, args.venue)
    print(f"[group {args.venue}] HTTP {code} names={names}")
    subs = fetch_submissions(base, args.venue, names["submission_name"], args.max_subs)
    reviews = collect_reviews(subs)
    rebuttals = collect_rebuttals(subs)
    print(f"[{args.venue}] submissions={len(subs)} reviews={len(reviews)} "
          f"comments={len(rebuttals)}")
    stats = analyze(reviews)
    _report(stats, rebuttals)
    if args.out:
        _dump(args.out, {"venue": args.venue, "names": names,
                         "n_submissions": len(subs), "stats": stats})
    return 0


def _report(stats, rebuttals):
    print(f"\n== rating distribution (n={stats['n_reviews']}) ==")
    for k, v in stats["rating_dist"].items():
        print(f"  rating {k}: {v}")
    print("\n== top weakness terms ==")
    for term, c in stats["top_weakness_terms"][:15]:
        print(f"  {term}: {c}")
    if rebuttals:
        sample = str(_cval(rebuttals[0], "comment"))[:300]
        print(f"\n== rebuttal sample (1 of {len(rebuttals)}) ==\n  {sample}")


def _dump(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print(f"\n[written] {path}")


def selftest():
    """合成 directReplies 跑全管线，不联网。"""
    fake_subs = [{
        "number": 1, "forum": "FAKE1",
        "details": {"directReplies": [
            {"invitations": ["V/2024/Conference/Submission1/-/Official_Review"],
             "content": {"rating": {"value": "3: reject, not good enough"},
                         "weaknesses": {"value": "The novelty is limited and the "
                                        "experiments are insufficient. No baseline comparison."}}},
            {"invitations": ["V/2024/Conference/Submission1/-/Official_Review"],
             "content": {"rating": {"value": "6: weak accept"},
                         "weaknesses": {"value": "Clarity issues in section 3; missing "
                                        "ablation on the novelty claim."}}},
            {"invitations": ["V/2024/Conference/Submission1/-/Official_Comment"],
             "content": {"comment": {"value": "We thank the reviewer. We added the "
                                     "requested baseline; see revised Table 2."}}},
            {"invitations": ["V/2024/Conference/Submission1/-/Decision"],
             "content": {"decision": {"value": "Reject"}}},
        ]},
    }]
    reviews = collect_reviews(fake_subs)
    rebuttals = collect_rebuttals(fake_subs)
    assert len(reviews) == 2, reviews
    assert len(rebuttals) == 1, rebuttals
    stats = analyze(reviews)
    assert stats["n_reviews"] == 2
    assert "3" in stats["rating_dist"] and "6" in stats["rating_dist"]
    terms = dict(stats["top_weakness_terms"])
    assert "novelty" in terms, terms
    assert _reply_type(fake_subs[0]["details"]["directReplies"][0]) == "Official_Review"
    print("[selftest] PASS — collect/analyze/reply_type all OK")
    _report(stats, rebuttals)
    return 0


if __name__ == "__main__":
    sys.exit(main())
