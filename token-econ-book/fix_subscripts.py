# -*- coding: utf-8 -*-
"""把正文与表格中残留的 ASCII 下标写法改写为引擎富文本标记 {sub:}。

白名单驱动（token 清单由审计脚本实测得到），只在 content_chNN.py 的普通字符串字面量中
替换，跳过 r'' 原始串（LaTeX 公式）、$...$ 数学区与既有 {sub:} 片段，确保不误伤
文件路径（figs/fig9_1.png）与结果字典键（by_job_2025 等）。
"""
import re
import sys

TOKENS = ['SMI_kt', 'VMI_t', 'D_kt', 'Q_kt', 'R_E', 'R_U', 'c_E', 'c_U', 'c_G',
          'λ_E', 'λ_U', 'λ_x', 'λ_y', 'λ_z', 'u_t', 'v_t', 'm_t', 'θ_t',
          'x_c', 'δ_a', 'φ0', 'φ1', 'ψ0', 'ψ1']
# 长 token 先替换，避免前缀冲突
TOKENS.sort(key=len, reverse=True)
# 词边界保护：token 前后不得再接字母/数字/下划线，避免误伤 x_crit、by_job_2025 等标识符
RE_TOK = re.compile(r'(?<![A-Za-z0-9_])(?:' + '|'.join(re.escape(t) for t in TOKENS) + r')(?![A-Za-z0-9_])')
SKIP = re.compile(r'\$[^$]*\$|\{sub:[^}]*\}|\{sup:[^}]*\}')


def _sub(seg):
    def one(m):
        t = m.group(0)
        if '_' in t:
            base, sub = t.split('_', 1)
        else:
            base, sub = t[0], t[1:]
        return f'{base}{{sub:{sub}}}'
    return RE_TOK.sub(one, seg)


def fix_text(s):
    out, pos = [], 0
    for m in SKIP.finditer(s):
        out.append(_sub(s[pos:m.start()]))
        out.append(m.group(0))
        pos = m.end()
    out.append(_sub(s[pos:]))
    return ''.join(out)


def process(path):
    src = open(path, encoding='utf-8').read()
    n = [0]

    def repl(m):
        prefix, q, body = m.group(1), m.group(2), m.group(3)
        if prefix:                       # r'' / b'' / f'' 原始串（LaTeX）不动
            return m.group(0)
        new = fix_text(body)
        if new != body:
            n[0] += 1
        return f'{q}{new}{q}'

    out = re.sub(r"([rbfRBF]?)(['\"])((?:[^'\"\\\n]|(?!\2)['\"])*?)\2", repl, src)
    if n[0]:
        open(path, 'w', encoding='utf-8').write(out)
    return n[0]


if __name__ == '__main__':
    for p in sys.argv[1:]:
        print(p, '修改字符串数:', process(p))
