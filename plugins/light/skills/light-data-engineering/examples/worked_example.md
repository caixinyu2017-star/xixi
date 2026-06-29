# Worked Example — 端到端数据先行走查（奶山羊行为数据集）

> 用一个真实风格的小数据集，把 data-engineering 的「四问 → 体检 → 规模 → 质量门禁 → 防泄漏划分 → 数据卡」走一遍，展示每步用哪个脚本、出什么结论。**数据为方法演示用的合理量级，非真实采集统计。**

## 场景

奶山羊发情行为识别：3000 条传感器片段（加速度计 + 视频帧特征），标 `behavior`（3 类：发情/正常/采食），按 `goat_id`（40 只羊）分组采集，含 `timestamp`。目标：判断"这批数据够不够训一个行为分类器"。

---

## Step 1 — 数据体检（data_doctor.py）

```bash
python scripts/data_doctor.py --csv goat_behavior.csv --target behavior --out quality_report.md
```

关注报告里的 HIGH/MED 项（示意结论）：
- `[MED] 1 个 ID-like 列：goat_id`（近乎逐行唯一？否——40 只羊重复出现，unique_ratio≈0.013，**不会**被标 ID-like；但若误用 `segment_id`(每片段唯一) 当特征，会被标 ID-like → 提示剔除）
- `[HIGH] possible target leakage：activity_label_raw`（若数据里混入了人工预标的原始标签列，η²≈1 会被抓出 → 必须剔除，否则是把答案当输入）
- `[MED] N 个高基数类别列`（阈值已随行数自适应）

**结论**：剔除 `segment_id`(ID-like) 与 `activity_label_raw`(泄漏)，其余进下一步。

---

## Step 2 — 规模是否足够（sample_size_check.py）

```bash
python scripts/sample_size_check.py --task clf --n 3000 --classes 3 \
    --per-class 1800,800,400 --features 25
```

示意输出：
```
# 数据规模充足性预警 ⚠️ WARN
- [warn] 最小类实际样本=400，介于 50~100... 否，400>100 → 实际 ok
- 样本/特征比=120 >> 10 → ok
```
若把 `--per-class` 改成 `1800,800,40`（发情类仅 40 条）：
```
🛑 INSUFFICIENT
- [insufficient] 最小类实际样本=40 < 50/类经验下限——小类学不动，考虑补采/重采样
```

**结论**：本例 3 类各 ≥400 够用；但要警惕"发情"这一**关键稀有类**的样本数——它才是任务核心，按最小类判而非总量。⚠ 这是经验粗筛，正式样本量须 power analysis。

---

## Step 3 — 质量门禁（quality_gate.py + rules.yaml）

规则文件（节选，演示 severity 分级）：
```yaml
dataset:
  min_rows: 500
  no_duplicate_rows: true
columns:
  behavior:
    required: true
    enum: [estrus, normal, feeding]
  goat_id:
    required: true
    non_null: true
  accel_x:
    dtype: numeric
    non_null: true
    min: -50
    max: 50
    severity: warn      # 越界仅警示不阻断（传感器偶发尖峰，后续异常处理）
```

```bash
python scripts/quality_gate.py --csv goat_behavior.csv --rules rules.yaml --out gate.md
echo "exit=$?"   # error 级全过 → 0；accel_x 越界是 warn → 不影响退出码
```

**结论**：`behavior` enum、`goat_id` 必填等 error 级规则必须全过才放行；`accel_x` 越界标 warn，记录但不一票否决（交 Step 处理异常值）。

---

## Step 4 — 防泄漏划分（safe_split.py）

**关键**：同一只羊的片段绝不能同时进训练和验证（否则模型记住的是"这只羊"而非"行为"——实体泄漏）。这是 group 任务，且目标是分类：

```bash
python scripts/safe_split.py --csv goat_behavior.csv --target behavior \
    --task group --group-col goat_id --group-clf
```

- `--task group --group-col goat_id`：用 GroupKFold 系，同羊不跨折。
- `--group-clf`：显式声明分类 → StratifiedGroupKFold 同时保 3 类平衡（**不靠 nunique 猜**）。
- 脚本内置泄漏断言：预处理（插补/标准化）在每折单独 refit，折内 mean ≠ 全量 mean。

若数据是时序预测（如"用前 N 天预测后一天发情"），则：
```bash
python scripts/safe_split.py --csv ts.csv --target estrus --task timeseries --time-col date
```
`--time-col date` 强制按时间升序重排并校验单调——**不给会警告**，乱序会穿越（用未来预测过去）。

**结论**：行为分类用 `group + --group-clf`（按羊分组+保类别平衡）；时序预测用 `timeseries + --time-col`。两类泄漏（实体跨折、时间穿越）都被脚本挡住。

---

## Step 4.5 — 四问结论卡（data_feasibility.py，交 m03/m04）

把 Step 1-4 收敛成给 m03/m04 的标准工件（区别于给 m05/a03 做实验的 data_card/quality_report）：

```bash
# 先把 Step 2 的规模检查存成 JSON 喂进来，其余三问手填：
python scripts/sample_size_check.py --task clf --n 3000 --classes 3 \
    --per-class 1800,800,400 --features 25 --json > size.json
python scripts/data_feasibility.py --project goat-behavior \
    --q1 ok:"3类行为有判别性传感器特征，剔除泄漏列后25维有效" \
    --q2 warn:"error级门禁全过；accel_x偶发越界(warn)待异常处理" \
    --scale-json size.json \
    --q4 ok:"无ID-like误用、无目标泄漏，特征-目标关系真实" \
    --out data_feasibility.md
```

产出 `data_feasibility.md`：四问各档 + 整体 verdict（本例含 warn → `USABLE_WITH_CAVEATS`）。
- **m03 读它**：verdict 非 INSUFFICIENT 才提 idea；warn 项（如"发情类规模待 power analysis"）写进 idea 约束。
- **m04 读它**：核 idea 自报"数据够"是否与该卡一致，不一致按封顶处理。
- 若把发情类改到 40 条，Q3 变 insufficient → 整体 INSUFFICIENT、退出码 1 → **不进 m03**。

> 落位：`python scripts/emit_artifacts.py --check --dir .` 核 data_card.md / quality_report.md / data_feasibility.md 三件套是否齐备并落到 §6.1 标准名。

---

## Step 5 — 数据卡（data_card_template.md）

填 `assets/data_card_template.md` 的 10 节（对齐 db04）。关键节示意：
- **质量评估**：引用 Step 1-3 的 quality_report.md / gate.md 结论。
- **推荐划分**：写明"按 goat_id 分组的 StratifiedGroupKFold"（Step 4），防后来者误用随机划分。
- **偏差/隐私**：40 只羊样本，品种/胎次分布是否均衡？视频帧含场景背景是否泄漏拍摄批次？
- **访问分级**：原始视频帧 `access_level: raw`（跑 `check_access_level.py` 守门，raw 流向 paper/public-repo 会被阻断）。

---

## 四问总结（喂给 m03/m04）

| 四问 | 本例结论 | 依据 |
|---|---|---|
| 是否足以支撑研究 | ✅ 是 | 3 类行为有判别性传感器特征，剔除泄漏列后 25 维有效特征 |
| 质量是否可靠 | ⚠ 基本可靠 | error 级门禁全过；accel_x 偶发越界(warn)待异常处理 |
| 规模是否足够 | ⚠ 关注稀有类 | 总量 3000 够，但"发情"类须 ≥100；正式结论待 power analysis |
| 特征是否有挖掘价值 | ✅ 是 | 无 ID-like 误用、无目标泄漏后，特征-目标关系真实 |

> 这套走查产出 quality_report.md + data_card.md + **data_feasibility.md**（+ gate.md）四件套：前两件交 m05/a03/m06 做实验，**data_feasibility.md 交 m03/m04 判 idea 是否有数据基础**（CONVENTIONS §6.1 标准交接，补此前靠聊天传的单向挂载）。每步脚本均纯本地零网络、带 selftest。

