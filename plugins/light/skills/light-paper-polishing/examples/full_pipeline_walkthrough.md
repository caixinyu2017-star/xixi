# 完整 before/after 范例（一段引言走完四步流水线）

> 演示从原始段落 → 跑脚本 → 逐条修改 → 终稿。这是 m08 paper-polishing 输出的标准样子。
> 四步流水线 distill→critique→polish→audit 见 SKILL.md；脚本 `scripts/mechanical_check.py`（离线）+ `scripts/polish.py`（LanguageTool）。

## 原始段落（before）
> In this paper, we study the problem of image segmentation. It is worth noting that segmentation is very important. Our novel method significantly outperforms existing approaches. The model was trained on a dataset and was evaluated on benchmarks and was compared with baselines. This may possibly suggest that our approach is state-of-the-art.

**step distill**：核心贡献 = 一个分割方法 + 它比 baseline 强。但全段没有一个可度量数字，贡献句被夸大词淹没。

**step critique（跑 `mechanical_check.py`）**：命中 `ai_tone: It is worth noting`、`overclaim: very/novel/significantly/outperforms/state-of-the-art`、`passive_overuse`（"was trained…was evaluated…was compared" 三连被动）、`hedge_stacking: may possibly suggest`。

**step polish（跑 `polish.py`，LanguageTool HTTP 200）**：补语法/冠词/标点；连同上面的裸论断逐条改。

## 四栏修改记录（节选）
- **原句**：It is worth noting that segmentation is very important.
  - **问题诊断**：`ai_tone` 填充开头 + `overclaim: very`，零信息。
  - **修改后**：（删除整句，把"为什么重要"并入下一句的痛点。）
  - **为什么更好**：审稿人把 "it is worth noting" 读作 AI 腔；重要性应由具体痛点而非形容词承担。
- **原句**：Our novel method significantly outperforms existing approaches.
  - **问题诊断**：`overclaim: novel/significantly/outperforms` + baseline 含糊 + 无数字（裸论断）。
  - **修改后**：On Cityscapes, our method raises mIoU by 2.1 points over DeepLabv3+ (80.4 vs. 78.3).
  - **为什么更好**：夸大词换成可度量增益 + 具体 baseline + 数据集，论断从"可质疑"变"可复现"。
- **原句**：The model was trained on a dataset and was evaluated on benchmarks and was compared with baselines.
  - **问题诊断**：`passive_overuse` 三连被动 + "a dataset/benchmarks" 含糊。
  - **修改后**：We train the model on Cityscapes and evaluate it on Cityscapes and ADE20K against four baselines.
  - **为什么更好**：主动语态 + 具名数据集与 baseline 数量，信息密度上升、可复现。
- **原句**：This may possibly suggest that our approach is state-of-the-art.
  - **问题诊断**：`hedge_stacking: may possibly suggest` 同时又 `overclaim: state-of-the-art`，自相矛盾。
  - **修改后**：These gains hold across two datasets, indicating the approach generalizes beyond a single benchmark.
  - **为什么更好**：去掉三连 hedge 与空泛 SOTA，给出有边界的、可被验证的结论。

## 终稿（after）
> We study image segmentation under domain shift, where models trained on one city degrade on another. We propose a method that aligns feature norms across domains. On Cityscapes, it raises mIoU by 2.1 points over DeepLabv3+ (80.4 vs. 78.3). We train on Cityscapes and evaluate on Cityscapes and ADE20K against four baselines. These gains hold across two datasets, indicating the approach generalizes beyond a single benchmark.

> after 段：0 个 overclaim / ai_tone / hedge 命中，被动比降到阈值下，贡献句可度量、可原样复用到 abstract 与 conclusion（三处一致）。
