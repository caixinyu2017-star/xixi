"""可复现性工具：一处设全局随机种子，覆盖 stdlib / numpy / torch。

科研代码的首要复现门槛是随机性可控。本模块演示「能设的都设、装了才设、
缺了就降级」的稳妥写法：scaffold 默认零运行期依赖，numpy/torch 未必装，
故全部用「尝试导入，失败则跳过」，绝不因缺包而抛错。

用法::

    from example.reproducibility import set_global_seed
    set_global_seed(42)   # 训练 / 实验入口最早处调用一次

返回值是一份「实际设置了哪些后端」的报告，便于在日志里留痕、复现核对。
"""

from __future__ import annotations

import os
import random
from dataclasses import dataclass


@dataclass(frozen=True)
class SeedReport:
    """记录 set_global_seed 实际作用到了哪些后端，便于日志留痕。

    seed:    本次使用的种子值。
    python:  是否设了 stdlib random + PYTHONHASHSEED。
    numpy:   是否设了 numpy 全局种子（未装则 False）。
    torch:   是否设了 torch 种子（未装则 False）。
    cudnn:   是否启用了 cudnn 确定性模式（无 CUDA / 未装 torch 则 False）。
    """

    seed: int
    python: bool
    numpy: bool
    torch: bool
    cudnn: bool


def set_global_seed(seed: int = 42, *, deterministic_cudnn: bool = True) -> SeedReport:
    """固定全局随机种子，覆盖 stdlib / numpy / torch，缺包自动降级。

    Args:
        seed: 种子值，需非负整数（哈希种子等场景要求）。
        deterministic_cudnn: 装了 torch 且有 CUDA 时，是否开启 cudnn 确定性
            （`deterministic=True` + `benchmark=False`）。会牺牲少量速度换可复现。

    Returns:
        SeedReport: 标明各后端是否实际生效。

    Raises:
        ValueError: seed 为负数时。
    """
    if seed < 0:
        raise ValueError(f"seed 需为非负整数，收到 {seed}")

    # 1) PYTHONHASHSEED 影响哈希随机化，须在进程级固定（部分仅新进程生效，
    #    但写下它能让 subprocess / 重启场景拿到确定值）。
    os.environ["PYTHONHASHSEED"] = str(seed)

    # 2) stdlib random —— 永远可用。
    random.seed(seed)

    # 3) numpy —— 装了才设。
    numpy_set = False
    try:
        import numpy as np

        np.random.seed(seed)
        numpy_set = True
    except ImportError:
        pass

    # 4) torch —— 装了才设；CUDA 存在再设 cudnn 确定性。
    torch_set = False
    cudnn_set = False
    try:
        import torch

        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
            if deterministic_cudnn:
                torch.backends.cudnn.deterministic = True
                torch.backends.cudnn.benchmark = False
                cudnn_set = True
        torch_set = True
    except ImportError:
        pass

    return SeedReport(
        seed=seed,
        python=True,
        numpy=numpy_set,
        torch=torch_set,
        cudnn=cudnn_set,
    )
