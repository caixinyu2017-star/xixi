# db03 方法卡模板与 canonical 索引

> 本文件保留 db03 的 method_card 模板，并记录早期 seed 卡迁移后的 canonical 位置。为避免重复卡片，真实方法卡不再写在本文件中；新增/维护请放入对应领域文件。

## 卡片模板
```yaml
- method_name:
  task_type:
  input_data:
  output_result:
  core_assumption:
  advantages:
  limitations:
  common_baselines:
  evaluation_metrics:
  suitable_datasets:
  implementation_repo:
  representative_papers:
  possible_innovation_points:
  maturity:        # 经典|主流|新兴|过时|不推荐
```

## Canonical 索引（原 seed 已迁移）

| 原 seed 方法 | canonical 文件 | 说明 |
|---|---|---|
| Transformer / 自注意力 | [cards_dl.md](cards_dl.md) | 深度学习/NLP/CV 通用骨干，含 OpenAlex 核验代表作说明 |
| 随机森林 | [cards_ml_stats.md](cards_ml_stats.md) | 机器学习/统计学习完整卡，含特征重要性、OOB、代表论文 |
| 梯度提升树(XGBoost/LightGBM) | [cards_ml_stats.md](cards_ml_stats.md) | GBDT/XGBoost/LightGBM/CatBoost 完整卡 |
| 扩散模型(Diffusion) | [cards_dl.md](cards_dl.md) | DDPM / Latent Diffusion 完整卡 |
| 普通 GAN(原始) | [cards_dl.md](cards_dl.md) | GAN 作为经典/部分过时生成模型基线收录 |

## 待补充
按用户具体领域补充 method_card，并定期复核 maturity。新增卡片必须放入领域文件，避免本模板文件重新产生重复 method_name。
