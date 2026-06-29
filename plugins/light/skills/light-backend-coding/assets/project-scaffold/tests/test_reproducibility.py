"""reproducibility 模块测试：演示「核心行为零依赖可测 + 可选后端按需跳过」。

scaffold 无运行期依赖，故：
  - stdlib random 的可复现性 —— 必跑，永远可断言。
  - numpy / torch 相关 —— 用 importorskip，未装则该用例跳过而非失败，
    保证 `uv run pytest` 在裸环境也全绿。
"""

import os
import random

import pytest

from example.reproducibility import SeedReport, set_global_seed


def test_set_seed_makes_python_random_reproducible():
    set_global_seed(123)
    first = [random.random() for _ in range(5)]
    set_global_seed(123)
    second = [random.random() for _ in range(5)]
    assert first == second


def test_report_marks_python_and_hashseed():
    report = set_global_seed(7)
    assert isinstance(report, SeedReport)
    assert report.seed == 7
    assert report.python is True
    assert os.environ["PYTHONHASHSEED"] == "7"


def test_negative_seed_raises():
    with pytest.raises(ValueError, match="非负整数"):
        set_global_seed(-1)


def test_numpy_reproducible_if_available():
    np = pytest.importorskip("numpy")
    report = set_global_seed(99)
    assert report.numpy is True
    first = np.random.rand(4)
    set_global_seed(99)
    second = np.random.rand(4)
    assert (first == second).all()


def test_torch_reproducible_if_available():
    torch = pytest.importorskip("torch")
    report = set_global_seed(99)
    assert report.torch is True
    first = torch.rand(4)
    set_global_seed(99)
    second = torch.rand(4)
    assert torch.equal(first, second)
