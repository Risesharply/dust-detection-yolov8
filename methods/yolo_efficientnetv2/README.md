# YOLO + EfficientNetV2 级联分类

这是与 refine 并列的另一种正式方法，而不是个人测试脚本。YOLOv8 首先检测
候选目标；仅对 `candidate_class_id` 对应的检测框按宽度的 1/8 向四周扩展并
裁剪到图像边界，再交给 EfficientNetV2-S 二分类器。

分类预处理为 224×224 中心裁剪/缩放，使用 `mean=[127.5]*3`、
`std=[127.5]*3` 归一化。类别顺序为 `down=0`、`other=1`。模型保持原检查点
的 `backbone.*`、`neck.*`、`head.fc.*` 参数布局；本地正式检查点共 782 个
参数项，已通过严格加载验证。

```powershell
python scripts/run_cascade.py `
  --detector weights/yolo.pt `
  --classifier weights/efficientnetv2.pth `
  --source path/to/video.mp4
```

权重不随公开仓库发布。原来分散在 `proxy_package`、`classify` 和演示脚本中的
实现已集中到本目录；无关骨干网络、训练头和个人实验已删除。
