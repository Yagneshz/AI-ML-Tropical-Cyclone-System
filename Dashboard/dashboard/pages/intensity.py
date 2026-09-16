import streamlit as st

from dashboard.components.charts import display_intensity_charts
from dashboard.data.sample_data import (
    CURRENT_CYCLONE,
    INTENSITY_FORECAST,
)


st.set_page_config(
    page_title="Cyclone Intensity",
    page_icon="📈",
    layout="wide",
)


# ---------------------------------------------------------
# PAGE TITLE
# ---------------------------------------------------------

st.title("📈 Cyclone Intensity Prediction")

st.markdown(
    """
    AI-based prediction of tropical cyclone intensity using
    wind speed and central pressure forecasts.
    """
)

st.info(
    "Development mode: intensity forecasts are currently "
    "sample values. The real ML intensity model will be "
    "connected later."
)


# ---------------------------------------------------------
# CURRENT CYCLONE DATA
# ---------------------------------------------------------

cyclone = CURRENT_CYCLONE

current_wind = cyclone["wind_speed"]
current_pressure = cyclone["pressure"]
classification = cyclone["classification"]
confidence = cyclone["confidence"]


# ---------------------------------------------------------
# CURRENT INTENSITY
# ---------------------------------------------------------

st.subheader("🌪️ Current Intensity")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Wind Speed",
        f"{current_wind} km/h",
    )

with col2:
    st.metric(
        "Central Pressure",
        f"{current_pressure} hPa",
    )

with col3:
    st.metric(
        "Classification",
        classification,
    )

with col4:
    st.metric(
        "AI Confidence",
        f"{confidence:.0%}",
    )


# ---------------------------------------------------------
# INTENSITY FORECAST
# ---------------------------------------------------------

st.subheader("🔮 Intensity Forecast")

display_intensity_charts(
    INTENSITY_FORECAST
)


# ---------------------------------------------------------
# FORECAST SUMMARY
# ---------------------------------------------------------

st.subheader("📊 Forecast Summary")

forecast_24h = next(
    (
        point
        for point in INTENSITY_FORECAST
        if point["hour"] == 24
    ),
    None,
)

forecast_48h = next(
    (
        point
        for point in INTENSITY_FORECAST
        if point["hour"] == 48
    ),
    None,
)

forecast_72h = next(
    (
        point
        for point in INTENSITY_FORECAST
        if point["hour"] == 72
    ),
    None,
)


col1, col2, col3 = st.columns(3)

with col1:

    st.markdown("### +24 Hours")

    if forecast_24h:
        st.metric(
            "Wind Speed",
            f"{forecast_24h['wind_speed']} km/h",
            delta=f"{forecast_24h['wind_speed'] - current_wind} km/h",
        )

        st.write(
            f"Pressure: **{forecast_24h['pressure']} hPa**"
        )


with col2:

    st.markdown("### +48 Hours")

    if forecast_48h:
        st.metric(
            "Wind Speed",
            f"{forecast_48h['wind_speed']} km/h",
            delta=f"{forecast_48h['wind_speed'] - current_wind} km/h",
        )

        st.write(
            f"Pressure: **{forecast_48h['pressure']} hPa**"
        )


with col3:

    st.markdown("### +72 Hours")

    if forecast_72h:
        st.metric(
            "Wind Speed",
            f"{forecast_72h['wind_speed']} km/h",
            delta=f"{forecast_72h['wind_speed'] - current_wind} km/h",
        )

        st.write(
            f"Pressure: **{forecast_72h['pressure']} hPa**"
        )


# ---------------------------------------------------------
# INTENSITY TREND
# ---------------------------------------------------------

st.subheader("📈 Intensity Trend")

initial_wind = INTENSITY_FORECAST[0]["wind_speed"]
final_wind = INTENSITY_FORECAST[-1]["wind_speed"]

wind_change = final_wind - initial_wind

if wind_change > 0:

    st.warning(
        f"⚠️ The sample forecast indicates increasing "
        f"wind intensity by **{wind_change} km/h** over "
        f"the forecast period."
    )

elif wind_change < 0:

    st.success(
        f"✅ The sample forecast indicates decreasing "
        f"wind intensity by **{abs(wind_change)} km/h**."
    )

else:

    st.info(
        "The sample forecast indicates relatively stable "
        "wind intensity."
    )


# ---------------------------------------------------------
# FORECAST TABLE
# ---------------------------------------------------------

st.subheader("📋 Detailed Intensity Forecast")

table_data = []

for point in INTENSITY_FORECAST:

    table_data.append(
        {
            "Forecast Hour": f"+{point['hour']} h",
            "Wind Speed (km/h)": point["wind_speed"],
            "Pressure (hPa)": point["pressure"],
        }
    )

st.dataframe(
    table_data,
    use_container_width=True,
    hide_index=True,
)


# ---------------------------------------------------------
# FUTURE MODEL INTEGRATION
# ---------------------------------------------------------

st.subheader("🤖 Future AI Intensity Model")

st.markdown(
    """
    Later, this page will receive predictions from the team's
    trained intensity model.

    **Expected model input:**

    - Satellite image features
    - Cyclone center
    - Historical intensity
    - Temporal sequence
    - Atmospheric/environmental features

    **Expected model output:**

    - Future wind speed
    - Future central pressure
    - Intensity trend
    - Prediction uncertainty
    """
)


st.warning(
    "⚠️ These are sample intensity predictions and are not "
    "official meteorological forecasts."
)