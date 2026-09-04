import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas

st.markdown(
    """
Draw boxes labeled with whatever class is currently selected below. Boxes
already on the canvas keep the label they were drawn with, even if you switch
the class afterward. Turn on the toolbar's pencil icon, select a box, then
click it again to relabel it.

If you need a class palette, keyboard shortcuts, or a box-list panel, check
[Streamlit Label Studio](https://discuss.streamlit.io/t/new-component-streamlit-labelstudio-allows-you-to-embed-the-label-studio-annotation-frontend-into-your-application/9524)
instead. This component only gives you the drawing and labeling gesture.
"""
)
with st.echo("below"):
    bg_image = Image.open("img/annotation.jpeg")

    label_source = st.sidebar.radio(
        "Label source:", ("Fixed class list", "Free-form")
    )
    if label_source == "Fixed class list":
        label = st.sidebar.selectbox(
            "Class:", ("pedestrian", "car", "traffic light")
        )
    else:
        label = st.sidebar.text_input("Label:", "pedestrian")

    fill_hex = st.sidebar.color_picker("Fill color: ", "#FFA500")
    fill_opacity = st.sidebar.slider("Fill opacity: ", 0.0, 1.0, 0.0)
    stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
    stroke_color = st.sidebar.color_picker("Box color: ", "#EA1010")
    font_size = st.sidebar.slider("Chip font size: ", 8, 40, 20)

    r, g, b = (int(fill_hex[i : i + 2], 16) for i in (1, 3, 5))
    fill_color = f"rgba({r}, {g}, {b}, {fill_opacity})"

    canvas_result = st_canvas(
        fill_color=fill_color,
        stroke_color=stroke_color,
        stroke_width=stroke_width,
        background_image=bg_image,
        height=320,
        width=512,
        drawing_mode="labeled_rect",
        label=label,
        font_size=font_size,
        key="labeled_boxes_app",
    )

    st.dataframe(pd.DataFrame(canvas_result.boxes))

    if canvas_result.boxes_in_image_space is not None:
        with st.expander("Boxes in the source image's own pixels"):
            st.dataframe(pd.DataFrame(canvas_result.boxes_in_image_space))
