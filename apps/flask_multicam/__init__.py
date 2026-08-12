"""Multi-camera streaming service."""

from .app import create_app
from .service import InferenceService

__all__ = ["InferenceService", "create_app"]
