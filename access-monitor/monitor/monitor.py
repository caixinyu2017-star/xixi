"""主循环：登录 → 抓取 → 解析 → 去重 → 检测 → 查 IP → 告警。

每轮只做一件正经事：把「最近访问记录」这张表拉下来，和上一轮比，多出来的就是新访问。
新访问进检测器，命中突发规则就查 IP、发告警。

抗折腾的几处设计：
  * 会话掉了自动重新登录（验证码能自动识别就不用管，识别不了会在终端提示）；
  * 记录页地址会被记住，掉线或改版时自动重新点菜单找；
  * 连续出错会退避，不会疯狂重试把 WebVPN 打爆；
  * 被冷却压下去的告警不会丢，会并进下一次发出去。
"""
from __future__ import annotations

import logging
import random
import signal
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from .config import AppConfig
from .detector import BurstDetector
from .ipintel import IpIntel
from .models import Alert, IpProfile, VisitRecord
from .navigator import RecordsNavigator
from .notify import NotificationHub
from .parser import parse_records
from .session import BrowserSession, LoginError
from .store import Store

log = logging.getLogger(__name__)


class AccessMonitor:
    def __init__(self, cfg: AppConfig, use_ocr: bool = True):
        self.cfg = cfg
        cfg.ensure_dirs()
        self.store = Store(cfg.state_path / "monitor.sqlite")
        self.detector = BurstDetector(cfg.rules)
        self.ipintel = IpIntel(cfg.ipintel, self.store)
        self.notifier = NotificationHub(cfg.notify, self.store,
                                       rule_cooldown_seconds=cfg.rules.cooldown_seconds)
        self.session = BrowserSession(cfg, use_ocr=use_ocr)
        self.navigator: Optional[RecordsNavigator] = None
        # 还没送出去的告警（被冷却压住的，或者所有通道都投递失败的）。
        # 存的是**告警对象本身**而不是零散记录：靠「下一轮重新成簇」来补发是不可靠的，
        # 抑制一旦超过检测窗口，那些记录就滑出窗口再也凑不成簇，告警会无声消失。
        self._deferred: List[Dict[str, object]] = []
        self._consecutive_errors = 0
        self._stop = False
        self._cycles = 0
        self._skew_warned = False
        self._last_prune = datetime.now()

    # ------------------------------------------------------------------ #
    def start(self) -> None:
        self.session.start()
        self.navigator = RecordsNavigator(self.cfg, self.session, self.store)
        outcome = self.session.ensure_logged_in()
        if not outcome.ok:
            raise LoginError(outcome.message or "登录失败")
        log.info("登录就绪（%s）", outcome.message or f"尝试 {outcome.attempts} 次")

    def close(self) -> None:
        try:
            self.session.close()
        finally:
            self.ipintel.close()
            self.store.close()

    def __enter__(self) -> "AccessMonitor":
        self.start()
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    # ------------------------------------------------------------------ #
    def run_once(self) -> Dict[str, object]:
        """跑一轮。返回这轮的统计，方便 --once 模式打印。"""
        assert self.navigator is not None, "请先调用 start()"
        now = datetime.now()
        self._cycles += 1

        fetch = self.navigator.fetch()
        if fetch.logged_out:
            log.warning("会话已过期，正在重新登录…")
            outcome = self.session.ensure_logged_in(force=True)
            if not outcome.ok:
                raise LoginError(outcome.message or "重新登录失败")
            fetch = self.navigator.fetch(force_rediscover=True)

        if not fetch.html or not fetch.verified:
            # verified=False 说明拿到的页面不能确认是记录页。**绝不能**硬着头皮去解析：
            # 解析器最后一层是全文正则捞 IP，啃错页面会捞出一堆时间戳相同的垃圾记录，
            # 直接触发一次假突发告警。
            self._consecutive_errors += 1
            log.error("第 %d 次抓取失败：%s", self._consecutive_errors, fetch.error or "未知原因")
            if self._consecutive_errors == 2:
                self.navigator.dump("fetch-fail")
            return {"ok": False, "error": fetch.error}

        records = parse_records(fetch.html, reference_time=now)
        if not records and fetch.record_count == 0:
            # 页面打开了但一条都没有：可能确实没访问，也可能页面结构变了
            log.info("本轮未解析到记录（页面可能暂时没有访问数据）")
        self._consecutive_errors = 0

        max_rows = self.cfg.poll.max_rows
        if max_rows and len(records) > max_rows:
            records = records[:max_rows]

        # 这是一次 DISTINCT 全表扫，只有「首次出现的 IP」规则真的开着才值得付这个代价
        known_ips_before = self.store.all_known_ips() if self.cfg.rules.new_ip_enabled else None
        first_run = self.store.is_empty()
        new_records = self.store.filter_new(records)
        for rec in new_records:
            rec.first_seen_at = now
        self.store.add_records(new_records, now)

        if first_run and self.cfg.rules.baseline_on_first_run:
            log.info("首次运行：把当前 %d 条记录作为基线，不告警。下一轮开始才会检测突发。",
                     len(new_records))
            return {"ok": True, "records": len(records), "new": len(new_records),
                    "baseline": True, "alerts": 0}

        if not new_records:
            # 没有新记录也要走一遍补发：上一轮可能有告警被冷却压着
            sent = self._flush_deferred(now)
            log.info("本轮无新增（页面共 %d 条）%s", len(records),
                     f"，补发了 %d 条挂起告警" % sent if sent else "")
            return {"ok": True, "records": len(records), "new": 0, "alerts": sent,
                    "deferred": len(self._deferred)}

        log.info("本轮新增 %d 条（页面共 %d 条）", len(new_records), len(records))

        # 检测窗口按「我们什么时候看到这条记录」来取，而不是按后台标注的访问时间。
        # 原因：后台服务器的时钟未必和这台电脑一致。差个十几分钟的话，
        # 按访问时间取窗口会一条都捞不到，突发检测就**静默失效**了——最坏的一种坏。
        # 而簇内的疏密仍然按访问时间算，那是相对量，不受时钟偏移影响。
        window = max(self.cfg.rules.burst_window_seconds, self.cfg.rules.ip_burst_window_seconds)
        window_records = self.store.records_since(
            now - timedelta(seconds=window * 2 + 60), use_visit_time=False
        )
        self._warn_on_clock_skew(new_records, now)

        profiles = self._enrich(new_records, window_records)

        alerted = self.store.alerted_keys([r.key for r in window_records])
        alerts = self.detector.detect(
            new_records, window_records, profiles,
            known_ips_before=known_ips_before, now=now, alerted_keys=alerted,
        )

        # 先补发上一轮压住的，再处理这一轮新发现的
        sent = self._flush_deferred(now)
        for alert in alerts:
            sent += 1 if self._deliver(alert, now) else 0

        self._housekeeping(now)
        return {"ok": True, "records": len(records), "new": len(new_records),
                "alerts": sent, "deferred": len(self._deferred)}

    # ------------------------------------------------------------------ #
    def _enrich(self, new_records, window_records) -> Dict[str, IpProfile]:
        if not self.cfg.ipintel.enabled:
            return {}
        ips = [r.ip for r in new_records]
        ips += [r.ip for r in window_records]
        uas = {r.ip: r.user_agent for r in list(new_records) + list(window_records) if r.user_agent}
        try:
            return self.ipintel.enrich_many(ips, uas)
        except Exception as exc:  # noqa: BLE001
            log.warning("IP 画像查询失败（不影响告警）：%s", exc)
            return {}

    def _warn_on_clock_skew(self, records, now: datetime) -> None:
        """后台时间和本机差太多时提醒一次。不影响检测，但值得让用户知道。"""
        if self._skew_warned:
            return
        stamps = [r.visited_at for r in records if r.visited_at]
        if not stamps:
            return
        skew = (max(stamps) - now).total_seconds()
        if abs(skew) > 600:
            self._skew_warned = True
            log.warning(
                "后台记录的最新访问时间是 %s，本机现在是 %s，差了约 %d 分钟。"
                "突发检测本身不受影响（按记录之间的相对间隔算），但告警里显示的时间会以后台为准。",
                max(stamps).strftime("%H:%M:%S"), now.strftime("%H:%M:%S"), round(skew / 60),
            )

    # ------------------------------------------------------------------ #
    # 投递
    # ------------------------------------------------------------------ #
    MAX_DEFERRED = 50
    DEFER_MAX_AGE = timedelta(hours=6)

    def _deliver(self, alert: Alert, now: datetime) -> bool:
        """尝试把一条告警发出去。发不出去就挂起，等下一轮再试。"""
        allowed, why = self.notifier.should_send(alert, now)
        if not allowed:
            log.info("告警被抑制，挂起等下一轮：%s（%s）", alert.title, why)
            self._defer(alert, now)
            return False

        results = self.notifier.dispatch(alert)
        if not results:
            # 一个通道都没配。挂起也没意义，记录下来别重复处理就是了。
            log.warning("没有任何可用的通知通道，告警只写进了本地数据库：%s", alert.title)
            self.store.record_alert(alert, {})
            self._undefer(alert)
            return True
        # 控制台通道只是打印到终端，不能拿它当「送到了」的证据
        push = [r for r in results if r.channel != "console"]
        delivered = any(r.ok for r in (push or results))
        if not delivered:
            log.error("告警「%s」所有推送通道都失败了，挂起重试：%s", alert.title,
                      "；".join(f"{r.channel}: {r.message}" for r in results) or "没有可用通道")
            self._defer(alert, now)
            return False

        self.store.record_alert(alert, {r.channel: r.ok for r in results})
        self._undefer(alert)
        return True

    def _flush_deferred(self, now: datetime) -> int:
        """把挂起的告警再试一遍。"""
        if not self._deferred:
            return 0
        sent = 0
        for item in list(self._deferred):
            alert: Alert = item["alert"]          # type: ignore[assignment]
            if now - item["since"] > self.DEFER_MAX_AGE:   # type: ignore[operator]
                log.warning("告警「%s」挂起超过 %d 小时仍未发出，放弃（共 %d 条记录）",
                            alert.title, self.DEFER_MAX_AGE.total_seconds() // 3600,
                            len(alert.records))
                self._deferred.remove(item)
                continue
            if self._deliver(alert, now):
                sent += 1
        return sent

    def _defer(self, alert: Alert, now: datetime) -> None:
        for item in self._deferred:
            if item["alert"].dedup_key == alert.dedup_key:   # type: ignore[union-attr]
                item["alert"] = alert          # 用最新的一份（可能记录更全）
                return
        self._deferred.append({"alert": alert, "since": now})
        if len(self._deferred) > self.MAX_DEFERRED:
            dropped = self._deferred.pop(0)
            log.warning("挂起的告警太多，丢弃最旧的一条：%s", dropped["alert"].title)  # type: ignore[union-attr]

    def _undefer(self, alert: Alert) -> None:
        self._deferred = [i for i in self._deferred
                          if i["alert"].dedup_key != alert.dedup_key]  # type: ignore[union-attr]

    def _housekeeping(self, now: datetime) -> None:
        if now - self._last_prune > timedelta(hours=12):
            removed = self.store.prune(older_than_days=30)
            self._last_prune = now
            if removed:
                log.info("清理了 %d 条 30 天前的历史记录", removed)

    # ------------------------------------------------------------------ #
    def watch(self) -> None:
        """持续监控，Ctrl+C 退出。"""
        self._install_signal_handlers()
        p = self.cfg.poll
        log.info("开始监控：每 %d 秒查一次；规则 = %d 秒内 ≥ %d 条 / 单 IP %d 秒内 ≥ %d 次",
                 p.interval_seconds, self.cfg.rules.burst_window_seconds,
                 self.cfg.rules.burst_threshold, self.cfg.rules.ip_burst_window_seconds,
                 self.cfg.rules.ip_burst_threshold)
        while not self._stop:
            started = time.monotonic()
            try:
                self.run_once()
            except LoginError as exc:
                log.error("登录出问题，停止监控：%s", exc)
                break
            except KeyboardInterrupt:
                break
            except Exception as exc:  # noqa: BLE001
                self._consecutive_errors += 1
                log.exception("本轮异常（连续第 %d 次）：%s", self._consecutive_errors, exc)

            # 这个检查必须放在 try/except **外面**。最常见的失败——抓不到页面、
            # 确认不了是不是记录页——是正常 return 出来的，不走异常分支；
            # 只在 except 里检查的话，程序会一直空转，用户既收不到告警也收不到任何提示，
            # 还以为这段时间真的没人访问。
            if self._consecutive_errors >= p.max_consecutive_errors:
                log.error("连续 %d 轮抓取失败，停止监控。请检查网络/账号，或看 dumps/ 里的快照。",
                          self._consecutive_errors)
                self._notify_health_failure()
                break

            # 连续出错就退避，避免把 WebVPN 打爆
            backoff = min(2 ** self._consecutive_errors, 8) if self._consecutive_errors else 1
            wait = p.interval_seconds * backoff + random.uniform(0, max(0, p.jitter_seconds))
            wait -= (time.monotonic() - started)
            if wait > 0 and not self._stop:
                self._sleep(wait)
        log.info("监控已停止（共 %d 轮）", self._cycles)

    def _notify_health_failure(self) -> None:
        """监控自己挂了，也要告诉用户一声——沉默是最坏的结果。"""
        try:
            alert = Alert(
                rule="monitor_down", severity="critical",
                title="❌ 网站访问监控已停止工作",
                summary=(f"连续 {self._consecutive_errors} 轮没能取到「最近访问记录」，已停止监控。"
                         f"常见原因：会话掉线且无法自动重登、后台页面改版、网络不通。"
                         f"请到 dumps/ 目录看最近的页面快照，或重跑一次 `python run.py discover`。"),
                triggered_at=datetime.now(), dedup_key="monitor_down",
            )
            self.notifier.dispatch(alert)
        except Exception as exc:  # noqa: BLE001
            log.debug("发送自检告警失败：%s", exc)

    def _sleep(self, seconds: float) -> None:
        """可被 Ctrl+C 立刻打断的 sleep。"""
        end = time.monotonic() + seconds
        while not self._stop and time.monotonic() < end:
            time.sleep(min(0.5, end - time.monotonic()))

    def _install_signal_handlers(self) -> None:
        def handler(signum, frame):  # noqa: ARG001
            if self._stop:
                raise KeyboardInterrupt
            log.info("收到退出信号，正在收尾…（再按一次强制退出）")
            self._stop = True

        for sig in (signal.SIGINT, getattr(signal, "SIGTERM", None)):
            if sig is not None:
                try:
                    signal.signal(sig, handler)
                except (ValueError, OSError):
                    pass
