"""Run YOLOv8 detections through the EfficientNetV2 binary classifier."""

import argparse
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="YOLOv8 to EfficientNetV2 cascade inference")
    parser.add_argument("--detector", required=True, help="YOLOv8 checkpoint")
    parser.add_argument("--classifier", required=True, help="EfficientNetV2 checkpoint")
    parser.add_argument("--source", required=True)
    parser.add_argument("--device", default="auto")
    parser.add_argument("--output", default="runs/dust/cascade.mp4")
    parser.add_argument("--candidate-class-id", type=int, default=2)
    parser.add_argument("--positive-class-id", type=int, default=0)
    return parser.parse_args()


def main():
    args = parse_args()
    import cv2
    from methods.yolo_efficientnetv2 import EfficientNetV2Classifier, expand_and_clip_box
    from ultralytics import YOLO

    detector = YOLO(args.detector, task="detect")
    classifier = EfficientNetV2Classifier(args.classifier, device=args.device)
    source = int(args.source) if args.source.isdigit() else args.source
    capture = cv2.VideoCapture(source)
    if not capture.isOpened(): raise RuntimeError(f"cannot open source: {args.source}")
    output = Path(args.output); output.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(str(output), cv2.VideoWriter_fourcc(*"mp4v"), capture.get(cv2.CAP_PROP_FPS) or 25.0,
                             (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    try:
        while True:
            ok, frame = capture.read()
            if not ok: break
            result = detector.predict(frame, device=None if args.device == "auto" else args.device, verbose=False)[0]
            rendered = result.plot()
            for box in result.boxes.data:
                if int(box[5].item()) != args.candidate_class_id: continue
                x1, y1, x2, y2 = expand_and_clip_box(box[:4].tolist(), frame.shape)
                if x2 <= x1 or y2 <= y1: continue
                classification = classifier.classify(frame[y1:y2, x1:x2])
                text = f"{classification.label} {classification.confidence:.2f}"
                color = (0, 0, 255) if classification.index == args.positive_class_id else (0, 180, 0)
                cv2.putText(rendered, text, (x1, max(20, y1 - 8)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            writer.write(rendered)
    finally:
        capture.release(); writer.release()


if __name__ == "__main__":
    main()
