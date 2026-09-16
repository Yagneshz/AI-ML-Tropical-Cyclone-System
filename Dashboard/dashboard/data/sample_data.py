"""
Temporary sample data for dashboard development.

This file will eventually be replaced/connected
to real ML and satellite data outputs.
"""


# ============================================================
# CURRENT CYCLONE
# ============================================================

CURRENT_CYCLONE = {
    "name": "Sample Cyclone",

    "latitude": 16.30,

    "longitude": 84.50,

    "wind_speed": 120,

    "pressure": 980,

    "classification": "Severe Cyclonic Storm",

    "confidence": 0.91,

    "status": "Detected",

    "development_stage": "Intensifying"
}


# ============================================================
# OBSERVED TRACK
# ============================================================

OBSERVED_TRACK = [
    {
        "hour": -18,
        "latitude": 14.20,
        "longitude": 82.10
    },
    {
        "hour": -12,
        "latitude": 14.80,
        "longitude": 82.80
    },
    {
        "hour": -6,
        "latitude": 15.50,
        "longitude": 83.60
    },
    {
        "hour": 0,
        "latitude": 16.30,
        "longitude": 84.50
    }
]


# ============================================================
# FORECAST TRACK
# ============================================================

FORECAST_TRACK = [
    {
        "hour": 24,
        "latitude": 17.10,
        "longitude": 85.40
    },
    {
        "hour": 48,
        "latitude": 18.00,
        "longitude": 86.30
    },
    {
        "hour": 72,
        "latitude": 18.80,
        "longitude": 87.20
    },
    {
        "hour": 96,
        "latitude": 19.60,
        "longitude": 88.00
    }
]


# ============================================================
# INTENSITY FORECAST
# ============================================================

INTENSITY_FORECAST = [
    {
        "hour": 0,
        "wind_speed": 120,
        "pressure": 980
    },
    {
        "hour": 6,
        "wind_speed": 123,
        "pressure": 978
    },
    {
        "hour": 12,
        "wind_speed": 127,
        "pressure": 975
    },
    {
        "hour": 18,
        "wind_speed": 130,
        "pressure": 973
    },
    {
        "hour": 24,
        "wind_speed": 135,
        "pressure": 970
    },
    {
        "hour": 30,
        "wind_speed": 138,
        "pressure": 968
    },
    {
        "hour": 36,
        "wind_speed": 141,
        "pressure": 965
    },
    {
        "hour": 42,
        "wind_speed": 143,
        "pressure": 963
    },
    {
        "hour": 48,
        "wind_speed": 145,
        "pressure": 960
    },
    {
        "hour": 72,
        "wind_speed": 150,
        "pressure": 955
    }
]


# ============================================================
# CLASSIFICATION PROBABILITIES
# ============================================================

CLASSIFICATION_PROBABILITIES = {
    "Depression": 0.01,
    "Deep Depression": 0.02,
    "Cyclonic Storm": 0.05,
    "Severe Cyclonic Storm": 0.82,
    "Very Severe Cyclonic Storm": 0.08,
    "Extremely Severe Cyclonic Storm": 0.02
}


# ============================================================
# MODEL PERFORMANCE
# ============================================================

MODEL_PERFORMANCE = {
    "detection_accuracy": 0.942,

    "classification_accuracy": 0.916,

    "intensity_mae": 8.4,

    "track_error": 42
}