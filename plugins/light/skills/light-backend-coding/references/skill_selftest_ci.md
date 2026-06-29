# 技能脚本 `--selftest` 与 CI 执行门

适用于技能包/插件包里维护大量可运行脚本的仓库。目标不是只声明“有 selftest”，而是 CI 能实际执行并防止假阳性。

## 分阶段治理

1. **清单一致性 gate**
   - 从 canonical 清单（如 `WHATS_INCLUDED.md` 的可运行脚本表）精确解析 `(skill_slug, script_name)`。
   - 校验：文件存在、清单不陈旧、不重复、脚本可 `py_compile`、有真实 AST 级 `if __name__ == "__main__"`。

2. **显式 selftest marker gate**
   - 不要只搜 `selftest` 字样；必须要求源码里有显式 `--selftest`。
   - 否则 docstring/默认 demo/旧注释会造成假阳性。

3. **实际执行 gate**
   - 新增 runner，发现全部 `skills/light-*/scripts/*.py`，逐个执行：
     ```bash
     python <script> --selftest
     ```
   - 失败/超时 hard fail；输出最慢脚本列表和分组统计。
   - Runner 本身尽量纯 stdlib；第三方依赖放到 workflow 安装步骤。

## 自测入口规范

- 新脚本优先支持唯一显式入口：`--selftest`。
- 可以保留历史无参自测，但不要让“无参数 demo”冒充 selftest。
- 旧脚本若保留无参自测，入口应严格接受：无参或唯一 `--selftest`；额外未知参数必须非零退出，例如：
  ```python
  if len(sys.argv) > 2 or (len(sys.argv) == 2 and sys.argv[1] != "--selftest"):
      raise SystemExit(f"usage: python {sys.argv[0]} [--selftest]")
  _selftest()
  ```
- 对 argparse 脚本：加 `--selftest` 参数，在解析后优先执行 `_selftest()`。

## 自测内容要求

- 离线：不依赖 DOI/Crossref/OpenAlex/S2、账号、LibreOffice、网络等外部状态。
- 使用合成数据、monkeypatch/fake 函数或 `TemporaryDirectory`。
- 包含真实断言，不只是打印 demo。
- 图表/文档类自测生成物写到临时目录并验证文件存在和非空。
- 可选依赖：可用时验证真实产物；不可用时断言降级/skip 路径，而不是把环境缺失当逻辑失败。

## Review 特别检查

- 逐个运行新增/修改脚本的 `--selftest`。
- 对旧式简单入口，再检查 `--selftest --unknown` 必须非零退出，防止吞参数。
- `git status --short` 应无自测生成物。
- 静态扫描新增行：secret、`shell=True`/`os.system`、`eval`/`exec`、`pickle.loads`、SQL 字符串拼接。
