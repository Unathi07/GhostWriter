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

    st.tabs(["Chords","Progressions","Suggestions"])
elif mode == "Song Writing":
    st.subheader('The pen behind your sound')
    st.tabs(["Lyrics","Brainstorm","Inspiration"])




