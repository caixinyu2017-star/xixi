# Phase1 "未能核实"开源库细节 — 重核结果

> 核验方式：Bash `curl` 直连 PyPI JSON API / GitHub REST API / npm registry。
> 核验日期：2026-06-06。许可与版本均取自真实接口返回；拿不到的如实标注。
> 凡 license 字段，优先采信 GitHub `/license`(SPDX) 与仓库 LICENSE 文件首行；PyPI classifier 作旁证，出现冲突时单独标注。

---

## 1. Deepchecks  → 回填到【ML/数据校验类技能（模型/数据质量验证）】

- **真实包名**：`deepchecks`
- **最新版本**：`0.19.1`（PyPI `info.version`）
- **License**：**AGPL-3.0-or-later**（PyPI classifier: `GNU Affero General Public License v3 or later (AGPLv3+)`）
  - ⚠️ GitHub `/license` API 返回 `NOASSERTION`/"Other"（自动识别未命中），但 PyPI classifier 明确为 AGPLv3+。**AGPL 为强 copyleft，商用/SaaS 集成需注意条款**。
- **链接**：PyPI <https://pypi.org/pypi/deepchecks/json> ｜ 仓库 <https://github.com/deepchecks/deepchecks>
- 文档：<https://docs.deepchecks.com>

---

## 2. Evidently  → 回填到【ML 监控/漂移检测类技能】

- **真实包名**：`evidently`
- **最新版本**：`0.7.21`（PyPI `info.version`）
- **License**：**Apache-2.0**（PyPI: "Apache License 2.0" / classifier "Apache Software License"；GitHub `/license` SPDX: `Apache-2.0` 一致）
- **0.6+ 现行导入路径**（取自仓库 main 分支 README，实测）：
  ```python
  from evidently import Report
  from evidently import Dataset, DataDefinition
  from evidently.presets import DataDriftPreset, TextEvals
  from evidently.descriptors import Sentiment, TextLength, Contains
  ```
  - ⚠️ **重大变更**：0.4.x 旧路径 `from evidently.report import Report`、`from evidently.metric_preset import DataDriftPreset` 已废弃。新版统一 `from evidently import Report` + `evidently.presets`。回填技能时务必更新示例代码。
- **链接**：PyPI <https://pypi.org/pypi/evidently/json> ｜ 仓库 <https://github.com/evidentlyai/evidently>（7.5k★）

---

## 3. Snyk CLI  → 回填到【依赖/安全扫描类技能】

- **真实包名（npm）**：`snyk`
- **最新版本**：`1.1305.1`（npm `dist-tags.latest`）
- **License**：**Apache-2.0**（npm version 字段）
- **链接**：npm <https://registry.npmjs.org/snyk> ｜ 仓库 <https://github.com/snyk/snyk>
- 说明：CLI 开源 Apache-2.0，但**后端扫描服务为商业 SaaS**，免费额度有限。CLI 可装但深度扫描依赖账号。

---

## 4. Socket.dev CLI  → 回填到【供应链/依赖安全类技能】

- **真实包名（npm）**：`@socketsecurity/cli`
- **最新版本**：`1.1.102`（npm `dist-tags.latest`）
- **License**：**MIT AND OFL-1.1**（npm version 字段；OFL 为内含字体许可）
- **链接**：npm <https://registry.npmjs.org/@socketsecurity/cli> ｜ 仓库 <https://github.com/SocketDev/socket-cli>
- 说明：CLI 开源 MIT；同 Snyk，后端为商业服务。

---

## 5. Cisco AI Skill Scanner  → 回填到【Agent Skill 安全/技能审计类技能】

- **状态**：✅ **PyPI 真实存在，且为 Cisco 官方包**（非臆造、非 typosquatting）
- **真实包名**：`cisco-ai-skill-scanner`
- **最新版本**：`2.0.11`（PyPI `info.version`）
- **License**：**Apache-2.0**
  - 三重核实：PyPI `info.license`=`Apache-2.0`；GitHub LICENSE 文件首行实读为 "Apache License Version 2.0 … Copyright 2026 Cisco Systems, Inc."；（GitHub `/license` API 显示 NOASSERTION 仅为头部识别误差，LICENSE 正文确为 Apache-2.0）。
- **作者**：Cisco（PyPI `info.author`）
- **简介**：Security scanner for Agent Skills packages - Detects prompt injection, data exfiltration, and malicious code
- **链接**：PyPI <https://pypi.org/pypi/cisco-ai-skill-scanner/json> ｜ 仓库 <https://github.com/cisco-ai-defense/skill-scanner>（2.1k★，最近 push 2026-04-30）
- ⚠️ **同名混淆提醒**：PyPI 另有 `skill-scanner`(v0.3.3, MIT, author 自称 "skill-scanner", 无 project_urls) —— **并非 Cisco 包**，来源不明，回填时勿混用。`pip install` 请用全名 `cisco-ai-skill-scanner`。

---

## 6. LiteParse  → 回填到【文档/PDF 解析类技能】

- **状态**：✅ PyPI 存在，由 run-llama (LlamaIndex) 维护
- **真实包名**：`liteparse`
- **最新版本**：`2.0.6`（PyPI `info.version`）
- **License**：⚠️ **存在标注冲突**
  - GitHub LICENSE 文件 SPDX = **Apache-2.0**（仓库 <https://github.com/run-llama/liteparse>，9.3k★，最近 push 2026-06-05）
  - PyPI classifier 却标 `MIT License`
  - **建议以仓库 LICENSE 文件（Apache-2.0）为准**，回填时注明此冲突，并提示使用前复核当前版本 LICENSE。
- **简介**：A fast, helpful, and open-source document parser
- **链接**：PyPI <https://pypi.org/pypi/liteparse/json> ｜ 仓库 <https://github.com/run-llama/liteparse>

---

## 7. python-pptx  → 回填到【PPT/演示生成类技能】

- **真实包名**：`python-pptx`
- **最新版本**：`1.0.2`（PyPI `info.version`）
- **License**：**MIT**（PyPI `info.license`=MIT，classifier 一致）
- **链接**：PyPI <https://pypi.org/pypi/python-pptx/json> ｜ 仓库 <https://github.com/scanny/python-pptx> ｜ 文档 <https://python-pptx.readthedocs.io>

---

## 8. Marp  → 回填到【Markdown 转幻灯片类技能】

- **真实包名（npm）**：`@marp-team/marp-core` / `@marp-team/marp-cli`
- **最新版本**：marp-core `4.3.0`；marp-cli `4.4.0`（npm `dist-tags.latest`）
- **License**：**MIT**（两包 npm version 字段一致）
- **链接**：<https://registry.npmjs.org/@marp-team/marp-core> ｜ <https://registry.npmjs.org/@marp-team/marp-cli> ｜ 仓库 <https://github.com/marp-team/marp-core>

---

## 9. reveal.js  → 回填到【HTML 幻灯片/网页演示类技能】

- **真实包名（npm）**：`reveal.js`
- **最新版本**：`6.0.1`（npm `dist-tags.latest`）
- **License**：**MIT**（npm version 字段）
- **链接**：npm <https://registry.npmjs.org/reveal.js> ｜ 仓库 <https://github.com/hakimel/reveal.js>

---

## 10. BioRender 导出授权  → 回填到【科研配图/图示类技能】

- **curl 可达性**：✅ `https://www.biorender.com/pricing` 返回 **HTTP 200**（curl 可读，下列条款实测自该页面）
- **核心授权事实（实测自定价页 FAQ + 套餐说明）**：
  - **Free 套餐（$0）**：仅低分辨率导出；**明确不授予 publication/commercial 权利**（原文："Does not provide permission for commercial use or publication"；FAQ："we do not allow figures made on the free plan to be used for publications or commercial use"）。最多 3 个 figure。
  - **付费套餐起授予发表权**：Individual（学术 $35/mo 年付，工业 $95/mo 年付）起即含 "Publish in journals" + "High-resolution export without watermarks"。
  - Lab/Team、Institution/Enterprise 套餐含团队协作与 SSO。
- **结论**：**期刊发表/商用必须升级到付费 Individual 及以上**；免费版导出图**不可**用于论文投稿。回填技能时应提示用户授权门槛，避免合规风险。
- **链接**：<https://www.biorender.com/pricing>

---

## 汇总表

| # | 库 | 真实包名 | 版本 | License（采信值） | 来源 | 备注 |
|---|----|---------|------|------|------|------|
| 1 | Deepchecks | `deepchecks` (PyPI) | 0.19.1 | **AGPL-3.0-or-later** | PyPI classifier | 强 copyleft，商用注意 |
| 2 | Evidently | `evidently` (PyPI) | 0.7.21 | Apache-2.0 | PyPI+GitHub | 0.6+ 导入路径已变，见正文 |
| 3 | Snyk CLI | `snyk` (npm) | 1.1305.1 | Apache-2.0 | npm | 后端商业 SaaS |
| 4 | Socket.dev | `@socketsecurity/cli` (npm) | 1.1.102 | MIT AND OFL-1.1 | npm | 后端商业 |
| 5 | Cisco AI Skill Scanner | `cisco-ai-skill-scanner` (PyPI) | 2.0.11 | Apache-2.0 | PyPI+LICENSE实读 | Cisco官方；勿混 `skill-scanner` |
| 6 | LiteParse | `liteparse` (PyPI) | 2.0.6 | Apache-2.0（GitHub）/ MIT（PyPI classifier）冲突 | GitHub LICENSE | 以仓库为准 |
| 7 | python-pptx | `python-pptx` (PyPI) | 1.0.2 | MIT | PyPI | — |
| 8 | Marp | `@marp-team/marp-core` `…/marp-cli` (npm) | 4.3.0 / 4.4.0 | MIT | npm | — |
| 9 | reveal.js | `reveal.js` (npm) | 6.0.1 | MIT | npm | — |
| 10 | BioRender | （SaaS，非包） | — | 专有/商业 | pricing页200 | 发表需付费版 |

### 诚实声明
- 所有 license/版本字段均来自上述真实 curl 接口返回（PyPI JSON / GitHub REST / npm registry），非记忆臆造。
- 两处主动标注的冲突/特殊情况：① Deepchecks 与 Cisco scanner 的 GitHub `/license` API 返回 NOASSERTION（自动识别局限），已用 PyPI classifier / LICENSE 正文实读补正；② LiteParse 的 GitHub(Apache-2.0) 与 PyPI classifier(MIT) 不一致，已如实标出并建议以仓库 LICENSE 为准。
- 免费源不可得字段：本批次无需 IF/SJR，未涉及付费墙。
