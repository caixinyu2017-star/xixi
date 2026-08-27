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
        self.notifier = NotificationHub(cfg.notify, self.store)
        self.session = BrowserSession(cfg, use_ocr=use_ocr)
        self.navigator: Optional[RecordsNavigator] = None
        self._pending: List[VisitRecord] = []      # 被冷却压住、还没报出去的记录
        self._consecutive_errors = 0
        self._stop = False
        self._cycles = 0
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

        if not new_records and not self._pending:
            log.info("本轮无新增（页面共 %d 条）", len(records))
            return {"ok": True, "records": len(records), "new": 0, "alerts": 0}

        log.info("本轮新增 %d 条（页面共 %d 条）", len(new_records), len(records))

        # 检测窗口：取两条规则里更长的那个窗口，再放宽一倍，保证跨轮的簇也能连上
        window = max(self.cfg.rules.burst_window_seconds, self.cfg.rules.ip_burst_window_seconds)
        window_records = self.store.records_since(now - timedelta(seconds=window * 2 + 60))

        profiles = self._enrich(new_records, window_records)

        candidates = list(self._pending) + [r for r in new_records
                                            if r.key not in {p.key for p in self._pending}]
        alerts = self.detector.detect(
            candidates, window_records, profiles, known_ips_before=known_ips_before, now=now
        )

        sent = 0
        for alert in alerts:
            allowed, why = self.notifier.should_send(alert, now)
            if not allowed:
                log.info("告警被抑制：%s（%s）", alert.title, why)
                self._remember_pending(alert.records)
                continue
            results = self.notifier.dispatch(alert)
            self.store.record_alert(alert, {r.channel: r.ok for r in results})
            self._forget_pending(alert.records)
            sent += 1

        if not alerts:
            self._pending = []      # 没有任何簇成型，积压的记录也就没意义了

        self._housekeeping(now)
        return {"ok": True, "records": len(records), "new": len(new_records),
                "alerts": sent, "suppressed": len(alerts) - sent}

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

    def _remember_pending(self, records) -> None:
        have = {r.key for r in self._pending}
        for rec in records:
            if rec.key not in have:
                self._pending.append(rec)
        # 别无限堆积
        if len(self._pending) > 500:
            self._pending = self._pending[-500:]

    def _forget_pending(self, records) -> None:
        done = {r.key for r in records}
        self._pending = [r for r in self._pending if r.key not in done]

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
                if self._consecutive_errors >= p.max_consecutive_errors:
                    log.error("连续 %d 轮失败，退出。请检查网络/账号，或看 dumps/ 里的快照。",
                              self._consecutive_errors)
                    break

            # 连续出错就退避，避免把 WebVPN 打爆
            backoff = min(2 ** self._consecutive_errors, 8) if self._consecutive_errors else 1
            wait = p.interval_seconds * backoff + random.uniform(0, max(0, p.jitter_seconds))
            wait -= (time.monotonic() - started)
            if wait > 0 and not self._stop:
                self._sleep(wait)
        log.info("监控已停止（共 %d 轮）", self._cycles)

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
