#Import libraries
import streamlit as st
from piano import render_piano
from chord_utils import get_chord_name, detect_key

#Title of the App
st.title("GhostWriter")
st.subheader("The pen behind your sound")

#Top-level sections
music_tab, writing_tab = st.tabs(["Music", "Writing"])

with music_tab:
    st.subheader("Make the sounds in your head ideas")
    options = st.multiselect(
        "What instrument(s) are you using?",
        ["Guitar", "Keys", "Bass Guitar", "Drums", "Strings"],
        default=["Keys", "Bass Guitar", "Drums"],
    )
    st.write("You selected:", options)
    chord_tab, progression_tab, suggestions_tab = st.tabs(
        ["Chords", "Progression", "Suggestions"]
    )

    type_map = {
        "Major": "",
        "Minor": "m",
        "7th": "7",
        "Major 7th": "maj7",
        "Minor 7th": "min7",
        "Suspended": "sus",
        "Diminished": "dim",
        "9th": "9",
        "Major 9th": "maj9",
        "Minor 9th": "min9",
        "Add9": "add9",
    }
    chord_types = (
        "Major",
        "Minor",
        "7th",
        "Major 7th",
        "Minor 7th",
        "Suspended",
        "Diminished",
        "9th",
        "Major 9th",
        "Minor 9th",
        "Add9",
    )
    root_notes = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")

    if "progression" not in st.session_state:
        st.session_state.progression = []

    with chord_tab:
        st.header("Chords")
        root_note = st.selectbox(
            "Select a root note",
            root_notes,
            key="root_note",
        )
        st.write("You selected:", root_note)
        chord_type = st.selectbox(
            "Select a chord type",
            chord_types,
            key="chord_type",
        )
        selected_chord, revised_notes = get_chord_name(root_note, chord_type, type_map)
        st.write("Chord:", selected_chord)
        st.write("Notes:", revised_notes)
        st.components.v1.html(render_piano(revised_notes), height=300)

    with progression_tab:
        st.header("Progression")
        root_note2 = st.selectbox(
            "Select a root note",
            root_notes,
            key="progression_root_note",
        )
        st.write("You selected:", root_note2)
        chord_type2 = st.selectbox(
            "Select a chord type",
            chord_types,
            key="progression_chord_type",
        )
        selected_chord2, revised_notes2 = get_chord_name(root_note2, chord_type2, type_map)
        st.write("Chord:", selected_chord2)
        st.write("Notes:", revised_notes2)
        st.components.v1.html(render_piano(revised_notes2, autoplay=True), height=300)

        if st.button("Add chord", key="add_progression_chord"):
            st.session_state.progression.append(selected_chord2)
            st.rerun()

        st.subheader("Current progression")
        if st.session_state.progression:
            progression_options = [
                f"{index + 1}. {chord}"
                for index, chord in enumerate(st.session_state.progression)
            ]
            st.write("Progression:", " -> ".join(st.session_state.progression))
            detect = detect_key(st.session_state.progression, type_map)
            st.write("Key: ", detect)
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

    with suggestions_tab:
        st.header("Suggestions")

with writing_tab:
    st.subheader("Turn your ideas into lyrics")
    lyric_tab, brainstorm_tab, inspiration_tab = st.tabs(
        ["Lyrics", "Brainstorm", "Inspiration"]
    )

    with lyric_tab:
        st.header("Lyrics")
    with brainstorm_tab:
        st.header("Brainstorm")
    with inspiration_tab:
        st.header("Inspiration")
