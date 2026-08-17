# GhostWriter

[![tests](https://github.com/Unathi07/GhostWriter/actions/workflows/tests.yml/badge.svg)](https://github.com/Unathi07/GhostWriter/actions/workflows/tests.yml)

**[Try it live &rarr;](https://ghostwrite.streamlit.app/)**

A songwriting assistant that takes a rough idea and helps turn it into a song.
Ghost writes a structured writing direction from your idea, you can talk the song
through with it in a brainstorming conversation, and music21 handles the harmony
side - key detection and diatonic chord suggestions.

![The Ghost workspace](docs/screenshots/ghost.png)

Built with Python and Streamlit. Gemini for the writing, music21 for the theory,
SQLAlchemy over SQLite locally and Postgres in production.

## Current Features

- AI-first workspace with side tabs for brainstorming, lyrics, and chords
- Build a chord progression from root notes and chord types
- Preview chord notes on a piano
- Detect the key of the current progression
- Generate diatonic chord suggestions from the detected key
- Write a free-form song idea
- Generate a structured writing direction from the song idea and progression
- Generate writing direction with the Gemini API (free tier)
- Fall back to a built-in template automatically when Gemini is unavailable
- Brainstorm with Ghost in a conversation that knows the idea, key, and progression
- Keep lyric notes in a scratchpad
- Save and reload song drafts, including the brainstorming conversation
- Download the song draft as a text file

## The Workspaces

**Brainstorm** - a conversation that already knows the idea, key, and progression.

![The Brainstorm workspace](docs/screenshots/brainstorm.png)

**Chords** - build a progression from a key, a preset, or by hand, and hear it on
the piano. music21 detects the key and suggests what fits next.

![The Chords workspace](docs/screenshots/chords.png)

**Lyrics** - a scratchpad with the draft snapshot beside it, and a text export.

![The Lyrics workspace](docs/screenshots/lyrics.png)

## Tech Stack

- Python
- Streamlit
- music21
- Gemini API (via the OpenAI-compatible endpoint)
- SQLAlchemy Core
- SQLite locally, Postgres in production

## Run Locally

From the project root:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Streamlit will print a local URL, usually:

```text
http://localhost:8501
```

## AI Setup

Ghost always asks Gemini first. If no key is set, or the free tier is busy, the
writing direction falls back to a built-in template and the page says so, so the
app never dead-ends.

The Brainstorm tab does need a key, because there is no template for an open
conversation.

To set one up, create:

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

The suite defaults to a throwaway SQLite file per test. To run the database
tests against Postgres instead, point them at a database first:

```powershell
$env:GHOSTWRITER_TEST_DB_URL="postgresql://user:password@host/dbname"
.\.venv\Scripts\python.exe -m pytest tests/test_database.py
```

## Database

The data layer is SQLAlchemy Core, so the same code runs on SQLite and Postgres.
`DATABASE_URL` picks the backend:

- unset - a local SQLite file, `ghostwriter.db`, ignored by git as local app data
- set - that database, which is how the deployed app uses Postgres

```toml
DATABASE_URL = "postgresql://user:password@host/dbname"
```

Streamlit copies `secrets.toml` entries into the environment, so setting
`DATABASE_URL` in secrets is all a deploy needs. No code changes.

Schema changes are applied on startup. `create_all()` never alters an existing
table, so `initialize_database()` compares the model against the live table and
adds any missing columns before the app reads from it.

## Project Direction

Planned improvements:

- Delete saved drafts
- Export progressions as MIDI

## Status

Deployed and actively developed. Tests run on every push via GitHub Actions.
