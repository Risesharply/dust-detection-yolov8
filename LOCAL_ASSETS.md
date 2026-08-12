# 本地实验资产

以下文件不提交 GitHub：

- `weights/`、`v8_weights/`、`*.pt`：YOLOv8 检测权重。
- `*.pth`：EfficientNetV2 分类检查点。
- `v8_train*/`、`runs/`：训练输出。
- `cut_imgs/`、`img_data/`：本地裁剪和数据集。
- `configs/*.local.yaml`：包含真实摄像头地址的本地配置。

建议使用 `weights/yolo.pt` 和 `weights/efficientnetv2.pth` 作为复现路径。
私有检查点不得直接写入 Git 历史。
