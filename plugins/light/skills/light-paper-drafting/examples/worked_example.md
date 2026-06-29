# Worked Example：从 brief 到节级初稿（含 [MATERIAL GAP] 前后对照）

本例端到端走一遍论文初稿流程，演示 brief → 大纲 → 论证图 → 某节初稿（含真实的"前/后"对照）。
主题为**合成虚构示例**（不对应任何真实论文/数据），用于演示方法，所有"数字"均标注为占位或合成。

---

## 0. 输入 brief（用户给的或从 m03/m05/m06 抽取）

- 题目方向：长尾图像分类中，重加权采样 vs 表征解耦哪个更稳。
- 结构类型：会议论文（CVPR 风格，模板 06_conference.md）。
- 创新点(m03/m04)：提出一个"两阶段：先解耦表征再轻量重采样"的组合，声称比单一策略在极端长尾下更稳。
- 结果与亮点(m06)：在合成长尾 CIFAR 上，尾部类准确率相对单一重采样基线有提升（**具体数字待实验补**）。
- 目标 venue 风格(db01/db02)：CVPR，双盲，正文 8 页。

---

## 1. Paper Configuration Record

| 字段 | 值 |
|---|---|
| 结构类型 | 会议论文（IMRaD 变体） |
| 目标 venue | CVPR（当年模板，双盲，正文 8 页 + 无限附录） |
| 引用格式 | IEEE |
| reporting 指南 | 无人体/动物 → 不触发 CONSORT/STROBE；遵 venue 的 Repro/Ethics 声明 |
| 必备声明 | Limitations、Repro Statement、AI Use Disclosure、Code Availability |

---

## 2. 贡献清单（pillar）

- **C1**：提出两阶段框架 DR2（Decoupled-Representation + Re-sampling），将表征学习与分类器再平衡分离。
- **C2**：给出何时重采样有害的经验判据（解耦后再采样才稳）。
- **C3**：在合成长尾基准上验证，尾部类提升、头部类不退化（**数字待补**）。

---

## 3. 大纲（节序 + 每节 brief + 字数）

| 节 | brief（要论证什么 / 用哪些证据 / 对标谁） | 字数/页 |
|---|---|---|
| Abstract | 长尾问题→单策略不稳→DR2→主结果一句话 | 150–200 词 |
| 1 Intro | 长尾普遍且重要 → 重采样会损头部表征(gap, 需引用佐证) → DR2 思想 → C1–C3 → teaser | ~1 页 |
| 2 Related | 两类：重加权/重采样类、解耦表征类；各点差异 | ~0.75 页 |
| 3 Method | 阶段一解耦表征、阶段二轻量重采样；架构图 F2 | ~2 页 |
| 4 Exp | setup(合成长尾CIFAR/baseline/指标) → 主表 T1 → 消融 T2 | ~2 页 |
| 5 Conclusion | 呼应 C1–C3 | ~0.25 页 |
| Limitations/Repro/AI | 必备声明 | 附录区 |

---

## 4. 论证图（Argument Map：论点→证据→反驳→回应）

```
主张(C1+C2): 解耦后再轻量重采样，比单一重采样在极端长尾下更稳
  ├─ 证据 E1: 单一重采样过采尾部 → 头部表征被稀释 [需引用经典长尾文献佐证]
  ├─ 证据 E2: 解耦把表征学习与分类器再平衡分开 → 表征不受采样扰动 [需引用解耦类工作]
  ├─ 证据 E3: 合成长尾实验，DR2 尾部↑且头部不退 [实验数据，待补]
  ├─ 反驳 R1(Devil's Advocate): "解耦本身已够，重采样是多余的"
  │     回应: 消融 T2 显示去掉阶段二后尾部类掉 X 点 [待补，若不成立则撤回 C1 的"组合"卖点]
  └─ 反驳 R2: "提升来自调参不是方法"
        回应: 固定预算公平对比 + 多随机种子报均值±std [setup 需写清]
```
注：R1 是让步阈值 ≥4 的硬反驳——若消融数据不支持"组合优于单解耦"，必须改写贡献而非硬撑（anti-sycophancy）。

---

## 5. 节级初稿：Introduction（前/后对照）

### 5A. 「前」——错误示范（看不见的幻觉，红线全踩）

> Long-tailed recognition is a long-standing challenge. **Prior work [Zhang 2019] showed re-sampling degrades head accuracy by 12.3%**, while decoupling **improves tail accuracy to 81.4% on ImageNet-LT**. Our DR2 **outperforms all baselines by 5–8% across every benchmark**, achieving a new state of the art.

问题诊断（对照 references/self_review_checklist.md 的失败模式）：
- M2 幻觉引用："[Zhang 2019]" 是凭印象写的，未核 DOI/出处。
- M3 幻觉结果："12.3%""81.4%" 是没做过的实验/没核过的他人数字，凭语感填的。
- M3+夸大："outperforms all baselines by 5–8% across every benchmark" 实验还没跑，结论已写死。
- 违反 anti-leakage：没有来源支撑却写成了确定句。

### 5B. 「后」——合规初稿（缺口显式标记，不凭空填充）

> Long-tailed class distributions are pervasive in real-world recognition datasets `[MATERIAL GAP: 需 1–2 篇长尾普遍性引用，候选 Liu et al. ImageNet-LT；落笔前 curl Crossref 核 DOI]`. A common remedy is re-sampling minority classes, but doing so can distort the feature representation learned on head classes `[MATERIAL GAP: 需经典证据支撑此 gap，核对原文确为此结论再引]`.
>
> We argue that **decoupling representation learning from classifier re-balancing** mitigates this distortion (C1). Building on this, we introduce **DR2**, a two-stage framework: stage one learns representations without resampling; stage two applies lightweight re-sampling only to the classifier.
>
> Our contributions: **(C1)** the DR2 framework; **(C2)** an empirical criterion for when re-sampling helps; **(C3)** experiments on synthetic long-tailed CIFAR showing tail-class accuracy improves by `[RESULT GAP: 待实验，填 Δ±std 与 p 值]` without head-class degradation.

为何「后」是对的：
- 每个未经核实的事实点都被 `[MATERIAL GAP]` / `[RESULT GAP]` 显式隔离，绝不伪装成确定句。
- 贡献句与 pillar C1–C3 一一对应。
- 结果留空待真实验填，杜绝 M3。
- gap 标注里写明了下一步动作（curl 核 DOI / 跑实验填数字），可被 m10/m05 接手。

---

## 6. 自检与诚信门快照（节选，详见 references/）

- claim 抽样：本节 8 条事实性 claim，初稿阶段抽 3 条（≥30%）核源 → 2 条标 GAP、1 条待核。
- 8 维自评：清晰度✓、与已有工作定位 △（Related 还没写差异）、可复现性 △（setup 未定 seed）。
- 失败模式排查：M2/M3 已通过 GAP 标记拦截；M7 frame-lock 风险——DR2 的"组合"卖点取决于消融，已在论证图标注撤回条件。

→ 进入 m05 补实验、m10 核引用后，再回填所有 GAP，方可进 4.5 终审诚信门（100% claim 核查）。
