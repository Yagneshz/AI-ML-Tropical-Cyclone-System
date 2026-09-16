import streamlit as st
import plotly.graph_objects as go

from dashboard.data.sample_data import MODEL_PERFORMANCE


st.set_page_config(
    page_title="Model Performance",
    page_icon="📊",
    layout="wide",
)


# ---------------------------------------------------------
# PAGE TITLE
# ---------------------------------------------------------

st.title("📊 Model Performance")

st.markdown(
    """
    Evaluation metrics for the AI-based tropical cyclone
    detection, classification, intensity prediction, and
    track forecasting models.
    """
)

st.info(
    "Development mode: the metrics shown below are sample "
    "values. They will be replaced with the team's actual "
    "evaluation results after model training."
)


# ---------------------------------------------------------
# LOAD PERFORMANCE DATA
# ---------------------------------------------------------

detection_accuracy = MODEL_PERFORMANCE["detection_accuracy"]
classification_accuracy = MODEL_PERFORMANCE[
    "classification_accuracy"
]
intensity_mae = MODEL_PERFORMANCE["intensity_mae"]
track_error = MODEL_PERFORMANCE["track_error"]


# ---------------------------------------------------------
# MAIN METRICS
# ---------------------------------------------------------

st.subheader("🎯 Overall Model Performance")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Detection Accuracy",
        f"{detection_accuracy:.1%}",
    )

with col2:
    st.metric(
        "Classification Accuracy",
        f"{classification_accuracy:.1%}",
    )

with col3:
    st.metric(
        "Intensity MAE",
        f"{intensity_mae:.1f} km/h",
    )

with col4:
    st.metric(
        "Track Error",
        f"{track_error:.0f} km",
    )


# ---------------------------------------------------------
# ACCURACY CHART
# ---------------------------------------------------------

st.subheader("📈 Classification & Detection Accuracy")

accuracy_labels = [
    "Detection",
    "Classification",
]

accuracy_values = [
    detection_accuracy * 100,
    classification_accuracy * 100,
]


fig_accuracy = go.Figure()

fig_accuracy.add_trace(
    go.Bar(
        x=accuracy_labels,
        y=accuracy_values,
        text=[
            f"{value:.1f}%"
            for value in accuracy_values
        ],
        textposition="auto",
        name="Accuracy",
    )
)

fig_accuracy.update_layout(
    yaxis_title="Accuracy (%)",
    xaxis_title="Model",
    yaxis=dict(range=[0, 100]),
    height=400,
)

st.plotly_chart(
    fig_accuracy,
    use_container_width=True,
)


# ---------------------------------------------------------
# ERROR METRICS
# ---------------------------------------------------------

st.subheader("📉 Prediction Error")

error_labels = [
    "Intensity MAE",
    "Track Error",
]

error_values = [
    intensity_mae,
    track_error,
]


fig_error = go.Figure()

fig_error.add_trace(
    go.Bar(
        x=error_labels,
        y=error_values,
        text=[
            f"{value:.1f}"
            for value in error_values
        ],
        textposition="auto",
        name="Error",
    )
)

fig_error.update_layout(
    yaxis_title="Error Value",
    xaxis_title="Prediction Task",
    height=400,
)

st.plotly_chart(
    fig_error,
    use_container_width=True,
)


# ---------------------------------------------------------
# METRIC EXPLANATION
# ---------------------------------------------------------

st.subheader("📚 Metric Explanation")

col1, col2 = st.columns(2)

with col1:

    st.markdown("### 🎯 Detection Accuracy")

    st.write(
        """
        Measures how accurately the system identifies whether
        a cyclone is present in the satellite observation.

        Higher accuracy is better.
        """
    )

    st.markdown("### 🌪️ Classification Accuracy")

    st.write(
        """
        Measures how accurately the model assigns the cyclone
        to the correct intensity category.

        Higher accuracy is better.
        """
    )


with col2:

    st.markdown("### 📈 Intensity MAE")

    st.write(
        """
        Mean Absolute Error measures the average difference
        between predicted and observed cyclone intensity.

        Lower MAE is better.
        """
    )

    st.markdown("### 🗺️ Track Error")

    st.write(
        """
        Measures the distance between the predicted cyclone
        position and the observed cyclone position.

        Lower track error is better.
        """
    )


# ---------------------------------------------------------
# PERFORMANCE SUMMARY
# ---------------------------------------------------------

st.subheader("📋 Performance Summary")

performance_table = [
    {
        "Task": "Cyclone Detection",
        "Metric": "Accuracy",
        "Value": f"{detection_accuracy:.1%}",
        "Better": "Higher",
    },
    {
        "Task": "Cyclone Classification",
        "Metric": "Accuracy",
        "Value": f"{classification_accuracy:.1%}",
        "Better": "Higher",
    },
    {
        "Task": "Intensity Prediction",
        "Metric": "MAE",
        "Value": f"{intensity_mae:.1f} km/h",
        "Better": "Lower",
    },
    {
        "Task": "Track Forecast",
        "Metric": "Track Error",
        "Value": f"{track_error:.0f} km",
        "Better": "Lower",
    },
]

st.dataframe(
    performance_table,
    use_container_width=True,
    hide_index=True,
)


# ---------------------------------------------------------
# FUTURE MODEL COMPARISON
# ---------------------------------------------------------

st.subheader("🤖 Future Model Comparison")

st.markdown(
    """
    After the team's models are trained, this section can be
    extended to compare different algorithms.

    Example:

    - CNN vs ResNet for image detection
    - CNN-LSTM vs ConvLSTM for temporal prediction
    - Random Forest vs XGBoost for classification
    - Different sequence lengths
    - Different satellite combinations
    """
)


st.warning(
    "⚠️ Performance metrics shown here are sample values "
    "for dashboard development."
)