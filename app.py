import streamlit as st

from src.ui import run_ui


st.set_page_config(

    page_title="AI Fake News Detection",

    page_icon="📰",

    layout="wide",

    initial_sidebar_state="collapsed"

)

run_ui()