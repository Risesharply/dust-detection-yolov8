"""Geometry helpers for detector-to-classifier crops."""

from typing import Sequence, Tuple


def expand_and_clip_box(box: Sequence[float], image_shape: Sequence[int], ratio: float = 0.125) -> Tuple[int, int, int, int]:
    """Expand a detection by a fraction of its width and clip to image bounds."""
    x1, y1, x2, y2 = (float(value) for value in box)
    height, width = int(image_shape[0]), int(image_shape[1])
    padding = int((x2 - x1) * ratio)
    return (
        max(0, int(x1) - padding),
        max(0, int(y1) - padding),
        min(width, int(x2) + padding),
        min(height, int(y2) + padding),
    )
