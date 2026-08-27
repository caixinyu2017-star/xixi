"""告警推送。

支持一堆通道，配了哪个发哪个；一个都没配也不会崩——控制台通道永远在，
至少能在终端看到告警。国内用户推荐组合：**邮件（留档、信息全）+ Bark 或 企业微信机器人（秒到手机）**。

所有通道都做了超时和异常隔离：某个通道挂了不影响其它通道，也不会把主循环带崩。
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import logging
import re
import smtplib
import time
import urllib.parse
from dataclasses import dataclass
from datetime import datetime, timedelta
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, formatdate
from typing import Any, Dict, List, Optional, Tuple

import requests

from .config import NotifyConfig
from .models import Alert
from .report import render_html, render_markdown, render_short, render_text

log = logging.getLogger(__name__)


@dataclass
class DeliveryResult:
    channel: str
    ok: bool
    message: str = ""


# --------------------------------------------------------------------------- #
class Channel:
    name = "base"

    def __init__(self, conf: Dict[str, Any]):
        self.conf = conf or {}
        self.timeout = int(self.conf.get("timeout", 10))

    #: 这个通道必须配齐的字段；缺一个就说明用户还没配好
    required_keys: Tuple[str, ...] = ()

    @property
    def enabled(self) -> bool:
        return bool(self.conf.get("enabled", True))

    @property
    def missing(self) -> List[str]:
        """还缺哪些配置项。启动时统一提示一次，省得每条告警都报一次错。"""
        return [k for k in self.required_keys if not self.conf.get(k)]

    def send(self, alert: Alert) -> DeliveryResult:  # pragma: no cover - 由子类实现
        raise NotImplementedError

    # 小工具
    @staticmethod
    def _post_json(url: str, payload: dict, timeout: int, params: Optional[dict] = None) -> Tuple[bool, str]:
        resp = requests.post(url, json=payload, params=params, timeout=timeout)
        text = (resp.text or "")[:300]
        return resp.status_code < 400, f"HTTP {resp.status_code} {text}"


class ConsoleChannel(Channel):
    """兜底通道：永远启用，直接打到终端和日志。"""
    name = "console"

    @property
    def enabled(self) -> bool:
        return bool(self.conf.get("enabled", True))

    def send(self, alert: Alert) -> DeliveryResult:
        body = render_text(alert)
        print("\n" + "=" * 66 + f"\n{body}\n" + "=" * 66, flush=True)
        log.warning("告警：%s", alert.title)
        return DeliveryResult(self.name, True, "已输出到终端")


class EmailChannel(Channel):
    """SMTP 邮件。QQ 邮箱 / 163 用的是「授权码」，不是登录密码。"""
    name = "email"
    required_keys = ("host", "username", "password", "to")

    def send(self, alert: Alert) -> DeliveryResult:
        c = self.conf
        host = c.get("host") or ""
        port = int(c.get("port") or 465)
        username = c.get("username") or ""
        password = c.get("password") or ""
        sender = c.get("from") or username
        to = c.get("to") or []
        if isinstance(to, str):
            to = [x.strip() for x in to.replace(";", ",").split(",") if x.strip()]
        if not (host and username and password and to):
            return DeliveryResult(self.name, False, "邮件配置不完整（host/username/password/to）")

        msg = MIMEMultipart("alternative")
        msg["Subject"] = Header(alert.title, "utf-8")
        msg["From"] = formataddr((str(Header(c.get("from_name", "网站访问监控"), "utf-8")), sender))
        msg["To"] = ", ".join(to)
        msg["Date"] = formatdate(localtime=True)
        msg.attach(MIMEText(render_text(alert), "plain", "utf-8"))
        msg.attach(MIMEText(render_html(alert), "html", "utf-8"))

        use_ssl = bool(c.get("ssl", port == 465))
        try:
            if use_ssl:
                server = smtplib.SMTP_SSL(host, port, timeout=self.timeout)
            else:
                server = smtplib.SMTP(host, port, timeout=self.timeout)
                if c.get("starttls", port == 587):
                    server.starttls()
            with server:
                server.login(username, password)
                server.sendmail(sender, to, msg.as_string())
        except smtplib.SMTPAuthenticationError:
            return DeliveryResult(self.name, False,
                                  "SMTP 认证失败：QQ/163 邮箱这里要填「授权码」而不是邮箱登录密码")
        except Exception as exc:  # noqa: BLE001
            return DeliveryResult(self.name, False, f"{type(exc).__name__}: {exc}")
        return DeliveryResult(self.name, True, f"已发送给 {', '.join(to)}")


class BarkChannel(Channel):
    """Bark（iOS）。App 里能直接拿到 key。level=critical 可以突破静音。"""
    name = "bark"
    required_keys = ("key",)

    def send(self, alert: Alert) -> DeliveryResult:
        key = self.conf.get("key") or ""
        if not key:
            return DeliveryResult(self.name, False, "缺少 bark key")
        server = (self.conf.get("server") or "https://api.day.app").rstrip("/")
        payload = {
            "title": alert.title[:100],
            "body": render_short(alert, 300),
            "group": self.conf.get("group") or "网站访问监控",
            # 配置里留空就按告警级别自动选：timeSensitive 能穿透专注模式，critical 能突破静音
            "level": self.conf.get("level") or ("critical" if alert.severity == "critical" else "timeSensitive"),
            "sound": self.conf.get("sound") or "alarm",
            "isArchive": 1,
        }
        if payload["level"] == "critical" and self.conf.get("volume") is not None:
            payload["volume"] = self.conf["volume"]      # volume 只对 critical 生效
        if alert.dedup_key:
            # 同一次突发就更新同一条通知，而不是在锁屏上堆一长串
            payload["id"] = hashlib.md5(alert.dedup_key.encode("utf-8")).hexdigest()[:16]
        try:
            resp = requests.post(f"{server}/{key}", json=payload, timeout=self.timeout)
            data = resp.json() if resp.content else {}
        except Exception as exc:  # noqa: BLE001
            return DeliveryResult(self.name, False, f"{type(exc).__name__}: {exc}")
        ok = resp.status_code < 400 and (not isinstance(data, dict) or data.get("code", 200) == 200)
        return DeliveryResult(self.name, ok, str(data)[:200] or f"HTTP {resp.status_code}")


class ServerChanChannel(Channel):
    """Server酱：老版 sctapi.ftqq.com，Server酱³ 用 https://<uid>.push.ft07.com/send/<key>.send"""
    name = "serverchan"

    @property
    def missing(self) -> List[str]:
        return [] if (self.conf.get("sendkey") or self.conf.get("url")) else ["sendkey"]

    #: Server酱³ 的 SendKey 形如 sctp<uid>t<随机串>，uid 就夹在 sctp 和 t 之间
    _SCT3_RE = re.compile(r"^sctp(\d+)t", re.IGNORECASE)

    def endpoint(self) -> str:
        """按 SendKey 前缀自动区分 Server酱³ 和老版 Turbo，不用用户自己填 uid。"""
        if self.conf.get("url"):
            return str(self.conf["url"])
        sendkey = self.conf.get("sendkey") or ""
        m = self._SCT3_RE.match(sendkey)
        if m:
            return f"https://{m.group(1)}.push.ft07.com/send/{sendkey}.send"
        uid = self.conf.get("uid") or ""
        if uid:
            return f"https://{uid}.push.ft07.com/send/{sendkey}.send"
        return f"https://sctapi.ftqq.com/{sendkey}.send"

    def send(self, alert: Alert) -> DeliveryResult:
        if not (self.conf.get("sendkey") or self.conf.get("url")):
            return DeliveryResult(self.name, False, "缺少 sendkey")
        try:
            resp = requests.post(self.endpoint(),
                                 data={"title": alert.title[:32], "desp": render_markdown(alert)},
                                 timeout=self.timeout)
        except Exception as exc:  # noqa: BLE001
            return DeliveryResult(self.name, False, f"{type(exc).__name__}: {exc}")
        try:
            data = resp.json() if resp.content else {}
        except ValueError:
            return DeliveryResult(self.name, resp.status_code < 400, f"HTTP {resp.status_code}")
        # Server酱 也是 HTTP 200 + body 里带错误码，不能只看状态码
        code = data.get("code", data.get("errno", 0))
        ok = resp.status_code < 400 and code in (0, 200)
        note = "" if ok else "（Turbo 免费版每天只有 5 条）"
        return DeliveryResult(self.name, ok, f"{str(data)[:200]}{note}")


class PushPlusChannel(Channel):
    name = "pushplus"
    required_keys = ("token",)

    def send(self, alert: Alert) -> DeliveryResult:
        token = self.conf.get("token") or ""
        if not token:
            return DeliveryResult(self.name, False, "缺少 token")
        payload = {"token": token, "title": alert.title[:100],
                   "content": render_html(alert), "template": "html"}
        if self.conf.get("topic"):
            payload["topic"] = self.conf["topic"]
        try:
            resp = requests.post("https://www.pushplus.plus/send", json=payload, timeout=self.timeout)
            data = resp.json() if resp.content else {}
        except Exception as exc:  # noqa: BLE001
            return DeliveryResult(self.name, False, f"{type(exc).__name__}: {exc}")
        code = data.get("code") if isinstance(data, dict) else None
        ok = resp.status_code < 400 and code == 200
        hint = {905: "（需要先完成实名认证）", 900: "（已达每日上限或被限制推送）"}.get(code, "")
        # 注意：code=200 只代表「已受理」，实际投递是异步的
        return DeliveryResult(self.name, ok, f"{str(data)[:200]}{hint}")


class WecomChannel(Channel):
    """企业微信群机器人。markdown 内容上限约 4096 字节。"""
    name = "wecom"
    required_keys = ("key",)

    def send(self, alert: Alert) -> DeliveryResult:
        key = self.conf.get("key") or ""
        if not key:
            return DeliveryResult(self.name, False, "缺少机器人 key")
        content = render_markdown(alert)
        content = content.encode("utf-8")[:4000].decode("utf-8", "ignore")
        payload = {"msgtype": "markdown", "markdown": {"content": content}}
        try:
            resp = requests.post("https://qyapi.weixin.qq.com/cgi-bin/webhook/send",
                                 params={"key": key}, json=payload, timeout=self.timeout)
            data = resp.json() if resp.content else {}
            ok = resp.status_code < 400 and data.get("errcode", 0) == 0
            return DeliveryResult(self.name, ok, str(data)[:200])
        except Exception as exc:  # noqa: BLE001
            return DeliveryResult(self.name, False, f"{type(exc).__name__}: {exc}")


class DingTalkChannel(Channel):
    """钉钉自定义机器人。安全设置选「加签」时必须带 timestamp+sign；
    选「自定义关键词」时正文里必须出现那个关键词（用 keyword 配置项加上）。"""
    name = "dingtalk"
    required_keys = ("token",)

    def send(self, alert: Alert) -> DeliveryResult:
        token = self.conf.get("token") or ""
        if not token:
            return DeliveryResult(self.name, False, "缺少 access_token")
        url = "https://oapi.dingtalk.com/robot/send"
        params = {"access_token": token}
        secret = self.conf.get("secret") or ""
        if secret:
            ts = str(round(time.time() * 1000))
            string_to_sign = f"{ts}\n{secret}"
            digest = hmac.new(secret.encode("utf-8"), string_to_sign.encode("utf-8"),
                              hashlib.sha256).digest()
            params["timestamp"] = ts
            params["sign"] = urllib.parse.quote_plus(base64.b64encode(digest))
        keyword = self.conf.get("keyword") or ""
        title = f"{keyword} {alert.title}".strip() if keyword else alert.title
        text = render_markdown(alert)
        if keyword and keyword not in text:
            text = f"{keyword}\n\n{text}"
        payload = {"msgtype": "markdown", "markdown": {"title": title[:60], "text": text}}
        if self.conf.get("at_mobiles"):
            payload["at"] = {"atMobiles": list(self.conf["at_mobiles"]), "isAtAll": False}
        elif self.conf.get("at_all"):
            payload["at"] = {"isAtAll": True}
        try:
            resp = requests.post(url, params=params, json=payload, timeout=self.timeout)
            data = resp.json() if resp.content else {}
            ok = resp.status_code < 400 and data.get("errcode", 0) == 0
            return DeliveryResult(self.name, ok, str(data)[:200])
        except Exception as exc:  # noqa: BLE001
            return DeliveryResult(self.name, False, f"{type(exc).__name__}: {exc}")


class FeishuChannel(Channel):
    """飞书自定义机器人。加签算法和钉钉不同：用 "timestamp\\nsecret" 当 **密钥**，对空消息做 HMAC。"""
    name = "feishu"
    required_keys = ("token",)

    def send(self, alert: Alert) -> DeliveryResult:
        token = self.conf.get("token") or ""
        if not token:
            return DeliveryResult(self.name, False, "缺少 webhook token")
        payload: Dict[str, Any] = {
            "msg_type": "text",
            "content": {"text": f"{alert.title}\n\n{render_text(alert)[:3000]}"},
        }
        secret = self.conf.get("secret") or ""
        if secret:
            ts = str(int(time.time()))
            digest = hmac.new(f"{ts}\n{secret}".encode("utf-8"), b"", hashlib.sha256).digest()
            payload["timestamp"] = ts
            payload["sign"] = base64.b64encode(digest).decode("utf-8")
        try:
            resp = requests.post(f"https://open.feishu.cn/open-apis/bot/v2/hook/{token}",
                                 json=payload, timeout=self.timeout)
            data = resp.json() if resp.content else {}
            ok = resp.status_code < 400 and data.get("code", 0) == 0
            return DeliveryResult(self.name, ok, str(data)[:200])
        except Exception as exc:  # noqa: BLE001
            return DeliveryResult(self.name, False, f"{type(exc).__name__}: {exc}")


class TelegramChannel(Channel):
    """Telegram。注意：大陆网络环境下通常需要代理才能连上。"""
    name = "telegram"
    required_keys = ("bot_token", "chat_id")

    def send(self, alert: Alert) -> DeliveryResult:
        token = self.conf.get("bot_token") or ""
        chat_id = self.conf.get("chat_id") or ""
        if not (token and chat_id):
            return DeliveryResult(self.name, False, "缺少 bot_token 或 chat_id")
        proxies = {"http": self.conf["proxy"], "https": self.conf["proxy"]} if self.conf.get("proxy") else None
        payload = {"chat_id": chat_id, "text": render_text(alert)[:4000], "disable_web_page_preview": True}
        try:
            resp = requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                                 json=payload, timeout=self.timeout, proxies=proxies)
            return DeliveryResult(self.name, resp.status_code < 400, f"HTTP {resp.status_code} {resp.text[:200]}")
        except Exception as exc:  # noqa: BLE001
            return DeliveryResult(self.name, False, f"{type(exc).__name__}: {exc}")


class WebhookChannel(Channel):
    """通用 webhook：把告警整个 JSON POST 出去，接到自己的系统里。"""
    name = "webhook"
    required_keys = ("url",)

    def send(self, alert: Alert) -> DeliveryResult:
        url = self.conf.get("url") or ""
        if not url:
            return DeliveryResult(self.name, False, "缺少 url")
        try:
            resp = requests.post(url, json=alert.to_dict(),
                                 headers=self.conf.get("headers") or {}, timeout=self.timeout)
            return DeliveryResult(self.name, resp.status_code < 400, f"HTTP {resp.status_code}")
        except Exception as exc:  # noqa: BLE001
            return DeliveryResult(self.name, False, f"{type(exc).__name__}: {exc}")


CHANNEL_TYPES = {
    "console": ConsoleChannel,
    "email": EmailChannel,
    "bark": BarkChannel,
    "serverchan": ServerChanChannel,
    "pushplus": PushPlusChannel,
    "wecom": WecomChannel,
    "dingtalk": DingTalkChannel,
    "feishu": FeishuChannel,
    "telegram": TelegramChannel,
    "webhook": WebhookChannel,
}


# --------------------------------------------------------------------------- #
class NotificationHub:
    """统一调度：冷却、限流、多通道分发。"""

    def __init__(self, cfg: NotifyConfig, store=None):
        self.cfg = cfg
        self.store = store
        self.channels: List[Channel] = []
        self.skipped: List[str] = []
        conf = dict(cfg.channels or {})
        conf.setdefault("console", {"enabled": True})
        for name, channel_conf in conf.items():
            cls = CHANNEL_TYPES.get(name)
            if cls is None:
                log.warning("未知的通知通道「%s」，已忽略", name)
                continue
            channel = cls(channel_conf or {})
            if not channel.enabled:
                continue
            if channel.missing:
                # 开着但没配全：提示一次就跳过，别让每条告警都刷一遍错误日志
                log.warning("通道「%s」已启用但缺少配置：%s —— 本次运行将跳过它",
                            channel.name, "、".join(channel.missing))
                self.skipped.append(channel.name)
                continue
            self.channels.append(channel)
        log.info("已启用通知通道：%s", ", ".join(c.name for c in self.channels) or "无")

    # ---- 节流 ----
    def should_send(self, alert: Alert, now: Optional[datetime] = None) -> Tuple[bool, str]:
        if not self.cfg.enabled:
            return False, "通知总开关关闭"
        if not self.store:
            return True, ""
        now = now or datetime.now()
        last = self.store.last_alert_ts(rule=alert.rule)
        if last is not None:
            elapsed = now.timestamp() - last
            if elapsed < self.cfg.cooldown_seconds:
                return False, (f"冷却中（{alert.rule} 距上次 {int(elapsed)} 秒 "
                               f"< {self.cfg.cooldown_seconds} 秒），本批记录会并入下次告警")
        if self.cfg.max_alerts_per_hour > 0:
            sent = self.store.alerts_since(now - timedelta(hours=1))
            if sent >= self.cfg.max_alerts_per_hour:
                return False, f"已达每小时上限（{self.cfg.max_alerts_per_hour} 条）"
        return True, ""

    def dispatch(self, alert: Alert) -> List[DeliveryResult]:
        results: List[DeliveryResult] = []
        for channel in self.channels:
            try:
                result = channel.send(alert)
            except Exception as exc:  # noqa: BLE001
                result = DeliveryResult(channel.name, False, f"未捕获异常 {type(exc).__name__}: {exc}")
            results.append(result)
            level = log.info if result.ok else log.error
            level("通道 %s：%s %s", result.channel, "成功" if result.ok else "失败", result.message)
        return results

    def test(self) -> List[DeliveryResult]:
        """发一条假告警，用来验证配置。"""
        from .models import IpProfile, VisitRecord
        now = datetime.now()
        prof = IpProfile(
            ip="223.104.3.77", ok=True, country="中国", country_code="CN", region="浙江省",
            city="嘉兴市", district="南湖区", isp="中国移动", asn="AS9808",
            as_name="China Mobile", rdns="", accuracy="district",
            lat=30.746, lon=120.755, sources=["测试数据"], risk_score=10,
            risk_reasons=["这是一条测试告警，用来确认推送通道能不能收到"],
        )
        records = [
            VisitRecord(ip="223.104.3.77", visited_at=now, page="https://example.edu.cn/index.htm",
                        page_title="首页", user_agent="Chrome 128", first_seen_at=now)
            for _ in range(3)
        ]
        alert = Alert(
            rule="test", severity="warning", title="✅ 测试告警：通知通道连通性检查",
            summary="如果你收到了这条消息，说明推送配置正确，真出事时也能收到。",
            triggered_at=now, records=records, profiles={"223.104.3.77": prof}, dedup_key="test",
        )
        return self.dispatch(alert)
