import streamlit as st
from streamlit_drawable_canvas import st_canvas

st.markdown(
    """
Reach for `st.form` when you only want the finished drawing, not every stroke.
The canvas keeps `update_streamlit=True` and records every stroke as usual, but
the form holds the rerun back until you press Submit. No toolbar button needed,
and the canvas never submits the form on its own.
"""
)
with st.echo("below"):
    with st.form("drawing_form"):
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",
            stroke_width=3,
            background_color="#eee",
            height=300,
            width=600,
            drawing_mode="freedraw",
            key="form_batching_app",
        )
        submitted = st.form_submit_button("Submit")

    if submitted and canvas_result.json_data is not None:
        st.write(f"Submitted {len(canvas_result.json_data['objects'])} object(s).")
