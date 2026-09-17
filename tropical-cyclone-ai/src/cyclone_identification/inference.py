"""Run a trained cyclone identifier and write downstream-ready scores."""
import argparse
from pathlib import Path
import torch
from torch.utils.data import DataLoader
from cyclone_identification.dataset import CycloneImageDataset, load_manifest
from cyclone_identification.model import CycloneCNN
from cyclone_identification.transforms import image_transform

def main():
    parser = argparse.ArgumentParser(description="Score satellite images with the cyclone CNN.")
    parser.add_argument("--manifest", required=True, help="CSV with image_path and optional metadata")
    parser.add_argument("--checkpoint", required=True); parser.add_argument("--output", default="data/processed/detections/cyclone_detections.csv")
    parser.add_argument("--threshold", type=float, default=.5); parser.add_argument("--batch-size", type=int, default=32)
    args = parser.parse_args(); frame = load_manifest(args.manifest, require_labels=False)
    checkpoint = torch.load(args.checkpoint, map_location="cpu", weights_only=True)
    model = CycloneCNN(); model.load_state_dict(checkpoint["model_state"]); model.eval()
    loader = DataLoader(CycloneImageDataset(frame, image_transform(checkpoint.get("image_size", 256)), labelled=False), batch_size=args.batch_size)
    scores = []
    with torch.no_grad():
        for images, _ in loader: scores.extend(torch.sigmoid(model(images)).tolist())
    output = frame.copy(); output["cyclone_probability"] = scores; output["cyclone_detected"] = output.cyclone_probability >= args.threshold
    destination = Path(args.output); destination.parent.mkdir(parents=True, exist_ok=True); output.to_csv(destination, index=False)
    print(f"Wrote {len(output)} detection result(s) to {destination}")

if __name__ == "__main__": main()
