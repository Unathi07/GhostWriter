#Import libraries
import streamlit as st
from music21 import harmony
from piano import render_piano

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
#For producers
if mode == "Producing":
    st.subheader('Make the sounds in your head ideas')
    options = st.multiselect(
        "What instrument(s) are you using?",
        ["Guitar", "Keys", "Bass Guitar", "Drums","Strings"],
        default=["Keys", "Bass Guitar", "Drums"],
    )
    #Tab options
    st.write("You selected:", options)
    tab1, tab2, tab3 = st.tabs(["Chords", "Progression", "Suggestions"])
    #Chord name
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
    #Information on the chords
    with tab1:
        st.header("Chords")
        root_note=st.selectbox(
            "Select a root note",
            ("C","C#","D","D#","E","F","F#","G","G#","A","A#","B"),
        )
        st.write("You selected:", root_note)
        chord_type=st.selectbox(
            "Select a chord type",
            ("Major","Minor","7th","Major 7th","Minor 7th","Suspended","Diminished","9th","Major 9th","Minor 9th","Minor 9th","Add9"),
        )
        #Make chord for music21
        chord_map = type_map.get(chord_type)
        full_chord = root_note + chord_map
        chord = harmony.ChordSymbol(full_chord)
        notes = [p.name for p in chord.pitches]
        revised_notes = [item.replace("-","b") for item in notes]

        selected_chord = root_note + " " + chord_type
        st.write("Chord:", selected_chord)
        st.write("Notes:", revised_notes)

        #HTML Code
        st.components.v1.html(render_piano(revised_notes), height=300)
    #Formulating a chord progression
    with tab2:
        st.header("Progression")
        root_note2 = st.selectbox(
            "Select a root note",
            ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"),
        )
        st.write("You selected:", root_note2)
        chord_type2 = st.selectbox(
            "Select a chord type",
            ("Major", "Minor", "7th", "Major 7th", "Minor 7th", "Suspended", "Diminished", "9th", "Major 9th",
             "Minor 9th", "Minor 9th", "Add9"),
        )
        # Make chord for music21
        chord_map2 = type_map.get(chord_type2)
        full_chord2 = root_note2 + chord_map2
        chord2 = harmony.ChordSymbol(full_chord2)
        notes2 = [p.name for p in chord2.pitches]
        revised_notes2 = [item.replace("-", "b") for item in notes2]

        selected_chord2 = root_note2 + " " + chord_type2
        st.write("Chord:", selected_chord2)
        st.write("Notes:", revised_notes2)

    with tab3:
        st.header("Suggestions")

#For song-writers
elif mode == "Song Writing":
    st.subheader('The pen behind your sound')
    tab1, tab2, tab3 = st.tabs(["Lyrics", "Brainstorm", "Inspiration"])

    with tab1:
        st.header("Lyrics")
    with tab2:
        st.header("Brainstorm")
    with tab3:
        st.header("Inspiration")







