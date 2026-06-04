import streamlit as st

from app_state import initialize_session_state
from ui_components import apply_theme
from workspace_views import (
    render_ai_workspace,
    render_chords_workspace,
    render_lyrics_workspace,
    render_sidebar,
)


# wide page so the side tabs have space
st.set_page_config(
    page_title="GhostWriter",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()
initialize_session_state()

selected_workspace = render_sidebar()

if selected_workspace == "AI":
    render_ai_workspace()
elif selected_workspace == "Lyrics":
    render_lyrics_workspace()
else:
    render_chords_workspace()
