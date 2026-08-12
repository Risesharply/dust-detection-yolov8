"""YAML configuration loader for the multi-camera service."""

from pathlib import Path

import yaml


def load_config(path):
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    streams = data.get("streams")
    if not isinstance(streams, list) or not streams:
        raise ValueError("config must contain a non-empty streams list")
    result = {}
    for item in streams:
        stream_id, source = item.get("id"), item.get("source")
        mode = item.get("mode", "tracking")
        if mode not in {"tracking", "cascade"}:
            raise ValueError("stream mode must be tracking or cascade")
        if not stream_id or source is None or stream_id in result:
            raise ValueError("each stream needs a unique id and a source")
        result[str(stream_id)] = {"source": source, "mode": mode}
    return {"detector": data.get("detector"), "classifier": data.get("classifier"), "device": data.get("device", "auto"),
            "host": data.get("host", "0.0.0.0"), "port": int(data.get("port", 5000)), "streams": result}
