import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from svgpathtools import parse_path

st.markdown(
    """
Using an external SVG manipulation library like [svgpathtools](https://github.com/mathandy/svgpathtools)
You can do some interesting things on drawn paths.
In this example we compute the length of any drawn path.
"""
)
with st.echo("below"):
    bg_image = Image.open("img/annotation.jpeg")

    canvas_result = st_canvas(
        stroke_color="yellow",
        stroke_width=3,
        background_image=bg_image,
        height=320,
        width=512,
        drawing_mode="freedraw",
        key="compute_arc_length",
    )
    if (
        canvas_result.json_data is not None
        and len(canvas_result.json_data["objects"]) != 0
    ):
        df = pd.json_normalize(canvas_result.json_data["objects"])
        paths = df["path"].tolist()
        for ind, path in enumerate(paths):
            path = parse_path(" ".join([str(e) for line in path for e in line]))
            st.write(f"Path {ind} has length {path.length():.3f} pixels")
