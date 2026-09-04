import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas

st.markdown(
    """
`background_image_fit` controls how a background image that doesn't match the
canvas's aspect ratio gets scaled. `"stretch"`, the default, fills the canvas
exactly and distorts the image if the ratios differ. `"contain"` scales the image
down to fit without cropping or distorting it, leaving empty canvas on the sides.
"""
)
with st.echo("below"):
    fit = st.sidebar.selectbox("background_image_fit", ("stretch", "contain"))
    bg_image = Image.open("img/tennis-balls.jpg")

    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=3,
        background_image=bg_image,
        background_image_fit=fit,
        height=300,
        width=600,
        drawing_mode="rect",
        key="background_image_fit_app",
    )

    if canvas_result.json_data is not None:
        objects = pd.json_normalize(canvas_result.json_data["objects"])
        for col in objects.columns:
            if objects[col].dtype == "object":
                objects[col] = objects[col].astype("str")
        st.dataframe(objects)
