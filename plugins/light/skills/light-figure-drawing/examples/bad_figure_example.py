#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bad_figure_example.py — **故意违规**的绘图代码，用作 figure_integrity_lint 的端到端命中样例
+ 用户对照教材（这些都是审稿人最爱抓的图表诚实性陷阱，别学）。

跑 `python scripts/figure_integrity_lint.py --file examples/bad_figure_example.py`
应命中多条 *_TRUNCATE / *_NO_ERR / TWIN_AXIS / RAINBOW_CMAP 等警告。
对照 examples 里的正例（example_matplotlib.py 等）看正确做法。

注意：本文件**只为触发 lint**，不追求能跑出好图；勿复制其中任何反模式到真实论文。
"""
import matplotlib.pyplot as plt
import numpy as np


def make_misleading_figure():
    fig, ax = plt.subplots()

    # 反模式 1：bar 无误差棒（掩盖不确定性）
    ax.bar(["baseline", "ours"], [0.80, 0.82])

    # 反模式 2：y 轴截断（0.80→0.82 的 0.02 差被放大成"巨大提升"）
    ax.set_ylim(bottom=0.78)            # 关键字形式，旧 lint 漏检

    # 反模式 3：双 y 轴（制造伪相关）
    ax2 = ax.twinx()
    ax2.plot([0, 1], [100, 5], color="red")

    # 反模式 4：rainbow/jet 配色（非感知均匀、非色盲安全）
    data = np.random.rand(10, 10)
    fig2, axh = plt.subplots()
    axh.imshow(data, cmap="jet")

    # 反模式 5：seaborn barplot 也无误差类型声明（旧 lint 漏检 seaborn）
    # import seaborn as sns
    # sns.barplot(x="method", y="acc", data=df)   # 取消注释会再触发一条 BAR_NO_ERR

    return fig


if __name__ == "__main__":
    print("这是 lint 的反例教材文件，不画真实图。"
          "跑 figure_integrity_lint.py --file 本文件 应命中多条诚实性警告。")
