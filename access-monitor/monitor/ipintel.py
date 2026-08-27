"""IP 画像：尽可能细地判断「这个访问者是谁、从哪来」。

分层查询，越靠前越便宜、越靠后越贵，结果合并进同一个 IpProfile。
突发告警的特点是「一次要查一批 IP」，所以**离线库优先**是刚需：

  0. 本地判断      内网 / 保留地址 —— 直接短路
  1. GeoCN.mmdb    国内 IP 的杀手锏：省-市-**区县** + 运营商（含「教育网」）+ 网络类型
                   （宽带 / 基站 / 专线 / IDC）。离线、零延迟、无配额。
  2. ip2region     全球覆盖的离线库，国内到市一级，国外也能用
  3. ip-api.com    补 ASN / org / 是否代理 / 是否机房；免费、中文
                   注意：免费版**只有 HTTP**，batch 限流 15 次/分钟（比单查的 45 更严）
  4. 腾讯位置服务  需要 key。目前唯一「国内基本都能到区/县」的在线 API
  5. 反向 DNS      认爬虫最可靠的手段（结果会缓存，包括「查不到」也缓存）
  6. RDAP          网段归属机构，能看出是教育网还是机房

结果按 IP 缓存（默认 7 天），所以真正打 API 的次数很少。
"""
from __future__ import annotations

import ipaddress
import json
import logging
import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import requests

from .config import IpIntelConfig
from .models import IpProfile
from .store import Store

log = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
# 爬虫识别
# --------------------------------------------------------------------------- #
# 反向解析域名后缀 -> 爬虫名。
# 注意：**不要求正向反查一致（FCrDNS）**。百度和字节的 PTR 主机名根本没有正向 A 记录，
# 严格校验会把它们全判成真人，反而制造大量误报。
BOT_RDNS_SUFFIXES: Dict[str, str] = {
    ".googlebot.com": "Googlebot",
    ".google.com": "Google",
    ".search.msn.com": "Bingbot",
    ".baidu.com": "Baiduspider",
    ".baidu.jp": "Baiduspider",
    ".crawl.bytedance.com": "Bytespider 字节跳动",
    ".bytedance.com": "Bytespider 字节跳动",
    ".crawl.sm.cn": "神马蜘蛛 YisouSpider",   # 神马的后缀是 sm.cn，不是 yisou.com
    ".yandex.ru": "YandexBot",
    ".yandex.net": "YandexBot",
    ".yandex.com": "YandexBot",
    ".duckduckgo.com": "DuckDuckBot",
    ".ahrefs.com": "AhrefsBot",
    ".semrush.com": "SemrushBot",
    ".applebot.apple.com": "Applebot",
    ".petalsearch.com": "PetalBot 华为",
    ".aspiegel.com": "PetalBot 华为",
    ".fbsv.net": "FacebookBot",
    ".crawl.amazon.com": "Amazonbot",
}

# 搜狗、360、部分 PetalBot 根本没有可用的 PTR（会反解成运营商的通用 ADSL 域名），
# 只能靠 UA 认。UA 可以伪造，所以标记为「疑似」。
BOT_UA_PATTERNS: Sequence[Tuple[str, str]] = (
    ("baiduspider", "Baiduspider"), ("googlebot", "Googlebot"), ("bingbot", "Bingbot"),
    ("sogou", "Sogou 搜狗蜘蛛"), ("360spider", "360Spider"), ("haosouspider", "360Spider"),
    ("yisouspider", "神马蜘蛛"), ("bytespider", "Bytespider"), ("petalbot", "PetalBot"),
    ("yandexbot", "YandexBot"), ("ahrefsbot", "AhrefsBot"), ("semrushbot", "SemrushBot"),
    ("mj12bot", "MJ12bot"), ("dotbot", "DotBot"), ("applebot", "Applebot"),
)
# 更宽泛的「这不是浏览器」特征
TOOL_UA_HINTS: Sequence[str] = (
    "spider", "bot", "crawler", "slurp", "scrapy", "python-requests", "httpclient",
    "curl/", "wget", "headlesschrome", "phantomjs", "puppeteer", "playwright",
    "okhttp", "go-http-client", "java/", "libwww", "apache-httpclient",
)

DATACENTER_HINTS: Sequence[str] = (
    "alibaba", "aliyun", "tencent", "huawei cloud", "hwclouds", "ucloud", "qiniu",
    "amazon", "aws", "google cloud", "microsoft", "azure", "digitalocean", "linode",
    "vultr", "ovh", "hetzner", "choopa", "cloudflare", "akamai", "fastly",
    "hosting", "data center", "datacenter", "idc", "cloud",
)

# GB/T 2260 省级行政区划代码（前两位）。GeoCN 返回的是 6 位数字码，
# 没有 divisions.json 时至少还能说出是哪个省。
PROVINCE_CODES: Dict[str, str] = {
    "11": "北京市", "12": "天津市", "13": "河北省", "14": "山西省", "15": "内蒙古自治区",
    "21": "辽宁省", "22": "吉林省", "23": "黑龙江省", "31": "上海市", "32": "江苏省",
    "33": "浙江省", "34": "安徽省", "35": "福建省", "36": "江西省", "37": "山东省",
    "41": "河南省", "42": "湖北省", "43": "湖南省", "44": "广东省", "45": "广西壮族自治区",
    "46": "海南省", "50": "重庆市", "51": "四川省", "52": "贵州省", "53": "云南省",
    "54": "西藏自治区", "61": "陕西省", "62": "甘肃省", "63": "青海省", "64": "宁夏回族自治区",
    "65": "新疆维吾尔自治区", "71": "台湾省", "81": "香港特别行政区", "82": "澳门特别行政区",
}

ACCURACY_RANK = {"": 0, "country": 1, "region": 2, "city": 3, "district": 4, "private": 5, "local": 5}


# --------------------------------------------------------------------------- #
class RateLimiter:
    """朴素令牌桶。ip-api 免费版：单查 45 次/分钟，**批量只有 15 次/分钟**。"""

    def __init__(self, limit: int, period: float = 60.0):
        self.limit = max(1, limit)
        self.period = period
        self._hits: List[float] = []
        self._lock = threading.Lock()
        self._blocked_until = 0.0

    def penalize(self, seconds: float) -> None:
        """服务端说「歇会儿」（X-Ttl / 429）时调用。"""
        with self._lock:
            self._blocked_until = max(self._blocked_until, time.monotonic() + seconds)

    def penalized(self) -> bool:
        with self._lock:
            return time.monotonic() < self._blocked_until

    def acquire(self, block: bool = True) -> bool:
        while True:
            with self._lock:
                now = time.monotonic()
                if now < self._blocked_until:
                    wait = self._blocked_until - now
                else:
                    self._hits = [t for t in self._hits if now - t < self.period]
                    if len(self._hits) < self.limit:
                        self._hits.append(now)
                        return True
                    wait = self.period - (now - self._hits[0]) + 0.05
            if not block:
                return False
            log.debug("ip-api 限流，等待 %.1fs", wait)
            time.sleep(min(wait, self.period))


# --------------------------------------------------------------------------- #
class IpIntel:
    IP_API_FIELDS = "66846719"   # 免费版可用的全部字段（去掉 PRO 专属的 accuracy 位）

    def __init__(self, cfg: IpIntelConfig, store: Optional[Store] = None):
        self.cfg = cfg
        self.store = store
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "access-monitor/1.0 (+site-visit-alerting)"})
        self._single_limiter = RateLimiter(40, 60.0)    # 官方 45，留点余量
        self._batch_limiter = RateLimiter(12, 60.0)     # 官方 15，留点余量
        self._geocn = None
        self._geocn_failed = False
        self._divisions: Dict[str, str] = {}
        self._xdb = None
        self._xdb_failed = False
        self._dns_pool = ThreadPoolExecutor(max_workers=4, thread_name_prefix="rdns")

    def close(self) -> None:
        self.session.close()
        self._dns_pool.shutdown(wait=False)
        for db in (self._geocn, self._xdb):
            try:
                if db is not None and hasattr(db, "close"):
                    db.close()
            except Exception:  # noqa: BLE001
                pass

    # ------------------------------------------------------------------ #
    def enrich_many(self, ips: Iterable[str], user_agents: Optional[Dict[str, str]] = None) -> Dict[str, IpProfile]:
        uas = user_agents or {}
        ips = [ip for ip in dict.fromkeys(ips) if ip]
        result: Dict[str, IpProfile] = {}
        base: Dict[str, IpProfile] = {}
        pending: List[str] = []
        need_rdns: List[str] = []

        for ip in ips:
            cached = self._from_cache(ip)
            if cached is None:
                pending.append(ip)
                continue
            # 缓存命中也要重新归类：爬虫判定要看**这一次**访问的 UA，
            # 不能沿用七天前那次的结论。归类是纯本地计算，不花任何 I/O。
            self._classify(cached, uas.get(ip, ""))
            result[ip] = cached
            base[ip] = cached
            if self.cfg.use_rdns and not cached.rdns_checked and not cached.is_private:
                need_rdns.append(ip)      # 上次反查超时了，这次补上

        needs_online: List[str] = []
        for ip in pending:
            prof = IpProfile(ip=ip, looked_up_at=datetime.now())
            base[ip] = prof
            if self._fill_local(prof):
                continue
            self._fill_geocn(prof)      # 层 1：国内到区县
            self._fill_ip2region(prof)  # 层 2：全球到市
            needs_online.append(ip)
            if self.cfg.use_rdns:
                need_rdns.append(ip)

        if needs_online and self.cfg.enabled:
            # 层 3：补 ASN / 代理 / 机房。批量一次搞定，比逐个查省配额得多。
            self._fill_ip_api_batch(needs_online, base)
            rdap_budget = self.cfg.rdap_max_per_cycle
            for ip in needs_online:
                prof = base[ip]
                if not prof.city and not prof.region:
                    self._fill_ipwho(prof)
                # 层 4：还没到区县、又配了腾讯 key，就再问一次
                if (self.cfg.use_qqmap and self.cfg.qqmap_key
                        and not prof.district and prof.country_code in ("CN", "")):
                    self._fill_qqmap(prof)
                # 层 5：RDAP 是串行外网请求，每轮限量。它给的「注册机构」是加分项，
                # 不值得为它把轮询节奏拖垮——剩下的 IP 下一轮再查。
                if self.cfg.use_rdap and rdap_budget > 0 and not prof.org and not prof.network:
                    self._fill_rdap(prof)
                    rdap_budget -= 1

        self._resolve_rdns(need_rdns, base)

        for ip in ips:
            prof = base.get(ip)
            if prof is None:
                continue
            self._classify(prof, uas.get(ip, ""))
            prof.ok = bool(prof.country or prof.region or prof.city or prof.rdns or prof.is_private)
            self._to_cache(prof)
            result[ip] = prof
        return result

    def _resolve_rdns(self, targets: Sequence[str], base: Dict[str, IpProfile]) -> None:
        """并发做反向 DNS，整批共享一个时间预算。

        两个坑：
        1. 线程池并发度有限，排在后面的任务可能**根本没开始跑**就被判超时。
           如果那时候把它记成「查过了，没有 PTR」，这个错误结论会被缓存七天，
           从此这个 IP 永远认不出是爬虫。所以只有真正跑完的才标记 checked。
        2. 逐个等 timeout 会让总耗时随 IP 数线性增长，几十个 IP 就能把一轮拖成几分钟。
           所以用整批统一的截止时间。
        """
        if not targets:
            return
        futures = {ip: self._dns_pool.submit(self._reverse_dns, ip) for ip in dict.fromkeys(targets)}
        deadline = time.monotonic() + max(1.0, self.cfg.rdns_budget_seconds)
        unfinished = 0
        for ip, future in futures.items():
            remaining = min(self.cfg.rdns_timeout_seconds, max(0.0, deadline - time.monotonic()))
            prof = base.get(ip)
            if prof is None:
                future.cancel()
                continue
            try:
                prof.rdns = future.result(timeout=remaining)
                prof.rdns_checked = True
            except Exception:  # noqa: BLE001
                future.cancel()
                unfinished += 1      # 没查完，不标记 checked，下一轮还会再试
        if unfinished:
            log.debug("%d 个 IP 的反向解析本轮没查完，下一轮继续", unfinished)

    def enrich(self, ip: str, user_agent: str = "") -> IpProfile:
        return self.enrich_many([ip], {ip: user_agent}).get(ip, IpProfile(ip=ip, error="查询失败"))

    # ------------------------------------------------------------------ #
    def _from_cache(self, ip: str) -> Optional[IpProfile]:
        if not self.store:
            return None
        return self.store.get_ip_profile(ip, self.cfg.cache_days, self.cfg.cache_failure_minutes)

    def _to_cache(self, prof: IpProfile) -> None:
        # 失败的结果也写进去（TTL 由 store 按 ok 标志区别对待），
        # 否则网络一抖，每 30 秒就把同一批 IP 全部重查一遍。
        if self.store:
            try:
                self.store.put_ip_profile(prof)
            except Exception as exc:  # noqa: BLE001
                log.debug("写 IP 缓存失败：%s", exc)

    @staticmethod
    def _set_if_empty(prof: IpProfile, attr: str, value) -> None:
        if value and not getattr(prof, attr):
            setattr(prof, attr, value)

    @staticmethod
    def _bump_accuracy(prof: IpProfile, level: str) -> None:
        if ACCURACY_RANK.get(level, 0) > ACCURACY_RANK.get(prof.accuracy, 0):
            prof.accuracy = level

    # ------------------------------------------------------------------ #
    # 层 0：本地
    # ------------------------------------------------------------------ #
    @staticmethod
    def _fill_local(prof: IpProfile) -> bool:
        try:
            addr = ipaddress.ip_address(prof.ip)
        except ValueError:
            prof.error = "不是合法 IP"
            return True
        if addr.is_loopback:
            prof.is_private, prof.country, prof.city = True, "本机", prof.ip
            prof.accuracy, prof.ok = "local", True
            return True
        if addr.is_private or addr.is_link_local or addr.is_reserved:
            prof.is_private = True
            prof.country = "内网"
            prof.isp = "局域网 / 校内网段"
            prof.accuracy, prof.ok = "private", True
            return True
        return False

    # ------------------------------------------------------------------ #
    # 层 1：GeoCN.mmdb（国内区县级）
    # ------------------------------------------------------------------ #
    def _load_geocn(self):
        if self._geocn is not None or self._geocn_failed:
            return self._geocn
        path = (self.cfg.geocn_mmdb or "").strip()
        if not path:
            self._geocn_failed = True
            return None
        try:
            import maxminddb  # type: ignore
            self._geocn = maxminddb.open_database(path)
            log.info("已加载 GeoCN 离线库：%s", path)
        except Exception as exc:  # noqa: BLE001
            log.warning("加载 GeoCN 失败（%s），跳过该层", exc)
            self._geocn_failed = True
            return None
        # 可选的行政区划码 -> 名称表
        divisions = Path(path).with_name("divisions.json")
        if self.cfg.divisions_json:
            divisions = Path(self.cfg.divisions_json)
        try:
            if divisions.exists():
                data = json.loads(divisions.read_text(encoding="utf-8"))
                self._divisions = {str(k): str(v) for k, v in data.items()} if isinstance(data, dict) else {}
                log.info("已加载行政区划名称表：%d 条", len(self._divisions))
        except Exception as exc:  # noqa: BLE001
            log.debug("行政区划名称表读取失败：%s", exc)
        return self._geocn

    def _fill_geocn(self, prof: IpProfile) -> None:
        db = self._load_geocn()
        if not db:
            return
        try:
            rec = db.get(prof.ip)
        except Exception as exc:  # noqa: BLE001
            log.debug("GeoCN 查询 %s 失败：%s", prof.ip, exc)
            return
        if not isinstance(rec, dict):
            return

        # GeoCN 不同版本的字段不完全一样：有的直接给中文名，有的只给 6 位区划码。两种都吃。
        for key, attr in (("country", "country"), ("province", "region"),
                          ("city", "city"), ("districts", "district"), ("district", "district")):
            value = rec.get(key)
            if isinstance(value, str):
                self._set_if_empty(prof, attr, value)

        code = str(rec.get("division_code") or rec.get("divisionCode") or "").strip()
        if code.isdigit() and len(code) == 6:
            prof.division_code = code
            self._set_if_empty(prof, "country", "中国")
            self._set_if_empty(prof, "country_code", "CN")
            self._set_if_empty(prof, "region", PROVINCE_CODES.get(code[:2], ""))
            city_name = self._divisions.get(code[:4] + "00", "")
            self._set_if_empty(prof, "city", city_name)
            # 后两位是 00 说明这条记录本身只到市级
            if not code.endswith("00"):
                self._set_if_empty(prof, "district", self._divisions.get(code, f"区划码 {code}"))

        isp = rec.get("isp")
        if isinstance(isp, str) and isp:
            self._set_if_empty(prof, "isp", isp)
            if isp == "教育网":
                prof.is_campus = True

        net_type = rec.get("type") or rec.get("net")
        if isinstance(net_type, str) and net_type:
            prof.network_type = net_type
            if net_type == "IDC":
                prof.is_datacenter = True
            elif net_type == "基站":
                prof.is_mobile = True

        if prof.district:
            self._bump_accuracy(prof, "district")
        elif prof.city:
            self._bump_accuracy(prof, "city")
        elif prof.region:
            self._bump_accuracy(prof, "region")
        prof.sources.append("GeoCN(离线)")

    # ------------------------------------------------------------------ #
    # 层 2：ip2region（全球，到市级）
    # ------------------------------------------------------------------ #
    def _load_xdb(self):
        if self._xdb is not None or self._xdb_failed:
            return self._xdb
        path = (self.cfg.ip2region_xdb or "").strip()
        if not path:
            self._xdb_failed = True
            return None
        try:
            # 官方绑定：pip install py-ip2region
            from ip2region.searcher import Searcher  # type: ignore
            from ip2region.util import load_content_from_file  # type: ignore
            self._xdb = Searcher.new_with_buffer(load_content_from_file(path))
            log.info("已加载 ip2region 离线库：%s", path)
            return self._xdb
        except Exception as exc:  # noqa: BLE001
            log.debug("py-ip2region 加载失败（%s），尝试旧版绑定", exc)
        try:
            from XdbSearchIP.xdbSearcher import XdbSearcher  # type: ignore
            self._xdb = XdbSearcher(contentBuff=XdbSearcher.loadContentFromFile(dbfile=path))
            log.info("已加载 ip2region 离线库（旧版绑定）：%s", path)
        except Exception as exc:  # noqa: BLE001
            log.warning("加载 ip2region 失败（%s），跳过该层", exc)
            self._xdb_failed = True
            self._xdb = None
        return self._xdb

    def _fill_ip2region(self, prof: IpProfile) -> None:
        if prof.city and prof.isp:
            return                      # GeoCN 已经给得更细了，不用再查
        searcher = self._load_xdb()
        if not searcher:
            return
        try:
            raw = searcher.search(prof.ip)
        except Exception as exc:  # noqa: BLE001
            log.debug("ip2region 查询 %s 失败：%s", prof.ip, exc)
            return
        if not raw:
            return
        country, region, city, isp = self._parse_ip2region(str(raw))
        for value, attr in ((country, "country"), (region, "region"), (city, "city"), (isp, "isp")):
            self._set_if_empty(prof, attr, value)
        self._bump_accuracy(prof, "city" if prof.city else "region")
        prof.sources.append("ip2region(离线)")

    @staticmethod
    def _parse_ip2region(raw: str) -> Tuple[str, str, str, str]:
        """兼容 v3 和 v2 两种字段顺序。

        v3: country|province|city|isp|countryCode      （新版，最后一段是两位国家码）
        v2: country|region|province|city|isp           （旧版，region 基本恒为 "0"）
        网上绝大多数教程写的还是 v2，照抄会把 ISP 塞进城市字段。
        """
        parts = [p.strip() for p in raw.split("|")]
        parts += [""] * (5 - len(parts))
        blank = ("", "0")
        last = parts[4]
        # 注意必须限定 ASCII：中文的「电信」也满足 len==2 and isalpha()，
        # 不加 isascii 会把 v2 的记录误判成 v3，运营商就被塞进城市字段了。
        if len(last) == 2 and last.isascii() and last.isalpha():   # v3：结尾是 CN / US 国家码
            country, region, city, isp = parts[0], parts[1], parts[2], parts[3]
        else:                                          # v2
            country, region, city, isp = parts[0], parts[2], parts[3], parts[4]
        clean = lambda v: "" if v in blank else v      # noqa: E731
        return clean(country), clean(region), clean(city), clean(isp)

    # ------------------------------------------------------------------ #
    # 层 3：ip-api.com（补 ASN / 代理 / 机房）
    # ------------------------------------------------------------------ #
    def _fill_ip_api_batch(self, ips: Sequence[str], base: Dict[str, IpProfile]) -> None:
        if not self.cfg.use_ip_api:
            return
        for start in range(0, len(ips), 100):
            chunk = list(ips[start:start + 100])
            if len(chunk) == 1:
                self._fill_ip_api_single(base[chunk[0]])
                continue
            self._batch_limiter.acquire()
            try:
                # 免费版只支持 http，写成 https 是最常见的踩坑
                resp = self.session.post(
                    "http://ip-api.com/batch",
                    params={"fields": self.IP_API_FIELDS, "lang": self.cfg.ip_api_lang},
                    json=[{"query": ip} for ip in chunk],
                    timeout=self.cfg.timeout_seconds,
                )
                self._respect_rate_headers(resp, self._batch_limiter)
                resp.raise_for_status()
                payload = resp.json()
            except Exception as exc:  # noqa: BLE001
                if self._batch_limiter.penalized():
                    # 刚被限流罚站，再逐个去查只会每个都阻塞一次 X-Ttl，
                    # 一批 IP 就能把主循环卡住好几分钟，而且更容易被封。
                    log.warning("ip-api 限流中，本轮跳过在线查询（%s）", exc)
                    return
                log.warning("ip-api 批量查询失败（%s），改逐个查", exc)
                for ip in chunk:
                    self._fill_ip_api_single(base[ip])
                continue
            if isinstance(payload, list):
                for item in payload:
                    prof = base.get(item.get("query", "")) if isinstance(item, dict) else None
                    if prof is not None:
                        self._apply_ip_api(prof, item)

    def _fill_ip_api_single(self, prof: IpProfile) -> None:
        self._single_limiter.acquire()
        try:
            resp = self.session.get(
                f"http://ip-api.com/json/{prof.ip}",
                params={"fields": self.IP_API_FIELDS, "lang": self.cfg.ip_api_lang},
                timeout=self.cfg.timeout_seconds,
            )
            self._respect_rate_headers(resp, self._single_limiter)
            resp.raise_for_status()
            self._apply_ip_api(prof, resp.json())
        except Exception as exc:  # noqa: BLE001
            log.debug("ip-api 查询 %s 失败：%s", prof.ip, exc)

    @staticmethod
    def _respect_rate_headers(resp, limiter: RateLimiter) -> None:
        """ip-api 用 X-Rl（剩余次数）和 X-Ttl（多少秒后重置）告诉你还能打几次。
        撞上限会被封 IP，所以老老实实退避。"""
        try:
            remaining = int(resp.headers.get("X-Rl", "1"))
            ttl = int(resp.headers.get("X-Ttl", "0"))
        except (TypeError, ValueError):
            return
        if resp.status_code == 429 or remaining <= 0:
            limiter.penalize(max(ttl, 5))
            log.warning("ip-api 达到速率上限，暂停 %d 秒", max(ttl, 5))

    def _apply_ip_api(self, prof: IpProfile, data: dict) -> None:
        if not isinstance(data, dict) or data.get("status") != "success":
            if isinstance(data, dict) and data.get("message"):
                prof.error = prof.error or f"ip-api: {data['message']}"
            return
        for src, dst in (("country", "country"), ("countryCode", "country_code"),
                         ("regionName", "region"), ("city", "city"), ("district", "district"),
                         ("zip", "zip_code"), ("timezone", "timezone"), ("isp", "isp"),
                         ("org", "org"), ("asname", "as_name"), ("reverse", "rdns")):
            value = data.get(src)
            if isinstance(value, str):
                self._set_if_empty(prof, dst, value.strip())
        if data.get("as") and not prof.asn:
            bits = str(data["as"]).split()
            prof.asn = bits[0]
            self._set_if_empty(prof, "as_name", " ".join(bits[1:]))
        if prof.lat is None and isinstance(data.get("lat"), (int, float)):
            prof.lat, prof.lon = float(data["lat"]), float(data.get("lon") or 0.0)
        prof.is_mobile = prof.is_mobile or bool(data.get("mobile"))
        prof.is_proxy = prof.is_proxy or bool(data.get("proxy"))
        prof.is_datacenter = prof.is_datacenter or bool(data.get("hosting"))
        self._bump_accuracy(prof, "district" if prof.district else ("city" if prof.city else "region"))
        prof.sources.append("ip-api.com")

    # ------------------------------------------------------------------ #
    def _fill_ipwho(self, prof: IpProfile) -> None:
        """纯 HTTPS 的免费兜底（有些校园网禁明文 HTTP，ip-api 免费版又只有 HTTP）。"""
        try:
            resp = self.session.get(f"https://ipwho.is/{prof.ip}", timeout=self.cfg.timeout_seconds)
            resp.raise_for_status()
            data = resp.json()
        except Exception as exc:  # noqa: BLE001
            log.debug("ipwho.is 查询 %s 失败：%s", prof.ip, exc)
            return
        if not data.get("success"):
            return
        for src, dst in (("country", "country"), ("country_code", "country_code"),
                         ("region", "region"), ("city", "city"), ("postal", "zip_code")):
            if data.get(src):
                self._set_if_empty(prof, dst, str(data[src]))
        conn = data.get("connection") or {}
        self._set_if_empty(prof, "isp", conn.get("isp"))
        self._set_if_empty(prof, "org", conn.get("org"))
        if conn.get("asn"):
            self._set_if_empty(prof, "asn", f"AS{conn['asn']}")
        if prof.lat is None and data.get("latitude") is not None:
            prof.lat, prof.lon = float(data["latitude"]), float(data.get("longitude") or 0.0)
        self._bump_accuracy(prof, "city" if prof.city else "region")
        prof.sources.append("ipwho.is")

    def _fill_qqmap(self, prof: IpProfile) -> None:
        """腾讯位置服务：目前唯一「国内基本都能到区/县」的在线 API，个人 key 每天 1 万次。"""
        try:
            resp = self.session.get(
                "https://apis.map.qq.com/ws/location/v1/ip",
                params={"ip": prof.ip, "key": self.cfg.qqmap_key},
                timeout=self.cfg.timeout_seconds,
            )
            resp.raise_for_status()
            data = resp.json()
        except Exception as exc:  # noqa: BLE001
            log.debug("腾讯位置服务查询 %s 失败：%s", prof.ip, exc)
            return
        if data.get("status") != 0:
            log.debug("腾讯位置服务返回错误：%s", data.get("message"))
            return
        info = (data.get("result") or {}).get("ad_info") or {}
        for src, dst in (("nation", "country"), ("province", "region"),
                         ("city", "city"), ("district", "district")):
            if info.get(src):
                self._set_if_empty(prof, dst, str(info[src]))
        if info.get("adcode"):
            self._set_if_empty(prof, "division_code", str(info["adcode"]))
        location = (data.get("result") or {}).get("location") or {}
        if prof.lat is None and location.get("lat") is not None:
            prof.lat, prof.lon = float(location["lat"]), float(location.get("lng") or 0.0)
        self._bump_accuracy(prof, "district" if prof.district else "city")
        prof.sources.append("腾讯位置服务")

    # ------------------------------------------------------------------ #
    @staticmethod
    def _reverse_dns(ip: str) -> str:
        """反查主机名。

        注意这里**没有**用 socket.setdefaulttimeout —— 那是进程级全局设置，
        在工作线程里改会波及同时在跑的 HTTP 请求。超时改由调用方
        future.result(timeout=...) 控制，卡住的线程让它自己慢慢退。
        """
        try:
            return socket.gethostbyaddr(ip)[0]
        except Exception:  # noqa: BLE001
            return ""

    def _fill_rdap(self, prof: IpProfile) -> None:
        try:
            resp = self.session.get(f"https://rdap.org/ip/{prof.ip}", timeout=self.cfg.timeout_seconds)
            if resp.status_code != 200:
                return
            data = resp.json()
        except Exception as exc:  # noqa: BLE001
            log.debug("RDAP 查询 %s 失败：%s", prof.ip, exc)
            return
        start, end = data.get("startAddress"), data.get("endAddress")
        if data.get("handle"):
            prof.network = str(data["handle"])
        elif start and end:
            prof.network = f"{start} - {end}"
        self._set_if_empty(prof, "org", data.get("name"))
        for entity in data.get("entities", []) or []:
            vcard = (entity.get("vcardArray") or [None, []])
            for item in (vcard[1] if len(vcard) > 1 else []) or []:
                if isinstance(item, list) and len(item) >= 4 and item[0] == "fn":
                    self._set_if_empty(prof, "org", str(item[3]))
        prof.sources.append("RDAP")

    # ------------------------------------------------------------------ #
    def _classify(self, prof: IpProfile, user_agent: str = "") -> None:
        haystack = " ".join([prof.rdns, prof.org, prof.isp, prof.as_name, prof.network]).lower()
        rdns = (prof.rdns or "").lower().rstrip(".")

        # 爬虫：先看反向域名（可信），再看 UA（可伪造，只算「疑似」）
        for suffix, name in BOT_RDNS_SUFFIXES.items():
            if rdns.endswith(suffix):
                prof.is_bot, prof.bot_name, prof.bot_evidence = True, name, "反向域名"
                break
        if not prof.is_bot and user_agent:
            ua = user_agent.lower()
            for pattern, name in BOT_UA_PATTERNS:
                if pattern in ua:
                    prof.is_bot, prof.bot_name, prof.bot_evidence = True, name, "UA（可伪造）"
                    break
            else:
                if any(h in ua for h in TOOL_UA_HINTS):
                    prof.is_bot = True
                    prof.bot_name = f"疑似程序访问（{user_agent[:36]}）"
                    prof.bot_evidence = "UA（可伪造）"

        # 校园网 / 教育网
        if not prof.is_campus:
            campus_hay = f"{haystack} {prof.city} {prof.region} {prof.country}".lower()
            if any(kw and kw.lower() in campus_hay for kw in self.cfg.campus_keywords):
                prof.is_campus = True
        if prof.asn.upper().lstrip("AS") in ("4538", "23910"):
            prof.is_campus = True

        if not prof.is_datacenter:
            prof.is_datacenter = any(h in haystack for h in DATACENTER_HINTS)

        score, reasons = 0, []
        if prof.is_proxy:
            score += 40
            reasons.append("疑似代理 / VPN 出口")
        if prof.is_datacenter:
            score += 25
            reasons.append("来自机房或云主机，不是家庭宽带")
        if prof.country_code and prof.country_code != "CN":
            score += 20
            reasons.append(f"境外来源：{prof.country}")
        if prof.is_bot:
            score = max(0, score - 15)
            reasons.append(f"识别为爬虫：{prof.bot_name}（依据：{prof.bot_evidence}）")
        if prof.is_campus:
            score = max(0, score - 20)
            reasons.append("校园网 / 教育网内部")
        if prof.is_mobile:
            reasons.append("移动蜂窝网络")
        if prof.network_type:
            reasons.append(f"网络类型：{prof.network_type}")
        if not prof.ok and not prof.is_private:
            score += 5
            reasons.append("未查到归属信息")
        prof.risk_score = max(0, min(100, score))
        prof.risk_reasons = reasons

    # ------------------------------------------------------------------ #
    @staticmethod
    def map_link(prof: IpProfile) -> str:
        if prof.lat is None or prof.lon is None:
            return ""
        return f"https://www.openstreetmap.org/?mlat={prof.lat}&mlon={prof.lon}#map=11/{prof.lat}/{prof.lon}"
