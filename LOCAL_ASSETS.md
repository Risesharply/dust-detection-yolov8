# 本地实验资产

本文件记录不上传 GitHub、但仍保留在本机的实验资产。整理过程不会删除这些目录。

| 路径 | 内容 | GitHub 策略 |
| --- | --- | --- |
| `v8_weights/` | YOLOv8 模型权重 | 忽略；在 README 说明自行放置 |
| `v8_train4/`, `v8_train5/` | 训练输出与检查点 | 忽略 |
| `cut_imgs/`, `img_data/` | 裁剪图和本地输入图 | 忽略 |
| `proxy_package/models/**/*.pth` | 分类模型检查点 | 忽略 |
| `refine.zip` | 核心源码的本地备份 | 忽略；以 `refine/` 源码为准 |
| 根目录图片和检测结果图 | 演示输入与运行结果 | 忽略 |
| `errorlog.txt`, `*.log` | 运行日志 | 忽略 |
| `.idea/`, `__pycache__/` | IDE 配置和 Python 缓存 | 忽略 |

推荐的复现资产布局：

```text
data/dust/              # 扬尘数据集（不提交）
v8_weights/best.pt      # 检测权重（不提交）
v8_train5/              # 自动生成输出（不提交）
```

公开发布权重或数据集时，应使用独立的 Release、云盘或数据存储服务，并在 README 中给出校验值和许可证，不应直接写入 Git 历史。
