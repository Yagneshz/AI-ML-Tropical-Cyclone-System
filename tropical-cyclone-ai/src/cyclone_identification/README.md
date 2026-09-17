# Step 6 — Cyclone identification

The CNN identifies whether a preprocessed satellite image contains a tropical cyclone. The fused table has track observations but no image-path column, and `data/processed/images` currently has no image assets, so this stage uses an explicit image manifest.

Place labelled crops in `data/processed/images/cyclone/` and `data/processed/images/no_cyclone/`, then run from the project root:

```powershell
$env:PYTHONPATH = "src"
python -c "from cyclone_identification.dataset import build_manifest; build_manifest('data/processed/images/cyclone', 'data/processed/images/no_cyclone', 'data/processed/detections/train_manifest.csv')"
python -m cyclone_identification.training.train --manifest data/processed/detections/train_manifest.csv
python -m cyclone_identification.inference --manifest data/processed/detections/train_manifest.csv --checkpoint models/cyclone_cnn.pt
```

Inference writes `data/processed/detections/cyclone_detections.csv` with `cyclone_probability` and `cyclone_detected`; keep detected rows for step 7. Extra manifest metadata columns are preserved for downstream joins.
