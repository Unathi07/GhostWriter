import streamlit as st

from chord_utils import detect_key


def initialize_session_state():
    # keeping my app stuff here so it does not reset after every click
    defaults = {
        "progression": [],
        "writing_direction": None,
        "writing_direction_context": None,
        "writing_direction_note": None,
        "song_notes": "",
        "song_brief": "",
        "song_title": "Untitled song",
        "current_song_id": None,
        "last_saved_at": None,
        "pending_load_song_id": None,
        "pending_start_new_song": False,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_detected_key():
    # no point checking the key if there are no chords yet
    if not st.session_state.progression:
        return None

    return detect_key(st.session_state.progression)


def get_progression_text():
    if not st.session_state.progression:
        return "No progression yet"

    return " -> ".join(st.session_state.progression)


def get_key_text():
    return get_detected_key() or "No key detected yet"


def load_song_into_session(song):
    # puts a saved song back into the app
    st.session_state.current_song_id = song["id"]
    st.session_state.song_title = song["title"]
    st.session_state.song_brief = song["song_brief"]
    st.session_state.song_notes = song["song_notes"]
    st.session_state.progression = song["progression"]
    st.session_state.writing_direction = song["writing_direction"]
    st.session_state.writing_direction_context = song["writing_direction_context"]
    st.session_state.writing_direction_note = None
    st.session_state.last_saved_at = song["updated_at"]


def start_new_song():
    # clears the current draft without touching saved songs
    st.session_state.current_song_id = None
    st.session_state.song_title = "Untitled song"
    st.session_state.song_brief = ""
    st.session_state.song_notes = ""
    st.session_state.progression = []
    st.session_state.writing_direction = None
    st.session_state.writing_direction_context = None
    st.session_state.writing_direction_note = None
    st.session_state.last_saved_at = None
