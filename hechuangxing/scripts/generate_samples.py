# -*- coding: utf-8 -*-
"""生成 samples 目录下的三份 Word 样张。

    python scripts/generate_samples.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from hcx import content_bp, content_improve, content_landing, docx_style  # noqa: E402

OUT = ROOT / "samples"
OUT.mkdir(parents=True, exist_ok=True)

JOBS = [
    ("测试用-网媒投稿发表公司创业计划书.docx", content_bp.blocks()),
    ("输出示例1-创业计划改进方案.docx", content_improve.blocks()),
    ("输出示例2-全链条创业落地方案.docx", content_landing.blocks()),
]

for name, blocks in JOBS:
    path = OUT / name
    docx_style.render(blocks, str(path))
    print(f"  已生成 {name}  （{len(blocks)} 个内容块，{path.stat().st_size // 1024} KB）")

print("完成。文件在 samples 目录下。")
