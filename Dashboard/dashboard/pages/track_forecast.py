import streamlit as st
import pandas as pd

from dashboard.components.maps import display_cyclone_map
from dashboard.data.sample_data import (
    CURRENT_CYCLONE,
    OBSERVED_TRACK,
    FORECAST_TRACK,
)


st.set_page_config(
    page_title="Track Forecast",
    page_icon="🗺️",
    layout="wide",
)


# ---------------------------------------------------------
# PAGE TITLE
# ---------------------------------------------------------

st.title("🗺️ Cyclone Track Forecast")

st.markdown(
    """
    AI-based prediction of the future movement and location
    of a tropical cyclone.
    """
)

st.info(
    "Development mode: track predictions are currently "
    "sample values. The real AI track model will be "
    "connected later."
)


# ---------------------------------------------------------
# CURRENT CYCLONE
# ---------------------------------------------------------

cyclone = CURRENT_CYCLONE

latitude = cyclone["latitude"]
longitude = cyclone["longitude"]
name = cyclone["name"]
classification = cyclone["classification"]
confidence = cyclone["confidence"]


# ---------------------------------------------------------
# CURRENT INFORMATION
# ---------------------------------------------------------

st.subheader("🌪️ Current Cyclone Position")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Cyclone",
        name,
    )

with col2:
    st.metric(
        "Latitude",
        f"{latitude:.2f}° N",
    )

with col3:
    st.metric(
        "Longitude",
        f"{longitude:.2f}° E",
    )

with col4:
    st.metric(
        "AI Confidence",
        f"{confidence:.0%}",
    )


# ---------------------------------------------------------
# TRACK DATA
# ---------------------------------------------------------

observed_points = [
    (
        point["latitude"],
        point["longitude"],
    )
    for point in OBSERVED_TRACK
]

forecast_points = [
    (
        point["latitude"],
        point["longitude"],
    )
    for point in FORECAST_TRACK
]


# ---------------------------------------------------------
# TRACK MAP
# ---------------------------------------------------------

st.subheader("🗺️ Observed Track & AI Forecast")

display_cyclone_map(
    latitude=latitude,
    longitude=longitude,
    observed_track=observed_points,
    forecast_track=forecast_points,
    zoom_start=5,
)


# ---------------------------------------------------------
# FORECAST POINTS
# ---------------------------------------------------------

st.subheader("📍 Forecast Positions")

forecast_table = []

for point in FORECAST_TRACK:

    forecast_table.append(
        {
            "Forecast": f"+{point['hour']} hours",
            "Latitude": f"{point['latitude']:.2f}° N",
            "Longitude": f"{point['longitude']:.2f}° E",
        }
    )

st.dataframe(
    forecast_table,
    use_container_width=True,
    hide_index=True,
)


# ---------------------------------------------------------
# FORECAST POSITION SELECTOR
# ---------------------------------------------------------

st.subheader("🔎 Inspect Forecast Position")

available_hours = [
    point["hour"]
    for point in FORECAST_TRACK
]

selected_hour = st.selectbox(
    "Select forecast time",
    available_hours,
    format_func=lambda x: f"+{x} hours",
)


selected_point = next(
    point
    for point in FORECAST_TRACK
    if point["hour"] == selected_hour
)


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Forecast Time",
        f"+{selected_hour} hours",
    )

with col2:
    st.metric(
        "Latitude",
        f"{selected_point['latitude']:.2f}° N",
    )

with col3:
    st.metric(
        "Longitude",
        f"{selected_point['longitude']:.2f}° E",
    )


# ---------------------------------------------------------
# MOVEMENT INFORMATION
# ---------------------------------------------------------

st.subheader("🧭 Track Movement")

start_point = FORECAST_TRACK[0]
end_point = FORECAST_TRACK[-1]

latitude_change = (
    end_point["latitude"] -
    start_point["latitude"]
)

longitude_change = (
    end_point["longitude"] -
    start_point["longitude"]
)


col1, col2 = st.columns(2)

with col1:

    st.write(
        f"**Latitude change:** "
        f"{latitude_change:+.2f}°"
    )

    if latitude_change > 0:
        st.success(
            "The sample forecast indicates "
            "northward movement."
        )
    elif latitude_change < 0:
        st.warning(
            "The sample forecast indicates "
            "southward movement."
        )
    else:
        st.info(
            "The sample forecast indicates "
            "little north-south movement."
        )


with col2:

    st.write(
        f"**Longitude change:** "
        f"{longitude_change:+.2f}°"
    )

    if longitude_change > 0:
        st.success(
            "The sample forecast indicates "
            "eastward movement."
        )
    elif longitude_change < 0:
        st.warning(
            "The sample forecast indicates "
            "westward movement."
        )
    else:
        st.info(
            "The sample forecast indicates "
            "little east-west movement."
        )


# ---------------------------------------------------------
# TRACK SUMMARY
# ---------------------------------------------------------

st.subheader("📊 Track Forecast Summary")

st.write(
    f"""
    The current cyclone is located at approximately
    **{latitude:.2f}° N, {longitude:.2f}° E**.

    The sample AI forecast extends to **+{end_point['hour']} hours**.

    Forecast endpoint:

    **{end_point['latitude']:.2f}° N,
    {end_point['longitude']:.2f}° E**
    """
)


# ---------------------------------------------------------
# FUTURE MODEL INTEGRATION
# ---------------------------------------------------------

st.subheader("🤖 Future AI Track Model")

st.markdown(
    """
    Later, this page will receive predictions from the team's
    trained track forecasting model.

    **Expected input:**

    - Historical cyclone positions
    - Satellite-derived cyclone center
    - Atmospheric/environmental features
    - Previous movement direction
    - Previous movement speed
    - Temporal sequence data

    **Expected output:**

    - Future latitude
    - Future longitude
    - Forecast time
    - Track uncertainty
    - Forecast cone
    """
)


st.warning(
    "⚠️ These are sample track predictions and are not "
    "official meteorological forecasts."
)