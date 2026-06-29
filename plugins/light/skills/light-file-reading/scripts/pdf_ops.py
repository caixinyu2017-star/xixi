#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PDF 读取与结构操作工具集（light-file-reading）。

依赖：pypdf（结构操作/内嵌文本），pdfplumber（版面文本+表格），pandas（表格→DataFrame）。
扫描件 OCR 不在此处——见 references/PDF-REF.md（pytesseract+pdf2image）。

所有函数可独立调用。

CLI（处理真实文件）：
    python pdf_ops.py meta        f.pdf
    python pdf_ops.py extract-text f.pdf [--pages 1-3,5] [--no-layout]
    python pdf_ops.py extract-tables f.pdf
    python pdf_ops.py merge a.pdf b.pdf --out merged.pdf
    python pdf_ops.py split      f.pdf --out-dir parts/
    python pdf_ops.py rotate     f.pdf --out r.pdf [--degrees 90] [--pages 1,2]
自检（reportlab 合成、离线、自清理）：
    python pdf_ops.py --selftest
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")  # Windows 控制台默认 GBK，强制 UTF-8 防乱码


def _imp(mod, pip_name=None):
    """惰性导入，缺失时给 pip 提示而非裸 ImportError。"""
    import importlib
    try:
        return importlib.import_module(mod)
    except ImportError as e:  # pragma: no cover - 仅依赖缺失时触发
        raise SystemExit(f"缺少 {mod}，请先安装：pip install {pip_name or mod}") from e


def read_meta(path):
    """读取页数与元数据（标题/作者/主题等），返回 dict。"""
    pypdf = _imp("pypdf")
    r = pypdf.PdfReader(path)
    m = r.metadata or {}
    return {
        "pages": len(r.pages),
        "title": m.get("/Title"),
        "author": m.get("/Author"),
        "subject": m.get("/Subject"),
        "creator": m.get("/Creator"),
    }


def extract_text(path, layout=True, pages=None):
    """逐页抽文本。layout=True 用 pdfplumber 保留版面（推荐论文/多栏）。
    pages 为 0 起页索引可迭代对象（None=全部），返回 [(page_no, text), ...]
    （page_no 从 1 起，对应原文档真实页号）。"""
    pdfplumber = _imp("pdfplumber")
    want = set(pages) if pages is not None else None
    out = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages):
            if want is not None and i not in want:
                continue
            txt = page.extract_text(layout=layout) or ""
            out.append((i + 1, txt))
    return out


def extract_tables(path):
    """抽所有表格 → [DataFrame]。首行作表头。空表跳过。"""
    pdfplumber = _imp("pdfplumber")
    pd = _imp("pandas")
    dfs = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            for tbl in page.extract_tables():
                if tbl and len(tbl) > 1:
                    dfs.append(pd.DataFrame(tbl[1:], columns=tbl[0]))
    return dfs


def merge(paths, out_path):
    """合并多个 PDF 为一个，返回输出页数。"""
    pypdf = _imp("pypdf")
    w = pypdf.PdfWriter()
    for p in paths:
        for page in pypdf.PdfReader(p).pages:
            w.add_page(page)
    with open(out_path, "wb") as f:
        w.write(f)
    return len(w.pages)


def split(path, out_dir):
    """每页拆成单独 PDF，返回生成的文件路径列表。"""
    import os
    pypdf = _imp("pypdf")
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    for i, page in enumerate(pypdf.PdfReader(path).pages, 1):
        w = pypdf.PdfWriter()
        w.add_page(page)
        op = os.path.join(out_dir, f"page_{i}.pdf")
        with open(op, "wb") as f:
            w.write(f)
        paths.append(op)
    return paths


def rotate(path, out_path, degrees=90, pages=None):
    """旋转指定页（pages 为 0 起索引列表，None=全部），degrees 顺时针。"""
    pypdf = _imp("pypdf")
    r = pypdf.PdfReader(path)
    w = pypdf.PdfWriter()
    for i, page in enumerate(r.pages):
        if pages is None or i in pages:
            page.rotate(degrees)
        w.add_page(page)
    with open(out_path, "wb") as f:
        w.write(f)
    return out_path


def parse_page_range(spec):
    """把 '1-3,5' 这类 1 起的页范围字符串解析为排序去重的 0 起索引列表。
    None 或空串返回 None（表示全部）。"""
    if not spec:
        return None
    idx = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            lo, hi = int(a), int(b)
            if lo > hi:
                lo, hi = hi, lo
            for n in range(lo, hi + 1):
                idx.add(n - 1)
        else:
            idx.add(int(part) - 1)
    bad = [i for i in idx if i < 0]
    if bad:
        raise SystemExit(f"页范围非法（页号从 1 起）：{spec}")
    return sorted(idx)


def _selftest():
    """合成测试 PDF（reportlab）跑全流程，断言每步结果，结束清理临时文件。"""
    import os
    import tempfile
    _imp("reportlab")
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors

    # 先验证纯函数 parse_page_range（无需文件）
    assert parse_page_range("1-3,5") == [0, 1, 2, 4], parse_page_range("1-3,5")
    assert parse_page_range(None) is None
    assert parse_page_range("2") == [1]

    tmp = tempfile.mkdtemp(prefix="pdfops_")
    try:
        src = os.path.join(tmp, "sample.pdf")
        styles = getSampleStyleSheet()
        tbl = Table([["Metric", "Value"], ["Accuracy", "0.91"], ["F1", "0.88"]])
        tbl.setStyle([("GRID", (0, 0), (-1, -1), 1, colors.black)])
        story = [
            Paragraph("Light File Reading Self Test", styles["Title"]),
            Paragraph("This is page one body text for extraction.", styles["Normal"]),
            tbl,
            PageBreak(),
            Paragraph("Second page content.", styles["Normal"]),
        ]
        SimpleDocTemplate(src, pagesize=letter).build(story)

        meta = read_meta(src)
        assert meta["pages"] == 2, meta

        text = extract_text(src)
        assert len(text) == 2 and "page one" in text[0][1], text[0][1][:80]

        # 页范围：只取第 2 页，page_no 仍是真实页号 2
        only2 = extract_text(src, pages=[1])
        assert len(only2) == 1 and only2[0][0] == 2, only2

        tables = extract_tables(src)
        assert tables and list(tables[0].columns) == ["Metric", "Value"], tables

        merged = os.path.join(tmp, "merged.pdf")
        assert merge([src, src], merged) == 4

        parts = split(src, os.path.join(tmp, "parts"))
        assert len(parts) == 2

        rot = rotate(src, os.path.join(tmp, "rot.pdf"), 90, pages=[0])
        assert read_meta(rot)["pages"] == 2
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)
    print("pdf_ops self-test OK: "
          "meta/text/pagerange/tables/merge/split/rotate all passed")


def _cli(argv):
    import argparse
    import json
    ap = argparse.ArgumentParser(prog="pdf_ops.py", description="PDF 读取与结构操作")
    ap.add_argument("--selftest", action="store_true",
                    help="reportlab 合成自检（离线、自清理），CI 用此标志")
    sub = ap.add_subparsers(dest="cmd")

    sub.add_parser("meta", help="页数+元数据").add_argument("file")

    sp = sub.add_parser("extract-text", help="逐页抽文本")
    sp.add_argument("file")
    sp.add_argument("--pages", help="页范围 1 起，如 1-3,5（默认全部）")
    sp.add_argument("--no-layout", action="store_true", help="不保留版面")

    sub.add_parser("extract-tables", help="抽表格").add_argument("file")

    sp = sub.add_parser("merge", help="合并多个 PDF")
    sp.add_argument("files", nargs="+")
    sp.add_argument("--out", required=True)

    sp = sub.add_parser("split", help="逐页拆分")
    sp.add_argument("file")
    sp.add_argument("--out-dir", required=True)

    sp = sub.add_parser("rotate", help="旋转页面")
    sp.add_argument("file")
    sp.add_argument("--out", required=True)
    sp.add_argument("--degrees", type=int, default=90)
    sp.add_argument("--pages", help="页范围 1 起（默认全部）")

    args = ap.parse_args(argv)

    if args.selftest:
        _selftest()
        return
    if not args.cmd:
        ap.print_help()
        raise SystemExit(2)

    if args.cmd == "meta":
        print(json.dumps(read_meta(args.file), ensure_ascii=False, indent=2))
    elif args.cmd == "extract-text":
        for no, txt in extract_text(args.file, layout=not args.no_layout,
                                    pages=parse_page_range(args.pages)):
            print(f"===== page {no} =====")
            print(txt)
    elif args.cmd == "extract-tables":
        dfs = extract_tables(args.file)
        print(f"抽到 {len(dfs)} 个表格")
        for i, df in enumerate(dfs, 1):
            print(f"--- table {i} (shape={df.shape}) ---")
            print(df.to_csv(index=False))
    elif args.cmd == "merge":
        n = merge(args.files, args.out)
        print(f"合并 {len(args.files)} 个 PDF → {args.out}（{n} 页）")
    elif args.cmd == "split":
        parts = split(args.file, args.out_dir)
        print(f"拆出 {len(parts)} 页到 {args.out_dir}")
    elif args.cmd == "rotate":
        out = rotate(args.file, args.out, degrees=args.degrees,
                     pages=parse_page_range(args.pages))
        print(f"旋转完成 → {out}")


if __name__ == "__main__":
    _cli(sys.argv[1:])
