"""Local bridge from the Streamlit dashboard to pipeline artifacts and Step 13."""
from __future__ import annotations
import json
import os
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[3] / 'tropical-cyclone-ai'
API_URL = os.getenv('PREDICTION_ENGINE_URL', 'http://127.0.0.1:8000')

ARTIFACTS = {
    'detections': PROJECT_ROOT / 'data/processed/detections/cyclone_detections.csv',
    'features': PROJECT_ROOT / 'data/processed/features/feature_metadata.csv',
    'categories': PROJECT_ROOT / 'data/processed/classification/cyclone_categories.csv',
    'temporal': PROJECT_ROOT / 'models/temporal_state_lstm.predictions.csv',
    'intensity': PROJECT_ROOT / 'models/intensity_lstm.predictions.csv',
    'track': PROJECT_ROOT / 'models/track_lstm.predictions.csv',
    'metrics': PROJECT_ROOT / 'data/processed/evaluation/metrics.json',
}

def read_artifact(name: str) -> pd.DataFrame:
    path = ARTIFACTS[name]
    return pd.read_csv(path) if path.is_file() else pd.DataFrame()

def artifact_status() -> dict[str, bool]:
    return {name: path.is_file() for name, path in ARTIFACTS.items()}

def metrics() -> dict:
    path = ARTIFACTS['metrics']
    return json.loads(path.read_text()) if path.is_file() else {}

def fused_data() -> pd.DataFrame:
    path = PROJECT_ROOT / 'data/processed/fused_dataset/tcir_ibtracs_fused.csv'
    return pd.read_csv(path, parse_dates=['TIME']) if path.is_file() else pd.DataFrame()

def engine_health() -> dict:
    try:
        with urlopen(f'{API_URL}/health', timeout=1.5) as response:
            return json.loads(response.read())
    except (URLError, OSError, json.JSONDecodeError):
        return {'status': 'offline', 'models': {}}

def engine_forecast(cyclone_id: str, history: list[list[float]]) -> dict:
    payload = json.dumps({'cyclone_id': cyclone_id, 'history': history}).encode()
    request = Request(f'{API_URL}/forecast', data=payload, headers={'Content-Type': 'application/json'}, method='POST')
    try:
        with urlopen(request, timeout=10) as response:
            return json.loads(response.read())
    except (URLError, OSError, json.JSONDecodeError) as error:
        return {'error': str(error)}
