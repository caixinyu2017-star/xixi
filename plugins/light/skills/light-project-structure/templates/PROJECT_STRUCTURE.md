# 科研项目标准目录结构说明

> 配套模板：本目录 `scaffold.py`（一键生成）、`README.template.md`、`PROJECT_PLAN.template.md`、`python-research.gitignore`、`CHANGELOG.template.md`、`editorconfig.template`。
> 数据分层与 notebooks 命名沿用 Cookiecutter Data Science（CCDS）；详见同技能 references.md。

## 完整骨架

```
project-name/
├── data/                  数据（大文件走 DVC，勿直接 git 跟踪）
│   ├── raw/               原始不可变数据
│   ├── interim/           中间转换结果
│   ├── processed/         建模用最终数据集
│   └── external/          第三方/外部源
├── src/                   源代码（或命名为模块包 <module_name>/）
├── models/                模型权重与定义（大二进制走 DVC）
├── experiments/           实验脚本与配置，按编号：exp_001_baseline/
├── results/               实验结果（指标、输出），文件名映射实验编号
├── figures/               论文/报告用图
├── notebooks/             探索性分析
│   ├── exploratory/       草稿 notebook，命名"编号-缩写-描述"如 1.0-jl-eda.ipynb
│   └── reports/           定稿、可重跑、产出对外图表的 notebook
├── configs/               配置（Hydra yaml 等）
├── logs/                  运行日志（MLflow/W&B 本地）
├── references/            文献库（Zotero 导出 / .bib）
├── docs/                  项目文档（MkDocs/Sphinx）
├── paper/                 论文工程（LaTeX/Word）
├── ppt/                   演示文稿
├── patent/                专利材料
├── software-copyright/    软著材料
├── assets/                图标/模板/素材
├── tests/                 单元/集成测试（pytest）
├── .light/                编排台账与会话衔接（纳入版本控制，勿忽略）
│   ├── passport.yaml      产物台账（orchestrator 维护，跨阶段续跑真相源）
│   └── handoff/           会话衔接卡 S<NN>-<slug>.md（CONVENTIONS §9 主动交接）
├── README.md              项目说明（用 README.template.md）
├── CHANGELOG.md           变更记录（用 CHANGELOG.template.md）
├── PROJECT_PLAN.md        实现计划（用 PROJECT_PLAN.template.md）
├── .gitignore             用 python-research.gitignore
├── .editorconfig          用 editorconfig.template
└── pyproject.toml         依赖与工具配置（uv/Ruff）
```

## 命名规范

- 目录/文件用小写 + 连字符或下划线，不用空格、不用中文。
- 实验/版本带日期或序号：`exp_004_ablation`、`paper_v3`、`fig3_ablation_v2`。
- 数据文件含版本/划分标记；结果文件名映射到实验编号，可追溯。
- notebooks：`<编号>-<作者缩写>-<描述>`，如 `1.0-jl-initial-exploration.ipynb`。

## 与项目库（db09）对应

| 目录 | project_card 字段 |
|------|-------------------|
| src/ | code_status |
| data/ | data_status |
| paper/ | paper_status |
| experiments/ | exp_status |

便于 a02 跟踪进度。

## 快速生成

```bash
# 方式一（推荐）：本目录 scaffold.py 一条命令建全树 + 拷模板 + 可选 dvc/uv|poetry
python scaffold.py ./my-proj --name my-proj --dvc

# 方式二：CCDS 脚手架（交互式选依赖管理/lint/存储/测试/文档）
pipx install cookiecutter-data-science
ccds

# 方式三：按上面骨架手工建目录后，复制本目录模板文件到项目根
```

## 与 CCDS 的差异（取舍说明）

CCDS 把图放 `reports/figures/`、源码放顶层模块包；本规范用 `figures/` 与 `src/`，
并额外增设 `paper/ ppt/ patent/ software-copyright/` 等科研/知识产权目录。对齐时按团队习惯取舍。
