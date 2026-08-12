"""Flask application factory for multi-camera MJPEG streaming."""

from __future__ import annotations

import cv2
from flask import Flask, Response, abort, jsonify, render_template


def _mjpeg_frames(buffer):
    version = 0
    while True:
        item = buffer.wait_for_frame(version, timeout=5.0)
        if item is None:
            continue
        version, frame = item
        ok, encoded = cv2.imencode(".jpg", frame)
        if ok:
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + encoded.tobytes() + b"\r\n"


def create_app(service) -> Flask:
    app = Flask(__name__)

    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html", stream_ids=service.stream_ids)

    @app.route("/streams", methods=["GET"])
    def streams():
        return jsonify(streams=list(service.stream_ids))

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify(status="ok", streams=len(service.stream_ids))

    @app.route("/video_feed/<stream_id>", methods=["GET"])
    def video_feed(stream_id):
        if stream_id not in service.stream_ids:
            abort(404)
        return Response(_mjpeg_frames(service.output_buffers[stream_id]), mimetype="multipart/x-mixed-replace; boundary=frame")

    return app
