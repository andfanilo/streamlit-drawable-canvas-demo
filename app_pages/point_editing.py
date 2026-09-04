import pandas as pd
import streamlit as st
from streamlit_drawable_canvas import st_canvas

st.markdown(
    """
Draw a few shapes below, then turn on the toolbar's pencil icon and select one.
That moves, scales or rotates it as a whole. Click it again, a second and separate
click, to edit its individual points instead: drag a polygon vertex, a line
endpoint, or a circle's rim. Dragging a rect's corner turns it into a polygon
first, since a rect has no corner that can move on its own.
"""
)
with st.echo("below"):
    drawing_mode = st.sidebar.selectbox(
        "Drawing tool:", ("rect", "line", "circle", "polygon")
    )

    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=3,
        stroke_color="#000000",
        background_color="#eee",
        height=400,
        width=600,
        drawing_mode=drawing_mode,
        key="point_edit_app",
    )

    if canvas_result.json_data is not None:
        objects = pd.json_normalize(canvas_result.json_data["objects"])
        for col in objects.columns:
            if objects[col].dtype == "object":
                objects[col] = objects[col].astype("str")
        st.dataframe(objects)
