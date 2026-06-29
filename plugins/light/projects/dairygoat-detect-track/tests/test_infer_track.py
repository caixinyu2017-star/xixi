"""TrackRecord 序列化与 JSONL 落盘的单元测试 (不依赖 GPU/模型)。

只测纯逻辑 (序列化/IO), 模型推理用集成测试单独跑。
运行: uv run pytest -x
"""

from __future__ import annotations

import json
from dataclasses import asdict

from src.infer_track import TrackRecord, write_jsonl


def test_track_record_roundtrip():
    rec = TrackRecord(frame=3, track_id=7, x1=1.0, y1=2.0, x2=3.0, y2=4.0, conf=0.91)
    d = asdict(rec)
    assert d == {
        "frame": 3,
        "track_id": 7,
        "x1": 1.0,
        "y1": 2.0,
        "x2": 3.0,
        "y2": 4.0,
        "conf": 0.91,
    }


def test_write_jsonl_counts_and_format(tmp_path):
    recs = [
        TrackRecord(0, 1, 0, 0, 10, 10, 0.8),
        TrackRecord(0, 2, 20, 20, 30, 30, 0.5),
        TrackRecord(1, 1, 1, 1, 11, 11, 0.82),
    ]
    out = tmp_path / "tracks.jsonl"
    n = write_jsonl(iter(recs), out)
    assert n == 3
    lines = out.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 3
    first = json.loads(lines[0])
    assert first["track_id"] == 1 and first["frame"] == 0
