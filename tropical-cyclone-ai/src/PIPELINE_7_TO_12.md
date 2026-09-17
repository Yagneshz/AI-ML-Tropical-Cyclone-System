# Steps 7–12: production handoffs

All commands run from the project root after `pip install -r requirements.txt -r requirements-step6.txt` and `$env:PYTHONPATH='src'`.

## 7. Feature extraction

`python -m feature_extraction.pipeline --detections data/processed/detections/cyclone_detections.csv --checkpoint models/cyclone_cnn.pt`

This filters on the detection probability, then writes `image_features.npy` and matching `feature_metadata.csv`.

## 8. Classification

`python -m cyclone_classification.pipeline train --label-column <category_column>`

Omit `--label-column` only if metadata includes `USA_WIND`; categories are then derived from wind thresholds. Score using `python -m cyclone_classification.pipeline predict`.

## 9. Temporal state

`python -m temporal_model.pipeline --data data/processed/fused_dataset/tcir_ibtracs_fused.csv`

The split is by storm (`SID`), so the same cyclone never leaks from train into test. It writes the model plus a row-level prediction CSV.

## 10. Intensity / 11. Track

`python -m intensity_prediction.pipeline train --data data/processed/fused_dataset/tcir_ibtracs_fused.csv`

`python -m track_prediction.pipeline train --data data/processed/fused_dataset/tcir_ibtracs_fused.csv`

Both accept `predict --history "lat,lon,wind,pres;..."`, using exactly the configured lookback rows.

## 12. Evaluation

`python -m model_evaluation.pipeline --data <predictions.csv> --task track --actual actual_LAT_IBTRACS,actual_LON_IBTRACS --predicted predicted_LAT_IBTRACS,predicted_LON_IBTRACS`

The evaluator writes JSON metrics. Track error uses Haversine distance in kilometres.
