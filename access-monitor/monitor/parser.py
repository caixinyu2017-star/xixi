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
_NEXT_YEAR_TOLERANCE = timedelta(days=7)
#: 「Chrome/121.0.0.0」这类版本号，后半段和 IPv4 无法用正则区分，只能靠前面的斜杠认出来
_VERSION_LIKE_RE = re.compile(r"[A-Za-z][\w.+-]*/\s*\d[\d.]*")


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
            try:
                dt = dt.replace(year=ref.year)
            except ValueError:            # 2 月 29 日碰上平年
                dt = dt.replace(year=ref.year, day=28)
            if "%m" not in fmt:
                # 只有时分秒：补今天的日期，比现在晚太多就说明其实是昨天的
                dt = dt.replace(month=ref.month, day=ref.day)
                if dt - ref > _FUTURE_TOLERANCE:
                    dt -= _ONE_DAY
            elif dt - ref > _NEXT_YEAR_TOLERANCE:
                # 有月日没年份：1 月看到「12-31」，补上今年会算到 11 个月后，
                # 实际是去年年底。按天数往回退一整年，别按一天退。
                try:
                    dt = dt.replace(year=ref.year - 1)
                except ValueError:
                    dt = dt.replace(year=ref.year - 1, day=28)
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
        # 必须用 extract_ip 而不是直接跑正则：IPV6_RE 是未校验的宽松式，
        # 「09:11:01」这种时间串也能匹配上。一张只有标题和时间的「最新文章」表
        # 会因此拿满每行 3 分的 IP 加分，反而压过真正的记录表。
        if extract_ip(text):
            ip_rows += 1
        if any(p.search(text) for p, _ in DATETIME_PATTERNS[:5]):
            time_rows += 1
    if ip_rows < 2:
        # 一条 IP 都没有的表不可能是记录表；只有一条的多半是布局表包住了内层的一格
        return 0.0, rows
    header_text = _norm_header(rows[0].get_text(" ", strip=True))
    header_hits = sum(1 for keys, _ in HEADER_MAP if any(k in header_text for k in keys))
    return ip_rows * 3.0 + time_rows * 1.5 + header_hits * 2.0, rows


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
    exact_ip_hits = [0] * width      # 整格就是一个 IP —— 最可信
    ip_hits = [0] * width            # 格子里含 IP
    time_hits = [0] * width
    url_hits = [0] * width
    for row in data_rows[:40]:
        for i, cell in enumerate(row):
            if i >= width:
                break
            text = (cell or "").strip()
            if IPV4_RE.fullmatch(text):
                exact_ip_hits[i] += 1
            # 先把「Chrome/121.0.0.0」这类版本号抹掉再找 IP，
            # 否则浏览器列会被当成 IP 列（版本号和 IPv4 长得一样）
            if extract_ip(_VERSION_LIKE_RE.sub(" ", text)):
                ip_hits[i] += 1
            if parse_datetime(text):
                time_hits[i] += 1
            if "/" in text and ("http" in text.lower() or text.startswith("/")):
                url_hits[i] += 1
    mapping: Dict[int, str] = {}
    if max(exact_ip_hits, default=0) > 0:
        mapping[exact_ip_hits.index(max(exact_ip_hits))] = "ip"
    elif max(ip_hits, default=0) > 0:
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


def _ip_column_holds_up(mapping: Dict[int, str], body: Sequence[Sequence[str]]) -> bool:
    """检查表头标出来的 IP 列里是不是真的有 IP。"""
    idx = next((i for i, field in mapping.items() if field == "ip"), None)
    if idx is None:
        return False
    rows_with_ip = [row for row in body if any(extract_ip(c) for c in row)]
    if not rows_with_ip:
        return True                     # 整表都没 IP，不是这条规则该管的事
    hits = sum(1 for row in rows_with_ip if idx < len(row) and extract_ip(row[idx]))
    return hits >= len(rows_with_ip) * 0.5


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
        row: List[Tuple[str, str]] = []
        for c in cells:
            value = _cell_text_and_link(c)
            row.append(value)
            # colspan 不展开的话，后面所有列都会整体左移，列映射全错位
            try:
                span = int(str(c.get("colspan") or 1))
            except (TypeError, ValueError):
                span = 1
            for _ in range(max(0, min(span, 20) - 1)):
                row.append(("", ""))
        grid.append(row)
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
    body_texts = [[c[0] for c in row] for row in body]
    if "ip" in mapping.values() and not _ip_column_holds_up(mapping, body_texts):
        # 表头写着「IP」但那一列里根本没有 IP：多半是 colspan / 合并单元格错位了。
        # 这时候宁可不信表头，改按内容推断，否则整表都会解析错位。
        log.debug("表头标出的 IP 列里没有 IP，改按内容推断列")
        mapping = {}
    if "ip" not in mapping.values():
        inferred = _infer_columns(body_texts)
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
    return _disambiguate(records)


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
    if not ip:
        # 列映射可能不准，整行再捞一次。但要小心 UA 里的版本号：
        # 「Chrome/121.0.0.0」的后半段长得和 IPv4 一模一样。
        ip = _rescue_ip([t for t, _ in row])
    if not ip:
        return None

    raw_time = _first_time_text(values.get("visited_at", ""))
    visited_at = parse_datetime(values.get("visited_at", ""), reference_time)
    if visited_at is None:
        for text, _ in row:
            visited_at = parse_datetime(text, reference_time)
            if visited_at:
                raw_time = _first_time_text(text)
                break

    page = values.get("page", "")
    page_title = values.get("page_title", "") or values.get("page_title_from_link", "")
    return VisitRecord(
        ip=ip,
        visited_at=visited_at,
        raw_time=raw_time,
        page=page,
        page_title=page_title,
        referer=values.get("referer", ""),
        user_agent=values.get("user_agent", ""),
        os=values.get("os", ""),
        site=values.get("site", ""),
        location_hint=values.get("location_hint", ""),
        raw=raw,
    )


_BLOCK_END_RE = re.compile(r"(?i)</(tr|table|div|p|li|h[1-6]|section|article)\s*>|<br\s*/?>")


def _rescue_ip(cells: Sequence[str]) -> str:
    """列没映射对时，从整行里找出最可能是 IP 的那一格。

    优先级：整格就是一个 IP > 不含版本号特征的格子 > 全行硬捞。
    这样「Chrome/121.0.0.0」不会被当成来访 IP。
    """
    for cell in cells:
        text = (cell or "").strip()
        if text and IPV4_RE.fullmatch(text):
            return text
    for cell in cells:
        text = cell or ""
        if _VERSION_LIKE_RE.search(text):
            continue
        found = extract_ip(text)
        if found:
            return found
    joined = " ".join(_VERSION_LIKE_RE.sub(" ", c or "") for c in cells)
    return extract_ip(joined)


def _fallback_regex(html: str, reference_time: Optional[datetime]) -> List[VisitRecord]:
    """最后的兜底：按「块」扫全文，捞出 IP 和同一块里的时间。

    关键是切分粒度：如果把**每个**标签都换成换行，`</td><td>` 也会被切开，
    同一行记录的 IP 和时间就永远落在不同行上，解析出来的记录全都没有时间。
    没有时间的记录会被统一按「此刻」处理，于是一批记录挤在同一瞬间——
    直接凑成一次假突发。所以只在块级边界换行，单元格内的标签换成空格。
    """
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    text = _BLOCK_END_RE.sub("\n", text)
    text = re.sub(r"<[^>]+>", " ", text)          # 剩下的行内标签换空格，别拆行
    chunks = [_norm(line) for line in text.splitlines()]

    records: List[VisitRecord] = []
    for i, line in enumerate(chunks):
        if not line:
            continue
        found = [m.group(0) for m in IPV4_RE.finditer(line)]
        if not found:
            candidate = extract_ip(line)
            found = [candidate] if candidate else []
        if not found:
            continue
        when = parse_datetime(line, reference_time)
        raw_time = _first_time_text(line)
        if when is None:
            # 有些后台一个字段一个 <div>，时间可能落在相邻的块里
            for j in (i - 1, i + 1, i - 2, i + 2):
                if 0 <= j < len(chunks) and not extract_ip(chunks[j]):
                    when = parse_datetime(chunks[j], reference_time)
                    if when is not None:
                        raw_time = _first_time_text(chunks[j])
                        break
        for ip in dict.fromkeys(found):
            records.append(VisitRecord(
                ip=ip, visited_at=when, raw_time=raw_time, page="",
                raw={"原始行": line[:300]},
            ))
    if records:
        log.debug("正则兜底解析出 %d 条记录", len(records))
    return _disambiguate(records)


def _disambiguate(records: List[VisitRecord]) -> List[VisitRecord]:
    """同一批里指纹撞车的记录，按出现次序编号。

    为什么必须做：一行如果只认出了 IP、时间和页面都没解析出来，指纹就退化成
    「只含 IP」。同一个 IP 的 N 条访问会坍缩成 1 条，后果是双份的——当轮凑不够
    阈值不告警，而且这个指纹一旦入库，该 IP 之后**每一条**访问都会被判为
    「已经见过」而丢弃，等于对这个 IP 永久失明。
    """
    seen: Dict[str, int] = {}
    degraded = 0
    for rec in records:
        base = rec.key
        n = seen.get(base, 0)
        seen[base] = n + 1
        if n:
            rec.dup_index = n
        if rec.is_degraded:
            degraded += 1
    if degraded:
        log.warning("有 %d 条记录只解析出了 IP（时间和页面都没认出来），去重能力已退化。"
                    "建议跑一次 `run.py discover` 把页面导出来调解析规则。", degraded)
    return records


def _first_time_text(text: str) -> str:
    """把页面上原样的时间字符串抠出来，用于生成稳定的去重指纹。"""
    for pattern, _ in DATETIME_PATTERNS:
        m = pattern.search(text or "")
        if m:
            return m.group(1)
    return ""


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
