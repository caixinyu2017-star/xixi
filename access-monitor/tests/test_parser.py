"""解析 / 检测 / 配置的离线测试。

不需要联网，也不需要真的登录：`python -m pytest tests/ -q` 或直接 `python tests/test_parser.py`。
"""
from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from monitor.config import RulesConfig                      # noqa: E402
from monitor.detector import BurstDetector, sliding_clusters  # noqa: E402
from monitor.models import VisitRecord                       # noqa: E402
from monitor.parser import parse_records, parse_datetime, extract_ip  # noqa: E402

FIXTURE = Path(__file__).parent / "fixtures" / "recent_visits_sample.html"


def test_extract_ip():
    assert extract_ip("来访IP：223.104.3.77 ") == "223.104.3.77"
    assert extract_ip("2026-08-27 15:32:11") == ""          # 日期不能被当成 IP
    assert extract_ip("999.1.1.1") == ""
    assert extract_ip("2001:db8::1 访问") == "2001:db8::1"


def test_parse_datetime():
    assert parse_datetime("2026-08-27 15:32:11") == datetime(2026, 8, 27, 15, 32, 11)
    assert parse_datetime("2026/08/27 15:32") == datetime(2026, 8, 27, 15, 32)
    ref = datetime(2026, 8, 27, 16, 0, 0)
    assert parse_datetime("15:32:11", ref) == datetime(2026, 8, 27, 15, 32, 11)
    # 只有时分秒且明显“晚于现在”，按昨天算
    assert parse_datetime("23:59:00", datetime(2026, 8, 27, 0, 30, 0)) == datetime(2026, 8, 26, 23, 59)
    assert parse_datetime("暂无数据") is None


def test_parse_table():
    records = parse_records(FIXTURE.read_text(encoding="utf-8"))
    assert len(records) == 4, [r.to_dict() for r in records]
    first = records[0]
    assert first.ip == "223.104.3.77"
    assert first.visited_at == datetime(2026, 8, 27, 15, 32, 11)
    assert "page.htm" in first.page
    assert first.referer.startswith("https://www.baidu.com")
    assert first.user_agent == "Chrome 128"
    assert first.os == "Windows 10"
    assert first.location_hint == "浙江"
    assert "序号" in first.raw and first.raw["序号"] == "1"
    assert records[2].ip == "106.11.159.22"


def test_record_key_stable_and_distinct():
    a = parse_records(FIXTURE.read_text(encoding="utf-8"))
    b = parse_records(FIXTURE.read_text(encoding="utf-8"))
    assert [r.key for r in a] == [r.key for r in b]          # 幂等
    assert len({r.key for r in a}) == 4                       # 四条互不相同


def test_parse_no_header_table():
    html = """<table>
      <tr><td>2026-08-27 10:00:01</td><td>1.2.3.4</td><td>/a.htm</td></tr>
      <tr><td>2026-08-27 10:00:05</td><td>1.2.3.5</td><td>/b.htm</td></tr>
    </table>"""
    recs = parse_records(html)
    assert [r.ip for r in recs] == ["1.2.3.4", "1.2.3.5"]
    assert recs[0].visited_at == datetime(2026, 8, 27, 10, 0, 1)


def test_parse_garbage_falls_back():
    html = "<div>来访 IP 8.8.8.8 于 2026-08-27 09:00:00 访问</div>"
    recs = parse_records(html)
    assert len(recs) == 1 and recs[0].ip == "8.8.8.8"
    assert parse_records("<html><body>暂无数据</body></html>") == []


def _rec(ip: str, t: datetime) -> VisitRecord:
    return VisitRecord(ip=ip, visited_at=t, page="/x.htm", first_seen_at=t)


def test_sliding_clusters_catches_cross_bucket_burst():
    base = datetime(2026, 8, 27, 23, 59, 58)
    recs = [_rec("1.1.1.1", base), _rec("1.1.1.2", base + timedelta(seconds=1)),
            _rec("1.1.1.3", base + timedelta(seconds=3))]
    assert len(sliding_clusters(recs, 60, 3)) == 1            # 跨分钟也能抓到
    assert sliding_clusters(recs, 60, 4) == []


def test_detector_burst_and_ip_burst():
    rules = RulesConfig(burst_threshold=3, burst_window_seconds=60,
                        ip_burst_threshold=3, ip_burst_window_seconds=300)
    det = BurstDetector(rules)
    base = datetime(2026, 8, 27, 10, 0, 0)
    recs = [_rec("9.9.9.9", base + timedelta(seconds=i * 5)) for i in range(4)]
    alerts = det.detect(recs, recs, {}, known_ips_before=set(), now=base)
    assert [a.rule for a in alerts] == ["burst"]              # 单 IP 告警被整体告警吸收
    assert len(alerts[0].records) == 4

    two = recs[:2]
    assert det.detect(two, two, {}, known_ips_before=set(), now=base) == []


def test_detector_ignores_filtered_ips():
    rules = RulesConfig(burst_threshold=3, burst_window_seconds=60, ignore_ips=["10.0.0.0/8"])
    det = BurstDetector(rules)
    base = datetime(2026, 8, 27, 10, 0, 0)
    recs = [_rec("10.0.0.5", base + timedelta(seconds=i)) for i in range(5)]
    assert det.detect(recs, recs, {}, known_ips_before=set(), now=base) == []


def test_detector_requires_a_new_record():
    """老簇不该被反复报警。"""
    rules = RulesConfig(burst_threshold=3, burst_window_seconds=60, ip_burst_enabled=False)
    det = BurstDetector(rules)
    base = datetime(2026, 8, 27, 10, 0, 0)
    old = [_rec("8.8.8.8", base + timedelta(seconds=i)) for i in range(3)]
    new = [_rec("8.8.4.4", base + timedelta(seconds=600))]     # 远离老簇
    alerts = det.detect(new, old + new, {}, known_ips_before=set(), now=base)
    assert alerts == []



def test_ip2region_v3_and_v2_formats():
    """ip2region v3 换了字段顺序，照抄网上 v2 的教程会把运营商塞进城市字段。"""
    from monitor.ipintel import IpIntel
    # v3: country|province|city|isp|countryCode
    assert IpIntel._parse_ip2region("中国|浙江省|嘉兴市|电信|CN") == ("中国", "浙江省", "嘉兴市", "电信")
    # v2: country|region|province|city|isp（region 恒为 0）
    assert IpIntel._parse_ip2region("中国|0|浙江省|嘉兴市|电信") == ("中国", "浙江省", "嘉兴市", "电信")
    # 空字段和 "0" 都要当成「没有」
    assert IpIntel._parse_ip2region("中国|0|0|0|内网IP") == ("中国", "", "", "内网IP")


def test_ip_profile_location_text_dedupes():
    from monitor.models import IpProfile
    p = IpProfile(ip="1.2.3.4", country="中国", region="浙江省", city="嘉兴市", district="南湖区")
    assert p.location_text == "中国 浙江省 嘉兴市 南湖区"
    # 直辖市这种「北京市 北京市」不该重复念两遍
    p2 = IpProfile(ip="1.2.3.4", country="中国", region="北京市", city="北京市")
    assert p2.location_text == "中国 北京市"
    assert IpProfile(ip="1.2.3.4").location_text == "未知"


def test_private_ip_short_circuits():
    from monitor.ipintel import IpIntel
    from monitor.models import IpProfile
    p = IpProfile(ip="192.168.1.10")
    assert IpIntel._fill_local(p) is True
    assert p.is_private and p.accuracy == "private"
    assert IpIntel._fill_local(IpProfile(ip="223.5.5.5")) is False




def test_decoy_table_without_ips_never_wins():
    """页面上常常还有一张「最新文章」表：只有标题和时间、一个 IP 都没有。

    以前打分时直接跑 IPv6 正则，「09:11:01」这种时间串也会被算成 IP，
    于是 30 行的假表能压过 20 行的真表，然后整页掉进正则兜底。
    """
    decoy = "".join(f"<tr><td>文章{i}</td><td>2026-08-27 09:{i:02d}:01</td></tr>" for i in range(30))
    real = "".join(
        f"<tr><td>{i}</td><td>2026-08-27 15:{i:02d}:11</td><td>10.1.2.{i}</td><td>/p{i}.htm</td></tr>"
        for i in range(20))
    html = (f"<html><body><table><tr><th>标题</th><th>发布时间</th></tr>{decoy}</table>"
            f"<table><tr><th>序号</th><th>访问时间</th><th>来访IP</th><th>访问页面</th></tr>"
            f"{real}</table></body></html>")
    recs = parse_records(html)
    assert len(recs) == 20, f"应该选中真正的记录表，实际解析出 {len(recs)} 条"
    assert all(r.visited_at is not None for r in recs), "时间必须都解析出来"
    assert recs[0].ip.startswith("10.1.2.")


def test_fallback_keeps_time_on_the_same_line_as_ip():
    """兜底解析必须能把同一行的 IP 和时间配上。

    否则所有记录都没有时间，会被统一按「此刻」处理，一批记录挤在同一瞬间，
    直接凑成一次假突发——跨度显示「0 秒内 N 条」。
    """
    rows = "".join(
        f"<tr><td>{i}</td><td>2026-08-27 1{i}:0{i}:00</td><td>10.9.9.{i}</td></tr>" for i in range(1, 5))
    # 故意不给表头，且外面套一层，让表格打分路径失效，强制走兜底
    html = f"<html><body><table>{rows}</table></body></html>"
    from monitor.parser import _fallback_regex
    recs = _fallback_regex(html, None)
    assert len(recs) == 4, [r.ip for r in recs]
    assert all(r.visited_at is not None for r in recs), \
        "兜底解析也必须带上时间，否则会制造假突发"
    assert len({r.visited_at for r in recs}) == 4, "四条记录的时间应该各不相同"


def test_fallback_handles_div_based_rows():
    """有些后台一个字段一个 <div>，不能因为没有 </tr> 就把整页并成一行。"""
    from monitor.parser import _fallback_regex
    html = ("<div class='row'><span>2026-08-27 10:00:01</span><span>10.1.1.1</span></div>"
            "<div class='row'><span>2026-08-27 10:00:05</span><span>10.1.1.2</span></div>"
            "<div class='row'><span>2026-08-27 10:00:09</span><span>10.1.1.3</span></div>")
    recs = _fallback_regex(html, None)
    assert [r.ip for r in recs] == ["10.1.1.1", "10.1.1.2", "10.1.1.3"], [r.ip for r in recs]
    assert all(r.visited_at is not None for r in recs)


def test_degraded_rows_do_not_collapse_into_one():
    """只认出 IP、其它字段全空时，多条记录不能坍缩成一条。

    坍缩的后果是双份的：当轮凑不够阈值不告警，而且这个指纹一旦入库，
    该 IP 之后每一条访问都会被当成「见过了」永久丢弃。
    """
    from monitor.parser import _disambiguate
    from monitor.models import VisitRecord
    recs = _disambiguate([VisitRecord(ip="7.7.7.7") for _ in range(4)])
    assert len({r.key for r in recs}) == 4, "四条退化记录必须有四个不同指纹"


def test_browser_version_is_not_mistaken_for_an_ip():
    """UA 里的「Chrome/121.0.0.0」和 IPv4 长得一模一样。"""
    html = ("<table><tr><td>2026-08-27 10:00:01</td><td>浙江</td>"
            "<td>Mozilla/5.0 Chrome/121.0.0.0 Safari/537.36</td><td>203.0.113.9</td></tr>"
            "<tr><td>2026-08-27 10:00:04</td><td>江苏</td>"
            "<td>Mozilla/5.0 Chrome/121.0.0.0 Safari/537.36</td><td>203.0.113.8</td></tr></table>")
    recs = parse_records(html)
    assert [r.ip for r in recs] == ["203.0.113.9", "203.0.113.8"], [r.ip for r in recs]


def test_month_day_across_new_year_is_not_a_year_in_the_future():
    ref = datetime(2027, 1, 3, 9, 0, 0)
    got = parse_datetime("12-31 23:05:00", ref)
    assert got == datetime(2026, 12, 31, 23, 5), got
    # 同年的正常日期不受影响
    assert parse_datetime("01-02 08:00:00", ref) == datetime(2027, 1, 2, 8, 0)


def test_raw_time_keeps_the_key_stable_around_midnight():
    """页面只给「23:50:00」时，我们补出来的日期会随「现在几点」变化。

    如果指纹用补出来的 datetime，同一行记录在午夜前后会算出两个不同的指纹，
    于是重复入库、重复告警。指纹用页面原样的字符串就没这个问题。
    """
    html = "<table><tr><td>23:50:00</td><td>1.2.3.4</td><td>/a.htm</td></tr></table>"
    # 11:40 和 12:00 正好跨过「比现在晚 12 小时」这条线，补出来的日期会翻转
    before = parse_records(html, reference_time=datetime(2026, 8, 27, 12, 0))
    after = parse_records(html, reference_time=datetime(2026, 8, 27, 11, 40))
    assert before[0].visited_at != after[0].visited_at, "前提：补出来的日期确实会变"
    assert before[0].key == after[0].key, "但指纹必须稳定，否则会重复入库、重复告警"


def test_colspan_does_not_shift_columns():
    html = ("<table>"
            "<tr><th>序号</th><th>访问时间</th><th>来访IP</th><th>访问页面</th></tr>"
            "<tr><td colspan='2'>合并单元格</td><td>10.0.0.7</td><td>/x.htm</td></tr>"
            "<tr><td>2</td><td>2026-08-27 10:00:00</td><td>10.0.0.8</td><td>/y.htm</td></tr>"
            "</table>")
    recs = parse_records(html)
    assert [r.ip for r in recs] == ["10.0.0.7", "10.0.0.8"], [r.ip for r in recs]



if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(list(globals().items())):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"  ✓ {name}")
            except AssertionError as exc:
                failures += 1
                print(f"  ✗ {name}: {exc}")
            except Exception as exc:  # noqa: BLE001
                failures += 1
                print(f"  ✗ {name}: {type(exc).__name__}: {exc}")
    print("全部通过" if not failures else f"{failures} 个测试失败")
    sys.exit(1 if failures else 0)
