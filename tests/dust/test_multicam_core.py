import threading

import numpy as np


def test_latest_frame_is_shared_not_consumed():
    from apps.flask_multicam.buffer import LatestFrameBuffer

    buffer = LatestFrameBuffer()
    buffer.publish(np.zeros((2, 2, 3), dtype=np.uint8))
    first = buffer.wait_for_frame(0, timeout=0.01)
    second = buffer.wait_for_frame(0, timeout=0.01)
    assert first is not None and second is not None
    assert first[0] == second[0] == 1


def test_service_keeps_processor_state_per_stream():
    from apps.flask_multicam.service import InferenceService

    created = []

    def factory(_stream):
        state = object()
        created.append(state)
        return lambda frame: frame

    service = InferenceService({"a": 0, "b": 1}, factory, threading.Event())
    assert len(created) == 2
    assert service.stream_ids == ("a", "b")


def test_app_lists_streams_and_reports_health():
    from apps.flask_multicam.app import create_app

    class Service:
        stream_ids = ("north", "south")
        output_buffers = {}

    client = create_app(Service()).test_client()
    assert client.get("/streams").get_json() == {"streams": ["north", "south"]}
    assert client.get("/health").get_json()["status"] == "ok"
    assert client.get("/video_feed/missing").status_code == 404
