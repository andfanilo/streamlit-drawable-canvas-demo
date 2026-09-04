import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas

st.markdown(
    """
Drawable Canvas doesn't provided out-of-the-box image annotation capabilities, but we can hack something with session state,
by mapping a drawing fill color to a label.

Annotate pedestrians, cars and traffic lights with this one, with any color/label you want
(though in a real app you should rather provide your own label and fills :smile:).

Draw a box below, then click the canvas toolbar's pencil icon to select and move
an existing box around instead of drawing a new one.

If you really want advanced image annotation capabilities, you'd better check [Streamlit Label Studio](https://discuss.streamlit.io/t/new-component-streamlit-labelstudio-allows-you-to-embed-the-label-studio-annotation-frontend-into-your-application/9524)
"""
)
with st.echo("below"):
    bg_image = Image.open("img/annotation.jpeg")
    label_color = (
        st.sidebar.color_picker("Annotation color: ", "#EA1010") + "77"
    )  # for alpha from 00 to FF
    label = st.sidebar.text_input("Label", "Default")

    canvas_result = st_canvas(
        fill_color=label_color,
        stroke_width=3,
        background_image=bg_image,
        height=320,
        width=512,
        drawing_mode="rect",
        key="color_annotation_app",
    )
    if canvas_result.json_data is not None:
        df = pd.json_normalize(canvas_result.json_data["objects"])
        if len(df) != 0:
            st.session_state["color_to_label"][label_color] = label
            df["label"] = df["fill"].map(st.session_state["color_to_label"])
            st.dataframe(df[["top", "left", "width", "height", "fill", "label"]])

    with st.expander("Color to label mapping"):
        st.json(st.session_state["color_to_label"])
