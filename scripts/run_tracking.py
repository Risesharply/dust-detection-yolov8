"""Run YOLOv8 inference followed by refine post-processing."""

import argparse
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="YOLOv8 dust detection with refine post-processing")
    parser.add_argument("--weights", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--device", default="auto")
    parser.add_argument("--output", default="runs/dust/tracking.mp4")
    parser.add_argument("--confidence", type=float, default=0.25)
    parser.add_argument("--iou", type=float, default=0.7)
    parser.add_argument("--class-id", type=int, default=0)
    return parser.parse_args()


def main():
    args = parse_args()
    import cv2
    from methods.refine_tracking import RefinePostprocessor
    from ultralytics import YOLO

    model = YOLO(args.weights, task="detect")
    postprocessor = RefinePostprocessor()
    source = int(args.source) if args.source.isdigit() else args.source
    capture = cv2.VideoCapture(source)
    if not capture.isOpened():
        raise RuntimeError(f"cannot open source: {args.source}")
    output = Path(args.output); output.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(str(output), cv2.VideoWriter_fourcc(*"mp4v"), capture.get(cv2.CAP_PROP_FPS) or 25.0,
                             (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    try:
        while True:
            ok, frame = capture.read()
            if not ok: break
            result = model.predict(frame, conf=args.confidence, iou=args.iou,
                                   device=None if args.device == "auto" else args.device, verbose=False)[0]
            result.boxes.data = postprocessor.refine_box(result.boxes.data, args.class_id)
            writer.write(result.plot())
    finally:
        capture.release(); writer.release()


if __name__ == "__main__":
    main()
