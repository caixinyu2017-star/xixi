"""示例模块：演示单一职责 + 输入校验 + 异常处理 + 固定可复现行为。

真实可跑：`uv run pytest` 应见 tests/test_stats.py 全绿。
"""

from __future__ import annotations

from collections.abc import Sequence


def mean(values: Sequence[float]) -> float:
    """返回数值序列的算术平均。

    输入校验在源头做（参见 systematic-debugging：在数据源头修而非症状处）。

    Raises:
        ValueError: 序列为空时无法定义平均值。
    """
    if not values:
        raise ValueError("mean() 需要至少一个数值，收到空序列")
    return sum(values) / len(values)
