import streamlit as st
from piano import render_piano
from chord_utils import get_chord_name, detect_key, suggest_diatonic_chords
from music_config import ROOT_NOTES, CHORD_TYPES, KEY_OPTIONS, PRESET_PROGRESSIONS
from writing_utils import build_writing_direction


def show_progression_chords(progression):
    # Shows the progression as small numbered blocks instead of one long sentence.
    chord_columns = st.columns(4)

    for index, chord_name in enumerate(progression):
        with chord_columns[index % 4]:
            with st.container(border=True):
                st.markdown(f"**{index + 1}. {chord_name}**")


def show_add_chord_buttons(chords, key_prefix):
    # Adds a row of quick-add buttons for suggested or key-based chords.
    chord_columns = st.columns(4)

    for index, chord_name in enumerate(chords):
        # Streamlit needs each button to have a unique key.
        button_key = f"{key_prefix}_{index}_{chord_name}"

        with chord_columns[index % 4]:
            if st.button(chord_name, key=button_key):
                st.session_state.progression.append(chord_name)
                st.rerun()


st.title("GhostWriter")
st.subheader("The pen behind your sound")

# Streamlit reruns this file after interactions, so progression must persist in session state.
if "progression" not in st.session_state:
    st.session_state.progression = []

# Progression builder: stores chords in order and analyzes the current key.
st.header("Progression Builder")

builder_column, progression_column = st.columns([1, 1])

with builder_column:
    simple_tab, advanced_tab = st.tabs(["Simple", "Advanced"])

    with simple_tab:
        # Starting key suggestions help the user begin before a progression exists.
        st.subheader("Start with a key")
        starting_key = st.selectbox(
            "Choose a starting key",
            KEY_OPTIONS,
            key="starting_key",
        )
        starting_key_chords = suggest_diatonic_chords(starting_key)
        show_add_chord_buttons(starting_key_chords, "starting_key_chord")

        # Presets give users a fast starting point they can still edit afterward.
        st.subheader("Start with a preset")
        preset_name = st.selectbox(
            "Choose a progression style",
            tuple(PRESET_PROGRESSIONS.keys()),
            key="preset_progression",
        )
        preset_progression = PRESET_PROGRESSIONS[preset_name]
        st.write("Preset:", " -> ".join(preset_progression))

        if st.button("Use preset", key="use_preset_progression"):
            st.session_state.progression = preset_progression.copy()
            st.rerun()

    with advanced_tab:
        # Manual chord selection is useful for chords outside the suggested options.
        st.subheader("Manual chord builder")
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

        if st.button("Add chord", key="add_progression_chord"):
            st.session_state.progression.append(selected_chord)
            st.rerun()

        st.components.v1.html(render_piano(revised_notes, autoplay=True), height=300)

        st.subheader("Edit progression")
        if st.session_state.progression:
            progression_options = [
                f"{index + 1}. {chord}"
                for index, chord in enumerate(st.session_state.progression)
            ]
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
        else:
            st.write("Add chords before using advanced editing.")

with progression_column:
    st.subheader("Current progression")
    if st.session_state.progression:
        detected_key = detect_key(st.session_state.progression)

        st.write("Progression")
        show_progression_chords(st.session_state.progression)
        st.write("Key:", detected_key)

        undo_column, clear_column = st.columns(2)

        with undo_column:
            if st.button("Undo last chord", key="undo_last_chord"):
                st.session_state.progression.pop()
                st.rerun()

        with clear_column:
            if st.button("Clear progression", key="clear_progression"):
                st.session_state.progression = []
                st.rerun()

        # Uses the detected key to suggest complementary chords.
        suggested_chords = suggest_diatonic_chords(detected_key)

        if suggested_chords:
            st.write("Suggested chords")
            show_add_chord_buttons(suggested_chords, "suggested_chord")
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
