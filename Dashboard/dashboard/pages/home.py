import streamlit as st
import plotly.graph_objects as go
from dashboard.components.maps import display_cyclone_map
from dashboard.components.satellite_viewer import display_satellite_panel
from dashboard.components.alerts import display_alert_summary
from dashboard.components.controls import display_dashboard_controls
from dashboard.data.sample_data import (
    CURRENT_CYCLONE,
    OBSERVED_TRACK,
    FORECAST_TRACK,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Cyclone AI Dashboard",
    page_icon="🌀",
    layout="wide",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 38px;
        font-weight: 700;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 17px;
        color: #8b96a5;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 650;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    .metric-card {
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #303846;
        background-color: #171d26;
    }

    .metric-label {
        font-size: 13px;
        color: #9ba6b5;
    }

    .metric-value {
        font-size: 25px;
        font-weight: 700;
        margin-top: 5px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# DASHBOARD CONTROLS
# ============================================================

controls = display_dashboard_controls()

selected_model = controls["model"]
selected_satellite = controls["satellite"]
forecast_hours = controls["forecast_hours"]
observation_time = controls["observation_time"]

# ============================================================
# DATA
# ============================================================

cyclone = CURRENT_CYCLONE

name = cyclone["name"]
latitude = cyclone["latitude"]
longitude = cyclone["longitude"]
wind_speed = cyclone["wind_speed"]
pressure = cyclone["pressure"]
classification = cyclone["classification"]
confidence = cyclone["confidence"]
status = cyclone["status"]
development_stage = cyclone["development_stage"]


observed_lat = [
    point["latitude"]
    for point in OBSERVED_TRACK
]

observed_lon = [
    point["longitude"]
    for point in OBSERVED_TRACK
]

observed_points = [
    (
        point["latitude"],
        point["longitude"]
    )
    for point in OBSERVED_TRACK
]

forecast_points = [
    (
        point["latitude"],
        point["longitude"]
    )
    for point in FORECAST_TRACK
]

forecast_lat = [
    latitude
] + [
    point["latitude"]
    for point in FORECAST_TRACK
]

forecast_lon = [
    longitude
] + [
    point["longitude"]
    for point in FORECAST_TRACK
]


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🌀 AI Tropical Cyclone Prediction System</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'Multi-Source Satellite Intelligence & Cyclone Forecasting'
    '</div>',
    unsafe_allow_html=True,
)

st.caption(
    f"Model: {selected_model} | "
    f"Satellite: {selected_satellite} | "
    f"Forecast: {forecast_hours} hours"
)


# ============================================================
# TOP METRICS
# ============================================================

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "System Status",
        "🟢 Online",
    )

with col2:
    st.metric(
        "Cyclone Status",
        status,
    )

with col3:
    st.metric(
        "Current Wind",
        f"{wind_speed} km/h",
    )

with col4:
    st.metric(
        "AI Confidence",
        f"{confidence:.0%}",
    )

with col5:
    st.metric(
        "Forecast",
        f"{forecast_hours} h",
    )


# ============================================================
# CYCLONE SUMMARY
# ============================================================

st.markdown(
    '<div class="section-title">🌪️ Current Cyclone</div>',
    unsafe_allow_html=True,
)

col1, col2 = st.columns([1, 2])

with col1:

    st.markdown(
        f"""
        <div class="metric-card">

        <div class="metric-label">CYCLONE NAME</div>
        <div class="metric-value">{name}</div>

        <br>

        <div class="metric-label">CLASSIFICATION</div>
        <div class="metric-value">{classification}</div>

        <br>

        <div class="metric-label">DEVELOPMENT STAGE</div>
        <div class="metric-value">{development_stage}</div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with col2:

    location_col1, location_col2, location_col3 = st.columns(3)

    with location_col1:
        st.metric(
            "Latitude",
            f"{latitude:.2f}° N",
        )

    with location_col2:
        st.metric(
            "Longitude",
            f"{longitude:.2f}° E",
        )

    with location_col3:
        st.metric(
            "Pressure",
            f"{pressure} hPa",
        )

# ============================================================
# CYCLONE ALERT
# ============================================================

st.markdown(
    '<div class="section-title">🚨 Cyclone Alert</div>',
    unsafe_allow_html=True,
)

display_alert_summary(
    wind_speed=wind_speed,
    pressure=pressure,
    classification=classification,
    confidence=confidence,
    development_stage=development_stage,
)
# ============================================================
# SATELLITE OBSERVATION
# ============================================================

st.markdown(
    '<div class="section-title">🛰️ Satellite Observation</div>',
    unsafe_allow_html=True,
)

display_satellite_panel(
    satellite_name=selected_satellite,
    timestamp=observation_time,
    channel="Infrared",
)


# ============================================================
# TRACK MAP
# ============================================================

st.markdown(
    '<div class="section-title">🗺️ Cyclone Track & AI Forecast</div>',
    unsafe_allow_html=True,
)

display_cyclone_map(
    latitude=latitude,
    longitude=longitude,
    observed_track=observed_points,
    forecast_track=forecast_points,
    zoom_start=5,
)

# ============================================================
# QUICK ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">⚡ Quick Analysis</div>',
    unsafe_allow_html=True,
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.info(
        """
        🛰️ **Detection**

        Cyclone structure detected from satellite imagery.
        """
    )

with col2:
    st.info(
        f"""
        🌪️ **Classification**

        Current category:

        **{classification}**
        """
    )

with col3:
    st.info(
        f"""
        📊 **Intensity**

        Current wind:

        **{wind_speed} km/h**
        """
    )

with col4:
    st.info(
        """
        🗺️ **Track**

        AI forecast available for the next 96 hours.
        """
    )


# ============================================================
# DEVELOPMENT NOTICE
# ============================================================

st.markdown("---")

st.warning(
    "Development mode: dashboard values are currently "
    "sample data. Real satellite observations and ML "
    "predictions will be connected later."
)

st.caption(
    "Research and educational system — not a replacement "
    "for official meteorological warnings."
)