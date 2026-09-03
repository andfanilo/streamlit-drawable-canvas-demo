# Streamlit - Drawable Canvas - Demo

Streamlit Drawable Canvas demo on Streamlit Sharing

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/andfanilo/streamlit-drawable-canvas-demo/master/app.py)

## Run it locally

Dependencies are managed with [uv](https://docs.astral.sh/uv/):

```sh
uv sync
uv run streamlit run app.py
```

`uv.lock` is the dependency file Streamlit Community Cloud reads, so commit it
whenever `pyproject.toml` changes:

```sh
uv lock
```
