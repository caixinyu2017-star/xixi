# db04 数据集卡模板与 canonical 索引

> 本文件保留 db04 的 dataset_card 模板，并记录早期 seed 卡迁移后的 canonical 位置。为避免重复卡片，真实数据集卡不再写在本文件中；新增/维护请放入对应领域文件。

## 卡片模板
```yaml
- dataset_name:
  domain:
  task:
  data_type:
  size:
  format:
  license:            # 含 商用?/再分发?/需授权?
  download_url:
  paper_url:
  citation:
  leaderboard_url:
  known_issues:
  bias_risk:
  privacy_risk:
  preprocessing_steps:
  recommended_splits:
```

## Canonical 索引（原 seed 已迁移）

| 原 seed 数据集 | canonical 文件 | 说明 |
|---|---|---|
| ImageNet (ILSVRC) | [cards_cv_nlp.md](cards_cv_nlp.md) | CV 图像分类/目标定位完整卡，含 license、OpenAlex、隐私风险 |
| MNIST | [cards_cv_nlp.md](cards_cv_nlp.md) | CV 教学基准完整卡，含 DOI/OpenAlex 与预处理说明 |
| GLUE | [cards_cv_nlp.md](cards_cv_nlp.md) | NLP 多任务基准完整卡，含逐子任务许可风险提醒 |
| UCI Adult (Census Income) | [cards_tabular_other.md](cards_tabular_other.md) | 表格/公平性基准完整卡，含 UCI DOI、CC BY 4.0 与敏感属性风险 |

## 待补充
按用户领域补充 dataset_card，重点核实 license、隐私、再分发与商用限制。新增卡片必须放入领域文件，避免本模板文件重新产生重复 dataset_name。
