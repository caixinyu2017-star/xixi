"""to_pdf.py — 把 .pptx 转 PDF，优先用 LibreOffice(soffice) 无头转换。

用法：
    python to_pdf.py deck.pptx                  # -> deck.pdf（同目录）
    python to_pdf.py deck.pptx -o out/slides.pdf
    python to_pdf.py deck.pptx --check          # 只探测可用引擎并退出

设计：soffice 是把 pptx 转 PDF 最可靠的离线方式（保真度高、可再 pdftoppm
出图做视觉 QA）。本环境默认未装 LibreOffice——脚本会清楚报告它不可用，
并给出安装指引与备选（thumbnail.py 的 pillow 版式示意 / 装 PyMuPDF 走图像）。
绝不静默失败或假装成功。
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
import os
import shutil
import argparse
import subprocess

SOFFICE_CANDIDATES = (
    "soffice", "libreoffice",
    r"C:\Program Files\LibreOffice\program\soffice.exe",
    r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
    "/usr/bin/soffice", "/usr/bin/libreoffice",
    "/Applications/LibreOffice.app/Contents/MacOS/soffice",
)


def find_soffice():
    for cand in SOFFICE_CANDIDATES:
        if shutil.which(cand) or os.path.exists(cand):
            return shutil.which(cand) or cand
    return None


def convert(pptx_path, out_path=None, timeout=180):
    """用 soffice 把 pptx 转 pdf。返回 (ok, message, pdf_path)。"""
    if not os.path.exists(pptx_path):
        return False, f"找不到输入文件：{pptx_path}", None
    soffice = find_soffice()
    if not soffice:
        msg = (
            "LibreOffice(soffice) 不可用，无法直接转 PDF。\n"
            "  安装：Windows 装 LibreOffice 后把 program 目录加进 PATH；\n"
            "        Linux: apt install libreoffice  / mac: brew install --cask libreoffice\n"
            "  备选：① python scripts/thumbnail.py deck.pptx（pillow 版式示意，无需 soffice）\n"
            "        ② pip install PyMuPDF 后用 thumbnail.py 的 soffice 引擎做像素渲染（仍需 soffice 转 PDF）\n"
            "        ③ 在装有 PowerPoint 的机器上『另存为 PDF』"
        )
        return False, msg, None

    base = os.path.splitext(os.path.basename(pptx_path))[0]
    outdir = os.path.dirname(os.path.abspath(out_path)) if out_path \
        else os.path.dirname(os.path.abspath(pptx_path))
    os.makedirs(outdir, exist_ok=True)
    try:
        proc = subprocess.run(
            [soffice, "--headless", "--convert-to", "pdf",
             "--outdir", outdir, os.path.abspath(pptx_path)],
            capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return False, f"soffice 转换超时（>{timeout}s）", None
    produced = os.path.join(outdir, base + ".pdf")
    if proc.returncode != 0 or not os.path.exists(produced):
        return False, f"soffice 返回 {proc.returncode}：{proc.stderr.strip()}", None
    if out_path and os.path.abspath(out_path) != os.path.abspath(produced):
        shutil.move(produced, out_path)
        produced = out_path
    size_kb = os.path.getsize(produced) / 1024
    return True, f"转换成功（{size_kb:.0f} KB）", produced



def _selftest() -> int:
    missing = os.path.join(os.path.dirname(os.path.abspath(__file__)), "__missing__.pptx")
    ok, msg, pdf = convert(missing)
    assert ok is False and pdf is None and "找不到" in msg, (ok, msg, pdf)
    soffice = find_soffice()
    assert soffice is None or isinstance(soffice, str), soffice
    print(f"[selftest] PASS to_pdf soffice={'yes' if soffice else 'no'}")
    return 0


def main():
    ap = argparse.ArgumentParser(description="pptx -> pdf（LibreOffice 无头转换）")
    ap.add_argument("pptx", nargs="?")
    ap.add_argument("-o", "--out", help="输出 PDF 路径（默认同名同目录）")
    ap.add_argument("--check", action="store_true", help="只探测引擎可用性")
    ap.add_argument("--selftest", action="store_true", help="run offline conversion precondition self-test")
    args = ap.parse_args()

    if args.selftest:
        raise SystemExit(_selftest())

    if args.check:
        s = find_soffice()
        print(f"soffice: {'可用 -> ' + s if s else '不可用'}")
        sys.exit(0 if s else 1)

    if not args.pptx:
        ap.error("需要提供 pptx 路径（或用 --check）")
    ok, msg, pdf = convert(args.pptx, args.out)
    print(("[ok] " if ok else "[unavailable] ") + msg)
    if ok:
        print(f"  -> {pdf}")
    sys.exit(0 if ok else 2)


if __name__ == "__main__":
    main()
