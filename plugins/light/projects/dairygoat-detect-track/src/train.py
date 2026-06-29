"""奶山羊检测模型 (YOLOv11) 训练入口。

依据: db03-methods/cards_detection_tracking.md 的 YOLOv11 卡
      (implementation_repo: ultralytics/ultralytics)。
复现: 固定随机种子 + 锁依赖版本 (见 pyproject.toml) + 确定性数据划分。

运行:
    uv run python -m src.train --config configs/train.yaml
    # 红外微调:
    uv run python -m src.train --config configs/train.yaml --stage finetune_ir
"""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml
from ultralytics import YOLO


def load_config(config_path: str | Path) -> dict:
    """读取 YAML 配置。配置化而非硬编码超参 (SKILL: 可维护/可复现)。"""
    with open(config_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def train_detector(cfg: dict) -> Path:
    """基础检测训练: COCO/CherryChèvre 预训练权重 → 奶山羊数据微调。

    返回 best.pt 路径, 供下游推理/红外微调/导出复用。
    """
    t = cfg["train"]
    model = YOLO(cfg["model"])  # 加载预训练权重 (迁移学习, 小数据更稳)
    results = model.train(
        data=t["data"],
        epochs=t["epochs"],
        imgsz=t["imgsz"],
        batch=t["batch"],
        device=t["device"],
        workers=t["workers"],
        optimizer=t["optimizer"],
        cos_lr=t["cos_lr"],
        patience=t["patience"],
        close_mosaic=t["close_mosaic"],
        seed=cfg["seed"],  # 确定性: 同种子同环境可复现
        hsv_h=t["hsv_h"],
        hsv_s=t["hsv_s"],
        hsv_v=t["hsv_v"],
        degrees=t["degrees"],
        fliplr=t["fliplr"],
        mosaic=t["mosaic"],
        project=t["project"],
        name=t["name"],
    )
    return Path(results.save_dir) / "weights" / "best.pt"


def finetune_infrared(cfg: dict) -> Path:
    """红外/夜间微调: 在 RGB 最优权重上小学习率续训, 防灾难性遗忘。

    依据 db03 场景段: 夜间红外 RGB 预训练域差大, 需红外微调而非直接迁移。
    """
    ft = cfg["finetune_ir"]
    model = YOLO(ft["weights"])
    results = model.train(
        data=cfg["train"]["data"],
        epochs=ft["epochs"],
        imgsz=cfg["train"]["imgsz"],
        lr0=ft["lr0"],
        seed=cfg["seed"],
        project=cfg["train"]["project"],
        name=cfg["train"]["name"] + "_ir",
    )
    return Path(results.save_dir) / "weights" / "best.pt"


def main() -> None:
    parser = argparse.ArgumentParser(description="Dairy goat YOLOv11 detector training")
    parser.add_argument("--config", default="configs/train.yaml")
    parser.add_argument(
        "--stage",
        default="train",
        choices=["train", "finetune_ir"],
        help="train: 基础检测; finetune_ir: 红外微调",
    )
    args = parser.parse_args()
    cfg = load_config(args.config)

    if args.stage == "finetune_ir":
        best = finetune_infrared(cfg)
    else:
        best = train_detector(cfg)
    print(f"Best weights: {best}")


if __name__ == "__main__":
    main()
