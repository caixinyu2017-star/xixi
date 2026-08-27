"""真浏览器端到端测试：登录 → 穿 iframe 点菜单 → 读到记录表 → 掉线自动重登。

跑的是真正的 Chromium，打的是本地起的假站点（tests/fake_site.py），不碰任何外网。
这一层覆盖的是纯逻辑测试碰不到的部分：Playwright 选择器、iframe 穿透、验证码循环、
以及**最要紧的账号保护——密码错时到底提交了几次表单**。

没装 playwright / 没有可用的 Chromium 时自动跳过。
    python tests/test_browser_flow.py
"""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

# 本地站点绝不能走代理
os.environ["NO_PROXY"] = os.environ["no_proxy"] = "127.0.0.1,localhost"

from fake_site import CORRECT_PASSWORD, CORRECT_USER, FakeSite   # noqa: E402
from monitor.config import AppConfig                             # noqa: E402
from monitor.navigator import RecordsNavigator                   # noqa: E402
from monitor.parser import parse_records                         # noqa: E402
from monitor.session import BrowserSession, LoginError           # noqa: E402
from monitor.store import Store                                  # noqa: E402


def chromium_path() -> str:
    """优先用 playwright 自己下的；找不到就用环境里现成的。"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return ""
    try:
        with sync_playwright() as pw:
            path = pw.chromium.executable_path
        if Path(path).exists():
            return ""            # 用默认的即可，不用显式指定
    except Exception:            # noqa: BLE001
        pass
    for candidate in ("/opt/pw-browsers/chromium", "/usr/bin/chromium",
                      "/usr/bin/chromium-browser", "/usr/bin/google-chrome"):
        if Path(candidate).exists():
            return candidate
    return "MISSING"


def make_config(site: FakeSite, tmp: Path, password: str = CORRECT_PASSWORD) -> AppConfig:
    cfg = AppConfig(base_dir=tmp)
    cfg.webvpn.login_url = site.login_url
    cfg.webvpn.target_url = site.target_url
    cfg.webvpn.username = CORRECT_USER
    cfg.webvpn.password = password
    cfg.webvpn.manual_captcha_fallback = False      # 测试里不能等人输入
    cfg.browser.headless = True
    cfg.browser.timeout_ms = 20000
    exe = chromium_path()
    if exe and exe != "MISSING":
        cfg.browser.executable_path = exe
    cfg.ensure_dirs()
    return cfg


# --------------------------------------------------------------------------- #
def test_wrong_password_stops_after_one_submit():
    """最重要的一条：密码错了必须**立刻**停，只提交一次，绝不把账号试锁。"""
    site = FakeSite(require_captcha=False)
    try:
        with tempfile.TemporaryDirectory() as td:
            cfg = make_config(site, Path(td), password="definitely-wrong")
            cfg.webvpn.max_login_attempts = 3        # 就算允许 3 次，也必须只用 1 次
            with BrowserSession(cfg, use_ocr=False) as session:
                try:
                    session.login()
                    raise AssertionError("密码错误却没有抛 LoginError")
                except LoginError as exc:
                    assert "密码" in str(exc) or "账号" in str(exc), str(exc)
            assert site.login_posts == 1, f"只该提交 1 次，实际提交了 {site.login_posts} 次"
    finally:
        site.stop()


def test_captcha_failure_never_exceeds_submit_budget():
    """OCR 一直识别不对时，提交次数不能超过 max_login_attempts。"""
    site = FakeSite(require_captcha=True)
    try:
        with tempfile.TemporaryDirectory() as td:
            cfg = make_config(site, Path(td))
            cfg.webvpn.max_login_attempts = 2
            cfg.webvpn.max_captcha_attempts = 3
            with BrowserSession(cfg, use_ocr=False) as session:   # 关掉 OCR，必然填不出验证码
                outcome = session.login()
            assert outcome.ok is False
            assert site.login_posts <= cfg.webvpn.max_login_attempts, (
                f"提交了 {site.login_posts} 次，超过了 {cfg.webvpn.max_login_attempts} 次的上限")
            assert site.captcha_fetches > 0, "应该至少去取过验证码图片"
    finally:
        site.stop()


def test_login_and_navigate_to_records():
    """正常路径：登录 → 点「运营中心 → 访问统计 → 最近访问记录」→ 读到 4 条记录。"""
    site = FakeSite(require_captcha=False)
    try:
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            cfg = make_config(site, tmp)
            store = Store(tmp / "s.sqlite")
            with BrowserSession(cfg, use_ocr=False) as session:
                outcome = session.ensure_logged_in()
                assert outcome.ok, outcome.message
                assert session.looks_logged_out() is False

                nav = RecordsNavigator(cfg, session, store)
                result = nav.fetch()
                assert result.ok, result.error
                assert result.verified, "应该识别出这是记录页"
                assert "/records.jsp" in result.url, result.url

                records = parse_records(result.html)
                assert len(records) == 4, [r.to_dict() for r in records]
                assert records[0].ip == "223.104.3.77"
                assert records[0].page.endswith("/2026/0824/c1001a12345/page.htm")
                assert records[0].page_title.startswith("“文化魔方”")
                assert records[2].ip == "106.11.159.22"

                # 地址被记住了，第二次应该直接开 URL，不用再点菜单
                assert store.get("records_url").endswith("/records.jsp")
                again = nav.fetch()
                assert again.ok and again.record_count == 4
            store.close()
    finally:
        site.stop()


def test_session_expiry_triggers_relogin():
    """会话被踢掉后，程序要自己重新登录并继续拿到数据。"""
    site = FakeSite(require_captcha=False)
    try:
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            cfg = make_config(site, tmp)
            store = Store(tmp / "s.sqlite")
            with BrowserSession(cfg, use_ocr=False) as session:
                assert session.ensure_logged_in().ok
                nav = RecordsNavigator(cfg, session, store)
                assert nav.fetch().ok

                site.expire_session()                     # 服务端把会话作废
                posts_before = site.login_posts
                dropped = nav.fetch()
                assert dropped.logged_out is True, f"没识别出掉线：{dropped.error}"

                assert session.ensure_logged_in(force=True).ok
                assert site.login_posts == posts_before + 1, "应该正好重新登录一次"
                recovered = nav.fetch(force_rediscover=True)
                assert recovered.ok and recovered.record_count == 4, recovered.error
            store.close()
    finally:
        site.stop()


def test_ocr_solves_the_captcha_when_available():
    """装了 ddddocr 的话，验证码整条链路（截图 → 识别 → 填入 → 提交）要能真的走通。"""
    try:
        import ddddocr  # noqa: F401
    except ImportError:
        print("      (跳过：没装 ddddocr)")
        return
    site = FakeSite(require_captcha=True)
    try:
        with tempfile.TemporaryDirectory() as td:
            cfg = make_config(site, Path(td))
            cfg.webvpn.max_login_attempts = 3
            cfg.webvpn.max_captcha_attempts = 8
            cfg.webvpn.captcha_min_confidence = 0.5
            with BrowserSession(cfg, use_ocr=True) as session:
                outcome = session.login()
            # OCR 不保证每次都对，所以这里只要求：要么成功，要么老老实实在预算内失败
            assert site.login_posts <= cfg.webvpn.max_login_attempts
            if outcome.ok:
                assert outcome.used_ocr, "成功了就应该是 OCR 认出来的"
            else:
                print(f"      (OCR 没认出来，提交 {site.login_posts} 次后按预算停止 —— 行为正确)")
    finally:
        site.stop()



def test_full_loop_detects_a_real_burst_through_the_browser():
    """最完整的一条：真浏览器 + 真主循环。

    先建立基线，然后往假站点里塞 3 条同一分钟内的新记录，主循环应该正好报一次警，
    而且告警里就是那 3 条。
    """
    from datetime import datetime, timedelta
    from monitor.monitor import AccessMonitor

    site = FakeSite(require_captcha=False)
    try:
        with tempfile.TemporaryDirectory() as td:
            cfg = make_config(site, Path(td))
            cfg.rules.burst_threshold = 3
            cfg.rules.burst_window_seconds = 60
            cfg.rules.ip_burst_enabled = False
            cfg.rules.baseline_on_first_run = True
            cfg.ipintel.enabled = False          # 沙箱里没网，跳过 IP 查询
            cfg.notify.channels = {}

            sent = []

            class Hub:
                def should_send(self, alert, now=None):
                    return True, ""

                def dispatch(self, alert):
                    sent.append(alert)
                    return []

            mon = AccessMonitor(cfg, use_ocr=False)
            mon.notifier = Hub()
            try:
                mon.start()
                first = mon.run_once()
                assert first.get("baseline") is True, first
                assert sent == [], "第一轮只建基线"

                # 塞 3 条新记录，时间挤在 20 秒内
                base = datetime.now().replace(microsecond=0) - timedelta(minutes=1)
                site.rows = site.rows + [
                    ((base + timedelta(seconds=i * 8)).strftime("%Y-%m-%d %H:%M:%S"),
                     f"203.0.113.{20 + i}", f"/news/{i}.htm", f"新页面{i}")
                    for i in range(3)
                ]
                second = mon.run_once()
                assert second["new"] == 3, second
                assert len(sent) == 1, f"应该正好报一次，实际 {len(sent)} 次"
                assert len(sent[0].records) == 3
                assert {r.ip for r in sent[0].records} == {"203.0.113.20", "203.0.113.21", "203.0.113.22"}

                third = mon.run_once()            # 页面没变，不该再报
                assert third["new"] == 0, third
                assert len(sent) == 1, "同样的记录不能重复告警"
            finally:
                mon.close()
    finally:
        site.stop()




def test_submit_budget_survives_a_new_login_call():
    """预算必须跨 login() 调用累计，否则 watch 循环每轮都能拿到一份新预算。

    真实触发路径：登录中途抛出一个不是 LoginError 的异常（比如页面 goto 超时），
    watch 的通用 except 会吞掉它继续轮询，下一轮又调一次 login()。
    如果预算只是 login() 里的循环变量，配置写的「最多 3 次」实际能变成 3 的好几倍。
    这里直接连着调两次 login() 来模拟那个效果。
    """
    site = FakeSite(require_captcha=False, generic_error=True)   # 提示含糊，判不出是密码错
    try:
        with tempfile.TemporaryDirectory() as td:
            cfg = make_config(site, Path(td), password="wrong-but-indistinguishable")
            cfg.webvpn.max_login_attempts = 3
            with BrowserSession(cfg, use_ocr=False) as session:
                first = session.login()
                assert first.ok is False
                assert site.login_posts == 3, f"第一次调用应该用满 3 次，实际 {site.login_posts}"

                # 第二次调用不能再拿到新预算，必须直接拒绝
                try:
                    session.login()
                    raise AssertionError("预算已耗尽却还允许再次登录")
                except LoginError as exc:
                    assert "锁定" in str(exc), str(exc)
            assert site.login_posts == 3, (
                f"跨调用总共只该提交 3 次，实际 {site.login_posts} 次")
    finally:
        site.stop()


def test_successful_login_clears_the_budget():
    """长期挂机时，正常的会话过期重登不能把预算越攒越少。"""
    site = FakeSite(require_captcha=False, generic_error=True)
    try:
        with tempfile.TemporaryDirectory() as td:
            cfg = make_config(site, Path(td), password="wrong-at-first")
            cfg.webvpn.max_login_attempts = 3
            with BrowserSession(cfg, use_ocr=False) as session:
                assert session.login().ok is False
                assert session._submits_left() == 0

                cfg.webvpn.password = CORRECT_PASSWORD     # 用户改对了密码
                session._failed_submits = session._failed_submits[:1]   # 模拟窗口过期掉两条
                assert session.login().ok is True
                assert session._submits_left() == cfg.webvpn.max_login_attempts, \
                    "登录成功后预算应该完全恢复"
    finally:
        site.stop()



if __name__ == "__main__":
    exe = chromium_path()
    if exe == "MISSING":
        print("跳过浏览器测试：没有可用的 Chromium（先跑 python -m playwright install chromium）")
        sys.exit(0)
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
                import traceback
                traceback.print_exc()
                print(f"  ✗ {name}: {type(exc).__name__}: {exc}")
    print("全部通过" if not failures else f"{failures} 个测试失败")
    sys.exit(1 if failures else 0)
