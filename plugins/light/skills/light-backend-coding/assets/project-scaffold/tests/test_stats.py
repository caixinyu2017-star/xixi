"""stats 模块测试：演示 assert 内省 + parametrize + 异常断言。

对应 TDD 流程：每个行为先有一个被看着失败过的测试。
"""

import pytest

from example.stats import mean


@pytest.mark.parametrize(
    "values,expected",
    [
        ([1, 2, 3], 2.0),
        ([10], 10.0),
        ([-2, 2], 0.0),
    ],
)
def test_mean_typical(values, expected):
    assert mean(values) == expected


def test_mean_empty_raises():
    with pytest.raises(ValueError, match="至少一个数值"):
        mean([])
