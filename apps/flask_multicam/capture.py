"""Reconnectable OpenCV capture worker."""

import logging
import threading

import cv2

LOGGER = logging.getLogger(__name__)


class CaptureWorker(threading.Thread):
    def __init__(self, stream_id, source, buffer, stop_event, reconnect_delay=1.0):
        super().__init__(name=f"capture-{stream_id}", daemon=True)
        self.stream_id, self.source, self.buffer = stream_id, source, buffer
        self.stop_event, self.reconnect_delay = stop_event, reconnect_delay

    def run(self):
        capture = None
        try:
            while not self.stop_event.is_set():
                capture = cv2.VideoCapture(self.source)
                while capture.isOpened() and not self.stop_event.is_set():
                    ok, frame = capture.read()
                    if not ok: break
                    self.buffer.publish(frame)
                capture.release(); capture = None
                if not self.stop_event.is_set():
                    LOGGER.warning("stream %s disconnected; retrying", self.stream_id)
                    self.stop_event.wait(self.reconnect_delay)
        finally:
            if capture is not None: capture.release()
