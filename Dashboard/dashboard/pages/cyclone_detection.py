import streamlit as st
import folium
from streamlit_folium import st_folium

from dashboard.components.satellite_viewer import display_satellite_panel
from dashboard.components.charts import display_confidence_chart
from dashboard.data.sample_data import CURRENT_CYCLONE


st.set_page_config(
    page_title="Cyclone Detection",
    page_icon="🌪️",
    layout="wide",
)


# ---------------------------------------------------------
# PAGE TITLE
# ---------------------------------------------------------

st.title("🌪️ Cyclone Detection")

st.markdown(
    """
    Detect tropical cyclone structures from satellite imagery
    and estimate the cyclone center.
    """
)

st.info(
    "Development mode: detection results shown here are "
    "currently sample values. The real detection model will "
    "be connected later."
)


# ---------------------------------------------------------
# GET SAMPLE DATA
# ---------------------------------------------------------

cyclone = CURRENT_CYCLONE

latitude = cyclone["latitude"]
longitude = cyclone["longitude"]
confidence = cyclone["confidence"]
status = cyclone["status"]
classification = cyclone["classification"]


# ---------------------------------------------------------
# SATELLITE IMAGE
# ---------------------------------------------------------

st.subheader("🛰️ Satellite Observation")

display_satellite_panel(
    satellite_name="INSAT-3D",
    # timestamp="2026-09-06 12:00 UTC",
    channel="Infrared",
)


# ---------------------------------------------------------
# DETECTION RESULT
# ---------------------------------------------------------

st.subheader("🔍 Detection Result")

col1, col2, col3 = st.columns(3)

with col1:
    if status == "Detected":
        st.success("🌀 Cyclone Detected")
    else:
        st.warning("No Cyclone Detected")

with col2:
    st.metric(
        "Detection Confidence",
        f"{confidence:.0%}"
    )

with col3:
    st.metric(
        "Classification",
        classification
    )


# ---------------------------------------------------------
# CONFIDENCE
# ---------------------------------------------------------

st.subheader("📊 Detection Confidence")

display_confidence_chart(
    confidence=confidence,
    title="Cyclone Detection Confidence"
)


# ---------------------------------------------------------
# DETECTED CENTER
# ---------------------------------------------------------

st.subheader("📍 Detected Cyclone Center")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Latitude",
        f"{latitude:.2f}° N"
    )

with col2:
    st.metric(
        "Longitude",
        f"{longitude:.2f}° E"
    )


# ---------------------------------------------------------
# DETECTION MAP
# ---------------------------------------------------------

st.subheader("🗺️ Detected Cyclone Location")

detection_map = folium.Map(
    location=[latitude, longitude],
    zoom_start=6,
    control_scale=True,
)

folium.Marker(
    location=[latitude, longitude],
    tooltip="Detected Cyclone Center",
    popup=(
        f"<b>Cyclone Center</b><br>"
        f"Latitude: {latitude:.2f}<br>"
        f"Longitude: {longitude:.2f}<br>"
        f"Confidence: {confidence:.0%}"
    ),
    icon=folium.Icon(
        color="red",
        icon="cloud",
    ),
).add_to(detection_map)


# Demo detection region
folium.Circle(
    location=[latitude, longitude],
    radius=50000,
    tooltip="Demo Detection Region",
    fill=True,
    fill_opacity=0.15,
).add_to(detection_map)


st_folium(
    detection_map,
    width=None,
    height=500,
)


# ---------------------------------------------------------
# DETECTION INFORMATION
# ---------------------------------------------------------

st.subheader("📋 Detection Information")

info_col1, info_col2 = st.columns(2)

with info_col1:
    st.write("**Detection Status:**", status)
    st.write("**Cyclone Type:**", classification)
    st.write("**Confidence:**", f"{confidence:.0%}")

with info_col2:
    st.write("**Latitude:**", f"{latitude:.2f}° N")
    st.write("**Longitude:**", f"{longitude:.2f}° E")
    st.write("**Satellite Channel:**", "Infrared")


# ---------------------------------------------------------
# FUTURE MODEL INTEGRATION
# ---------------------------------------------------------

st.subheader("🤖 Future AI Detection")

st.markdown(
    """
    When the detection model is available, this page will receive:

    - Satellite image
    - Cyclone / No-Cyclone prediction
    - Detection confidence
    - Cyclone center latitude
    - Cyclone center longitude
    - Detection region / bounding box
    - Model name and version

    The sample values above will then be replaced by real
    model predictions.
    """
)


st.warning(
    "⚠️ Demo detection only — this result is not an official "
    "meteorological detection or warning."
)