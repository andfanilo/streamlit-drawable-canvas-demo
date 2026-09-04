import streamlit as st
from streamlit_drawable_canvas import st_canvas

DISABLED_CANVAS_SEED = {
    "objects": [
        {
            "type": "rect",
            "left": 40,
            "top": 40,
            "width": 120,
            "height": 80,
            "fill": "rgba(255, 165, 0, 0.3)",
            "stroke": "#000000",
            "strokeWidth": 3,
        },
        {
            "type": "circle",
            "left": 220,
            "top": 60,
            "radius": 50,
            "fill": "rgba(0, 165, 255, 0.3)",
            "stroke": "#000000",
            "strokeWidth": 3,
        },
    ]
}

st.markdown(
    """
`disabled=True` makes a canvas read-only: no drawing, no selection, no toolbar.
Feed it a previous drawing through `initial_drawing` to show a result without
letting anyone touch it.
"""
)
with st.echo("below"):
    st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=3,
        background_color="#eee",
        height=250,
        width=400,
        initial_drawing=DISABLED_CANVAS_SEED,
        disabled=True,
        key="disabled_canvas_app",
    )
