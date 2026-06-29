# 复现清单 checklist：{{项目/课题名称}}

逐项勾选，给出具体配置而非工具名。`[ ]` 未完成 / `[x]` 已完成。

## 环境
- [ ] OS / 驱动 / CUDA 版本已记录：{{填写}}
- [ ] 依赖锁版本（requirements.txt 固定版本 / environment.yml / lockfile）：{{文件路径}}

## 目录脚手架
- [ ] 目录布局已生成 —— **调用 a06 `scaffold.py` 或 `ccds` 生成**（Cookiecutter Data Science 布局），本清单不重复造脚手架
- [ ] raw 数据只读不改：{{确认}}
- [ ] 可复用逻辑下沉到 `src/`，notebook 不放核心逻辑：{{确认}}

## 配置管理
- [ ] Hydra 分层配置（conf/ 下 model、dataset 分组 + defaults 列表）：{{conf 路径}}
- [ ] 命令行可覆盖（如 `lr=0.1`），run 自动存最终合成配置：{{确认}}

## 数据 / 模型版本
- [ ] DVC 跟踪大文件（`dvc add`，git 只存 .dvc 指针）：{{确认}}
- [ ] `dvc.yaml` 定义 stages（cmd/deps/params/outs/metrics）：{{确认}}
- [ ] `dvc.lock` 锁哈希，`dvc repro` 可增量复现：{{确认}}

## 流水线
- [ ] Snakemake rule（input/output/params/wildcards）自动推 DAG：{{Snakefile 路径}}
- [ ] 每个 rule 用 `conda:` / `container:` 锁环境：{{确认}}

## 实验日志
- [ ] MLflow（set_experiment→start_run→log_param/log_metric/log_artifact）或 W&B（init→log，Artifacts 管血缘）：{{选型}}
- [ ] 敏感数据用 offline 模式避免外发：{{确认}}

## 固定项
- [ ] 随机种子已固定（≥3~5 个）：{{种子列表}}
- [ ] 数据划分已固定：{{划分记录}}
- [ ] 超参 / 训练策略已记录：{{配置链接}}
- [ ] 结果文件命名规范已定义：{{规范}}
- [ ] 运行命令已记录（可一键复现）：{{命令}}
