"""Model-independent multi-stream inference coordinator."""

from __future__ import annotations

import threading
from typing import Callable, Mapping

from .buffer import LatestFrameBuffer
from .capture import CaptureWorker


class InferenceService:
    """Own input/output buffers and an independent processor for each stream."""

    def __init__(self, sources: Mapping[str, object], processor_factory: Callable[[str], Callable], stop_event: threading.Event):
        self.sources = dict(sources)
        self.stop_event = stop_event
        self.input_buffers = {name: LatestFrameBuffer() for name in self.sources}
        self.output_buffers = {name: LatestFrameBuffer() for name in self.sources}
        self.processors = {name: processor_factory(name) for name in self.sources}
        self._versions = {name: 0 for name in self.sources}
        self._capture_workers = []
        self._inference_worker = None

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

    def _run_inference(self):
        while not self.stop_event.is_set():
            processed = False
            for stream_id in self.stream_ids:
                version = self.process_latest(stream_id, self._versions[stream_id], 0.0)
                processed |= version != self._versions[stream_id]
                self._versions[stream_id] = version
            if not processed: self.stop_event.wait(0.01)

    def start(self):
        self._capture_workers = [CaptureWorker(name, source, self.input_buffers[name], self.stop_event)
                                 for name, source in self.sources.items()]
        for worker in self._capture_workers: worker.start()
        self._inference_worker = threading.Thread(target=self._run_inference, name="inference", daemon=True)
        self._inference_worker.start()

    def stop(self):
        self.stop_event.set()
        for worker in self._capture_workers: worker.join(timeout=3)
        if self._inference_worker is not None: self._inference_worker.join(timeout=3)
