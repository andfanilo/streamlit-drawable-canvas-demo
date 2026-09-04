import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas

st.markdown(
    """
Draw boxes labeled with whatever class is currently selected below. Switch the
class between boxes -- boxes already on the canvas keep the label they were
drawn with. Turn on the toolbar's pencil icon, select a box, then click it
again to relabel it.

If you need a class palette, keyboard shortcuts, or a box-list panel, check
[Streamlit Label Studio](https://discuss.streamlit.io/t/new-component-streamlit-labelstudio-allows-you-to-embed-the-label-studio-annotation-frontend-into-your-application/9524)
instead -- this component only gives you the drawing and labeling gesture.
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

    stroke_color = st.sidebar.color_picker("Box color: ", "#EA1010")

    canvas_result = st_canvas(
        stroke_color=stroke_color,
        stroke_width=3,
        background_image=bg_image,
        height=320,
        width=512,
        drawing_mode="labeled_rect",
        label=label,
        key="labeled_boxes_app",
    )

    st.dataframe(pd.DataFrame(canvas_result.boxes))

    if canvas_result.boxes_in_image_space is not None:
        with st.expander("Boxes in the source image's own pixels"):
            st.dataframe(pd.DataFrame(canvas_result.boxes_in_image_space))
