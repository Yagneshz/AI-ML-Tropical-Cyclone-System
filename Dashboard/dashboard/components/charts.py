import streamlit as st
import plotly.graph_objects as go


# ============================================================
# WIND SPEED CHART
# ============================================================

def display_wind_speed_chart(
    forecast_data,
    severe_threshold=118
):
    """
    Display cyclone wind-speed forecast.
    """

    if not forecast_data:
        st.info("No wind-speed forecast available.")
        return

    time = [
        point["hour"]
        for point in forecast_data
    ]

    wind_speed = [
        point["wind_speed"]
        for point in forecast_data
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=time,
            y=wind_speed,
            mode="lines+markers",
            name="Wind Speed",
        )
    )

    # Severe cyclone threshold
    fig.add_hline(
        y=severe_threshold,
        line_dash="dash",
        annotation_text="Severe Cyclone Threshold",
        annotation_position="top left",
    )

    fig.update_layout(
        title="🌪️ Cyclone Wind Speed Forecast",
        xaxis_title="Forecast Hour",
        yaxis_title="Wind Speed (km/h)",
        height=420,
        hovermode="x unified",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


# ============================================================
# PRESSURE CHART
# ============================================================

def display_pressure_chart(
    forecast_data
):
    """
    Display central-pressure forecast.
    """

    if not forecast_data:
        st.info("No pressure forecast available.")
        return

    time = [
        point["hour"]
        for point in forecast_data
    ]

    pressure = [
        point["pressure"]
        for point in forecast_data
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=time,
            y=pressure,
            mode="lines+markers",
            name="Central Pressure",
        )
    )

    fig.update_layout(
        title="📉 Central Pressure Forecast",
        xaxis_title="Forecast Hour",
        yaxis_title="Pressure (hPa)",
        height=420,
        hovermode="x unified",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


# ============================================================
# CLASSIFICATION PROBABILITY CHART
# ============================================================

def display_classification_chart(
    probabilities
):
    """
    Display cyclone classification probabilities.
    """

    if not probabilities:
        st.info("No classification probabilities available.")
        return

    labels = list(probabilities.keys())
    values = list(probabilities.values())

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=values,
            y=labels,
            orientation="h",
            text=[
                f"{value:.1%}"
                for value in values
            ],
            textposition="auto",
            name="Probability",
        )
    )

    fig.update_layout(
        title="🌪️ Cyclone Classification Probability",
        xaxis_title="Probability",
        yaxis_title="Classification",
        xaxis=dict(
            range=[0, 1]
        ),
        height=420,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


# ============================================================
# CONFIDENCE CHART
# ============================================================

def display_confidence_chart(
    confidence,
    title="AI Prediction Confidence"
):
    """
    Display model confidence.
    """

    fig = go.Figure()

    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=confidence * 100,
            title={
                "text": title
            },
            number={
                "suffix": "%"
            },
            gauge={
                "axis": {
                    "range": [0, 100]
                }
            },
        )
    )

    fig.update_layout(
        height=300,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


# ============================================================
# COMPLETE INTENSITY DASHBOARD
# ============================================================

def display_intensity_charts(
    forecast_data
):
    """
    Display wind-speed and pressure charts together.
    """

    col1, col2 = st.columns(2)

    with col1:

        display_wind_speed_chart(
            forecast_data
        )

    with col2:

        display_pressure_chart(
            forecast_data
        )