# MarkItDown MCP 服务器 / MarkItDown MCP Server

把 **PDF、Word、PowerPoint、Excel、图片、HTML、CSV/JSON/XML、EPUB、YouTube 链接**等格式
转换成干净的 **Markdown**，通过 MCP 暴露给 Claude Code —— 非常适合本仓库的文献检索、数据抽取、
论文阅读与写作等科研技能。

Converts **PDF, Word, PowerPoint, Excel, images, HTML, CSV/JSON/XML, EPUB, YouTube URLs** and more
into clean **Markdown**, exposed to Claude Code over MCP. Handy for the literature-search, data-extraction,
paper-reading and writing skills bundled in this marketplace.

- 上游 / Upstream: [`markitdown-mcp`](https://pypi.org/project/markitdown-mcp/) (Microsoft, part of the
  [`markitdown`](https://github.com/microsoft/markitdown) project)
- 传输 / Transport: **STDIO** by default (`--http` / `--sse` also available)

---

## 工具 / Tool

| 工具 / Tool | 参数 / Args | 功能 / What it does |
| --- | --- | --- |
| `convert_to_markdown` | `uri: str` | 把 `http:`、`https:`、`file:` 或 `data:` URI 指向的资源转换为 Markdown 字符串。/ Convert a resource addressed by an `http:`, `https:`, `file:` or `data:` URI to a Markdown string. |

示例 / Examples:

```text
convert_to_markdown  file:///home/user/xixi/work/data/paper.pdf
convert_to_markdown  https://example.com/report.docx
convert_to_markdown  data:text/html;base64,PGgxPkhpPC9oMT4=
```

> 注意 / Note: 只接受 URI。本地文件请使用 `file://` 前缀的绝对路径。
> Only URIs are accepted — pass local files as absolute `file://` paths.

---

## 安装 / Install

### 方式 A — 一键脚本 / One-shot script (recommended)

```bash
bash mcp/markitdown/install.sh
```

脚本会：`pip install markitdown-mcp` → 把 `markitdown` 服务器合并进 `~/.claude/.mcp.json` →
在 `~/.claude/settings.json` 的 `enabledMcpjsonServers` 中启用 → 校验服务器可启动。之后**重启 Claude Code**。

The script runs `pip install markitdown-mcp`, merges the `markitdown` server into `~/.claude/.mcp.json`,
enables it in `~/.claude/settings.json`, and verifies it boots. **Restart Claude Code** afterwards.

### 方式 B — 手动 / Manual

```bash
pip install markitdown-mcp
```

然后把本目录 [`mcp-snippet.json`](./mcp-snippet.json) 的 `mcpServers` 块合并进你的 `~/.claude/.mcp.json`
（或项目级 `.mcp.json`）：

Then merge the `mcpServers` block from [`mcp-snippet.json`](./mcp-snippet.json) into your
`~/.claude/.mcp.json` (or a project-level `.mcp.json`):

```json
{
  "mcpServers": {
    "markitdown": {
      "command": "markitdown-mcp",
      "args": []
    }
  }
}
```

也可用 `claude mcp add`：/ Or use the CLI:

```bash
claude mcp add markitdown -- markitdown-mcp
```

### 方式 C — 免安装 uvx / No-install via uvx

不想全局安装时，可用 [`uv`](https://docs.astral.sh/uv/) 在隔离环境中直接运行：

To avoid a global install, run it in an isolated environment with [`uv`](https://docs.astral.sh/uv/):

```json
{
  "mcpServers": {
    "markitdown": {
      "command": "uvx",
      "args": ["markitdown-mcp"]
    }
  }
}
```

### 方式 D — Docker

```json
{
  "mcpServers": {
    "markitdown": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "markitdown-mcp:latest"]
    }
  }
}
```

> Docker 方式下 `file:` URI 只能看到容器内文件系统，需自行挂载卷。
> With Docker, `file:` URIs only see the container filesystem — mount a volume to expose host files.

---

## 校验 / Verify

安装后可用以下命令自检（无需接入 Claude Code）：/ Sanity-check the install without Claude Code:

```bash
markitdown-mcp --help        # should print usage
python3 -c "from markitdown import MarkItDown; \
print(MarkItDown().convert_uri('data:text/html;base64,PGgxPk9LPC9oMT4=').markdown)"
# -> # OK
```

---

## 故障排查 / Troubleshooting

- **`ModuleNotFoundError: No module named '_cffi_backend'`** —
  某些基础镜像自带 `cryptography` 却缺少 `cffi` 的已编译后端，会导致 PDF 转换链在启动时崩溃。
  修复：`pip install cffi`。（`install.sh` 会自动检测并修复。）
  Some base images ship `cryptography` without `cffi`'s compiled backend, crashing the PDF path on
  startup. Fix with `pip install cffi` — `install.sh` detects and repairs this automatically.
- **`Couldn't find ffmpeg or avconv` (RuntimeWarning)** —
  仅音频转写需要 `ffmpeg`，其余格式不受影响；如需音频请安装 `ffmpeg`。
  Only audio transcription needs `ffmpeg`; every other format is unaffected. Install `ffmpeg` if you
  need audio.
- **服务器未出现 / Server not showing up** — 确认 `~/.claude/settings.json` 的
  `enabledMcpjsonServers` 含 `"markitdown"`，并重启 Claude Code。
  Ensure `"markitdown"` is in `enabledMcpjsonServers` in `~/.claude/settings.json`, then restart
  Claude Code.

---

## 许可 / License

`markitdown` / `markitdown-mcp` 由 Microsoft 以 MIT 许可发布；本目录仅提供配置与安装脚本。
`markitdown` / `markitdown-mcp` are released by Microsoft under the MIT license; this directory only
adds configuration and an installer.
