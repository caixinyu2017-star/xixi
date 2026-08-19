# -*- coding: utf-8 -*-
"""语料库加载与检索。

采用中文友好的字符 n-gram 加权检索：不引入向量库依赖，
在几十篇本地语料的规模下召回质量足够，且零配置、可离线。
"""
import json
import re
from dataclasses import dataclass, field
from typing import List

from .config import CORPUS_DIR


@dataclass
class Doc:
    doc_id: str
    title: str
    stage: str
    keywords: List[str]
    body: str
    path: str
    _grams: set = field(default_factory=set, repr=False)


_FRONT_MATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)


def _parse_front_matter(text: str):
    meta, body = {}, text
    m = _FRONT_MATTER.match(text)
    if m:
        body = text[m.end():]
        for line in m.group(1).splitlines():
            if ":" not in line:
                continue
            k, _, v = line.partition(":")
            k, v = k.strip(), v.strip()
            if v.startswith("[") and v.endswith("]"):
                meta[k] = [x.strip() for x in v[1:-1].split(",") if x.strip()]
            else:
                meta[k] = v
    return meta, body


def _grams(text: str, n: int = 2) -> set:
    """中文按 2-gram，英文与数字按词。"""
    text = text.lower()
    words = set(re.findall(r"[a-z0-9]+", text))
    zh = re.sub(r"[^一-鿿]", "", text)
    grams = {zh[i:i + n] for i in range(len(zh) - n + 1)}
    return words | grams


class Corpus:
    def __init__(self):
        self.docs: List[Doc] = []
        self.policies = []
        self.load()

    def load(self):
        self.docs.clear()
        for path in sorted(CORPUS_DIR.glob("*.md")):
            raw = path.read_text(encoding="utf-8")
            meta, body = _parse_front_matter(raw)
            doc = Doc(
                doc_id=meta.get("id", path.stem),
                title=meta.get("title", path.stem),
                stage=meta.get("stage", "通用"),
                keywords=meta.get("keywords", []) or [],
                body=body.strip(),
                path=str(path),
            )
            doc._grams = _grams(doc.title + " " + " ".join(doc.keywords) + " " + doc.body)
            self.docs.append(doc)
        pol_path = CORPUS_DIR / "policies.json"
        if pol_path.exists():
            self.policies = json.loads(pol_path.read_text(encoding="utf-8"))["policies"]

    # ---------------------------------------------------------------- 检索 --
    def search(self, query: str, top_k: int = 6) -> List[Doc]:
        q = _grams(query)
        if not q:
            return self.docs[:top_k]
        scored = []
        for doc in self.docs:
            overlap = len(q & doc._grams)
            kw_hit = sum(3 for kw in doc.keywords if kw and kw.lower() in query.lower())
            title_hit = 5 if any(t in query for t in re.findall(r"[一-鿿]{2,}", doc.title)) else 0
            score = overlap / (len(q) ** 0.5 + 1) + kw_hit + title_hit
            scored.append((score, doc))
        scored.sort(key=lambda x: -x[0])
        return [d for s, d in scored[:top_k] if s > 0] or self.docs[:top_k]

    # 场景词 -> 政策标签。用户很少直接说出政策名，更多是描述场景，
    # 这张表把口语化的描述翻译成政策标签，避免检索空转。
    SCENE_TAGS = {
        "创业": ["创业启蒙", "普惠"], "开公司": ["创业启蒙", "普惠"], "注册": ["创业启蒙", "普惠"],
        "公司": ["普惠"], "个体": ["个体工商户", "普惠"], "工作室": ["个体工商户", "普惠"],
        "大学生": ["大学生", "人才"], "毕业": ["大学生", "人才"], "学生": ["大学生"],
        "硕士": ["人才"], "博士": ["人才"], "本科": ["人才"], "应届": ["人才", "大学生"],
        "软件": ["软件", "科技"], "系统": ["软件", "科技"], "平台": ["软件", "科技"],
        "开发": ["软件", "科技", "研发"], "算法": ["科技", "研发"], "技术": ["技术", "科技"],
        "人工智能": ["人工智能", "科技"], "智能": ["人工智能", "科技"], "模型": ["人工智能", "备案"],
        "算力": ["算力", "人工智能"], "数据": ["人工智能", "科技"],
        "研发": ["研发", "科技"], "专利": ["科技", "研发"], "著作权": ["软件", "科技"],
        "税": ["税收", "普惠"], "发票": ["税收", "普惠"], "增值税": ["税收", "普惠"],
        "所得税": ["税收", "普惠"], "小微": ["普惠", "小微企业"], "小规模": ["税收", "普惠"],
        "租": ["场地", "租金", "选址"], "场地": ["场地", "租金"], "办公室": ["场地", "租金"],
        "选址": ["选址", "场地"], "孵化": ["场地", "创业启蒙"],
        "社保": ["社保"], "员工": ["用工", "社保"], "招人": ["用工"], "用工": ["用工"],
        "贷款": ["融资", "贷款", "科创"], "融资": ["融资", "科创"], "钱": ["融资"],
        "投资": ["融资"], "担保": ["融资", "担保"], "贴息": ["融资", "贷款"],
        "补贴": ["普惠", "创业启蒙", "大学生"], "政策": ["普惠", "创业启蒙"],
        "内容": ["软件", "科技"], "媒体": ["软件", "科技"], "投稿": ["软件", "科技"],
        "广告": ["软件", "科技"], "宣传": ["软件", "科技"],
        "扩张": ["用工", "融资"], "招聘": ["用工"], "住": ["安居"], "房": ["安居"],
    }

    # 任何创业者都用得上的兜底政策，保证政策雷达不会空着
    FALLBACK_IDS = [
        "JX-CY-001", "JX-CY-003", "JX-CY-005", "JX-CY-006",
        "CN-SS-003", "CN-SS-004", "CN-SS-005", "JX-RC-001",
    ]

    def match_policies(self, text: str, top_k: int = 12):
        """按场景词、标签、政策名与条件多路打分，返回匹配度排序的政策列表。"""
        text = text or ""
        t = text.lower()

        # 1) 把口语描述翻译成政策标签
        hit_tags = {}
        for scene, tags in self.SCENE_TAGS.items():
            if scene in text:
                for tag in tags:
                    hit_tags[tag] = hit_tags.get(tag, 0) + 1

        results = []
        for pol in self.policies:
            score = 0.0
            for tag in pol.get("tags", []):
                if tag.lower() in t:
                    score += 5
                if tag in hit_tags:
                    score += 3 + min(hit_tags[tag], 3)
            for word in re.findall(r"[一-鿿]{2,6}", pol["name"]):
                if word in text:
                    score += 3
            for cond in pol.get("conditions", []):
                for word in re.findall(r"[一-鿿]{3,8}", cond):
                    if word in text:
                        score += 1.5
            if pol.get("dept") and pol["dept"][:2] in text:
                score += 1
            if score > 0:
                results.append((score, pol))

        results.sort(key=lambda x: -x[0])
        matched = [p for s, p in results[:top_k]]

        # 2) 兜底：命中太少时补上人人可用的普惠政策
        if len(matched) < 5:
            have = {p["id"] for p in matched}
            by_id = {p["id"]: p for p in self.policies}
            for pid in self.FALLBACK_IDS:
                if pid in by_id and pid not in have:
                    matched.append(by_id[pid])
                    have.add(pid)
                if len(matched) >= max(6, top_k // 2):
                    break
        return matched[:top_k]

    def context_for(self, query: str, top_k: int = 6, budget_chars: int = 22000) -> str:
        docs = self.search(query, top_k)
        parts, used = [], 0
        for doc in docs:
            chunk = f"### 语料：{doc.title}（环节：{doc.stage}）\n{doc.body}\n"
            if used + len(chunk) > budget_chars:
                chunk = chunk[: max(0, budget_chars - used)]
            parts.append(chunk)
            used += len(chunk)
            if used >= budget_chars:
                break
        return "\n".join(parts)


CORPUS = Corpus()
