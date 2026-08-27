"""浏览器会话：WebVPN + 统一身份认证（CAS）登录，并保持登录态。

为什么用 Playwright 而不是 requests：
  * CAS 登录有图形验证码，需要真实渲染；
  * CAS 表单里的 execution / _eventId / lt 是一次性隐藏字段，交给浏览器自动带上最省事；
  * 博达后台是多层 iframe 的 JSP 页面，靠浏览器解析最可靠；
  * WebVPN 会往页面里注入 JS 重写链接，非浏览器很难跟上。

登录态保存在 `state/browser/`（完整浏览器 profile）+ `state/storage_state.json`（cookie 备份），
第二次启动一般不用再输验证码。会话掉了会自动重新登录。
"""
from __future__ import annotations

import logging
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

from .config import AppConfig

log = logging.getLogger(__name__)

DEFAULT_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")

USERNAME_SELECTORS = [
    "input[name='username']", "#username", "input#un", "input[name='user']",
    "input[name='loginName']", "input[name='account']",
    "input[placeholder*='学号']", "input[placeholder*='工号']", "input[placeholder*='账号']",
    "input[placeholder*='用户名']",
]
PASSWORD_SELECTORS = [
    "input[name='password']", "#password", "input[type='password']",
    "input[name='pwd']", "input[placeholder*='密码']",
]
CAPTCHA_INPUT_SELECTORS = [
    "input[name='captcha']", "input[name='code']", "input[name='captchaResponse']",
    "input[name='authcode']", "input[name='verifyCode']", "input[name='checkcode']",
    "#captcha", "#code", "#captchaResponse", "#verifyCode",
    "input[placeholder*='验证码']",
]
CAPTCHA_IMAGE_SELECTORS = [
    "img#captchaImg", "img#captcha", "img#code", "img#imgCode", "img#verifyCodeImg",
    "img[src*='captcha']", "img[src*='Captcha']", "img[src*='code']", "img[src*='verify']",
    "img[alt*='验证码']", "img[title*='验证码']",
]
SUBMIT_SELECTORS = [
    "button[type='submit']", "input[type='submit']", "#login", "#loginBtn", ".login-btn",
    "button:has-text('登 录')", "button:has-text('登录')", "a:has-text('登录')",
    "input[value='登录']", "input[value='登 录']",
]

# 页面上出现这些文字 = 验证码错了（可以重试）
CAPTCHA_ERROR_HINTS = ("验证码", "captcha", "校验码", "图形码")
# 出现这些 = 账号密码错了（**绝不能**重试，会锁账号）
CREDENTIAL_ERROR_HINTS = (
    "用户名或密码", "密码错误", "账号或密码", "帐号或密码", "用户不存在", "认证失败",
    "invalid credentials", "账户已被锁定", "账号已锁定", "已被锁定", "密码不正确",
)


class LoginError(RuntimeError):
    """登录失败且不该自动重试（例如密码错误）。"""


@dataclass
class LoginOutcome:
    ok: bool
    attempts: int
    used_ocr: bool
    message: str = ""


# --------------------------------------------------------------------------- #
# 验证码识别
# --------------------------------------------------------------------------- #
class CaptchaSolver:
    """ddddocr 优先；识别不出来就让人工输入。"""

    def __init__(self, enabled: bool = True):
        self._ocr = None
        self._tried = False
        self.enabled = enabled

    @property
    def available(self) -> bool:
        return self._load() is not None

    def _load(self):
        if self._tried:
            return self._ocr
        self._tried = True
        if not self.enabled:
            return None
        try:
            import ddddocr  # type: ignore
            self._ocr = ddddocr.DdddOcr(show_ad=False)
            log.info("验证码自动识别已启用（ddddocr）")
        except Exception as exc:  # noqa: BLE001
            log.warning("ddddocr 不可用（%s），验证码将需要手工输入", exc)
            self._ocr = None
        return self._ocr

    def solve(self, image_bytes: bytes) -> Tuple[str, float]:
        """返回 (识别结果, 置信度 0~1)。

        ddddocr 支持 probability=True 拿到每个字符的概率；置信度低的时候我们宁可换一张，
        也不要拿去提交——有些 CAS 会把「验证码错」和「密码错」报成同一句话，
        提交一次错的验证码可能被算成一次密码错误，多试几次就把账号锁了。
        """
        ocr = self._load()
        if not ocr or not image_bytes:
            return "", 0.0
        text, confidence = "", 1.0
        try:
            result = ocr.classification(image_bytes, probability=True)
            if isinstance(result, dict):
                text = result.get("text") or ""
                if result.get("confidence") is not None:
                    confidence = float(result["confidence"])
                elif result.get("probabilities"):
                    per_char = [max(p) for p in result["probabilities"] if p]
                    confidence = min(per_char) if per_char else 1.0
            else:
                text = result or ""
        except TypeError:
            try:
                text = ocr.classification(image_bytes) or ""
            except Exception as exc:  # noqa: BLE001
                log.debug("验证码识别异常：%s", exc)
                return "", 0.0
        except Exception as exc:  # noqa: BLE001
            log.debug("验证码识别异常：%s", exc)
            return "", 0.0
        return re.sub(r"[^0-9A-Za-z]", "", text).strip(), confidence


def prompt_captcha(image_path: Optional[Path]) -> str:
    """人工兜底：把验证码图片存下来，让用户在终端里敲。"""
    if image_path:
        print(f"\n请打开验证码图片并输入：{image_path}", file=sys.stderr)
    else:
        print("\n请在打开的浏览器窗口中查看验证码", file=sys.stderr)
    try:
        return input("验证码（直接回车 = 换一张）：").strip()
    except (EOFError, KeyboardInterrupt):
        return ""


# --------------------------------------------------------------------------- #
# 浏览器会话
# --------------------------------------------------------------------------- #
class BrowserSession:
    def __init__(self, cfg: AppConfig, use_ocr: bool = True):
        self.cfg = cfg
        self._pw = None
        self._browser = None
        self.context = None
        self.page = None
        self.solver = CaptchaSolver(enabled=use_ocr)

    # ---------------- 生命周期 ----------------
    def __enter__(self) -> "BrowserSession":
        self.start()
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    def start(self) -> None:
        try:
            from playwright.sync_api import sync_playwright  # type: ignore
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError(
                "缺少 playwright。请执行：pip install -r requirements.txt && python -m playwright install chromium"
            ) from exc

        b = self.cfg.browser
        self._pw = sync_playwright().start()
        launch_kwargs = {
            "headless": b.headless,
            "slow_mo": b.slow_mo_ms or 0,
            "args": ["--disable-blink-features=AutomationControlled", "--no-sandbox"],
        }
        if b.channel:
            launch_kwargs["channel"] = b.channel

        # 用「持久化 profile」而不是普通 context：深信服 WebVPN 的票据有时不只在 cookie 里，
        # 整个 profile 存盘最稳，第二次启动基本不用重新登录。
        user_data_dir = self.cfg.path(b.user_data_dir)
        user_data_dir.mkdir(parents=True, exist_ok=True)
        context_kwargs = {
            "viewport": {"width": b.viewport_width, "height": b.viewport_height},
            "user_agent": b.user_agent or DEFAULT_UA,
            "ignore_https_errors": b.ignore_https_errors,
            "locale": "zh-CN",
            "timezone_id": "Asia/Shanghai",
        }
        try:
            self.context = self._pw.chromium.launch_persistent_context(
                str(user_data_dir), **launch_kwargs, **context_kwargs
            )
        except Exception as exc:  # noqa: BLE001
            log.warning("持久化 profile 启动失败（%s），改用普通模式 + storage_state", exc)
            self._browser = self._pw.chromium.launch(**launch_kwargs)
            state_file = self.cfg.path(b.storage_state)
            if state_file.exists():
                context_kwargs["storage_state"] = str(state_file)
            self.context = self._browser.new_context(**context_kwargs)

        self.context.set_default_timeout(b.timeout_ms)
        self.context.set_default_navigation_timeout(b.timeout_ms)
        self.page = self.context.pages[0] if self.context.pages else self.context.new_page()

    def close(self) -> None:
        self.save_state()
        for closer in (self.context, self._browser):
            try:
                if closer:
                    closer.close()
            except Exception:  # noqa: BLE001
                pass
        try:
            if self._pw:
                self._pw.stop()
        except Exception:  # noqa: BLE001
            pass

    def save_state(self) -> None:
        if not self.context:
            return
        try:
            path = self.cfg.path(self.cfg.browser.storage_state)
            path.parent.mkdir(parents=True, exist_ok=True)
            self.context.storage_state(path=str(path))
        except Exception as exc:  # noqa: BLE001
            log.debug("保存登录态失败：%s", exc)

    # ---------------- 登录判定 ----------------
    def looks_logged_out(self, page=None) -> bool:
        """两种信号任一命中就认为掉线：URL 回到登录页，或页面上出现密码框。"""
        page = page or self.page
        try:
            url = page.url or ""
        except Exception:  # noqa: BLE001
            return True
        lowered = url.lower()
        if any(m in lowered for m in ("cas_login=true", "/cas/login", "/authserver/login")):
            return True
        if lowered.rstrip("/").endswith("webvpn.zjxu.edu.cn/login") or "/login?" in lowered:
            return True
        try:
            if page.locator("input[type='password']").count() > 0:
                return True
            body = (page.inner_text("body", timeout=3000) or "")[:2000]
        except Exception:  # noqa: BLE001
            return False
        return any(m in body for m in self.cfg.webvpn.login_page_markers)

    # ---------------- 登录 ----------------
    def ensure_logged_in(self, target_url: str = "", force: bool = False) -> LoginOutcome:
        """确保处于登录态。已经登录就直接返回。"""
        target = target_url or self.cfg.webvpn.target_url
        if not force and target:
            try:
                self.page.goto(target, wait_until="domcontentloaded")
                self._settle()
                if not self.looks_logged_out():
                    log.info("已有登录态，直接使用")
                    return LoginOutcome(ok=True, attempts=0, used_ocr=False, message="复用已有会话")
            except Exception as exc:  # noqa: BLE001
                log.debug("直接访问目标页失败（%s），走完整登录流程", exc)

        outcome = self.login()
        if outcome.ok and target:
            self.page.goto(target, wait_until="domcontentloaded")
            self._settle()
            if self.looks_logged_out():
                outcome.ok = False
                outcome.message = "登录后仍被弹回登录页，可能是账号在别处登录、或目标地址不对"
        if outcome.ok:
            self.save_state()
        return outcome

    def login(self) -> LoginOutcome:
        """完整登录流程。

        **账号安全是第一位的**：有些 CAS 对「密码错」和「验证码错」返回同一句话，
        分不清的时候只能保守处理。所以这里把两种预算分开：

          * `max_login_attempts`（默认 3）—— 真正**提交表单**的次数上限。
            提交一次就可能被服务器计一次失败登录，超过就停，绝不硬刚。
          * `max_captcha_attempts`（默认 6）—— **不提交**、只换验证码重识别的次数。
            这个动作不消耗登录次数，所以可以多试，直到 OCR 有把握了再提交。
        """
        cfg = self.cfg.webvpn
        if not cfg.login_url:
            raise LoginError("没有配置 webvpn.login_url")
        if not cfg.username or not cfg.password:
            raise LoginError("没有配置账号或密码（请写在 .env 里：WEBVPN_USERNAME / WEBVPN_PASSWORD）")

        used_ocr = False
        last_message = ""
        for submit_no in range(1, max(1, cfg.max_login_attempts) + 1):
            log.info("正在登录（第 %d/%d 次提交）…", submit_no, cfg.max_login_attempts)
            # execution / lt 这类隐藏字段是一次性的，每次提交前都要重新打开登录页
            self.page.goto(cfg.login_url, wait_until="domcontentloaded")
            self._settle()

            if not self.looks_logged_out():
                log.info("打开登录页时发现已经是登录态")
                return LoginOutcome(ok=True, attempts=submit_no - 1, used_ocr=used_ocr)

            self._fill_first(USERNAME_SELECTORS, cfg.username, cfg.username_selector, "账号")
            self._fill_first(PASSWORD_SELECTORS, cfg.password, cfg.password_selector, "密码")

            captcha_input = self._first_visible(CAPTCHA_INPUT_SELECTORS, cfg.captcha_input_selector)
            if captcha_input is not None:
                code, from_ocr = self._acquire_captcha()
                used_ocr = used_ocr or from_ocr
                if not code:
                    return LoginOutcome(
                        ok=False, attempts=submit_no - 1, used_ocr=used_ocr,
                        message="没能拿到验证码。把 config.yaml 里 browser.headless 设成 false，"
                                "或装上 ddddocr（pip install \"ddddocr>=1.6.1\"）再试。",
                    )
                captcha_input.fill(code)
                log.info("验证码填入 %s（%s）", code, "自动识别" if from_ocr else "人工输入")

            if not self._submit():
                raise LoginError("找不到登录按钮，请在 config.yaml 里配置 webvpn.submit_selector")
            self._settle(extra_wait=1.2)

            if not self.looks_logged_out():
                log.info("登录成功")
                self.save_state()
                return LoginOutcome(ok=True, attempts=submit_no, used_ocr=used_ocr)

            reason, text = self._classify_failure()
            last_message = text
            self._dump_debug(f"login-fail-{submit_no}")
            if reason == "credential":
                # 明确是账号密码问题：立刻停，绝不重试，避免账号被锁
                raise LoginError(f"账号或密码不正确，已立即停止重试以免账号被锁定。页面提示：{text[:120]}")
            log.warning("第 %d 次提交未通过（判定为%s）：%s",
                        submit_no, {"captcha": "验证码错误"}.get(reason, "原因不明"), text[:100])

        return LoginOutcome(
            ok=False, attempts=cfg.max_login_attempts, used_ocr=used_ocr,
            message=(f"连续 {cfg.max_login_attempts} 次登录未通过，已停止（继续试可能触发账号锁定）。"
                     f"页面最后的提示：{last_message[:100] or '无'}。"
                     "建议先手工登录一次确认账号密码没问题，再把 browser.headless 设为 false 观察。"),
        )

    def _acquire_captcha(self) -> Tuple[str, bool]:
        """在**不提交表单**的前提下，反复换验证码直到 OCR 有把握。

        返回 (验证码, 是否来自 OCR)。拿不到就返回 ("", False) 交给上层处理。
        """
        cfg = self.cfg.webvpn
        best_code, best_conf = "", 0.0
        rounds = max(1, cfg.max_captcha_attempts)
        for i in range(1, rounds + 1):
            image_bytes, image_path = self._capture_captcha_image()
            if not image_bytes:
                break
            code, confidence = self.solver.solve(image_bytes)
            if code and 3 <= len(code) <= 8:
                if confidence >= cfg.captcha_min_confidence:
                    return code, True
                if confidence > best_conf:
                    best_code, best_conf = code, confidence
                log.debug("验证码「%s」置信度 %.2f 偏低，换一张（第 %d/%d 次）",
                          code, confidence, i, rounds)
            if i < rounds:
                self._refresh_captcha()

        # OCR 一直没把握：优先请人工，其次拿最有把握的那次去赌一把
        if cfg.manual_captcha_fallback and sys.stdin and sys.stdin.isatty():
            _, image_path = self._capture_captcha_image()
            manual = prompt_captcha(image_path)
            if manual:
                return manual, False
        if best_code:
            log.warning("验证码识别始终不太确定，用置信度最高的一次（%s，%.2f）试一下", best_code, best_conf)
            return best_code, True
        return "", False

    def _capture_captcha_image(self) -> Tuple[bytes, Optional[Path]]:
        """对页面上的 <img> 元素截图。

        绝对**不能**重新 GET 图片地址 —— 服务端会因此换成新的一张，
        我们填的就永远是上一张的答案了。
        """
        img = self._first_visible(CAPTCHA_IMAGE_SELECTORS, self.cfg.webvpn.captcha_image_selector)
        if img is None:
            return b"", None
        try:
            image_bytes = img.screenshot()
        except Exception as exc:  # noqa: BLE001
            log.debug("验证码截图失败：%s", exc)
            return b"", None
        path: Optional[Path] = None
        try:
            path = self.cfg.dump_path / "captcha.png"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(image_bytes)
        except Exception:  # noqa: BLE001
            path = None
        return image_bytes, path

    def _refresh_captcha(self) -> None:
        """点一下验证码图片换新的（绝大多数 CAS 都绑了 onclick 刷新）。"""
        img = self._first_visible(CAPTCHA_IMAGE_SELECTORS, self.cfg.webvpn.captcha_image_selector)
        if img is None:
            return
        try:
            img.click()
            time.sleep(0.7)
        except Exception:  # noqa: BLE001
            pass

    # ---------------- 内部工具 ----------------
    def _classify_failure(self) -> Tuple[str, str]:
        """看页面提示判断失败原因：credential（停手）/ captcha（可重试）/ unknown。"""
        chunks: List[str] = []
        for frame in self._frames():
            try:
                chunks.append(frame.inner_text("body", timeout=2000) or "")
            except Exception:  # noqa: BLE001
                continue
        text = "\n".join(chunks)
        if not text:
            return "unknown", ""
        flat = text.replace(" ", "")
        for hint in CREDENTIAL_ERROR_HINTS:
            if hint.replace(" ", "") in flat:
                return "credential", text.strip()[:200]
        for hint in CAPTCHA_ERROR_HINTS:
            if hint in flat and ("错误" in flat or "不正确" in flat or "失效" in flat or "过期" in flat):
                return "captcha", text.strip()[:200]
        return "unknown", text.strip()[:200]

    def _fill_first(self, selectors: List[str], value: str, override: str, label: str):
        """填第一个能找到的输入框（同样会钻进 iframe）。"""
        loc = self._first_visible(selectors, override)
        if loc is None:
            raise LoginError(f"登录页上找不到{label}输入框，请在 config.yaml 里手工指定选择器")
        loc.fill("")
        loc.fill(value)
        return loc

    def _first_visible(self, selectors: List[str], override: str = ""):
        """按优先级找第一个可见元素，**并且会钻进 iframe 里找**。

        WebVPN + 博达后台经常把登录框和验证码放在子 frame 里，
        只在主文档上 locator 会什么都找不到。
        """
        candidates = ([override] if override else []) + selectors
        for sel in candidates:
            for frame in self._frames():
                try:
                    loc = frame.locator(sel).first
                    if loc.count() > 0 and loc.is_visible():
                        return loc
                except Exception:  # noqa: BLE001
                    continue
        return None

    def _frames(self) -> List:
        """主文档优先，然后是各级 iframe。"""
        try:
            frames = list(self.page.frames)
        except Exception:  # noqa: BLE001
            return [self.page]
        main = getattr(self.page, "main_frame", None)
        if main is not None and main in frames:
            frames.remove(main)
            frames.insert(0, main)
        return frames

    def _submit(self) -> bool:
        loc = self._first_visible(SUBMIT_SELECTORS, self.cfg.webvpn.submit_selector)
        if loc is not None:
            try:
                loc.click()
                return True
            except Exception as exc:  # noqa: BLE001
                log.debug("点击登录按钮失败：%s", exc)
        # 兜底：在密码框里回车
        pwd = self._first_visible(PASSWORD_SELECTORS, self.cfg.webvpn.password_selector)
        if pwd is not None:
            try:
                pwd.press("Enter")
                return True
            except Exception:  # noqa: BLE001
                pass
        return False

    def _settle(self, extra_wait: float = 0.0) -> None:
        try:
            self.page.wait_for_load_state("networkidle", timeout=8000)
        except Exception:  # noqa: BLE001
            pass
        if extra_wait:
            time.sleep(extra_wait)

    def _dump_debug(self, tag: str) -> None:
        try:
            out = self.cfg.dump_path
            out.mkdir(parents=True, exist_ok=True)
            stamp = time.strftime("%Y%m%d-%H%M%S")
            self.page.screenshot(path=str(out / f"{tag}-{stamp}.png"), full_page=True)
            (out / f"{tag}-{stamp}.html").write_text(self.page.content(), encoding="utf-8")
            log.info("调试快照已保存到 %s", out)
        except Exception as exc:  # noqa: BLE001
            log.debug("保存调试快照失败：%s", exc)
