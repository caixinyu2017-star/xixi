"""数据流边界打点（systematic-debugging Phase 1.5 反向追踪）。

用途：坏值深埋在调用栈里时，给每个函数边界打点，一次跑出
入参/出参的 shape/dtype/有无 NaN-Inf，定位坏值最早在哪一层产生，
然后去**源头**修，而非在症状处修。

真实可跑：`python boundary_trace.py` 触发文末合成自测（无需外部数据）。
"""

from __future__ import annotations

import functools
import sys
from collections.abc import Callable
from typing import Any

sys.stdout.reconfigure(encoding="utf-8")  # Windows 控制台默认 GBK，避免中文乱码


def _describe(x: Any) -> str:
    """对任意值给出边界诊断摘要：优先暴露 shape/dtype/NaN-Inf。"""
    shape = getattr(x, "shape", None)
    dtype = getattr(x, "dtype", None)
    parts: list[str] = [type(x).__name__]
    if shape is not None:
        parts.append(f"shape={tuple(shape)}")
    if dtype is not None:
        parts.append(f"dtype={dtype}")
    # 数值数组：报告是否含 NaN/Inf（高频根因），不依赖具体库
    try:
        import math

        if shape is not None and hasattr(x, "__iter__"):
            flat = [float(v) for v in (x.flatten() if hasattr(x, "flatten") else x)]
            if any(math.isnan(v) or math.isinf(v) for v in flat):
                parts.append("HAS_NAN_OR_INF")
        elif isinstance(x, (int, float)):
            if math.isnan(float(x)) or math.isinf(float(x)):
                parts.append("HAS_NAN_OR_INF")
    except (TypeError, ValueError):
        pass
    return "<" + " ".join(parts) + ">"


def trace_boundary(fn: Callable) -> Callable:
    """装饰器：打印进入该函数的实参与返回值的边界摘要。"""

    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        ins = ", ".join(_describe(a) for a in args)
        print(f"[enter {fn.__name__}] in: {ins}")
        out = fn(*args, **kwargs)
        print(f"[exit  {fn.__name__}] out: {_describe(out)}")
        return out

    return wrapper


def _self_test() -> None:
    """合成自测：构造一条产生 NaN 的数据流，演示如何定位最早源头。"""
    import numpy as np

    @trace_boundary
    def load() -> np.ndarray:
        return np.array([1.0, 2.0, 0.0])  # 干净

    @trace_boundary
    def normalize(x: np.ndarray) -> np.ndarray:
        return x / x  # 0/0 -> NaN：根因在这一层，下游会一路带着 NaN

    @trace_boundary
    def aggregate(x: np.ndarray) -> float:
        return float(x.sum())

    print("--- boundary_trace 合成自测：观察 NaN 最早在哪层出现 ---")
    result = aggregate(normalize(load()))
    # 断言：normalize 是 NaN 源头，结果也应为 NaN —— 证明打点能定位源头
    assert result != result, "自测预期结果为 NaN（演示根因在 normalize 层）"
    print("OK: NaN 源头定位在 [exit normalize]，应在该源头修复而非在 aggregate 处")


if __name__ == "__main__":
    _self_test()
