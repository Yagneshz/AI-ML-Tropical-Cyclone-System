import folium


# ============================================================
# ADD FORECAST UNCERTAINTY CONE
# ============================================================

def add_forecast_cone(
    cyclone_map,
    forecast_points,
    initial_width=0.25,
    width_growth=0.15
):
    """
    Add AI forecast track and uncertainty cone to a Folium map.

    Parameters
    ----------
    cyclone_map : folium.Map
        Existing Folium map.

    forecast_points : list
        List of (latitude, longitude) forecast points.

    initial_width : float
        Initial uncertainty width in degrees.

    width_growth : float
        Additional uncertainty width for each forecast point.
    """

    if not forecast_points:
        return cyclone_map

    # --------------------------------------------------------
    # FORECAST TRACK
    # --------------------------------------------------------

    folium.PolyLine(
        locations=forecast_points,
        weight=3,
        dash_array="8, 8",
        tooltip="AI Forecast Track"
    ).add_to(cyclone_map)

    # --------------------------------------------------------
    # CREATE UNCERTAINTY BOUNDARIES
    # --------------------------------------------------------

    left_boundary = []
    right_boundary = []

    for index, (lat, lon) in enumerate(forecast_points):

        # Uncertainty increases with forecast time
        width = initial_width + (
            index * width_growth
        )

        left_boundary.append(
            (
                lat + width,
                lon - width
            )
        )

        right_boundary.append(
            (
                lat - width,
                lon + width
            )
        )

    # Combine boundaries into polygon
    cone_polygon = (
        left_boundary +
        right_boundary[::-1]
    )

    # --------------------------------------------------------
    # DRAW UNCERTAINTY CONE
    # --------------------------------------------------------

    folium.Polygon(
        locations=cone_polygon,
        tooltip="AI Forecast Uncertainty Cone",
        fill=True,
        fill_opacity=0.20,
        weight=1
    ).add_to(cyclone_map)

    # --------------------------------------------------------
    # FORECAST POINTS
    # --------------------------------------------------------

    for index, point in enumerate(forecast_points):

        folium.CircleMarker(
            location=point,
            radius=5,
            tooltip=f"Forecast Point {index + 1}",
            fill=True
        ).add_to(cyclone_map)

    return cyclone_map