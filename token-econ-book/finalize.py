# -*- coding: utf-8 -*-
"""本轮修订的收口脚本：机制图版面加宽 → 引注去括号 → 结构审计 → 装配 → 核验。

用法：python3 finalize.py [--check-only]
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# 机制图（D 型）：改用 gpt-image-2 重绘后字号仍受版面宽度约束，
# 统一放大到 14.8 cm（版心 15.0 cm，留 0.2 cm 安全余量）。
D_FIGS = {'fig1_1', 'fig1_2', 'fig2_2', 'fig3_1', 'fig5_1', 'fig6_1', 'fig6_2',
          'fig7_1', 'fig8_1', 'fig9_1', 'fig10_1', 'fig10_2', 'fig11_1',
          'fig12_1', 'fig13_1', 'fig13_3', 'fig14_1'}
D_WIDTH = 14.8


def widen_mechanism_figures():
    """把 D 型图的 width_cm 统一改为 14.8。"""
    changed = []
    for fn in sorted(os.listdir(HERE)):
        if not re.fullmatch(r'content_ch\d+\.py', fn):
            continue
        p = os.path.join(HERE, fn)
        lines = open(p, encoding='utf-8').read().split('\n')
        hit = False
        for i, ln in enumerate(lines):
            m = re.search(r"'fig':\s*'figs/(fig\d+_\d+)\.png'", ln)
            if not m or m.group(1) not in D_FIGS:
                continue
            # width_cm 可能落在本行或紧随其后的两行内
            for j in range(i, min(i + 3, len(lines))):
                if "'width_cm'" in lines[j]:
                    new = re.sub(r"'width_cm':\s*[\d.]+", f"'width_cm': {D_WIDTH}", lines[j])
                    if new != lines[j]:
                        lines[j] = new
                        hit = True
                        changed.append(f'{fn}:{m.group(1)}')
                    break
        if hit:
            open(p, 'w', encoding='utf-8').write('\n'.join(lines))
    return changed


def strip_corner_quotes_in_refs():
    """references.py 中机构作者的文中引用串误加了「」，去掉；不动作者与年份本身。"""
    p = os.path.join(HERE, 'references.py')
    s = open(p, encoding='utf-8').read()
    new = re.sub(r"(\(\s*'[^']+',\s*)'「([^」]+)」'", r"\1'\2'", s)
    n = len(re.findall(r"(\(\s*'[^']+',\s*)'「([^」]+)」'", s))
    if n:
        open(p, 'w', encoding='utf-8').write(new)
    return n


def scan_corner_quotes():
    """全仓扫描仍残留直角引号的书稿源文件。"""
    left = []
    for fn in sorted(os.listdir(HERE)):
        if not fn.endswith('.py'):
            continue
        s = open(os.path.join(HERE, fn), encoding='utf-8').read()
        c = s.count('「') + s.count('」') + s.count('『') + s.count('』')
        if c:
            left.append((fn, c))
    return left


def run(cmd):
    print(f'$ {cmd}')
    r = subprocess.run(cmd, shell=True, cwd=HERE, capture_output=True, text=True)
    out = (r.stdout or '') + (r.stderr or '')
    print(out[-3000:])
    return r.returncode, out


def main():
    check_only = '--check-only' in sys.argv

    if not check_only:
        ch = widen_mechanism_figures()
        print(f'机制图版面加宽至 {D_WIDTH} cm：{len(ch)} 处')
        n = strip_corner_quotes_in_refs()
        print(f'参考文献引用串去直角引号：{n} 条')

    left = scan_corner_quotes()
    print('仍含直角引号的源文件：', left if left else '无')

    rc, _ = run('python3 audit.py')
    if rc:
        print('审计失败，终止'); return 1
    rc, _ = run('python3 assemble.py')
    if rc:
        print('装配失败，终止'); return 1
    run('timeout 900 soffice --headless --convert-to pdf --outdir build '
        'build/*.docx >/dev/null 2>&1; pdfinfo build/*.pdf | grep -E "Pages|Page size"')
    return 0


if __name__ == '__main__':
    sys.exit(main())
