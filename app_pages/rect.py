import pandas as pd
import streamlit as st
from streamlit_drawable_canvas import st_canvas

st.markdown(
    """
Click and drag to draw a rectangle from one corner to the opposite corner.
"""
)
with st.echo("below"):
    fill_hex = st.sidebar.color_picker("Fill color: ", "#FFA500")
    fill_opacity = st.sidebar.slider("Fill opacity: ", 0.0, 1.0, 0.3)
    stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
    stroke_color = st.sidebar.color_picker("Stroke color: ", "#000000")
    background_color = st.sidebar.color_picker("Background color: ", "#eeeeee")

    r, g, b = (int(fill_hex[i : i + 2], 16) for i in (1, 3, 5))
    fill_color = f"rgba({r}, {g}, {b}, {fill_opacity})"

    canvas_result = st_canvas(
        fill_color=fill_color,
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=background_color,
        height=400,
        width=600,
        drawing_mode="rect",
        key="rect_app",
    )

    if canvas_result.json_data is not None:
        objects = pd.json_normalize(canvas_result.json_data["objects"])
        for col in objects.columns:
            if objects[col].dtype == "object":
                objects[col] = objects[col].astype("str")
        st.dataframe(objects)
