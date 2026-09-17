"""Dataset and manifest utilities for binary cyclone identification."""

from __future__ import annotations
from pathlib import Path
from typing import Callable
import pandas as pd
from PIL import Image
from torch.utils.data import Dataset

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}
REQUIRED_COLUMNS = {"image_path", "label"}

def build_manifest(positive_dir: str | Path, negative_dir: str | Path, output_csv: str | Path) -> pd.DataFrame:
    """Create a labelled manifest from folders of cyclone and non-cyclone images."""
    rows = []
    for directory, label in ((Path(positive_dir), 1), (Path(negative_dir), 0)):
        if not directory.is_dir(): raise FileNotFoundError(f"Image directory not found: {directory}")
        rows.extend({"image_path": str(path.resolve()), "label": label} for path in sorted(directory.rglob("*")) if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS)
    manifest = pd.DataFrame(rows)
    if manifest.empty or manifest["label"].nunique() != 2: raise ValueError("Both positive and negative image folders must contain at least one image.")
    output = Path(output_csv); output.parent.mkdir(parents=True, exist_ok=True); manifest.to_csv(output, index=False)
    return manifest

def load_manifest(manifest_csv: str | Path, require_labels: bool = True) -> pd.DataFrame:
    manifest = pd.read_csv(manifest_csv)
    missing = (REQUIRED_COLUMNS if require_labels else {"image_path"}) - set(manifest.columns)
    if missing: raise ValueError(f"Manifest is missing columns: {sorted(missing)}")
    unavailable = [p for p in manifest["image_path"] if not Path(p).is_file()]
    if unavailable: raise FileNotFoundError(f"Manifest references {len(unavailable)} unavailable image(s); first: {unavailable[0]}")
    return manifest.reset_index(drop=True)

class CycloneImageDataset(Dataset):
    def __init__(self, manifest: pd.DataFrame, transform: Callable, labelled: bool = True): self.manifest, self.transform, self.labelled = manifest.reset_index(drop=True), transform, labelled
    def __len__(self) -> int: return len(self.manifest)
    def __getitem__(self, index: int):
        row = self.manifest.iloc[index]
        with Image.open(row.image_path) as image: tensor = self.transform(image.convert("RGB"))
        return (tensor, int(row.label)) if self.labelled else (tensor, str(row.image_path))
