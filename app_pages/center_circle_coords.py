import json

import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas

st.markdown(
    """
Computation of center coordinates for circle drawings some understanding of Fabric.js coordinate system
and play with some trigonometry.

Coordinates are canvas-related to top-left of image, increasing x going down and y going right.

```
center_x = left + radius * cos(angle * pi / 180)
center_y = top + radius * sin(angle * pi / 180)
```
"""
)
bg_image = Image.open("img/tennis-balls.jpg")

with open("saved_state.json", "r") as f:
    saved_state = json.load(f)

canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.2)",  # Fixed fill color with some opacity
    stroke_width=5,
    stroke_color="black",
    background_image=bg_image,
    initial_drawing=saved_state
    if st.sidebar.checkbox("Initialize with saved state", False)
    else None,
    height=400,
    width=600,
    drawing_mode="circle",
    key="center_circle_app",
)
with st.echo("below"):
    if canvas_result.json_data is not None:
        df = pd.json_normalize(canvas_result.json_data["objects"])
        if len(df) != 0:
            df["center_x"] = df["left"] + df["radius"] * np.cos(
                df["angle"] * np.pi / 180
            )
            df["center_y"] = df["top"] + df["radius"] * np.sin(
                df["angle"] * np.pi / 180
            )

            st.subheader("List of circle drawings")
            for _, row in df.iterrows():
                st.markdown(
                    f'Center coords: ({row["center_x"]:.2f}, {row["center_y"]:.2f}). Radius: {row["radius"]:.2f}'
                )
