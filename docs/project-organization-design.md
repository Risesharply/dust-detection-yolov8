# 扬尘检测 YOLOv8 仓库整理设计

日期：2026-08-12

## 目标

将当前 Ultralytics YOLOv8 工程整理为独立、精简、可复现的 GitHub 仓库 `dust-detection-yolov8`，用于论文第四章中与 YOLOv5 的对照实验。仓库突出 `refine/` 中的多目标跟踪扬尘检测核心，同时保留 YOLOv8 适配差异。

## 范围

保留并发布：

- 实验所基于的 Ultralytics YOLOv8 基础源码及其上游历史、许可证和依赖说明。
- 论文实验实际使用的模型配置、训练入口和推理入口。
- `refine/` 核心源码及 YOLOv8 适配参数。
- 能说明使用方式的必要示例、配置和文档。

本地保留但不发布：

- 数据集、模型权重、训练输出、推理结果和裁剪图片。
- 临时图片、视频、日志、压缩包、缓存和 IDE 配置。
- 无法确认用途的实验文件；这些文件在完成归类前不删除。

## 目标结构

```text
dust-detection-yolov8/
├── configs/             # 论文实验配置
├── data/                # 数据目录说明，不提交数据集
├── docs/                # 算法、复现和来源说明
├── examples/            # 精简后的推理与演示入口
├── refine/              # 跟踪、匹配和时序筛选核心
├── tests/               # 上游测试及核心模块最小测试
├── ultralytics/         # YOLOv8 上游包和论文模型适配
├── README.md
├── NOTICE.md
├── LICENSE
└── requirements.txt
```

现有脚本仅在确认导入关系后移动。上游目录结构保持稳定，避免破坏 Ultralytics 包导入；目标结构主要约束个人实验代码和生成物。

## `refine` 边界

`refine/` 是论文第四章的核心实现，包含 IoU/GIoU 匹配、轨迹状态维护、时序判定和检测框筛选。它与 YOLOv5 仓库共享算法思想，但保留本仓库实际使用的默认参数、输入格式和集成接口，不用另一个版本覆盖。

整理期间只进行以下安全改动：

- 修复包内导入和文件命名，使接口含义清晰。
- 补充来源、输入输出和参数说明。
- 添加不依赖数据集或权重的最小测试。
- 不改变已经用于论文实验的算法阈值，除非单独记录并验证。

## 上游与第三方引用

- 保留 Ultralytics 上游 Git 历史、README 归属和当前许可证；仓库说明其为研究修改版。
- README、NOTICE 和基于其实现的相关源码明确引用 `bochinski/iou-tracker`：https://github.com/bochinski/iou-tracker 。
- 保留 iou-tracker 的 MIT 版权声明：Copyright (c) 2017 TU Berlin, Communication Systems Group。
- 说明本项目对相关跟踪逻辑所作的修改；不复制 iou-tracker 仓库或伪装为原创。

## Git 与发布

当前目录是 Ultralytics 官方仓库的本地检出，且存在大量个人的已暂存和未暂存文件。实施时保留上游历史，为个人整理建立独立提交，并把远端改为新仓库；不向 `ultralytics/ultralytics` 推送。通过 GitHub Desktop 创建并发布 `dust-detection-yolov8`。

实施过程中必须显式暂存本次整理文件，不使用会混入不相关改动的全量暂存操作，直至现有个人文件全部完成分类审查。

## 验证标准

- Git 待提交清单中不存在权重、数据集、训练输出、缓存或隐私文件。
- 所有本项目新增或修改的 Python 文件通过语法编译检查。
- `refine` 的 IoU/GIoU、轨迹更新和筛选接口具有最小测试。
- README 中的安装、目录和最小运行命令与实际文件一致。
- LICENSE、NOTICE 和源码引用完整。
- GitHub 仓库能由新目录克隆，并按 README 完成最小导入测试。

## 回退策略

保留原 Ultralytics 上游提交和个人工作区内容；整理优先采用 Git 可追踪移动、复制和忽略规则，不删除实验资产。发布前记录文件分类清单，任何不确定文件留在本地且不纳入提交。
