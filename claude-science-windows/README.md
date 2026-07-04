# Claude Science — Windows 一键安装

[Claude Science](https://claude.com/product/claude-science) 是 Anthropic 面向科学家的 AI 科研工作台（Beta），
官方目前只提供 macOS / Linux 客户端。在 Windows 上的官方推荐方式是通过
**WSL 2（Windows 的 Linux 子系统）** 运行 Linux 版，然后**在 Windows 的浏览器里打开**它的网页界面
（参见官方文档 [Run on Windows with WSL](https://claude.com/docs/claude-science/run-on-windows-wsl)）。

本目录的 **`ClaudeScience-Install.bat`** 把这整个过程做成了一键安装：双击即可自动完成
WSL2 → Ubuntu 24.04 → Claude Science 的安装，并在桌面生成 `ClaudeScience.bat` 启动器，
以后双击启动器就会自动启动服务并在浏览器中打开页面。

---

## ✅ 前提条件

| 条件 | 说明 |
| --- | --- |
| Windows 10 2004 以上 或 Windows 11 | 64 位，需支持 WSL 2 |
| 电脑已开启虚拟化 | 绝大多数电脑默认开启；若报错需进 BIOS 打开 |
| Claude 订阅 | 需要 **Pro / Max / Team / Enterprise** 其中之一（Beta 期间要求） |
| 网络 | 需要能访问 `claude.ai`（中国大陆网络环境可能需要自行解决连通性） |

## 🚀 使用步骤

1. **下载**本目录中的 `ClaudeScience-Install.bat` 到电脑上（在 GitHub 文件页面点右上角
   "Download raw file" 按钮）。
2. **双击运行**。
   - 如果出现蓝色的 "Windows 已保护你的电脑" 提示：点 **更多信息 → 仍要运行**；
   - 弹出管理员权限（UAC）确认窗口时：点 **是**。
3. 如果你的电脑是第一次装 WSL，脚本会提示**重启电脑**。重启后，**再次双击本文件**，
   安装会自动继续。
4. 安装 Ubuntu 时会弹出黑色窗口要求**创建 Linux 用户**：输入一个英文小写用户名
   （如 `kexue`）回车，再设置两遍密码（输入时屏幕不显示，属正常现象）。
5. 安装完成后，**双击桌面上的 `ClaudeScience.bat`**：它会启动 Claude Science 服务，
   并自动用你的默认浏览器打开登录网址（形如 `http://localhost:8765/?token=…`）。
6. 在打开的网页中**登录你的 Claude 账号**，按向导完成初始化，即可开始使用。

> 脚本可以重复运行：再次双击 `ClaudeScience-Install.bat` 会跳过已完成的步骤，
> 并把 Claude Science 更新到最新版本。

## 🛑 停止 / 常见问题

- **停止服务**：在命令提示符（cmd）中运行 `wsl --shutdown`。
- **浏览器打不开 / 页面提示无权限**：先运行 `wsl --shutdown`，再双击桌面的
  `ClaudeScience.bat`（每次冷启动会生成新的一次性登录令牌）。
- **WSL 安装失败**：多为 Windows 版本过旧（请先更新系统）或 BIOS 未开启虚拟化。
- **Claude Science 下载失败**：确认当前网络能访问 `claude.ai` 后重试。
- **登录后提示无法使用**：确认你的 Claude 账号有 Pro / Max / Team / Enterprise 订阅。

## 🔧 它到底做了什么（手动等效步骤）

如果你想手动安装，等效命令如下：

```powershell
# PowerShell（管理员）
wsl --install -d Ubuntu-24.04
```

```bash
# 重启并创建用户后，在 Ubuntu 终端中：
sudo apt-get update && sudo apt-get install -y curl ca-certificates bubblewrap
curl -fsSL https://claude.ai/install-claude-science.sh | bash
~/.local/bin/claude-science serve --port 8765 --no-browser
# 然后把终端里打印的 http://localhost:8765/?token=… 网址复制到 Windows 浏览器打开
```

说明：官方安装脚本会校验下载文件的 SHA-256 后把程序装到 `~/.local/bin/claude-science`；
沙箱运行依赖 `bubblewrap`（因此需要 Ubuntu 24.04 及以上）。WSL 2 会自动把 `localhost`
转发给 Windows，所以网址在 Windows 浏览器里直接可用。

## 📚 参考

- 官方产品页：<https://claude.com/product/claude-science>
- 官方发布公告：<https://www.anthropic.com/news/claude-science-ai-workbench>
- 官方 Windows/WSL 文档：<https://claude.com/docs/claude-science/run-on-windows-wsl>
