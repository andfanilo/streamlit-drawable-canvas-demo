import streamlit as st
from streamlit_drawable_canvas import st_canvas

st.markdown(
    """
`image_bytes` returns the canvas's raw PNG bytes, no numpy or Pillow decode
involved. Reach for it when all you want is to hand the file to
`st.download_button` or write it straight to disk.
"""
)
with st.echo("below"):
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=3,
        background_color="#eee",
        height=300,
        width=400,
        drawing_mode="freedraw",
        return_image_data=True,
        key="download_png_bytes_app",
    )

    if canvas_result.image_bytes is not None:
        st.download_button(
            "Download PNG",
            data=canvas_result.image_bytes,
            file_name="canvas.png",
            mime="image/png",
        )
