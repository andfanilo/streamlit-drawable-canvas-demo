import pandas as pd
import streamlit as st
from streamlit_drawable_canvas import st_canvas

SCROLLABLE_CANVAS_SEED = {
    "objects": [
        {
            "type": "rect",
            "left": 50,
            "top": 900,
            "width": 200,
            "height": 100,
            "fill": "rgba(255, 165, 0, 0.3)",
            "stroke": "#000000",
            "strokeWidth": 3,
        },
        {
            "type": "rect",
            "left": 1550,
            "top": 50,
            "width": 200,
            "height": 100,
            "fill": "rgba(0, 165, 255, 0.3)",
            "stroke": "#000000",
            "strokeWidth": 3,
        },
    ]
}

st.markdown(
    """
`max_display_height` caps the canvas's displayed height and scrolls it vertically
inside that box instead of pushing the rest of the page down. Horizontal scrolling
needs no parameter at all: it's always on for a canvas wider than the space
Streamlit gives it. This canvas is both taller and wider than its display box, with
one seeded box near the bottom and another off to the right; scroll in both
directions to find them.
"""
)
with st.echo("below"):
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=3,
        stroke_color="#000000",
        background_color="#eee",
        height=1200,
        width=1800,
        max_display_height=400,
        initial_drawing=SCROLLABLE_CANVAS_SEED,
        drawing_mode="rect",
        key="scrollable_canvas_app",
    )

    if canvas_result.json_data is not None:
        objects = pd.json_normalize(canvas_result.json_data["objects"])
        for col in objects.columns:
            if objects[col].dtype == "object":
                objects[col] = objects[col].astype("str")
        st.dataframe(objects)
