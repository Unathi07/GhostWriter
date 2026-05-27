import streamlit as st
from piano import render_piano
from chord_utils import get_chord_name, detect_key

# Music options used by the progression builder.
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

st.title("GhostWriter")
st.subheader("The pen behind your sound")

# Main workflow: build the music first, then use it as context for writing.
music_tab, writing_tab = st.tabs(["Music", "Writing"])

with music_tab:
    st.subheader("Make the sounds in your head ideas")
    progression_tab, suggestions_tab = st.tabs(
        ["Progression", "Suggestions"]
    )

    # Streamlit reruns this file after interactions, so progression must persist in session state.
    if "progression" not in st.session_state:
        st.session_state.progression = []

    with progression_tab:
        # Progression builder: stores chords in order and analyzes the current key.
        st.header("Progression")
        root_note = st.selectbox(
            "Select a root note",
            root_notes,
            key="progression_root_note",
        )
        st.write("You selected:", root_note)
        chord_type = st.selectbox(
            "Select a chord type",
            chord_types,
            key="progression_chord_type",
        )
        selected_chord, revised_notes = get_chord_name(root_note, chord_type, type_map)
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
    if st.session_state.get("progression"):
        st.write("Current progression:", " -> ".join(st.session_state.progression))
        detected_key = detect_key(st.session_state.progression, type_map)
        st.write("Detected key:", detected_key)
    else:
        st.write("Build a progression in the Music tab to connect your writing to the song.")

    # Writing will use the music tab's progression/key as context for lyric ideas.
    st.subheader("Turn your ideas into lyrics")
    lyric_tab, brainstorm_tab, inspiration_tab = st.tabs(
        ["Lyrics", "Brainstorm", "Inspiration"]
    )

    with lyric_tab:
        st.header("Lyrics")
        # A simple scratchpad
        st.text_area(
            "Song notes",
            placeholder="Write lyric ideas, hooks, themes, or rough lines here...",
            height=220,
            key="song_notes",
        )

    with brainstorm_tab:
        st.header("Brainstorm")
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
                st.warning("Build a progression in the Music tab first.")
            else:
                current_progression = " -> ".join(st.session_state.progression)
                detected_key = detect_key(st.session_state.progression, type_map)

                st.subheader("Writing direction")
                st.write("Song brief:", song_brief)
                st.write("Progression:", current_progression)
                st.write("Detected key:", detected_key)

                # Template-based guidance for now; this section can later be replaced by an AI response.
                st.write("Core idea:", f"Build the song around: {song_brief}")
                st.write(
                    "Hook angle:",
                    "Focus the chorus on one simple emotional truth the listener can repeat.",
                )
                st.write(
                    "Verse scene:",
                    "Start with a specific moment, place, or memory instead of explaining the whole feeling.",
                )
                st.write(
                    "Questions to explore:",
                    [
                        "What does the singer want but cannot say directly?",
                        "What small detail makes the emotion feel real?",
                        "What changes between the first verse and the final chorus?",
                    ],
                )
                # Connects the writing prompt back to the harmonic context from the Music tab.
                st.write(
                    "Starter line:",
                    f"In {detected_key}, let the progression {current_progression} carry a feeling of honesty and movement.",
                )

    with inspiration_tab:
        st.header("Inspiration")
