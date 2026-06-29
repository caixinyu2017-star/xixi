# 技术栈检测呈现模板

`scripts/detect_stack.py` 跑完后，按此模板向用户汇报选型建议。脚本只对清单里真实出现、且命中内置规则的依赖给建议；未命中标 `no signal`，不臆造。

## 汇报结构

```
扫描了 <项目目录>，依据 <清单文件列表>：

技术栈：<按类别列出命中的依赖>
  - 数据处理：pandas → 当前数据 <2GB 够用，更大切 polars/dask
  - 后端：fastapi → OpenAPI 自动生成，便于确定性调用
  - ...

环境/复现：
  - <检测到 uv.lock / conda / Dockerfile 的对应建议>

无内置规则的依赖（no signal，未给建议）：<列表>

下一步建议：<结合 references/decision_matrix.md 的阈值，给 1-2 条具体行动>
```

## 用法

```bash
# 扫描真实项目
python scripts/detect_stack.py /path/to/project

# 机器可读
python scripts/detect_stack.py /path/to/project --json

# 无项目时自检（合成清单，验证脚本可用）
python scripts/detect_stack.py --self-test
```

## 边界（诚实）

- 仅解析 package.json / pyproject.toml / requirements.txt / environment.yml(.yaml)。
- 规则表是经验映射，覆盖常见库；冷门/私有库进 no-signal，需人工判断。
- 建议是“起点”，临界规模（如数据 ~2GB）应实测而非照搬阈值。
