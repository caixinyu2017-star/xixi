# 禾灵儿数字画像 · 指标体系与评分内核技术说明

《“禾灵儿数字画像”功能建设方案》的技术配套文件，回答三个问题：五个维度下设了哪些指标、
各渠道对各维度的权重取值多少、从一条原始学习记录到五维得分中间经过哪几步换算。

## 交付物

| 文件 | 说明 |
| --- | --- |
| `禾灵儿数字画像指标体系与评分内核技术说明.docx` | 主交付物，15 页，8 幅图、17 张三线表、12 个 Word 原生公式 |
| `figures/fig1~fig3` | 概念类示意图，由环境中配置的 gpt-image-2 生成 |
| `figures/fig4~fig8` | 数据类图件，由 matplotlib 绑真实数据绘制 |
| `scripts/kernel_facts.py` | 全部实算结果，图件脚本与文档脚本共用 |
| `scripts/make_figures.py` | 图 4—图 8 的生成脚本 |
| `scripts/ai_prompts.json` | 图 1—图 3 的生成提示词 |
| `scripts/build_docx.py` | 文档生成脚本 |
| `scripts/docx_helpers.py`、`scripts/omml.py` | 中文排版与 OMML 公式辅助 |

## 数字的来源

文中每一个参数与实测数值都不是写死的，而是在生成文档时由已上线的算分内核
`禾灵儿德育画像系统/hlr_portrait.py` 与真实数据库实时读出或实算。
正文、表格与图件三者引用同一份 `kernel_facts.facts()` 结果，不会互相打架。
改了 `weights.json` 之后重新跑一遍脚本，文档里的所有数字与图件会同步更新。

## 复现步骤

```bash
cd 禾灵儿指标体系说明
python3 scripts/make_figures.py     # 重绘图 4—图 8
python3 scripts/build_docx.py       # 重新生成 docx
```

图 1—图 3 需要调用 gpt-image-2：

```bash
python3 /root/.claude/skills/gpt-image-2/scripts/gpt_image2.py \
        --manifest scripts/ai_prompts.json -o figures/
```

依赖：`python-docx`、`matplotlib`、`openpyxl`，中文字体 Noto Sans CJK SC。

## 排版规范

一级标题黑体小三加粗、二级黑体四号、三级黑体小四；正文宋体小四、无段前段后间距、
首行缩进 2 字符；图题置于图下、表题置于表上，均为五号黑体；表格一律三线表；
公式用 Word 自带公式编辑器（OMML 原生公式，可在 Word 中直接编辑），公式居中、
编号 (1)(2)(3)… 右对齐；全部图表均先在正文中引用再出现。
文档已通过 OOXML XSD 校验。
