"""端到端离线测试：用假的浏览器会话跑完整个「抓取 → 去重 → 检测 → 告警」链路。

不联网、不开浏览器，所以可以在 CI 或任何机器上跑，用来保证主循环的逻辑没写错。
"""
from __future__ import annotations

import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from monitor.config import AppConfig, NotifyConfig, RulesConfig   # noqa: E402
from monitor.models import Alert                                   # noqa: E402
from monitor.monitor import AccessMonitor                          # noqa: E402
from monitor.navigator import FetchResult, sibling_webvpn_url      # noqa: E402


def _page_html(rows):
    """造一张和博达后台同构的表格。"""
    body = "".join(
        f"<tr><td>{i+1}</td><td>{t}</td><td>{ip}</td>"
        f"<td><a href='/a/{i}.htm'>页面{i}</a></td><td>-</td><td>Chrome</td></tr>"
        for i, (t, ip) in enumerate(rows)
    )
    # 标题里的「最近访问记录」是给 navigator 用来确认页面身份的特征词
    return ("<html><body><h2>最近访问记录</h2><table>"
            "<tr><th>序号</th><th>访问时间</th><th>来访IP</th>"
            "<th>访问页面</th><th>来源页面</th><th>浏览器</th></tr>"
            + body + "</table></body></html>")


class FakeSession:
    """假会话：不开浏览器，永远处于登录态。"""
    def __init__(self, cfg):
        self.cfg = cfg
        self.page = None
        self.started = False

    def start(self):
        self.started = True

    def close(self):
        self.started = False

    def ensure_logged_in(self, target_url="", force=False):
        from monitor.session import LoginOutcome
        return LoginOutcome(ok=True, attempts=0, used_ocr=False, message="假会话")

    def looks_logged_out(self, page=None):
        return False

    def _settle(self, extra_wait=0.0):
        pass


class FakeNavigator:
    """按预设脚本一轮一轮吐 HTML。"""
    def __init__(self, pages, verified=True):
        self.pages = list(pages)
        self.calls = 0
        self.verified = verified
        self.dumped = 0

    def fetch(self, force_rediscover=False):
        html = self.pages[min(self.calls, len(self.pages) - 1)]
        self.calls += 1
        return FetchResult(ok=self.verified, html=html, url="http://fake/records",
                           record_count=1, verified=self.verified,
                           error="" if self.verified else "确认不了这是记录页")

    def dump(self, tag="x"):
        self.dumped += 1
        return Path(".")


class CapturingHub:
    """把「发出去的告警」记下来，方便断言。"""
    def __init__(self):
        self.sent = []

    def should_send(self, alert, now=None):
        return True, ""

    def dispatch(self, alert: Alert):
        self.sent.append(alert)
        return []


def _make_monitor(tmp: Path, pages, rules=None) -> AccessMonitor:
    cfg = AppConfig(base_dir=tmp)
    cfg.rules = rules or RulesConfig(burst_threshold=3, burst_window_seconds=60,
                                     ip_burst_enabled=False, baseline_on_first_run=False)
    cfg.notify = NotifyConfig(enabled=True, channels={})
    cfg.ipintel.enabled = False
    mon = AccessMonitor(cfg)
    mon.session = FakeSession(cfg)
    mon.navigator = FakeNavigator(pages)
    mon.notifier = CapturingHub()
    return mon


def test_burst_triggers_alert_once_and_dedupes():
    base = datetime.now().replace(microsecond=0) - timedelta(minutes=5)
    fmt = "%Y-%m-%d %H:%M:%S"
    three = [((base + timedelta(seconds=i * 5)).strftime(fmt), f"1.2.3.{i+1}") for i in range(3)]
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        mon = _make_monitor(tmp, [_page_html(three), _page_html(three)])
        try:
            r1 = mon.run_once()
            assert r1["new"] == 3, r1
            assert len(mon.notifier.sent) == 1, "3 条落在 60 秒窗口内，应该正好报一次"
            assert len(mon.notifier.sent[0].records) == 3

            r2 = mon.run_once()           # 同一张页面再抓一次
            assert r2["new"] == 0, r2
            assert len(mon.notifier.sent) == 1, "同样的记录不能重复告警"
        finally:
            mon.store.close()


def test_two_records_do_not_alert():
    base = datetime.now().replace(microsecond=0) - timedelta(minutes=5)
    fmt = "%Y-%m-%d %H:%M:%S"
    two = [((base + timedelta(seconds=i * 5)).strftime(fmt), f"9.9.9.{i}") for i in range(2)]
    with tempfile.TemporaryDirectory() as td:
        mon = _make_monitor(Path(td), [_page_html(two)])
        try:
            mon.run_once()
            assert mon.notifier.sent == [], "只有 2 条，不该告警"
        finally:
            mon.store.close()


def test_baseline_suppresses_first_run():
    base = datetime.now().replace(microsecond=0) - timedelta(minutes=5)
    fmt = "%Y-%m-%d %H:%M:%S"
    many = [((base + timedelta(seconds=i)).strftime(fmt), f"5.5.5.{i}") for i in range(6)]
    rules = RulesConfig(burst_threshold=3, burst_window_seconds=60,
                        ip_burst_enabled=False, baseline_on_first_run=True)
    with tempfile.TemporaryDirectory() as td:
        mon = _make_monitor(Path(td), [_page_html(many)], rules)
        try:
            r = mon.run_once()
            assert r.get("baseline") is True
            assert mon.notifier.sent == [], "第一次运行只建基线，不应该轰炸"
        finally:
            mon.store.close()


def test_cooldown_defers_but_does_not_lose_records():
    """被冷却压住的记录必须并进下一次告警，不能人间蒸发。"""
    base = datetime.now().replace(microsecond=0) - timedelta(minutes=5)
    fmt = "%Y-%m-%d %H:%M:%S"
    first = [((base + timedelta(seconds=i * 5)).strftime(fmt), f"1.1.1.{i}") for i in range(3)]

    class BlockingHub(CapturingHub):
        def __init__(self):
            super().__init__()
            self.block = True

        def should_send(self, alert, now=None):
            return (False, "冷却中") if self.block else (True, "")

    with tempfile.TemporaryDirectory() as td:
        mon = _make_monitor(Path(td), [_page_html(first), _page_html(first)])
        hub = BlockingHub()
        mon.notifier = hub
        try:
            mon.run_once()
            assert hub.sent == [] and len(mon._pending) == 3, "被压住的 3 条要挂在待发队列里"
            hub.block = False
            mon.run_once()                       # 页面没变，但积压的记录应该被重新报出去
            assert len(hub.sent) == 1
            assert len(hub.sent[0].records) == 3
            assert mon._pending == []
        finally:
            mon.store.close()


def test_sibling_webvpn_url():
    cur = ("https://webvpn.zjxu.edu.cn/http-8080/"
           "77726476706e69737468656265737421a1a70fcd777e391e2d/system/caslogin.jsp")
    got = sibling_webvpn_url(cur, "/system/statistics/visit.jsp?a=1")
    assert got == ("https://webvpn.zjxu.edu.cn/http-8080/"
                   "77726476706e69737468656265737421a1a70fcd777e391e2d/"
                   "system/statistics/visit.jsp?a=1"), got
    assert sibling_webvpn_url("https://example.com/foo", "/bar") == ""



def test_unverified_page_is_never_parsed():
    """抓到一个确认不了身份的页面时，必须整轮跳过。

    解析器最后一层是全文正则捞 IP。如果拿它去啃错误页/登录页，捞出来的垃圾记录
    时间戳全都是「此刻」，会立刻凑够 3 条触发假告警——这是最危险的失败模式。
    """
    junk = ("<html><body>系统繁忙，请稍后再试。"
            "服务器 10.20.30.41 / 10.20.30.42 / 10.20.30.43 均无响应</body></html>")
    with tempfile.TemporaryDirectory() as td:
        mon = _make_monitor(Path(td), [junk])
        mon.navigator = FakeNavigator([junk], verified=False)
        try:
            r = mon.run_once()
            assert r["ok"] is False, r
            assert mon.notifier.sent == [], "确认不了的页面绝不能产生告警"
            assert mon.store.stats()["records"] == 0, "也不能把垃圾写进数据库"
        finally:
            mon.store.close()


def test_slow_trickle_is_not_merged_into_one_giant_burst():
    """每 59 秒来一条的细水长流，不该被串成「一小时 60 条」的假突发。"""
    from monitor.detector import sliding_clusters
    from monitor.models import VisitRecord
    base = datetime(2026, 8, 27, 10, 0, 0)
    # 前三条是真突发（0/5/10 秒），后面每 59 秒一条
    times = [0, 5, 10] + [10 + 59 * i for i in range(1, 8)]
    recs = [VisitRecord(ip=f"1.1.1.{i}", visited_at=base + timedelta(seconds=t), first_seen_at=base)
            for i, t in enumerate(times)]
    clusters = sliding_clusters(recs, window_seconds=60, threshold=3)
    assert len(clusters) == 1, f"应该只认出开头那一次突发，实际 {len(clusters)} 个"
    assert len(clusters[0]) == 3, f"突发应该只含开头 3 条，实际 {len(clusters[0])} 条"




def test_burst_detected_even_when_server_clock_is_skewed():
    """后台服务器时钟和本机差 40 分钟时，突发检测必须照样工作。

    这是最阴险的一类 bug：窗口如果按后台标注的访问时间去取，时钟一偏就一条都捞不到，
    程序看起来一切正常、日志也没有报错，但**永远不会告警**。
    所以窗口按「我们什么时候看到它」取，簇内疏密才按访问时间算。
    """
    skewed = datetime.now().replace(microsecond=0) - timedelta(minutes=40)
    fmt = "%Y-%m-%d %H:%M:%S"
    rows = [((skewed + timedelta(seconds=i * 6)).strftime(fmt), f"198.51.100.{i}") for i in range(3)]
    rules = RulesConfig(burst_threshold=3, burst_window_seconds=60,
                        ip_burst_enabled=False, baseline_on_first_run=False)
    with tempfile.TemporaryDirectory() as td:
        mon = _make_monitor(Path(td), [_page_html(rows)], rules)
        try:
            r = mon.run_once()
            assert r["new"] == 3, r
            assert len(mon.notifier.sent) == 1, "时钟偏移不该让告警消失"
            assert len(mon.notifier.sent[0].records) == 3
        finally:
            mon.store.close()



if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"  ✓ {name}")
            except AssertionError as exc:
                failures += 1
                print(f"  ✗ {name}: {exc}")
            except Exception as exc:  # noqa: BLE001
                failures += 1
                import traceback; traceback.print_exc()
                print(f"  ✗ {name}: {type(exc).__name__}: {exc}")
    print("全部通过" if not failures else f"{failures} 个测试失败")
    sys.exit(1 if failures else 0)
