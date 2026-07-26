"""Helpers for editing the submitted manuscript in place.

The revision is produced by editing the original .docx rather than rebuilding
it, so the MDPI template styles, the native OMML equations and every embedded
figure survive untouched.  All inserted or modified text is colour-coded by
reviewer, as requested:

    Reviewer 1 -> red        Reviewer 2 -> blue        Reviewer 3 -> green
"""
import copy

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

COLORS = {
    'R1': RGBColor(0xC0, 0x00, 0x00),      # red
    'R2': RGBColor(0x00, 0x70, 0xC0),      # blue
    'R3': RGBColor(0x00, 0xA0, 0x33),      # green
}
COLOR_NAMES = {'R1': 'red', 'R2': 'blue', 'R3': 'green'}


# ------------------------------------------------------------------ lookup
def iter_paragraphs(doc):
    return doc.paragraphs


def find_para(doc, needle, start=0, exact=False):
    """Index of the first paragraph containing `needle` (or None)."""
    for i, p in enumerate(doc.paragraphs[start:], start):
        t = p.text.strip()
        if (t == needle) if exact else (needle in p.text):
            return i
    return None


def para_by(doc, needle, **kw):
    i = find_para(doc, needle, **kw)
    if i is None:
        raise LookupError(f'paragraph not found: {needle!r}')
    return doc.paragraphs[i]


# ------------------------------------------------------------- new content
def _style_run(run, color, italic=False, bold=False, size=None):
    run.font.color.rgb = COLORS[color]
    run.font.bold = bold
    run.font.italic = italic
    if size:
        run.font.size = Pt(size)


def _clone_format(src_para, new_para):
    """Copy paragraph properties (style, spacing, indent) from src to new."""
    if src_para.style is not None:
        try:
            new_para.style = src_para.style
        except Exception:
            pass
    src_pPr = src_para._p.find(qn('w:pPr'))
    if src_pPr is not None:
        new_pPr = new_para._p.find(qn('w:pPr'))
        if new_pPr is not None:
            new_para._p.remove(new_pPr)
        new_para._p.insert(0, copy.deepcopy(src_pPr))


def insert_para_after(para, text, color, template=None, bold=False,
                      italic=False, align=None, style=None):
    """Insert a new paragraph directly after `para`; return it."""
    new_p = copy.deepcopy(para._p)
    for child in list(new_p):
        if child.tag != qn('w:pPr'):
            new_p.remove(child)
    para._p.addnext(new_p)
    from docx.text.paragraph import Paragraph
    np_ = Paragraph(new_p, para._parent)
    if template is not None:
        _clone_format(template, np_)
    if style is not None:
        try:
            np_.style = style
        except Exception:
            pass
    if align is not None:
        np_.alignment = align
    if text:
        _style_run(np_.add_run(text), color, italic=italic, bold=bold)
    return np_


def insert_paras_after(para, texts, color, **kw):
    """Insert several paragraphs in order; return the last one."""
    cur = para
    for t in texts:
        cur = insert_para_after(cur, t, color, **kw)
    return cur


def append_run(para, text, color, bold=False, italic=False):
    _style_run(para.add_run(text), color, bold=bold, italic=italic)
    return para


# --------------------------------------------------------- text surgery
def replace_in_para(para, old, new, color):
    """Replace `old` by `new` inside a paragraph, colouring only the new text.

    Works across run boundaries by rebuilding the paragraph's runs while
    preserving the formatting of the run that contained the start of `old`.
    """
    full = ''.join(r.text for r in para.runs)
    if old not in full:
        return False
    head, _, tail = full.partition(old)
    runs = list(para.runs)
    if not runs:
        return False
    keep = runs[0]
    for r in runs[1:]:
        r._element.getparent().remove(r._element)
    keep.text = head
    r_new = para.add_run(new)
    _style_run(r_new, color)
    if tail:
        para.add_run(tail)
    return True


def strike_and_replace(para, old, new, color):
    """Show a deletion as struck-through text followed by the new wording."""
    full = ''.join(r.text for r in para.runs)
    if old not in full:
        return False
    head, _, tail = full.partition(old)
    runs = list(para.runs)
    keep = runs[0]
    for r in runs[1:]:
        r._element.getparent().remove(r._element)
    keep.text = head
    r_del = para.add_run(old)
    _style_run(r_del, color)
    r_del.font.strike = True
    r_new = para.add_run(new)
    _style_run(r_new, color)
    if tail:
        para.add_run(tail)
    return True


# ------------------------------------------------------------------ tables
def insert_table_after(doc, para, rows, color, caption=None, template_style=None,
                       widths=None, header_bold=True):
    """Insert a caption paragraph plus a table right after `para`.

    Returns the empty paragraph that trails the table, so that further content
    can be chained after it in document order.
    """
    cur = para
    if caption:
        cur = insert_para_after(cur, caption, color, bold=False)
    ncols = max(len(r) for r in rows)
    rows = [list(r) + [''] * (ncols - len(r)) for r in rows]
    tbl = doc.add_table(rows=len(rows), cols=ncols)
    try:
        tbl.style = template_style or 'Table Grid'
    except Exception:
        pass
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = tbl.cell(i, j)
            cell.text = ''
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(str(val))
            _style_run(run, color, bold=(header_bold and i == 0), size=8.5)
    cur._p.addnext(tbl._tbl)
    trailer = insert_para_after(cur, '', color)
    trailer._p.getparent().remove(trailer._p)
    tbl._tbl.addnext(trailer._p)
    return trailer


def insert_picture_after(doc, para, path, color, caption, width):
    """Insert a centred picture plus its caption after `para`."""
    holder = insert_para_after(para, '', color)
    holder.alignment = WD_ALIGN_PARAGRAPH.CENTER
    holder.add_run().add_picture(path, width=width)
    cap = insert_para_after(holder, caption, color)
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    return cap
