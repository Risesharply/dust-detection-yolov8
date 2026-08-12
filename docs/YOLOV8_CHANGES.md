# 相对原版 Ultralytics YOLOv8 的改动

本仓库不修改 Ultralytics 核心推理代码，项目功能通过外部方法包和入口接入：

- `methods/refine_tracking/`：论文第四章的 GIoU 时序后处理。
- `methods/yolo_efficientnetv2/`：YOLO 检测后级联 EfficientNetV2-S 二分类。
- `scripts/run_tracking.py`：YOLOv8 + refine。
- `scripts/run_cascade.py`：YOLOv8 + EfficientNetV2。
- `apps/flask_multicam/` 与 `scripts/run_flask_multicam.py`：多摄像头服务。

Refine 数据流为 `YOLO -> boxes.data -> refine -> result.plot()`；级联数据流为
`YOLO -> 候选类别筛选 -> 扩框/裁剪 -> EfficientNetV2 -> 结果关联/绘制`。

本次整理修复了旧实现的错误类方法导入、全局 `sys.path` 修改、动态 `eval`
构建失败、本地绝对路径、张量切片索引、资源未释放和逐帧调试输出问题。
