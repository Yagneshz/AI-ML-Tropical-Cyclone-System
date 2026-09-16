import streamlit as st


# ============================================================
# DISPLAY ALERT
# ============================================================

def display_alert(
    title,
    message,
    level="info"
):
    """
    Display a formatted cyclone alert.
    """

    if level == "success":

        st.success(
            f"✅ {title}\n\n{message}"
        )

    elif level == "warning":

        st.warning(
            f"⚠️ {title}\n\n{message}"
        )

    elif level == "error":

        st.error(
            f"🚨 {title}\n\n{message}"
        )

    else:

        st.info(
            f"ℹ️ {title}\n\n{message}"
        )


# ============================================================
# DETERMINE ALERT LEVEL
# ============================================================

def get_alert_level(wind_speed):
    """
    Determine dashboard alert level from wind speed.
    """

    if wind_speed >= 118:
        return "error"

    elif wind_speed >= 89:
        return "warning"

    elif wind_speed >= 63:
        return "warning"

    else:
        return "success"


# ============================================================
# CYCLONE ALERT
# ============================================================

def cyclone_alert(
    wind_speed,
    pressure,
    classification,
    confidence,
    development_stage
):
    """
    Generate cyclone alert based on current conditions.
    """

    # --------------------------------------------------------
    # DETERMINE LEVEL
    # --------------------------------------------------------

    if wind_speed >= 118:

        title = "Severe Cyclone Alert"

        level = "error"

        message = (
            f"Classification: {classification}\n\n"
            f"Wind Speed: {wind_speed} km/h\n\n"
            f"Central Pressure: {pressure} hPa\n\n"
            f"AI Confidence: {confidence:.0%}\n\n"
            f"Development Stage: {development_stage}"
        )

    elif wind_speed >= 89:

        title = "Cyclone Warning"

        level = "warning"

        message = (
            f"Classification: {classification}\n\n"
            f"Wind Speed: {wind_speed} km/h\n\n"
            f"Central Pressure: {pressure} hPa\n\n"
            f"AI Confidence: {confidence:.0%}\n\n"
            f"Development Stage: {development_stage}"
        )

    elif wind_speed >= 63:

        title = "Cyclone Watch"

        level = "warning"

        message = (
            f"Classification: {classification}\n\n"
            f"Wind Speed: {wind_speed} km/h\n\n"
            f"AI Confidence: {confidence:.0%}"
        )

    else:

        title = "Cyclone Monitoring"

        level = "success"

        message = (
            f"Current wind speed: {wind_speed} km/h.\n\n"
            "Intensity is currently below the dashboard "
            "cyclone warning threshold."
        )

    # --------------------------------------------------------
    # DISPLAY
    # --------------------------------------------------------

    display_alert(
        title,
        message,
        level
    )


# ============================================================
# ALERT SUMMARY
# ============================================================

def display_alert_summary(
    wind_speed,
    pressure,
    classification,
    confidence,
    development_stage
):
    """
    Display cyclone alert together with key parameters.
    """

    st.markdown("### 🚨 Cyclone Alert")

    cyclone_alert(
        wind_speed=wind_speed,
        pressure=pressure,
        classification=classification,
        confidence=confidence,
        development_stage=development_stage
    )

    st.markdown("#### Current Conditions")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Wind Speed",
            f"{wind_speed} km/h"
        )

    with col2:
        st.metric(
            "Pressure",
            f"{pressure} hPa"
        )

    with col3:
        st.metric(
            "Confidence",
            f"{confidence:.0%}"
        )

    with col4:
        st.metric(
            "Stage",
            development_stage
        )