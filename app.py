import streamlit as st

st.set_page_config(page_title="Streamlit Drawable Canvas Demo", page_icon=":pencil2:")

page = st.navigation(
    {
        "": [
            st.Page("app_pages/about.py", title="About", icon=":material/info:"),
            st.Page(
                "app_pages/basic_example.py",
                title="Basic example",
                icon=":material/dashboard:",
            ),
        ],
        "Drawing tools": [
            st.Page(
                "app_pages/freedraw.py", title="Freedraw", icon=":material/gesture:"
            ),
            st.Page(
                "app_pages/line.py", title="Line", icon=":material/horizontal_rule:"
            ),
            st.Page(
                "app_pages/rect.py", title="Rect", icon=":material/crop_square:"
            ),
            st.Page(
                "app_pages/circle.py",
                title="Circle",
                icon=":material/radio_button_unchecked:",
            ),
            st.Page(
                "app_pages/polygon.py", title="Polygon", icon=":material/pentagon:"
            ),
            st.Page("app_pages/point.py", title="Point", icon=":material/place:"),
            st.Page(
                "app_pages/text.py", title="Text", icon=":material/text_fields:"
            ),
            st.Page(
                "app_pages/labeled_boxes.py",
                title="Labeled boxes",
                icon=":material/label:",
            ),
        ],
        "Editing & canvas": [
            st.Page(
                "app_pages/point_editing.py",
                title="Point editing",
                icon=":material/point_scan:",
            ),
            st.Page(
                "app_pages/scrollable_canvas.py",
                title="Scrollable canvas",
                icon=":material/height:",
            ),
            st.Page(
                "app_pages/disabled_canvas.py",
                title="Disabled (read-only) canvas",
                icon=":material/lock:",
            ),
            st.Page(
                "app_pages/background_image_fit.py",
                title="Background image fit",
                icon=":material/crop:",
            ),
        ],
        "Recipes": [
            st.Page(
                "app_pages/center_circle_coords.py",
                title="Get center coords of circles",
                icon=":material/adjust:",
            ),
            st.Page(
                "app_pages/color_annotation.py",
                title="Color-based image annotation",
                icon=":material/palette:",
            ),
            st.Page(
                "app_pages/form_submit.py",
                title="Update on form submit",
                icon=":material/assignment:",
            ),
            st.Page(
                "app_pages/download_png_bytes.py",
                title="Download PNG (image_bytes)",
                icon=":material/download:",
            ),
            st.Page(
                "app_pages/download_base64_png.py",
                title="Download Base64 encoded PNG",
                icon=":material/download_for_offline:",
            ),
            st.Page(
                "app_pages/arc_length.py",
                title="Compute the length of drawn arcs",
                icon=":material/route:",
            ),
        ],
    },
    position="sidebar",
)

st.title(page.title, icon=page.icon)
page.run()

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
