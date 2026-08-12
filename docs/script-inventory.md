# 脚本分类清单

## 上游结构

`ultralytics/`、`tests/`、`docs/`、`examples/`、`docker/` 和打包配置属于上游工程结构，保持原位置。

## 论文与部署候选

- `flask_yolo.py`、`flask_yolo1.py`：YOLOv8 与 `refine` 的视频流/服务集成。
- `crop_loader_area.py`：区域裁剪实验。
- `class.py`、`first.py`、`test.py`、`demo_jilian.py`：个人实验脚本，功能和依赖仍需逐一验证。

## 本地依赖快照

`proxy_package/` 是 `flask_yolo.py` 和 `flask_yolo1.py` 调用的装载设备分类依赖，因此保留源码、排除模型权重。`proxy_package/models/efficientnetv2/efficientnetv2_s.py` 中仍有旧机器的绝对权重路径，运行前需改为本机权重位置；该分类模块不是扬尘跟踪核心。
