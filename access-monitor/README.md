# 网站访问实时监控（博达网站群 + WebVPN）

盯着你网站后台的「运营中心 → 访问统计 → 最近访问记录」，**短时间内访问突然变多就立刻推到你手机上**，
并且把每个来访 IP 查到尽可能细的地步（国家/省/市/区、运营商、AS 号、反向域名、是不是爬虫/机房/代理）。

```
      每 30 秒
浏览器登录 WebVPN ──► 打开「最近访问记录」──► 和上轮比对 ──► 只留新增的
                                                              │
                                        ┌─────────────────────┘
                                        ▼
                        60 秒内新增 ≥ 3 条？ ──否──► 什么都不做，继续等
                                        │是
                                        ▼
                              查 IP 归属（分层、带缓存）
                                        ▼
                     邮件 / Bark / 企业微信 / 钉钉 / 飞书 …… 立刻推送
```

---

## ⚠️ 先做这一件事：改密码

你的账号密码在聊天里以明文出现过。这个程序本身不需要你把密码告诉任何人——它只在你自己电脑上读 `.env`。
**但既然已经发出来了，请先去统一身份认证里把密码改掉**，然后把新密码填进 `.env`。

另外三条：

- `.env`、`config.yaml`、`state/` 都已经写进 `.gitignore`，不会被提交到仓库。**不要**手动把密码写进 `config.yaml`。
- 这个程序只在**你自己的电脑**上跑。它做的事和你手动点后台完全一样，只是自动化了。
- 学校的 WebVPN 常常**只允许一个地方登录**。如果你在自己浏览器里再登一次同一个账号，
  监控程序可能会被顶下线（它会自动重登，但会有几十秒的空档）。

---

## 一、安装（大约 5 分钟）

需要 Python 3.10 或更高版本。Windows 从 [python.org](https://www.python.org/downloads/) 装，
安装时记得勾上 “Add Python to PATH”。

```bash
cd access-monitor

# 建议用虚拟环境，免得污染系统 Python
python -m venv .venv
# Windows:  .venv\Scripts\activate
# macOS:    source .venv/bin/activate

pip install -r requirements.txt
python -m playwright install chromium      # 下载浏览器内核，约 150MB
```

> `ddddocr`（验证码自动识别）连同依赖大约 400MB，下载会慢一点。
> 装它的意义很大：**不装的话，每次会话过期都要你人工输一次验证码，就没法真正挂机了。**
> 实在不想装可以先跳过，程序会在终端里提示你手工输入。

## 二、配置（大约 5 分钟）

```bash
cp .env.example .env               # Windows: copy .env.example .env
cp config.example.yaml config.yaml
```

**`.env`** 放秘密（账号、密码、邮箱授权码）：

```ini
WEBVPN_USERNAME=00008227
WEBVPN_PASSWORD=你改好的新密码

SMTP_USERNAME=你的邮箱@qq.com
SMTP_PASSWORD=QQ邮箱的十六位授权码      # 不是QQ密码！见下面第五节
```

**`config.yaml`** 放不敏感的设置（阈值、间隔、开哪些通道）。里面每一项都有中文注释，
默认值就是你要的规则：**60 秒内新增 ≥ 3 条记录就告警**。

## 三、第一次运行，按顺序来

```bash
python run.py doctor          # ① 自检：依赖装齐没、配置填对没
python run.py test-notify     # ② 发一条测试告警，确认手机/邮箱能收到
python run.py login           # ③ 登录一次（第一次可能要你手工输验证码）
python run.py discover        # ④ 自动找到「最近访问记录」页，并导出页面快照
python run.py once            # ⑤ 跑一轮，看看能不能正确解析出记录
python run.py watch           # ⑥ 正式开始实时监控，Ctrl+C 停止
```

第 ③ 步会弹出一个浏览器窗口（`config.yaml` 里 `browser.headless: false`）。
你能亲眼看到它填账号、填验证码、点登录。跑顺了之后把 `headless` 改成 `true`，它就安静地在后台跑了。

**第 ④ 步是关键。** 各学校博达后台的页面地址、菜单文字、表格列名都不完全一样，网上也查不到，
所以程序的做法是：像人一样点一遍菜单，把落地的真实地址记下来，以后直接开那个地址。
`discover` 会打印类似这样的诊断：

```
✅ 记录页地址：https://webvpn.zjxu.edu.cn/http-8080/xxx/system/.../visitlog.jsp?...
--- 解析诊断 ---
页面里共有 6 张 <table>
  表 #4: 得分 32.0, 21 行, 首行: 序号 访问时间 来访IP 访问页面 来源页面 浏览器
解析出 20 条记录
  2026-08-27 15:32:11 | 223.104.3.77 | /2026/0824/c1001a12345/page.htm | ['序号','访问时间',...]
```

**如果这里显示「解析出 0 条记录」**，说明表格结构和预期不同。这时候：
`dumps/discover-时间戳/` 里已经有完整的页面 HTML 和截图了，把 `frames.json` 和得分最高的那个 `.html`
发给我，我十分钟内就能把解析规则调准。你也可以自己反复调试而不用重新登录：

```bash
python run.py parse dumps/discover-20260827-153211/04-content.html
```

## 四、告警规则怎么调

`config.yaml` 的 `rules` 段：

| 配置项 | 默认 | 含义 |
| --- | --- | --- |
| `burst_threshold` | 3 | 多少条算突发（**含 3**，即 ≥3 条就报） |
| `burst_window_seconds` | 60 | 在多长的时间窗口内统计 |
| `ip_burst_threshold` / `ip_burst_window_seconds` | 3 / 300 | 同一个 IP 在 5 分钟内访问 ≥3 次 |
| `cooldown_seconds` | 300 | 同一规则多久内不重复告警 |
| `ignore_ips` | `[]` | 排除你自己的 IP，支持 `1.2.3.4`、`10.0.0.0/8`、`192.168.` |
| `ignore_bots` | `false` | 设 `true` 则百度/谷歌等爬虫不告警 |
| `baseline_on_first_run` | `true` | 第一次运行把已有记录当基线，避免一启动就轰炸 |

几个实现上的细节，你可能会关心：

- **用的是滑动窗口，不是「每分钟分桶」。** 分桶会漏掉 `23:59:58 / 23:59:59 / 00:00:01` 这种跨分钟的突发，
  滑动窗口不会。
- **不会重复告警。** 每条记录按「时间+IP+页面+来源」算指纹存进本地数据库，同一条只会触发一次。
- **被冷却压下去的告警不会丢**，会并进下一次一起发出来。
- **时间基准优先用后台标注的访问时间**；万一某一列解析不出时间，就退回「我们第一次看到它的时刻」。

## 五、告警发到哪里

至少配一个能推到手机的通道，光靠控制台没意义（关掉终端就看不见了）。

### 邮件（推荐，信息最全，能留档）

以 QQ 邮箱为例：登录网页版 → 设置 → 账户 → 找到「IMAP/SMTP 服务」→ 开启 → 按提示发短信 → **拿到 16 位授权码**。
把授权码（不是 QQ 密码）填进 `.env` 的 `SMTP_PASSWORD`。163 邮箱同理，`host` 改成 `smtp.163.com`。

邮件是 HTML 的，每个 IP 一张小卡片，位置、运营商、AS、标签、地图链接都在里面。

### 手机即时推送（秒到，推荐配一个）

| 通道 | 适合谁 | 怎么拿 key |
| --- | --- | --- |
| **Bark** | iPhone 用户 | App Store 装 Bark，打开就能复制 key。支持响铃、重要警告 |
| **Server酱** | 想用微信收 | https://sct.ftqq.com 微信扫码登录即得 SendKey |
| **企业微信群机器人** | 单位有企微 | 群设置 → 群机器人 → 添加 → 复制 webhook 里 `key=` 后面那段 |
| **钉钉机器人** | 单位用钉钉 | 群设置 → 智能群助手 → 添加机器人 → 安全设置选「加签」，token 和 secret 都填上 |
| **飞书机器人** | 单位用飞书 | 群设置 → 群机器人 → 添加自定义机器人 |

在 `config.yaml` 里把对应通道的 `enabled` 改成 `true`，key 填进 `.env`，然后 `python run.py test-notify` 验证。

## 六、IP 定位精度

你要求「越精细越好」，所以做了分层查询，一个 IP 会把下面这些源的结果合并起来：

| 层 | 数据源 | 能给什么 | 成本 |
| --- | --- | --- | --- |
| 0 | 本地判断 | 内网 / 保留地址直接短路 | 0 |
| 1 | **GeoCN.mmdb**（离线） | 国内 IP 的 **省-市-区/县** + 运营商（含「教育网」）+ 网络类型（宽带 / 基站 / 专线 / **IDC**） | 0，零延迟 |
| 2 | **ip2region.xdb**（离线） | 全球覆盖，国内到市级，境外也能用 | 0，零延迟 |
| 3 | **ip-api.com** | ASN、组织、**是否代理**、**是否机房**、是否移动网络，中文 | 免费 |
| 4 | 腾讯位置服务 | 国内基本都能到 **区/县**，支持 IPv6 | 需要 key，免费 1 万次/天 |
| 5 | 反向 DNS | **认爬虫最可靠的手段**（百度/谷歌/必应/字节/神马…） | 0 |
| 6 | RDAP | 网段归属机构，能看出教育网还是机房 | 0 |

结果按 IP 缓存 7 天，所以真正打 API 的次数很少。

### 强烈建议：装离线库（10 分钟，一劳永逸）

**免费在线 API 在中国大陆基本只能到市级**（ip-api 的 `district` 字段对国内 IP 几乎永远是空的），
所以想要区县级精度，离线库是唯一免费的路。

```bash
pip install maxminddb py-ip2region
```

然后下两个数据文件放进 `state/`：

| 文件 | 下载地址 | 大小 | 作用 |
| --- | --- | --- | --- |
| `GeoCN.mmdb` | https://github.com/ljxi/GeoCN/releases | ~9 MB | 大陆 IP 到区/县，91% 的网段都有区县码 |
| `ip2region.xdb` | https://github.com/lionsoul2014/ip2region（`data/` 目录） | ~11 MB | 全球到市级，给境外 IP 兜底 |

在 `config.yaml` 里填上路径：

```yaml
ipintel:
  geocn_mmdb: "state/GeoCN.mmdb"
  ip2region_xdb: "state/ip2region.xdb"
```

> GeoCN 返回的是 6 位行政区划码（如 `330402`）。如果同目录下放了 `divisions.json`（码 → 名称对照表），
> 就能显示成「浙江省 嘉兴市 南湖区」；没有的话程序至少会告诉你是哪个省，区县显示为区划码。

### 单独查一个 IP

```bash
python run.py ip 223.104.3.77 8.8.8.8
```

### 两个必须说清楚的限制

1. **后台记录的是访客到达服务器时的 IP。** 如果对方走了代理、CDN、或者学校的反向代理，
   记到的就是那个出口 IP，任何定位服务都只能定位到出口。程序会把「疑似代理 / 机房」标出来，
   提醒你这个位置不能全信。
2. **爬虫的识别强弱不同。** 百度、谷歌、必应、字节、神马能靠反向域名认出来（可信）；
   搜狗和 360 根本没有可用的反向域名，只能看 User-Agent（可以伪造）。
   程序会在告警里注明判定依据是「反向域名」还是「UA（可伪造）」。
   字节的 Bytespider 抓得很凶，很容易自己就触发「3 条以上」——如果你不想被它吵，
   把 `rules.ignore_bots` 设成 `true`。

## 七、挂在后台长期跑

**Windows（任务计划程序）**：创建基本任务 → 触发器「计算机启动时」→ 操作「启动程序」：
程序 `C:\路径\access-monitor\.venv\Scripts\python.exe`，参数 `run.py watch`，起始于 `C:\路径\access-monitor`。
记得先把 `config.yaml` 里 `browser.headless` 改成 `true`。

**macOS / Linux**：

```bash
nohup python run.py watch >> logs/watch.out 2>&1 &
```

或者用 `screen` / `tmux`。日志在 `logs/monitor.log`，按天滚动保留 14 天。

## 八、出问题了怎么查

| 现象 | 多半是什么原因 |
| --- | --- |
| `找不到账号输入框` | 登录页结构不同。把 `browser.headless` 设 `false` 看一眼，按 F12 找到输入框，填进 `webvpn.username_selector` |
| `连续 3 次登录未通过` | 程序**故意**停在这里，防止把账号试锁。先手工登录一次确认密码没问题 |
| `验证码识别始终不确定` | 装了 `ddddocr` 吗？装了还不行就把 `headless` 设 `false`，手工输一次，会话能存好久 |
| `一个菜单项都没点到` | 后台菜单文字不一样。照实际界面改 `navigation.menu_path` |
| `解析出 0 条记录` | 表格结构不同。看 `dumps/` 里的快照，或把它发我调解析规则 |
| 老是被踢下线 | 学校 WebVPN 多半只允许单点登录。别在自己浏览器里同时登同一个账号 |
| 收不到告警 | `python run.py test-notify` 单独测通道；邮箱要用**授权码** |

程序在失败时会自动往 `dumps/` 里存截图和 HTML，排查时先看那里。

## 九、这个工具现在的边界

我在自己的环境里**没法连到学校的 WebVPN**（校外网络 + 需要你的账号），所以：

- ✅ **已经离线验证过的**：表格解析（含无表头、脏页面的兜底）、去重指纹、滑动窗口突发检测、
  冷却与不丢记录、配置加载、告警渲染、通道调度。`python tests/test_parser.py`
  和 `python tests/test_integration.py` 都能跑通。
- ⚠️ **必须在你机器上第一次运行时才能确定的**：登录页的具体选择器、验证码是否区分大小写、
  「最近访问记录」页的真实地址和表格列名、后台会话多久过期。
  程序对这些都做了自动探测 + 兜底，但第一次跑很可能需要按 `discover` 的输出微调一到两处。

这不是设计缺陷，是没有公开文档只能这么办——**把 `discover` 的输出和 `dumps/` 发我，我来调**。

## 十、目录结构

```
access-monitor/
├── run.py                  命令行入口
├── config.example.yaml     配置模板（复制成 config.yaml）
├── .env.example            密钥模板（复制成 .env）
├── requirements.txt
├── monitor/
│   ├── config.py           配置加载（.env + YAML + 环境变量覆盖）
│   ├── session.py          WebVPN/CAS 登录、验证码、登录态保持、防锁账号
│   ├── navigator.py        找到并读取「最近访问记录」页（点菜单 + 记地址 + 钻 iframe）
│   ├── parser.py           HTML 表格 → 访问记录（三层兜底）
│   ├── store.py            SQLite：去重、窗口查询、告警历史、IP 缓存
│   ├── detector.py         滑动窗口突发检测
│   ├── ipintel.py          分层 IP 画像（离线库 + 在线 API + 反查 + RDAP）
│   ├── report.py           告警渲染（文本 / Markdown / HTML 邮件）
│   ├── notify.py           10 个推送通道 + 冷却限流
│   └── monitor.py          主循环
└── tests/                  离线测试，不联网就能跑
```
