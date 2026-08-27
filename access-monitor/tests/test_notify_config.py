"""通知通道与配置加载的离线测试。不发任何真实请求。"""
from __future__ import annotations

import base64
import hashlib
import hmac
import os
import sys
import tempfile
import urllib.parse
from datetime import datetime
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from monitor.config import load_config, load_dotenv        # noqa: E402
from monitor.models import Alert                           # noqa: E402
from monitor.notify import (                               # noqa: E402
    DingTalkChannel, EmailChannel, FeishuChannel, NotificationHub, ServerChanChannel,
)


def _alert() -> Alert:
    return Alert(rule="burst", title="测试", summary="测试", triggered_at=datetime.now(),
                 dedup_key="k")


def test_dingtalk_sign_is_encoded_exactly_once():
    """钉钉加签：自己 quote 一次、requests 再编一次，钉钉解出来就对不上了。"""
    secret = "SECabcdef1234567890"
    ch = DingTalkChannel({"token": "tok", "secret": secret})
    with mock.patch("monitor.notify.requests.post") as post:
        post.return_value.status_code = 200
        post.return_value.content = b"{}"
        post.return_value.json = lambda: {"errcode": 0}
        ch.send(_alert())
        params = post.call_args.kwargs["params"]

    ts = params["timestamp"]
    expected = base64.b64encode(
        hmac.new(secret.encode(), f"{ts}\n{secret}".encode(), hashlib.sha256).digest()
    ).decode()
    assert params["sign"] == expected, "签名必须是原始 base64，交给 requests 编码一次"
    assert "%" not in params["sign"], "自己 quote 过就说明会被编码两次"
    # 再确认一下：URL 编码一次之后确实能还原
    assert urllib.parse.unquote(urllib.parse.quote_plus(params["sign"])) == expected


def test_feishu_sign_uses_timestamp_as_key_over_empty_message():
    """飞书的加签算法和钉钉不一样：拿 "时间戳\\n密钥" 当 key，对空消息做 HMAC。"""
    secret = "abc123"
    ch = FeishuChannel({"token": "t", "secret": secret})
    with mock.patch("monitor.notify.requests.post") as post:
        post.return_value.status_code = 200
        post.return_value.content = b"{}"
        post.return_value.json = lambda: {"code": 0}
        ch.send(_alert())
        payload = post.call_args.kwargs["json"]
    ts = payload["timestamp"]
    expected = base64.b64encode(
        hmac.new(f"{ts}\n{secret}".encode(), b"", hashlib.sha256).digest()
    ).decode()
    assert payload["sign"] == expected
    assert len(ts) == 10, "飞书用的是秒级时间戳（钉钉才是毫秒）"


def test_serverchan_routes_by_key_prefix():
    assert ServerChanChannel({"sendkey": "sctp88tXYZ"}).endpoint() == \
        "https://88.push.ft07.com/send/sctp88tXYZ.send"
    assert ServerChanChannel({"sendkey": "SCT9tABC"}).endpoint() == \
        "https://sctapi.ftqq.com/SCT9tABC.send"


def test_unset_env_var_in_a_list_counts_as_missing():
    """`to: ["${SMTP_USERNAME}"]` 在变量没设置时会展开成 [""]。

    它是个非空列表，用 `not value` 判断会以为填好了，于是通道被启用，
    然后每条告警都在日志里报一次错。
    """
    ch = EmailChannel({"host": "smtp.qq.com", "username": "u", "password": "p", "to": [""]})
    assert "to" in ch.missing
    assert EmailChannel({"host": "h", "username": "u", "password": "p",
                         "to": ["a@b.com"]}).missing == []


def test_channel_with_empty_yaml_body_does_not_crash():
    """YAML 里只写了 `bark:` 没有子项时，值是 None 而不是 {}。"""
    with tempfile.TemporaryDirectory() as td:
        base = Path(td)
        (base / "config.yaml").write_text(
            "notify:\n  channels:\n    bark:\n    console:\n      enabled: true\n", encoding="utf-8")
        os.environ["BARK_KEY"] = "从环境变量来的"
        try:
            cfg = load_config(base / "config.yaml", base_dir=base)
            assert cfg.notify.channels["bark"]["key"] == "从环境变量来的"
        finally:
            os.environ.pop("BARK_KEY", None)


def test_dotenv_strips_trailing_comment_but_keeps_hash_in_password():
    with tempfile.TemporaryDirectory() as td:
        env = Path(td) / ".env"
        env.write_text(
            'A_TOKEN=abcd1234      # 这是注释\n'
            'A_PASSWORD=Pa55w#rd\n'                 # 密码里就带 #，不能被截断
            'A_QUOTED="有 # 的值"   # 也是注释\n',
            encoding="utf-8")
        for k in ("A_TOKEN", "A_PASSWORD", "A_QUOTED"):
            os.environ.pop(k, None)
        try:
            loaded = load_dotenv(env)
            assert loaded["A_TOKEN"] == "abcd1234", repr(loaded["A_TOKEN"])
            assert loaded["A_PASSWORD"] == "Pa55w#rd", repr(loaded["A_PASSWORD"])
            assert loaded["A_QUOTED"] == "有 # 的值", repr(loaded["A_QUOTED"])
        finally:
            for k in ("A_TOKEN", "A_PASSWORD", "A_QUOTED"):
                os.environ.pop(k, None)


def test_configured_but_disabled_channel_is_reported():
    """只在 .env 里填了 key、忘了把 enabled 改成 true —— 必须说出来。"""
    from monitor.config import NotifyConfig
    hub = NotificationHub(NotifyConfig(channels={
        "console": {"enabled": True},
        "bark": {"enabled": False, "key": "填好了"},
    }))
    assert hub.configured_but_off == ["bark"]
    assert [c.name for c in hub.channels] == ["console"]


def test_rule_cooldown_is_actually_used():
    """rules.cooldown_seconds 以前是个死配置，改它没有任何效果。"""
    from monitor.config import NotifyConfig

    class FakeStore:
        def __init__(self, ts):
            self.ts = ts

        def last_alert_ts(self, rule=None, dedup_key=None):
            return self.ts

        def alerts_since(self, since):
            return 0

    now = datetime.now()
    store = FakeStore(now.timestamp() - 100)
    hub = NotificationHub(NotifyConfig(cooldown_seconds=10), store, rule_cooldown_seconds=600)
    ok, why = hub.should_send(_alert(), now)
    assert ok is False and "600" in why, why


if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"  ✓ {name}")
            except AssertionError as exc:
                failures += 1
                print(f"  ✗ {name}: {exc}")
            except Exception as exc:  # noqa: BLE001
                failures += 1
                import traceback
                traceback.print_exc()
                print(f"  ✗ {name}: {type(exc).__name__}: {exc}")
    print("全部通过" if not failures else f"{failures} 个测试失败")
    sys.exit(1 if failures else 0)
