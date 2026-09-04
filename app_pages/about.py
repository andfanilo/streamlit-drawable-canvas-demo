import streamlit as st

st.markdown(
    """
Welcome to the demo of [Streamlit Drawable Canvas](https://github.com/andfanilo/streamlit-drawable-canvas).

On this site, you will find a full use case for this Streamlit component, and answers to some frequently asked questions.

:pencil2: [Demo source code](https://github.com/andfanilo/streamlit-drawable-canvas-demo/)
"""
)
st.image("img/demo.gif")
st.markdown(
    """
What you can do with Drawable Canvas:

* Draw freely, lines, circles, boxes, polygons and text on the canvas, with options on stroke & fill
* Turn on the toolbar's pencil icon to rotate, skew, scale or move any object on demand
* Click a shape a second time to edit its individual points instead of the whole thing
* Select a background color or image to draw on
* Get image data and every drawn object properties back to Streamlit !
* Choose to fetch back data in realtime or on demand with a button
* Undo, Redo or Drop canvas
* Save canvas data as JSON to reuse for another session
"""
)
