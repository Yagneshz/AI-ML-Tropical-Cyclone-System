# Technical Project README — Data, Resources, and Technology Stack

## What was built

This repository implements a local AI/ML workflow for tropical cyclones. It takes cleaned and fused cyclone records, supports satellite-image cyclone identification, extracts image features, classifies cyclone category, forecasts intensity and position, evaluates results, and exposes outputs through a local API and dashboard.

## Data handling

### Source data used

| Source | Purpose | Project use |
|---|---|---|
| TCIR satellite metadata | Satellite observation time, location, wind, pressure | Cleaned satellite input and image association |
| IBTrACS | Historical cyclone track, wind, pressure, identifiers | Track alignment, labels, temporal forecasting |
| Fused TCIR–IBTrACS data | Time-aligned combined observations | Main tabular input for Steps 9–12 |
| Satellite image crops | Cyclone / non-cyclone visual examples | Required to train Steps 6–8 |

### Data transformations

1. Raw satellite and track records are cleaned and quality checked.
2. Timestamps and locations are aligned during data fusion.
3. The fused dataset combines TCIR fields with matched IBTrACS fields.
4. Image records are supplied through a CSV manifest containing `image_path` and `label`.
5. The detection model writes probability and Boolean detection columns.
6. Positive detections are converted into 256-dimensional CNN features.
7. Features and metadata are used for category classification.
8. Per-storm time sequences are built from latitude, longitude, wind, and pressure.
9. Forecast models write next-step predictions and evaluation-ready actual values.

### Important data artifacts

```text
tropical-cyclone-ai/data/
├── interim/
│   ├── cleaned_satellite/tcir_metadata_cleaned.csv
│   └── cleaned_tracks/
├── processed/
│   ├── fused_dataset/tcir_ibtracs_fused.csv
│   ├── images/                       # Add labelled satellite images here
│   ├── detections/                   # Step 6 outputs
│   ├── features/                     # Step 7 outputs
│   ├── classification/               # Step 8 outputs
│   └── evaluation/                   # Step 12 metrics
└── models/                           # Generated model checkpoints
```

The available fused dataset contains 21,076 records. Image assets are not stored in the repository, so image-driven modules need a supplied labelled image dataset before they can train.

## Code structure

```text
D:\SIH
├── tropical-cyclone-ai/
│   ├── notebooks/                    # Exploratory work for Steps 1–5
│   ├── data/                         # Inputs and generated artifacts
│   ├── src/
│   │   ├── data_cleaning/             # Step 3
│   │   ├── preprocessing/             # Step 4
│   │   ├── data_fusion/               # Step 5
│   │   ├── cyclone_identification/    # Step 6 CNN detector
│   │   ├── feature_extraction/        # Step 7 feature vectors
│   │   ├── cyclone_classification/    # Step 8 MLP classifier
│   │   ├── cyclone_forecasting/       # Shared sequence/LSTM utilities
│   │   ├── temporal_model/            # Step 9 temporal model
│   │   ├── intensity_prediction/      # Step 10 wind and pressure model
│   │   ├── track_prediction/          # Step 11 coordinate model
│   │   ├── model_evaluation/          # Step 12 metrics
│   │   └── prediction_engine/         # Step 13 FastAPI service
│   ├── requirements.txt
│   ├── requirements-step6.txt
│   └── requirements-step13.txt
├── Dashboard/
│   └── dashboard/
│       ├── app.py                     # Streamlit application
│       ├── pages/                     # Detection, class, intensity, track views
│       └── data/pipeline.py           # Reads ML artifacts and calls Step 13
└── conclusion/                        # Final project documentation
```

## Models and outputs

| Step | Model / method | Input | Output |
|---:|---|---|---|
| 6 | PyTorch CNN | Satellite image | Cyclone probability, detection flag |
| 7 | CNN feature pooling | Positive detection image | 256-value feature vector |
| 8 | Scikit-learn MLP | CNN features | Category, confidence |
| 9 | PyTorch LSTM | Historical storm state | Next state |
| 10 | PyTorch LSTM | Lat/lon/wind/pressure history | Wind and pressure |
| 11 | PyTorch LSTM | Lat/lon/wind/pressure history | Latitude and longitude |
| 12 | Scikit-learn + Haversine | Actual and predicted results | Accuracy, F1, MAE, RMSE, track error |
| 13 | FastAPI service | Latest storm history | Forecast, category when available, alerts |
| 14 | Streamlit | Artifacts and local API | Operational visualization |

## Technologies and resources

### Programming and data

- Python 3.10+
- pandas and NumPy — CSV handling, transformations, numerical arrays
- SciPy, xarray, h5py, netCDF4 — scientific and geospatial data support
- Jupyter — exploration notebooks for the data pipeline

### Machine learning

- PyTorch — CNN detector and LSTM forecasting models
- scikit-learn — MLP category classifier, train/test split, metrics
- Pillow — satellite image loading and resizing

### Evaluation and visualization

- scikit-learn — accuracy, precision, recall, F1, MAE, RMSE
- Haversine formula — geodesic track-error measurement in kilometres
- matplotlib and seaborn — offline plotting support
- Plotly, Folium, streamlit-folium — interactive dashboard charts and maps

### Application layer

- FastAPI — local prediction API (`/health`, `/forecast`)
- Uvicorn — local ASGI server
- Streamlit — dashboard user interface

## Local resources and endpoints

| Resource | Location / address | Purpose |
|---|---|---|
| Fused data | `tropical-cyclone-ai/data/processed/fused_dataset/` | Training source for temporal models |
| Model artifacts | `tropical-cyclone-ai/models/` | Detector, classifier, intensity, and track checkpoints |
| Pipeline artifacts | `tropical-cyclone-ai/data/processed/` | Outputs consumed by dashboard |
| Prediction API | `http://127.0.0.1:8000` | Local health and forecast endpoints |
| Dashboard | `http://localhost:8501` | Streamlit interface |

## Reproducible execution order

1. Install dependencies from the three `requirements` files.
2. Complete or load cleaned/fused data for Steps 1–5.
3. Add labelled satellite image crops and run Steps 6–8.
4. Train the temporal, intensity, and track models in Steps 9–11.
5. Run Step 12 evaluation and save metrics.
6. Start the local Step 13 API.
7. Start the Streamlit dashboard and use **Pipeline Control Center**.

No cloud deployment is required. All model training, artifact storage, API calls, and dashboard communication are designed to run locally.
