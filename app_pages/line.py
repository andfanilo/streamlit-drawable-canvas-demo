import pandas as pd
import streamlit as st
from streamlit_drawable_canvas import st_canvas

st.markdown(
    """
Click and drag to draw a straight line from where you press down to wherever
you release the mouse.
"""
)
with st.echo("below"):
    canvas_result = st_canvas(
        stroke_width=3,
        stroke_color="#000000",
        background_color="#eee",
        height=400,
        width=600,
        drawing_mode="line",
        key="line_app",
    )

    if canvas_result.json_data is not None:
        objects = pd.json_normalize(canvas_result.json_data["objects"])
        for col in objects.columns:
            if objects[col].dtype == "object":
                objects[col] = objects[col].astype("str")
        st.dataframe(objects)
