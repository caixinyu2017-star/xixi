# R5-04 统计功效分析算例核验

- 核验日期：2026-06-11
- 工具：statsmodels 0.14.5（本机 Anaconda，Python 3.11）
- 目的：m05(light-research-plan) references「统计功效与样本量/种子数规划」节的算例数值，须与 statsmodels `TTestIndPower` 实跑一致并留痕（诚信纪律：功效算例数值禁凭记忆）。

## 实跑命令与输出

```python
from statsmodels.stats.power import TTestIndPower
a = TTestIndPower()
# 正向：给定效应量/功效/显著性，求每组最小样本量（双侧）
for d in (0.3, 0.5, 0.8):
    n = a.solve_power(effect_size=d, power=0.8, alpha=0.05, alternative='two-sided')
# 反查：给定每组样本量，求实际功效
for d, n in ((0.5, 5), (0.8, 30), (0.5, 64), (0.8, 26)):
    p = a.solve_power(effect_size=d, nobs1=n, alpha=0.05, alternative='two-sided')
```

实际输出（逐字粘贴，未修改）：

```
statsmodels 0.14.5
d=0.3 power=0.8 a=0.05 two-sided -> n/group = 175.3847  (向上取整 176)
d=0.5 power=0.8 a=0.05 two-sided -> n/group = 63.7656  (向上取整 64)
d=0.8 power=0.8 a=0.05 two-sided -> n/group = 25.5246  (向上取整 26)
---反查 power---
d=0.5 n=5  -> power=0.1077
d=0.8 n=30 -> power=0.8614
d=0.5 n=64 -> power=0.8015
d=0.8 n=26 -> power=0.8075
```

## 写进 m05 的数值（均来自上面实跑）

| 场景 | 效应量 Cohen's d | power=0.8, α=0.05 双侧 → 每组最小 n |
|---|---|---|
| 小效应（难检测的微小提升） | 0.3 | 175.38 → 取 **176** |
| 中效应（典型 mAP/准确率差异） | 0.5 | 63.77 → 取 **64** |
| 大效应（显著差异） | 0.8 | 25.52 → 取 **26** |

反查（用于回答"3~5 个种子够不够"）：
- d=0.5、每组 n=5 → power **0.108**（远低于 0.8，说明仅 5 个种子检测中等效应严重欠功效）。
- d=0.8、每组 n=30 → power **0.861**（达标）。
- 验证一致性：d=0.5 取 n=64 → power **0.802**（≈0.8，与正向求解自洽）；d=0.8 取 n=26 → power **0.808**（≈0.8 自洽）。

## 结论与口径

- 算例数值与 statsmodels 实跑**完全一致**，已写入 m05 references「统计功效与样本量/种子数规划」节，并在该节注明"数值经 statsmodels 0.14.5 实跑核验，留痕见 `_verification_log/R5-04-power-analysis.md`"。
- 重要科研含义：常见"跑 3~5 个种子"只够检测**大效应**；要稳健检测中等效应（d≈0.5）每组需约 64 次重复——这正是 m05 要提醒用户的功效缺口。
- 效应量 d 的现实换算：Cohen 经验档 0.2 小 / 0.5 中 / 0.8 大；若已有预实验，用 `(mean1-mean2)/pooled_sd` 估 d 再代入，比套经验档更准。
