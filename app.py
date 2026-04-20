#Import libraries
import streamlit as st

#Title of the App
st.title('GhostWriter')
st.subheader('The pen behind your sound')

#Select a mode
mode = st.radio(
    "What do you need help with?",
    ["Producing","Song Writing"],
    captions=[
        "Match the perfect beats.",
        "Turn your ideas into life.",
    ],
    index=None,
)

if mode == "Producing":
    st.subheader('Make the sounds in your head ideas')
    options = st.multiselect(
        "What instrument(s) are you using?",
        ["Guitar", "Keys", "Bass Guitar", "Drums","Strings"],
        default=["Keys", "Bass Guitar", "Drums"],
    )

    st.write("You selected:", options)
    tab1, tab2, tab3 = st.tabs(["Chords", "Progression", "Suggestions"])

    with tab1:
        st.header("Chords")
        root_note=st.selectbox(
            "Select a root note",
            ("C","C#","D","D#","E","F","F#","G","G#","A","A#","B"),
        )
        st.write("You selected:", root_note)
        chord_type=st.selectbox(
            "Select a chord type",
            ("Major","Minor","7th","Major 7th","Minor 7th","Suspended","Diminished"),
        )
        selected_chord = root_note + " " + chord_type
        st.write("Chord:", selected_chord)
    with tab2:
        st.header("Progression")
    with tab3:
        st.header("Suggestions")


elif mode == "Song Writing":
    st.subheader('The pen behind your sound')
    tab1, tab2, tab3 = st.tabs(["Lyrics", "Brainstorm", "Inspiration"])

    with tab1:
        st.header("Lyrics")
    with tab2:
        st.header("Brainstorm")
    with tab3:
        st.header("Inspiration")







