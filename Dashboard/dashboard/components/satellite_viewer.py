import streamlit as st
from PIL import Image
from pathlib import Path


def display_satellite_image(
    image_path=None,
    satellite_name="Sample Satellite",
    timestamp="Not available",
    channel="Infrared"
):
    """
    Display satellite image and observation information.
    """

    if image_path is not None:

        image_path = Path(image_path)

        if image_path.exists():

            try:
                image = Image.open(image_path)

                st.image(
                    image,
                    caption=f"{satellite_name} — {channel}",
                    use_container_width=True
                )

            except Exception as e:
                st.error(
                    f"Unable to load satellite image: {e}"
                )

        else:
            st.warning(
                "Satellite image file was not found."
            )

    else:

        st.info(
            "🛰️ No satellite image is currently connected."
        )

        st.markdown(
            """
            **Satellite data pipeline is not connected yet.**

            When the satellite-processing pipeline is ready,
            this section will display the actual cyclone imagery.
            """
        )

    st.markdown("### Observation Information")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Satellite",
            satellite_name
        )

    with col2:
        st.metric(
            "Channel",
            channel
        )

    with col3:
        st.metric(
            "Timestamp",
            timestamp
        )


def satellite_upload_section():

    st.markdown("### 📤 Upload Satellite Image")

    uploaded_file = st.file_uploader(
        "Upload satellite image",
        type=[
            "png",
            "jpg",
            "jpeg",
            "tif",
            "tiff"
        ]
    )

    if uploaded_file is not None:

        try:

            image = Image.open(uploaded_file)

            st.image(
                image,
                caption="Uploaded Satellite Image",
                use_container_width=True
            )

            st.success(
                "Satellite image loaded successfully."
            )

        except Exception as e:

            st.error(
                f"Unable to process image: {e}"
            )


def display_satellite_panel(
    image_path=None,
    satellite_name="Sample Satellite",
    timestamp="Not available",
    channel="Infrared"
):
    """
    Complete satellite observation panel.
    """

    display_satellite_image(
        image_path=image_path,
        satellite_name=satellite_name,
        timestamp=timestamp,
        channel=channel
    )

    st.divider()

    satellite_upload_section()