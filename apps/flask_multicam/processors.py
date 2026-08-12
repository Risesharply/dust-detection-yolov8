"""YOLOv8 tracking and cascade frame processors."""

import cv2

from methods.refine_tracking import RefinePostprocessor
from methods.yolo_efficientnetv2 import expand_and_clip_box


class YoloV8TrackingProcessor:
    def __init__(self, detector, device="auto", class_id=0):
        self.detector, self.device, self.class_id = detector, device, class_id
        self.postprocessor = RefinePostprocessor()

    def __call__(self, frame):
        result = self.detector.predict(frame, device=None if self.device == "auto" else self.device, verbose=False)[0]
        result.boxes.data = self.postprocessor.refine_box(result.boxes.data, self.class_id)
        return result.plot()


class YoloV8CascadeProcessor:
    def __init__(self, detector, classifier, device="auto", candidate_class_id=2, positive_class_id=0):
        self.detector, self.classifier, self.device = detector, classifier, device
        self.candidate_class_id, self.positive_class_id = candidate_class_id, positive_class_id

    def __call__(self, frame):
        result = self.detector.predict(frame, device=None if self.device == "auto" else self.device, verbose=False)[0]
        rendered = result.plot()
        for box in result.boxes.data:
            if int(box[5].item()) != self.candidate_class_id: continue
            x1, y1, x2, y2 = expand_and_clip_box(box[:4].tolist(), frame.shape)
            if x2 <= x1 or y2 <= y1: continue
            classification = self.classifier.classify(frame[y1:y2, x1:x2])
            color = (0, 0, 255) if classification.index == self.positive_class_id else (0, 180, 0)
            cv2.putText(rendered, f"{classification.label} {classification.confidence:.2f}",
                        (x1, max(20, y1 - 8)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        return rendered
