# -*- coding: utf-8 -*-
"""按参考试卷 A/B/C 的排版，生成四套随堂测试试卷 DOCX。
做法：复用参考 docx 的整个包（styles/settings/fontTable/theme 原样保留），
只重写 word/document.xml 的 body，段落属性逐字段照抄参考文件。"""
import os, re, shutil, zipfile, html

SRC = "/root/.claude/uploads/4c7b3765-7fc0-56c9-a23c-b8d8222c3081/5e8182b5-________________________A.docx"
OUT_DIR = "/home/user/xixi/亚德客管理培训/随堂测试试卷"

E = lambda s: html.escape(s, quote=False)

# ---------- 与参考试卷完全一致的段落模板 ----------
PPR_COMMON = ('<w:keepNext w:val="0"/><w:keepLines w:val="0"/><w:pageBreakBefore w:val="0"/>'
              '<w:kinsoku/><w:wordWrap/><w:overflowPunct/><w:topLinePunct w:val="0"/>'
              '<w:autoSpaceDE/><w:autoSpaceDN/><w:bidi w:val="0"/><w:adjustRightInd/><w:snapToGrid/>')

def p_title(text):
    rpr = ('<w:rFonts w:hint="eastAsia" w:ascii="微软雅黑" w:hAnsi="微软雅黑" w:eastAsia="微软雅黑" '
           'w:cs="微软雅黑"/><w:b/><w:bCs/><w:sz w:val="32"/><w:szCs w:val="32"/>')
    return ('<w:p><w:pPr>' + PPR_COMMON.replace('<w:kinsoku/>', '<w:widowControl w:val="0"/><w:kinsoku/>') +
            '<w:spacing w:before="0" w:line="360" w:lineRule="auto"/>'
            '<w:ind w:firstLine="0" w:firstLineChars="0"/><w:jc w:val="center"/>'
            '<w:textAlignment w:val="auto"/><w:rPr>' + rpr + '</w:rPr></w:pPr>'
            '<w:r><w:rPr>' + rpr + '</w:rPr><w:t xml:space="preserve">' + E(text) + '</w:t></w:r></w:p>')

def p_subtitle(text):
    rpr = ('<w:rFonts w:hint="default" w:ascii="Times New Roman" w:hAnsi="Times New Roman" '
           'w:cs="Times New Roman"/><w:sz w:val="24"/><w:szCs w:val="24"/>'
           '<w:lang w:val="en-US" w:eastAsia="zh-CN"/>')
    return ('<w:p><w:pPr><w:keepNext w:val="0"/><w:keepLines w:val="0"/><w:pageBreakBefore w:val="0"/>'
            '<w:widowControl w:val="0"/><w:kinsoku/><w:wordWrap/><w:overflowPunct/>'
            '<w:topLinePunct w:val="0"/><w:autoSpaceDE/><w:autoSpaceDN/><w:bidi w:val="0"/>'
            '<w:adjustRightInd/><w:snapToGrid/><w:spacing w:line="360" w:lineRule="auto"/>'
            '<w:jc w:val="center"/><w:textAlignment w:val="auto"/><w:rPr>' + rpr + '</w:rPr></w:pPr>'
            '<w:r><w:rPr>' + rpr + '</w:rPr><w:t xml:space="preserve">' + E(text) + '</w:t></w:r></w:p>')

def TBL(unit='班组'):
  """页首信息栏：单位（班组/营业部）、姓名、得分。"""
  return ('<w:tbl><w:tblPr><w:tblStyle w:val="32"/><w:tblW w:w="9360" w:type="dxa"/>'
       '<w:tblInd w:w="0" w:type="dxa"/><w:tblBorders>'
       '<w:top w:val="single" w:color="auto" w:sz="4" w:space="0"/>'
       '<w:left w:val="single" w:color="auto" w:sz="4" w:space="0"/>'
       '<w:bottom w:val="single" w:color="auto" w:sz="4" w:space="0"/>'
       '<w:right w:val="single" w:color="auto" w:sz="4" w:space="0"/>'
       '<w:insideH w:val="single" w:color="auto" w:sz="4" w:space="0"/>'
       '<w:insideV w:val="single" w:color="auto" w:sz="4" w:space="0"/></w:tblBorders>'
       '<w:tblLayout w:type="autofit"/><w:tblCellMar><w:top w:w="0" w:type="dxa"/>'
       '<w:left w:w="10" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/>'
       '<w:right w:w="10" w:type="dxa"/></w:tblCellMar></w:tblPr>'
       '<w:tblGrid><w:gridCol w:w="3120"/><w:gridCol w:w="3120"/><w:gridCol w:w="3120"/></w:tblGrid>'
       '<w:tr>' + ''.join(
           '<w:tc><w:tcPr><w:tcW w:w="3120" w:type="dxa"/><w:tcBorders><w:top w:val="nil"/>'
           '<w:left w:val="nil"/><w:bottom w:val="nil"/><w:right w:val="nil"/></w:tcBorders>'
           '<w:tcMar><w:top w:w="60" w:type="dxa"/><w:left w:w="80" w:type="dxa"/>'
           '<w:bottom w:w="60" w:type="dxa"/><w:right w:w="80" w:type="dxa"/></w:tcMar></w:tcPr>'
           '<w:p><w:pPr><w:jc w:val="left"/></w:pPr><w:r><w:rPr>'
           '<w:rFonts w:ascii="微软雅黑" w:hAnsi="微软雅黑" w:eastAsia="微软雅黑" w:cs="微软雅黑"/>'
           '<w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr><w:t>' + c + '</w:t></w:r></w:p></w:tc>'
           for c in (unit + '：____________', '姓名：____________', '得分：____________')) +
       '</w:tr></w:tbl>')

SPACER = ('<w:p><w:pPr><w:spacing w:after="80"/><w:rPr><w:sz w:val="28"/>'
          '<w:szCs w:val="28"/></w:rPr></w:pPr></w:p>')

def p_body(text, bold=False, sz=24, after=20):
    """正文段落：宋体，两端对齐，1.5 倍行距，与参考试卷逐字段一致。"""
    b = '<w:b/>' if bold else '<w:b w:val="0"/>'
    rpr = ('<w:rFonts w:ascii="宋体" w:hAnsi="宋体" w:eastAsia="宋体"/>' + b +
           '<w:sz w:val="%d"/><w:szCs w:val="28"/>' % sz)
    return ('<w:p><w:pPr>' + PPR_COMMON +
            '<w:spacing w:before="0" w:after="%d" w:line="360" w:lineRule="auto"/>' % after +
            '<w:jc w:val="both"/><w:textAlignment w:val="auto"/>'
            '<w:rPr><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr></w:pPr>'
            '<w:r><w:rPr>' + rpr + '</w:rPr><w:t xml:space="preserve">' + E(text) + '</w:t></w:r></w:p>')

p_head = lambda t: p_body(t, bold=True, sz=28, after=20)      # 一、二、三 大题标题
p_q    = lambda t, after=20: p_body(t, sz=24, after=after)    # 题干

BLANK_LINES = 8   # 每题留给学员作答的空行数

def p_blank():
    """空行（一个回车），行距与正文一致，供学员手写作答。"""
    return ('<w:p><w:pPr>' + PPR_COMMON +
            '<w:spacing w:before="0" w:after="20" w:line="360" w:lineRule="auto"/>'
            '<w:jc w:val="both"/><w:textAlignment w:val="auto"/>'
            '<w:rPr><w:rFonts w:ascii="宋体" w:hAnsi="宋体" w:eastAsia="宋体"/>'
            '<w:sz w:val="24"/><w:szCs w:val="28"/></w:rPr></w:pPr></w:p>')

p_answer_space = lambda: ''.join(p_blank() for _ in range(BLANK_LINES))

SECT = ('<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="1304" w:right="1247" w:bottom="1134" w:left="1361" '
        'w:header="720" w:footer="720" w:gutter="0"/>'
        '<w:cols w:space="720" w:num="1"/>'
        '<w:docGrid w:linePitch="360" w:charSpace="0"/></w:sectPr>')


def build_document_xml(head_xml, paper):
    body = [p_title(paper['title']), p_subtitle('（考试时长：60分钟 满分：100分）'),
            TBL(paper.get('unit', '班组')), SPACER]
    body.append(p_head('一、简答题（共20分）'))
    body.append(p_q(paper['short'], after=60))
    body.append(p_answer_space())
    body.append(p_head('二、论述题（每题25分，共50分）'))
    for i, q in enumerate(paper['essays'], 1):
        body.append(p_q('%d. %s' % (i, q), after=40))
        body.append(p_answer_space())
    body.append(p_head('三、案例分析（共30分）'))
    body.append(p_q(paper['case'], after=40))
    body.append(p_body('问题：', bold=True, sz=24, after=20))
    body.append(p_q(paper['case_q'], after=20))
    body.append(p_answer_space())
    return head_xml + '<w:body>' + ''.join(body) + SECT + '</w:body></w:document>'


def write_paper(paper, out_path):
    with zipfile.ZipFile(SRC) as zin:
        names = zin.namelist()
        src_doc = zin.read('word/document.xml').decode('utf-8')
        head_xml = src_doc[:src_doc.index('<w:body>')]
        new_doc = build_document_xml(head_xml, paper).encode('utf-8')
        tmp = out_path + '.tmp'
        with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
            for n in names:
                data = zin.read(n)
                if n == 'word/document.xml':
                    data = new_doc
                elif n == 'docProps/core.xml':
                    data = re.sub(rb'<dc:title>.*?</dc:title>', b'', data)
                zout.writestr(n, data)
    shutil.move(tmp, out_path)
    print('written:', out_path)
