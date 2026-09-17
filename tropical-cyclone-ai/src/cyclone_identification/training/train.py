"""Train and validate the step-6 binary cyclone CNN."""
import argparse
from pathlib import Path
import torch
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, roc_auc_score
from sklearn.model_selection import train_test_split
from torch import nn
from torch.utils.data import DataLoader
from cyclone_identification.dataset import CycloneImageDataset, load_manifest
from cyclone_identification.model import CycloneCNN
from cyclone_identification.transforms import image_transform

def evaluate(model, loader, device):
    model.eval(); labels, predictions, scores = [], [], []
    with torch.no_grad():
        for images, target in loader:
            probability = torch.sigmoid(model(images.to(device))).cpu()
            labels.extend(target.tolist()); scores.extend(probability.tolist()); predictions.extend((probability >= .5).int().tolist())
    precision, recall, f1, _ = precision_recall_fscore_support(labels, predictions, average="binary", zero_division=0)
    return {"accuracy": accuracy_score(labels, predictions), "precision": precision, "recall": recall, "f1": f1, "roc_auc": roc_auc_score(labels, scores) if len(set(labels)) == 2 else None}

def main():
    parser = argparse.ArgumentParser(description="Train CNN cyclone identifier from image_path,label manifest.")
    parser.add_argument("--manifest", required=True); parser.add_argument("--output", default="models/cyclone_cnn.pt")
    parser.add_argument("--epochs", type=int, default=15); parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--image-size", type=int, default=256); parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args(); torch.manual_seed(args.seed)
    manifest = load_manifest(args.manifest)
    train_frame, validation_frame = train_test_split(manifest, test_size=.2, random_state=args.seed, stratify=manifest.label)
    transform = image_transform(args.image_size)
    train_loader = DataLoader(CycloneImageDataset(train_frame, transform), batch_size=args.batch_size, shuffle=True)
    valid_loader = DataLoader(CycloneImageDataset(validation_frame, transform), batch_size=args.batch_size)
    device = "cuda" if torch.cuda.is_available() else "cpu"; model = CycloneCNN().to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4); criterion = nn.BCEWithLogitsLoss()
    best_f1 = -1.0; output = Path(args.output); output.parent.mkdir(parents=True, exist_ok=True)
    for epoch in range(1, args.epochs + 1):
        model.train()
        for images, labels in train_loader:
            optimizer.zero_grad(); loss = criterion(model(images.to(device)), labels.float().to(device)); loss.backward(); optimizer.step()
        metrics = evaluate(model, valid_loader, device)
        print(f"epoch={epoch} " + " ".join(f"{key}={value:.4f}" for key, value in metrics.items() if value is not None))
        if metrics["f1"] > best_f1:
            best_f1 = metrics["f1"]
            torch.save({"model_state": model.state_dict(), "image_size": args.image_size, "metrics": metrics}, output)
    print(f"Saved best model to {output}")

if __name__ == "__main__": main()
