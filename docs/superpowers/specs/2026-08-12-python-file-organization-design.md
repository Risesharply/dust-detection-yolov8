# YOLOv8 Python 文件平衡整理设计

日期：2026-08-12

## 目标

将仓库根目录中的个人实验脚本按部署、分类、预处理和历史实验分类，保持 Ultralytics 上游包结构稳定，并让论文第四章的当前入口与旧快照一目了然。

## 根目录边界

上游 `setup.py` 继续保留在根目录。个人脚本不再散落在根目录；`refine/` 和 `proxy_package/` 作为当前功能包保留在顶层，因为 Flask 集成直接依赖它们。

## 目标结构

```text
examples/dust/
├── web/             # 当前 Flask/视频流服务入口
├── classification/  # 装载设备分类调用示例
├── preprocessing/   # 区域裁剪与图像预处理
└── experiments/     # 已识别但尚非正式入口的实验脚本

archive/legacy/
└── web/             # 被当前服务入口替代的 Flask 快照
```

`flask_yolo.py` 作为当前 Web 服务入口；`flask_yolo1.py` 作为历史快照归档。`class.py`、`crop_loader_area.py`、`demo_jilian.py`、`first.py` 和 `test.py` 根据实际依赖与行为分别归入上述示例目录，不删除非完全重复脚本。

## `proxy_package` 处理

`proxy_package/` 是当前 Flask 服务的分类依赖，因此保留源码。模型检查点继续由 `.gitignore` 排除。`proxy_package/models/efficientnetv2/efficientnetv2_s.py` 中写死的旧电脑权重路径改为相对默认路径或显式参数，错误信息应说明如何提供权重；不改变分类网络结构和预测语义。

## 导入与兼容性

移动后的示例从仓库根目录运行。每个当前入口的导入路径必须更新并通过静态检查；README 与 `docs/script-inventory.md` 同步更新。历史脚本只保证语法可解析，并注明所需旧资产或环境。

不改动 `ultralytics/` 上游包结构，不合并 YOLOv5 与 YOLOv8 的 `refine` 参数，也不向官方 `upstream` 推送。

## 验证与发布

- 当前 `refine` 聚焦测试全部通过。
- 移动后的当前示例通过语法编译和导入路径检查。
- 分类器权重路径不再写死到旧机器盘符。
- 根目录只剩上游入口和顶层功能包，不再散落个人实验脚本。
- Git 变更不包含权重、媒体、训练输出或缓存。
- 变更以独立提交推送至 `Risesharply/dust-detection-yolov8`；官方仓库保留为 `upstream`。

