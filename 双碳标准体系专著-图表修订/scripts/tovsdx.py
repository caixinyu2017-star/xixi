# -*- coding: utf-8 -*-
"""把 out/svg/ 的矢量图逐张转换为 Visio .vsdx：
SVG --(inkscape)--> EMF --(嵌入 Foreign 形状)--> 单页 .vsdx
EMF 为矢量图元，在 Visio 中右键“组合→取消组合”即可转为可编辑形状。
打包组装方式沿用 visio-rebuild/build_vsdx.py 的最小 OPC 结构。
"""
import os, re, subprocess, zipfile, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SVG = os.path.join(HERE, 'out', 'svg')
EMF = os.path.join(HERE, 'out', 'emf_final')
VSD = os.path.join(HERE, 'out', 'vsdx')
os.makedirs(EMF, exist_ok=True); os.makedirs(VSD, exist_ok=True)

NS = "http://schemas.microsoft.com/office/visio/2012/main"
RNS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
MARGIN = 0.5          # 页边距（英寸）
MAX_W, MAX_H = 10.0, 10.0   # 图形最大宽/高（英寸）


def build_vsdx(name, emf_path, w_in, h_in, out_path):
    pw, ph = w_in + 2*MARGIN, h_in + 2*MARGIN
    cx, cy = round(pw/2, 4), round(ph/2, 4)
    emf_data = open(emf_path, 'rb').read()

    content_types = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Default Extension="emf" ContentType="image/x-emf"/>
<Override PartName="/visio/document.xml" ContentType="application/vnd.ms-visio.drawing.main+xml"/>
<Override PartName="/visio/pages/pages.xml" ContentType="application/vnd.ms-visio.pages+xml"/>
<Override PartName="/visio/pages/page1.xml" ContentType="application/vnd.ms-visio.page+xml"/>
<Override PartName="/visio/windows.xml" ContentType="application/vnd.ms-visio.windows+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>"""
    root_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.microsoft.com/visio/2010/relationships/document" Target="visio/document.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/core-properties" Target="docProps/core.xml"/>
<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>"""
    document = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<VisioDocument xmlns="{NS}" xmlns:r="{RNS}" xml:space="preserve">
<DocumentSettings TopPage="0" DefaultTextStyle="0" DefaultLineStyle="0" DefaultFillStyle="0">
<GlueSettings>9</GlueSettings><SnapSettings>65847</SnapSettings>
</DocumentSettings>
<Colors/>
<StyleSheets>
<StyleSheet ID="0" NameU="No Style" Name="No Style">
<Cell N="LineWeight" V="0.01"/><Cell N="LineColor" V="0"/><Cell N="LinePattern" V="0"/>
<Cell N="FillForegnd" V="1"/><Cell N="FillPattern" V="1"/>
<Cell N="Color" V="0"/><Cell N="Size" V="0.1667"/>
</StyleSheet>
</StyleSheets>
</VisioDocument>"""
    document_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.microsoft.com/visio/2010/relationships/pages" Target="pages/pages.xml"/>
<Relationship Id="rId2" Type="http://schemas.microsoft.com/visio/2010/relationships/windows" Target="windows.xml"/>
</Relationships>"""
    pages = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Pages xmlns="{NS}" xmlns:r="{RNS}" xml:space="preserve">
<Page ID="0" NameU="{name}" Name="{name}" ViewScale="-1" ViewCenterX="{cx}" ViewCenterY="{cy}">
<PageSheet LineStyle="0" FillStyle="0" TextStyle="0">
<Cell N="PageWidth" V="{pw:.4f}"/><Cell N="PageHeight" V="{ph:.4f}"/>
<Cell N="PageScale" V="1" U="IN_F"/><Cell N="DrawingScale" V="1" U="IN_F"/>
<Cell N="DrawingScaleType" V="0"/><Cell N="DrawingSizeType" V="3"/>
</PageSheet>
<Rel r:id="rId1"/>
</Page>
</Pages>"""
    pages_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.microsoft.com/visio/2010/relationships/page" Target="page1.xml"/>
</Relationships>"""
    page1 = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<PageContents xmlns="{NS}" xmlns:r="{RNS}" xml:space="preserve">'
        f'<Shapes>'
        f'<Shape ID="1" NameU="{name}" Name="{name}" Type="Foreign" LineStyle="0" FillStyle="0" TextStyle="0">'
        f'<Cell N="PinX" V="{cx}"/><Cell N="PinY" V="{cy}"/>'
        f'<Cell N="Width" V="{w_in:.4f}"/><Cell N="Height" V="{h_in:.4f}"/>'
        f'<Cell N="LocPinX" V="{w_in/2:.4f}" F="Width*0.5"/><Cell N="LocPinY" V="{h_in/2:.4f}" F="Height*0.5"/>'
        f'<Cell N="Angle" V="0"/><Cell N="FlipX" V="0"/><Cell N="FlipY" V="0"/>'
        f'<Cell N="LockAspect" V="1"/>'
        f'<Cell N="LinePattern" V="0"/><Cell N="FillPattern" V="0"/>'
        f'<Cell N="ImgOffsetX" V="0" F="ImgWidth*0"/><Cell N="ImgOffsetY" V="0" F="ImgHeight*0"/>'
        f'<Cell N="ImgWidth" V="{w_in:.4f}" F="Width*1"/><Cell N="ImgHeight" V="{h_in:.4f}" F="Height*1"/>'
        f'<ForeignData ForeignType="EnhMetaFile"><Rel r:id="rId1"/></ForeignData>'
        f'</Shape>'
        f'</Shapes>'
        f'</PageContents>')
    page1_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/image1.emf"/>
</Relationships>"""
    windows = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Windows xmlns="{NS}" xmlns:r="{RNS}" ClientWidth="1600" ClientHeight="900">
<Window ID="0" WindowType="Drawing" WindowState="1073741824" WindowLeft="0" WindowTop="0" WindowWidth="1600" WindowHeight="900" ContainerType="Page" Page="0" ViewScale="-1" ViewCenterX="{cx}" ViewCenterY="{cy}"/>
</Windows>"""
    core = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<dc:title>{name}</dc:title>
<dc:creator>figure-conversion</dc:creator>
<cp:lastModifiedBy>figure-conversion</cp:lastModifiedBy>
</cp:coreProperties>"""
    app = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">
<Application>Microsoft Visio</Application><Company></Company>
</Properties>"""
    parts = {
        "_rels/.rels": root_rels,
        "docProps/core.xml": core,
        "docProps/app.xml": app,
        "visio/document.xml": document,
        "visio/_rels/document.xml.rels": document_rels,
        "visio/pages/pages.xml": pages,
        "visio/pages/_rels/pages.xml.rels": pages_rels,
        "visio/pages/page1.xml": page1,
        "visio/pages/_rels/page1.xml.rels": page1_rels,
        "visio/windows.xml": windows,
    }
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        for n, data in parts.items():
            z.writestr(n, data)
        z.writestr("visio/media/image1.emf", emf_data)


def main():
    svgs = sorted(f for f in os.listdir(SVG) if f.endswith('.svg'))
    for f in svgs:
        name = f[:-4]
        svg_path = os.path.join(SVG, f)
        emf_path = os.path.join(EMF, name + '.emf')
        if not os.path.exists(emf_path):
            r = subprocess.run(['inkscape', svg_path, '--export-type=emf',
                                '--export-filename=' + emf_path],
                               capture_output=True, timeout=300)
            if not os.path.exists(emf_path):
                print(name, 'EMF FAIL', r.stderr[-200:]); continue
        m = re.search(r'viewBox="0 0 (\d+) (\d+)"|width="(\d+)" height="(\d+)"',
                      open(svg_path, encoding='utf-8').read()[:400])
        g = [x for x in m.groups() if x]
        w_px, h_px = int(g[0]), int(g[1])
        scale = min(MAX_W / w_px, MAX_H / h_px)
        w_in, h_in = w_px * scale, h_px * scale
        out_path = os.path.join(VSD, name + '.vsdx')
        build_vsdx(name, emf_path, w_in, h_in, out_path)
        print(name, f'{w_in:.1f}x{h_in:.1f}in', os.path.getsize(out_path)//1024, 'KB', flush=True)

if __name__ == '__main__':
    main()
