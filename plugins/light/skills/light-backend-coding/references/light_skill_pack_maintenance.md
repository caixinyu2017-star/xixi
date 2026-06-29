# Light 技能包维护：断点恢复、质量门与入口防漂移

适用于维护 `D:/skill/Light` 这类多技能包仓库：用户经常在 Claude/Hermes 断流后说“继续 / 刚断了”，期望直接接手并完成真实验证、提交、推送、等待 CI。

## 断点恢复流程

1. **不要询问用户复述**：把“继续 / 刚断了 / 接手 Claude”视为恢复指令。
2. 立即读取活状态：
   - `git status --short --branch`
   - 最近提交：`git log --oneline -8`
   - 相关 CI：`gh run list --branch master --limit 5`
   - 当前 todo（若可用）
   - 当前任务相关文件 diff / 校验器输出
3. 若看到 CRLF/整文件换行污染，先转 LF 再继续；不要把换行污染和真实改动混在一起提交。
4. 只在真实 blocker（缺上下文且工具无法恢复、危险破坏性操作）时问用户。

## 提交前必须做到“真实跑过”

- 不能只写脚本或文档；要跑对应校验器和自测。
- Light 仓库当前核心 gates：
  - `python .github/scripts/check_skills.py`
  - `python .github/scripts/check_databases.py`
  - `python .github/scripts/check_skill_assets.py`
  - `python .github/scripts/check_entry_docs.py`
  - `/d/Anaconda/python.exe .github/scripts/run_skill_selftests.py --group all --timeout 120`
- 运行 `git diff --check` 和 added-line 静态扫描：secret、`shell=True`/`os.system`、`eval`/`exec`、`pickle.loads`、SQL 字符串拼接。
- 推送后用 `gh run watch <run_id> --exit-status` 等 CI 通过，再汇报。

## 技能脚本 `--selftest` 治理

- 资产校验不能只搜 `selftest` 字样；必须要求显式 `--selftest`。
- CI 不只检查 marker，还要实际执行 `python <script> --selftest`。
- 自测必须离线、合成数据/临时目录、真实断言，不依赖 DOI/Crossref/OpenAlex/S2、账号、LibreOffice 或网络。
- 旧脚本若保留无参自测，入口只能接受无参或唯一 `--selftest`：

```python
if len(sys.argv) > 2 or (len(sys.argv) == 2 and sys.argv[1] != "--selftest"):
    raise SystemExit(f"usage: python {sys.argv[0]} [--selftest]")
_selftest()
```

## 入口文档防漂移

- `README.md` / `README.en.md` / `ROUTER.md` / `MODE_REGISTRY.md` / `CONVENTIONS.md` / `WHATS_INCLUDED.md` 是用户入口层，改动要一起审计。
- `ROUTER_EXAMPLES.md` 是路由样例回归集；新增/修改路由规则时同步样例。
- 重点锁定边界：
  - “继续 / 刚断了 / 接手 Claude” → `a02 memory-pm + light-orchestrator` 断点恢复。
  - “继续写 / 继续润色当前段落” → 单技能 `m07` / `m08`，不要启动 orchestrator。
  - 图表规划 `m09`、实际绘图/图表审查 `m11`、PPT/deck QA `m16`。
  - paper-drafting 的草稿 self-review 属 `m07`；正式模拟审稿/rebuttal 属 `m14`。
- 禁止重新引入非本包技能：`light-software`、`light-miniprogram`、`light-novel`。

## 安装脚本与客户端集成防漂移

维护 Light 这类技能包时，安装入口和仓库内部质量门同等重要。新增/修改 `install.sh`、`install.ps1`、`AGENTS.snippet.md`、`.codex/INSTALL.md`、`.claude-plugin/`、`.codex-plugin/` 时，必须验证以下边界：

- **逐技能安装路径**：Codex/Hermes/Claude 路由文档应指向 `~/.agents/skills/<skill-name>/SKILL.md` / 对应客户端的逐技能目录，而不是旧式聚合路径 `~/.agents/skills/light`。
- **共享资源同级链接**：安装脚本必须同时链接/创建 `databases` 与 `code_assets` 为 skills 目录父级的同级资源，否则技能内相对路径会断。
- **拒绝覆盖用户目录**：安装器只能覆盖已确认的 symlink/junction/reparse point；遇到非链接目录必须 fail-closed 并提示用户手动处理。
- **Windows 与 POSIX 分流**：`install.sh` 只面向 macOS/Linux；Windows Git Bash/MSYS/Cygwin 可能把链接表现成普通目录，二次运行会误判，脚本应明确提示改用 `install.ps1`。Windows 侧用 PowerShell Junction，并测试 `install.ps1 -Client codex` 在临时 `HOME/USERPROFILE` 下连续运行两次。
- **安全卸载文档**：不要写整棵目录递归强删这类 blanket 删除命令。卸载说明必须只删除 symlink/junction，非链接路径打印 `skip non-symlink/non-link` 并保留。
- **安装资产校验器**：把上述规则写成 CI gate（例如 `check_installation_assets.py`），并让 CI 在 `install.sh`、`install.ps1`、`AGENTS.snippet.md`、`.codex/**`、`.claude-plugin/**`、`.codex-plugin/**` 改动时触发。Linux CI 应实际跑 `install.sh` 临时 HOME 二次安装；Windows 本地若只可做 PowerShell 测试，要明确这是本地限制，不能削弱 Linux CI 检查。

## 技能内部链接防漂移

技能内 `SKILL.md` 常用反引号引用 `references/`、`assets/`、`scripts/`、`templates/`、`examples/`，这些不是普通文档装饰，而是 agent 实际会按路径读取/执行的入口。维护时要把它们纳入 CI，而不是等用户使用时才发现断链。

- **硬校验范围**：`SKILL.md` 里的具体反引号路径必须能在该技能目录下解析到真实文件/目录；`SKILL.md`、`references.md`、`references/*.md`、`templates/*.md`、`examples/*.md` 中显式 Markdown/HTML 本地链接也要验证。
- **避免误报**：研究笔记里的第三方仓库结构（如 `scripts/foo.py`）不应按本技能资产硬校验；泛称目录 `scripts/`、通配符 `scripts/*.py`、占位符 `examples/xxx.py`、自测生成目录要跳过。
- **接入点**：新增 `check_skill_links.py` 后同步更新 `WHATS_INCLUDED.md` 与 CI lint job，并把 `skills/**/references.md`、`skills/**/references/**`、`skills/**/templates/**`、`skills/**/examples/**` 加入 CI 触发路径，防止非 SKILL.md 文档改动绕过链接校验。
- **负例验证**：链接/manifest 类校验器不能只证明“当前仓库通过”。临时注入一个应通过的相对 sibling link 样例和一个应失败的逃逸/断链（如 `references/../SKILL.md`），确认脚本分别 pass/fail；测试后必须恢复文件并跑 `git diff --check`，防止临时写回造成 CRLF/整文件换行污染。
- **审查日志可读性**：如果变量名或 diff 片段触发平台脱敏（如把正则变量误显示成 `***`），优先改成不似密钥的中性命名，避免独立 reviewer 基于被遮蔽 diff 误判语法错误。

## 提交习惯

- 按用途分组提交，中文 commit message 描述文件/模块目的，不写 Claude/AI co-author trailer。
- 推送前在提交后再跑一次完整 gate，避免 rebase/squash 后产生换行或校验漂移。
