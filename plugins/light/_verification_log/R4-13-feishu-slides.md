# R4.13 飞书/Lark 幻灯片 — 实查留痕

- 研究日期：2026-06-11
- 执行：Claude Opus 4.8（Claude Code）
- 任务：light-slides references 工具清单补飞书文档/演示文稿条目（国内协作场景）。

## 1. 飞书官方开放平台云文档体系（WebFetch 实查 ✓）

来源：https://open.feishu.cn/document/server-docs/docs/docs-overview?lang=zh-CN

官方云文档资源类型（实查确认）：
1. 文档 Doc/Docx（`doc_token`）
2. 电子表格 Spreadsheet（`spreadsheet_token`）
3. 多维表格 Bitable（`app_token`）
4. 文件 File（`file_token`）
5. 文件夹 Folder（`folder_token`）
6. 知识库 Wiki/Space（`space_id`）
7. 节点 Node（`node_token`）

→ **关键诚实点**：官方云文档概述**没有把"演示文稿/Slides"列为独立开放资源类型**。
页面定义云文档为"在线文档、电子表格、多维表格、知识库、云空间等产品的统称"，
未提演示文稿。资源表无 slides token。「思维笔记不在支持范围内」也佐证并非所有产品开放 API。

服务端 API：文档/电子表格/多维表格可用 `tenant_access_token`/`user_access_token`
程序化创建编辑；**无证据表明存在程序化创建/编辑演示文稿的服务端 API**。

## 2. lark-slides 的真实身份（WebSearch 命中）

WebSearch「飞书 演示文稿 slides API」命中的 lark-slides 来自 **larksuite/cli 仓库的
skills 目录**（github.com/larksuite/cli/blob/main/skills/lark-slides/），是 Lark CLI 的
社区/工具 skill，**非飞书开放平台官方 OpenAPI**。含 SKILL.md / examples.md /
xml-schema-quick-ref.md。

## 3. 写入 references 的诚实口径

飞书条目应说清：
- 飞书**文档/多维表格**有官方服务端 API（适合协作写稿、数据表，可作 PPT 内容来源）；
- 飞书**演示文稿无官方开放 API**（截至实查），程序化生成 PPT 仍走 python-pptx/PptxGenJS/Marp；
- lark-slides 是 larksuite/cli 的工具 skill，非官方 OpenAPI，引用前注明性质。
- 适用场景：国内团队协作、内容初稿在飞书文档协同后导出，再用本 skill 自有资产渲染。
不臆造"飞书演示文稿 API"。
