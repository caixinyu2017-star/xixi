# 机制图（D 型，17 幅）重绘规范 —— gpt-image-2

## 0. 为什么重绘

现有 D 型机制图由 matplotlib 绘制，框大字小：以 13.5—15 cm 版心宽度印刷时，
框内文字折合仅约 4.4 pt，正文旁几乎不可读。用户明确要求「字要放大、框内留白要收紧」。
本轮改用 `gpt-image-2` 生成扁平矢量风格信息图，使印刷后主标签观感达到 9 pt 以上。

**参照样张**：`/home/user/xixi/ai-talent-book/figs/fig10_1.png`（前一本书的同类图，
用户认可的观感）——大字、紧框、浅色填充＋深色描边、白底、细而均匀的线宽。
先用 Read 工具看一眼这张样张，再动手。

## 1. 待重绘清单（共 17 幅）

| 文件 | 定义位置 | 图名 |
|---|---|---|
| fig1_1 | diagrams_a.py:152 | 本书研究技术路线 |
| fig1_2 | diagrams_a.py:236 | 全书结构与章节安排 |
| fig2_2 | diagrams_a.py:288 | 理论基础与研究框架的逻辑关系 |
| fig3_1 | diagrams_a.py:330 | 词元的技术属性与经济属性谱系 |
| fig5_1 | diagrams_a.py:382 | 标准词元效值折算体系的构建框架 |
| fig6_1 | diagrams_a.py:451 | 词元价值创造的劳动凝结结构 |
| fig6_2 | diagrams_a.py:494 | 词元价值实现与增值的循环 |
| fig7_1 | diagrams_a.py:531 | 词元价格的三层结构 |
| fig8_1 | diagrams_b.py:116 | 词元市场的多边平台结构 |
| fig9_1 | diagrams_b.py:181 | 算力—词元转化与配置分析框架 |
| fig10_1 | diagrams_b.py:247 | 五类词元运营主体的资产禀赋与职能匹配 |
| fig10_2 | diagrams_b.py:309 | 「五个统一」的机制设计与交易费用节约 |
| fig11_1 | diagrams_b.py:363 | 词元的能耗—碳足迹核算框架 |
| fig12_1 | diagrams_b.py:435 | 引入词元流量的智能经济增长核算框架 |
| fig13_1 | diagrams_b.py:494 | 多案例研究的分析框架 |
| fig13_3 | diagrams_b.py:546 | 企业采纳词元服务的障碍因素编码结构 |
| fig14_1 | diagrams_b.py:608 | 词元经济的政策体系框架 |

## 2. 强制四步

### 第 1 步 中文图释
读三处材料后写出图释，**不要向用户确认，直接进入第 2 步**（本轮已获授权）：
1. `diagrams_a.py` / `diagrams_b.py` 中该图的函数源码 —— 这是要素与关系的**权威定义**；
2. `data/figures_manifest.md` 中该图的一行说明；
3. 正文中引称该图的段落（`grep -n "图N.M" content_chNN.py`）—— 确认图与正文一致。

图释须逐条写明：要素清单（每个方块的中文标签原文）、关系与方向、布局、画幅。

### 第 2 步 英文提示词，中文标签
- 提示词主体用英文；**图内标签必须是中文**，在提示词里用引号原样写出，
  例如 `a box labeled "算力投入"`。
- 必须写死的风格：`flat vector infographic, clean white background,
  thin uniform stroke weight, pale pastel fills with darker matching outlines,
  rounded rectangles, Chinese labels in a bold sans-serif typeface`。
- 必须写死的排除项：`no photorealism, no 3D bevel, no drop shadows, no gradients,
  no lens flare, no stock-photo people, no watermark, no signature, no logo,
  no decorative clutter, no English text, no figure caption, no title, no source line`。
- **字号是本轮的第一目标**，务必在提示词里明确要求，例如：
  `text must be LARGE and fill its box — each label should occupy at least 70% of
  its box width, with tight padding; the smallest character height must be no less
  than 1/28 of the image height; prefer fewer words over smaller type`。

### 第 3 步 生成
```bash
python3 /root/.claude/skills/synced/gpt-image-2/scripts/gpt_image2.py "<英文提示词>" \
  -o /home/user/xixi/token-econ-book/figs/figN_M.png --size 1536x1024 --quality high
```
画幅：横向流程／分层图用 `1536x1024`；纵向分层框架用 `1024x1536`；
方形中心辐射用 `1024x1024`。

### 第 4 步 看图质检（不可跳过）
用 Read 工具把 PNG 实际看一遍，逐项核对：
- [ ] 每个中文标签**逐字正确**，无乱码、无叠字、无伪汉字、无英文混入
- [ ] 图释列出的要素一个不少，没有凭空多出的元素、水印、签名
- [ ] 箭头方向与图释一致
- [ ] 图内没有图名、图注、资料来源文字
- [ ] **最小字符高度 ≥ 图高的 1/28**（即 1024 高的图上不小于 36 px）；
      框内留白收紧，不再出现「大框小字」

不合格就改提示词重生成，**最多两轮**。两轮仍不达标：保留
`figs_mpl_backup/figN_M.png` 的原 matplotlib 版本（`cp` 回 `figs/`），
并在返回结果里明确写出失败模式，不要无限重试。

## 3. 硬性约束

- 图中出现的**数字必须与书中一致**（效值系数 0.38／1.00／1.96／2.94／4.28／2.62、
  四项损失 18／9／12／7、利用率 62%→38%→54%、上界 61% 等），
  以 `diagrams_*.py` 源码与 `data/RESULTS_SPEC.md` 为准，不得自行编造。
- 全书已废止直角引号「」，图内标签一律用 “ ”，且**能不用引号就不用**
  （详见 `data/SPEC_TEXT_REVISE.md`）。
- 图内不得出现具体商业产品名或服务商名，档位一律用抽象类别名。
- 不得覆盖 `figs_mpl_backup/` 里的备份。

## 4. 返回值

返回 JSON：`{"fig": "figN_M", "ok": true/false, "rounds": 1/2,
"size": "1536x1024", "labels_checked": ["…"], "issues": "…", "note": "…"}`
