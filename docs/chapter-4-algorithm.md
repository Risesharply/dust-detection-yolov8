# 第四章算法与代码对应关系

本仓库是论文第四章 YOLOv8 对照实验实现，与 `dust-detection-yolov5` 共享基于多目标跟踪的扬尘时序筛选思想。

## 检测网络支持

- `ultralytics/nn/modules/conv.py`：`GhostConv`、`CBAM` 及注意力模块。
- `ultralytics/nn/modules/block.py`：`C3Ghost`、`GhostBottleneck`。
- `ultralytics/nn/tasks.py`：模型 YAML 解析和模块构建。

当前目录中未确认唯一的论文专用 YOLOv8 YAML，因此发布文档不指定未经验证的配置文件。复现时应补充实验实际使用的 YAML 或训练参数记录。

## 时序与跟踪核心

| 论文职责 | 代码 |
| --- | --- |
| 检测框 IoU/GIoU 计算与匹配 | `refine/iou_giou_matching.py` |
| 单条轨迹状态和生命周期 | `refine/track.py` |
| 多目标轨迹集合更新 | `refine/Tracker.py` |
| 扬尘框时序筛选 | `refine/TSYDD.py` |
| 设备/装载状态运动判断 | `refine/PPMove.py` |
| Flask/视频流集成 | `examples/dust/web/serve.py` |

跟踪实现参考并改编自 `bochinski/iou-tracker`，加入 GIoU 匹配、适用于扬尘目标的轨迹状态判定以及 YOLO 检测张量筛选。版权与修改声明见 `NOTICE.md`。

## 对照实验边界

YOLOv8 与 YOLOv5 版本共享算法核心，但保留各自的默认 `max_age`、输入接口和集成代码。为了忠实复现实验，不以其中一个目录覆盖另一个目录。
