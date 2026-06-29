#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""detect_stack.py — 读取项目清单文件，识别技术栈，给出工具/技能选型建议。

支持的清单：package.json / pyproject.toml(含 poetry 段) /
requirements.txt / environment.yml(.yaml) / Pipfile。

用法：
  python detect_stack.py <项目目录>      # 扫描真实项目
  python detect_stack.py --self-test     # 无数据时用合成清单自检
  python detect_stack.py <目录> --json   # 机器可读输出

设计：纯标准库（tomllib 3.11+）+ 可选 PyYAML（缺失则降级正则解析 yml）。
不臆造——只对“清单里真实出现的依赖”给建议，未命中标 'no signal'。
"""
import sys, os, json, re, argparse

sys.stdout.reconfigure(encoding="utf-8")

try:
    import tomllib  # py3.11+
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None

# 依赖名(规整后精确匹配) -> (类别, 选型建议)。suggest() 按 dep==key
# 或 dep==key 的连字符转下划线 变体精确相等命中，不做子串匹配。
RULES = {
    # ---- Python 数据 ----
    "pandas": ("数据处理", "中小数据(<2GB)主力；超内存切 polars/dask"),
    "polars": ("数据处理", "已选高性能 DataFrame，适合 1-50GB 单机"),
    "dask": ("数据处理", "已选超内存/并行；确认是否真需要分布式"),
    "duckdb": ("数据处理", "out-of-core SQL 直查 parquet/csv；超内存分析首选之一"),
    "vaex": ("数据处理", "⚠ vaex 2023 后停维护(已淘汰)；迁 DuckDB / polars streaming"),
    "pyspark": ("数据处理", "集群级；单机数据 <50GB 时 polars 更省心"),
    # ---- Python 科学/ML ----
    "numpy": ("科学计算", "数值基座，向量化优先于 Python 循环"),
    "scipy": ("科学计算", "统计/优化/信号；配 statsmodels 做推断统计"),
    "statsmodels": ("统计推断", "回归/检验/时序，要 p 值/置信区间选它"),
    "scikit-learn": ("机器学习", "经典 ML 主力；深度学习转 torch"),
    "sklearn": ("机器学习", "经典 ML 主力；深度学习转 torch"),
    "xgboost": ("机器学习", "梯度提升树；表格数据强基线，调参看 early_stopping"),
    "lightgbm": ("机器学习", "高效 GBDT；大表格/类别特征比 xgboost 更省内存"),
    "torch": ("深度学习", "PyTorch；GPU 训练考虑 Modal 云算力"),
    "pytorch": ("深度学习", "PyTorch(conda 包名)；GPU 训练考虑 Modal 云算力"),
    "torchvision": ("深度学习", "PyTorch 视觉数据集/模型/变换，配 torch 用"),
    "tensorflow": ("深度学习", "TF；环境用 conda 协调 CUDA"),
    "transformers": ("深度学习", "HF 模型；大模型推理可上 Modal/serverless"),
    "opencv-python": ("计算机视觉", "图像/视频处理；导入名 cv2，重计算可上 GPU/云"),
    # ---- LLM/API ----
    "openai": ("大模型API", "OpenAI SDK；密钥走环境变量/Secrets，勿硬编码"),
    "anthropic": ("大模型API", "Anthropic Claude SDK；密钥走环境变量/Secrets，勿硬编码"),
    "langchain": ("大模型编排", "LLM 应用编排/RAG；注意版本拆分(langchain-core 等)"),
    # ---- 绘图 ----
    "matplotlib": ("绘图", "投稿矢量图(pdf/svg)；演示用 png"),
    "seaborn": ("绘图", "统计图速成，底层 matplotlib"),
    "plotly": ("绘图", "交互图/HTML 报告；静态投稿仍用 matplotlib"),
    # ---- Python Web/后端 ----
    "fastapi": ("后端", "异步 API 首选；OpenAPI 自动生成便于确定性调用"),
    "django": ("后端", "全功能框架；ORM/admin/auth 齐全"),
    "flask": ("后端", "轻量 API；规模上来考虑 FastAPI 异步"),
    "uvicorn": ("后端", "ASGI 服务器，配 FastAPI"),
    "sqlalchemy": ("数据库", "ORM；参数化查询防注入"),
    "psycopg": ("数据库", "Postgres 驱动"),
    "redis": ("数据库", "缓存/队列"),
    # ---- 演示/原型 ----
    "gradio": ("演示界面", "ML 模型快速 Web demo；分享/评测原型首选"),
    "streamlit": ("演示界面", "数据应用/看板原型；纯 Python 交互页面"),
    # ---- 文档/排版 ----
    "python-docx": ("文档", "程序化生成 Word"),
    "python-pptx": ("PPT", "程序化生成 PPT；模板化幻灯片"),
    "openpyxl": ("文档", "读写 Excel xlsx"),
    "pylatex": ("排版", "Python 驱动 LaTeX；复杂排版直接写 .tex + latexmk"),
    # ---- 实验/版本管理 ----
    "mlflow": ("实验管理", "实验追踪/模型注册"),
    "wandb": ("实验管理", "W&B 实验可视化"),
    "dvc": ("数据版本", "大数据/模型版本化，配 Git"),
    "hydra-core": ("配置管理", "分层配置/多组实验扫描"),
    "snakemake": ("流水线", "可复现工作流编排"),
    # ---- 浏览器/抓取 ----
    "browser-use": ("浏览器自动化", "LLM 驱动 Playwright；偏 CLI/CDP 选 agent-browser"),
    "playwright": ("浏览器自动化", "底层自动化；AI 任务封装看 browser-use"),
    "scrapy": ("抓取", "大规模爬虫框架"),
    "requests": ("HTTP", "同步请求；有 OpenAPI 描述按 schema 确定性调用"),
    "httpx": ("HTTP", "异步/同步 HTTP，支持 HTTP/2"),
    # ---- JS/前端 ----
    "next": ("前端", "Next.js/React 全栈；配 shadcn/ui + Tailwind"),
    "react": ("前端", "组件库 shadcn/ui，图表 ECharts/D3"),
    "vue": ("前端", "Vue 生态；图表同样 ECharts"),
    "tailwindcss": ("前端", "原子化 CSS"),
    "echarts": ("前端", "数据可视化图表库"),
    "d3": ("前端", "底层可视化，自定义图形"),
    "vite": ("前端构建", "快速 dev server/打包"),
    "typescript": ("前端", "类型安全 JS；新项目默认开启"),
    "express": ("后端", "Node 轻量 API"),
    "jest": ("测试", "JS 单测"),
    "vitest": ("测试", "Vite 原生单测，比 jest 快"),
    "playwright-test": ("测试", "E2E 测试"),
    "pytest": ("测试", "Python 单测主力；配 pytest-cov 看覆盖率"),
    "ruff": ("代码质量", "Rust 写的极速 lint+format，替代 flake8/isort/black"),
    "black": ("代码质量", "格式化；新项目可用 ruff format 统一"),
    "mypy": ("代码质量", "静态类型检查"),
    "pre-commit": ("代码质量", "提交前钩子统一跑 lint/format/检查"),
    "great-expectations": ("数据质量", "数据校验/期望套件"),
    "ydata-profiling": ("数据质量", "一键数据画像报告"),
}

# 锁文件/配置文件存在性 -> 环境工具结论
ENV_HINTS = {
    "uv.lock": "检测到 uv.lock：用 `uv sync` 确定性安装，`uv run` 执行",
    "poetry.lock": "检测到 poetry.lock：延续 `poetry install`，勿混 pip/conda",
    "Pipfile.lock": "检测到 Pipfile.lock：pipenv 项目",
    "environment.yml": "检测到 conda 环境：`conda env create -f`，提速用 mamba",
    "environment.yaml": "检测到 conda 环境：`conda env create -f`，提速用 mamba",
    "Dockerfile": "检测到 Dockerfile：钉 FROM 版本 tag，依赖层在前源码在后",
    "package-lock.json": "npm 锁文件：`npm ci` 复现安装",
    "pnpm-lock.yaml": "pnpm 锁文件：`pnpm install --frozen-lockfile`",
    "yarn.lock": "yarn 锁文件：`yarn install --frozen-lockfile`",
}


def _norm(name):
    """规整依赖名：去版本/extras/空白，转小写。"""
    name = name.strip().lower()
    name = re.split(r"[<>=!~;\[\(@\s]", name, 1)[0]
    return name.strip()


def parse_package_json(path):
    deps = []
    try:
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
    except Exception as e:
        return deps, [f"package.json 解析失败: {e}"]
    for key in ("dependencies", "devDependencies", "peerDependencies"):
        for k in (d.get(key) or {}):
            deps.append(_norm(k))
    return deps, []


def parse_pyproject(path):
    deps, notes = [], []
    if tomllib is None:
        return deps, ["tomllib 不可用(需 Python 3.11+)，跳过 pyproject.toml"]
    try:
        with open(path, "rb") as f:
            d = tomllib.load(f)
    except Exception as e:
        return deps, [f"pyproject.toml 解析失败: {e}"]
    # PEP 621
    for item in (d.get("project", {}).get("dependencies") or []):
        deps.append(_norm(item))
    og = d.get("project", {}).get("optional-dependencies", {})
    for grp in og.values():
        for item in grp:
            deps.append(_norm(item))
    # Poetry
    poetry = d.get("tool", {}).get("poetry", {})
    for k in (poetry.get("dependencies") or {}):
        if k.lower() != "python":
            deps.append(_norm(k))
    return deps, notes


def parse_requirements(path):
    deps = []
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith(("#", "-")):
                    continue
                deps.append(_norm(line))
    except Exception as e:
        return deps, [f"requirements 解析失败: {e}"]
    return deps, []


def parse_environment_yml(path):
    """conda environment.yml：优先 PyYAML，缺失则正则降级。"""
    deps, notes = [], []
    try:
        text = open(path, encoding="utf-8").read()
    except Exception as e:
        return deps, [f"environment.yml 读取失败: {e}"]
    try:
        import yaml
        d = yaml.safe_load(text) or {}
        for item in (d.get("dependencies") or []):
            if isinstance(item, str):
                deps.append(_norm(item))
            elif isinstance(item, dict):  # pip: 子列表
                for sub in item.get("pip", []) or []:
                    deps.append(_norm(sub))
    except ModuleNotFoundError:
        notes.append("PyYAML 缺失，environment.yml 用正则降级解析")
        for line in text.splitlines():
            m = re.match(r"\s*-\s*([A-Za-z0-9_.\-]+)", line)
            if m:
                deps.append(_norm(m.group(1)))
    return deps, notes


def parse_pipfile(path):
    """Pipfile 本质是 TOML，读 [packages] 与 [dev-packages] 的键名。"""
    deps, notes = [], []
    if tomllib is None:
        return deps, ["tomllib 不可用(需 Python 3.11+)，跳过 Pipfile"]
    try:
        with open(path, "rb") as f:
            d = tomllib.load(f)
    except Exception as e:
        return deps, [f"Pipfile 解析失败: {e}"]
    for section in ("packages", "dev-packages"):
        for k in (d.get(section) or {}):
            if k.lower() != "python":
                deps.append(_norm(k))
    return deps, notes


MANIFESTS = {
    "package.json": parse_package_json,
    "pyproject.toml": parse_pyproject,
    "requirements.txt": parse_requirements,
    "environment.yml": parse_environment_yml,
    "environment.yaml": parse_environment_yml,
    "Pipfile": parse_pipfile,
}


def _detect_ci(project_dir):
    """探测 .github/workflows/*.yml(.yaml) 是否存在 → CI 已配置提示。"""
    wf_dir = os.path.join(project_dir, ".github", "workflows")
    if not os.path.isdir(wf_dir):
        return None
    try:
        wfs = [f for f in os.listdir(wf_dir)
               if f.endswith((".yml", ".yaml"))]
    except OSError:
        return None
    if not wfs:
        return None
    return (f"检测到 GitHub Actions({len(wfs)} 个 workflow: "
            f"{', '.join(sorted(wfs)[:5])}{' ...' if len(wfs) > 5 else ''})："
            "CI 已配置；事件触发/定时/matrix 复现走 Actions，本地数据依赖编排仍用 Snakemake/Make")


def _detect_lang_stacks(project_dir):
    """探测 SKILL 宣称但无依赖清单的科研语言栈：R/MATLAB/LaTeX/Jupyter。

    靠特征文件存在性 + 顶层扩展名扫描判断（与 MANIFESTS 一致的浅层扫描，
    确定性、不臆造）。返回结论字符串列表。
    """
    hits = []
    try:
        entries = os.listdir(project_dir)
    except OSError:
        entries = []
    names = set(entries)

    def _has_ext(ext):
        return any(e.lower().endswith(ext) for e in entries)

    # ---- R ----
    r_signals = []
    if "DESCRIPTION" in names:
        r_signals.append("DESCRIPTION")
    if "renv.lock" in names:
        r_signals.append("renv.lock")
    if _has_ext(".rproj"):
        r_signals.append(".Rproj")
    if r_signals:
        hits.append(f"检测到 R 项目({', '.join(r_signals)})："
                    "高级统计/混合模型/ggplot2 出图用 R；"
                    "依赖复现用 renv(`renv::restore()`)")
    # ---- MATLAB ----
    if _has_ext(".m"):
        hits.append("检测到 MATLAB 源码(.m)："
                    "信号/控制/数值/Simulink 场景用 MATLAB；"
                    "可复现脚本化运行、跨语言可经 conda 协调")
    # ---- LaTeX ----
    tex_signals = []
    if _has_ext(".tex"):
        tex_signals.append(".tex")
    if "latexmkrc" in names or ".latexmkrc" in names:
        tex_signals.append("latexmkrc")
    if tex_signals:
        hits.append(f"检测到 LaTeX 排版({', '.join(tex_signals)})："
                    "用 latexmk 一键编译(TinyTeX/TeX Live)，矢量 PDF 投稿")
    # ---- Jupyter ----
    if _has_ext(".ipynb"):
        hits.append("检测到 Jupyter Notebook(.ipynb)："
                    "探索/演示用；投稿/复现把稳定逻辑抽进 .py 脚本，配 nbconvert")
    return hits


def scan(project_dir):
    """扫描目录，返回 (deps集合, 命中清单文件, env提示, 解析备注)。"""
    deps, found_manifests, env_hits, notes = [], [], [], []
    for fname, parser in MANIFESTS.items():
        p = os.path.join(project_dir, fname)
        if os.path.isfile(p):
            d, n = parser(p)
            deps.extend(d)
            notes.extend(n)
            found_manifests.append(fname)
    for fname, hint in ENV_HINTS.items():
        if os.path.isfile(os.path.join(project_dir, fname)):
            env_hits.append(hint)
    ci = _detect_ci(project_dir)
    if ci:
        env_hits.append(ci)
    env_hits.extend(_detect_lang_stacks(project_dir))
    return sorted(set(deps)), found_manifests, env_hits, notes


def suggest(deps):
    """对命中规则的依赖给建议，按类别聚合。"""
    by_cat = {}
    matched = []
    for dep in deps:
        for key, (cat, advice) in RULES.items():
            if dep == key or dep == key.replace("-", "_"):
                by_cat.setdefault(cat, []).append((dep, advice))
                matched.append(dep)
                break
    return by_cat, matched


def build_report(project_dir):
    deps, manifests, env_hits, notes = scan(project_dir)
    by_cat, matched = suggest(deps)
    unmatched = [d for d in deps if d not in matched]
    return {
        "project_dir": os.path.abspath(project_dir),
        "manifests_found": manifests,
        "total_deps": len(deps),
        "matched": matched,
        "unmatched_no_signal": unmatched,
        "suggestions_by_category": {
            c: [{"dep": d, "advice": a} for d, a in v] for c, v in by_cat.items()
        },
        "env_recommendations": env_hits,
        "parse_notes": notes,
    }


def print_report(rep):
    print("=" * 60)
    print(f"技术栈检测报告  目录: {rep['project_dir']}")
    print("=" * 60)
    if not rep["manifests_found"]:
        if rep["env_recommendations"]:
            print("未发现依赖清单文件，但检测到以下语言栈/环境信号：")
            for h in rep["env_recommendations"]:
                print(f"  - {h}")
            return
        print("未发现任何清单文件 (package.json/pyproject.toml/requirements.txt/"
              "environment.yml/Pipfile)。无信号，无法建议。")
        return
    print(f"清单文件: {', '.join(rep['manifests_found'])}")
    print(f"依赖总数: {rep['total_deps']}  命中规则: {len(rep['matched'])}")
    print()
    if rep["env_recommendations"]:
        print("[环境/复现]")
        for h in rep["env_recommendations"]:
            print(f"  - {h}")
        print()
    if rep["suggestions_by_category"]:
        print("[工具选型建议]")
        for cat, items in sorted(rep["suggestions_by_category"].items()):
            print(f"  {cat}:")
            for it in items:
                print(f"    - {it['dep']}: {it['advice']}")
        print()
    if rep["unmatched_no_signal"]:
        u = rep["unmatched_no_signal"]
        print(f"[no signal] {len(u)} 个依赖无内置规则(不臆造建议): "
              f"{', '.join(u[:12])}{' ...' if len(u) > 12 else ''}")
        print()
    if rep["parse_notes"]:
        print("[解析备注]")
        for n in rep["parse_notes"]:
            print(f"  - {n}")


def self_test():
    """无数据时：在临时目录写合成清单，跑全流程并断言。"""
    import tempfile, shutil
    tmp = tempfile.mkdtemp(prefix="detect_stack_")
    try:
        # 合成一个 Python 数据科学 + conda 项目
        with open(os.path.join(tmp, "requirements.txt"), "w", encoding="utf-8") as f:
            f.write("pandas>=2.0\nscikit-learn==1.4.0\nmatplotlib\n"
                    "fastapi\nxgboost\nopencv-python\ngradio\n"
                    "some-private-internal-lib==9.9\n# comment\n")
        with open(os.path.join(tmp, "environment.yml"), "w", encoding="utf-8") as f:
            f.write("name: demo\nchannels:\n  - conda-forge\n"
                    "dependencies:\n  - numpy\n  - pytorch\n  - pip:\n"
                    "      - wandb\n")
        # 合成一个 JS 前端清单
        with open(os.path.join(tmp, "package.json"), "w", encoding="utf-8") as f:
            json.dump({"dependencies": {"next": "15", "react": "19",
                       "tailwindcss": "4"}, "devDependencies": {"vitest": "3"}}, f)
        open(os.path.join(tmp, "uv.lock"), "w").close()

        # 合成 GitHub Actions workflow
        wf_dir = os.path.join(tmp, ".github", "workflows")
        os.makedirs(wf_dir, exist_ok=True)
        with open(os.path.join(wf_dir, "ci.yml"), "w", encoding="utf-8") as f:
            f.write("name: ci\non: [push]\njobs:\n  test:\n"
                    "    runs-on: ubuntu-latest\n    steps:\n"
                    "      - uses: actions/checkout@v6\n")

        # 合成 SKILL 宣称的科研语言栈特征文件：R/MATLAB/LaTeX/Jupyter
        open(os.path.join(tmp, "DESCRIPTION"), "w").close()
        open(os.path.join(tmp, "renv.lock"), "w").close()
        open(os.path.join(tmp, "analysis.m"), "w").close()
        open(os.path.join(tmp, "paper.tex"), "w").close()
        open(os.path.join(tmp, "explore.ipynb"), "w").close()

        rep = build_report(tmp)
        print_report(rep)
        print("\n--- 自检断言 ---")
        checks = {
            "命中 pandas": "pandas" in rep["matched"],
            "命中 fastapi": "fastapi" in rep["matched"],
            "命中 next(JS)": "next" in rep["matched"],
            "命中 wandb(conda pip 子列表)": "wandb" in rep["matched"],
            "命中 xgboost(新增别名)": "xgboost" in rep["matched"],
            "命中 opencv-python(新增别名)": "opencv-python" in rep["matched"],
            "命中 gradio(新增别名)": "gradio" in rep["matched"],
            "私有库归入 no-signal": "some-private-internal-lib"
                in rep["unmatched_no_signal"],
            "识别 uv.lock 环境": any("uv.lock" in h
                for h in rep["env_recommendations"]),
            "识别 conda 环境": any("conda" in h
                for h in rep["env_recommendations"]),
            "识别 GitHub Actions CI": any("GitHub Actions" in h
                for h in rep["env_recommendations"]),
            "识别 R 项目(DESCRIPTION/renv.lock)": any("R 项目" in h
                for h in rep["env_recommendations"]),
            "识别 MATLAB(.m)": any("MATLAB" in h
                for h in rep["env_recommendations"]),
            "识别 LaTeX(.tex)": any("LaTeX" in h
                for h in rep["env_recommendations"]),
            "识别 Jupyter(.ipynb)": any("Jupyter" in h
                for h in rep["env_recommendations"]),
            "三个清单都解析到": set(rep["manifests_found"]) >=
                {"package.json", "requirements.txt", "environment.yml"},
        }
        ok = True
        for name, passed in checks.items():
            print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
            ok = ok and passed
        print(f"\n自检结果: {'全部通过' if ok else '存在失败'}")
        return 0 if ok else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser(description="检测项目技术栈并建议工具选型")
    ap.add_argument("project_dir", nargs="?", help="项目目录")
    ap.add_argument("--self-test", "--selftest", dest="self_test", action="store_true", help="合成清单自检")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    if args.self_test or not args.project_dir:
        if not args.project_dir:
            print("[未提供目录，运行自检 --self-test]\n")
        return self_test()

    if not os.path.isdir(args.project_dir):
        print(f"错误：目录不存在 {args.project_dir}", file=sys.stderr)
        return 2
    rep = build_report(args.project_dir)
    if args.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        print_report(rep)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
