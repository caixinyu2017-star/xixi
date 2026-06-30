"""Helper: convert LaTeX math -> OMML (Word native equation) elements for python-docx.

Uses pandoc to render LaTeX into OMML, extracts the <m:oMath> element, and returns
an lxml element that can be inserted into a python-docx paragraph. Results cached.
"""
import os, re, subprocess, hashlib, functools
from lxml import etree
from docx.oxml.ns import qn
from docx.oxml import parse_xml

PANDOC = "/tmp/claude-0/-home-user-xixi/013086be-932a-56cd-b187-9ec3125f6bc6/scratchpad/pandoc-3.1.11/bin/pandoc"
CACHE = "/tmp/claude-0/-home-user-xixi/013086be-932a-56cd-b187-9ec3125f6bc6/scratchpad/.omml_cache"
os.makedirs(CACHE, exist_ok=True)

M_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

import zipfile
@functools.lru_cache(maxsize=2048)
def _omml_raw(latex):
    """Return the inner XML string of the <m:oMath> element for a LaTeX snippet."""
    h = hashlib.md5(latex.encode()).hexdigest()
    cf = os.path.join(CACHE, h + ".xml")
    if os.path.exists(cf):
        return open(cf, encoding="utf-8").read()
    md = f"${latex.strip()}$\n"          # no space after $ (pandoc would treat as literal)
    docx_path = os.path.join(CACHE, h + ".docx")
    p = subprocess.run([PANDOC, "-f", "markdown", "-t", "docx", "-o", docx_path],
                       input=md, text=True, capture_output=True)
    if p.returncode != 0:
        raise RuntimeError(f"pandoc failed for {latex!r}: {p.stderr}")
    z = zipfile.ZipFile(docx_path)
    xml = z.read("word/document.xml").decode("utf-8")
    m = re.search(r"<m:oMath\b.*?</m:oMath>", xml, re.S)
    if not m:
        raise RuntimeError(f"no oMath produced for {latex!r}")
    frag = m.group(0)
    open(cf, "w", encoding="utf-8").write(frag)
    return frag

def omath_element(latex):
    """Return an lxml <m:oMath> element with namespaces declared, ready to insert."""
    frag = _omml_raw(latex)
    # ensure namespaces are declared on the root element
    wrapped = frag.replace("<m:oMath>", f'<m:oMath xmlns:m="{M_NS}" xmlns:w="{W_NS}">', 1)
    if "xmlns:m" not in wrapped[:200]:
        # oMath may already have attrs; inject namespaces
        wrapped = re.sub(r"<m:oMath\b", f'<m:oMath xmlns:m="{M_NS}" xmlns:w="{W_NS}"', frag, count=1)
    return parse_xml(wrapped)

def add_math(paragraph, latex):
    """Append an inline equation to a python-docx paragraph."""
    paragraph._p.append(omath_element(latex))
    return paragraph

def add_text_and_math(paragraph, segments):
    """segments: list of ('text', s) or ('math', latex). Builds a mixed paragraph."""
    for kind, val in segments:
        if kind == "text":
            run = paragraph.add_run(val)
        else:
            paragraph._p.append(omath_element(val))
    return paragraph
