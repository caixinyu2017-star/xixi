# XLSX-REF — Excel/CSV 深度读取参考（copy-paste ready）

配套脚本：`scripts/xlsx_read.py`（已自检：sheets/formulas/values/profile）。
铁律：openpyxl **无求值引擎**——公式只存字符串。要算值用 `data_only=True` 读缓存，
或写后跑 LibreOffice 重算。

## 决策表

| 任务 | 首选 | 说明 |
|------|------|------|
| 数据画像/分析 | pandas | `read_excel(sheet_name=None)` 读全部 sheet |
| 读公式（不求值） | openpyxl | `data_only=False`（默认） |
| 读缓存计算值 | openpyxl | `data_only=True`（需之前算过保存） |
| 读格式/合并/条件格式 | openpyxl | Font/PatternFill/Alignment |
| 重算公式 + 扫错 | LibreOffice recalc | openpyxl 不算，必须外部重算 |

## 数据画像（pandas，读全部 sheet）

```python
import pandas as pd
sheets = pd.read_excel("file.xlsx", sheet_name=None)  # dict: name→DataFrame
for name, df in sheets.items():
    print(f"=== {name} {df.shape} ===")
    print(df.info())
    print(df.describe(include="all"))
```

读特定列/类型，避免推断错（如 id 当数字丢前导 0）：
```python
df = pd.read_excel("file.xlsx", dtype={"id": str},
                   usecols=["id", "amount"], parse_dates=["date"])
```

## 读公式（openpyxl，不求值）

```python
from openpyxl import load_workbook
wb = load_workbook("model.xlsx")          # data_only=False 默认，保留公式
ws = wb.active
for row in ws.iter_rows():
    for c in row:
        if isinstance(c.value, str) and c.value.startswith("="):
            print(c.coordinate, c.value)
```

## 读缓存计算值（data_only=True）

```python
from openpyxl import load_workbook
wb = load_workbook("model.xlsx", data_only=True)   # 读 Excel 上次算的值
ws = wb.active
for row in ws.iter_rows(values_only=True):
    print(row)
# 警告：data_only=True 打开后再 save() 会永久丢公式！只读用。
```

## 多 sheet 关系 / 跨表引用

```python
from openpyxl import load_workbook
wb = load_workbook("model.xlsx")
for name in wb.sheetnames:
    print(name, wb[name].max_row, "x", wb[name].max_column)
# 跨表引用写法：=Sheet1!A1 ；财务模型 FY 数据常在 50+ 列（col 64 = BL）
```

## 写后重算（LibreOffice，openpyxl 不算）

```bash
# Anthropic XLSX skill 提供 scripts/recalc.py（用 LibreOffice 重算并扫错）
python scripts/recalc.py output.xlsx 30
# 返回 JSON：total_errors / total_formulas / error_summary
# 有 #REF!/#DIV/0!/#VALUE!/#NAME? 就改了再算
```

## 已知坑

- openpyxl **无公式求值**：写完公式不会有值，必须 LibreOffice/Excel 重算。
- `data_only=True` 保存会**永久销毁公式**——只读取时用。
- openpyxl **1-based** 索引（row=1,col=1=A1）；**pandas DataFrame 第 5 行 = Excel 第 6 行**（表头偏移）。
- 财务配色约定：蓝=硬编码输入、黑=公式、绿=跨表链接、红=外部文件链接、黄底=关键假设。
- 大文件用 `read_only=True`/`write_only=True` 省内存；防 XML 攻击装 `defusedxml`。

## 链接（2026-06 curl 200 核验）

- Anthropic XLSX skill: https://github.com/anthropics/skills/blob/main/skills/xlsx/SKILL.md
- openpyxl: https://openpyxl.readthedocs.io/en/stable/
