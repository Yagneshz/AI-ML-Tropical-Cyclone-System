"""Model registry and business rules for local cyclone predictions."""
from __future__ import annotations
import pickle
from pathlib import Path
from typing import Any
import numpy as np
from cyclone_forecasting.core import predict

DEFAULT_MODELS = {'intensity': 'models/intensity_lstm.pt', 'track': 'models/track_lstm.pt', 'category': 'models/cyclone_category_mlp.pkl'}

class PredictionEngine:
    def __init__(self, model_paths: dict[str, str] | None = None):
        self.paths = {key: Path(value) for key, value in (model_paths or DEFAULT_MODELS).items()}
        self.category_model = None
        if self.paths['category'].is_file():
            with self.paths['category'].open('rb') as source: self.category_model = pickle.load(source)

    def status(self) -> dict[str, bool]:
        return {name: path.is_file() for name, path in self.paths.items()}

    def forecast(self, history: list[list[float]], feature_vector: list[float] | None = None) -> dict[str, Any]:
        available = self.status()
        if not available['intensity'] or not available['track']:
            missing = [name for name in ('intensity', 'track') if not available[name]]
            raise FileNotFoundError(f'Missing trained model(s): {", ".join(missing)}')
        intensity = predict(self.paths['intensity'], history)
        track = predict(self.paths['track'], history)
        result: dict[str, Any] = {'intensity': intensity, 'track': track, 'alerts': self.alerts(intensity)}
        if feature_vector is not None:
            if self.category_model is None: raise FileNotFoundError('Category classifier is not trained.')
            vector = np.asarray(feature_vector, dtype=float).reshape(1, -1)
            result['category'] = str(self.category_model.predict(vector)[0])
            result['category_confidence'] = float(self.category_model.predict_proba(vector).max())
        return result

    @staticmethod
    def alerts(intensity: dict[str, float]) -> list[dict[str, str]]:
        wind, pressure = intensity.get('USA_WIND'), intensity.get('USA_PRES'); alerts=[]
        if wind is not None and wind >= 64: alerts.append({'level': 'warning', 'rule': 'wind', 'message': f'Predicted gale-force wind: {wind:.1f} kt'})
        if wind is not None and wind >= 96: alerts.append({'level': 'critical', 'rule': 'wind', 'message': f'Predicted major-cyclone wind: {wind:.1f} kt'})
        if pressure is not None and pressure <= 980: alerts.append({'level': 'warning', 'rule': 'pressure', 'message': f'Predicted low central pressure: {pressure:.1f} hPa'})
        return alerts
