# 排错手册

先跑自检，它会打印全部生效配置并探测连通性，不产生生成费用：

```bash
python3 <SKILL_DIR>/scripts/gpt_image2.py --check
```

退出码含义：

| 码 | 含义 | 下一步 |
|---|---|---|
| 0 | 正常 | — |
| 2 | 配置缺失或参数非法 | 看下方「配置」段 |
| 3 | 网络/代理不可达 | 看下方「网络」段 |
| 4 | 上游 API 报错 | 看下方「API」段 |
| 5 | 响应无法解析 | 看下方「响应」段 |
| 6 | 批量里部分失败 | 看逐项 stderr，只重跑失败项 |

---

## 配置（退出码 2）

**`未找到 API Key`**

按优先级读取 `GPT_IMAGE_API_KEY` → `CHEDANKJ_API_KEY` → `OPENAI_API_KEY`。三个都没有就报这个。

- Claude Code 远程环境：在环境设置的 Environment variables 里加 `CHEDANKJ_API_KEY`。
- 本地：`export CHEDANKJ_API_KEY=sk-...`，或在仓库根建 `.env` 写一行 `CHEDANKJ_API_KEY=sk-...`。
- 注意进程环境变量**优先于** `.env`。改了 `.env` 却不生效，先看环境里是不是已有同名变量。

**`--size 不支持 ...`**

只接受 `1024x1024` / `1536x1024` / `1024x1536` / `auto`，或别名 `1:1` `3:2` `16:9` `2:3` `9:16`
`square` `landscape` `portrait` `wide`。gpt-image 系列不支持任意宽高。

**`参考图不存在`**

`--image` 的路径按当前工作目录解析。用绝对路径最稳。

---

## 网络（退出码 3）

**`Tunnel connection failed: 403 Forbidden` / `CONNECT tunnel failed, response 403`**

当前环境的出网策略没放行目标域名。这是**策略拒绝，不是故障**：

- 不要重试，不要改 `HTTPS_PROXY`，不要关 TLS 校验——这些都绕不过去，也不该绕。
- 正确做法：在 Claude Code 环境设置里把 `api.chedankj.com` 加入允许的出网域名；
  或改配一个已放行的 OpenAI 兼容网关（设 `GPT_IMAGE_BASE_URL`）。
- 确认策略状态：`curl -sS "$HTTPS_PROXY/__agentproxy/status"`，
  `recentRelayFailures` 里会记录被拒的主机名。

**`certificate verify failed`**

脚本已自动读取 `SSL_CERT_FILE` / `REQUESTS_CA_BUNDLE`。若仍失败，确认这两个变量指向
`/root/.ccr/ca-bundle.crt`（远程环境）或系统 CA 包。**不要**用 `verify=False` 类的手段跳过。

**超时**

大图 + `--quality high` 单张可能要 60–120 秒。默认超时 180 秒。网络慢时 `--timeout 300`。
可重试的错误（超时、429、5xx）默认自动退避重试 2 次，用 `--retries` 调整。

---

## API（退出码 4）

| 状态码 | 含义 | 处理 |
|---|---|---|
| 401 | Key 无效或已过期 | 核对 Key；`--check` 会显示 Key 的前 6 位和长度，比对是否是你以为的那一把 |
| 403 | Key 有效但无权限 | 该 Key 可能没开通 gpt-image-2，或网关限制了模型范围 |
| 404 | 端点或模型不存在 | 核对 `GPT_IMAGE_BASE_URL` 是否以 `/v1` 结尾；核对 `GPT_IMAGE_MODEL` 拼写 |
| 429 | 限流或余额不足 | 脚本会自动退避重试；持续 429 就是配额问题，去网关后台看余额 |
| 400 | 请求体被拒 | 多半是 `size`/`quality`/`background` 组合不被该网关支持。用 `--dry-run` 打印请求体，逐项去掉可选参数试 |
| 5xx | 上游故障 | 自动重试；持续失败换时间或换网关 |

**内容策略拒绝**：提示词里若含真实人物姓名、商标 logo、受版权保护的图像描述，网关可能返回
400 并附政策说明。改写提示词，去掉具名主体，用通用描述替代。

---

## 响应（退出码 5）

**`响应里既无 b64_json 也无 url`**

脚本兼容三种返回形态：`data[].b64_json`、`data[].url`、部分网关的 `output[]` 包裹。
都对不上说明该网关返回结构特殊。用 `--dry-run` 确认请求没问题后，手动 curl 一次看原始响应：

```bash
curl -sS "$GPT_IMAGE_BASE_URL/images/generations" \
  -H "Authorization: Bearer $CHEDANKJ_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"model":"gpt-image-2","prompt":"a red circle","n":1,"size":"1024x1024"}' | head -c 800
```

把实际结构报给用户，再决定是否给脚本加一条兼容分支。

**`b64_json 解码失败`**

网关返回的 base64 被截断，通常伴随超时。加大 `--timeout` 重试。

---

## 图像质量问题

不是报错，是出图不对。全部对症改法见 `diagram-recipes.md` 末尾的「常见失败模式」表。
两轮改不好就停手，换矢量方案，别耗轮次。
