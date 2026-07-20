# -*- coding: utf-8 -*-
"""内容撰写辅助：加载实证结果、格式化回归单元格、引用快捷方式。"""
import json
import os
import references as _R
from references import c, cc

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, 'data', 'results.json'), encoding='utf-8'))


def star(p):
    return '***' if p < 0.01 else ('**' if p < 0.05 else ('*' if p < 0.1 else ''))


def cell(entry, dec=3):
    """回归系数单元格：系数+星号 换行 (标准误)。entry 为 {coef,se,t,p}。"""
    co = entry['coef']
    return f"{co:.{dec}f}{star(entry['p'])}\n({entry['se']:.{dec}f})"


def coef(entry, dec=3):
    return f"{entry['coef']:.{dec}f}"


def t_of(entry):
    return f"{entry['t']:.2f}"


def se_of(entry, dec=3):
    return f"{entry['se']:.{dec}f}"


def sig(entry):
    return star(entry['p'])


def pct(x, dec=1):
    return f"{x*100:.{dec}f}%"


# 常用取值
NUMI06 = R['numi_national']['2006']
NUMI23 = R['numi_national']['2023']
ACE06 = R['ace_national']['2006']
ACE23 = R['ace_national']['2023']
SEG06 = R['seg_national']['2006']
SEG23 = R['seg_national']['2023']
BASE = R['baseline']['m3']['numi']         # 基准全控制
LOSS06 = R['tfp_loss']['2006']
LOSS23 = R['tfp_loss']['2023']
DID = R['did']['did']
IV = R['iv']
