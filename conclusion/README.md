# AI/ML Tropical Cyclone Identification, Classification and Prediction System

An end-to-end local research platform for identifying tropical cyclones in satellite imagery, classifying their category, forecasting intensity and track, evaluating models, and visualizing outputs in Streamlit.

> **Safety notice:** This project is for research and education. It does not replace warnings issued by official meteorological agencies.

## Workflow

| Step | Module | Output |
|---:|---|---|
| 1–5 | Data collection, cleaning, preprocessing, fusion | Fused TCIR–IBTrACS data |
| 6 | Cyclone identification | Detection probability and flag |
| 7 | Feature extraction | 256-dimensional CNN features |
| 8 | Cyclone classification | Category and confidence |
| 9 | Temporal model | Next-state predictions |
| 10 | Intensity prediction | Wind speed and central pressure |
| 11 | Track prediction | Next latitude and longitude |
| 12 | Model evaluation | Classification, regression, track metrics |
| 13 | Prediction engine | Local FastAPI forecasts and alerts |
| 14 | Dashboard | Streamlit monitoring and control view |

## Project structure

```text
D:\SIH
├── tropical-cyclone-ai/          # Data pipeline and ML modules
│   ├── data/processed/fused_dataset/
│   ├── src/cyclone_identification/   # Step 6
│   ├── src/feature_extraction/        # Step 7
│   ├── src/cyclone_classification/    # Step 8
│   ├── src/temporal_model/             # Step 9
│   ├── src/intensity_prediction/      # Step 10
│   ├── src/track_prediction/          # Step 11
│   ├── src/model_evaluation/          # Step 12
│   └── src/prediction_engine/         # Step 13
├── Dashboard/                    # Streamlit dashboard
└── conclusion/                   # Project documentation
```

## Setup

```powershell
cd D:\SIH\tropical-cyclone-ai
python -m pip install -r requirements.txt -r requirements-step6.txt -r requirements-step13.txt
$env:PYTHONPATH = 'src'
```

## Run workflow

Steps 1–5 have generated:

`data/processed/fused_dataset/tcir_ibtracs_fused.csv`

For Steps 6–8, put labelled images in `data/processed/images/cyclone/` and `data/processed/images/no_cyclone/`.

```powershell
python -c "from cyclone_identification.dataset import build_manifest; build_manifest('data/processed/images/cyclone', 'data/processed/images/no_cyclone', 'data/processed/detections/train_manifest.csv')"
python -m cyclone_identification.training.train --manifest data/processed/detections/train_manifest.csv
python -m cyclone_identification.inference --manifest data/processed/detections/train_manifest.csv --checkpoint models/cyclone_cnn.pt
python -m feature_extraction.pipeline --detections data/processed/detections/cyclone_detections.csv --checkpoint models/cyclone_cnn.pt
python -m cyclone_classification.pipeline train --label-column <category_column>
python -m cyclone_classification.pipeline predict
python -m temporal_model.pipeline --data data/processed/fused_dataset/tcir_ibtracs_fused.csv
python -m intensity_prediction.pipeline train --data data/processed/fused_dataset/tcir_ibtracs_fused.csv
python -m track_prediction.pipeline train --data data/processed/fused_dataset/tcir_ibtracs_fused.csv
```

Evaluate a result file:

```powershell
python -m model_evaluation.pipeline --data <predictions.csv> --task track --actual actual_LAT_IBTRACS,actual_LON_IBTRACS --predicted predicted_LAT_IBTRACS,predicted_LON_IBTRACS
```

## Start prediction engine and dashboard

```powershell
# Terminal 1
cd D:\SIH\tropical-cyclone-ai
$env:PYTHONPATH = 'src'
uvicorn prediction_engine.app:app --reload

# Terminal 2
cd D:\SIH\Dashboard
streamlit run dashboard/app.py
```

Visit `http://localhost:8501` and use **Pipeline Control Center**. It reads pipeline artifacts locally and sends forecasts to Step 13 at `http://127.0.0.1:8000`.

## Current state

The fused dataset contains 21,076 rows. Satellite images and trained checkpoints are not included, so image-dependent steps and live prediction become available after the required images are added and models are trained.

## Detailed documentation

- `tropical-cyclone-ai/src/cyclone_identification/README.md` — Step 6
- `tropical-cyclone-ai/src/PIPELINE_7_TO_12.md` — Steps 7–12
- `tropical-cyclone-ai/src/prediction_engine/README.md` — Step 13
- `Dashboard/README_PIPELINE_CONNECTION.md` — dashboard connection
