"""Model-independent multi-stream inference coordinator."""

from __future__ import annotations

import threading
from typing import Callable, Mapping

from .buffer import LatestFrameBuffer


class InferenceService:
    """Own input/output buffers and an independent processor for each stream."""

    def __init__(self, sources: Mapping[str, object], processor_factory: Callable[[str], Callable], stop_event: threading.Event):
        self.sources = dict(sources)
        self.stop_event = stop_event
        self.input_buffers = {name: LatestFrameBuffer() for name in self.sources}
        self.output_buffers = {name: LatestFrameBuffer() for name in self.sources}
        self.processors = {name: processor_factory(name) for name in self.sources}

    @property
    def stream_ids(self):
        return tuple(self.sources)

    def process_latest(self, stream_id: str, after_version: int = 0, timeout: float = 0.0) -> int:
        item = self.input_buffers[stream_id].wait_for_frame(after_version, timeout)
        if item is None:
            return after_version
        version, frame = item
        self.output_buffers[stream_id].publish(self.processors[stream_id](frame))
        return version
