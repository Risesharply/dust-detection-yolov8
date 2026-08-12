# 基于 YOLOv8 的扬尘检测对照实验

本仓库包含两种相互独立的正式方法：

1. YOLOv8 检测后接 GIoU 轨迹关联与时序 refine 后处理。
2. YOLOv8 检测候选区域后接 EfficientNetV2-S 二分类器。

## 运行入口

```powershell
pip install -e .
python scripts/run_tracking.py --weights weights/yolo.pt --source video.mp4 --device 0
python scripts/run_cascade.py --detector weights/yolo.pt --classifier weights/efficientnetv2.pth --source video.mp4
python scripts/run_flask_multicam.py --config configs/cameras.local.yaml
```

数据集、检测权重、分类权重、真实 RTSP 地址和输出文件不随公开仓库发布。
详细步骤见 [复现说明](docs/REPRODUCTION.md)。

## 项目结构

- `methods/refine_tracking/`：时序 refine 后处理。
- `methods/yolo_efficientnetv2/`：自包含的级联分类方法和检查点兼容模型。
- `scripts/`：三个标准运行文件。
- `apps/flask_multicam/`：动态多摄像头 Flask 服务。
- `configs/cameras.example.yaml`：tracking/cascade 双模式脱敏配置。
- [YOLOv8 改动说明](docs/YOLOV8_CHANGES.md)：相对上游的改动和数据流。

## 来源与许可

项目基于 [Ultralytics](https://github.com/ultralytics/ultralytics)，保留仓库
中的 GNU AGPL v3 许可证和 Git 历史。跟踪实现参考并改编自
[bochinski/iou-tracker](https://github.com/bochinski/iou-tracker)（MIT
License）。详细版权与论文引用见 [NOTICE.md](NOTICE.md)。
