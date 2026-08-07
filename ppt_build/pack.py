# -*- coding: utf-8 -*-
"""Write a deck by reusing the source template package (masters, layouts,
theme, chalkboard background media) and replacing every slide."""
import os, re, shutil, zipfile

TEMPLATE = '/root/.claude/uploads/c21e8928-f36a-5709-a57b-0dbac4f75a52/02316753-01._________.pptx'
LAYOUT_KEEP = 'slideLayout18.xml'      # 内容与标题, inherits slideMaster2 (chalkboard)

CT = 'http://schemas.openxmlformats.org/package/2006/content-types'
PR = 'http://schemas.openxmlformats.org/package/2006/relationships'
RT = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
NS_P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
NS_A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
MIME = {'png': 'image/png', 'jpg': 'image/jpeg', 'jpeg': 'image/jpeg',
        'gif': 'image/gif', 'webp': 'image/webp', 'svg': 'image/svg+xml'}


def _esc(t):
    return (str(t).replace('&', '&amp;').replace('<', '&lt;')
            .replace('>', '&gt;'))


def _ensure_default(parts, ext):
    ct = parts['[Content_Types].xml'].decode('utf-8')
    if f'Extension="{ext}"' in ct:
        return
    ct = ct.replace('<Types ', '<Types ', 1)
    ins = f'<Default Extension="{ext}" ContentType="{MIME.get(ext, "image/png")}"/>'
    ct = re.sub(r'(<Types[^>]*>)', r'\1' + ins, ct, count=1)
    parts['[Content_Types].xml'] = ct.encode('utf-8')


def _notes_xml(paragraphs):
    def para(t):
        if not t:
            return ('<a:p><a:endParaRPr lang="zh-CN" altLang="en-US" '
                    'sz="1200" dirty="0"/></a:p>')
        rpr = ('<a:rPr lang="zh-CN" altLang="en-US" sz="1200" dirty="0"/>')
        return (f'<a:p><a:r>{rpr}<a:t>'
                + t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                + '</a:t></a:r></a:p>')
    body = ''.join(para(p) for p in paragraphs)
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
            f'<p:notes xmlns:a="{NS_A}" xmlns:r="{RT}" xmlns:p="{NS_P}">'
            '<p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/>'
            '<p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm>'
            '<a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/>'
            '<a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
            '<p:sp><p:nvSpPr><p:cNvPr id="2" name="备注占位符 1"/>'
            '<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
            '<p:nvPr><p:ph type="body" idx="1"/></p:nvPr></p:nvSpPr>'
            '<p:spPr/><p:txBody><a:bodyPr/><a:lstStyle/>'
            f'{body}</p:txBody></p:sp>'
            '</p:spTree></p:cSld>'
            '<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:notes>')


def _resolve(base, target):
    """Resolve a rel Target against the part that declares it."""
    if target.startswith('/'):
        return target.lstrip('/')
    d = os.path.dirname(os.path.dirname(base))      # strip /_rels/<name>
    return os.path.normpath(os.path.join(d, target)).replace('\\', '/')


def _gc(parts):
    """Keep only parts reachable from the package root, then prune
    [Content_Types].xml overrides for whatever was dropped."""
    keep, queue = set(), ['_rels/.rels']
    while queue:
        cur = queue.pop()
        if cur in keep or cur not in parts:
            continue
        keep.add(cur)
        rels = (cur if cur.endswith('.rels')
                else f'{os.path.dirname(cur)}/_rels/{os.path.basename(cur)}.rels')
        if rels in parts:
            keep.add(rels)
            for m in re.finditer(r'Target="([^"]+)"(?:\s+TargetMode="(\w+)")?',
                                 parts[rels].decode('utf-8')):
                if m.group(2) == 'External':
                    continue
                queue.append(_resolve(rels, m.group(1)))
    keep.add('[Content_Types].xml')
    dropped = set(parts) - keep

    ct = parts['[Content_Types].xml'].decode('utf-8')
    for d in dropped:
        ct = re.sub(r'<Override PartName="/%s"[^>]*/>' % re.escape(d), '', ct)
    parts = {k: v for k, v in parts.items() if k in keep}
    parts['[Content_Types].xml'] = ct.encode('utf-8')
    return parts


def build(slides, out_path, title='', author='嘉兴大学商学院'):
    """slides: list of Slide objects (in order)."""
    with zipfile.ZipFile(TEMPLATE) as z:
        parts = {n: z.read(n) for n in z.namelist()}

    # ---- drop every original slide + notesSlide -------------------
    for n in list(parts):
        if re.match(r'ppt/(slides|notesSlides)/', n):
            del parts[n]

    # ---- write new slide parts -----------------------------------
    notes_for = {}
    for i, sl in enumerate(slides, 1):
        parts[f'ppt/slides/slide{i}.xml'] = sl.xml().encode('utf-8')
        rels = [f'<Relationship Id="rId1" Type="{RT}/slideLayout" '
                f'Target="../slideLayouts/{LAYOUT_KEEP}"/>']

        for rid, src in getattr(sl, 'pictures', []):
            ext = os.path.splitext(src)[1].lower().lstrip('.') or 'png'
            media = f'ppt/media/gen{i}_{rid}.{ext}'
            with open(src, 'rb') as fh:
                parts[media] = fh.read()
            rels.append(f'<Relationship Id="{rid}" Type="{RT}/image" '
                        f'Target="../media/{os.path.basename(media)}"/>')
            _ensure_default(parts, ext)

        if getattr(sl, 'notes_text', None):
            n = len(notes_for) + 1
            notes_for[n] = (i, sl.notes_text)
            rels.append(f'<Relationship Id="rIdNS" Type="{RT}/notesSlide" '
                        f'Target="../notesSlides/notesSlide{n}.xml"/>')

        parts[f'ppt/slides/_rels/slide{i}.xml.rels'] = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
            f'<Relationships xmlns="{PR}">{"".join(rels)}</Relationships>'
        ).encode('utf-8')

    # ---- notes slides --------------------------------------------
    for n, (slide_no, body) in notes_for.items():
        parts[f'ppt/notesSlides/notesSlide{n}.xml'] = _notes_xml(body).encode('utf-8')
        parts[f'ppt/notesSlides/_rels/notesSlide{n}.xml.rels'] = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
            f'<Relationships xmlns="{PR}">'
            f'<Relationship Id="rId1" Type="{RT}/notesMaster" '
            'Target="../notesMasters/notesMaster1.xml"/>'
            f'<Relationship Id="rId2" Type="{RT}/slide" '
            f'Target="../slides/slide{slide_no}.xml"/>'
            '</Relationships>').encode('utf-8')

    # ---- presentation.xml : rebuild <p:sldIdLst> ------------------
    pres = parts['ppt/presentation.xml'].decode('utf-8')
    ids = ''.join(f'<p:sldId id="{255 + i}" r:id="rIdSL{i}"/>'
                  for i in range(1, len(slides) + 1))
    pres = re.sub(r'<p:sldIdLst>.*?</p:sldIdLst>', f'<p:sldIdLst>{ids}</p:sldIdLst>',
                  pres, flags=re.S)
    parts['ppt/presentation.xml'] = pres.encode('utf-8')

    # ---- presentation rels : drop old slide rels, add new --------
    rels = parts['ppt/_rels/presentation.xml.rels'].decode('utf-8')
    rels = re.sub(r'<Relationship[^>]*?/slides/[^>]*?/>', '', rels)
    new = ''.join(
        f'<Relationship Id="rIdSL{i}" Type="http://schemas.openxmlformats.org/'
        f'officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>'
        for i in range(1, len(slides) + 1))
    rels = rels.replace('</Relationships>', new + '</Relationships>')
    parts['ppt/_rels/presentation.xml.rels'] = rels.encode('utf-8')

    # ---- [Content_Types].xml -------------------------------------
    ct = parts['[Content_Types].xml'].decode('utf-8')
    ct = re.sub(r'<Override PartName="/ppt/(slides|notesSlides)/[^"]*"[^>]*/>', '', ct)
    ov = ''.join(
        f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType='
        '"application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        for i in range(1, len(slides) + 1))
    ov += ''.join(
        f'<Override PartName="/ppt/notesSlides/notesSlide{n}.xml" ContentType='
        '"application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml"/>'
        for n in notes_for)
    ct = ct.replace('</Types>', ov + '</Types>')
    parts['[Content_Types].xml'] = ct.encode('utf-8')

    # ---- docProps -------------------------------------------------
    # titles carry things like 「价值 & 开发」 — an unescaped & makes the whole
    # package invalid XML and PowerPoint reports the file as corrupt
    title, author = _esc(title), _esc(author)
    if 'docProps/core.xml' in parts:
        c = parts['docProps/core.xml'].decode('utf-8')
        c = re.sub(r'<dc:title>.*?</dc:title>', f'<dc:title>{title}</dc:title>', c, flags=re.S)
        c = re.sub(r'<dc:creator>.*?</dc:creator>', f'<dc:creator>{author}</dc:creator>', c, flags=re.S)
        parts['docProps/core.xml'] = c.encode('utf-8')
    if 'docProps/app.xml' in parts:
        a = parts['docProps/app.xml'].decode('utf-8')
        a = re.sub(r'<Slides>\d+</Slides>', f'<Slides>{len(slides)}</Slides>', a)
        a = re.sub(r'<TitlesOfParts>.*?</TitlesOfParts>', '', a, flags=re.S)
        a = re.sub(r'<HeadingPairs>.*?</HeadingPairs>', '', a, flags=re.S)
        parts['docProps/app.xml'] = a.encode('utf-8')

    # ---- garbage-collect parts the deleted source slides used ----
    parts = _gc(parts)

    os.makedirs(os.path.dirname(out_path) or '.', exist_ok=True)
    if os.path.exists(out_path):
        os.remove(out_path)
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for n, b in parts.items():
            z.writestr(n, b)
    return out_path
