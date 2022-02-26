import base64
import json
import os
import re
import time
import uuid
from io import BytesIO
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from svgpathtools import parse_path


def main():
    if "button_id" not in st.session_state:
        st.session_state["button_id"] = ""
    if "color_to_label" not in st.session_state:
        st.session_state["color_to_label"] = {}
    PAGES = {
        "About": about,
        "Basic example": full_app,
        "Get center coords of circles": center_circle_app,
        "Color-based image annotation": color_annotation_app,
        "Download Base64 encoded PNG": png_export,
        "Compute the length of drawn arcs": compute_arc_length,
    }
    page = st.sidebar.selectbox("Page:", options=list(PAGES.keys()))
    PAGES[page]()

    with st.sidebar:
        st.markdown("---")
        st.markdown(
            '<h6>Made in &nbsp<img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit logo" height="16">&nbsp by <a href="https://twitter.com/andfanilo">@andfanilo</a></h6>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div style="margin: 0.75em 0;"><a href="https://www.buymeacoffee.com/andfanilo" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a></div>',
            unsafe_allow_html=True,
        )


def about():
    st.markdown(
        """
    Welcome to the demo of [Streamlit Drawable Canvas](https://github.com/andfanilo/streamlit-drawable-canvas).
    
    On this site, you will find a full use case for this Streamlit component, and answers to some frequently asked questions.
    
    :pencil: [Demo source code](https://github.com/andfanilo/streamlit-drawable-canvas-demo/)    
    """
    )
    st.image("img/demo.gif")
    st.markdown(
        """
    What you can do with Drawable Canvas:

    * Draw freely, lines, circles and boxes on the canvas, with options on stroke & fill
    * Rotate, skew, scale, move any object of the canvas on demand
    * Select a background color or image to draw on
    * Get image data and every drawn object properties back to Streamlit !
    * Choose to fetch back data in realtime or on demand with a button
    * Undo, Redo or Drop canvas
    * Save canvas data as JSON to reuse for another session
    """
    )


def full_app():
    st.sidebar.header("Configuration")
    st.markdown(
        """
    Draw on the canvas, get the drawings back to Streamlit!
    * Configure canvas in the sidebar
    * In transform mode, double-click an object to remove it
    * In polygon mode, left-click to add a point, right-click to close the polygon, double-click to remove the latest point
    """
    )

    with st.echo("below"):
        # Specify canvas parameters in application
        drawing_mode = st.sidebar.selectbox(
            "Drawing tool:",
            ("freedraw", "line", "rect", "circle", "transform", "polygon", "point"),
        )
        stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
        if drawing_mode == 'point':
            point_display_radius = st.sidebar.slider("Point display radius: ", 1, 25, 3)
        stroke_color = st.sidebar.color_picker("Stroke color hex: ")
        bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")
        bg_image = st.sidebar.file_uploader("Background image:", type=["png", "jpg"])
        realtime_update = st.sidebar.checkbox("Update in realtime", True)

        # Create a canvas component
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
            stroke_width=stroke_width,
            stroke_color=stroke_color,
            background_color=bg_color,
            background_image=Image.open(bg_image) if bg_image else None,
            update_streamlit=realtime_update,
            height=150,
            drawing_mode=drawing_mode,
            point_display_radius=point_display_radius if drawing_mode == 'point' else 0,
            display_toolbar=st.sidebar.checkbox("Display toolbar", True),
            key="full_app",
        )

        # Do something interesting with the image data and paths
        if canvas_result.image_data is not None:
            st.image(canvas_result.image_data)
        if canvas_result.json_data is not None:
            objects = pd.json_normalize(canvas_result.json_data["objects"])
            for col in objects.select_dtypes(include=["object"]).columns:
                objects[col] = objects[col].astype("str")
            st.dataframe(objects)


def center_circle_app():
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
            if len(df) == 0:
                return
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


def color_annotation_app():
    st.markdown(
        """
    Drawable Canvas doesn't provided out-of-the-box image annotation capabilities, but we can hack something with session state,
    by mapping a drawing fill color to a label.

    Annotate pedestrians, cars and traffic lights with this one, with any color/label you want 
    (though in a real app you should rather provide your own label and fills :smile:).

    If you really want advanced image annotation capabilities, you'd better check [Streamlit Label Studio](https://discuss.streamlit.io/t/new-component-streamlit-labelstudio-allows-you-to-embed-the-label-studio-annotation-frontend-into-your-application/9524)
    """
    )
    with st.echo("below"):
        bg_image = Image.open("img/annotation.jpeg")
        label_color = (
            st.sidebar.color_picker("Annotation color: ", "#EA1010") + "77"
        )  # for alpha from 00 to FF
        label = st.sidebar.text_input("Label", "Default")
        mode = "transform" if st.sidebar.checkbox("Move ROIs", False) else "rect"

        canvas_result = st_canvas(
            fill_color=label_color,
            stroke_width=3,
            background_image=bg_image,
            height=320,
            width=512,
            drawing_mode=mode,
            key="color_annotation_app",
        )
        if canvas_result.json_data is not None:
            df = pd.json_normalize(canvas_result.json_data["objects"])
            if len(df) == 0:
                return
            st.session_state["color_to_label"][label_color] = label
            df["label"] = df["fill"].map(st.session_state["color_to_label"])
            st.dataframe(df[["top", "left", "width", "height", "fill", "label"]])

        with st.expander("Color to label mapping"):
            st.json(st.session_state["color_to_label"])


def png_export():
    st.markdown(
        """
    Realtime update is disabled for this demo. 
    Press the 'Download' button at the bottom of canvas to update exported image.
    """
    )
    try:
        Path("tmp/").mkdir()
    except FileExistsError:
        pass

    # Regular deletion of tmp files
    # Hopefully callback makes this better
    now = time.time()
    N_HOURS_BEFORE_DELETION = 1
    for f in Path("tmp/").glob("*.png"):
        st.write(f, os.stat(f).st_mtime, now)
        if os.stat(f).st_mtime < now - N_HOURS_BEFORE_DELETION * 3600:
            Path.unlink(f)

    if st.session_state["button_id"] == "":
        st.session_state["button_id"] = re.sub(
            "\d+", "", str(uuid.uuid4()).replace("-", "")
        )

    button_id = st.session_state["button_id"]
    file_path = f"tmp/{button_id}.png"

    custom_css = f""" 
        <style>
            #{button_id} {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                background-color: rgb(255, 255, 255);
                color: rgb(38, 39, 48);
                padding: .25rem .75rem;
                position: relative;
                text-decoration: none;
                border-radius: 4px;
                border-width: 1px;
                border-style: solid;
                border-color: rgb(230, 234, 241);
                border-image: initial;
            }} 
            #{button_id}:hover {{
                border-color: rgb(246, 51, 102);
                color: rgb(246, 51, 102);
            }}
            #{button_id}:active {{
                box-shadow: none;
                background-color: rgb(246, 51, 102);
                color: white;
                }}
        </style> """

    data = st_canvas(update_streamlit=False, key="png_export")
    if data is not None and data.image_data is not None:
        img_data = data.image_data
        im = Image.fromarray(img_data.astype("uint8"), mode="RGBA")
        im.save(file_path, "PNG")

        buffered = BytesIO()
        im.save(buffered, format="PNG")
        img_data = buffered.getvalue()
        try:
            # some strings <-> bytes conversions necessary here
            b64 = base64.b64encode(img_data.encode()).decode()
        except AttributeError:
            b64 = base64.b64encode(img_data).decode()

        dl_link = (
            custom_css
            + f'<a download="{file_path}" id="{button_id}" href="data:file/txt;base64,{b64}">Export PNG</a><br></br>'
        )
        st.markdown(dl_link, unsafe_allow_html=True)


def compute_arc_length():
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


if __name__ == "__main__":
    st.set_page_config(
        page_title="Streamlit Drawable Canvas Demo", page_icon=":pencil2:"
    )
    st.title("Drawable Canvas Demo")
    st.sidebar.subheader("Configuration")
    main()
