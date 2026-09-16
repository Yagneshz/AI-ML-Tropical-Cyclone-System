import folium
from streamlit_folium import st_folium

from dashboard.components.forecast_cone import add_forecast_cone


# ============================================================
# CREATE CYCLONE MAP
# ============================================================

def create_cyclone_map(
    latitude,
    longitude,
    observed_track=None,
    forecast_track=None,
    zoom_start=5
):
    """
    Create an interactive cyclone map.
    """

    cyclone_map = folium.Map(
        location=[latitude, longitude],
        zoom_start=zoom_start,
        control_scale=True
    )

    # --------------------------------------------------------
    # CURRENT CYCLONE POSITION
    # --------------------------------------------------------

    folium.Marker(
        location=[latitude, longitude],
        tooltip="Current Cyclone Position",
        popup=(
            f"Current Cyclone Position<br>"
            f"Latitude: {latitude:.2f}<br>"
            f"Longitude: {longitude:.2f}"
        ),
        icon=folium.Icon(
            color="red",
            icon="cloud"
        )
    ).add_to(cyclone_map)

    # --------------------------------------------------------
    # OBSERVED TRACK
    # --------------------------------------------------------

    if observed_track:

        folium.PolyLine(
            locations=observed_track,
            weight=4,
            tooltip="Observed Cyclone Track"
        ).add_to(cyclone_map)

        for index, point in enumerate(observed_track):

            folium.CircleMarker(
                location=point,
                radius=4,
                tooltip=f"Observed Point {index + 1}",
                fill=True
            ).add_to(cyclone_map)

    # --------------------------------------------------------
    # FORECAST TRACK + UNCERTAINTY CONE
    # --------------------------------------------------------

    if forecast_track:

        add_forecast_cone(
            cyclone_map=cyclone_map,
            forecast_points=forecast_track
        )

    return cyclone_map


# ============================================================
# DISPLAY CYCLONE MAP
# ============================================================

def display_cyclone_map(
    latitude,
    longitude,
    observed_track=None,
    forecast_track=None,
    zoom_start=5
):
    """
    Display cyclone map inside Streamlit.
    """

    cyclone_map = create_cyclone_map(
        latitude=latitude,
        longitude=longitude,
        observed_track=observed_track,
        forecast_track=forecast_track,
        zoom_start=zoom_start
    )

    return st_folium(
        cyclone_map,
        width=None,
        height=550
    )