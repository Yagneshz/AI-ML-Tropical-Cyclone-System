import streamlit as st

from dashboard.components.charts import (
    display_classification_chart,
    display_confidence_chart,
)

from dashboard.data.sample_data import (
    CURRENT_CYCLONE,
    CLASSIFICATION_PROBABILITIES,
)


st.set_page_config(
    page_title="Cyclone Classification",
    page_icon="🌪️",
    layout="wide",
)


# ---------------------------------------------------------
# PAGE TITLE
# ---------------------------------------------------------

st.title("🌪️ Cyclone Classification")

st.markdown(
    """
    AI-based classification of tropical cyclones into
    different intensity categories.
    """
)

st.info(
    "Development mode: classification values are currently "
    "sample model outputs. Real ML predictions will be "
    "connected later."
)


# ---------------------------------------------------------
# CURRENT CYCLONE DATA
# ---------------------------------------------------------

cyclone = CURRENT_CYCLONE

classification = cyclone["classification"]
confidence = cyclone["confidence"]
wind_speed = cyclone["wind_speed"]
pressure = cyclone["pressure"]


# ---------------------------------------------------------
# CURRENT CLASSIFICATION
# ---------------------------------------------------------

st.subheader("🎯 Current Classification")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Classification",
        classification,
    )

with col2:
    st.metric(
        "Confidence",
        f"{confidence:.0%}",
    )

with col3:
    st.metric(
        "Wind Speed",
        f"{wind_speed} km/h",
    )

with col4:
    st.metric(
        "Pressure",
        f"{pressure} hPa",
    )


# ---------------------------------------------------------
# CLASSIFICATION PROBABILITIES
# ---------------------------------------------------------

st.subheader("📊 Classification Probabilities")

display_classification_chart(
    CLASSIFICATION_PROBABILITIES
)


# ---------------------------------------------------------
# HIGHEST PROBABILITY
# ---------------------------------------------------------

predicted_class = max(
    CLASSIFICATION_PROBABILITIES,
    key=CLASSIFICATION_PROBABILITIES.get,
)

predicted_probability = CLASSIFICATION_PROBABILITIES[
    predicted_class
]


st.subheader("🤖 AI Prediction")

col1, col2 = st.columns(2)

with col1:
    st.success(
        f"### {predicted_class}"
    )

    st.write(
        f"The AI model currently predicts "
        f"**{predicted_class}** as the most likely category."
    )

with col2:
    display_confidence_chart(
        confidence=predicted_probability,
        title="Classification Probability",
    )


# ---------------------------------------------------------
# CATEGORY TABLE
# ---------------------------------------------------------

st.subheader("📋 Category Probabilities")

for category, probability in CLASSIFICATION_PROBABILITIES.items():

    st.write(
        f"**{category}** — {probability:.1%}"
    )

    st.progress(
        probability
    )


# ---------------------------------------------------------
# CLASSIFICATION INTERPRETATION
# ---------------------------------------------------------

st.subheader("🧠 Classification Interpretation")

if predicted_probability >= 0.80:

    st.success(
        f"High confidence classification: "
        f"**{predicted_class}** ({predicted_probability:.1%})"
    )

elif predicted_probability >= 0.60:

    st.warning(
        f"Moderate confidence classification: "
        f"**{predicted_class}** ({predicted_probability:.1%})"
    )

else:

    st.warning(
        f"Low confidence classification: "
        f"**{predicted_class}** ({predicted_probability:.1%})"
    )


# ---------------------------------------------------------
# FUTURE MODEL INTEGRATION
# ---------------------------------------------------------

st.subheader("🔌 Future ML Integration")

st.markdown(
    """
    Later, this page will receive classification output from
    the team's trained ML model.

    Expected input/output:

    **Input**
    - Preprocessed satellite features
    - Cyclone detection information
    - Temporal features
    - Environmental features

    **Output**
    - Predicted cyclone category
    - Probability for each category
    - Model confidence
    - Model name/version
    """
)


st.warning(
    "⚠️ These are sample classification results and "
    "must not be interpreted as official cyclone warnings."
)