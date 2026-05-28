import streamlit as st


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
