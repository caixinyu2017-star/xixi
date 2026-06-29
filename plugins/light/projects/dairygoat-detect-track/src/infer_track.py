"""奶山羊检测 + ByteTrack 跟踪推理流水线。

数据流 (db02/方案主线): 视频帧 → YOLOv11 检测 → ByteTrack 跨帧关联个体 ID
                        → 输出 (frame, track_id, bbox, conf) → 交下游时序行为识别。

依据:
  - 检测: db03 YOLOv11 卡 (ultralytics/ultralytics)。
  - 跟踪: db03 ByteTrack 卡 (低分框二次关联, 无需 re-id, 规避奶山羊外观相似难题)。
  - ultralytics `model.track(..., persist=True)` 维持跨帧轨迹状态。

运行:
    uv run python -m src.infer_track \
        --weights runs/goat_det/yolo11m_1280/weights/best.pt \
        --source path/to/barn_video.mp4 \
        --tracker configs/bytetrack_goat.yaml \
        --out tracks.jsonl
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterator


@dataclass(frozen=True)
class TrackRecord:
    """单帧单个体的跟踪记录, 是下游行为识别的输入单元。"""

    frame: int
    track_id: int
    x1: float
    y1: float
    x2: float
    y2: float
    conf: float


def run_tracking(
    weights: str,
    source: str,
    tracker_cfg: str,
    conf: float = 0.25,
    iou: float = 0.7,
    imgsz: int = 1280,
    device: str = "0",
) -> Iterator[TrackRecord]:
    """逐帧产出跟踪记录 (生成器, 避免长视频一次性占满内存)。

    conf 取偏低值 (0.25): 让更多遮挡羊只的低分框进入 ByteTrack 的二次关联,
    这正是 ByteTrack 救回遮挡目标的机制 (db03 ByteTrack 卡 core_assumption)。
    """
    from ultralytics import YOLO  # 延迟导入: 纯逻辑(序列化/IO)测试无需加载重依赖

    model = YOLO(weights)
    # stream=True 惰性逐帧; persist=True 跨帧保持轨迹状态 (否则每帧重置 ID)
    results = model.track(
        source=source,
        tracker=tracker_cfg,
        conf=conf,
        iou=iou,
        imgsz=imgsz,
        device=device,
        persist=True,
        stream=True,
        verbose=False,
    )
    for frame_idx, r in enumerate(results):
        if r.boxes is None or r.boxes.id is None:
            continue  # 该帧无已确认轨迹 (如视频开头轨迹未起)
        ids = r.boxes.id.int().tolist()
        xyxy = r.boxes.xyxy.tolist()
        confs = r.boxes.conf.tolist()
        for tid, (x1, y1, x2, y2), c in zip(ids, xyxy, confs):
            yield TrackRecord(frame_idx, tid, x1, y1, x2, y2, c)


def write_jsonl(records: Iterator[TrackRecord], out_path: str | Path) -> int:
    """落盘为 JSONL (每行一条记录), 便于下游按 track_id 聚合成行为片段。

    返回写入条数。JSONL 流式可追加, 长视频不爆内存。
    """
    n = 0
    with open(out_path, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(asdict(rec)) + "\n")
            n += 1
    return n


def main() -> None:
    parser = argparse.ArgumentParser(description="Dairy goat detect + ByteTrack inference")
    parser.add_argument("--weights", required=True)
    parser.add_argument("--source", required=True, help="视频文件/目录/摄像头流")
    parser.add_argument("--tracker", default="configs/bytetrack_goat.yaml")
    parser.add_argument("--out", default="tracks.jsonl")
    parser.add_argument("--conf", type=float, default=0.25)
    parser.add_argument("--imgsz", type=int, default=1280)
    parser.add_argument("--device", default="0")
    args = parser.parse_args()

    records = run_tracking(
        weights=args.weights,
        source=args.source,
        tracker_cfg=args.tracker,
        conf=args.conf,
        imgsz=args.imgsz,
        device=args.device,
    )
    n = write_jsonl(records, args.out)
    print(f"Wrote {n} track records to {args.out}")


if __name__ == "__main__":
    main()
