# -*- coding: utf-8 -*-
import course1_a, course1_b, course1_c          # noqa: F401  (side-effect build)
from course1_a import S
from course1_c import EXTRA
from lint import check
from pack import build

# S = [...48 content..., 结课任务(idx49), ] ; insert EXTRA before the closing task
closing = S[49]
slides = S[:49] + EXTRA + [closing]

assert len(slides) == 60, len(slides)
issues = check(slides)
assert not issues, f'{len(issues)} 处布局问题'

out = build(slides, '/home/user/xixi/管理基础课-个体及群体行为分析.pptx',
            title='个体及群体行为分析｜亚德客企业内训')
print('OK ->', out, len(slides), '页')
