# -*- coding: utf-8 -*-
"""Claude 接入层：流式对话 + 结构化文档生成 + 离线演示回退。"""
import json
import re
from typing import Iterator, List

from . import config
from .corpus import CORPUS
from . import prompts


class LLMUnavailable(Exception):
    pass


def _client():
    if not config.ANTHROPIC_API_KEY:
        raise LLMUnavailable("未配置 ANTHROPIC_API_KEY")
    import anthropic
    kwargs = {"api_key": config.ANTHROPIC_API_KEY}
    if config.ANTHROPIC_BASE_URL:
        kwargs["base_url"] = config.ANTHROPIC_BASE_URL
    return anthropic.Anthropic(**kwargs)


def _policy_digest(text: str) -> str:
    matched = CORPUS.match_policies(text)
    if not matched:
        return "（未命中结构化政策库，请基于语料库自行判断）"
    lines = []
    for p in matched:
        conds = "；".join(p.get("conditions", []))
        lines.append(
            f"- {p['name']}（{p['level']}，{p['dept']}）：{p['amount']}。条件：{conds}。来源：{p.get('source','')}"
        )
    return "\n".join(lines)


def build_system(user_text: str) -> str:
    ctx = CORPUS.context_for(user_text, top_k=6)
    return prompts.system_prompt(ctx, _policy_digest(user_text))


# ------------------------------------------------------------------ 对话 ---
def stream_chat(messages: List[dict], attachment_text: str = "") -> Iterator[str]:
    """messages: [{'role':'user'|'assistant','content': str 或 内容块列表}]"""
    probe = attachment_text + " " + " ".join(
        m["content"] if isinstance(m.get("content"), str) else ""
        for m in messages[-4:]
    )
    system = build_system(probe)

    if config.DEMO_MODE:
        from .demo import demo_stream
        yield from demo_stream(messages, attachment_text)
        return

    client = _client()
    with client.messages.stream(
        model=config.MODEL,
        max_tokens=config.MAX_TOKENS,
        system=system,
        messages=messages,
    ) as stream:
        for text in stream.text_stream:
            yield text


# -------------------------------------------------------------- 文档生成 ---
def _extract_json(raw: str) -> dict:
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    start, end = raw.find("{"), raw.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("模型没有返回 JSON")
    return json.loads(raw[start:end + 1])


def _complete(prompt: str, max_tokens: int = 16000) -> str:
    client = _client()
    chunks = []
    with client.messages.stream(
        model=config.MODEL,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            chunks.append(text)
    return "".join(chunks)


def gen_improve_doc(plan_text: str) -> dict:
    if config.DEMO_MODE:
        from .demo import demo_improve_blocks
        return demo_improve_blocks(plan_text)
    ctx = CORPUS.context_for(plan_text + " 政策 税收 改造 人工智能 资质", top_k=8)
    prompt = prompts.improve_plan_prompt(plan_text, ctx, _policy_digest(plan_text))
    return _extract_json(_complete(prompt))


def gen_landing_doc(plan_text: str, improve_summary: str = "") -> dict:
    if config.DEMO_MODE:
        from .demo import demo_landing_blocks
        return demo_landing_blocks(plan_text)
    ctx = CORPUS.context_for(
        plan_text + " 注册 开户 选址 租金 税务 社保 融资 复盘 政策申报", top_k=10
    )
    prompt = prompts.landing_plan_prompt(
        plan_text, improve_summary or "把人工服务产品化、引入人工智能、形成软件著作权、按科技类企业路径申报政策。",
        ctx, _policy_digest(plan_text),
    )
    return _extract_json(_complete(prompt, max_tokens=20000))
