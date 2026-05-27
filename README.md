# GhostWriter

GhostWriter is a work-in-progress songwriting assistant built with Python and Streamlit.

The goal is to help users move from a chord progression to a song idea by combining basic music theory tools with lyric brainstorming support.

## Current Features

- Build a chord progression from root notes and chord types
- Preview chord notes on a piano
- Detect the key of the current progression
- Write a free-form song idea
- Generate a structured writing direction from the song idea and progression
- Keep lyric notes in a scratchpad

## Tech Stack

- Python
- Streamlit
- music21

## Run Locally

From the project root:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Streamlit will print a local URL, usually:

```text
http://localhost:8501
```

## Project Direction

Planned improvements:

- Add smarter chord and progression suggestions
- Add AI-powered interpretation of song ideas
- Save and reload song projects
- Export progressions as MIDI
- Separate core music logic from the Streamlit interface

## Status

This project is actively being developed as a portfolio project.
