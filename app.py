import streamlit as st
from piano import render_piano
from chord_utils import get_chord_name, detect_key, suggest_diatonic_chords
from music_config import ROOT_NOTES, CHORD_TYPES
from writing_utils import build_writing_direction

st.title("GhostWriter")
st.subheader("The pen behind your sound")

# Streamlit reruns this file after interactions, so progression must persist in session state.
if "progression" not in st.session_state:
    st.session_state.progression = []

# Progression builder: stores chords in order and analyzes the current key.
st.header("Progression Builder")
root_note = st.selectbox(
    "Select a root note",
    ROOT_NOTES,
    key="progression_root_note",
)
st.write("You selected:", root_note)

chord_type = st.selectbox(
    "Select a chord type",
    CHORD_TYPES,
    key="progression_chord_type",
)
selected_chord, revised_notes = get_chord_name(root_note, chord_type)
st.write("Chord:", selected_chord)
st.write("Notes:", revised_notes)
st.components.v1.html(render_piano(revised_notes, autoplay=True), height=300)

if st.button("Add chord", key="add_progression_chord"):
    st.session_state.progression.append(selected_chord)
    st.rerun()

st.subheader("Current progression")
if st.session_state.progression:
    progression_options = [
        f"{index + 1}. {chord}"
        for index, chord in enumerate(st.session_state.progression)
    ]
    current_progression = " -> ".join(st.session_state.progression)
    detected_key = detect_key(st.session_state.progression)

    st.write("Progression:", current_progression)
    st.write("Key:", detected_key)

    suggested_chords = suggest_diatonic_chords(detected_key)

    if suggested_chords:
        st.write("Suggested chords:", " -> ".join(suggested_chords))

    selected_to_remove = st.multiselect(
        "Select chord(s) to remove",
        progression_options,
        key="progression_remove_selection",
    )

    if st.button(
        "Remove selected chord(s)",
        key="remove_progression_chords",
        disabled=not selected_to_remove,
    ):
        selected_indices = {
            progression_options.index(option) for option in selected_to_remove
        }
        st.session_state.progression = [
            chord
            for index, chord in enumerate(st.session_state.progression)
            if index not in selected_indices
        ]
        st.rerun()

    if st.button("Clear progression", key="clear_progression"):
        st.session_state.progression = []
        st.rerun()
else:
    st.write("Your progression is empty.")

st.divider()

# Writing direction uses the progression/key as context for lyric ideas.
st.header("Writing Direction")
if st.session_state.get("progression"):
    st.write("Current progression:", " -> ".join(st.session_state.progression))
    st.write("Detected key:", detect_key(st.session_state.progression))
else:
    st.write("Build a progression first to connect your writing to the song.")

# User describes the feeling, story, mood, or situation behind the song.
song_brief = st.text_area(
    "Song idea",
    placeholder="Describe the feeling, story, mood, or situation behind the song...",
    height=160,
    key="song_brief",
)

# Builds a writing direction from the user's song idea and progression.
if st.button("Build writing direction", key="build_writing_direction"):
    if not song_brief:
        st.warning("Add a song brief first.")
    elif not st.session_state.get("progression"):
        st.warning("Build a progression first.")
    else:
        current_progression = " -> ".join(st.session_state.progression)
        detected_key = detect_key(st.session_state.progression)

        st.subheader("Writing direction")
        direction = build_writing_direction(
            song_brief,
            detected_key,
            current_progression,
        )

        # Template-based guidance for now; this section can later be replaced by an AI response.
        for section, content in direction.items():
            st.write(section + ":", content)

st.divider()

st.header("Lyrics Scratchpad")
st.text_area(
    "Song notes",
    placeholder="Write lyric ideas, hooks, themes, or rough lines here...",
    height=220,
    key="song_notes",
)
