# 发现 MCP server 呈现模板

当任务需要接外部数据/工具，去 registry.modelcontextprotocol.io 或官方参考集找到候选 MCP server 时，用此模板汇报。先 `tools/list` / `resources/list` 看清暴露了什么，再决定调用。

## 单个候选

```
找到一个能接「<外部能力>」的 MCP server：

  名称：<server-name>（如 io.github.owner/server）
  用途：<它暴露的 tools/resources 概述>
  传输：<stdio / streamable-http>，运行方式：
    - TS  : npx -y @modelcontextprotocol/server-<x>
    - Py  : uvx mcp-server-<x>
    - Win : 用 cmd /c 包裹 npx 项
  暴露能力（先探测再用）：
    - tools/list   → <列出工具名>
    - resources/list → <列出资源>
  来源/信誉：<官方参考集 / 社区 registry>
  链接：https://registry.modelcontextprotocol.io/ 或仓库 URL

注意：装 MCP server = 授权它访问文件/网络，先评估安全。要接入吗？
```

## 接入前探测清单

1. `tools/list`（支持 cursor 分页）——看有哪些工具、入参 schema。
2. `resources/list` / `resources/templates/list`——看可读资源与 URI 模板。
3. 仅在确认能力匹配后 `tools/call` / `resources/read`。
4. 区分错误：协议错误（JSON-RPC，如 -32002 未找到）vs 执行错误（`isError: true`）。

## 官方参考 server（教学用、非生产级）

| server | 用途 | 运行 |
|--------|------|------|
| Fetch | 取网页转 LLM 友好格式 | uvx mcp-server-fetch |
| Filesystem | 带访问控制的文件操作 | npx -y @modelcontextprotocol/server-filesystem |
| Git | 读/搜/改 Git 仓库 | uvx mcp-server-git |
| Memory | 知识图谱持久记忆 | npx -y @modelcontextprotocol/server-memory |
| Sequential Thinking | 反思式分步推理 | npx -y @modelcontextprotocol/server-sequential-thinking |
| Time | 时区转换 | uvx mcp-server-time |
| Everything | 演示 prompts/resources/tools | npx -y @modelcontextprotocol/server-everything |

## 验证过的入口（2026-06 实测）

- MCP 官方注册中心 API：`https://registry.modelcontextprotocol.io/v0/servers` → 200，
  返回 `{"servers":[{server:{name,description,version,remotes:[{type,url}]},_meta:{...}}]}`，
  当前 schema 版本 `2025-12-11/server.schema.json`，支持 `?limit=` 分页。
- 参考 server 集：github.com/modelcontextprotocol/servers
- Windows 坑：JSON 配置里的 npx 命令要写成 `cmd /c npx -y ...`，否则起不来。
