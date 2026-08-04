#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gpt-image-2 图像生成 CLI —— 零第三方依赖（仅标准库）。

面向 OpenAI 兼容的 /v1/images/generations 与 /v1/images/edits 接口，
默认走环境中已配置好的 chedankj 中转网关。

配置解析顺序（前者优先，进程环境变量 > .env 文件）：
  API Key    GPT_IMAGE_API_KEY > CHEDANKJ_API_KEY > OPENAI_API_KEY
  Base URL   GPT_IMAGE_BASE_URL > CHEDANKJ_BASE_URL > OPENAI_BASE_URL
             > 默认 https://api.chedankj.com/v1
  Model      GPT_IMAGE_MODEL > 默认 gpt-image-2

.env 查找顺序：当前工作目录 → skill 目录 → skill 上溯的仓库根 → ~/.gpt-image-2/.env

用法：
  # 自检（不产生任何生成费用，只打印配置并探测连通性）
  python3 gpt_image2.py --check

  # 单张生成
  python3 gpt_image2.py "flat vector schematic ..." -o figures/fig1.png --size 1536x1024

  # 批量（manifest：{"items":[{"filename":"f1.png","prompt":"...","size":"1536x1024"}, ...]}）
  python3 gpt_image2.py --manifest prompts.json -o figures/

  # 参考图改画 / 局部重绘（走 /images/edits）
  python3 gpt_image2.py "redraw as a clean journal schematic" --image sketch.png -o figures/fig2.png

  # 只看将要发出的请求，不实际调用
  python3 gpt_image2.py "..." --dry-run

退出码：0 成功；2 配置缺失；3 网络/代理不可达；4 上游 API 报错；5 响应无法解析；6 部分失败（批量）。
"""

from __future__ import annotations

import argparse
import base64
import binascii
import json
import mimetypes
import os
import random
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

DEFAULT_BASE_URL = "https://api.chedankj.com/v1"
DEFAULT_MODEL = "gpt-image-2"

KEY_VARS = ("GPT_IMAGE_API_KEY", "CHEDANKJ_API_KEY", "OPENAI_API_KEY")
BASE_URL_VARS = ("GPT_IMAGE_BASE_URL", "CHEDANKJ_BASE_URL", "OPENAI_BASE_URL")

# gpt-image 系列接受的画幅。别名让调用方可以直接写宽高比。
SIZE_ALIASES = {
    "auto": "auto",
    "1:1": "1024x1024",
    "square": "1024x1024",
    "3:2": "1536x1024",
    "16:9": "1536x1024",
    "landscape": "1536x1024",
    "wide": "1536x1024",
    "2:3": "1024x1536",
    "9:16": "1024x1536",
    "portrait": "1024x1536",
}
KNOWN_SIZES = {"auto", "1024x1024", "1536x1024", "1024x1536"}

QUALITIES = ("auto", "low", "medium", "high")
FORMATS = ("png", "jpeg", "webp")
BACKGROUNDS = ("auto", "transparent", "opaque")


# --------------------------------------------------------------------------
# 配置
# --------------------------------------------------------------------------
def _candidate_env_files() -> list[Path]:
    here = Path(__file__).resolve()
    skill_dir = here.parent.parent  # skills/gpt-image-2/
    cands = [Path.cwd() / ".env", skill_dir / ".env"]
    for parent in skill_dir.parents:
        cands.append(parent / ".env")
        if (parent / ".git").exists():
            break
    cands.append(Path.home() / ".gpt-image-2" / ".env")
    seen, out = set(), []
    for c in cands:
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out


def load_env_file() -> tuple[dict, Path | None]:
    """读取第一个存在的 .env。只认我们关心的键，且不覆盖进程环境变量。"""
    wanted = set(KEY_VARS) | set(BASE_URL_VARS) | {"GPT_IMAGE_MODEL"}
    for path in _candidate_env_files():
        try:
            if not path.is_file():
                continue
            values = {}
            for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                if k not in wanted:
                    continue
                v = v.strip().strip('"').strip("'")
                if v:
                    values[k] = v
            if values:
                return values, path
        except OSError:
            continue
    return {}, None


def resolve_config(args) -> dict:
    file_env, env_path = load_env_file()

    def pick(names, cli=None, default=None):
        if cli:
            return cli, "--cli"
        for n in names:
            v = os.environ.get(n)
            if v:
                return v, n
        for n in names:
            v = file_env.get(n)
            if v:
                return v, f"{n} (.env)"
        return default, "default"

    key, key_src = pick(KEY_VARS)
    base_url, base_src = pick(BASE_URL_VARS, cli=getattr(args, "base_url", None),
                              default=DEFAULT_BASE_URL)
    model, model_src = pick(("GPT_IMAGE_MODEL",), cli=getattr(args, "model", None),
                            default=DEFAULT_MODEL)

    return {
        "api_key": key,
        "api_key_source": key_src,
        "base_url": (base_url or DEFAULT_BASE_URL).rstrip("/"),
        "base_url_source": base_src,
        "model": model,
        "model_source": model_src,
        "env_file": str(env_path) if env_path else None,
    }


def mask(secret: str | None) -> str:
    if not secret:
        return "<未设置>"
    if len(secret) <= 10:
        return secret[:2] + "***"
    return f"{secret[:6]}...{secret[-4:]} (len={len(secret)})"


# --------------------------------------------------------------------------
# HTTP
# --------------------------------------------------------------------------
def _opener():
    ctx = ssl.create_default_context()  # 尊重 SSL_CERT_FILE / REQUESTS_CA_BUNDLE 环境
    ca = os.environ.get("SSL_CERT_FILE") or os.environ.get("REQUESTS_CA_BUNDLE")
    if ca and Path(ca).is_file():
        try:
            ctx.load_verify_locations(ca)
        except OSError:
            pass
    handlers = [urllib.request.HTTPSHandler(context=ctx)]
    proxies = urllib.request.getproxies()  # 读取 HTTPS_PROXY / NO_PROXY
    if proxies:
        handlers.append(urllib.request.ProxyHandler(proxies))
    return urllib.request.build_opener(*handlers)


class ConfigError(RuntimeError):
    """参数或环境配置问题——退出码 2，不重试。"""


class ApiError(RuntimeError):
    def __init__(self, status: int, body: str, url: str):
        self.status, self.body, self.url = status, body, url
        super().__init__(f"HTTP {status} from {url}: {body[:600]}")


class NetworkError(RuntimeError):
    pass


def _request(url: str, data: bytes, headers: dict, timeout: int) -> dict:
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with _opener().open(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        body = ""
        try:
            body = exc.read().decode("utf-8", errors="replace")
        except Exception:  # noqa: BLE001 - 读不到 body 不应掩盖原始状态码
            pass
        raise ApiError(exc.code, body, url) from exc
    except urllib.error.URLError as exc:
        raise NetworkError(f"无法连接 {url}：{exc.reason}") from exc
    except TimeoutError as exc:
        raise NetworkError(f"连接 {url} 超时（{timeout}s）") from exc

    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ApiError(200, f"响应不是合法 JSON：{raw[:600]}", url) from exc


def _retryable(exc: Exception) -> bool:
    if isinstance(exc, NetworkError):
        return True
    if isinstance(exc, ApiError):
        return exc.status in (408, 409, 425, 429, 500, 502, 503, 504)
    return False


def post_json(url: str, payload: dict, cfg: dict, timeout: int, retries: int) -> dict:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {cfg['api_key']}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    return _with_retries(lambda: _request(url, body, headers, timeout), retries)


def post_multipart(url: str, fields: dict, files: list[tuple[str, Path]],
                   cfg: dict, timeout: int, retries: int) -> dict:
    boundary = f"----gptimage2{uuid.uuid4().hex}"
    buf = bytearray()

    def wr(text: str):
        buf.extend(text.encode("utf-8"))

    for name, value in fields.items():
        if value is None:
            continue
        wr(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"\r\n\r\n{value}\r\n")
    for name, path in files:
        ctype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        wr(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"; "
           f"filename=\"{path.name}\"\r\nContent-Type: {ctype}\r\n\r\n")
        buf.extend(path.read_bytes())
        wr("\r\n")
    wr(f"--{boundary}--\r\n")

    headers = {
        "Authorization": f"Bearer {cfg['api_key']}",
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Accept": "application/json",
    }
    return _with_retries(lambda: _request(url, bytes(buf), headers, timeout), retries)


def _with_retries(call, retries: int):
    last = None
    for attempt in range(retries + 1):
        try:
            return call()
        except Exception as exc:  # noqa: BLE001 - 由 _retryable 决定是否吞掉
            last = exc
            if attempt >= retries or not _retryable(exc):
                raise
            delay = min(2 ** attempt, 16) + random.uniform(0, 0.75)
            print(f"  ! 第 {attempt + 1} 次失败（{type(exc).__name__}），{delay:.1f}s 后重试",
                  file=sys.stderr)
            time.sleep(delay)
    raise last  # pragma: no cover - 循环必然 return 或 raise


# --------------------------------------------------------------------------
# 生成
# --------------------------------------------------------------------------
def normalize_size(value: str) -> str:
    v = (value or "auto").strip().lower()
    v = SIZE_ALIASES.get(v, v)
    if v not in KNOWN_SIZES:
        raise ConfigError(
            f"--size 不支持 {value!r}。可用：{', '.join(sorted(KNOWN_SIZES))}，"
            f"或别名 {', '.join(sorted(SIZE_ALIASES))}"
        )
    return v


def extract_images(resp: dict) -> list[bytes]:
    """兼容 b64_json / url 两种返回形态，以及部分网关的 output 包裹。"""
    items = resp.get("data")
    if not items and isinstance(resp.get("output"), list):
        items = resp["output"]
    if not isinstance(items, list) or not items:
        raise ApiError(200, f"响应缺少 data 数组：{json.dumps(resp, ensure_ascii=False)[:600]}", "")

    out = []
    for item in items:
        if not isinstance(item, dict):
            continue
        b64 = item.get("b64_json") or item.get("image_base64") or item.get("b64")
        if b64:
            try:
                out.append(base64.b64decode(b64))
            except (binascii.Error, ValueError) as exc:
                raise ApiError(200, f"b64_json 解码失败：{exc}", "") from exc
            continue
        url = item.get("url")
        if url:
            try:
                with _opener().open(url, timeout=120) as resp_img:
                    out.append(resp_img.read())
            except (urllib.error.URLError, TimeoutError) as exc:
                raise NetworkError(f"下载生成结果失败 {url}：{exc}") from exc
    if not out:
        raise ApiError(200, f"响应里既无 b64_json 也无 url：{json.dumps(resp, ensure_ascii=False)[:600]}", "")
    return out


def generate(prompt: str, cfg: dict, args, ref_images: list[Path]) -> list[bytes]:
    size = normalize_size(args.size)

    if ref_images:
        url = f"{cfg['base_url']}/images/edits"
        fields = {
            "model": cfg["model"],
            "prompt": prompt,
            "n": str(args.n),
            "size": size,
        }
        if args.quality != "auto":
            fields["quality"] = args.quality
        if args.background != "auto":
            fields["background"] = args.background
        files = [("image[]", p) for p in ref_images] if len(ref_images) > 1 else \
                [("image", ref_images[0])]
        if args.dry_run:
            print(json.dumps({"endpoint": url, "multipart_fields": fields,
                              "files": [str(p) for p in ref_images]},
                             ensure_ascii=False, indent=2))
            return []
        resp = post_multipart(url, fields, files, cfg, args.timeout, args.retries)
    else:
        url = f"{cfg['base_url']}/images/generations"
        payload = {"model": cfg["model"], "prompt": prompt, "n": args.n, "size": size}
        if args.quality != "auto":
            payload["quality"] = args.quality
        if args.background != "auto":
            payload["background"] = args.background
        if args.format != "png":
            payload["output_format"] = args.format
        if args.dry_run:
            print(json.dumps({"endpoint": url, "payload": payload}, ensure_ascii=False, indent=2))
            return []
        resp = post_json(url, payload, cfg, args.timeout, args.retries)

    return extract_images(resp)


def save(images: list[bytes], out: Path, fmt: str) -> list[Path]:
    written = []
    if out.suffix:  # 明确的文件名
        out.parent.mkdir(parents=True, exist_ok=True)
        for i, blob in enumerate(images):
            target = out if i == 0 else out.with_name(f"{out.stem}_{i + 1}{out.suffix}")
            target.write_bytes(blob)
            written.append(target)
    else:  # 目录
        out.mkdir(parents=True, exist_ok=True)
        stamp = uuid.uuid4().hex[:8]
        for i, blob in enumerate(images):
            target = out / f"gpt-image-2_{stamp}_{i + 1}.{fmt}"
            target.write_bytes(blob)
            written.append(target)
    return written


# --------------------------------------------------------------------------
# 子命令
# --------------------------------------------------------------------------
def cmd_check(cfg: dict, args) -> int:
    print("=== gpt-image-2 配置自检 ===")
    print(f"  Base URL : {cfg['base_url']}   ← {cfg['base_url_source']}")
    print(f"  Model    : {cfg['model']}   ← {cfg['model_source']}")
    print(f"  API Key  : {mask(cfg['api_key'])}   ← {cfg['api_key_source']}")
    print(f"  .env     : {cfg['env_file'] or '<未找到，纯环境变量>'}")
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    print(f"  代理     : {proxy or '<直连>'}")

    if not cfg["api_key"]:
        print(f"\n[配置缺失] 未找到 API Key。请设置 {' 或 '.join(KEY_VARS)} 之一。")
        return 2

    host = urllib.parse.urlparse(cfg["base_url"]).netloc
    print(f"\n正在探测 {host} 连通性 …")
    try:
        # 用 /models 探活：多数 OpenAI 兼容网关都实现了它，且不产生生成费用。
        req = urllib.request.Request(
            f"{cfg['base_url']}/models",
            headers={"Authorization": f"Bearer {cfg['api_key']}"},
        )
        with _opener().open(req, timeout=args.timeout) as resp:
            body = resp.read(4000).decode("utf-8", errors="replace")
        print(f"  ✓ 可达（HTTP {resp.status}）")
        if cfg["model"] in body:
            print(f"  ✓ 模型列表中出现 {cfg['model']}")
        else:
            print(f"  ! 模型列表里没直接看到 {cfg['model']}；网关可能不返回全量列表，"
                  f"不代表不可用。可用一次真实生成确认。")
        return 0
    except urllib.error.HTTPError as exc:
        print(f"  ! /models 返回 HTTP {exc.code}（部分网关不开放该端点，属正常）")
        if exc.code in (401, 403):
            print("    401/403 通常意味着 Key 无效或无权限，请核对。")
            return 4
        return 0
    except urllib.error.URLError as exc:
        print(f"  ✗ 不可达：{exc.reason}")
        print(f"\n[网络] 若报 'CONNECT tunnel failed, response 403'，说明当前环境的出网策略"
              f"未放行 {host}。这是环境侧的白名单问题，不能绕过：请在 Claude Code 环境设置里"
              f"把该域名加入允许列表，或改用已放行的网关。")
        return 3


def cmd_manifest(cfg: dict, args) -> int:
    manifest_path = Path(args.manifest)
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[配置错误] 无法读取 manifest {manifest_path}：{exc}", file=sys.stderr)
        return 2

    items = manifest.get("items") if isinstance(manifest, dict) else manifest
    if not isinstance(items, list) or not items:
        print(f"[配置错误] manifest 里没有 items 数组：{manifest_path}", file=sys.stderr)
        return 2

    out_dir = Path(args.out or ".")
    failures = 0
    for idx, item in enumerate(items, 1):
        prompt = (item or {}).get("prompt")
        if not prompt:
            print(f"[{idx}/{len(items)}] 跳过：缺 prompt", file=sys.stderr)
            failures += 1
            continue
        filename = item.get("filename") or f"image_{idx:02d}.{args.format}"
        item_args = argparse.Namespace(**vars(args))
        item_args.size = item.get("size", args.size)
        item_args.quality = item.get("quality", args.quality)
        item_args.background = item.get("background", args.background)
        item_args.n = int(item.get("n", args.n))

        print(f"[{idx}/{len(items)}] {filename} …")
        try:
            refs = [Path(p) for p in item.get("images", [])]
            missing = [p for p in refs if not p.is_file()]
            if missing:
                raise FileNotFoundError(f"参考图不存在：{', '.join(map(str, missing))}")
            images = generate(prompt, cfg, item_args, refs)
            if images:
                written = save(images, out_dir / filename, args.format)
                for w in written:
                    print(f"      ✓ {w}")
        except (ApiError, NetworkError, FileNotFoundError, ConfigError) as exc:
            print(f"      ✗ 失败：{exc}", file=sys.stderr)
            failures += 1

    if failures:
        print(f"\n完成，但有 {failures}/{len(items)} 项失败。", file=sys.stderr)
        return 6
    print(f"\n全部 {len(items)} 项完成。")
    return 0


def cmd_single(cfg: dict, args) -> int:
    refs = [Path(p) for p in (args.image or [])]
    missing = [p for p in refs if not p.is_file()]
    if missing:
        print(f"[配置错误] 参考图不存在：{', '.join(map(str, missing))}", file=sys.stderr)
        return 2

    images = generate(args.prompt, cfg, args, refs)
    if not images:  # dry-run
        return 0
    for path in save(images, Path(args.out), args.format):
        print(f"✓ {path}")
    return 0


# --------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="gpt_image2.py",
        description="gpt-image-2 图像生成（OpenAI 兼容接口，默认走 chedankj 中转）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("prompt", nargs="?", help="英文提示词（推荐英文，图内文字更稳）")
    p.add_argument("-o", "--out", default="images/", help="输出文件或目录，默认 images/")
    p.add_argument("--size", default="1536x1024",
                   help="1024x1024 / 1536x1024 / 1024x1536 / auto，或别名 16:9、3:2、9:16、1:1")
    p.add_argument("--quality", default="high", choices=QUALITIES, help="默认 high")
    p.add_argument("--format", default="png", choices=FORMATS, help="输出格式，默认 png")
    p.add_argument("--background", default="auto", choices=BACKGROUNDS,
                   help="transparent 需要 png/webp")
    p.add_argument("-n", type=int, default=1, help="一次生成几张，默认 1")
    p.add_argument("--image", action="append",
                   help="参考图路径，可重复；给了就走 /images/edits 改画")
    p.add_argument("--manifest", help="批量生成的 JSON 清单")
    p.add_argument("--model", help="覆盖模型名，默认 gpt-image-2")
    p.add_argument("--base-url", help="覆盖 Base URL")
    p.add_argument("--timeout", type=int, default=180, help="单次请求超时秒数，默认 180")
    p.add_argument("--retries", type=int, default=2, help="可重试错误的重试次数，默认 2")
    p.add_argument("--check", action="store_true", help="只做配置与连通性自检")
    p.add_argument("--dry-run", action="store_true", help="只打印将要发出的请求")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    cfg = resolve_config(args)

    if args.check:
        return cmd_check(cfg, args)

    if not cfg["api_key"]:
        print(f"[配置缺失] 未找到 API Key。请设置 {' 或 '.join(KEY_VARS)} 之一，"
              f"然后 `python3 gpt_image2.py --check` 复查。", file=sys.stderr)
        return 2

    if not args.manifest and not args.prompt:
        print("[用法错误] 需要一个 prompt，或用 --manifest 走批量。", file=sys.stderr)
        return 2

    try:
        if args.manifest:
            return cmd_manifest(cfg, args)
        return cmd_single(cfg, args)
    except ConfigError as exc:
        print(f"[配置错误] {exc}", file=sys.stderr)
        return 2
    except ApiError as exc:
        print(f"\n[上游 API 错误] {exc}", file=sys.stderr)
        if exc.status in (401, 403):
            print("  → Key 无效/无权限，或该 Key 未开通 gpt-image-2。核对 CHEDANKJ_API_KEY。",
                  file=sys.stderr)
        elif exc.status == 404:
            print(f"  → 端点或模型不存在。核对 Base URL（当前 {cfg['base_url']}）"
                  f"与模型名（当前 {cfg['model']}）。", file=sys.stderr)
        elif exc.status == 429:
            print("  → 触发限流或余额不足。", file=sys.stderr)
        return 4
    except NetworkError as exc:
        print(f"\n[网络错误] {exc}", file=sys.stderr)
        print("  → 若是 'CONNECT tunnel failed, response 403'，是环境出网白名单没放行该域名，"
              "不要绕过，去环境设置里加白名单。", file=sys.stderr)
        return 3
    except KeyboardInterrupt:
        print("\n已中断。", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
