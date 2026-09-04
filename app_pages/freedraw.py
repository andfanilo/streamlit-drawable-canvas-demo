import pandas as pd
import streamlit as st
from streamlit_drawable_canvas import st_canvas

st.markdown(
    """
Click and drag to draw freehand strokes, same as a pencil. Each stroke becomes
one object; every point the mouse passes through while held down gets recorded
in that object's path.
"""
)
with st.echo("below"):
    stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
    stroke_color = st.sidebar.color_picker("Stroke color: ", "#000000")
    background_color = st.sidebar.color_picker("Background color: ", "#eeeeee")

    canvas_result = st_canvas(
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=background_color,
        height=400,
        width=600,
        drawing_mode="freedraw",
        key="freedraw_app",
    )

    if canvas_result.json_data is not None:
        objects = pd.json_normalize(canvas_result.json_data["objects"])
        for col in objects.columns:
            if objects[col].dtype == "object":
                objects[col] = objects[col].astype("str")
        st.dataframe(objects)
