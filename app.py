import streamlit as st

from app_state import initialize_session_state
from database import initialize_database
from ui_components import ICON_PATH, apply_theme
from workspace_views import (
    render_ai_workspace,
    render_chords_workspace,
    render_lyrics_workspace,
    render_sidebar,
)


# wide page so the side tabs have space
st.set_page_config(
    page_title="GhostWriter",
    page_icon=str(ICON_PATH),
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()
initialize_database()
initialize_session_state()

selected_workspace = render_sidebar()

if selected_workspace == "Ghost":
    render_ai_workspace()
elif selected_workspace == "Lyrics":
    render_lyrics_workspace()
else:
    render_chords_workspace()
