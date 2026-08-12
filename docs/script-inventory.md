# 脚本分类清单

## 上游结构

`ultralytics/`、`tests/`、`docs/`、`examples/`、`docker/` 和打包配置属于上游工程结构，保持原位置。

## 当前论文与部署示例

- `examples/dust/web/serve.py`：YOLOv8、`refine` 和装载设备分类器的视频流服务入口。
- `examples/dust/preprocessing/crop_loader_area.py`：区域裁剪实验。
- `examples/dust/classification/class_names.py`：分类标签草稿。
- `examples/dust/experiments/`：视频预测、旧 YOLOv5 演示和 NumPy 草稿。
- `archive/legacy/web/flask_yolo1.py`：被当前服务入口替代的历史快照。

## 本地依赖快照

`proxy_package/` 是当前服务调用的装载设备分类依赖，因此保留源码、排除模型权重。默认检查点路径相对于 `proxy_package/models/efficientnetv2/efficientnetv2_s.py` 解析；运行前需把权重放到该文件同目录。该分类模块不是扬尘跟踪核心。
