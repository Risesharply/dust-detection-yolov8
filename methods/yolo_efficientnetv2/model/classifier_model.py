"""Explicit composition of the binary EfficientNetV2-S classifier."""

import torch
import torch.nn as nn

from .legacy.backbones.efficientnet_v2 import EfficientNetV2


class GlobalAveragePooling(nn.Module):
    def __init__(self):
        super().__init__()
        self.gap = nn.AdaptiveAvgPool2d((1, 1))

    def forward(self, inputs):
        if isinstance(inputs, tuple):
            inputs = inputs[-1]
        return self.gap(inputs).view(inputs.size(0), -1)


class LinearClassificationHead(nn.Module):
    def __init__(self, in_channels: int = 1280, num_classes: int = 2):
        super().__init__()
        self.fc = nn.Linear(in_channels, num_classes)

    def forward(self, inputs):
        if isinstance(inputs, tuple):
            inputs = inputs[-1]
        return self.fc(inputs)


class EfficientNetV2ClassifierModel(nn.Module):
    """Binary classifier retaining the legacy backbone/neck/head key names."""

    def __init__(self):
        super().__init__()
        self.backbone = EfficientNetV2(arch="s")
        self.neck = GlobalAveragePooling()
        self.head = LinearClassificationHead()

    def forward(self, image: torch.Tensor) -> torch.Tensor:
        return self.head(self.neck(self.backbone(image)))
