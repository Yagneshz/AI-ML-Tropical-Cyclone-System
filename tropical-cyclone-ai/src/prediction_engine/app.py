"""Local HTTP interface for Step 13; intentionally contains no deployment setup."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from prediction_engine.service import PredictionEngine

app = FastAPI(title='Tropical Cyclone Prediction Engine', version='1.0.0')
engine = PredictionEngine()

class ForecastRequest(BaseModel):
    cyclone_id: str | None = None
    history: list[list[float]] = Field(description='Latest rows: LAT_IBTRACS, LON_IBTRACS, USA_WIND, USA_PRES')
    feature_vector: list[float] | None = Field(default=None, description='Optional 256-dimensional Step-7 feature vector')

@app.get('/health')
def health(): return {'status': 'ready' if all(engine.status().values()) else 'models_missing', 'models': engine.status()}

@app.post('/forecast')
def forecast(request: ForecastRequest):
    try:
        response = engine.forecast(request.history, request.feature_vector)
        return {'cyclone_id': request.cyclone_id, **response}
    except (ValueError, FileNotFoundError) as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
