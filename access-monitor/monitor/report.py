"""把告警渲染成人能看的几种格式：纯文本 / Markdown / HTML 邮件。

IP 信息尽量摊开写：位置精确到区县、运营商、AS 号、反向域名、标签（爬虫/机房/代理/校园网）、
以及一个可以直接点开的地图链接。
"""
from __future__ import annotations

import html as html_lib
from datetime import datetime
from typing import Dict, List, Sequence

from .models import Alert, IpProfile, VisitRecord

MAX_RECORDS_IN_BODY = 40


# --------------------------------------------------------------------------- #
def _fmt_time(dt) -> str:
    return dt.strftime("%m-%d %H:%M:%S") if isinstance(dt, datetime) else "时间未知"


def _map_link(prof: IpProfile) -> str:
    if prof.lat is None or prof.lon is None:
        return ""
    return f"https://www.openstreetmap.org/?mlat={prof.lat}&mlon={prof.lon}#map=11/{prof.lat}/{prof.lon}"


def _profile_lines(prof: IpProfile) -> List[str]:
    lines = [f"位置：{prof.location_text}" + (f"（精度：{prof.accuracy}）" if prof.accuracy else "")]
    if prof.network_text != "未知":
        lines.append(f"网络：{prof.network_text}")
    if prof.rdns:
        lines.append(f"反向域名：{prof.rdns}")
    if prof.labels:
        lines.append(f"标签：{'、'.join(prof.labels)}")
    if prof.zip_code:
        lines.append(f"邮编：{prof.zip_code}")
    if prof.risk_reasons:
        lines.append(f"判断：{'；'.join(prof.risk_reasons)}")
    if prof.sources:
        lines.append(f"数据来源：{'、'.join(dict.fromkeys(prof.sources))}")
    link = _map_link(prof)
    if link:
        lines.append(f"地图：{link}")
    return lines


def _ip_counts(records: Sequence[VisitRecord]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for r in records:
        counts[r.ip] = counts.get(r.ip, 0) + 1
    return dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))


# --------------------------------------------------------------------------- #
def render_short(alert: Alert, limit: int = 120) -> str:
    """给手机推送用的一句话。"""
    counts = _ip_counts(alert.records)
    top = list(counts)[:2]
    where = []
    for ip in top:
        prof = alert.profiles.get(ip)
        where.append(f"{ip}({prof.location_text})" if prof else ip)
    text = f"{alert.summary} 主要来源：{'、'.join(where)}" if where else alert.summary
    return text if len(text) <= limit else text[: limit - 1] + "…"


def render_text(alert: Alert) -> str:
    lines = [alert.title, "=" * 40, alert.summary, ""]
    counts = _ip_counts(alert.records)

    lines.append(f"【IP 分析】共 {len(counts)} 个 IP")
    for ip, n in counts.items():
        prof = alert.profiles.get(ip)
        lines.append(f"\n● {ip}（本次 {n} 次访问）" + (f"  风险分 {prof.risk_score}" if prof else ""))
        if prof:
            lines += ["    " + line for line in _profile_lines(prof)]
        else:
            lines.append("    （未查询到归属信息）")

    lines.append("")
    shown = alert.records[:MAX_RECORDS_IN_BODY]
    lines.append(f"【访问明细】共 {len(alert.records)} 条" +
                 (f"，以下显示前 {len(shown)} 条" if len(shown) < len(alert.records) else ""))
    for r in shown:
        page = r.page_title or r.page or "-"
        lines.append(f"  {_fmt_time(r.visited_at)}  {r.ip:<16}  {page[:60]}")
        if r.referer and r.referer not in ("-", ""):
            lines.append(f"{'':>26}来源：{r.referer[:80]}")

    lines += ["", f"触发时间：{alert.triggered_at:%Y-%m-%d %H:%M:%S}",
              f"规则：{alert.rule}｜级别：{alert.severity}",
              "—— 由 access-monitor 自动发送"]
    return "\n".join(lines)


def render_markdown(alert: Alert) -> str:
    """给企业微信 / 钉钉 / 飞书用（它们的 markdown 子集都比较窄，别用表格）。"""
    lines = [f"### {alert.title}", "", alert.summary, ""]
    counts = _ip_counts(alert.records)
    for ip, n in list(counts.items())[:6]:
        prof = alert.profiles.get(ip)
        if prof:
            tags = f"（{'、'.join(prof.labels)}）" if prof.labels else ""
            lines.append(f"> **{ip}** ×{n}{tags}")
            lines.append(f"> {prof.location_text}｜{prof.network_text}")
            if prof.rdns:
                lines.append(f"> 反向域名 {prof.rdns}")
        else:
            lines.append(f"> **{ip}** ×{n}")
        lines.append("")
    if len(counts) > 6:
        lines.append(f"> …另有 {len(counts) - 6} 个 IP")
    lines.append(f"\n时间：{alert.triggered_at:%Y-%m-%d %H:%M:%S}")
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
_HTML_STYLE = """
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;
     color:#1a1a1a;line-height:1.6;margin:0;padding:0;background:#f5f6f8}
.wrap{max-width:760px;margin:0 auto;padding:20px}
.card{background:#fff;border-radius:10px;padding:20px 24px;margin-bottom:16px;
      box-shadow:0 1px 3px rgba(0,0,0,.08)}
h1{font-size:19px;margin:0 0 6px}
.sub{color:#555;font-size:14px;margin:0 0 4px}
.badge{display:inline-block;padding:2px 8px;border-radius:10px;font-size:12px;margin-right:6px}
.b-warn{background:#fff4e5;color:#a35b00}.b-crit{background:#fdeaea;color:#b3261e}
.b-info{background:#e8f0fe;color:#1a56b3}.b-tag{background:#eef1f5;color:#41485a}
table{width:100%;border-collapse:collapse;font-size:13px;margin-top:8px}
th,td{border-bottom:1px solid #eceef2;padding:7px 6px;text-align:left;vertical-align:top}
th{background:#fafbfc;font-weight:600;color:#444;white-space:nowrap}
td.ip{font-family:ui-monospace,Menlo,Consolas,monospace;white-space:nowrap}
.kv{font-size:13px;color:#333;margin:2px 0}
.kv b{color:#666;font-weight:500;display:inline-block;min-width:5.2em}
.risk{float:right;font-size:12px;color:#888}
.foot{color:#8a8f99;font-size:12px;text-align:center;padding:8px}
a{color:#1a56b3}
"""


def render_html(alert: Alert) -> str:
    e = html_lib.escape
    badge = {"critical": "b-crit", "warning": "b-warn"}.get(alert.severity, "b-info")
    counts = _ip_counts(alert.records)

    parts = [
        "<!doctype html><html><head><meta charset='utf-8'>",
        f"<style>{_HTML_STYLE}</style></head><body><div class='wrap'>",
        "<div class='card'>",
        f"<h1>{e(alert.title)}</h1>",
        f"<p class='sub'><span class='badge {badge}'>{e(alert.severity)}</span>"
        f"<span class='badge b-tag'>规则 {e(alert.rule)}</span>{e(alert.triggered_at.strftime('%Y-%m-%d %H:%M:%S'))}</p>",
        f"<p class='sub'>{e(alert.summary)}</p>",
        "</div>",
    ]

    parts.append("<div class='card'><h1>IP 分析</h1>")
    for ip, n in counts.items():
        prof = alert.profiles.get(ip)
        risk = f"<span class='risk'>风险分 {prof.risk_score}</span>" if prof else ""
        tags = "".join(f"<span class='badge b-tag'>{e(t)}</span>" for t in (prof.labels if prof else []))
        parts.append(f"<div style='margin:14px 0 4px'><b style='font-family:monospace'>{e(ip)}</b> "
                     f"<span class='badge b-tag'>{n} 次</span>{tags}{risk}</div>")
        if not prof:
            parts.append("<div class='kv'>未查询到归属信息</div>")
            continue
        rows = [("位置", prof.location_text + (f"（精度 {prof.accuracy}）" if prof.accuracy else "")),
                ("网络", prof.network_text)]
        if prof.rdns:
            rows.append(("反向域名", prof.rdns))
        if prof.zip_code:
            rows.append(("邮编", prof.zip_code))
        if prof.risk_reasons:
            rows.append(("判断", "；".join(prof.risk_reasons)))
        if prof.sources:
            rows.append(("数据来源", "、".join(dict.fromkeys(prof.sources))))
        for k, v in rows:
            parts.append(f"<div class='kv'><b>{e(k)}</b>{e(str(v))}</div>")
        link = _map_link(prof)
        if link:
            parts.append(f"<div class='kv'><b>地图</b><a href='{e(link)}'>在地图上查看</a></div>")
    parts.append("</div>")

    shown = alert.records[:MAX_RECORDS_IN_BODY]
    parts.append("<div class='card'><h1>访问明细</h1>")
    parts.append(f"<p class='sub'>共 {len(alert.records)} 条"
                 + (f"，显示前 {len(shown)} 条" if len(shown) < len(alert.records) else "") + "</p>")
    parts.append("<table><tr><th>时间</th><th>IP</th><th>页面</th><th>来源</th><th>浏览器</th></tr>")
    for r in shown:
        page = r.page_title or r.page or "-"
        page_cell = (f"<a href='{e(r.page)}'>{e(page[:70])}</a>"
                     if r.page.startswith("http") else e(page[:70]))
        parts.append(
            f"<tr><td>{e(_fmt_time(r.visited_at))}</td><td class='ip'>{e(r.ip)}</td>"
            f"<td>{page_cell}</td><td>{e((r.referer or '-')[:50])}</td>"
            f"<td>{e((r.user_agent or '-')[:30])}</td></tr>"
        )
    parts.append("</table></div>")
    parts.append("<div class='foot'>由 access-monitor 自动发送 · 如需调整阈值请修改 config.yaml</div>")
    parts.append("</div></body></html>")
    return "".join(parts)
