# GhostWriter

GhostWriter is a work-in-progress songwriting assistant built with Python and Streamlit.

The goal is to help users move from a chord progression to a song idea by combining basic music theory tools with lyric brainstorming support.

## Current Features

- One-page workflow for moving from progression to writing direction
- Build a chord progression from root notes and chord types
- Preview chord notes on a piano
- Detect the key of the current progression
- Generate diatonic chord suggestions from the detected key
- Write a free-form song idea
- Generate a structured writing direction from the song idea and progression
- Optionally generate writing direction with OpenAI
- Fall back to a local template when AI mode is off
- Keep lyric notes in a scratchpad

## Tech Stack

- Python
- Streamlit
- music21
- OpenAI API

## Run Locally

From the project root:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Streamlit will print a local URL, usually:

```text
http://localhost:8501
```

## Optional AI Setup

GhostWriter works without an API key when AI mode is off.

To use AI writing direction, create:

```text
.streamlit/secrets.toml
```

Add your OpenAI API key:

```toml
OPENAI_API_KEY = "your_real_api_key_here"
```

Do not commit `secrets.toml`. The project includes `.streamlit/secrets.example.toml`
as a safe example file.

If OpenAI returns a quota or billing error, turn off AI mode and use the local
template mode until the account has available API credits.

## Run Tests

```powershell
.\.venv\Scripts\python.exe -m pytest
```

## Project Direction

Planned improvements:

- Save and reload song projects
- Export progressions as MIDI
- Separate core music logic from the Streamlit interface

## Status

This project is actively being developed as a portfolio project.
