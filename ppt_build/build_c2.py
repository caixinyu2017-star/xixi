# -*- coding: utf-8 -*-
import course2_a, course2_b, course2_c          # noqa: F401
from course2_a import S
from course2_c import EXTRA
from lint import check
from pack import build

closing = S[49]                    # 结课任务 must stay last
slides = S[:49] + EXTRA + [closing]

assert len(slides) == 60, len(slides)
issues = check(slides)
assert not issues, f'{len(issues)} 处布局问题'

out = build(slides, '/home/user/xixi/管理技能课-问题分析与解决.pptx',
            title='问题分析与解决｜亚德客企业内训')
print('OK ->', out, len(slides), '页')
