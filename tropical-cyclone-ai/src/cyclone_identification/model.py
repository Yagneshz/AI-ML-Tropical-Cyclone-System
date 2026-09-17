"""A compact CNN baseline for image-level cyclone identification."""
import torch.nn as nn

class CycloneCNN(nn.Module):
    """Binary classifier producing one logit per satellite image."""
    def __init__(self) -> None:
        super().__init__()
        self.features = nn.Sequential(self._block(3, 32), self._block(32, 64), self._block(64, 128), self._block(128, 256))
        self.classifier = nn.Sequential(nn.AdaptiveAvgPool2d(1), nn.Flatten(), nn.Dropout(0.35), nn.Linear(256, 1))
    @staticmethod
    def _block(in_channels: int, out_channels: int) -> nn.Sequential: return nn.Sequential(nn.Conv2d(in_channels, out_channels, 3, padding=1), nn.BatchNorm2d(out_channels), nn.ReLU(inplace=True), nn.MaxPool2d(2))
    def forward(self, x): return self.classifier(self.features(x)).squeeze(1)
