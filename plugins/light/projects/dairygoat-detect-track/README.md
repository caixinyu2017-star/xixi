# 奶山羊检测(YOLOv11) + ByteTrack 跟踪

规模化羊场监控视频的个体定位与跨帧关联,作为下游时序行为识别(采食/反刍/站立/躺卧/爬跨/跛行)的前端。

## 流水线
视频帧 → YOLOv11 检测(定位个体) → ByteTrack 跨帧关联个体 ID → `(frame, track_id, bbox, conf)` JSONL → 下游时序行为识别。

## 选型依据(均来自 Light 知识库,可核查)
- 检测 YOLOv11:db03 方法卡 `implementation_repo: ultralytics/ultralytics`;anchor-free、含 OBB 旋转框(利于俯拍贴合朝向)、边缘友好。
- 跟踪 ByteTrack:db03 方法卡(`ifzhang/ByteTrack` / ultralytics 内置)。core_assumption 是低分框二次关联,恰好救回栏舍遮挡羊只。
- **不用 re-id**:db04 dairy goat 专项卡与 db03 场景表明确警示——同品种白色奶山羊外观高度相似,DeepSORT/FairMOT/StrongSORT 的 embedding 区分度低、易 ID switch。故选纯运动/位置驱动的 ByteTrack。移动/云台相机再换 BoT-SORT(开 CMC)。

## 数据现状(db04 真实核查,2026-06-06)
- **CherryChèvre**(Scientific Data 2023, DOI:10.1038/s41597-023-02555-8;数据 DOI:10.57745/4C03OG):同为山羊、自然环境检测、已提供 YOLO 格式标注 → 最直接的迁移预训练/补充数据源。
- **GoatABRD**(GSCW-YOLO, Animals 2024, DOI:10.3390/ani14243667):奶山羊行为(含跛行),许可未声明需联系作者。
- 缺口:暂无"奶山羊姿态关键点 + 多场景 + 个体ID"的大规模开源许可基准 → 需自建(俯拍+侧视双视角、同步 RFID/耳标作 ID ground truth)。

## 环境与运行(uv)
```bash
uv sync                                   # 按 uv.lock 精确复现
uv run python -m src.train --config configs/train.yaml
uv run python -m src.train --config configs/train.yaml --stage finetune_ir   # 红外微调
uv run python -m src.infer_track \
    --weights runs/goat_det/yolo11m_1280/weights/best.pt \
    --source path/to/barn_video.mp4 \
    --tracker configs/bytetrack_goat.yaml --out tracks.jsonl
```

## 质量门
```bash
uv run pytest -x          # 纯逻辑测试(序列化/IO),不需 GPU
uv run ruff check . && uv run ruff format --check .
```

## 复现
固定 `seed=42`;依赖在 `pyproject.toml` 锁定版本区间,提交 `uv.lock` 做精确还原;数据划分需确定性(train/val/test 固定)。

## 投稿定位(db01,可选)
精准畜牧方向:Computers and Electronics in Agriculture、Biosystems Engineering、Animals (MDPI)、Journal of Dairy Science。
