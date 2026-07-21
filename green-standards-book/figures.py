# -*- coding: utf-8 -*-
"""全部分析图：由 figures_a.py（第2—7章）与 figures_b.py（第8—13章）生成。"""
import subprocess, sys
for m in ('figures_a.py','figures_b.py'):
    subprocess.run([sys.executable, m], check=True)
print('all figures done')
