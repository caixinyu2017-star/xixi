# 在 Codex 中安装 Light

Light 是一套全流程科研技能包。Codex 通过原生 skill 发现机制加载 28 个 `light-*` 技能；全局 `AGENTS.md` 只负责告诉 Codex 何时调用这些技能。

## 前置

- Git
- 已安装 Codex CLI

## 安装（推荐：克隆 + 安装脚本）

1. **克隆 Light 仓库：**
   ```bash
   git clone https://github.com/Light0305/Light-skills.git ~/.codex/Light-skills
   cd ~/.codex/Light-skills
   ```

2. **链接 28 个技能与共享资源：**

   **macOS / Linux：**
   ```bash
   ./install.sh codex
   ```

   **Windows (PowerShell)：**
   ```powershell
   powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\Light-skills\install.ps1" -Client codex
   ```

   安装脚本会把每个技能链接为：
   ```text
   ~/.agents/skills/light-literature-search/
   ~/.agents/skills/light-data-engineering/
   ...
   ~/.agents/skills/light-research-ethics/
   ```

   同时把共享库链接到 `~/.agents/databases` 与 `~/.agents/code_assets`，这样技能内的相对路径引用能正常解析。

3. **追加路由说明到全局 `AGENTS.md`**（让 Codex 知道何时调用 Light）：

   **macOS / Linux：**
   ```bash
   mkdir -p ~/.codex
   touch ~/.codex/AGENTS.md
   if ! grep -q '<!-- LIGHT-SKILLS-START -->' ~/.codex/AGENTS.md; then
     cat ~/.codex/Light-skills/AGENTS.snippet.md >> ~/.codex/AGENTS.md
   else
     echo 'Light routing block already exists in ~/.codex/AGENTS.md; replace that block manually if you are upgrading.'
   fi
   ```

   **Windows (PowerShell)：**
   ```powershell
   New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.codex" | Out-Null
   $agents = "$env:USERPROFILE\.codex\AGENTS.md"
   if (-not (Test-Path $agents)) { New-Item -ItemType File -Path $agents | Out-Null }
   if (-not (Select-String -Path $agents -Pattern '<!-- LIGHT-SKILLS-START -->' -Quiet)) {
     Get-Content "$env:USERPROFILE\.codex\Light-skills\AGENTS.snippet.md" | Add-Content $agents
   } else {
     Write-Host 'Light routing block already exists in ~/.codex/AGENTS.md; replace that block manually if you are upgrading.'
   }
   ```

4. **重启 Codex**（退出并重新启动 CLI）以发现技能。

## 验证

启动 Codex 后输入：

```text
帮我做文献调研
这篇论文该投哪个期刊？
继续，刚断了
```

预期：Codex 根据 `AGENTS.md` 路由到对应 `~/.agents/skills/light-*/SKILL.md`；断点恢复类请求应先走 `light-memory-pm` + `light-orchestrator`。

## 升级

```bash
cd ~/.codex/Light-skills
git pull
./install.sh codex
```

如果 `AGENTS.snippet.md` 有更新，手动替换 `~/.codex/AGENTS.md` 中 `LIGHT-SKILLS-START` / `LIGHT-SKILLS-END` 之间的旧块。

## 卸载

删除 Light 创建的链接与克隆目录，并移除 `~/.codex/AGENTS.md` 中 Light 追加的小节即可。为避免误删用户自己的目录，**只删除链接/确认的克隆目录，不对共享路径做 blanket `rm -rf`**。

**macOS / Linux：**
```bash
for p in ~/.agents/skills/light-* ~/.agents/databases ~/.agents/code_assets; do
  if [ -L "$p" ]; then
    rm "$p"
  elif [ -e "$p" ]; then
    echo "skip non-symlink path: $p"
  fi
done
rm -rf ~/.codex/Light-skills
```

**Windows (PowerShell)：**
```powershell
$paths = @(
  "$env:USERPROFILE\.agents\databases",
  "$env:USERPROFILE\.agents\code_assets"
) + @(Get-ChildItem "$env:USERPROFILE\.agents\skills" -Filter 'light-*' -ErrorAction SilentlyContinue | ForEach-Object { $_.FullName })
foreach ($p in $paths) {
  if (Test-Path -LiteralPath $p) {
    $item = Get-Item -LiteralPath $p -Force
    if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
      cmd /c rmdir "$p"
    } else {
      Write-Host "skip non-link path: $p"
    }
  }
}
Remove-Item -Recurse -Force "$env:USERPROFILE\.codex\Light-skills" -ErrorAction SilentlyContinue
```
