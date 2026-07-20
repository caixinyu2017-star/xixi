#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Emit the methodology flowchart as a NATIVE, fully editable Visio drawing
(.vsdx = Office Open XML / OPC package).  Every box, arrow and label is a real
Visio shape with real text runs -- nothing is a rasterised image.  All text uses
the Microsoft YaHei (微软雅黑) font in bold at large point sizes.

Layout comes from layout.build_shapes(); this module only serialises it.
"""

import math
import os
import zipfile

import layout as LY

SCALE = LY.SCALE
PAGE_W = LY.DESIGN_W / SCALE
PAGE_H = LY.DESIGN_H / SCALE
FONT = LY.FONT

def X(px):  return round(px / SCALE, 4)
def Yh(py): return round(PAGE_H - py / SCALE, 4)
def Ln(px): return round(px / SCALE, 4)
def pt(p):  return round(p / 72.0, 5)

_id = [0]
def nid():
    _id[0] += 1
    return _id[0]

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# --- text section builder --------------------------------------------------
def build_text(paras):
    chars, parags, lines = [], [], []
    def cix(size, color):
        k = (round(pt(size), 5), color)
        if k not in chars: chars.append(k)
        return chars.index(k)
    def pix(align, spafter):
        k = (align, round(spafter, 4))
        if k not in parags: parags.append(k)
        return parags.index(k)
    for p in paras:
        ci = cix(p["size"], p["color"])
        pi = pix(p.get("align", 0), p.get("spafter", 0.0))
        lines.append(f"<pp IX='{pi}'/><cp IX='{ci}'/>{esc(p['text'])}")
    text_body = "\n".join(lines)

    crows = "".join(
        f"<Row IX='{i}'><Cell N='Font' V='{FONT}'/><Cell N='AsianFont' V='{FONT}'/>"
        f"<Cell N='Color' V='{color}'/><Cell N='Size' V='{size}'/>"
        f"<Cell N='Style' V='1'/><Cell N='RTLText' V='0'/></Row>"
        for i, (size, color) in enumerate(chars))
    prows = "".join(
        f"<Row IX='{i}'><Cell N='HorzAlign' V='{align}'/><Cell N='SpBefore' V='0'/>"
        f"<Cell N='SpAfter' V='{spafter}'/><Cell N='SpLine' V='-1.1'/>"
        f"<Cell N='Bullet' V='0'/></Row>"
        for i, (align, spafter) in enumerate(parags))
    return (f"<Section N='Character'>{crows}</Section>"
            f"<Section N='Paragraph'>{prows}</Section>", text_body)

def rect_geom(w, h):
    return (
        "<Section N='Geometry' IX='0'>"
        "<Cell N='NoFill' V='0'/><Cell N='NoLine' V='0'/>"
        "<Cell N='NoShow' V='0'/><Cell N='NoSnap' V='0'/>"
        f"<Row T='MoveTo' IX='1'><Cell N='X' V='0'/><Cell N='Y' V='0'/></Row>"
        f"<Row T='LineTo' IX='2'><Cell N='X' V='{w}'/><Cell N='Y' V='0'/></Row>"
        f"<Row T='LineTo' IX='3'><Cell N='X' V='{w}'/><Cell N='Y' V='{h}'/></Row>"
        f"<Row T='LineTo' IX='4'><Cell N='X' V='0'/><Cell N='Y' V='{h}'/></Row>"
        f"<Row T='LineTo' IX='5'><Cell N='X' V='0'/><Cell N='Y' V='0'/></Row>"
        "</Section>")

def emit_box(s):
    w, h = Ln(s["w"]), Ln(s["h"])
    pinx, piny = X(s["x"] + s["w"] / 2), Yh(s["y"] + s["h"] / 2)
    fill = s.get("fill", LY.WHITE)
    border = s.get("border", LY.BORDER)
    valign = s.get("valign", 0)
    rounding = s.get("rounding", 0.09)
    lw = s.get("lw", 0.016)
    sec, body = build_text(s["paras"])
    return f"""<Shape ID='{nid()}' Name='{s['name']}' NameU='{s['name']}' Type='Shape'>
<Cell N='PinX' V='{pinx}'/><Cell N='PinY' V='{piny}'/>
<Cell N='Width' V='{w}'/><Cell N='Height' V='{h}'/>
<Cell N='LocPinX' V='{round(w/2,4)}' F='Width*0.5'/>
<Cell N='LocPinY' V='{round(h/2,4)}' F='Height*0.5'/>
<Cell N='Angle' V='0'/>
<Cell N='FillForegnd' V='{fill}'/><Cell N='FillPattern' V='1'/>
<Cell N='LineColor' V='{border}'/><Cell N='LineWeight' V='{lw}'/>
<Cell N='LinePattern' V='1'/><Cell N='Rounding' V='{rounding}'/>
<Cell N='VerticalAlign' V='{valign}'/>
<Cell N='LeftMargin' V='0.09'/><Cell N='RightMargin' V='0.09'/>
<Cell N='TopMargin' V='0.07'/><Cell N='BottomMargin' V='0.05'/>
{sec}{rect_geom(w, h)}
<Text>{body}</Text>
</Shape>"""

def emit_label(s):
    w, h = Ln(s["w"]), Ln(s["h"])
    pinx, piny = X(s["x"] + s["w"] / 2), Yh(s["y"] + s["h"] / 2)
    valign = s.get("valign", 1)
    sec, body = build_text(s["paras"])
    return f"""<Shape ID='{nid()}' Name='{s['name']}' NameU='{s['name']}' Type='Shape'>
<Cell N='PinX' V='{pinx}'/><Cell N='PinY' V='{piny}'/>
<Cell N='Width' V='{w}'/><Cell N='Height' V='{h}'/>
<Cell N='LocPinX' V='{round(w/2,4)}' F='Width*0.5'/>
<Cell N='LocPinY' V='{round(h/2,4)}' F='Height*0.5'/>
<Cell N='Angle' V='0'/>
<Cell N='FillForegnd' V='#FFFFFF'/><Cell N='FillPattern' V='0'/>
<Cell N='LineColor' V='#FFFFFF'/><Cell N='LineWeight' V='0'/><Cell N='LinePattern' V='0'/>
<Cell N='VerticalAlign' V='{valign}'/>
<Cell N='LeftMargin' V='0.02'/><Cell N='RightMargin' V='0.02'/>
<Cell N='TopMargin' V='0.02'/><Cell N='BottomMargin' V='0.02'/>
{sec}
<Text>{body}</Text>
</Shape>"""

def emit_line(s):
    ax1, ay1, ax2, ay2 = X(s["x1"]), Yh(s["y1"]), X(s["x2"]), Yh(s["y2"])
    dx, dy = ax2 - ax1, ay2 - ay1
    length = round(math.hypot(dx, dy), 4)
    angle = round(math.atan2(dy, dx), 6)
    pinx, piny = round((ax1 + ax2) / 2, 4), round((ay1 + ay2) / 2, 4)
    color = s.get("color", LY.BLK)
    lw = s.get("lw", 0.015)
    pattern = s.get("pattern", 1)
    ba = s.get("begin_arrow", 0)
    ea = s.get("end_arrow", 0)
    asz = s.get("arrow_size", 2)
    return f"""<Shape ID='{nid()}' Name='{s['name']}' NameU='{s['name']}' Type='Shape'>
<Cell N='PinX' V='{pinx}'/><Cell N='PinY' V='{piny}'/>
<Cell N='Width' V='{length}'/><Cell N='Height' V='0'/>
<Cell N='LocPinX' V='{round(length/2,4)}' F='Width*0.5'/>
<Cell N='LocPinY' V='0' F='Height*0.5'/>
<Cell N='Angle' V='{angle}'/>
<Cell N='BeginX' V='{ax1}'/><Cell N='BeginY' V='{ay1}'/>
<Cell N='EndX' V='{ax2}'/><Cell N='EndY' V='{ay2}'/>
<Cell N='LineColor' V='{color}'/><Cell N='LineWeight' V='{lw}'/>
<Cell N='LinePattern' V='{pattern}'/>
<Cell N='BeginArrow' V='{ba}'/><Cell N='EndArrow' V='{ea}'/>
<Cell N='BeginArrowSize' V='{asz}'/><Cell N='EndArrowSize' V='{asz}'/>
<Section N='Geometry' IX='0'>
<Cell N='NoFill' V='1'/><Cell N='NoLine' V='0'/>
<Row T='MoveTo' IX='1'><Cell N='X' V='0'/><Cell N='Y' V='0'/></Row>
<Row T='LineTo' IX='2'><Cell N='X' V='{length}'/><Cell N='Y' V='0'/></Row>
</Section>
</Shape>"""

def emit_shapes():
    out = []
    for s in LY.build_shapes():
        if s["kind"] == "box":
            out.append(emit_box(s))
        elif s["kind"] == "label":
            out.append(emit_label(s))
        elif s["kind"] == "line":
            out.append(emit_line(s))
    return out

# --- OPC package -----------------------------------------------------------
NS = "http://schemas.microsoft.com/office/visio/2012/main"
RNS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

def package(shapes):
    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
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
<FaceNames>
<FaceName ID="1" Name="{FONT}" UnicodeRanges="-536859905 -1073732485 9 0" CharSets="-2147483609 0" Panose="2 11 5 3 2 2 4 2 2 4" Flags="325"/>
</FaceNames>
<StyleSheets>
<StyleSheet ID="0" NameU="No Style" Name="No Style">
<Cell N="LineWeight" V="0.01"/><Cell N="LineColor" V="0"/><Cell N="LinePattern" V="1"/>
<Cell N="FillForegnd" V="1"/><Cell N="FillPattern" V="1"/>
<Cell N="Font" V="{FONT}"/><Cell N="Color" V="0"/><Cell N="Size" V="0.1667"/>
<Cell N="Style" V="0"/><Cell N="HorzAlign" V="1"/><Cell N="VerticalAlign" V="1"/>
</StyleSheet>
</StyleSheets>
</VisioDocument>"""
    document_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.microsoft.com/visio/2010/relationships/pages" Target="pages/pages.xml"/>
<Relationship Id="rId2" Type="http://schemas.microsoft.com/visio/2010/relationships/windows" Target="windows.xml"/>
</Relationships>"""
    cx, cy = round(PAGE_W / 2, 3), round(PAGE_H / 2, 3)
    pages = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Pages xmlns="{NS}" xmlns:r="{RNS}" xml:space="preserve">
<Page ID="0" NameU="Methodology" Name="Methodology" ViewScale="-1" ViewCenterX="{cx}" ViewCenterY="{cy}">
<PageSheet LineStyle="0" FillStyle="0" TextStyle="0">
<Cell N="PageWidth" V="{PAGE_W}"/><Cell N="PageHeight" V="{PAGE_H}"/>
<Cell N="ShdwOffsetX" V="0.125"/><Cell N="ShdwOffsetY" V="-0.125"/>
<Cell N="PageScale" V="1" U="IN_F"/><Cell N="DrawingScale" V="1" U="IN_F"/>
<Cell N="DrawingScaleType" V="0"/><Cell N="DrawingSizeType" V="3"/>
<Cell N="InhibitSnap" V="0"/><Cell N="UIVisibility" V="0"/>
</PageSheet>
<Rel r:id="rId1"/>
</Page>
</Pages>"""
    pages_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.microsoft.com/visio/2010/relationships/page" Target="page1.xml"/>
</Relationships>"""
    page1 = (f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<PageContents xmlns="{NS}" xmlns:r="{RNS}" xml:space="preserve">
<Shapes>
""" + "\n".join(shapes) + """
</Shapes>
</PageContents>""")
    windows = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Windows xmlns="{NS}" xmlns:r="{RNS}" ClientWidth="1600" ClientHeight="900">
<Window ID="0" WindowType="Drawing" WindowState="1073741824" WindowLeft="0" WindowTop="0" WindowWidth="1600" WindowHeight="900" ContainerType="Page" Page="0" ViewScale="-1" ViewCenterX="{cx}" ViewCenterY="{cy}"/>
</Windows>"""
    core = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<dc:title>Career-narrative study methodology</dc:title>
<dc:creator>Visio rebuild</dc:creator>
<cp:lastModifiedBy>Visio rebuild</cp:lastModifiedBy>
</cp:coreProperties>"""
    app = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">
<Application>Microsoft Visio</Application><Company></Company>
</Properties>"""
    return {
        "[Content_Types].xml": content_types,
        "_rels/.rels": root_rels,
        "docProps/core.xml": core,
        "docProps/app.xml": app,
        "visio/document.xml": document,
        "visio/_rels/document.xml.rels": document_rels,
        "visio/pages/pages.xml": pages,
        "visio/pages/_rels/pages.xml.rels": pages_rels,
        "visio/pages/page1.xml": page1,
        "visio/windows.xml": windows,
    }

def main():
    shapes = emit_shapes()
    parts = package(shapes)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "method_flowchart.vsdx")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", parts.pop("[Content_Types].xml"))
        for name, data in parts.items():
            z.writestr(name, data)
    print("wrote", out)
    print("shapes:", len(shapes), "| page:", PAGE_W, "x", PAGE_H, "in")

if __name__ == "__main__":
    main()
