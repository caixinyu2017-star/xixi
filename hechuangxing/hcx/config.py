# -*- coding: utf-8 -*-
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS_DIR = ROOT / "corpus"
WEB_DIR = ROOT / "web"
OUTPUT_DIR = ROOT / "outputs"
UPLOAD_DIR = ROOT / "uploads"
SAMPLE_DIR = ROOT / "samples"

for d in (OUTPUT_DIR, UPLOAD_DIR):
    d.mkdir(parents=True, exist_ok=True)


def _load_dotenv():
    """极简 .env 读取，避免额外依赖。"""
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key, val = key.strip(), val.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val


_load_dotenv()

def _usable_key(raw: str) -> str:
    """判断 Key 是不是真的填了。

    很多人会把配置模板里的占位符原样留着（比如 sk-ant-在这里填你的key），
    这种情况下如果当成真 Key 去调接口，演示时第一句话就会报鉴权错误。
    所以这里做一次形状检查，不像真 Key 的一律当成没填，直接走离线演示模式。
    """
    key = (raw or "").strip().strip('"').strip("'")
    if not key:
        return ""
    if not key.isascii():                      # 含中文占位符
        return ""
    if len(key) < 20:                          # 太短，不可能是真 Key
        return ""
    lowered = key.lower()
    for placeholder in ("your", "xxx", "here", "填", "示例", "example", "changeme"):
        if placeholder in lowered:
            return ""
    return key


ANTHROPIC_API_KEY = _usable_key(os.environ.get("ANTHROPIC_API_KEY", ""))
ANTHROPIC_BASE_URL = os.environ.get("ANTHROPIC_BASE_URL", "").strip()
MODEL = os.environ.get("HCX_MODEL", "claude-sonnet-4-5-20250929").strip()
MAX_TOKENS = int(os.environ.get("HCX_MAX_TOKENS", "8000"))
HOST = os.environ.get("HCX_HOST", "127.0.0.1")
PORT = int(os.environ.get("HCX_PORT", "8848"))

# 没有配置 API Key 时自动进入演示模式：用内置的嘉兴案例脚本作答，
# 保证录屏演示在任何网络环境下都能跑通。
DEMO_MODE = os.environ.get("HCX_DEMO", "").strip() == "1" or not ANTHROPIC_API_KEY
