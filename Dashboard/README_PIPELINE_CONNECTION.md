# Dashboard connection

The Streamlit dashboard now reads pipeline artifacts directly from `../tropical-cyclone-ai` and exposes a **Pipeline Control Center** page. It never fabricates model output: missing artifacts are clearly marked as not generated.

Run locally in two terminals:

```powershell
# Terminal 1 — after training Steps 8, 10 and 11
cd ..\tropical-cyclone-ai
$env:PYTHONPATH = 'src'
uvicorn prediction_engine.app:app --reload

# Terminal 2
cd ..\Dashboard
streamlit run dashboard/app.py
```

The existing visualization pages remain available. The new page provides the connected source of truth for Steps 6–13, live forecast requests, artifacts, alerts, and saved evaluation metrics.
