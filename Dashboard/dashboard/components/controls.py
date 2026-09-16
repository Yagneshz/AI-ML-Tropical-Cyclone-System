import streamlit as st


# ============================================================
# MODEL OPTIONS
# ============================================================

MODEL_OPTIONS = [
    "CNN-LSTM",
    "ConvLSTM",
    "Random Forest",
    "XGBoost",
]


# ============================================================
# SATELLITE OPTIONS
# ============================================================

SATELLITE_OPTIONS = [
    "INSAT-3D",
    "INSAT-3DR",
    "NOAA",
    "NASA",
    "Himawari",
    "GOES",
]


# ============================================================
# FORECAST OPTIONS
# ============================================================

FORECAST_OPTIONS = [
    24,
    48,
    72,
    96,
]


# ============================================================
# DASHBOARD CONTROLS
# ============================================================

def display_dashboard_controls():
    """
    Display common dashboard controls in the sidebar.

    Returns
    -------
    dict
        Selected dashboard options.
    """

    st.sidebar.header("🎛️ Dashboard Controls")

    # --------------------------------------------------------
    # MODEL
    # --------------------------------------------------------

    model = st.sidebar.selectbox(
        "🤖 Prediction Model",
        MODEL_OPTIONS,
        index=0,
    )

    # --------------------------------------------------------
    # SATELLITE SOURCE
    # --------------------------------------------------------

    satellite = st.sidebar.selectbox(
        "🛰️ Satellite Source",
        SATELLITE_OPTIONS,
        index=0,
    )

    # --------------------------------------------------------
    # FORECAST HORIZON
    # --------------------------------------------------------

    forecast_hours = st.sidebar.selectbox(
        "⏱️ Forecast Horizon",
        FORECAST_OPTIONS,
        index=3,
        format_func=lambda x: f"{x} hours",
    )

    # --------------------------------------------------------
    # OBSERVATION TIME
    # --------------------------------------------------------

    observation_time = st.sidebar.text_input(
        "📅 Observation Time",
        value="2026-09-06 12:00 UTC",
    )

    # --------------------------------------------------------
    # RESET BUTTON
    # --------------------------------------------------------

    if st.sidebar.button("🔄 Reset Controls"):

        st.rerun()

    return {
        "model": model,
        "satellite": satellite,
        "forecast_hours": forecast_hours,
        "observation_time": observation_time,
    }