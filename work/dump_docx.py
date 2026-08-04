import zipfile, re, sys, xml.etree.ElementTree as ET
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
def dump(path):
    z=zipfile.ZipFile(path)
    xml=z.read('word/document.xml').decode('utf8')
    root=ET.fromstring(xml)
    body=root.find('w:body',NS)
    out=[]
    def para_text(p):
        return ''.join(t.text or '' for t in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'))
    for el in body:
        tag=el.tag.split('}')[1]
        if tag=='p':
            style=''
            pPr=el.find('w:pPr',NS)
            if pPr is not None:
                ps=pPr.find('w:pStyle',NS)
                if ps is not None: style=ps.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
            txt=para_text(el)
            has_img = el.find('.//{http://schemas.openxmlformats.org/drawingml/2006/main}blip') is not None or '<w:pict' in ET.tostring(el).decode('utf8')
            if has_img: txt = (txt+' [[IMAGE]]').strip()
            if txt.strip():
                out.append((f'[{style}] ' if style else '')+txt)
        elif tag=='tbl':
            out.append('<<TABLE>>')
            for tr in el.findall('w:tr',NS):
                cells=[]
                for tc in tr.findall('w:tc',NS):
                    cells.append(' '.join(para_text(p) for p in tc.findall('w:p',NS)).strip())
                out.append(' | '.join(cells))
            out.append('<</TABLE>>')
    return '\n'.join(out)
if __name__=='__main__':
    print(dump(sys.argv[1]))
