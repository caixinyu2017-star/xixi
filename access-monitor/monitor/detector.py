"""突发访问检测。

核心规则（对应你说的「短时间内有 3 条以上访问记录」）：
    在任意一个 `burst_window_seconds` 长的滑动窗口里，访问记录数 >= `burst_threshold`。

用滑动窗口而不是「每分钟固定分桶」，是因为分桶会漏掉跨桶的突发：
23:59:58 / 23:59:59 / 00:00:01 这三条在分桶法里是 2+1，不触发；滑动窗口能抓到。

时间基准优先用后台表格里的「访问时间」；解析不出时间时回落到「我们第一次看到这条记录的时间」。
"""
from __future__ import annotations

import ipaddress
import logging
from datetime import datetime, timedelta
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from .config import RulesConfig
from .models import Alert, IpProfile, VisitRecord

log = logging.getLogger(__name__)


# --------------------------------------------------------------------------- #
# 工具
# --------------------------------------------------------------------------- #
def effective_time(rec: VisitRecord) -> datetime:
    return rec.visited_at or rec.first_seen_at or datetime.now()


def ip_matches(ip: str, patterns: Sequence[str]) -> bool:
    """支持单个 IP、CIDR 网段、以及 `192.168.` 这样的前缀写法。"""
    if not patterns:
        return False
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        addr = None
    for pat in patterns:
        pat = str(pat).strip()
        if not pat:
            continue
        if pat == ip:
            return True
        if addr is not None and "/" in pat:
            try:
                if addr in ipaddress.ip_network(pat, strict=False):
                    return True
            except ValueError:
                pass
        elif pat.endswith(".") and ip.startswith(pat):
            return True
    return False


def is_private_ip(ip: str) -> bool:
    try:
        a = ipaddress.ip_address(ip)
    except ValueError:
        return False
    return a.is_private or a.is_loopback or a.is_link_local or a.is_reserved


def sliding_clusters(
    records: Sequence[VisitRecord], window_seconds: int, threshold: int
) -> List[List[VisitRecord]]:
    """找出所有「窗口内条数 >= threshold」的最大簇。

    返回的簇之间不重叠：一旦某个窗口达标，就把这一簇整体吐出来，从簇尾之后继续找，
    避免同一批记录被拆成 N 个高度重叠的告警。
    """
    if threshold <= 0 or not records:
        return []
    ordered = sorted(records, key=effective_time)
    times = [effective_time(r).timestamp() for r in ordered]
    clusters: List[List[VisitRecord]] = []
    i = 0
    n = len(ordered)
    while i < n:
        j = i
        while j + 1 < n and times[j + 1] - times[i] <= window_seconds:
            j += 1
        size = j - i + 1
        if size >= threshold:
            # 把簇往后撑大，但**必须保持密度**：只有当「新来这条 + 它前面 threshold-1 条」
            # 仍然挤在同一个窗口里，才算还是同一次突发。
            # 如果只判断「和上一条间隔 < window」，那么每 59 秒来一条的细水长流
            # 会被一路串起来，最后报出一个「一小时内 60 条」的假突发。
            k = j
            while k + 1 < n:
                lo = k + 1 - (threshold - 1)
                if lo < i or times[k + 1] - times[lo] > window_seconds:
                    break
                k += 1
            clusters.append(ordered[i:k + 1])
            i = k + 1
        else:
            i += 1
    return clusters


def _span_text(records: Sequence[VisitRecord]) -> Tuple[str, float]:
    if not records:
        return "", 0.0
    ts = [effective_time(r) for r in records]
    lo, hi = min(ts), max(ts)
    span = (hi - lo).total_seconds()
    return f"{lo:%H:%M:%S} ~ {hi:%H:%M:%S}", span


# --------------------------------------------------------------------------- #
# 检测器
# --------------------------------------------------------------------------- #
class BurstDetector:
    def __init__(self, rules: RulesConfig):
        self.rules = rules

    # ---- 过滤 ----
    def keep(self, rec: VisitRecord, profile: Optional[IpProfile]) -> Tuple[bool, str]:
        r = self.rules
        if r.only_ips and not ip_matches(rec.ip, r.only_ips):
            return False, "不在 only_ips 白名单内"
        if ip_matches(rec.ip, r.ignore_ips):
            return False, "命中 ignore_ips"
        if r.ignore_private and is_private_ip(rec.ip):
            return False, "内网地址"
        if r.ignore_bots and profile is not None and profile.is_bot:
            return False, f"搜索引擎爬虫 {profile.bot_name}".strip()
        return True, ""

    def filter_records(
        self, records: Iterable[VisitRecord], profiles: Dict[str, IpProfile]
    ) -> List[VisitRecord]:
        kept: List[VisitRecord] = []
        for rec in records:
            ok, why = self.keep(rec, profiles.get(rec.ip))
            if ok:
                kept.append(rec)
            else:
                log.debug("过滤掉 %s（%s）", rec.ip, why)
        return kept

    # ---- 主入口 ----
    def detect(
        self,
        new_records: Sequence[VisitRecord],
        window_records: Sequence[VisitRecord],
        profiles: Dict[str, IpProfile],
        known_ips_before: Optional[set] = None,
        now: Optional[datetime] = None,
        alerted_keys: Optional[set] = None,
    ) -> List[Alert]:
        """
        :param new_records:    本轮新抓到的记录（已入库）
        :param window_records: 最近一段时间的全部记录（含 new_records），用来算窗口
        :param profiles:       IP 画像，用于过滤和告警正文
        :param known_ips_before: 本轮之前已知的 IP 集合，用于「首次出现的 IP」规则
        :param alerted_keys:   已经成功推送过的记录指纹。簇的**密度**仍然算上它们
                               （「60 秒内 3 条」是整簇的性质），但**触发**必须靠
                               一条既是新记录、又没报过的记录，否则一个已经报过的簇
                               会在每次冷却到期后反复再报一遍。
        """
        now = now or datetime.now()
        r = self.rules
        alerts: List[Alert] = []

        new_kept = self.filter_records(new_records, profiles)
        if not new_kept:
            return alerts
        window_kept = self.filter_records(window_records, profiles)
        done = alerted_keys or set()
        new_keys = {rec.key for rec in new_kept} - done
        if not new_keys:
            return alerts

        # ---- 规则一：整体突发 ----
        if r.burst_enabled:
            for cluster in sliding_clusters(window_kept, r.burst_window_seconds, r.burst_threshold):
                if not any(rec.key in new_keys for rec in cluster):
                    continue  # 老簇，之前已经报过
                span_text, span = _span_text(cluster)
                ips = sorted({rec.ip for rec in cluster})
                alerts.append(Alert(
                    rule="burst",
                    severity="critical" if len(cluster) >= r.burst_threshold * 3 else "warning",
                    title=f"⚠️ 短时突发访问：{int(span)} 秒内 {len(cluster)} 条记录，来自 {len(ips)} 个 IP",
                    summary=(
                        f"在 {span_text}（跨度 {int(span)} 秒）内检测到 {len(cluster)} 条访问记录，"
                        f"达到阈值（{r.burst_window_seconds} 秒内 ≥ {r.burst_threshold} 条）。"
                        f"涉及 {len(ips)} 个 IP：{', '.join(ips[:8])}"
                        + ("…" if len(ips) > 8 else "")
                    ),
                    triggered_at=now,
                    records=cluster,
                    profiles={ip: profiles[ip] for ip in ips if ip in profiles},
                    dedup_key="burst:" + ",".join(sorted(rec.key for rec in cluster))[:120],
                ))

        # ---- 规则二：单 IP 高频 ----
        if r.ip_burst_enabled:
            by_ip: Dict[str, List[VisitRecord]] = {}
            for rec in window_kept:
                by_ip.setdefault(rec.ip, []).append(rec)
            for ip, recs in sorted(by_ip.items()):
                for cluster in sliding_clusters(recs, r.ip_burst_window_seconds, r.ip_burst_threshold):
                    if not any(rec.key in new_keys for rec in cluster):
                        continue
                    span_text, span = _span_text(cluster)
                    prof = profiles.get(ip)
                    where = prof.location_text if prof else "位置未知"
                    alerts.append(Alert(
                        rule="ip_burst",
                        severity="critical" if len(cluster) >= r.ip_burst_threshold * 4 else "warning",
                        title=f"🔎 单 IP 高频访问：{ip}（{len(cluster)} 次 / {int(span)} 秒）",
                        summary=(
                            f"IP {ip}（{where}）在 {span_text} 内访问了 {len(cluster)} 次，"
                            f"达到阈值（{r.ip_burst_window_seconds} 秒内 ≥ {r.ip_burst_threshold} 次）。"
                        ),
                        triggered_at=now,
                        records=cluster,
                        profiles={ip: prof} if prof else {},
                        dedup_key=f"ip_burst:{ip}:" + ",".join(sorted(rec.key for rec in cluster))[:100],
                    ))

        # ---- 规则三：首次出现的 IP ----
        if r.new_ip_enabled and known_ips_before is not None:
            fresh = sorted({rec.ip for rec in new_kept} - set(known_ips_before))
            if fresh:
                recs = [rec for rec in new_kept if rec.ip in set(fresh)]
                alerts.append(Alert(
                    rule="new_ip",
                    severity="info",
                    title=f"🆕 出现 {len(fresh)} 个从未见过的 IP",
                    summary="首次出现：" + ", ".join(fresh[:10]) + ("…" if len(fresh) > 10 else ""),
                    triggered_at=now,
                    records=recs,
                    profiles={ip: profiles[ip] for ip in fresh if ip in profiles},
                    dedup_key="new_ip:" + ",".join(fresh)[:120],
                ))

        return self._merge_overlapping(alerts)

    @staticmethod
    def _merge_overlapping(alerts: List[Alert]) -> List[Alert]:
        """同一轮里，如果单 IP 告警的记录已经被整体突发告警完全覆盖，就不重复发。"""
        if len(alerts) < 2:
            return alerts
        burst_keys = set()
        for a in alerts:
            if a.rule == "burst":
                burst_keys |= {r.key for r in a.records}
        out: List[Alert] = []
        for a in alerts:
            if a.rule == "ip_burst" and burst_keys and {r.key for r in a.records} <= burst_keys:
                log.debug("单 IP 告警 %s 已被整体突发告警覆盖，跳过", a.dedup_key)
                continue
            out.append(a)
        return out
