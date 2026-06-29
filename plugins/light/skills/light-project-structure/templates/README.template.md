<!-- README 模板 — 科研项目通用。复制为项目根目录 README.md，按需填充 {{占位符}} 。 -->

# {{项目名称}}

> 一句话描述：本项目做什么、解决什么问题。
> 关联论文/软著/专利：{{标题或编号，无则写"待定"}}

## 状态

| 维度 | 状态 | 说明 |
|------|------|------|
| 代码 code | planning / in-progress / done | 对应 src/ |
| 数据 data | planning / in-progress / done | 对应 data/ |
| 实验 experiments | planning / in-progress / done | 对应 experiments/ |
| 论文 paper | planning / drafting / submitted | 对应 paper/ |

（状态字段与项目库 db09 project_card 对应，便于 a02 跟踪。）

## 环境与安装

```bash
# 推荐用 uv（提交 uv.lock 保证团队/CI 一致）
uv sync
uv run python -m {{module_name}} --help
```

依赖锁定：应用项目提交 lock 文件（uv.lock；Poetry 备选则 poetry.lock）。Python 版本要求见 pyproject.toml 的 requires-python。

## 目录结构

详见同目录 `PROJECT_STRUCTURE.md`。核心约定：

- `data/{raw,interim,processed,external}/` — 数据分层（沿用 Cookiecutter Data Science）
- `src/` — 源代码
- `experiments/` — 按编号组织的实验脚本与配置
- `results/` `figures/` — 实验产物与论文用图
- `paper/` `ppt/` `patent/` `software-copyright/` — 写作与知识产权材料

## 数据

| 数据集 | 来源 | 版本 | 位置 | DVC |
|--------|------|------|------|-----|
| {{名称}} | {{来源/链接}} | {{版本}} | data/raw/ | 是/否 |

大文件用 DVC 管理：`dvc pull` 拉取（须先 `git pull`）。

## 快速复现

```bash
# 1. 拉数据
dvc pull
# 2. 跑管线（dvc.yaml 定义的多阶段）
dvc repro
# 3. 查看实验指标
dvc exp show
```

## 主要结果

| 实验编号 | 配置 | 关键指标 | 结果文件 |
|----------|------|----------|----------|
| exp_001  | {{配置}} | {{指标}} | results/exp_001/ |

## 引用

```bibtex
{{citation_key}}
```

## 许可

{{LICENSE，如 MIT / BSD-3-Clause}}
