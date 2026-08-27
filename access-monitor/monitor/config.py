"""配置加载。

优先级：命令行 > 环境变量 / .env > config.yaml > 内置默认值。

设计原则：**账号密码永远不进 YAML 也不进 git**，只放 `.env`（已在 .gitignore 里）。
YAML 里可以写 `${WEBVPN_PASSWORD}` 这样的占位符，加载时会用环境变量替换。
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

_ENV_PATTERN = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)(?::-([^}]*))?\}")


# --------------------------------------------------------------------------- #
# .env
# --------------------------------------------------------------------------- #
def load_dotenv(path: Path) -> Dict[str, str]:
    """极简 .env 解析器（不额外引入 python-dotenv）。

    支持 `KEY=value`、`export KEY=value`、`#` 注释、单/双引号包裹。
    已存在的环境变量不会被覆盖，方便临时用 `WEBVPN_PASSWORD=xxx python run.py` 覆盖。
    """
    loaded: Dict[str, str] = {}
    if not path.exists():
        return loaded
    for raw_line in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):].strip()
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        loaded[key] = value
        os.environ.setdefault(key, value)
    return loaded


def _expand(value: Any) -> Any:
    """递归展开 ${ENV} / ${ENV:-默认值}。"""
    if isinstance(value, str):
        def repl(m: "re.Match[str]") -> str:
            return os.environ.get(m.group(1), m.group(2) if m.group(2) is not None else "")
        return _ENV_PATTERN.sub(repl, value)
    if isinstance(value, dict):
        return {k: _expand(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_expand(v) for v in value]
    return value


# --------------------------------------------------------------------------- #
# 各段配置
# --------------------------------------------------------------------------- #
@dataclass
class WebvpnConfig:
    login_url: str = ""
    target_url: str = ""
    username: str = ""
    password: str = ""
    # 登录页上的选择器，留空则用内置的一组启发式规则自动找
    username_selector: str = ""
    password_selector: str = ""
    captcha_input_selector: str = ""
    captcha_image_selector: str = ""
    submit_selector: str = ""
    # 判断「已经被踢回登录页」的关键词
    login_page_markers: List[str] = field(
        default_factory=lambda: ["统一身份认证", "用户登录", "cas/login", "请输入验证码", "账号登录"]
    )
    # 提交表单的次数上限。服务器可能把「验证码错」也算成一次失败登录，所以必须保守。
    max_login_attempts: int = 3
    # 不提交、只换验证码重新识别的次数上限。这个动作不消耗登录次数，可以多试。
    max_captcha_attempts: int = 6
    # OCR 置信度低于这个值就换一张，别拿去赌那 3 次提交机会
    captcha_min_confidence: float = 0.6
    manual_captcha_fallback: bool = True


@dataclass
class BrowserConfig:
    headless: bool = False
    channel: str = ""                    # "" / chrome / msedge
    slow_mo_ms: int = 0
    timeout_ms: int = 45000
    user_data_dir: str = "state/browser"
    storage_state: str = "state/storage_state.json"
    viewport_width: int = 1600
    viewport_height: int = 950
    user_agent: str = ""
    ignore_https_errors: bool = True     # 校内自签证书常见


@dataclass
class NavigationConfig:
    # 从后台首页点到「最近访问记录」的菜单文字路径
    menu_path: List[str] = field(default_factory=lambda: ["运营中心", "访问统计", "最近访问记录"])
    # 自动发现到的记录页 URL（第一次跑完会自动写回 state/records_url.txt）
    records_url: str = ""
    # 页面上用来确认「我确实在最近访问记录页」的关键词
    page_markers: List[str] = field(default_factory=lambda: ["最近访问记录", "来访IP", "访问时间"])
    # 表格识别：表头里出现下面任意一个词，就认为这是记录表
    table_header_hints: List[str] = field(
        default_factory=lambda: ["IP", "ip", "访问时间", "时间", "来访", "访问页面", "页面"]
    )
    reload_strategy: str = "auto"        # auto / url / menu


@dataclass
class PollConfig:
    interval_seconds: int = 30
    jitter_seconds: int = 5
    max_rows: int = 300
    max_consecutive_errors: int = 5
    relogin_backoff_seconds: int = 60


@dataclass
class RulesConfig:
    # 规则一：任意 window_seconds 内新增记录数 >= threshold（用户要的「短时间内 3 条以上」）
    burst_enabled: bool = True
    burst_threshold: int = 3
    burst_window_seconds: int = 60
    # 规则二：同一个 IP 在 window 内访问 >= threshold 次
    ip_burst_enabled: bool = True
    ip_burst_threshold: int = 3
    ip_burst_window_seconds: int = 300
    # 规则三：出现从未见过的 IP（默认关，太吵）
    new_ip_enabled: bool = False
    # 过滤
    ignore_ips: List[str] = field(default_factory=list)          # 支持单个 IP 或 CIDR
    ignore_bots: bool = False                                     # 忽略搜索引擎爬虫
    ignore_private: bool = False                                  # 忽略内网地址
    only_ips: List[str] = field(default_factory=list)             # 只关心这些 IP/网段
    # 冷却：同一条规则多久之内不重复告警
    cooldown_seconds: int = 300
    # 首次启动时把已有记录当成「基线」，不告警（避免一启动就轰炸）
    baseline_on_first_run: bool = True


@dataclass
class IpIntelConfig:
    enabled: bool = True
    # 离线库一：GeoCN.mmdb —— 国内 IP 能到「区/县」，还带运营商和网络类型，强烈建议装
    geocn_mmdb: str = ""
    divisions_json: str = ""             # 可选：行政区划码 -> 名称对照表
    # 离线库二：ip2region 的 .xdb —— 全球覆盖，国内到市级
    ip2region_xdb: str = ""
    # 在线 API
    use_ip_api: bool = True              # ip-api.com：免费、中文、带 ASN/代理/机房判定
    ip_api_lang: str = "zh-CN"
    use_qqmap: bool = False              # 腾讯位置服务：国内基本能到区/县，需要 key
    qqmap_key: str = ""
    use_rdns: bool = True                # 反向 DNS，用来认爬虫
    use_rdap: bool = True                # RDAP 查 ASN / 网段归属
    timeout_seconds: int = 6
    rdns_timeout_seconds: float = 3.0    # 单个反向 DNS 最多等多久
    cache_days: int = 7
    # 认定为「本校/校园网」的关键词，命中即打标签
    campus_keywords: List[str] = field(
        default_factory=lambda: ["Jiaxing University", "嘉兴", "CERNET", "教育和科研", "edu.cn", "zjxu"]
    )


@dataclass
class NotifyConfig:
    enabled: bool = True
    channels: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    cooldown_seconds: int = 120          # 全局最短告警间隔，防轰炸
    max_alerts_per_hour: int = 20
    include_html: bool = True
    attach_ip_map_link: bool = True      # 邮件里附一个地图链接


@dataclass
class AppConfig:
    webvpn: WebvpnConfig = field(default_factory=WebvpnConfig)
    browser: BrowserConfig = field(default_factory=BrowserConfig)
    navigation: NavigationConfig = field(default_factory=NavigationConfig)
    poll: PollConfig = field(default_factory=PollConfig)
    rules: RulesConfig = field(default_factory=RulesConfig)
    ipintel: IpIntelConfig = field(default_factory=IpIntelConfig)
    notify: NotifyConfig = field(default_factory=NotifyConfig)
    state_dir: str = "state"
    log_dir: str = "logs"
    dump_dir: str = "dumps"
    log_level: str = "INFO"
    base_dir: Path = field(default_factory=lambda: Path.cwd())

    # ---- 路径助手 ----
    def path(self, value: str) -> Path:
        p = Path(value).expanduser()
        return p if p.is_absolute() else (self.base_dir / p)

    @property
    def state_path(self) -> Path:
        return self.path(self.state_dir)

    @property
    def log_path(self) -> Path:
        return self.path(self.log_dir)

    @property
    def dump_path(self) -> Path:
        return self.path(self.dump_dir)

    def ensure_dirs(self) -> None:
        for p in (self.state_path, self.log_path, self.dump_path):
            p.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------------------------------- #
# 组装
# --------------------------------------------------------------------------- #
def _fill(dc_type, data: Dict[str, Any]):
    """只取 dataclass 认识的字段，多余的 key 忽略（并交给调用方提示）。"""
    known = {f.name for f in dc_type.__dataclass_fields__.values()}  # type: ignore[attr-defined]
    kwargs = {k: v for k, v in (data or {}).items() if k in known}
    return dc_type(**kwargs), sorted(set((data or {}).keys()) - known)


def load_config(config_file: Optional[Path] = None, base_dir: Optional[Path] = None) -> "AppConfig":
    base = (base_dir or Path.cwd()).resolve()
    load_dotenv(base / ".env")

    raw: Dict[str, Any] = {}
    if config_file is None:
        for candidate in (base / "config.yaml", base / "config.yml", base / "config.example.yaml"):
            if candidate.exists():
                config_file = candidate
                break
    if config_file and Path(config_file).exists():
        raw = yaml.safe_load(Path(config_file).read_text(encoding="utf-8-sig")) or {}
    raw = _expand(raw)

    unknown: List[str] = []
    webvpn, u = _fill(WebvpnConfig, raw.get("webvpn", {})); unknown += [f"webvpn.{x}" for x in u]
    browser, u = _fill(BrowserConfig, raw.get("browser", {})); unknown += [f"browser.{x}" for x in u]
    nav, u = _fill(NavigationConfig, raw.get("navigation", {})); unknown += [f"navigation.{x}" for x in u]
    poll, u = _fill(PollConfig, raw.get("poll", {})); unknown += [f"poll.{x}" for x in u]
    rules, u = _fill(RulesConfig, raw.get("rules", {})); unknown += [f"rules.{x}" for x in u]
    ipintel, u = _fill(IpIntelConfig, raw.get("ipintel", {})); unknown += [f"ipintel.{x}" for x in u]
    notify, u = _fill(NotifyConfig, raw.get("notify", {})); unknown += [f"notify.{x}" for x in u]

    cfg = AppConfig(
        webvpn=webvpn, browser=browser, navigation=nav, poll=poll,
        rules=rules, ipintel=ipintel, notify=notify,
        state_dir=raw.get("state_dir", "state"),
        log_dir=raw.get("log_dir", "logs"),
        dump_dir=raw.get("dump_dir", "dumps"),
        log_level=str(raw.get("log_level", "INFO")).upper(),
        base_dir=base,
    )

    # 环境变量对敏感项做最终覆盖
    cfg.webvpn.username = os.environ.get("WEBVPN_USERNAME") or cfg.webvpn.username
    cfg.webvpn.password = os.environ.get("WEBVPN_PASSWORD") or cfg.webvpn.password
    cfg.webvpn.login_url = os.environ.get("WEBVPN_LOGIN_URL") or cfg.webvpn.login_url
    cfg.webvpn.target_url = os.environ.get("WEBVPN_TARGET_URL") or cfg.webvpn.target_url
    cfg.ipintel.qqmap_key = os.environ.get("QQMAP_KEY") or cfg.ipintel.qqmap_key

    # 通道里的 ${ENV} 已经展开过，这里再兜底几个常用的
    _env_channel_defaults(cfg)

    cfg.unknown_keys = unknown  # type: ignore[attr-defined]
    cfg.config_file = str(config_file) if config_file else ""  # type: ignore[attr-defined]
    cfg.using_example_config = bool(  # type: ignore[attr-defined]
        config_file and Path(config_file).name == "config.example.yaml"
    )
    return cfg


def _env_channel_defaults(cfg: AppConfig) -> None:
    ch = cfg.notify.channels
    mapping = {
        ("email", "password"): "SMTP_PASSWORD",
        ("email", "username"): "SMTP_USERNAME",
        ("bark", "key"): "BARK_KEY",
        ("serverchan", "sendkey"): "SERVERCHAN_SENDKEY",
        ("pushplus", "token"): "PUSHPLUS_TOKEN",
        ("wecom", "key"): "WECOM_KEY",
        ("dingtalk", "token"): "DINGTALK_TOKEN",
        ("dingtalk", "secret"): "DINGTALK_SECRET",
        ("feishu", "token"): "FEISHU_TOKEN",
        ("feishu", "secret"): "FEISHU_SECRET",
        ("telegram", "bot_token"): "TELEGRAM_BOT_TOKEN",
        ("telegram", "chat_id"): "TELEGRAM_CHAT_ID",
    }
    for (channel, key), env_name in mapping.items():
        env_value = os.environ.get(env_name)
        if not env_value:
            continue
        ch.setdefault(channel, {})
        if not ch[channel].get(key):
            ch[channel][key] = env_value
            ch[channel].setdefault("enabled", True)
