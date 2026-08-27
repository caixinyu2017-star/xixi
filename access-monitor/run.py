#!/usr/bin/env python3
"""网站访问实时监控 —— 命令行入口。

常用：
    python run.py doctor          # 环境自检，先跑这个
    python run.py test-notify     # 测试告警能不能发到你手机/邮箱
    python run.py login           # 只登录一次，把会话存下来（第一次可能要手工输验证码）
    python run.py discover        # 登录 + 自动找到「最近访问记录」页，并导出页面快照
    python run.py once            # 跑一轮看看效果
    python run.py watch           # 正式开始实时监控（Ctrl+C 停止）

辅助：
    python run.py ip 8.8.8.8 223.5.5.5     # 单独查 IP 归属，不用开浏览器
    python run.py parse dumps/xxx.html     # 离线调试页面解析
    python run.py stats                    # 看看攒了多少数据
"""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from monitor.config import load_config                      # noqa: E402
from monitor.logging_setup import setup_logging             # noqa: E402

log = logging.getLogger("run")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="run.py",
        description="博达网站群「最近访问记录」实时监控与告警",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("-c", "--config", type=Path, help="配置文件路径（默认 config.yaml）")
    p.add_argument("-v", "--verbose", action="store_true", help="输出调试日志")
    p.add_argument("--headless", dest="headless", action="store_true", help="强制无头模式（不显示浏览器）")
    p.add_argument("--show", dest="headless", action="store_false", help="强制显示浏览器窗口")
    p.set_defaults(headless=None)
    p.add_argument("--no-ocr", action="store_true", help="不用 ddddocr，验证码全部手工输入")

    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor", help="环境自检：依赖、配置、目录、网络")
    sub.add_parser("login", help="登录并保存会话")
    d = sub.add_parser("discover", help="找到「最近访问记录」页并导出页面快照")
    d.add_argument("--no-dump", action="store_true", help="不导出 HTML 快照")
    o = sub.add_parser("once", help="跑一轮抓取 + 检测")
    o.add_argument("--force-alert", action="store_true", help="忽略冷却，强制把命中的告警发出去")
    w = sub.add_parser("watch", help="持续实时监控")
    w.add_argument("--interval", type=int, help="覆盖轮询间隔（秒）")
    sub.add_parser("test-notify", help="给所有已启用通道发一条测试告警")
    ip = sub.add_parser("ip", help="查询 IP 归属")
    ip.add_argument("addresses", nargs="+", help="一个或多个 IP")
    ps = sub.add_parser("parse", help="离线解析一个 HTML 文件")
    ps.add_argument("file", type=Path)
    sub.add_parser("stats", help="显示本地数据库统计")
    return p


# --------------------------------------------------------------------------- #
def cmd_doctor(cfg, args) -> int:
    print("=== 环境自检 ===\n")
    ok = True

    print("[依赖]")
    required = {"playwright": "浏览器自动化（必须）", "requests": "HTTP 请求（必须）",
                "yaml": "读配置（必须）", "bs4": "HTML 解析（必须）"}
    optional = {"ddddocr": "验证码自动识别（强烈建议，否则每次掉线都要手工输）",
                "lxml": "更快更稳的 HTML 解析（建议）",
                "maxminddb": "读 GeoCN 离线库（可选，国内 IP 能到区/县）",
                "ip2region": "读 ip2region 离线库（可选，全球到市级）"}
    for mod, why in required.items():
        try:
            __import__(mod)
            print(f"  ✓ {mod:<12} {why}")
        except ImportError:
            ok = False
            print(f"  ✗ {mod:<12} {why}  → 缺失！请 pip install -r requirements.txt")
    for mod, why in optional.items():
        try:
            __import__(mod)
            print(f"  ✓ {mod:<12} {why}")
        except ImportError:
            print(f"  ○ {mod:<12} {why}  → 未安装")

    print("\n[离线 IP 库]")
    for label, value in (("GeoCN.mmdb", cfg.ipintel.geocn_mmdb),
                         ("ip2region.xdb", cfg.ipintel.ip2region_xdb)):
        if not value:
            print(f"  ○ {label:<14} 未配置（国内 IP 只能靠在线 API，精度到市级）")
        elif cfg.path(value).exists():
            size = cfg.path(value).stat().st_size / 1024 / 1024
            print(f"  ✓ {label:<14} {cfg.path(value)}（{size:.1f} MB）")
        else:
            print(f"  ✗ {label:<14} 配置了但文件不存在：{cfg.path(value)}")

    print("\n[浏览器]")
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            path = pw.chromium.executable_path
            exists = Path(path).exists()
            print(f"  {'✓' if exists else '✗'} Chromium: {path}")
            if not exists:
                ok = False
                print("     → 请执行：python -m playwright install chromium")
    except Exception as exc:  # noqa: BLE001
        ok = False
        print(f"  ✗ 无法启动 Playwright：{exc}")

    print("\n[配置]")
    print(f"  配置文件：{getattr(cfg, 'config_file', '') or '（没找到，用的内置默认值）'}")
    for label, value, required_ in (
        ("登录地址 login_url", cfg.webvpn.login_url, True),
        ("目标后台 target_url", cfg.webvpn.target_url, True),
        ("账号 WEBVPN_USERNAME", cfg.webvpn.username, True),
        ("密码 WEBVPN_PASSWORD", "已设置" if cfg.webvpn.password else "", True),
    ):
        mark = "✓" if value else ("✗" if required_ else "○")
        if required_ and not value:
            ok = False
        shown = value if label.startswith(("登录", "目标")) else ("已设置" if value else "未设置")
        print(f"  {mark} {label}: {shown[:96] or '未设置'}")
    unknown = getattr(cfg, "unknown_keys", [])
    if unknown:
        print(f"  ! 配置里有无法识别的项（已忽略）：{', '.join(unknown)}")

    print("\n[告警通道]")
    from monitor.notify import NotificationHub
    hub = NotificationHub(cfg.notify, None)
    names = [c.name for c in hub.channels]
    print(f"  已启用：{', '.join(names) or '无'}")
    for name in hub.skipped:
        print(f"  ! {name}：配置不完整，已跳过（去 .env / config.yaml 里补齐）")
    if names == ["console"]:
        print("  ! 只有控制台通道 —— 关掉终端就收不到告警了。建议至少配一个邮箱或 Bark。")

    print("\n[检测规则]")
    r = cfg.rules
    print(f"  整体突发：{r.burst_window_seconds} 秒内 ≥ {r.burst_threshold} 条"
          f"（{'开' if r.burst_enabled else '关'}）")
    print(f"  单 IP 高频：{r.ip_burst_window_seconds} 秒内 ≥ {r.ip_burst_threshold} 次"
          f"（{'开' if r.ip_burst_enabled else '关'}）")
    print(f"  轮询间隔：{cfg.poll.interval_seconds} 秒｜告警冷却：{cfg.notify.cooldown_seconds} 秒")

    print("\n[目录]")
    cfg.ensure_dirs()
    for name, path in (("状态", cfg.state_path), ("日志", cfg.log_path), ("快照", cfg.dump_path)):
        print(f"  ✓ {name}：{path}")

    print("\n" + ("✅ 自检通过，可以跑 `python run.py login` 了。" if ok else
                  "❌ 上面标 ✗ 的问题要先解决。"))
    return 0 if ok else 1


def cmd_login(cfg, args) -> int:
    from monitor.session import BrowserSession, LoginError
    with BrowserSession(cfg, use_ocr=not args.no_ocr) as session:
        try:
            outcome = session.ensure_logged_in()
        except LoginError as exc:
            log.error("%s", exc)
            return 2
        if outcome.ok:
            print(f"✅ 登录成功（{outcome.message or f'尝试 {outcome.attempts} 次'}），"
                  f"会话已保存到 {cfg.path(cfg.browser.user_data_dir)}")
            return 0
        print(f"❌ 登录失败：{outcome.message}")
        return 1


def cmd_discover(cfg, args) -> int:
    from monitor.navigator import RecordsNavigator
    from monitor.parser import describe_parse
    from monitor.session import BrowserSession
    from monitor.store import Store

    cfg.ensure_dirs()
    store = Store(cfg.state_path / "monitor.sqlite")
    with BrowserSession(cfg, use_ocr=not args.no_ocr) as session:
        outcome = session.ensure_logged_in()
        if not outcome.ok:
            print(f"❌ 登录失败：{outcome.message}")
            return 1
        nav = RecordsNavigator(cfg, session, store)
        result = nav.fetch(force_rediscover=True)
        if not args.no_dump:
            out = nav.dump("discover")
            print(f"\n页面快照已导出：{out}")
        if not result.ok and not result.html:
            print(f"❌ 没找到记录页：{result.error}")
            print("   建议：把 config.yaml 里 browser.headless 设成 false，再跑一次亲眼看看菜单文字。")
            return 1
        print(f"\n✅ 记录页地址：{result.url}")
        print(f"   frame: {result.frame_name or '(主文档)'}")
        if result.xhr_endpoints:
            print("   页面用到的 JSON 接口（以后可以直接打接口，更省资源）：")
            for u in result.xhr_endpoints[:10]:
                print(f"     - {u}")
        print("\n--- 解析诊断 ---")
        print(describe_parse(result.html))
    store.close()
    return 0


def cmd_once(cfg, args) -> int:
    from monitor.monitor import AccessMonitor
    if args.force_alert:
        cfg.notify.cooldown_seconds = 0
        cfg.rules.baseline_on_first_run = False
    with AccessMonitor(cfg, use_ocr=not args.no_ocr) as mon:
        result = mon.run_once()
    print(f"\n结果：{result}")
    return 0 if result.get("ok") else 1


def cmd_watch(cfg, args) -> int:
    from monitor.monitor import AccessMonitor
    if args.interval:
        cfg.poll.interval_seconds = args.interval
    with AccessMonitor(cfg, use_ocr=not args.no_ocr) as mon:
        mon.watch()
    return 0


def cmd_test_notify(cfg, args) -> int:
    from monitor.notify import NotificationHub
    hub = NotificationHub(cfg.notify, None)
    results = hub.test()
    print()
    failed = 0
    for r in results:
        print(f"  {'✓' if r.ok else '✗'} {r.channel:<12} {r.message}")
        failed += 0 if r.ok else 1
    print(f"\n{len(results) - failed}/{len(results)} 个通道发送成功")
    return 0 if failed == 0 else 1


def cmd_ip(cfg, args) -> int:
    from monitor.ipintel import IpIntel
    from monitor.store import Store
    cfg.ensure_dirs()
    store = Store(cfg.state_path / "monitor.sqlite")
    intel = IpIntel(cfg.ipintel, store)
    profiles = intel.enrich_many(args.addresses)
    for ip in args.addresses:
        prof = profiles.get(ip)
        print(f"\n=== {ip} ===")
        if not prof:
            print("  查询失败")
            continue
        print(f"  位置      {prof.location_text}" + (f"（精度 {prof.accuracy}）" if prof.accuracy else ""))
        print(f"  网络      {prof.network_text}")
        if prof.rdns:
            print(f"  反向域名  {prof.rdns}")
        if prof.labels:
            print(f"  标签      {'、'.join(prof.labels)}")
        if prof.lat is not None:
            print(f"  经纬度    {prof.lat}, {prof.lon}")
        print(f"  风险分    {prof.risk_score}" + (f"（{'；'.join(prof.risk_reasons)}）" if prof.risk_reasons else ""))
        print(f"  数据来源  {'、'.join(dict.fromkeys(prof.sources)) or '无'}")
        if prof.error:
            print(f"  备注      {prof.error}")
    intel.close()
    store.close()
    return 0


def cmd_parse(cfg, args) -> int:
    from monitor.parser import describe_parse
    if not args.file.exists():
        print(f"文件不存在：{args.file}")
        return 1
    print(describe_parse(args.file.read_text(encoding="utf-8", errors="replace")))
    return 0


def cmd_stats(cfg, args) -> int:
    from monitor.store import Store
    cfg.ensure_dirs()
    store = Store(cfg.state_path / "monitor.sqlite")
    s = store.stats()
    print(f"已记录访问：{s['records']} 条")
    print(f"不同 IP：  {s['ips']} 个")
    print(f"发出告警：  {s['alerts']} 条")
    print(f"IP 缓存：   {s['ip_cache']} 条")
    print(f"记录页地址：{store.get('records_url') or '（还没发现，跑一次 discover）'}")
    store.close()
    return 0


COMMANDS = {
    "doctor": cmd_doctor, "login": cmd_login, "discover": cmd_discover,
    "once": cmd_once, "watch": cmd_watch, "test-notify": cmd_test_notify,
    "ip": cmd_ip, "parse": cmd_parse, "stats": cmd_stats,
}


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    cfg = load_config(args.config, base_dir=BASE_DIR)
    if args.headless is not None:
        cfg.browser.headless = args.headless
    if args.verbose:
        cfg.log_level = "DEBUG"
    setup_logging(cfg.log_path, cfg.log_level)
    if getattr(cfg, "using_example_config", False):
        log.warning("没找到 config.yaml，正在直接用 config.example.yaml。"
                    "建议先 cp config.example.yaml config.yaml 再改，免得下次更新被覆盖。")
    try:
        return COMMANDS[args.command](cfg, args)
    except KeyboardInterrupt:
        print("\n已中断")
        return 130


if __name__ == "__main__":
    sys.exit(main())
