"""Thread-safe latest-frame storage for live video."""

from __future__ import annotations

import threading
from typing import Optional, Tuple

import numpy as np


class LatestFrameBuffer:
    """Store one frame while allowing any number of non-consuming readers."""

    def __init__(self) -> None:
        self._condition = threading.Condition()
        self._frame: Optional[np.ndarray] = None
        self._version = 0

    def publish(self, frame: np.ndarray) -> int:
        with self._condition:
            self._frame = frame
            self._version += 1
            self._condition.notify_all()
            return self._version

    def wait_for_frame(self, after_version: int, timeout: float = 1.0) -> Optional[Tuple[int, np.ndarray]]:
        with self._condition:
            if self._version <= after_version:
                self._condition.wait_for(lambda: self._version > after_version, timeout)
            if self._frame is None or self._version <= after_version:
                return None
            return self._version, self._frame.copy()
