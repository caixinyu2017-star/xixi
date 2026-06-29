"""共享 fixture / 路径设置。

把 src/ 加入 import 路径，使 `import example.stats` 在未安装包时也能跑测试。
✅ 已实测：`pip install -e ".[dev]"` 装包成功后，删掉下面的 sys.path hack
仍可 `import example.stats`（解析到已安装包），故正式项目装包后应删除此 hack。
✅ 已实测：`uv sync --extra dev` 同样能装包（uv 0.11.21 / Python 3.11，2026-06），
随后 `uv run ruff/mypy/pytest` 四道质量门全绿；故 README 的 uv 路线已跑通。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
