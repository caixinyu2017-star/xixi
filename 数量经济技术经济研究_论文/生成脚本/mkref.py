# -*- coding: utf-8 -*-
"""Build a journal-style reference.docx for pandoc, matching 《数量经济技术经济研究》.
Body: 五号(10.5pt) 宋体 + Times New Roman, exact line spacing, first-line indent 2 chars.
Headings: 黑体.
"""
import zipfile, shutil, re, os

SRC = "ref_default.docx"
OUT = "reference.docx"
shutil.copy(SRC, "ref_work.docx")

# Rewrite styles.xml fully with our own definitions.
STYLES = r'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" mc:Ignorable="w14">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="宋体" w:cs="Times New Roman"/>
        <w:sz w:val="21"/>
        <w:szCs w:val="21"/>
        <w:lang w:val="en-US" w:eastAsia="zh-CN" w:bidi="ar-SA"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr>
        <w:spacing w:line="360" w:lineRule="exact"/>
        <w:jc w:val="both"/>
      </w:pPr>
    </w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:qFormat/>
    <w:pPr>
      <w:spacing w:line="360" w:lineRule="exact"/>
      <w:ind w:firstLine="420" w:firstLineChars="200"/>
      <w:jc w:val="both"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="宋体" w:cs="Times New Roman"/>
      <w:sz w:val="21"/><w:szCs w:val="21"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="BodyText">
    <w:name w:val="Body Text"/><w:basedOn w:val="Normal"/>
  </w:style>
  <w:style w:type="paragraph" w:styleId="FirstParagraph">
    <w:name w:val="First Paragraph"/><w:basedOn w:val="Normal"/>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Compact">
    <w:name w:val="Compact"/><w:basedOn w:val="Normal"/>
  </w:style>
  <w:style w:type="character" w:default="1" w:styleId="DefaultParagraphFont">
    <w:name w:val="Default Paragraph Font"/>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/>
    <w:pPr>
      <w:keepNext/><w:spacing w:before="180" w:after="120" w:line="360" w:lineRule="exact"/>
      <w:ind w:firstLine="0" w:firstLineChars="0"/><w:jc w:val="center"/><w:outlineLvl w:val="0"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="黑体" w:cs="Times New Roman"/>
      <w:b/><w:bCs/><w:sz w:val="24"/><w:szCs w:val="24"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/>
    <w:pPr>
      <w:keepNext/><w:spacing w:before="180" w:after="120" w:line="360" w:lineRule="exact"/>
      <w:ind w:firstLine="0" w:firstLineChars="0"/><w:jc w:val="center"/><w:outlineLvl w:val="1"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="黑体" w:cs="Times New Roman"/>
      <w:b/><w:bCs/><w:sz w:val="22"/><w:szCs w:val="22"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/>
    <w:pPr>
      <w:keepNext/><w:spacing w:before="60" w:after="60" w:line="360" w:lineRule="exact"/>
      <w:ind w:firstLine="420" w:firstLineChars="200"/><w:jc w:val="both"/><w:outlineLvl w:val="2"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="楷体" w:cs="Times New Roman"/>
      <w:b/><w:bCs/><w:sz w:val="21"/><w:szCs w:val="21"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading4">
    <w:name w:val="heading 4"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/>
    <w:pPr><w:spacing w:line="360" w:lineRule="exact"/><w:ind w:firstLine="420" w:firstLineChars="200"/><w:outlineLvl w:val="3"/></w:pPr>
    <w:rPr><w:rFonts w:eastAsia="宋体"/><w:b/><w:bCs/><w:sz w:val="21"/><w:szCs w:val="21"/></w:rPr>
  </w:style>
  <w:style w:type="table" w:default="1" w:styleId="TableNormal">
    <w:name w:val="Normal Table"/>
    <w:tblPr><w:tblCellMar>
      <w:top w:w="28" w:type="dxa"/><w:left w:w="80" w:type="dxa"/>
      <w:bottom w:w="28" w:type="dxa"/><w:right w:w="80" w:type="dxa"/>
    </w:tblCellMar></w:tblPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Caption">
    <w:name w:val="Caption"/><w:basedOn w:val="Normal"/><w:qFormat/>
    <w:pPr><w:spacing w:line="360" w:lineRule="exact"/><w:ind w:firstLine="0" w:firstLineChars="0"/><w:jc w:val="center"/></w:pPr>
    <w:rPr><w:rFonts w:eastAsia="黑体"/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="FootnoteText">
    <w:name w:val="footnote text"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:snapToGrid w:val="0"/><w:spacing w:line="240" w:lineRule="auto"/><w:ind w:firstLine="0" w:firstLineChars="0"/></w:pPr>
    <w:rPr><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>
  </w:style>
  <w:style w:type="character" w:styleId="FootnoteReference">
    <w:name w:val="footnote reference"/><w:rPr><w:vertAlign w:val="superscript"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Figure">
    <w:name w:val="Figure"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:line="360" w:lineRule="exact"/><w:ind w:firstLine="0" w:firstLineChars="0"/><w:jc w:val="center"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="ImageCaption">
    <w:name w:val="Image Caption"/><w:basedOn w:val="Caption"/>
  </w:style>
  <w:style w:type="paragraph" w:styleId="BlockText">
    <w:name w:val="Block Text"/><w:basedOn w:val="Normal"/>
  </w:style>
  <w:style w:type="paragraph" w:styleId="AbstractTitle">
    <w:name w:val="Abstract Title"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:ind w:firstLine="0" w:firstLineChars="0"/></w:pPr>
    <w:rPr><w:rFonts w:eastAsia="黑体"/><w:b/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Abstract">
    <w:name w:val="Abstract"/><w:basedOn w:val="Normal"/>
  </w:style>
  <w:style w:type="character" w:styleId="VerbatimChar">
    <w:name w:val="Verbatim Char"/><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Bibliography">
    <w:name w:val="Bibliography"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="0" w:hanging="0" w:firstLine="0" w:firstLineChars="0"/></w:pPr>
    <w:rPr><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>
  </w:style>
</w:styles>
'''

# Read zip, replace styles.xml
tmp = "ref_tmp"
if os.path.exists(tmp): shutil.rmtree(tmp)
os.makedirs(tmp)
with zipfile.ZipFile("ref_work.docx") as z:
    z.extractall(tmp)
with open(os.path.join(tmp,"word","styles.xml"),"w",encoding="utf-8") as f:
    f.write(STYLES)

# repackage
if os.path.exists(OUT): os.remove(OUT)
with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED) as z:
    for root,_,files in os.walk(tmp):
        for fn in files:
            full=os.path.join(root,fn)
            arc=os.path.relpath(full,tmp)
            z.write(full,arc)
print("wrote", OUT)
