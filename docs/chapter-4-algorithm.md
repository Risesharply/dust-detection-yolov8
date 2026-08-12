# 第四章方法与源码对应关系

本仓库包含两个独立实验流程：

| 方法 | 当前源码 | 运行入口 |
| --- | --- | --- |
| YOLOv8 + GIoU 时序 refine | `methods/refine_tracking/` | `scripts/run_tracking.py` |
| YOLOv8 + EfficientNetV2 二分类 | `methods/yolo_efficientnetv2/` | `scripts/run_cascade.py` |
| 多摄像头部署 | `apps/flask_multicam/` | `scripts/run_flask_multicam.py` |

Refine 的检测张量格式、级联裁剪和分类预处理参数分别记录在两个方法目录的
README 中。两个流程共享 YOLO 检测器，但不会隐式混合后处理状态。
