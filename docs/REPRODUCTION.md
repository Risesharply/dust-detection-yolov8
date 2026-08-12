# YOLOv8 扬尘检测复现

安装项目：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

权重和数据集不随仓库发布。Refine 推理：

```powershell
python scripts/run_tracking.py --weights weights/yolo.pt --source video.mp4 --device 0
```

级联分类：

```powershell
python scripts/run_cascade.py --detector weights/yolo.pt --classifier weights/efficientnetv2.pth --source video.mp4
```

多摄像头服务支持 `tracking` 和 `cascade` 两种逐流模式。复制并修改示例配置后：

```powershell
python scripts/run_flask_multicam.py --config configs/cameras.local.yaml
```

浏览器入口为 `/`，健康检查为 `/health`，流列表为 `/streams`，MJPEG 地址为
`/video_feed/<stream_id>`。服务使用每路采集线程和一个共享推理线程；多个
浏览器客户端读取同一路流时不会互相抢帧。
