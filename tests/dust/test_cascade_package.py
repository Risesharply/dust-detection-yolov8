import numpy as np
import torch


def test_legacy_proxy_package_is_not_part_of_public_api():
    from pathlib import Path

    assert not Path("proxy_package/__init__.py").exists()


def test_cascade_crop_is_expanded_and_clipped():
    from methods.yolo_efficientnetv2.cascade import expand_and_clip_box

    assert expand_and_clip_box((-4, 8, 12, 24), (20, 20), ratio=0.125) == (0, 6, 14, 20)


def test_preprocess_produces_normalized_chw_tensor():
    from methods.yolo_efficientnetv2.pipeline import preprocess_image

    image = np.full((300, 400, 3), 127.5, dtype=np.float32)
    tensor = preprocess_image(image)
    assert tuple(tensor.shape) == (1, 3, 224, 224)
    assert float(tensor.abs().max()) < 1e-6


def test_explicit_model_preserves_checkpoint_parameter_layout():
    from methods.yolo_efficientnetv2.model import EfficientNetV2ClassifierModel

    state = EfficientNetV2ClassifierModel().state_dict()
    assert len(state) == 782
    assert "backbone.layers.0.conv.weight" in state
    assert tuple(state["head.fc.weight"].shape) == (2, 1280)


def test_classifier_returns_structured_prediction(tmp_path):
    from methods.yolo_efficientnetv2.classifier import EfficientNetV2Classifier
    from methods.yolo_efficientnetv2.model import EfficientNetV2ClassifierModel

    checkpoint = tmp_path / "classifier.pth"
    torch.save({"state_dict": EfficientNetV2ClassifierModel().state_dict()}, checkpoint)
    classifier = EfficientNetV2Classifier(checkpoint, labels=("down", "other"), device="cpu")
    result = classifier.classify(np.zeros((224, 224, 3), dtype=np.uint8))
    assert result.label in {"down", "other"}
    assert result.index in {0, 1}
    assert 0.0 <= result.confidence <= 1.0
