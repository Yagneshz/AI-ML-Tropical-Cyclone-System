import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Tropical Cyclone Prediction System",
    page_icon="🌀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🌀 Cyclone AI")

    st.markdown("---")

    st.markdown(
        """
        ### Navigation

        Use the pages above to explore:

        - Cyclone Detection
        - Classification
        - Intensity Estimation
        - Track Forecast
        - Model Performance
        """
    )

    st.markdown("---")

    st.caption(
        "AI Tropical Cyclone Prediction System"
    )

    st.caption(
        "Multi-Source Satellite Intelligence"
    )


# ============================================================
# MAIN PAGE
# ============================================================

st.title(
    "🌀 AI Tropical Cyclone Prediction System"
)

st.subheader(
    "Multi-Source Satellite Intelligence & Forecasting"
)

st.markdown(
    """
    An AI/ML-based platform for **tropical cyclone
    identification, classification, intensity estimation,
    and track prediction** using multi-source satellite data.
    """
)


# ============================================================
# SYSTEM STATUS
# ============================================================

st.markdown("## 🟢 System Status")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "System",
        "Online"
    )

with col2:
    st.metric(
        "Satellite Sources",
        "5"
    )

with col3:
    st.metric(
        "ML Modules",
        "4"
    )

with col4:
    st.metric(
        "Dashboard",
        "Ready"
    )


# ============================================================
# PROJECT MODULES
# ============================================================

st.markdown("## 🚀 Project Modules")

col1, col2 = st.columns(2)

with col1:

    st.markdown(
        """
        ### 🛰️ Cyclone Detection

        Detect potential tropical cyclone structures
        from satellite imagery.

        **Input:** Satellite imagery

        **Output:** Cyclone location + confidence
        """
    )

    st.markdown(
        """
        ### 📊 Intensity Estimation

        Estimate cyclone intensity using satellite
        and temporal information.

        **Output:**

        - Wind speed
        - Central pressure
        - Intensity trend
        """
    )


with col2:

    st.markdown(
        """
        ### 🌪️ Classification

        Identify the cyclone development stage and
        intensity category.

        **Output:** Cyclone category + probability
        """
    )

    st.markdown(
        """
        ### 🗺️ Track Forecast

        Predict the future movement of the cyclone.

        **Output:**

        - Future coordinates
        - Track
        - Forecast uncertainty
        """
    )


# ============================================================
# PIPELINE
# ============================================================

st.markdown("## 🔄 AI Processing Pipeline")

st.code(
    """
Multi-Source Satellite Data
          ↓
Data Cleaning
          ↓
Preprocessing
          ↓
Feature Extraction
          ↓
Cyclone Detection
          ↓
Classification
          ↓
Intensity Estimation
          ↓
Track Forecasting
          ↓
Dashboard Visualization
          ↓
Cyclone Alerts
    """
)


# ============================================================
# DEVELOPMENT STATUS
# ============================================================

st.markdown("## 📌 Development Status")

st.progress(
    0.55,
    text="Dashboard Development: 55%"
)

st.info(
    """
    The dashboard currently uses demonstration data.
    Actual ML model outputs will be integrated after the
    data-processing and model-development pipelines are ready.
    """
)


st.markdown("---")

st.caption(
    "⚠️ This system is intended for research and educational purposes. "
    "It should not replace official meteorological warnings."
)