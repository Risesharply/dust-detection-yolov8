# YOLOv8 扬尘检测公开复现、级联分类与服务设计

## 目标

将仓库整理为适合公开复现的 YOLOv8 对照实验项目。保留与 YOLOv5 相同核心思想的 refine 后处理，同时把 `proxy_package` 中正式的 YOLO→EfficientNetV2 级联分类方法收敛为一个自包含方法目录，并提供命令行和 Flask 多摄像头入口。

## 范围

- 保留 Ultralytics 上游训练、验证、检测和导出能力。
- 将 refine 整理为 `methods/refine_tracking`。
- 将级联分类所需实现集中到 `methods/yolo_efficientnetv2`，删除未参与该方法的通用分类框架文件。
- 提供跟踪后处理、级联分类和 Flask 多摄像头入口。
- 删除个人实验、重复脚本、缓存、输出结果和本地绝对路径。
- 不提交检测或分类权重；文档说明预期文件名、放置位置和获取方式。

## 目录与接口

```text
methods/
  refine_tracking/
    __init__.py
    tracker.py
    matching.py
    filtering.py
    README.md
  yolo_efficientnetv2/
    __init__.py
    classifier.py
    pipeline.py
    config.py
    labels.txt
    model/efficientnetv2.py
    README.md
apps/flask_multicam/
  __init__.py
  app.py
  capture.py
  service.py
  templates/index.html
configs/cameras.example.yaml
scripts/run_tracking.py
scripts/run_cascade.py
scripts/run_flask_multicam.py
docs/YOLOV8_CHANGES.md
docs/REPRODUCTION.md
tests/dust/
```

方法包使用浅层结构和明确的 `__all__`。不保留 `proxy_package` 这种会急切导入大量无关骨干网络、损失函数和训练组件的公共接口。

## Refine 后处理数据流

YOLOv8 检测结果转换为 `[x1, y1, x2, y2, confidence, class_id]` 张量，交给每个视频源独占的 refine 实例。处理结果写回可视化层，但不修改 Ultralytics 核心模型代码。标准入口为：

```powershell
python scripts/run_tracking.py --weights weights/best.pt --source video.mp4 --device 0
```

## YOLO→EfficientNetV2 级联数据流

1. YOLOv8 对输入帧执行目标检测。
2. 仅对配置指定的候选类别裁剪检测框，并按比例扩展后裁剪到图像边界。
3. EfficientNetV2 分类器完成 224×224 中心裁剪、归一化和二分类推理。
4. 分类结果与原检测框关联，最终入口负责标注和视频输出。

分类器对外接口为一个可复用类；构造阶段加载一次模型和标签，`classify(image)` 返回结构化类别、置信度和索引。设备支持 `auto`、CPU 和指定 CUDA 设备。空裁剪不进入分类器。

标准入口为：

```powershell
python scripts/run_cascade.py --detector weights/yolo.pt --classifier weights/efficientnetv2.pth --source video.mp4
```

模型结构、归一化参数、二分类标签含义及原训练检查点兼容要求记录在方法 README 中。迁移只修复封装、导入和路径，不无依据改变网络结构、类别映射或判定语义。

## Flask 多摄像头架构

- 任意数量视频源由 YAML 配置，不写死本地路径或四路摄像头。
- 每路一个采集工作线程；一个共享 GPU 推理工作线程拥有检测器和可选分类器。
- 每路独立 refine 状态；级联分类器可安全共享并只在推理工作线程调用。
- 最新帧缓冲避免生产者被慢客户端阻塞，并允许多个客户端同时查看同一路流。
- 提供 `/`、`/streams`、`/video_feed/<stream_id>` 和 `/health`。
- 配置决定处理模式：`tracking` 或 `cascade`，单个服务进程不在同一路流上隐式混合两种论文方法。
- 断线有限退避重连；关闭时释放视频源并停止线程。
- Flask 模块导入无副作用，入口才负责加载配置、权重和启动服务。

标准调用形式：

```powershell
python scripts/run_flask_multicam.py --config configs/cameras.example.yaml
```

## 已知缺陷修复

- 修复服务将 `InferenceModel.classify_loader` 错当成模块级 `classify_loader` 导入的问题。
- 删除 `D:/...`、`E:/...` 等本地视频、权重和输出路径。
- 消除 `proxy_package/__init__.py` 修改 `sys.path` 及错误顶层导入。
- 模型和标签路径相对方法包或由命令行传入，不依赖当前工作目录。
- 修复未释放 `VideoWriter`、异常后继续使用未赋值结果、张量直接作为切片索引等问题。
- 清理乱码注释、巨型废弃注释块和无效的 `boxes != None` 判断。

## 清理规则

- 先通过静态导入图和测试确定 EfficientNetV2 推理所需的最小传递依赖，再删除 `proxy_package` 未使用部分。
- 删除 `archive/legacy`、个人实验脚本、缓存和可再生成输出。
- 保留许可证和第三方来源说明；从外部项目借用的代码必须明确引用。
- 不修改上游 Ultralytics 核心代码，除非级联或 refine 的兼容性确实要求；所有改动记录在 `docs/YOLOV8_CHANGES.md`。

## 测试与验收

- refine 现有行为测试继续通过。
- 使用伪检测器和伪分类器验证候选类别筛选、边界裁剪、空裁剪和结果关联。
- 使用临时检查点或依赖注入验证分类器只加载一次；无需公开真实权重。
- 验证每路状态隔离、多客户端读取、断线重连和退出释放。
- 三个 CLI 的 `--help` 无需权重即可运行。
- Python 编译检查通过；静态扫描不存在个人绝对路径、真实 RTSP 凭据、缓存和无法解释的个人 Python 文件。
- README 能清楚区分 refine 后处理与 YOLO→EfficientNetV2 级联分类，列出各自入口和运行命令。

## Git 与发布

重构按“方法提取、级联分类、CLI、Flask、文档与清理”分为可审阅提交。验证通过后推送到公开仓库 `Risesharply/dust-detection-yolov8`，保留 `upstream` 远端且不改写公开历史。
