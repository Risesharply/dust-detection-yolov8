import numpy as np


def test_proxy_package_import_has_no_path_side_effect():
    import sys

    before = list(sys.path)
    import proxy_package  # noqa: F401

    assert sys.path == before


def test_cascade_crop_is_expanded_and_clipped():
    from methods.yolo_efficientnetv2.cascade import expand_and_clip_box

    assert expand_and_clip_box((-4, 8, 12, 24), (20, 20), ratio=0.125) == (0, 6, 14, 20)


def test_preprocess_produces_normalized_chw_tensor():
    from methods.yolo_efficientnetv2.pipeline import preprocess_image

    image = np.full((300, 400, 3), 127.5, dtype=np.float32)
    tensor = preprocess_image(image)
    assert tuple(tensor.shape) == (1, 3, 224, 224)
    assert float(tensor.abs().max()) < 1e-6
