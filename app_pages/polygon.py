import pandas as pd
import streamlit as st
from streamlit_drawable_canvas import st_canvas

st.markdown(
    """
Click to add a vertex; every vertex shows a handle. Click the first vertex's
handle to close the shape (needs at least three vertices), or click any other
handle to remove that vertex.
"""
)
with st.echo("below"):
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=3,
        stroke_color="#000000",
        background_color="#eee",
        height=400,
        width=600,
        drawing_mode="polygon",
        key="polygon_app",
    )

    if canvas_result.json_data is not None:
        objects = pd.json_normalize(canvas_result.json_data["objects"])
        for col in objects.columns:
            if objects[col].dtype == "object":
                objects[col] = objects[col].astype("str")
        st.dataframe(objects)
