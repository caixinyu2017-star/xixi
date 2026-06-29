#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
consistency_audit.py —— 跨材料一致性审计器 (Light / light-consistency)

读取 db09 单一事实源(受控术语表 / 方法名锁定 / 指标登记表)，扫描一组材料文本，
检测并定位以下不一致，输出结构化报告：

  SUBSTITUTION  受控术语/方法名被同义改写或写错(大小写、连字符、近义词)
  METRIC_NAME   同一指标被换名(如把 F1 写成 准确率)
  METRIC_VALUE  同一指标(同方法×数据集)在不同材料数值不一致(论文 vs PPT)
  GROSS_MISMATCH 数值同量级但超容差(30%~300%)，疑严重错填，单列告警不静默丢弃
  CONTRIBUTION_DRIFT 创新点/贡献在某材料提法偏离 db09 标准措辞
  COVERAGE_GAP  某规范术语/指标只在部分材料出现，在应出现的材料里缺席

每条发现带定位(material:line)与修正建议。报告末尾做完整性自检(条数核对)。

用法：
  python consistency_audit.py --db09 <dir> --materials a.txt b.txt [--json out.json]
  python consistency_audit.py            # 无参数 -> 内置合成材料自测

依赖：PyYAML(已确认环境可用)；无网络、无外部数据。
"""
import sys, os, re, json, argparse, glob
sys.stdout.reconfigure(encoding="utf-8")

try:
    import yaml
except ImportError:
    sys.stderr.write("需要 PyYAML: pip install pyyaml\n"); sys.exit(2)

NUM_RE = re.compile(r"(?<![\d.])(\d+(?:\.\d+)?)")

# 数值比对的相对偏差分带(X-2)：
#   reldiff <= SCOPE_REL          -> 视为该指标取值，进入按 decimals 的精确比对
#   SCOPE_REL < reldiff <= GROSS_REL -> 疑似严重错填，单列 GROSS_MISMATCH 告警(不再静默丢弃)
#   reldiff > GROSS_REL           -> 数量级无关(年份/计数等)，丢弃
SCOPE_REL = 0.30
GROSS_REL = 3.0

# 创新点漂移检测阈值(X-5)：
#   coverage(材料行覆盖 canonical 关键 token 的比例) >= ADDR_MIN -> 认定该材料在表述此贡献
#   该行与 canonical 的 Jaccard < DRIFT_SIM            -> 提法偏离，报 CONTRIBUTION_DRIFT
ADDR_MIN = 0.25
DRIFT_SIM = 0.55


def _forbidden_literals(forbidden):
    """规范化 forbidden 列表(X-1)：

    字符串 = 需实际匹配的禁用写法；
    映射 {text:..., placeholder: true} = 说明性占位(如"本文方法"在正式名出现后仍这么写)，
        语义需人工判断、不能 literal 匹配，故由 schema 显式标记跳过——
        取代旧的 bad.startswith("本文方法") 字符串 hack，使其余 forbidden 项真正生效。
    返回需实际匹配的禁用写法字符串列表。
    """
    out = []
    for item in forbidden or []:
        if isinstance(item, dict):
            if item.get("placeholder"):
                continue
            txt = item.get("text")
            if txt:
                out.append(txt)
        elif isinstance(item, str) and item.strip():
            out.append(item)
    return out


def _normalize_value(num, auth, unit):
    """单位归一化(X-2)：% 指标的分数写法(0-1)与百分数(0-100)互转，使 0.876 与 87.6 可比。

    仅对 unit=='%' 生效：权威值为百分数而抽取值像分数则放大 100 倍，反之缩小。
    其它单位(ms/M/无)原样返回。
    """
    if unit == "%" and auth:
        if 0 < num <= 1.0 and abs(auth) > 1.0:
            return num * 100.0
        if 0 < abs(auth) <= 1.0 and num > 1.0:
            return num / 100.0
    return num


def load_db09(db_dir):
    """加载三份 db09 schema；缺失文件容错返回空表。"""
    def _load(name):
        p = os.path.join(db_dir, name)
        if not os.path.exists(p):
            return {}
        with open(p, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {
        "glossary": _load("db09_glossary.yaml").get("terms", []),
        "methods": _load("db09_method_lock.yaml").get("methods", []),
        "metrics": _load("db09_metric_registry.yaml").get("metrics", []),
        "contributions": _load("db09_glossary.yaml").get("contributions", []),
    }


def load_db09_markdown(path):
    """解析真实 db09 项目的 terminology.md(Markdown 表)为 db09 结构。

    db09 项目按 light-memory-pm 约定把受控术语存为 Markdown 表:
        | 类别 | 标准叫法 | 缩写 | 英文 | 备注 |
    本加载器把 方法/数据集→methods+glossary，指标→metrics+glossary，其余→glossary。
    诚实限制:Markdown 表无 forbidden/confusable/权威数值列，故只支撑
    COVERAGE_GAP(覆盖缺口)检测;SUBSTITUTION/METRIC_VALUE 需 YAML schema 才完整。
    """
    glossary, methods, metrics = [], [], []
    contributions = []
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    n = 0
    for ln in lines:
        if not ln.strip().startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        cat, canon = cells[0], cells[1]
        if cat in ("类别", "") or set(canon) <= {"-", "—", " "} or canon == "标准叫法":
            continue  # 表头 / 分隔行 / 空
        if cat.startswith("创新点"):  # X-5：创新点行作贡献单一事实源(只读)
            if canon:
                contributions.append({"id": cat, "canonical": canon})
            continue
        abbr = cells[2].strip() if len(cells) > 2 else ""
        en = cells[3].strip() if len(cells) > 3 else ""
        aliases = [a for a in (abbr, en) if a and set(a) > {"-", "—"}]
        n += 1
        item = {"id": f"md.{n}", "canonical": canon, "aliases": aliases,
                "forbidden": [], "case_lock": False, "zh": canon, "en": en}
        glossary.append(item)
        if cat == "指标":
            metrics.append({"id": f"md.metric.{n}", "canonical": canon,
                            "aliases": aliases, "confusable": [], "unit": "",
                            "decimals": 1, "records": []})
        elif cat in ("方法", "数据集"):
            methods.append({"id": f"md.method.{n}", "canonical": canon, "forbidden": []})
    return {"glossary": glossary, "methods": methods, "metrics": metrics,
            "contributions": contributions}


def load_db09_auto(path):
    """db09 来源自适应:目录含三份 yaml 走 schema 模式;否则找 terminology.md 走 Markdown 模式。"""
    if os.path.isfile(path) and path.endswith(".md"):
        return load_db09_markdown(path)
    if os.path.isdir(path):
        if os.path.exists(os.path.join(path, "db09_glossary.yaml")):
            return load_db09(path)
        term = os.path.join(path, "terminology.md")
        if os.path.exists(term):
            return load_db09_markdown(term)
    raise FileNotFoundError(
        f"db09 源无法识别:{path}(需含 db09_*.yaml 的目录,或 terminology.md)")


def read_material(path):
    with open(path, encoding="utf-8") as f:
        return {"name": os.path.basename(path), "lines": f.read().splitlines()}


def _finding(kind, severity, material, line_no, line_text, detail, suggestion):
    return {
        "kind": kind, "severity": severity,
        "location": f"{material}:{line_no}",
        "line": line_text.strip(),
        "detail": detail, "suggestion": suggestion,
    }


def _word_present(text, token, case_lock):
    """词在文本中是否出现。含中文则按子串匹配；纯 ASCII 用词边界，避免 'AP' 命中 'mAP'。"""
    if re.search(r"[^\x00-\x7f]", token):
        hay = text if case_lock else text.lower()
        ndl = token if case_lock else token.lower()
        return ndl in hay
    flags = 0 if case_lock else re.IGNORECASE
    return re.search(r"(?<![A-Za-z0-9_])" + re.escape(token) + r"(?![A-Za-z0-9_])", text, flags) is not None


# ---------------------------------------------------------------------------
# 检测 1：受控术语 / 方法名 的禁用写法 (SUBSTITUTION)
# ---------------------------------------------------------------------------
def audit_substitution(materials, db09):
    findings = []
    entries = []
    for t in db09["glossary"]:
        entries.append(("term", t.get("canonical"), _forbidden_literals(t.get("forbidden", [])), t.get("case_lock", False)))
    for m in db09["methods"]:
        entries.append(("method", m.get("canonical"), _forbidden_literals(m.get("forbidden", [])), True))
    for mat in materials:
        for i, line in enumerate(mat["lines"], 1):
            for kind, canon, forbidden, case_lock in entries:
                for bad in forbidden:
                    if _word_present(line, bad, case_lock):
                        findings.append(_finding(
                            "SUBSTITUTION", "error", mat["name"], i, line,
                            f"出现禁用写法 '{bad}'（{kind} 规范名应为 '{canon}'）",
                            f"将 '{bad}' 改为规范写法 '{canon}'"))
    return findings


# ---------------------------------------------------------------------------
# 检测 2：指标换名 (METRIC_NAME) —— 把易混名(confusable)当成该指标在用
# ---------------------------------------------------------------------------
def audit_metric_name(materials, db09):
    findings = []
    for mat in materials:
        for i, line in enumerate(mat["lines"], 1):
            for met in db09["metrics"]:
                canon = met.get("canonical")
                for conf in met.get("confusable", []):
                    # 仅当该行同时带数字时才疑似"用错名报指标值"，降低误报
                    if _word_present(line, conf, case_lock=False) and NUM_RE.search(line):
                        findings.append(_finding(
                            "METRIC_NAME", "warn", mat["name"], i, line,
                            f"疑似用易混名 '{conf}' 指代指标 '{canon}'（二者语义不同）",
                            f"若确指 '{canon}' 则改名；若确是 '{conf}' 则它未登记，需在 db09 注册"))
    return findings


# ---------------------------------------------------------------------------
# 检测 3：指标数值冲突 (METRIC_VALUE)
#   思路：对每个指标的权威 records(method×dataset→value)，在材料中找"同时提到
#   该指标名 + 该方法名"的行，抽取数字，与权威值比对；并跨材料比对同一(指标,方法)
#   出现的不同数值。
# ---------------------------------------------------------------------------
def _extract_numbers(line):
    return [float(x) for x in NUM_RE.findall(line)]


def _positions(line, token, case_lock):
    """返回 token 在行内所有出现的起始下标(词边界规则同 _word_present)。"""
    if re.search(r"[^\x00-\x7f]", token):
        hay = line if case_lock else line.lower()
        ndl = token if case_lock else token.lower()
        return [m.start() for m in re.finditer(re.escape(ndl), hay)]
    flags = 0 if case_lock else re.IGNORECASE
    pat = r"(?<![A-Za-z0-9_])" + re.escape(token) + r"(?![A-Za-z0-9_])"
    return [m.start() for m in re.finditer(pat, line, flags)]


def audit_metric_value(materials, db09):
    """位置感知：一行内可并列多指标/多方法，按"就近"把每个数字配给
    最近的指标名与最近的方法名，避免 F1 与 mAP 的数字互相串位。"""
    findings = []
    observed = {}  # (mid, canon, method, dec, auth) -> [(value, material, line_no, line)]
    metrics = []
    for met in db09["metrics"]:
        metrics.append({
            "mid": met["id"], "canon": met["canonical"],
            "names": [met["canonical"]] + met.get("aliases", []),
            "dec": met.get("decimals", 1),
            "unit": met.get("unit", ""),
            "rec": {r["method"]: r["value"] for r in met.get("records", [])},
        })
    all_methods = sorted({m for met in metrics for m in met["rec"]}, key=len, reverse=True)

    for mat in materials:
        for i, line in enumerate(mat["lines"], 1):
            # 1) 收集本行所有"指标名出现位置" -> (pos, metric)
            mpos = []
            for met in metrics:
                for n in met["names"]:
                    for p in _positions(line, n, case_lock=False):
                        mpos.append((p, p + len(n), met))
            if not mpos:
                continue
            # 2) 收集方法名位置
            methpos = [(p, mname) for mname in all_methods
                       for p in _positions(line, mname, case_lock=True)]
            if not methpos:
                continue
            # 3) 把"命名实体"片段从行内挖空再取数字：避免实体内嵌数字被误读为指标值
            #    (mAP@0.5 的 0.5、YOLOv8 的 8、CrowdScene-2k 的 2)。
            #    挖空范围 = 指标名 + 方法名 + 受控术语/数据集名(含别名)，但保留位置坐标。
            mask_spans = [(s, e) for s, e, _ in mpos]
            mask_spans += [(p, p + len(mn)) for p, mn in methpos]
            for term in db09.get("glossary", []):
                for nm in [term.get("canonical")] + term.get("aliases", []):
                    if nm and re.search(r"\d", nm):  # 仅含数字的实体才需挖空
                        for p in _positions(line, nm, term.get("case_lock", False)):
                            mask_spans.append((p, p + len(nm)))
            masked = list(line)
            for s, e in mask_spans:
                for k in range(s, e):
                    masked[k] = " "
            masked = "".join(masked)
            for m in NUM_RE.finditer(masked):
                num, npos = float(m.group(1)), m.start()
                # 数字归属：最近(优先在其左侧)的指标名
                met = min(mpos, key=lambda mp: (npos < mp[0], abs(npos - mp[0])))[2]
                # 方法归属：优先取数字左侧最近的方法名(主语通常在指标/数值之前；
                # 句尾的"优于基线 YOLOv8"虽文本更近，但不是该数值的归属方)。
                left = [mp for mp in methpos if mp[0] <= npos]
                cand = left if left else methpos
                owner = min(cand, key=lambda mp: abs(npos - mp[0]))[1]
                auth = met["rec"].get(owner)
                if auth is None:
                    continue  # 该方法无此指标记录，与本数字无关
                # 单位归一化(X-2)：% 指标的分数/百分数互转，使 0.876 与 87.6 可比
                num_n = _normalize_value(num, auth, met["unit"])
                reldiff = abs(num_n - auth) / abs(auth) if auth else 0.0
                if reldiff > GROSS_REL:
                    continue  # 数量级无关(年份/计数等)，丢弃
                if reldiff > SCOPE_REL:
                    # 中间带：疑似严重错填，单列 GROSS_MISMATCH(不再静默丢弃)
                    findings.append(_finding(
                        "GROSS_MISMATCH", "error", mat["name"], i, line,
                        f"{owner} 的 {met['canon']} 标为 {num:g}，与 db09 权威值 "
                        f"{auth:g} 相差 {reldiff*100:.0f}%(疑严重错填或张冠李戴)",
                        f"核对该数值是否填错指标/方法；确属 {met['canon']} 则订正为 {auth:g}"))
                    continue
                observed.setdefault(
                    (met["mid"], met["canon"], owner, met["dec"], auth), []
                ).append((num_n, mat["name"], i, line))
    return findings, observed


def evaluate_value_conflicts(observed):
    """对每个(指标,方法)：标记与权威值不符、以及跨材料互相矛盾的数值。"""
    findings = []
    for (mid, canon, method, dec, auth), obs in observed.items():
        seen_vals = {}
        for claimed, mat, ln, line in obs:
            seen_vals.setdefault(round(claimed, dec), []).append((mat, ln, line))
            if abs(claimed - auth) > (0.5 * 10 ** (-dec)):  # 超出约定精度的容差即冲突
                findings.append(_finding(
                    "METRIC_VALUE", "error", mat, ln, line,
                    f"{method} 的 {canon} 标为 {claimed:.{dec}f}，与 db09 权威值 {auth:.{dec}f} 不符",
                    f"核对实验记录后统一为权威值 {auth:.{dec}f}，并更新 db09 或材料"))
        if len(seen_vals) > 1:  # 跨材料出现多个不同数值
            spread = ", ".join(f"{v}@{loc[0][0]}" for v, loc in seen_vals.items())
            first = obs[0]
            findings.append(_finding(
                "METRIC_VALUE", "error", first[1], first[2], first[3],
                f"{method} 的 {canon} 在不同材料数值不一致：{spread}",
                f"以 db09 权威值 {auth:.{dec}f} 为准，逐处统一"))
    return findings


# ---------------------------------------------------------------------------
# 检测 4：覆盖缺口 (COVERAGE_GAP) —— 规范术语/指标只在部分材料出现
# ---------------------------------------------------------------------------
def audit_coverage(materials, db09):
    findings = []
    # must_cover(贡献级)术语/指标缺席报 WARN；普通术语缺席降 INFO(X-4 降噪)
    targets = [("术语", t["canonical"], t.get("aliases", []), t.get("case_lock", False),
                bool(t.get("must_cover", False)))
               for t in db09["glossary"]]
    targets += [("指标", m["canonical"], m.get("aliases", []), False,
                 bool(m.get("must_cover", False)))
                for m in db09["metrics"]]
    mat_names = [m["name"] for m in materials]
    for kind, canon, aliases, cl, must in targets:
        present = []
        for mat in materials:
            text = "\n".join(mat["lines"])
            if any(_word_present(text, n, cl) for n in [canon] + aliases):
                present.append(mat["name"])
        if present and len(present) < len(mat_names):
            missing = [n for n in mat_names if n not in present]
            sev = "warn" if must else "info"
            tier = "贡献级(must_cover)" if must else "一般术语"
            findings.append(_finding(
                "COVERAGE_GAP", sev, missing[0], 0, "",
                f"{tier}{kind} '{canon}' 出现在 {present}，但在 {missing} 缺席",
                f"确认 {missing} 是否应包含 '{canon}'；若应包含则补齐措辞"))
    return findings


# ---------------------------------------------------------------------------
# 检测 5：创新点/贡献提法漂移 (CONTRIBUTION_DRIFT) —— X-5
#   背景：db09 terminology.md 已有"创新点1/2/3"行(只读，由 a02 维护)，是 3 条贡献的
#   单一事实源。SKILL 反复承诺"创新点跨论文/PPT/软著一字对齐"却零脚本实现——本检测补缺。
#   做法：对每条创新点 canonical，抽关键 token；在每份材料里找"覆盖足够 token 的行"
#   (认定该材料在表述此贡献)，再用句级 Jaccard 相似度判断提法是否偏离 canonical。
# ---------------------------------------------------------------------------
# 中文停用词 + 标点，降低 token 噪声
_STOP = set("的了与和及对在为是用做以并把被让使其之于而且或等这那一二三四五六"
            "七八九十个项条点级与都也很更最就还把对从向到上下里中外前后左右")
_TOKEN_SPLIT = re.compile(r"[\s，。、；：（）()【】\[\]\"“”‘’,.;:!?！？/\\|—\-_+=<>]+")


def _tokens(text):
    """中英混合分词:ASCII 词整体保留(小写)，中文按二元/一元切，去停用词与短噪声。"""
    toks = set()
    for seg in _TOKEN_SPLIT.split(text):
        if not seg:
            continue
        if re.fullmatch(r"[\x00-\x7f]+", seg):  # 纯 ASCII 词
            s = seg.lower()
            if len(s) >= 2 and s not in _STOP:
                toks.add(s)
            continue
        # 含中文:逐字 + 相邻二元(二元更能锁定术语，如"级联""传播")
        chars = [c for c in seg if c.strip()]
        for c in chars:
            if c not in _STOP and not re.match(r"[\x00-\x7f]", c):
                toks.add(c)
        for a, b in zip(chars, chars[1:]):
            bg = a + b
            if a not in _STOP and b not in _STOP:
                toks.add(bg)
    return toks


def _jaccard(a, b):
    if not a or not b:
        return 0.0
    inter = len(a & b)
    uni = len(a | b)
    return inter / uni if uni else 0.0


def audit_contribution(materials, db09):
    """创新点提法漂移检测。db09["contributions"] = [{id, canonical}]。

    每条贡献:
      - 抽 canonical 关键 token(实词)；
      - 对每份材料逐行算"覆盖率"=行 token∩贡献 token / 贡献 token；
        取覆盖率最高的行作为该材料对此贡献的"代表句"；
      - 覆盖率 >= ADDR_MIN 视为该材料在表述此贡献；
      - 代表句与 canonical 的 Jaccard < DRIFT_SIM -> 提法偏离，报 CONTRIBUTION_DRIFT。
    """
    findings = []
    contribs = db09.get("contributions", [])
    for c in contribs:
        canon = c.get("canonical", "")
        ctoks = _tokens(canon)
        if not ctoks:
            continue
        for mat in materials:
            best = (0.0, 0, "", 0.0)  # (coverage, line_no, line, sim)
            for i, line in enumerate(mat["lines"], 1):
                ltoks = _tokens(line)
                if not ltoks:
                    continue
                cover = len(ltoks & ctoks) / len(ctoks)
                if cover > best[0]:
                    best = (cover, i, line, _jaccard(ltoks, ctoks))
            cover, ln, line, sim = best
            if cover >= ADDR_MIN and sim < DRIFT_SIM:
                findings.append(_finding(
                    "CONTRIBUTION_DRIFT", "warn", mat["name"], ln, line,
                    f"贡献 '{c.get('id', '?')}' 在此处提法偏离 db09 标准措辞"
                    f"(覆盖 {cover*100:.0f}% / 相似 {sim*100:.0f}%)：标准为「{canon}」",
                    f"按 db09 创新点统一措辞改写，使 {mat['name']} 与论文/软著一字对齐"))
    return findings


def run_audit(materials, db09):
    findings = []
    findings += audit_substitution(materials, db09)
    findings += audit_metric_name(materials, db09)
    gross, observed = audit_metric_value(materials, db09)
    findings += gross  # GROSS_MISMATCH(X-2)：超阈值单列告警，不再静默丢弃
    findings += evaluate_value_conflicts(observed)
    findings += audit_coverage(materials, db09)
    findings += audit_contribution(materials, db09)  # CONTRIBUTION_DRIFT(X-5)
    # 去重：同一(类型,位置,问题)只保留一条(如 DCANet 同时命中术语表与方法锁)。
    seen, deduped = set(), []
    for f in findings:
        key = (f["kind"], f["location"], f.get("suggestion"), f["detail"]
               if f["kind"] != "SUBSTITUTION" else f.get("suggestion"))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(f)
    findings = deduped
    order = {"error": 0, "warn": 1, "info": 2}
    findings.sort(key=lambda f: (order.get(f["severity"], 9), f["kind"], f["location"]))
    return findings


def render_report(findings, materials):
    out = []
    out.append("=" * 64)
    out.append("跨材料一致性审计报告 (light-consistency)")
    out.append(f"材料数：{len(materials)}　发现总数：{len(findings)}")
    out.append("=" * 64)
    by_kind = {}
    for f in findings:
        by_kind.setdefault(f["kind"], []).append(f)
    labels = {"SUBSTITUTION": "受控术语/方法名替换", "METRIC_NAME": "指标换名",
              "METRIC_VALUE": "指标数值冲突", "GROSS_MISMATCH": "指标数值严重偏离",
              "COVERAGE_GAP": "覆盖缺口", "CONTRIBUTION_DRIFT": "创新点提法漂移"}
    n = 0
    for kind in ["SUBSTITUTION", "METRIC_NAME", "METRIC_VALUE", "GROSS_MISMATCH",
                 "CONTRIBUTION_DRIFT", "COVERAGE_GAP"]:
        items = by_kind.get(kind, [])
        out.append(f"\n## [{kind}] {labels[kind]}　({len(items)} 条)")
        if not items:
            out.append("  （无）")
        for f in items:
            n += 1
            tag = {"error": "ERROR", "warn": "WARN ", "info": "INFO "}.get(f["severity"], "WARN ")
            loc = f["location"] if not f["location"].endswith(":0") else f["location"][:-2] + ":(全篇)"
            out.append(f"  {n:>3}. [{tag}] {loc}")
            out.append(f"       现状：{f['line'] or '(跨材料/全篇)'}")
            out.append(f"       问题：{f['detail']}")
            out.append(f"       建议：{f['suggestion']}")
    out.append("\n" + "=" * 64)
    out.append(f"完整性自检：累计输出 {n} 条 == 发现总数 {len(findings)} -> "
               + ("通过" if n == len(findings) else "不一致(请检查)"))
    out.append("=" * 64)
    return "\n".join(out)


# ---------------------------------------------------------------------------
# 合成自测：无参数运行时，用内置 db09 + 内置材料跑一遍，验证全部检测类型都能命中
# ---------------------------------------------------------------------------
SYNTH_DB09 = {
    "glossary": [
        # forbidden 混用 字符串 与 dict 形式(X-1)：dict{text} 也须生效
        {"id": "t1", "canonical": "DCA-Net",
         "forbidden": ["DCANet", {"text": "DCA网络"}], "case_lock": True,
         "must_cover": False},
        {"id": "t2", "canonical": "fine-tune", "forbidden": ["finetune"],
         "case_lock": True, "must_cover": True},  # must_cover -> 缺席报 WARN(X-4)
    ],
    "methods": [
        # placeholder:true 项须被跳过(X-1)，否则"本文方法"会误命中正文；
        # 真实禁用写法"我们的网络"仍须生效。
        {"id": "m1", "canonical": "DCA-Net",
         "forbidden": ["我们的网络",
                       {"text": "本文方法(在正式名出现后仍这么写)", "placeholder": True}]},
    ],
    "metrics": [
        {"id": "f1", "canonical": "F1", "aliases": ["F1-score"],
         "confusable": ["准确率"], "unit": "%", "decimals": 1, "higher_is_better": True,
         "records": [{"method": "DCA-Net", "dataset": "D", "value": 87.6}]},
    ],
    # 创新点单一事实源(X-5)：取自 db09 terminology.md 的"创新点N"行(此处为合成等价物)
    "contributions": [
        {"id": "创新点1",
         "canonical": "级联误差传播抑制：检测跟踪行为四级流水线的不确定性传播建模"},
    ],
}
SYNTH_MATERIALS = [
    {"name": "paper.txt", "lines": [
        "我们提出 DCA-Net 用于检测。",
        "DCA-Net 的 F1 达到 87.6%。",
        "训练阶段对骨干网络做 fine-tune。",
        "本文的级联误差传播抑制对检测跟踪行为四级流水线的不确定性传播建模。",
    ]},
    {"name": "ppt.txt", "lines": [
        "本页介绍 DCANet 架构。",                 # SUBSTITUTION: DCANet
        "DCA-Net 的 F1 为 85.2%。",                # METRIC_VALUE: 与权威 87.6 冲突(小偏差)
        "我们的网络准确率 85.2% 领先。",            # SUBSTITUTION(我们的网络)+METRIC_NAME(准确率)
        "采用 finetune 策略。",                    # SUBSTITUTION: finetune
        "DCA-Net 的 F1 是 50.0%。",                # GROSS_MISMATCH: 偏差 43% (X-2)
        "DCA-Net 的 F1 写作 0.876。",              # 单位归一化后==87.6，不应误报(X-2)
        "这里做了流水线的误差处理。",               # 覆盖不足，不应误报为漂移
        "本页讲多级流水线误差传播的处理思路与系统稳健性提升方案。",  # CONTRIBUTION_DRIFT(X-5)
    ]},
    # fine-tune(must_cover) 仅出现在 paper -> COVERAGE_GAP/WARN
]


def selftest():
    print(">>> 无参数：运行内置合成自测\n")
    findings = run_audit(SYNTH_MATERIALS, SYNTH_DB09)
    print(render_report(findings, SYNTH_MATERIALS))
    kinds = {f["kind"] for f in findings}
    expect = {"SUBSTITUTION", "METRIC_NAME", "METRIC_VALUE",
              "GROSS_MISMATCH", "CONTRIBUTION_DRIFT", "COVERAGE_GAP"}
    missing = expect - kinds
    ok = not missing
    checks = []
    # X-1: dict 形式禁用写法生效(DCA网络 不在材料里，改测"我们的网络"已被 SUBSTITUTION 覆盖)；
    #      placeholder 跳过 = 没有任何 detail 含"本文方法"的误报
    no_placeholder = not any("本文方法" in f["detail"] for f in findings)
    checks.append(("X-1 placeholder 占位被跳过", no_placeholder))
    # X-2: GROSS_MISMATCH 恰好命中 50.0 那行，且 0.876 行未被误报
    gm = [f for f in findings if f["kind"] == "GROSS_MISMATCH"]
    gm_ok = len(gm) == 1 and "50" in gm[0]["line"]
    norm_ok = not any("0.876" in f["line"] for f in findings)
    checks.append(("X-2 GROSS_MISMATCH 单列且未静默丢弃", gm_ok))
    checks.append(("X-2 单位归一化 0.876==87.6 不误报", norm_ok))
    # X-4: 普通术语降 INFO；must_cover(fine-tune)缺席报 WARN
    cov = [f for f in findings if f["kind"] == "COVERAGE_GAP"]
    cov_warn = any(f["severity"] == "warn" and "fine-tune" in f["detail"] for f in cov)
    checks.append(("X-4 must_cover 缺席报 WARN", cov_warn))
    # X-5: 创新点漂移命中 ppt 的偏离句
    drift = [f for f in findings if f["kind"] == "CONTRIBUTION_DRIFT"]
    drift_ok = any(f["location"].startswith("ppt.txt") for f in drift)
    checks.append(("X-5 创新点漂移命中 PPT 偏离句", drift_ok))

    print("\n[自测断言] 全部检测类型均触发：",
          "通过" if ok else f"缺失 {missing}")
    for name, passed in checks:
        print(f"  - {name}：{'通过' if passed else '失败'}")
        ok = ok and passed
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="跨材料一致性审计器")
    ap.add_argument("--db09", help="db09 源:含三份 yaml 的目录,或真实项目的 terminology.md(Markdown 表)")
    ap.add_argument("--materials", nargs="*", help="材料文本文件(支持 glob)")
    ap.add_argument("--json", help="同时把发现写入该 JSON 文件")
    ap.add_argument("--selftest", action="store_true", help="run built-in offline synthetic self-test")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    if not args.db09 or not args.materials:
        return selftest()

    db09 = load_db09_auto(args.db09)
    paths = []
    for pat in args.materials:
        paths += glob.glob(pat) or [pat]
    materials = [read_material(p) for p in paths if os.path.isfile(p)]
    if not materials:
        sys.stderr.write("未找到任何材料文件\n"); return 2

    findings = run_audit(materials, db09)
    print(render_report(findings, materials))
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(findings, f, ensure_ascii=False, indent=2)
        print(f"\n[已写出 JSON] {args.json}")
    errors = sum(1 for f in findings if f["severity"] == "error")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
