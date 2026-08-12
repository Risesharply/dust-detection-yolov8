"""Public inference API for the EfficientNetV2 cascade stage."""

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence, Union

import numpy as np
import torch

from .model import EfficientNetV2ClassifierModel
from .pipeline import preprocess_image


@dataclass(frozen=True)
class Classification:
    label: str
    confidence: float
    index: int


def _resolve_device(device: Union[str, torch.device]) -> torch.device:
    if str(device) == "auto":
        return torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    resolved = torch.device(device)
    if resolved.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested but is not available")
    return resolved


class EfficientNetV2Classifier:
    """Load the binary classifier once and classify detector crops."""

    def __init__(
        self,
        checkpoint: Union[str, Path],
        labels: Sequence[str] = ("down", "other"),
        device: Union[str, torch.device] = "auto",
    ) -> None:
        if len(labels) != 2:
            raise ValueError("the published classifier requires exactly two labels")
        self.labels = tuple(labels)
        self.device = _resolve_device(device)
        self.model = EfficientNetV2ClassifierModel()
        payload = torch.load(str(checkpoint), map_location="cpu")
        if isinstance(payload, dict):
            state = payload.get("state_dict", payload.get("model", payload))
        else:
            state = payload
        self.model.load_state_dict(state, strict=True)
        self.model.to(self.device).eval()

    def classify(self, image: np.ndarray) -> Classification:
        tensor = preprocess_image(image).to(self.device)
        with torch.inference_mode():
            probabilities = torch.softmax(self.model(tensor), dim=1)[0]
        index = int(probabilities.argmax().item())
        return Classification(self.labels[index], float(probabilities[index].item()), index)
