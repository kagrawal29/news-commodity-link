"""
Commodity News x Price Correlation Dashboard
=============================================
Entry point.  Run with::

    streamlit run app.py
"""

import streamlit as st

# ---- Page config (must be first Streamlit call) ----
st.set_page_config(
    page_title="Commodity Pulse",
    page_icon="\U0001f4c8",
    layout="wide",
    initial_sidebar_state="expanded",
)

from dashboard.layout import render_dashboard  # noqa: E402

render_dashboard()
