# GhostWriter

GhostWriter is a work-in-progress songwriting assistant built with Python and Streamlit.

The goal is to help users move from a song idea to lyrics and chord progressions by combining basic music theory tools with lyric brainstorming support.

## Current Features

- AI-first workspace with side tabs for lyrics and chords
- Build a chord progression from root notes and chord types
- Preview chord notes on a piano
- Detect the key of the current progression
- Generate diatonic chord suggestions from the detected key
- Write a free-form song idea
- Generate a structured writing direction from the song idea and progression
- Generate writing direction with the Gemini API (free tier)
- Fall back to a built-in template automatically when Gemini is unavailable
- Keep lyric notes in a scratchpad
- Save and reload song drafts with SQLite
- Download the song draft as a text file

## Tech Stack

- Python
- Streamlit
- music21
- Gemini API (via the OpenAI-compatible endpoint)
- SQLite

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

GhostWriter runs without an API key. Ghost falls back to a built-in writing
template and says so, so the app never dead-ends on a missing key.

To use AI writing direction, create:

```text
.streamlit/secrets.toml
```

Add your Gemini API key:

```toml
GEMINI_API_KEY = "your_real_api_key_here"
```

Get a free key from [Google AI Studio](https://aistudio.google.com/apikey). The
free tier does not require a payment method. GhostWriter talks to Gemini through
its OpenAI-compatible endpoint, so the `openai` client library is still used —
only the base URL and model name differ.

Do not commit `secrets.toml`. The project includes `.streamlit/secrets.example.toml`
as a safe example file.

Free tier models are shared and sometimes return `503 UNAVAILABLE` when they are
busy. GhostWriter handles this automatically: it retries, then falls back through
the model list in `ai_utils.GEMINI_MODELS`.

If every model is busy, Ghost uses its built-in template instead and notes that
on the page, so a visitor always gets a writing direction.

## Run Tests

```powershell
.\.venv\Scripts\python.exe -m pytest
```

## Local Database

GhostWriter saves drafts to a local SQLite database:

```text
ghostwriter.db
```

This file is ignored by git because it is local app data.

## Project Direction

Planned improvements:

- Delete saved drafts
- Export progressions as MIDI
- Polish the app icon and visual identity

## Status

This project is actively being developed as a portfolio project.
