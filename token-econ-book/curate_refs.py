# -*- coding: utf-8 -*-
"""将核实后的 refs_raw.json 整理为 references.py 与 data/refkeys.txt。

规则：剔除 verified=false；按（第一作者+年+题名前缀）去重；key 唯一化；
同作者同年多篇加 a/b 后缀（intext 同步）；统计 2021+ 占比。
"""
import json
import os
import re
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
raw = json.load(open(os.path.join(HERE, 'data', 'refs_raw.json'), encoding='utf-8'))

# 边缘旧文献裁剪名单（保证 2021+ 占比过半；理论/方法经典、政策文件、教育经典一律保留）
DROP = set()   # 本书暂无需剔除的条目


seen_title = {}
by_key = {}
order = []
for r in raw:
    if not r.get('verified') or r.get('key') in DROP:
        continue
    gb = r['gb'].strip()
    # 去重指纹：题名片段
    m = re.split(r'[\.。]\s*', gb)
    title = (m[1] if len(m) > 1 else gb)
    fp = re.sub(r'[^0-9a-z一-鿿]', '', unicodedata.normalize('NFKC', title).lower())[:40]
    if fp in seen_title:
        continue
    seen_title[fp] = True
    key = re.sub(r'[^0-9a-z]', '', r['key'].lower()) or f"ref{len(order)}"
    base = key
    i = 98  # 'b'
    while key in by_key:
        key = f"{base}{chr(i)}"
        i += 1
    r = dict(r)
    r['key'] = key
    by_key[key] = r
    order.append(key)

# intext 冲突（同 intext 不同文献）→ 加 a/b
intext_map = {}
for k in order:
    it = by_key[k]['intext']
    intext_map.setdefault(it, []).append(k)
for it, ks in intext_map.items():
    if len(ks) > 1:
        for idx, k in enumerate(ks):
            suf = chr(ord('a') + idx)
            year_m = re.search(r'(\d{4})', it)
            if year_m:
                y = year_m.group(1)
                by_key[k]['intext'] = it.replace(y, y + suf)
                by_key[k]['gb'] = by_key[k]['gb']  # gb 不动

n_new = sum(1 for k in order if by_key[k]['year'] >= 2021)
print(f"verified & deduped: {len(order)}; 2021+: {n_new} ({n_new/len(order)*100:.0f}%)")
print(f"zh: {sum(1 for k in order if by_key[k]['lang']=='zh')}, en: {sum(1 for k in order if by_key[k]['lang']=='en')}")

with open(os.path.join(HERE, 'references.py'), 'w', encoding='utf-8') as f:
    f.write('''# -*- coding: utf-8 -*-
"""参考文献数据库与引用引擎（GB/T 7714 顺序编码制 + 文中作者—年）。
条目经联网核实（CrossRef/CNKI/期刊官网）。
"""

# (key, 文中引用串, GB 著录)
_DATA = [
''')
    for k in order:
        r = by_key[k]
        it = r['intext'].replace("'", "\\'")
        gb = r['gb'].replace("\\", "\\\\").replace("'", "\\'")
        f.write(f" ('{k}', '{it}',\n  '{gb}'),\n")
    f.write(''']

REFS = {k: {'intext': it, 'gb': gb} for k, it, gb in _DATA}
_ORDER = []


def c(key, paren=True, prefix='', suffix=''):
    """登记并返回文中引用串。paren=False 用于句法嵌入。"""
    if key not in REFS:
        raise KeyError(f'未知文献 key: {key}')
    if key not in _ORDER:
        _ORDER.append(key)
    it = REFS[key]['intext']
    body = f'{prefix}{it}{suffix}'
    return f'（{body}）' if paren else body


def _year_of(key):
    import re as _re
    m = _re.search(r'(\\d{4})', REFS[key]['intext'])
    return int(m.group(1)) if m else 9999


def cc(*keys):
    """合引：自动按年份升序排列（同年保持传入顺序）。"""
    for k in keys:
        if k not in REFS:
            raise KeyError(f'未知文献 key: {k}')
    parts = []
    for k in sorted(keys, key=_year_of):
        if k not in _ORDER:
            _ORDER.append(k)
        parts.append(REFS[k]['intext'])
    return '（' + '；'.join(parts) + '）'


def gb_ordered():
    used = list(_ORDER)
    rest = [k for k in REFS if k not in _ORDER]
    return [REFS[k]['gb'] for k in used + rest]


def n_used():
    return len(_ORDER)


def reset():
    _ORDER.clear()
''')

with open(os.path.join(HERE, 'data', 'refkeys.txt'), 'w', encoding='utf-8') as f:
    f.write('# key → 文中引用（c(key) 输出加外括号）。仅可使用本清单中的 key。\n')
    for k in order:
        r = by_key[k]
        f.write(f"{k}\t（{r['intext']}）\t{r['gb'][:60]}\n")
print('written references.py, data/refkeys.txt')
