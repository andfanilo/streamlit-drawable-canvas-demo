import json
import math

import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas


def main():
    st.title("Drawable Canvas Demo")
    PAGES = {
        "About": about,
        "Full example": full_app,
        "Get center coords of circles": center_circle_app,
    }
    page = st.sidebar.selectbox("Page:", options=list(PAGES.keys()))
    PAGES[page]()


def about():
    st.markdown(
        """
    Welcome to the demo of [Streamlit Drawable Canvas](https://github.com/andfanilo/streamlit-drawable-canvas).
    
    On this site, you will find a full use case for this Streamlit component, and lots of other smaller tips.
    """
    )
    st.image("./demo.gif")
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
    * Doubleclick to remove the selected object when not in drawing mode
    """
    )

    with st.echo("below"):
        # Specify canvas parameters in application
        stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
        stroke_color = st.sidebar.color_picker("Stroke color hex: ")
        bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")
        bg_image = st.sidebar.file_uploader("Background image:", type=["png", "jpg"])
        drawing_mode = st.sidebar.selectbox(
            "Drawing tool:", ("freedraw", "line", "rect", "circle", "transform")
        )
        realtime_update = st.sidebar.checkbox("Update in realtime", True)

        with open("star_state.json", "r") as f:
            star_state = json.load(f)
            star_state["background"] = bg_color

        # Create a canvas component
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
            stroke_width=stroke_width,
            stroke_color=stroke_color,
            background_color="" if bg_image else bg_color,
            background_image=Image.open(bg_image) if bg_image else None,
            update_streamlit=realtime_update,
            height=150,
            drawing_mode=drawing_mode,
            initial_drawing=star_state
            if st.sidebar.checkbox("Initialize with star")
            else None,
            key="canvas",
        )

        # Do something interesting with the image data and paths
        if canvas_result.image_data is not None:
            st.image(canvas_result.image_data)
        if canvas_result.json_data is not None:
            st.dataframe(pd.json_normalize(canvas_result.json_data["objects"]))


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
    bg_image = Image.open("tennis-balls.jpg")
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.2)",  # Fixed fill color with some opacity
        stroke_width=5,
        stroke_color="black",
        background_image=bg_image,
        height=400,
        width=600,
        drawing_mode="circle",
        key="canvas",
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


if __name__ == "__main__":
    st.set_page_config(
        page_title="Streamlit Drawable Canvas Demo", page_icon=":pencil2:"
    )
    main()
