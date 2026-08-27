"""数据模型：访问记录、IP 画像、告警。

全部用 dataclass，方便直接 asdict() 存 JSON / 塞进模板。
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Dict, List, Optional

CN_TZ_NAME = "Asia/Shanghai"


@dataclass
class VisitRecord:
    """一条「最近访问记录」。

    表格列名在不同版本的博达后台里不完全一样，所以除了几个我们真正依赖的字段
    （时间 / IP）之外，其余原始列全部原样塞进 ``raw``，告警邮件里会完整展示。
    """

    ip: str
    visited_at: Optional[datetime] = None      # 访问时间（Asia/Shanghai）
    #: 页面上原样的时间文字。指纹用它而不是解析后的 datetime——
    #: 页面只给「15:32:11」时我们要自己补日期，补法依赖「现在几点」，
    #: 于是同一行记录在午夜前后会算出两个不同的 datetime、两个不同的指纹，
    #: 结果重复入库、重复告警。原始字符串没有这个问题。
    raw_time: str = ""
    page: str = ""                             # 访问页面 / URL
    page_title: str = ""                       # 页面标题（如果有单独一列）
    referer: str = ""                          # 来源页面
    user_agent: str = ""                       # 浏览器 / UA 原文
    browser: str = ""
    os: str = ""
    site: str = ""                             # 所属站点（多站点时有用）
    location_hint: str = ""                    # 后台自带的地区列（通常只到省）
    raw: Dict[str, str] = field(default_factory=dict)
    row_index: int = -1                        # 在当次抓取的表格里的行号
    #: 同一批解析里，指纹完全相同的第几条（0 表示唯一）。
    #: 用于兜住「一行的所有可辨识字段都没解析出来」的退化情况，
    #: 否则 N 条记录会坍缩成 1 条：当轮凑不够阈值不告警，而且这个 IP
    #: 之后的每一条访问都会被当成「见过了」永久丢弃。
    dup_index: int = 0
    first_seen_at: Optional[datetime] = None   # 我们第一次看到它的时间

    @property
    def key(self) -> str:
        """去重指纹。

        博达后台的表格没有稳定的行 ID，所以用「时间 + IP + 页面 + 来源」做指纹。
        时间优先取页面上的原始字符串（见 raw_time 的说明），实在没有才用解析结果。
        """
        ts = self.raw_time or (
            self.visited_at.strftime("%Y-%m-%d %H:%M:%S") if self.visited_at else ""
        )
        payload = "|".join([ts, self.ip, self.page, self.referer, self.page_title])
        if self.dup_index:
            payload += f"|#{self.dup_index}"
        return hashlib.sha1(payload.encode("utf-8", "replace")).hexdigest()[:20]

    @property
    def is_degraded(self) -> bool:
        """这条记录除了 IP 之外什么都没解析出来——去重能力已经退化。"""
        return not (self.raw_time or self.visited_at or self.page or self.page_title)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["visited_at"] = self.visited_at.isoformat() if self.visited_at else None
        d["first_seen_at"] = self.first_seen_at.isoformat() if self.first_seen_at else None
        d["key"] = self.key
        return d


@dataclass
class IpProfile:
    """一个 IP 的画像，尽可能细。"""

    ip: str
    ok: bool = False
    # --- 地理 ---
    country: str = ""
    country_code: str = ""
    region: str = ""            # 省 / 州
    city: str = ""              # 市
    district: str = ""          # 区 / 县（能拿到就拿）
    division_code: str = ""     # GB/T 2260 六位行政区划码，如 330402
    zip_code: str = ""
    lat: Optional[float] = None
    lon: Optional[float] = None
    timezone: str = ""
    accuracy: str = ""          # 粗略说明定位精度：country / region / city / district
    # --- 网络归属 ---
    isp: str = ""               # 运营商，如 中国电信 / 中国教育和科研计算机网
    org: str = ""
    asn: str = ""               # AS4538
    as_name: str = ""
    network: str = ""           # CIDR
    network_type: str = ""      # 宽带 / 基站 / 专线 / IDC（GeoCN 提供）
    rdns: str = ""              # 反向解析域名
    rdns_checked: bool = False  # 查过没（查不到也算查过，避免每轮重付 DNS 超时）
    # --- 风险 / 身份判定 ---
    is_private: bool = False    # 内网地址
    is_campus: bool = False     # 疑似校园网 / CERNET
    is_datacenter: bool = False # 机房 / 云主机
    is_proxy: bool = False      # 代理 / VPN
    is_mobile: bool = False     # 移动蜂窝网络
    is_bot: bool = False        # 搜索引擎爬虫
    bot_name: str = ""          # Baiduspider / Googlebot / ...
    bot_evidence: str = ""      # 判定依据：反向域名（可信）/ UA（可伪造）
    risk_score: int = 0         # 0-100，越高越值得看一眼
    risk_reasons: List[str] = field(default_factory=list)
    # --- 溯源 ---
    sources: List[str] = field(default_factory=list)  # 数据来自哪几个源
    looked_up_at: Optional[datetime] = None
    error: str = ""

    @property
    def location_text(self) -> str:
        """人话版位置：中国 浙江省 嘉兴市 南湖区。"""
        parts = [p for p in (self.country, self.region, self.city, self.district) if p]
        # 去掉「浙江省 浙江省」这种重复
        deduped: List[str] = []
        for p in parts:
            if not deduped or p not in deduped[-1] and deduped[-1] not in p:
                deduped.append(p)
        return " ".join(deduped) if deduped else "未知"

    @property
    def network_text(self) -> str:
        bits = [b for b in (self.isp, self.org) if b]
        if self.asn:
            bits.append(f"AS{self.asn.lstrip('ASas')}" if not self.asn.upper().startswith("AS") else self.asn)
        seen, out = set(), []
        for b in bits:
            if b not in seen:
                seen.add(b)
                out.append(b)
        return " / ".join(out) if out else "未知"

    @property
    def labels(self) -> List[str]:
        tags = []
        if self.is_private:
            tags.append("内网")
        if self.is_campus:
            tags.append("校园网/教育网")
        if self.is_bot:
            tags.append(f"爬虫:{self.bot_name}" if self.bot_name else "爬虫")
        if self.is_datacenter:
            tags.append("机房/云主机")
        if self.is_proxy:
            tags.append("代理/VPN")
        if self.is_mobile:
            tags.append("移动网络")
        if self.network_type and self.network_type not in ("IDC", "基站"):
            tags.append(self.network_type)
        return tags

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["looked_up_at"] = self.looked_up_at.isoformat() if self.looked_up_at else None
        d["location_text"] = self.location_text
        d["network_text"] = self.network_text
        d["labels"] = self.labels
        return d


@dataclass
class Alert:
    """一次告警。"""

    rule: str                       # burst / ip_burst / ...
    title: str
    summary: str
    triggered_at: datetime
    records: List[VisitRecord] = field(default_factory=list)
    profiles: Dict[str, IpProfile] = field(default_factory=dict)
    severity: str = "warning"       # info / warning / critical
    dedup_key: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule": self.rule,
            "title": self.title,
            "summary": self.summary,
            "triggered_at": self.triggered_at.isoformat(),
            "severity": self.severity,
            "dedup_key": self.dedup_key,
            "records": [r.to_dict() for r in self.records],
            "profiles": {k: v.to_dict() for k, v in self.profiles.items()},
        }
