"""Dependency-light image transforms shared by training and inference."""
import numpy as np
import torch
from PIL import Image
MEAN, STD = (0.485, 0.456, 0.406), (0.229, 0.224, 0.225)

def image_transform(image_size: int = 256):
    def transform(image: Image.Image) -> torch.Tensor:
        image = image.resize((image_size, image_size), Image.Resampling.BILINEAR)
        array = np.asarray(image, dtype=np.float32) / 255.0
        return torch.from_numpy(((array - np.asarray(MEAN)) / np.asarray(STD)).transpose(2, 0, 1)).float()
    return transform
