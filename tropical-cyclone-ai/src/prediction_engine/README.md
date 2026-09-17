# Step 13 — Local prediction engine

This is a local FastAPI prediction service; it does not include deployment, Docker, cloud, or background-worker configuration.

Install its dependency and start it from the project root:

```powershell
pip install -r requirements-step13.txt
$env:PYTHONPATH = 'src'
uvicorn prediction_engine.app:app --reload
```

Train Steps 10 and 11 first. `GET /health` reports which model files are available. `POST /forecast` accepts the latest four (or configured lookback) rows ordered as `LAT_IBTRACS,LON_IBTRACS,USA_WIND,USA_PRES` and returns the next intensity and track predictions. Supply the optional Step-7 256-value feature vector once the Step-8 category model is trained.

Example request body:

```json
{"cyclone_id":"example","history":[[12.0,82.0,45,990],[12.3,82.4,50,987],[12.7,82.8,55,984],[13.0,83.2,60,982]]}
```

Alerts are generated locally for predicted wind at or above 64 kt, major-cyclone wind at or above 96 kt, and pressure at or below 980 hPa.
