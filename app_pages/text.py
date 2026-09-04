import pandas as pd
import streamlit as st
from streamlit_drawable_canvas import st_canvas

st.markdown(
    """
Click the canvas to place a text object and start typing right away. Click
elsewhere, or press Escape, to finish. Nothing is sent to Streamlit until then,
so one undo removes the whole text object, not one keystroke.
"""
)
with st.echo("below"):
    font_size = st.sidebar.slider("Font size: ", 8, 72, 24)
    stroke_color = st.sidebar.color_picker("Text color: ", "#000000")

    canvas_result = st_canvas(
        stroke_color=stroke_color,
        background_color="#eee",
        height=300,
        width=600,
        drawing_mode="text",
        font_size=font_size,
        key="text_app",
    )

    if canvas_result.json_data is not None:
        objects = pd.json_normalize(canvas_result.json_data["objects"])
        for col in objects.columns:
            if objects[col].dtype == "object":
                objects[col] = objects[col].astype("str")
        st.dataframe(objects)
