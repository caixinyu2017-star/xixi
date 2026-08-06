# -*- coding: utf-8 -*-
"""Package-level check: every relationship target exists, every part has a
content type, and the slide list is consistent. Catches the kind of breakage
PowerPoint reports as “需要修复” long before a human opens the file."""
import os, re, sys, zipfile

PR = 'http://schemas.openxmlformats.org/package/2006/relationships'


def _resolve(base, target):
    if target.startswith('/'):
        return target.lstrip('/')
    d = os.path.dirname(os.path.dirname(base))
    return os.path.normpath(os.path.join(d, target)).replace('\\', '/')


def validate(path):
    bad = []
    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
        ct = z.read('[Content_Types].xml').decode('utf-8')
        defaults = set(re.findall(r'<Default Extension="([^"]+)"', ct))
        overrides = set(re.findall(r'<Override PartName="/([^"]+)"', ct))

        for n in names:
            if n.endswith('/') or n == '[Content_Types].xml':
                continue
            ext = n.rsplit('.', 1)[-1].lower()
            if n not in overrides and ext not in defaults:
                bad.append(f'无内容类型: {n}')

        for n in sorted(names):
            if not n.endswith('.rels'):
                continue
            for m in re.finditer(r'Target="([^"]+)"(?:\s+TargetMode="(\w+)")?',
                                 z.read(n).decode('utf-8')):
                if m.group(2) == 'External':
                    continue
                t = _resolve(n, m.group(1))
                if t not in names:
                    bad.append(f'关系指向不存在的部件: {n} -> {m.group(1)}')

        pres = z.read('ppt/presentation.xml').decode('utf-8')
        rels = z.read('ppt/_rels/presentation.xml.rels').decode('utf-8')
        rid2t = dict(re.findall(r'Id="([^"]+)"[^>]*Target="([^"]+)"', rels))
        ids = re.findall(r'<p:sldId [^>]*r:id="([^"]+)"', pres)
        for rid in ids:
            if rid not in rid2t:
                bad.append(f'presentation.xml 引用了不存在的关系 {rid}')
        n_slides = len([n for n in names if re.fullmatch(r'ppt/slides/slide\d+\.xml', n)])
        if len(ids) != n_slides:
            bad.append(f'sldIdLst {len(ids)} 条，实际 {n_slides} 张幻灯片')

        notes = [n for n in names if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml', n)]
        media = [n for n in names if n.startswith('ppt/media/')]
    return bad, n_slides, len(notes), len(media)


if __name__ == '__main__':
    for p in sys.argv[1:]:
        bad, ns, nn, nm = validate(p)
        print(f'{os.path.basename(p)}: {ns} 页 / 备注 {nn} / 媒体 {nm} — '
              + ('OK' if not bad else f'{len(bad)} 处问题'))
        for b in bad[:20]:
            print('   ', b)
