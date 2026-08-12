"""Start the configurable YOLOv8 multi-camera Flask service."""

import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="YOLOv8 Flask multi-camera service")
    parser.add_argument("--config", required=True, help="camera service YAML")
    return parser.parse_args()


def main():
    args = parse_args()
    import logging
    import threading
    from apps.flask_multicam import create_app
    from apps.flask_multicam.config import load_config
    from apps.flask_multicam.processors import YoloV8CascadeProcessor, YoloV8TrackingProcessor
    from apps.flask_multicam.service import InferenceService
    from methods.yolo_efficientnetv2 import EfficientNetV2Classifier
    from ultralytics import YOLO

    config = load_config(args.config)
    if not config["detector"]:
        raise ValueError("config must define detector")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    detector = YOLO(config["detector"], task="detect")
    needs_classifier = any(item["mode"] == "cascade" for item in config["streams"].values())
    classifier = EfficientNetV2Classifier(config["classifier"], device=config["device"]) if needs_classifier else None

    def processor_factory(name):
        mode = config["streams"][name]["mode"]
        if mode == "tracking": return YoloV8TrackingProcessor(detector, config["device"])
        return YoloV8CascadeProcessor(detector, classifier, config["device"])

    sources = {name: item["source"] for name, item in config["streams"].items()}
    service = InferenceService(sources, processor_factory, threading.Event())
    service.start()
    try:
        create_app(service).run(host=config["host"], port=config["port"], threaded=True, use_reloader=False)
    finally:
        service.stop()


if __name__ == "__main__":
    main()
