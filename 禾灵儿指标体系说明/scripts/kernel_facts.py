# -*- coding: utf-8 -*-
"""供图件脚本与文档脚本共用的实算结果。

所有数值都由已上线的算分内核 hlr_portrait 与真实数据库实时算出，
两个脚本引用同一份结果，保证正文、表格与图件三者数字完全一致。
"""
from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, "/home/user/xixi/禾灵儿德育画像系统")
os.environ.setdefault("HLR_DB",
                      "/home/user/xixi/禾灵儿德育画像系统/hlr_data/portrait.db")
import hlr_portrait as H   # noqa: E402

DIMS = list(H.DIMS)
GRADE = "大一"

# ---- 标定前的旧参数（对照用）--------------------------------------------
W_OLD = {
    "dialogue": {"文化体验": .20, "文化认知": .55, "文化志趣": .50, "文化认同": .40, "文化研创": .25},
    "enrollment": {"文化体验": .40, "文化认知": .25, "文化志趣": .60, "文化认同": .25, "文化研创": .10},
    "homework": {"文化体验": .25, "文化认知": .65, "文化志趣": .40, "文化认同": .20, "文化研创": .35},
    "video": {"文化体验": .60, "文化认知": .45, "文化志趣": .35, "文化认同": .20, "文化研创": .05},
    "artifact": {"文化体验": .35, "文化认知": .45, "文化志趣": .30, "文化认同": .40, "文化研创": .85},
    "agent": {"文化体验": .20, "文化认知": .50, "文化志趣": .40, "文化认同": .35, "文化研创": 1.0},
}
CAP_OLD = {"dialogue": 6., "enrollment": 6., "homework": 8., "video": 6.,
           "artifact": 12., "agent": 12.}
K_OLD = {"文化体验": 4.5, "文化认知": 5.0, "文化志趣": 4.5, "文化认同": 4.0, "文化研创": 3.5}
B_OLD = 0.50

CH_CN = {"dialogue": "文化对话", "enrollment": "文化课程报名", "homework": "课程作业",
         "video": "课程视频", "artifact": "学生作业成果", "agent": "学生自建智能体"}
CH_ORDER = ["dialogue", "homework", "artifact", "agent", "enrollment", "video"]
UNIT_LABEL = {"enrollment": "报名 1 门文化课程", "video": "学完 1 门课程的视频",
              "homework": "完成 1 门课程的作业", "dialogue": "1 轮文化对话",
              "artifact": "提交 1 份作业成果", "agent": "自建 1 个文化智能体"}
UNIT_ORDER = ["enrollment", "video", "homework", "dialogue", "artifact", "agent"]

_CACHE = {}


def _pct(v, p):
    k = (len(v) - 1) * p / 100.0
    lo = int(k); hi = min(lo + 1, len(v) - 1)
    return v[lo] + (v[hi] - v[lo]) * (k - lo)


def _cci(m, W, CAP, K, B):
    t = 0.0
    for d in DIMS:
        a = sum(min(mm.get(d, 0.0) * W[ch][d], CAP.get(ch, 8.0))
                for ch, mm in m.items() if ch in W)
        t += min(1.0, B + (1 - B) * (1 - math.exp(-a / K[d])))
    return t / 5


def facts():
    if _CACHE:
        return _CACHE
    cx = H.STORE.conn()
    D = {"n_stu": cx.execute("SELECT COUNT(DISTINCT sid) c FROM evidences "
                             "WHERE grade=?", (GRADE,)).fetchone()["c"],
         "n_ev": cx.execute("SELECT COUNT(*) c FROM evidences WHERE grade=?",
                            (GRADE,)).fetchone()["c"]}

    # 单位行为的原始量（该渠道每条记录的均值）与证据当量
    unit, eqv = {}, {}
    for ch in CH_ORDER:
        u = {r["dim"]: float(r["s"] or 0) for r in cx.execute(
            "SELECT dim, AVG(amount*quality*relevance) s FROM evidences "
            "WHERE grade=? AND channel=? GROUP BY 1", (GRADE, ch))}
        unit[ch] = u
        eqv[ch] = (sum(u.get(d, 0) * W_OLD[ch][d] for d in DIMS),
                   sum(u.get(d, 0) * H.CHANNEL_WEIGHTS[ch][d] for d in DIMS))
    D["unit"], D["eqv"] = unit, eqv

    # 全体大一学生（尚未做问卷，初始得分取各自默认值）
    raw = {}
    for r in cx.execute("SELECT sid,channel,dim,SUM(amount*quality*relevance) s "
                        "FROM evidences WHERE grade=? GROUP BY 1,2,3", (GRADE,)):
        raw.setdefault(r["sid"], {}).setdefault(r["channel"], {})[r["dim"]] = float(r["s"] or 0)
    D["raw"] = raw
    old_all = [_cci(m, W_OLD, CAP_OLD, K_OLD, B_OLD) for m in raw.values()]
    new_all = [_cci(m, H.CHANNEL_WEIGHTS, H.CHANNEL_A_CAP, H.KAPPA,
                    H.BASELINE_DEFAULT) for m in raw.values()]
    D["old_all"], D["new_all"] = old_all, new_all
    o, n = sorted(old_all), sorted(new_all)
    D["dist"] = {"old": {p: _pct(o, p) for p in (10, 25, 50, 75, 90, 99)},
                 "new": {p: _pct(n, p) for p in (10, 25, 50, 75, 90, 99)},
                 "old_max": o[-1], "new_max": n[-1]}

    # 中位学生追加文化对话
    sids = list(raw)
    med = min(sids, key=lambda s: abs(_cci(raw[s], H.CHANNEL_WEIGHTS,
                                           H.CHANNEL_A_CAP, H.KAPPA,
                                           H.BASELINE_DEFAULT) - D["dist"]["new"][50]))
    D["med0_old"] = _cci(raw[med], W_OLD, CAP_OLD, K_OLD, B_OLD)
    D["med0_new"] = _cci(raw[med], H.CHANNEL_WEIGHTS, H.CHANNEL_A_CAP,
                         H.KAPPA, H.BASELINE_DEFAULT)
    go, gn = [], []
    for k in (10, 30, 60):
        m2 = {ch: dict(v) for ch, v in raw[med].items()}
        dd = m2.setdefault("dialogue", {})
        for d in DIMS:
            dd[d] = dd.get(d, 0.0) + unit["dialogue"].get(d, 0.0) * k
        go.append(_cci(m2, W_OLD, CAP_OLD, K_OLD, B_OLD))
        gn.append(_cci(m2, H.CHANNEL_WEIGHTS, H.CHANNEL_A_CAP, H.KAPPA,
                       H.BASELINE_DEFAULT))
    D["gain_old"], D["gain_new"] = go, gn

    # 问卷映射示例
    def bmap(items):
        """返回（折减系数, 初始得分, 问卷均分, 题目标准差, 折减后的作答强度）。"""
        pen = H.straight_line_penalty(items)
        mean = sum(items) / len(items)
        sd = math.sqrt(sum((x - mean) ** 2 for x in items) / len(items))
        return pen, H.baseline_from_intensity(mean * pen), mean, sd, mean * pen
    D["qex"] = {"straight": bmap([1.0] * 20),
                "near": bmap([1.0] * 17 + [0.75] * 3),
                "high": bmap([1.0] * 10 + [0.75] * 8 + [0.5] * 2),
                "mid": bmap([0.75] * 6 + [0.5] * 10 + [0.25] * 4),
                "low": bmap([0.5] * 5 + [0.25] * 10 + [0.0] * 5)}

    # 两类学生的四年轨迹（单位量取实测均值，逐年承接上一学年得分）
    # 起点直接取上表两种作答方式的初始得分：认真作答 vs 每题都选最高档
    def mk(course, video, hw, dlg, art, agt):
        r = {}
        for ch, k in (("enrollment", course), ("video", video), ("homework", hw),
                      ("dialogue", dlg), ("artifact", art), ("agent", agt)):
            if k:
                r[ch] = {d: unit[ch].get(d, 0.0) * k for d in DIMS}
        return r

    def traj(paths, b0):
        B = {d: b0 for d in DIMS}
        out = []
        for m in paths:
            S = {}
            for d in DIMS:
                a = sum(min(mm.get(d, 0.0) * H.CHANNEL_WEIGHTS[ch][d],
                            H.CHANNEL_A_CAP[ch]) for ch, mm in m.items())
                S[d] = min(1.0, B[d] + (1 - B[d]) * (1 - math.exp(-a / H.KAPPA[d])))
            out.append(sum(S.values()) / 5)
            B = S
        return out

    D["path_act"] = [("1 门课 + 1 门课的视频 + 2 轮对话", mk(1, 1, 0, 2, 0, 0)),
                     ("2 门课 + 2 门课的视频 + 2 门作业 + 15 轮对话", mk(2, 2, 2, 15, 0, 0)),
                     ("3 门课 + 3 门课的视频 + 4 门作业 + 35 轮对话 + 2 份成果",
                      mk(3, 3, 4, 35, 2, 0)),
                     ("4 门课 + 4 门课的视频 + 6 门作业 + 60 轮对话 + 4 份成果 + 2 个智能体",
                      mk(4, 4, 6, 60, 4, 2))]
    D["b_act"], D["b_pas"] = D["qex"]["high"][1], D["qex"]["straight"][1]
    D["act"] = traj([m for _, m in D["path_act"]], D["b_act"])
    D["pas"] = traj([mk(1, 0.4, 0, 0, 0, 0)] * 4, D["b_pas"])

    _CACHE.update(D)
    return D
