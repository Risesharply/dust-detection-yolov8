"""Image preprocessing compatible with the original classifier config."""

import cv2
import numpy as np
import torch


def preprocess_image(image: np.ndarray, size: int = 224) -> torch.Tensor:
    """Center-crop, resize and normalize a BGR image to NCHW float tensor."""
    if image is None or image.size == 0:
        raise ValueError("classification crop is empty")
    height, width = image.shape[:2]
    edge = min(height, width)
    top = (height - edge) // 2
    left = (width - edge) // 2
    cropped = image[top : top + edge, left : left + edge]
    resized = cv2.resize(cropped, (size, size), interpolation=cv2.INTER_CUBIC)
    normalized = (resized.astype(np.float32) - 127.5) / 127.5
    return torch.from_numpy(normalized.transpose(2, 0, 1)).unsqueeze(0)
