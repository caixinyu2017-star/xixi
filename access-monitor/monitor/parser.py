"""把「最近访问记录」页面的 HTML 解析成 VisitRecord 列表。

我们**没有**博达后台的页面源码，各学校的版本、列顺序、列名也不一样，所以这里不写死
选择器，而是三层兜底：

  1. 表头匹配：找到所有 <table>，按「表头里有没有 IP/时间/页面这类词 + 单元格里像不像 IP」
     打分，挑分最高的那张表，再按表头中文把列映射到字段。
  2. 无表头推断：没有 <th>/表头行时，按「哪一列的值长得像 IP、哪一列长得像时间」来定位。
  3. 全文兜底：连表格都认不出来时，直接从整页文本里正则捞 IP + 时间，至少不会漏报。

`python run.py dump` 会把原始 HTML 存到 dumps/，拿到真实页面后可以用
`python run.py parse dumps/xxx.html` 单独调参数，不用反复登录。
"""
from __future__ import annotations

import ipaddress
import logging
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Sequence, Tuple

from .models import VisitRecord

log = logging.getLogger(__name__)

try:  # bs4 是主力
    from bs4 import BeautifulSoup  # type: ignore
    _HAS_BS4 = True
except ImportError:  # pragma: no cover - 只在没装依赖时走到
    BeautifulSoup = None  # type: ignore
    _HAS_BS4 = False


IPV4_RE = re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\b")
IPV6_RE = re.compile(r"(?<![:.\w])(?:[0-9A-Fa-f]{0,4}:){2,7}[0-9A-Fa-f]{0,4}(?:%[0-9A-Za-z]+)?(?![:.\w])")

DATETIME_PATTERNS: Sequence[Tuple[re.Pattern, str]] = (
    (re.compile(r"\b(\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2})\b"), "%Y-%m-%d %H:%M:%S"),
    (re.compile(r"\b(\d{4}/\d{2}/\d{2}[ T]\d{2}:\d{2}:\d{2})\b"), "%Y/%m/%d %H:%M:%S"),
    (re.compile(r"\b(\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2})\b"), "%Y-%m-%d %H:%M"),
    (re.compile(r"\b(\d{4}/\d{2}/\d{2}[ T]\d{2}:\d{2})\b"), "%Y/%m/%d %H:%M"),
    (re.compile(r"\b(\d{4}年\d{1,2}月\d{1,2}日\s*\d{1,2}:\d{2}:\d{2})\b"), "%Y年%m月%d日 %H:%M:%S"),
    (re.compile(r"\b(\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\b"), "%m-%d %H:%M:%S"),
    (re.compile(r"\b(\d{2}:\d{2}:\d{2})\b"), "%H:%M:%S"),
)

# 表头中文 -> 字段名。key 是「表头里包含的关键词」，匹配时统一去空格、转小写。
HEADER_MAP: Sequence[Tuple[Sequence[str], str]] = (
    (("来访ip", "访问ip", "客户端ip", "访客ip", "ip地址", "来源ip", "ip"), "ip"),
    (("访问时间", "来访时间", "时间", "日期", "datetime", "time"), "visited_at"),
    (("访问页面", "访问地址", "页面地址", "访问url", "url", "网址", "地址", "页面"), "page"),
    (("页面标题", "标题", "文章标题", "title"), "page_title"),
    (("来源页面", "来源地址", "来路", "referer", "referrer", "来源"), "referer"),
    (("浏览器", "客户端", "user agent", "useragent", "ua", "终端"), "user_agent"),
    (("操作系统", "系统", "os"), "os"),
    (("所属站点", "站点", "网站", "site"), "site"),
    (("地区", "地域", "省份", "归属地", "位置", "来访地"), "location_hint"),
)

_WS_RE = re.compile(r"[\s 　]+")

_ONE_DAY = timedelta(days=1)
_FUTURE_TOLERANCE = timedelta(hours=12)


def _norm(text: str) -> str:
    return _WS_RE.sub(" ", (text or "")).strip()


def _norm_header(text: str) -> str:
    return _WS_RE.sub("", (text or "")).strip().lower()


# --------------------------------------------------------------------------- #
# 基础提取
# --------------------------------------------------------------------------- #
def extract_ip(text: str) -> str:
    """从一段文本里抠出 IP。

    注意：`15:32:11` 这类时间串长得很像 IPv6，所以候选串一律交给 ipaddress 校验，
    不能只靠正则——不然「访问时间」列会被误判成「IP」列。
    """
    if not text:
        return ""
    m = IPV4_RE.search(text)
    if m:
        return m.group(0)
    for m in IPV6_RE.finditer(text):
        candidate = m.group(0).split("%")[0]
        if candidate.count(":") < 2:
            continue
        try:
            ipaddress.IPv6Address(candidate)
        except ValueError:
            continue
        return candidate
    return ""


def parse_datetime(text: str, reference: Optional[datetime] = None) -> Optional[datetime]:
    """把单元格文本转成 datetime。缺年/缺日期的，用 reference（默认当前时间）补齐。"""
    if not text:
        return None
    text = _norm(text).replace("T", " ")
    ref = reference or datetime.now()
    for pattern, fmt in DATETIME_PATTERNS:
        m = pattern.search(text)
        if not m:
            continue
        raw = _WS_RE.sub(" ", m.group(1)).replace("T", " ")
        try:
            dt = datetime.strptime(raw, fmt)
        except ValueError:
            continue
        if "%Y" not in fmt:
            dt = dt.replace(year=ref.year)
            if "%m" not in fmt:
                dt = dt.replace(month=ref.month, day=ref.day)
            # 只有时分秒时，若比现在晚很多，说明其实是昨天的记录
            if dt - ref > _FUTURE_TOLERANCE:
                dt -= _ONE_DAY
        return dt
    return None


# --------------------------------------------------------------------------- #
# 表格解析
# --------------------------------------------------------------------------- #
def _cell_text_and_link(cell) -> Tuple[str, str]:
    text = _norm(cell.get_text(" ", strip=True))
    href = ""
    a = cell.find("a")
    if a is not None:
        href = _norm(a.get("href") or "")
        if a.get("title"):
            text = text or _norm(a.get("title"))
    if not text:
        for attr in ("title", "alt"):
            val = cell.get(attr)
            if val:
                text = _norm(val)
                break
    return text, href


def _own_rows(table) -> List:
    """只取属于这张表自己的 <tr>（博达后台大量使用嵌套表格做布局）。"""
    rows = []
    for tr in table.find_all("tr"):
        parent_table = tr.find_parent("table")
        if parent_table is table:
            rows.append(tr)
    return rows


def _score_table(table) -> Tuple[float, List]:
    rows = _own_rows(table)
    if len(rows) < 2:
        return 0.0, rows
    ip_rows = 0
    time_rows = 0
    for tr in rows[:60]:
        text = tr.get_text(" ", strip=True)
        if IPV4_RE.search(text) or IPV6_RE.search(text):
            ip_rows += 1
        if any(p.search(text) for p, _ in DATETIME_PATTERNS[:5]):
            time_rows += 1
    header_text = _norm_header(rows[0].get_text(" ", strip=True))
    header_hits = sum(1 for keys, _ in HEADER_MAP if any(k in header_text for k in keys))
    score = ip_rows * 3.0 + time_rows * 1.5 + header_hits * 2.0
    # 嵌套布局表通常只有 1~2 行有效数据，压低它们
    if ip_rows == 0:
        score *= 0.1
    return score, rows


def _map_header(header_cells: Sequence[str]) -> Dict[int, str]:
    """表头文字 -> 列索引到字段名的映射。"""
    mapping: Dict[int, str] = {}
    used: set = set()
    normalized = [_norm_header(h) for h in header_cells]
    # 先匹配更长更具体的关键词，避免 "ip" 抢走 "来访ip"
    for keys, field in HEADER_MAP:
        if field in used:
            continue
        best_idx, best_len = -1, -1
        for idx, h in enumerate(normalized):
            if idx in mapping or not h:
                continue
            for k in keys:
                if k in h and len(k) > best_len:
                    best_idx, best_len = idx, len(k)
        if best_idx >= 0:
            mapping[best_idx] = field
            used.add(field)
    return mapping


def _infer_columns(data_rows: Sequence[Sequence[str]]) -> Dict[int, str]:
    """没有可用表头时，靠内容猜列。"""
    if not data_rows:
        return {}
    width = max(len(r) for r in data_rows)
    ip_hits = [0] * width
    time_hits = [0] * width
    url_hits = [0] * width
    for row in data_rows[:40]:
        for i, cell in enumerate(row):
            if i >= width:
                break
            if extract_ip(cell):
                ip_hits[i] += 1
            if parse_datetime(cell):
                time_hits[i] += 1
            if "/" in cell and ("http" in cell.lower() or cell.strip().startswith("/")):
                url_hits[i] += 1
    mapping: Dict[int, str] = {}
    if max(ip_hits, default=0) > 0:
        mapping[ip_hits.index(max(ip_hits))] = "ip"
    if max(time_hits, default=0) > 0:
        idx = time_hits.index(max(time_hits))
        if idx not in mapping:
            mapping[idx] = "visited_at"
    if max(url_hits, default=0) > 0:
        idx = url_hits.index(max(url_hits))
        if idx not in mapping:
            mapping[idx] = "page"
    return mapping


def _looks_like_header(cells: Sequence[str]) -> bool:
    joined = _norm_header(" ".join(cells))
    if not joined:
        return False
    if IPV4_RE.search(" ".join(cells)):
        return False
    hits = sum(1 for keys, _ in HEADER_MAP if any(k in joined for k in keys))
    return hits >= 2


def parse_records(html: str, reference_time: Optional[datetime] = None) -> List[VisitRecord]:
    """主入口：HTML -> 记录列表。解析不到就返回空列表（调用方负责告警/dump）。"""
    if not html:
        return []
    if not _HAS_BS4:
        log.warning("没装 beautifulsoup4，退化为纯正则解析（准确度较低）")
        return _fallback_regex(html, reference_time)

    soup = BeautifulSoup(html, "lxml" if _lxml_available() else "html.parser")
    for tag in soup.find_all(["script", "style"]):
        tag.decompose()

    tables = soup.find_all("table")
    best_table, best_rows, best_score = None, [], 0.0
    for t in tables:
        score, rows = _score_table(t)
        if score > best_score:
            best_table, best_rows, best_score = t, rows, score

    if best_table is None or best_score <= 0:
        log.debug("没找到像样的表格（共 %d 张表），走全文正则兜底", len(tables))
        return _fallback_regex(html, reference_time)

    grid: List[List[Tuple[str, str]]] = []
    for tr in best_rows:
        cells = tr.find_all(["td", "th"], recursive=False) or tr.find_all(["td", "th"])
        if not cells:
            continue
        grid.append([_cell_text_and_link(c) for c in cells])
    if not grid:
        return _fallback_regex(html, reference_time)

    header_cells = [c[0] for c in grid[0]]
    if _looks_like_header(header_cells):
        mapping = _map_header(header_cells)
        headers = header_cells
        body = grid[1:]
    else:
        mapping = {}
        headers = []
        body = grid
    if "ip" not in mapping.values():
        inferred = _infer_columns([[c[0] for c in row] for row in body])
        for idx, field in inferred.items():
            mapping.setdefault(idx, field)

    records: List[VisitRecord] = []
    for row_index, row in enumerate(body):
        texts = [c[0] for c in row]
        if not any(texts):
            continue
        rec = _row_to_record(row, mapping, headers, reference_time)
        if rec is None:
            continue
        rec.row_index = row_index
        records.append(rec)

    if not records:
        return _fallback_regex(html, reference_time)
    log.debug("表格解析成功：%d 行，列映射=%s", len(records), mapping)
    return records


def _row_to_record(
    row: Sequence[Tuple[str, str]],
    mapping: Dict[int, str],
    headers: Sequence[str],
    reference_time: Optional[datetime],
) -> Optional[VisitRecord]:
    values: Dict[str, str] = {}
    raw: Dict[str, str] = {}
    for idx, (text, href) in enumerate(row):
        field = mapping.get(idx)
        col_name = _norm(headers[idx]) if idx < len(headers) and headers else f"列{idx + 1}"
        if text or href:
            raw[col_name] = text or href
        if field:
            values[field] = text
            if field == "page" and href:
                # 页面列通常是 <a href="真实URL">标题</a>：URL 更适合做监控主键，
                # 标题则塞进 page_title（如果没有单独的标题列）。
                values["page"] = href
                values.setdefault("page_title_from_link", text)
        elif href:
            raw.setdefault(f"{col_name}(链接)", href)

    ip = extract_ip(values.get("ip", ""))
    if not ip:  # 列映射可能不准，整行再捞一次
        ip = extract_ip(" ".join(t for t, _ in row))
    if not ip:
        return None

    visited_at = parse_datetime(values.get("visited_at", ""), reference_time)
    if visited_at is None:
        for text, _ in row:
            visited_at = parse_datetime(text, reference_time)
            if visited_at:
                break

    page = values.get("page", "")
    page_title = values.get("page_title", "") or values.get("page_title_from_link", "")
    return VisitRecord(
        ip=ip,
        visited_at=visited_at,
        page=page,
        page_title=page_title,
        referer=values.get("referer", ""),
        user_agent=values.get("user_agent", ""),
        os=values.get("os", ""),
        site=values.get("site", ""),
        location_hint=values.get("location_hint", ""),
        raw=raw,
    )


def _fallback_regex(html: str, reference_time: Optional[datetime]) -> List[VisitRecord]:
    """最后的兜底：按行扫全文，捞出 IP（顺带捞同一行的时间）。"""
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", "\n", text)
    records: List[VisitRecord] = []
    for line in text.splitlines():
        line = _norm(line)
        ip = extract_ip(line)
        if not ip:
            continue
        records.append(VisitRecord(
            ip=ip,
            visited_at=parse_datetime(line, reference_time),
            page="",
            raw={"原始行": line[:300]},
        ))
    if records:
        log.debug("正则兜底解析出 %d 条记录", len(records))
    return records


def _lxml_available() -> bool:
    try:
        import lxml  # noqa: F401
        return True
    except ImportError:
        return False


def describe_parse(html: str) -> str:
    """给 `run.py parse` 用的诊断输出。"""
    lines: List[str] = []
    if not _HAS_BS4:
        return "未安装 beautifulsoup4，无法做结构化诊断。请先 pip install -r requirements.txt"
    soup = BeautifulSoup(html, "lxml" if _lxml_available() else "html.parser")
    tables = soup.find_all("table")
    lines.append(f"页面里共有 {len(tables)} 张 <table>")
    scored = sorted(((_score_table(t)[0], i, t) for i, t in enumerate(tables)), reverse=True)
    for score, i, t in scored[:5]:
        rows = _own_rows(t)
        head = _norm(rows[0].get_text(" ", strip=True))[:120] if rows else ""
        lines.append(f"  表 #{i}: 得分 {score:.1f}, {len(rows)} 行, 首行: {head}")
    recs = parse_records(html)
    lines.append(f"解析出 {len(recs)} 条记录")
    for r in recs[:5]:
        lines.append(f"  {r.visited_at} | {r.ip} | {r.page[:60]} | {list(r.raw)[:6]}")
    return "\n".join(lines)
