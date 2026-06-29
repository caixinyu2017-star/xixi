# R12.2 Windows 安装 CI 看护 — install.ps1 幂等/junction/卸载安全实测留痕

- 日期：2026-06-12
- 环境：本机 Windows 11 Home China 10.0.26200，Windows PowerShell **5.1**.26100.8457（CI Windows runner 用 pwsh 7.x）。
- 任务：为 ci.yml 增 `windows-latest` job 看护 install.ps1（幂等、junction 指向、卸载安全）；本地复现"穿透删除会被抓"。

## 一、幂等 + junction 指向（本地实测）
- install.ps1 的 `Link-Dir` 已在重链前判定旧路径是否 ReparsePoint，非链接则 throw 拒绝覆盖；是链接则 `cmd /c rmdir`（**不带 /s**）只摘链接再重建。连跑两遍，第二遍照常把 28 技能 + databases/code_assets/4 文档重新链接，技能计数仍 == 28（`$ExpectedSkills` 断言），幂等成立。
- junction 指向校验：`(Get-Item $link).Target` 应等于源仓库技能目录。CI job 据此断言。

## 二、卸载安全：穿透删除复现（关键诚实结论）
复现脚本 `_tmp_junction_repro.ps1`（跑完即删，不入库）建"源仓库 + SENTINEL.txt"，路径含空格，分别测四种卸载写法后看源文件是否还在：

| 卸载写法 | 源 SENTINEL 是否被穿透删除 | 结论 |
|---|---|---|
| `cmd /c rmdir "<link>"`（install.ps1 现用，无 /s） | 否，完好 | ✅ 安全 |
| `Remove-Item -LiteralPath <link> -Recurse -Force` | 否，完好 | 本机未穿透 |
| `cmd /c rmdir /s /q "<link>"` | 否，完好 | 本机未穿透 |
| 先 `Get-Item.Target` 解析到源目录再 `Remove-Item -Recurse` | **是，源被删** | 🛑 危险，被断言抓出（exit 1） |

**诚实发现**：在本 Windows 11 + .NET 版本上，经典的"`rmdir /s` 穿透 junction 删源"已被系统/.NET 修复——Case 2/3 未复现穿透。真正稳定触发穿透删除的是"先把链接解析成目标真实路径、再递归删该路径"（Case 4），这在任何 OS 都会删到源。
- 因此 CI 的卸载安全断言以"**卸载后源仓库哨兵文件 + 28 个 SKILL.md 必须完好**"为准（对穿透删除的任何成因都成立），而非假设某条具体命令必然穿透。Case 4 证明该断言有牙：穿透发生时 exit 1、build 变红。

## 三、CI job 设计（ci.yml `install-windows`）
1. checkout → 在 `$RUNNER_TEMP` 下建一个"假 HOME"（路径**含空格**，复现真实用户 `C:\Users\Light Wang\` 场景）。
2. `pwsh install.ps1 -Client claude`（HOME 改指向假 HOME）连跑两遍 → 断言两遍后技能数都 == 28（幂等）。
3. 断言每个 `~/.claude/skills/light-*` 是 ReparsePoint 且 Target 指回源仓库 skills 目录（junction 指向正确）。
4. 写一个源仓库哨兵文件 → 用 `cmd /c rmdir`（安全写法）逐个摘除技能链接模拟卸载 → 断言哨兵文件与所有 28 个源 SKILL.md 完好无损（卸载不伤源）。
5. 全程 pwsh；注释 ASCII-only（PowerShell 5.1 GBK 解析坑，PROGRESS R1.5 有记，CI 用 pwsh 7 仍守此纪律以防本地 5.1 复跑）。

## 局限
- 本机只有 PS 5.1，CI 用 pwsh 7；junction 行为两版一致（均走 Win32 ReparsePoint），但 install.ps1 的 `New-Item -ItemType Junction` 在 pwsh 7 同样支持。
- 未测 admin 符号链接路径（install.ps1 用 junction 正是为免 admin），符合现状设计。
