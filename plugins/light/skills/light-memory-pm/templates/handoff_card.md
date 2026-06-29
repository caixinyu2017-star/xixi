---
session_no: S03                 # 本会话序号（两位，递增）
suggested_title: "[goat] S04 图表绘制"   # 给下一个对话的建议名称（编号让对话列表天然有序）
parent_session: S02             # 上级会话号（衔接链；可沿此追到任意上级；首卡写 none）
project: dairygoat-detect-track # db09 项目 slug；无项目写 none
date: 2026-06-12                # 造卡日期（绝对日期）
---
## 当前阶段
<pipeline 阶段 / 当前 skill / 本段在做什么，一两句>

## 已完成（产物路径 + 验证摘要）
- <相对项目根的路径> — <怎么验证的：命令输出 / 测试 / diff / 人工确认>

## 工作区状态
<clean / 未提交清单 / 已提交未推送(sha) / 等 CI(run id)>

## 下一步（≤3 条，最小动作）
1. ...

## 阻塞/风险
<需用户决策 / 数据缺口 / 诚信风险 / 无>

## 必读文件（按序）
1. 本卡 → 2. .light/passport.yaml → 3. databases/db09-projects/projects/<slug>/project_card.md → 4. <本段关键产物>

## 禁止
- 别重做"已完成"清单里的事；别凭记忆补写未验证结论。
- 别把本卡当作当前事实——接手后先用 git status / git log 刷新现实再动手。
