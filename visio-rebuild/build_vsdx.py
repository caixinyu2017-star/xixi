#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Emit a NATIVE, editable Microsoft Visio (.vsdx) file from scene.py.

Output is a Visio 2013+ Open-Packaging-Conventions package whose single page
holds native Visio shapes (rectangles, poly-line connectors, formatted text
runs).  Nothing is an embedded image: every shape has real geometry, fill/line
formatting and a Character section, so it is fully selectable and editable in
Visio.  All text is Microsoft YaHei, bold.
"""
import os
import zipfile
from xml.sax.saxutils import escape

import scene as SC

# ---- coordinate mapping: image px -> Visio inches (Y flips) --------------- #
SCALE = 0.01
PAGE_W = SC.IMG_W * SCALE      # 14.0 in
PAGE_H = SC.IMG_H * SCALE      # 10.4 in

def vx(px):
    return round(px * SCALE, 4)

def vy(py):
    return round((SC.IMG_H - py) * SCALE, 4)

NS_MAIN = "http://schemas.microsoft.com/office/visio/2012/main"
NS_R    = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

_id = [0]
def nid():
    _id[0] += 1
    return _id[0]

VALIGN = {"top": 0, "middle": 1, "bottom": 2}


def char_section(paras):
    rows = []
    for i, (style, _txt) in enumerate(paras):
        st = SC.STYLES[style]
        size_in = round(st["size"] / 72.0, 5)
        rows.append(
            f'<Row IX="{i}">'
            f'<Cell N="Font" V="{SC.FONT}"/>'
            f'<Cell N="Color" V="{st["color"]}"/>'
            f'<Cell N="Style" V="1"/>'
            f'<Cell N="Size" V="{size_in}"/>'
            f'<Cell N="AsianFont" V="{SC.FONT}"/>'
            f'<Cell N="ComplexScriptFont" V="{SC.FONT}"/>'
            f'<Cell N="ComplexScriptSize" V="{size_in}"/>'
            f'</Row>'
        )
    return '<Section N="Character">' + "".join(rows) + "</Section>"


def para_section(paras):
    rows = []
    for i, (style, _txt) in enumerate(paras):
        st = SC.STYLES[style]
        rows.append(
            f'<Row IX="{i}">'
            f'<Cell N="HorzAlign" V="{st["align"]}"/>'
            f'<Cell N="SpLine" V="-1.2"/>'
            f'<Cell N="SpBefore" V="0"/><Cell N="SpAfter" V="0"/>'
            f'</Row>'
        )
    return '<Section N="Paragraph">' + "".join(rows) + "</Section>"


def text_body(paras):
    parts = [f'<pp IX="{i}"/><cp IX="{i}"/>' + escape(t) for i, (_s, t) in enumerate(paras)]
    return "<Text>" + "\n".join(parts) + "</Text>"


def rect_shape(b):
    sid = nid()
    l, t, r, bot = b["px"]
    L, R = vx(l), vx(r)
    T, B = vy(t), vy(bot)
    w = round(R - L, 4)
    h = round(T - B, 4)
    cx = round((L + R) / 2, 4)
    cy = round((T + B) / 2, 4)
    fill = b["fill"] or SC.WHITE
    fill_pat = 1 if b["fill"] else 0
    line = b["line"] or SC.WHITE
    line_pat = 1 if b["line"] else 0
    line_w = round(b["line_w"] / 72.0, 4)     # pt -> in
    rounding = round(b["rounding"] * SCALE, 4)
    valign = VALIGN[b["valign"]]

    return (
        f'<Shape ID="{sid}" NameU="{b["name"]}" Name="{b["name"]}" Type="Shape" '
        f'LineStyle="3" FillStyle="3" TextStyle="3">'
        f'<Cell N="ObjType" V="1"/>'
        f'<Cell N="PinX" V="{cx}"/><Cell N="PinY" V="{cy}"/>'
        f'<Cell N="Width" V="{w}"/><Cell N="Height" V="{h}"/>'
        f'<Cell N="LocPinX" V="{round(w/2,4)}" F="Width*0.5"/>'
        f'<Cell N="LocPinY" V="{round(h/2,4)}" F="Height*0.5"/>'
        f'<Cell N="Angle" V="0"/>'
        f'<Cell N="FillForegnd" V="{fill}"/><Cell N="FillBkgnd" V="{fill}"/>'
        f'<Cell N="FillPattern" V="{fill_pat}"/>'
        f'<Cell N="LineColor" V="{line}"/><Cell N="LineWeight" V="{line_w}"/>'
        f'<Cell N="LinePattern" V="{line_pat}"/><Cell N="Rounding" V="{rounding}"/>'
        f'<Cell N="VerticalAlign" V="{valign}"/>'
        f'<Cell N="TxtPinX" V="{round(w/2,4)}" F="Width*0.5"/>'
        f'<Cell N="TxtPinY" V="{round(h/2,4)}" F="Height*0.5"/>'
        f'<Cell N="TxtWidth" V="{w}" F="Width*1"/>'
        f'<Cell N="TxtHeight" V="{h}" F="Height*1"/>'
        f'<Cell N="LeftMargin" V="0.05"/><Cell N="RightMargin" V="0.05"/>'
        f'<Cell N="TopMargin" V="0.03"/><Cell N="BottomMargin" V="0.03"/>'
        + char_section(b["paras"]) + para_section(b["paras"])
        + '<Section N="Geometry" IX="0">'
          f'<Cell N="NoFill" V="{0 if b["fill"] else 1}"/>'
          f'<Cell N="NoLine" V="{0 if b["line"] else 1}"/>'
          '<Row T="RelMoveTo" IX="1"><Cell N="X" V="0"/><Cell N="Y" V="0"/></Row>'
          '<Row T="RelLineTo" IX="2"><Cell N="X" V="1"/><Cell N="Y" V="0"/></Row>'
          '<Row T="RelLineTo" IX="3"><Cell N="X" V="1"/><Cell N="Y" V="1"/></Row>'
          '<Row T="RelLineTo" IX="4"><Cell N="X" V="0"/><Cell N="Y" V="1"/></Row>'
          '<Row T="RelLineTo" IX="5"><Cell N="X" V="0"/><Cell N="Y" V="0"/></Row>'
          '</Section>'
        + text_body(b["paras"])
        + '</Shape>'
    )


def conn_shape(c):
    sid = nid()
    vpts = [(vx(px), vy(py)) for px, py in c["points"]]
    xs = [p[0] for p in vpts]
    ys = [p[1] for p in vpts]
    L, R = min(xs), max(xs)
    B, T = min(ys), max(ys)
    w = round(R - L, 4) or 0.0001
    h = round(T - B, 4) or 0.0001
    cx = round((L + R) / 2, 4)
    cy = round((T + B) / 2, 4)

    geo = ['<Section N="Geometry" IX="0"><Cell N="NoFill" V="1"/><Cell N="NoLine" V="0"/>']
    for i, (x, y) in enumerate(vpts):
        typ = "MoveTo" if i == 0 else "LineTo"
        geo.append(f'<Row T="{typ}" IX="{i+1}"><Cell N="X" V="{round(x-L,4)}"/>'
                   f'<Cell N="Y" V="{round(y-B,4)}"/></Row>')
    geo.append('</Section>')

    line_w = round(c["w"] / 72.0, 4)
    pattern = 2 if c["dash"] else 1
    ba = 4 if c["begin"] else 0
    ea = 4 if c["end"] else 0
    return (
        f'<Shape ID="{sid}" NameU="{c["name"]}" Name="{c["name"]}" Type="Shape" '
        f'LineStyle="3" FillStyle="3" TextStyle="3">'
        f'<Cell N="ObjType" V="1"/>'
        f'<Cell N="PinX" V="{cx}"/><Cell N="PinY" V="{cy}"/>'
        f'<Cell N="Width" V="{w}"/><Cell N="Height" V="{h}"/>'
        f'<Cell N="LocPinX" V="{round(w/2,4)}" F="Width*0.5"/>'
        f'<Cell N="LocPinY" V="{round(h/2,4)}" F="Height*0.5"/>'
        f'<Cell N="Angle" V="0"/>'
        f'<Cell N="LineColor" V="{c["color"]}"/><Cell N="LineWeight" V="{line_w}"/>'
        f'<Cell N="LinePattern" V="{pattern}"/><Cell N="FillPattern" V="0"/>'
        f'<Cell N="BeginArrow" V="{ba}"/><Cell N="EndArrow" V="{ea}"/>'
        f'<Cell N="BeginArrowSize" V="2"/><Cell N="EndArrowSize" V="2"/>'
        + "".join(geo) + '</Shape>'
    )


def shapes_xml():
    out = []
    for b in SC.BOXES:
        out.append(rect_shape(b))
    for c in SC.CONNS:
        out.append(conn_shape(c))
    return "".join(out)


# ---- OPC parts ----------------------------------------------------------- #
def content_types():
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/visio/document.xml" ContentType="application/vnd.ms-visio.drawing.main+xml"/>'
        '<Override PartName="/visio/pages/pages.xml" ContentType="application/vnd.ms-visio.pages+xml"/>'
        '<Override PartName="/visio/pages/page1.xml" ContentType="application/vnd.ms-visio.page+xml"/>'
        '<Override PartName="/visio/windows.xml" ContentType="application/vnd.ms-visio.windows+xml"/>'
        '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
        '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
        '</Types>')

def root_rels():
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.microsoft.com/visio/2010/relationships/document" Target="visio/document.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
        '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
        '</Relationships>')

def core_props():
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        '<dc:title>Research methodology flowchart</dc:title>'
        '<dc:creator>visio-rebuild</dc:creator>'
        '<cp:lastModifiedBy>visio-rebuild</cp:lastModifiedBy>'
        '</cp:coreProperties>')

def app_props():
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
        'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
        '<Application>Microsoft Visio</Application><AppVersion>15.0000</AppVersion></Properties>')

_HERE = os.path.dirname(os.path.abspath(__file__))

def document_xml():
    # Authentic Visio-authored document-level part (DocumentSettings, Colors,
    # FaceNames incl. Microsoft YaHei, StyleSheets 0-7, DocumentSheet).  Reusing
    # Visio's own structures maximises real-Visio openability.
    with open(os.path.join(_HERE, "assets", "document.xml"), encoding="utf-8") as f:
        return f.read()

def document_rels():
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.microsoft.com/visio/2010/relationships/pages" Target="pages/pages.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.microsoft.com/visio/2010/relationships/windows" Target="windows.xml"/>'
        '</Relationships>')

def windows_xml():
    with open(os.path.join(_HERE, "assets", "windows.xml"), encoding="utf-8") as f:
        return f.read()

def pages_xml():
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        f'<Pages xmlns="{NS_MAIN}" xmlns:r="{NS_R}" xml:space="preserve">'
        '<Page ID="0" NameU="Page-1" Name="Page-1" ViewScale="-1" '
        f'ViewCenterX="{round(PAGE_W/2,3)}" ViewCenterY="{round(PAGE_H/2,3)}">'
        '<PageSheet>'
        f'<Cell N="PageWidth" V="{PAGE_W}"/><Cell N="PageHeight" V="{PAGE_H}"/>'
        '<Cell N="ShdwOffsetX" V="0.125"/><Cell N="ShdwOffsetY" V="-0.125"/>'
        '<Cell N="PageScale" V="1"/><Cell N="DrawingScale" V="1"/>'
        '<Cell N="DrawingSizeType" V="3"/><Cell N="DrawingScaleType" V="0"/>'
        '<Cell N="InhibitSnap" V="0"/><Cell N="XRulerOrigin" V="0"/><Cell N="YRulerOrigin" V="0"/>'
        '</PageSheet>'
        '<Rel r:id="rId1"/>'
        '</Page></Pages>')

def pages_rels():
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.microsoft.com/visio/2010/relationships/page" Target="page1.xml"/>'
        '</Relationships>')

def page1_xml():
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        f'<PageContents xmlns="{NS_MAIN}" xmlns:r="{NS_R}" xml:space="preserve">'
        '<Shapes>' + shapes_xml() + '</Shapes></PageContents>')


def write_vsdx(path):
    _id[0] = 0
    parts = {
        "_rels/.rels": root_rels(),
        "docProps/core.xml": core_props(),
        "docProps/app.xml": app_props(),
        "visio/document.xml": document_xml(),
        "visio/_rels/document.xml.rels": document_rels(),
        "visio/windows.xml": windows_xml(),
        "visio/pages/pages.xml": pages_xml(),
        "visio/pages/_rels/pages.xml.rels": pages_rels(),
        "visio/pages/page1.xml": page1_xml(),
    }
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types())
        for name, data in parts.items():
            z.writestr(name, data)
    return path


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "research_methodology_flowchart.vsdx")
    write_vsdx(out)
    print("wrote", out, os.path.getsize(out), "bytes,", _id[0], "shapes")
