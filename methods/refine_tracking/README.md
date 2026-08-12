# Refine 时序后处理

该方法处理 YOLOv8 检测结果中的
`[x1, y1, x2, y2, confidence, class_id]` 张量，通过跨帧 GIoU 关联和轨迹
状态筛除不稳定扬尘框。标准入口为 `scripts/run_tracking.py`。

跟踪部分参考并改编自
[bochinski/iou-tracker](https://github.com/bochinski/iou-tracker)（MIT
License，AVSS 2017/2018 IOU/V-IOU Tracker）。每路摄像头必须使用独立的
`RefinePostprocessor`，版权与引用见 `NOTICE.md`。
