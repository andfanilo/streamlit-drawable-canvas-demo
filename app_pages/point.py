import pandas as pd
import streamlit as st
from streamlit_drawable_canvas import st_canvas

st.markdown(
    """
Click to drop a point marker, sized by `point_display_radius`. Useful for
marking landmarks or keypoints rather than drawing shapes.
"""
)
with st.echo("below"):
    point_display_radius = st.sidebar.slider("Point display radius: ", 1, 25, 3)

    canvas_result = st_canvas(
        stroke_color="#000000",
        background_color="#eee",
        height=400,
        width=600,
        drawing_mode="point",
        point_display_radius=point_display_radius,
        key="point_app",
    )

    if canvas_result.json_data is not None:
        objects = pd.json_normalize(canvas_result.json_data["objects"])
        for col in objects.columns:
            if objects[col].dtype == "object":
                objects[col] = objects[col].astype("str")
        st.dataframe(objects)
