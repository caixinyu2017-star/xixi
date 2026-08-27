"""在博达后台里找到并读取「最近访问记录」页面。

这个模块要解决的现实问题是：**我们事先不知道那个页面的真实 URL**。
博达各版本的 JSP 文件名、menuid、sysid 都不一样，网上也查不到，所以策略是：

  1. 第一次运行：像人一样点菜单（运营中心 → 访问统计 → 最近访问记录），
     点完把落地的 iframe URL 记到数据库里；
  2. 之后每次轮询：直接开那个 URL，几百毫秒就拿到数据；
  3. 万一 URL 失效（改版 / 掉线 / 参数过期）：自动退回第 1 步重新点一遍。

顺便在发现阶段监听所有 XHR —— 如果这个页面背后有 JSON 接口，日志里会记下来，
以后可以改成直接打接口，比渲染整个 JSP 便宜得多。
"""
from __future__ import annotations

import json
import logging
import re
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from .config import AppConfig
from .parser import parse_records

log = logging.getLogger(__name__)

STATE_KEY_RECORDS_URL = "records_url"
STATE_KEY_RECORDS_FRAME = "records_frame_name"

# 判断「这个 frame 里装的是记录表」用的关键词
CONTENT_MARKERS = ("最近访问记录", "来访IP", "访问时间", "访问统计", "访问页面")


@dataclass
class FetchResult:
    ok: bool
    html: str = ""
    url: str = ""
    frame_name: str = ""
    record_count: int = 0
    logged_out: bool = False
    #: 页面上出现了「最近访问记录 / 来访IP / 访问时间」这类特征词，确认是记录页。
    #: 这个标志很重要：解析器最后一层兜底是「全文正则捞 IP」，如果放它去啃一个
    #: 错误页或登录页，捞出来的垃圾 IP 会全部落在同一时刻，立刻触发一次假突发。
    verified: bool = False
    error: str = ""
    xhr_endpoints: List[str] = field(default_factory=list)


def sibling_webvpn_url(current_url: str, new_path: str) -> str:
    """在同一个 WebVPN 主机哈希下换路径。

    WebVPN 把上游主机加密成一段十六进制放在路径里，**哈希之后的路径是明文透传的**，
    所以只要上游主机和端口没变，就可以直接换后半段。
    例：https://webvpn.x.cn/http-8080/<hash>/system/caslogin.jsp
      → https://webvpn.x.cn/http-8080/<hash>/<new_path>
    """
    m = re.match(r"^(https?://[^/]+/[^/]+/[0-9a-fA-F]{16,}/)", current_url)
    if not m:
        return ""
    return m.group(1) + new_path.lstrip("/")


class RecordsNavigator:
    def __init__(self, cfg: AppConfig, session, store=None):
        self.cfg = cfg
        self.session = session
        self.store = store
        self._records_url: str = cfg.navigation.records_url or (
            store.get(STATE_KEY_RECORDS_URL) if store else ""
        )
        self._xhr: List[Dict[str, str]] = []
        self._sniffing = False

    @property
    def page(self):
        return self.session.page

    @property
    def records_url(self) -> str:
        return self._records_url

    # ------------------------------------------------------------------ #
    # 对外主入口
    # ------------------------------------------------------------------ #
    def fetch(self, force_rediscover: bool = False) -> FetchResult:
        """抓一次记录页面的 HTML。"""
        if self._records_url and not force_rediscover:
            result = self._fetch_by_url(self._records_url)
            if result.ok:
                return result
            if result.logged_out:
                return result
            log.info("记住的记录页地址不好使了（%s），重新点菜单查找", result.error or "无记录")

        result = self._discover_by_menu()
        if result.ok and result.url:
            self._remember(result.url)
        return result

    def _remember(self, url: str) -> None:
        if url and url != self._records_url:
            self._records_url = url
            if self.store:
                self.store.set(STATE_KEY_RECORDS_URL, url)
            log.info("已记住记录页地址：%s", url)

    # ------------------------------------------------------------------ #
    # 路线一：直接开记住的 URL
    # ------------------------------------------------------------------ #
    def _fetch_by_url(self, url: str) -> FetchResult:
        try:
            self.page.goto(url, wait_until="domcontentloaded")
        except Exception as exc:  # noqa: BLE001
            return FetchResult(ok=False, error=f"打开记录页失败：{exc}")
        self.session._settle()
        if self.session.looks_logged_out():
            return FetchResult(ok=False, logged_out=True, error="会话已过期")
        return self._read_best_frame(fallback_url=url)

    # ------------------------------------------------------------------ #
    # 路线二：点菜单找过去
    # ------------------------------------------------------------------ #
    def _discover_by_menu(self) -> FetchResult:
        target = self.cfg.webvpn.target_url
        if target:
            try:
                self.page.goto(target, wait_until="domcontentloaded")
                self.session._settle(extra_wait=1.0)
            except Exception as exc:  # noqa: BLE001
                return FetchResult(ok=False, error=f"打开后台首页失败：{exc}")
        if self.session.looks_logged_out():
            return FetchResult(ok=False, logged_out=True, error="会话已过期")

        self._start_sniffing()
        clicked: List[str] = []
        for label in self.cfg.navigation.menu_path:
            if self._click_menu_label(label):
                clicked.append(label)
                self.session._settle(extra_wait=0.8)
            else:
                log.warning("菜单里没找到「%s」（已点到：%s）", label, " → ".join(clicked) or "无")
        if not clicked:
            return FetchResult(
                ok=False,
                error="一个菜单项都没点到。请确认 navigation.menu_path 和后台实际菜单文字一致，"
                      "或者把 browser.headless 设为 false 亲眼看看。",
            )

        result = self._read_best_frame()
        result.xhr_endpoints = self._stop_sniffing()
        if result.xhr_endpoints:
            log.info("发现 %d 个候选 XHR 接口（已写入 dumps/xhr-endpoints.json）", len(result.xhr_endpoints))
        return result

    def _click_menu_label(self, label: str) -> bool:
        """在所有 frame 里找这个菜单文字并点它。"""
        selectors = [
            f"a:text-is('{label}')", f"span:text-is('{label}')", f"td:text-is('{label}')",
            f"li:text-is('{label}')", f"div:text-is('{label}')",
            f"a:has-text('{label}')", f"span:has-text('{label}')", f"*:text-is('{label}')",
        ]
        for frame in self._all_frames():
            for sel in selectors:
                try:
                    loc = frame.locator(sel).first
                    if loc.count() == 0 or not loc.is_visible():
                        continue
                    loc.click(timeout=5000)
                    log.debug("点击菜单「%s」（frame=%s, 选择器=%s）", label, frame.name or "main", sel)
                    return True
                except Exception:  # noqa: BLE001
                    continue
        return False

    # ------------------------------------------------------------------ #
    # 找出装着记录表的那个 frame
    # ------------------------------------------------------------------ #
    def _all_frames(self) -> List:
        try:
            return list(self.page.frames)
        except Exception:  # noqa: BLE001
            return [self.page]

    def _read_best_frame(self, fallback_url: str = "", wait_seconds: float = 8.0) -> FetchResult:
        """表格可能是 AJAX 异步塞进来的，所以要轮询等一会儿。"""
        deadline = time.monotonic() + wait_seconds
        best: Optional[Tuple[float, str, str, str, int, int]] = None
        while time.monotonic() < deadline:
            for frame in self._all_frames():
                try:
                    html = frame.content()
                except Exception:  # noqa: BLE001
                    continue
                if not html:
                    continue
                score, count, markers = self._score_html(html)
                if score <= 0:
                    continue
                if best is None or score > best[0]:
                    best = (score, html, getattr(frame, "url", "") or fallback_url,
                            getattr(frame, "name", "") or "", count, markers)
            # 特征词齐了、记录也解析出来了才算稳，否则再等等（表格常是 AJAX 后塞进来的）
            if best and best[4] > 0 and best[5] > 0:
                break
            time.sleep(0.6)

        if not best:
            return FetchResult(ok=False, url=fallback_url,
                               error="页面里没找到访问记录表（可能菜单没点到，或页面结构不同）")
        score, html, url, name, count, markers = best
        if not markers:
            # 宁可这一轮什么都不报，也不能拿一个不确定是什么的页面去解析。
            return FetchResult(
                ok=False, html=html, url=url, frame_name=name, record_count=0, verified=False,
                error="页面上找不到「最近访问记录 / 来访IP / 访问时间」之类的特征词，"
                      "无法确认这是记录页，本轮跳过（如果你们后台用词不同，"
                      "改 config.yaml 的 navigation.page_markers）",
            )
        return FetchResult(ok=True, html=html, url=url, frame_name=name, record_count=count,
                           verified=True,
                           error="" if count else "找到了记录页但当前没有访问记录")

    def _score_html(self, html: str) -> Tuple[float, int, int]:
        markers = self.cfg.navigation.page_markers or list(CONTENT_MARKERS)
        marker_hits = sum(1 for m in markers if m in html)
        records = parse_records(html)
        return marker_hits * 2.0 + len(records) * 1.0, len(records), marker_hits

    # ------------------------------------------------------------------ #
    # XHR 嗅探（为以后走 JSON 接口做准备）
    # ------------------------------------------------------------------ #
    def _start_sniffing(self) -> None:
        if self._sniffing:
            return
        self._xhr = []
        self._sniffing = True

        def on_response(response):
            try:
                ct = (response.headers or {}).get("content-type", "")
                if "json" in ct.lower() or response.url.lower().endswith(".json"):
                    self._xhr.append({"url": response.url, "status": str(response.status),
                                      "content_type": ct})
            except Exception:  # noqa: BLE001
                pass

        try:
            self.page.on("response", on_response)
            self._on_response = on_response
        except Exception:  # noqa: BLE001
            self._sniffing = False

    def _stop_sniffing(self) -> List[str]:
        if not self._sniffing:
            return []
        try:
            self.page.remove_listener("response", self._on_response)
        except Exception:  # noqa: BLE001
            pass
        self._sniffing = False
        urls = [x["url"] for x in self._xhr]
        if self._xhr:
            try:
                out = self.cfg.dump_path / "xhr-endpoints.json"
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(json.dumps(self._xhr, ensure_ascii=False, indent=2), encoding="utf-8")
            except Exception:  # noqa: BLE001
                pass
        return urls

    # ------------------------------------------------------------------ #
    # 调试用：把当前所有 frame 的 HTML 和截图存下来
    # ------------------------------------------------------------------ #
    def dump(self, tag: str = "discover") -> Path:
        out = self.cfg.dump_path / f"{tag}-{datetime.now():%Y%m%d-%H%M%S}"
        out.mkdir(parents=True, exist_ok=True)
        try:
            self.page.screenshot(path=str(out / "screenshot.png"), full_page=True)
        except Exception as exc:  # noqa: BLE001
            log.debug("截图失败：%s", exc)
        index: List[Dict[str, object]] = []
        for i, frame in enumerate(self._all_frames()):
            try:
                html = frame.content()
            except Exception:  # noqa: BLE001
                continue
            name = re.sub(r"[^0-9A-Za-z_.-]", "_", (getattr(frame, "name", "") or f"frame{i}"))[:40]
            fp = out / f"{i:02d}-{name}.html"
            fp.write_text(html, encoding="utf-8")
            score, count, markers = self._score_html(html)
            index.append({"file": fp.name, "url": getattr(frame, "url", ""),
                          "name": getattr(frame, "name", ""), "score": score,
                          "records": count, "markers": markers})
        (out / "frames.json").write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
        log.info("已导出 %d 个 frame 到 %s", len(index), out)
        return out
