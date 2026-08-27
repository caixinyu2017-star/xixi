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
