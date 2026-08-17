from html import escape

import streamlit as st
from openai import APIStatusError, OpenAIError, RateLimitError

from ai_utils import build_writing_prompt, chat_with_ghost, generate_writing_direction
from app_state import (
    get_detected_key,
    get_key_text,
    get_progression_text,
    load_song_into_session,
    start_new_song,
)
from chord_utils import get_chord_name, suggest_diatonic_chords
from database import get_song, list_songs, save_song
from export_utils import build_song_draft_export
from music_config import CHORD_TYPES, KEY_OPTIONS, PRESET_PROGRESSIONS, ROOT_NOTES
from piano import render_piano
from ui_components import (
    ICON_PATH,
    USER_ICON_PATH,
    show_add_chord_buttons,
    show_brand_header,
    show_empty_state,
    show_fact_card,
    show_progression_chords,
    show_section_label,
)
from writing_utils import build_writing_direction


def _save_current_song(song_id=None):
    saved_song_id = save_song(
        st.session_state.get("song_title", "Untitled song"),
        st.session_state.get("song_brief", ""),
        st.session_state.get("song_notes", ""),
        st.session_state.get("progression", []),
        get_detected_key(),
        st.session_state.get("writing_direction"),
        st.session_state.get("writing_direction_context"),
        st.session_state.get("direction_source"),
        st.session_state.get("chat_messages"),
        song_id=song_id,
    )
    saved_song = get_song(saved_song_id)
    st.session_state.current_song_id = saved_song_id
    st.session_state.last_saved_at = saved_song["updated_at"]
    return saved_song_id


def _apply_pending_song_action():
    if st.session_state.get("pending_load_song_id"):
        song = get_song(st.session_state.pending_load_song_id)
        st.session_state.pending_load_song_id = None
        if song:
            load_song_into_session(song)

    if st.session_state.get("pending_start_new_song"):
        st.session_state.pending_start_new_song = False
        start_new_song()


def render_sidebar():
    # my side menu for switching between the main tools
    with st.sidebar:
        show_brand_header()

        if st.session_state.get("workspace") == "AI":
            st.session_state.workspace = "Ghost"

        workspace = st.radio(
            "Workspace",
            ("Ghost", "Brainstorm", "Lyrics", "Chords"),
            label_visibility="collapsed",
            key="workspace",
        )

        _apply_pending_song_action()

        if st.session_state.progression:
            context_body = escape(get_progression_text())
            context_caption = "Key: " + escape(get_key_text())
        else:
            context_body = "No chords yet"
            context_caption = "Start in Ghost or open Chords."

        # cleaning the text first because this card uses html
        st.markdown(
            f"""
            <div class="gw-sidebar-context">
                <p class="gw-mini-label">Current song</p>
                <p class="gw-sidebar-song">{context_body}</p>
                <p class="gw-sidebar-note">{context_caption}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.text_input("Song title", key="song_title")

        save_label = "Update draft" if st.session_state.current_song_id else "Save draft"
        if st.button(save_label, key="save_current_song", use_container_width=True):
            _save_current_song(st.session_state.current_song_id)
            st.success("Draft saved.")

        if st.button("Save as new", key="save_as_new_song", use_container_width=True):
            _save_current_song()
            st.success("Saved as a new draft.")

        saved_songs = list_songs()
        if saved_songs:
            song_options = {
                f"{song['title']} - {song['updated_at']}": song["id"]
                for song in saved_songs
            }
            selected_saved_song = st.selectbox(
                "Saved drafts",
                tuple(song_options.keys()),
                key="saved_song_selector",
            )

            load_column, new_column = st.columns(2)
            with load_column:
                if st.button("Load", key="load_saved_song", use_container_width=True):
                    st.session_state.pending_load_song_id = song_options[
                        selected_saved_song
                    ]
                    st.rerun()
            with new_column:
                if st.button("New", key="start_new_song", use_container_width=True):
                    st.session_state.pending_start_new_song = True
                    st.rerun()
        else:
            st.caption("No saved drafts yet.")

    return workspace


def render_direction():
    if not st.session_state.writing_direction:
        return

    show_section_label("Writing direction")

    if st.session_state.get("writing_direction_note"):
        st.caption(st.session_state.writing_direction_note)
    elif st.session_state.get("direction_source"):
        # a reloaded draft has no note, so fall back to the stored source
        source_labels = {"gemini": "Written by Gemini.", "template": "Written by the built-in template."}
        st.caption(source_labels.get(st.session_state.direction_source, ""))

    # showing what the ai/template used so I can remember the context
    if st.session_state.writing_direction_context:
        context_columns = st.columns(3)
        for column, (label, value) in zip(
            context_columns,
            st.session_state.writing_direction_context.items(),
        ):
            with column:
                st.caption(label)
                st.write(value)

    direction = st.session_state.writing_direction

    # template gives sections, the model gives markdown
    if isinstance(direction, dict):
        for section, content in direction.items():
            st.markdown(f"**{section}**")
            if isinstance(content, list):
                for item in content:
                    st.write("- " + item)
            else:
                st.write(content)
    else:
        st.markdown(direction)

    if st.button("Clear direction", key="clear_writing_direction"):
        st.session_state.writing_direction = None
        st.session_state.writing_direction_context = None
        st.session_state.writing_direction_note = None
        st.session_state.direction_source = None
        st.rerun()


def _read_api_key():
    # streamlit raises if there is no secrets file at all, not just a missing key,
    # so template mode has to keep working on a machine that never set one up
    try:
        return st.secrets.get("GEMINI_API_KEY")
    except Exception:
        return None


def _fetch_ai_direction(song_brief, progression_text, detected_key_text):
    """Ask Gemini for a direction. Returns (direction, note).

    direction is None when the model could not answer, and note explains why so
    the page can say what happened before falling back to the template.
    """
    api_key = _read_api_key()

    if not api_key:
        return None, "No Gemini API key is set, so Ghost used its built-in template."

    prompt = build_writing_prompt(song_brief, detected_key_text, progression_text)

    with st.spinner("Ghost is writing..."):
        try:
            return generate_writing_direction(prompt, api_key), None
        except RateLimitError:
            return None, (
                "Gemini's free tier rate limit was hit, so Ghost used its "
                "built-in template."
            )
        except APIStatusError as error:
            if error.status_code in (500, 502, 503):
                return None, (
                    "The free Gemini models are all busy, so Ghost used its "
                    "built-in template. Try again in a moment for an AI answer."
                )

            return None, "Gemini could not answer, so Ghost used its built-in template."
        except OpenAIError:
            return None, "Gemini could not answer, so Ghost used its built-in template."


def _build_direction(song_brief):
    # this can start with just an idea, then use chords later
    progression_text = get_progression_text()
    detected_key_text = get_key_text()

    direction, note = _fetch_ai_direction(
        song_brief,
        progression_text,
        detected_key_text,
    )

    # the template keeps the app useful when the free tier is busy or unset,
    # so a visitor always gets a direction instead of an error
    if direction is None:
        direction = build_writing_direction(
            song_brief,
            detected_key_text,
            progression_text,
        )
        st.session_state.direction_source = "template"
    else:
        st.session_state.direction_source = "gemini"

    st.session_state.writing_direction = direction
    st.session_state.writing_direction_note = note
    st.session_state.writing_direction_context = {
        "Song idea": song_brief,
        "Progression": progression_text,
        "Key": detected_key_text,
    }


def render_ai_workspace():
    # main ghost page, keeping it simple like gemini
    st.markdown(
        """
        <div class="gw-hero">
            <div class="gw-ai-mark">Ghost</div>
            <h1>What are we writing?</h1>
            <p class="gw-hero-copy">
                Drop a feeling, scene, title, or messy idea. Ghost can start there,
                then use chords later when the song needs them.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # prompt first, song context on the side
    prompt_column, context_column = st.columns([2.3, 1])

    with prompt_column:
        song_brief = st.text_area(
            "Ask Ghost",
            placeholder=(
                "Example: Write a late-night R&B song about missing someone but "
                "pretending not to care..."
            ),
            height=130,
            key="song_brief",
            label_visibility="collapsed",
        )

        action_column, _ = st.columns([1, 1.4])
        with action_column:
            # this is the one action the whole page exists for
            generate_clicked = st.button(
                "Ask Ghost",
                key="build_writing_direction",
                type="primary",
                use_container_width=True,
            )

        if generate_clicked:
            if not song_brief.strip():
                st.warning("Add a song idea first.")
            else:
                _build_direction(song_brief.strip())

    with context_column:
        show_section_label("Song context")
        has_chords = bool(st.session_state.progression)
        show_fact_card(
            [
                ("Progression", get_progression_text(), has_chords),
                ("Key", get_key_text(), has_chords),
            ]
        )
        st.caption("Used by Ghost when available.")

    # a divider with nothing after it reads as a section that failed to load
    if st.session_state.writing_direction:
        st.divider()

    render_direction()


def render_lyrics_workspace():
    # notes page for lyrics and exporting
    st.markdown(
        """
        <div class="gw-page-heading">
            <h1>Lyrics notepad</h1>
            <p>Keep hooks, verse fragments, and rough lines in one clean place.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    notes_column, export_column = st.columns([1.7, 1])

    with notes_column:
        st.text_area(
            "Song notes",
            placeholder="Write lyric ideas, hooks, themes, or rough lines here...",
            height=360,
            key="song_notes",
        )

    with export_column:
        show_section_label("Draft snapshot")
        has_chords = bool(st.session_state.progression)
        has_direction = bool(st.session_state.writing_direction)
        show_fact_card(
            [
                ("Progression", get_progression_text(), has_chords),
                ("Key", get_key_text(), has_chords),
                (
                    "Ghost direction",
                    "Ready to export" if has_direction else "Not generated yet",
                    has_direction,
                ),
            ]
        )

        # export whatever I have so far
        song_draft = build_song_draft_export(
            st.session_state.progression,
            get_detected_key(),
            st.session_state.writing_direction,
            st.session_state.get("song_notes", ""),
        )

        st.download_button(
            "Download song draft",
            data=song_draft,
            file_name="ghostwriter_song_draft.txt",
            mime="text/plain",
            use_container_width=True,
        )


def render_chords_workspace():
    # chords get their own tab so the ai page stays clean
    st.markdown(
        """
        <div class="gw-page-heading">
            <h1>Chord progression</h1>
            <p>Build the harmonic idea only when the song needs it.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    builder_column, progression_column = st.columns([1.2, 1])

    with builder_column:
        # quick options first so I can start fast
        show_section_label("Quick start")
        starting_key = st.selectbox(
            "Choose a starting key",
            KEY_OPTIONS,
            key="starting_key",
        )
        starting_key_chords = suggest_diatonic_chords(starting_key)
        show_add_chord_buttons(starting_key_chords, "starting_key_chord")

        preset_name = st.selectbox(
            "Choose a preset",
            tuple(PRESET_PROGRESSIONS.keys()),
            key="preset_progression",
        )
        preset_progression = PRESET_PROGRESSIONS[preset_name]
        st.caption("Preset: " + " -> ".join(preset_progression))

        if st.button(
            "Use preset",
            key="use_preset_progression",
            use_container_width=True,
        ):
            st.session_state.progression = preset_progression.copy()
            st.rerun()

        # manual builder for chords that are not in the quick options
        with st.expander("Manual chord builder"):
            root_note = st.selectbox(
                "Root note",
                ROOT_NOTES,
                key="progression_root_note",
            )
            chord_type = st.selectbox(
                "Chord type",
                CHORD_TYPES,
                key="progression_chord_type",
            )
            selected_chord, revised_notes = get_chord_name(root_note, chord_type)
            st.write("Chord:", selected_chord)
            st.write("Notes:", ", ".join(revised_notes))

            if st.button("Add chord", key="add_progression_chord"):
                st.session_state.progression.append(selected_chord)
                st.rerun()

            st.components.v1.html(
                render_piano(revised_notes, autoplay=True),
                height=300,
            )

    with progression_column:
        show_section_label("Current progression")
        if st.session_state.progression:
            show_progression_chords(st.session_state.progression)
            st.write("Detected key:", get_key_text())

            undo_column, clear_column = st.columns(2)
            with undo_column:
                if st.button(
                    "Undo last",
                    key="undo_last_chord",
                    use_container_width=True,
                ):
                    st.session_state.progression.pop()
                    st.rerun()
            with clear_column:
                if st.button(
                    "Clear",
                    key="clear_progression",
                    use_container_width=True,
                ):
                    st.session_state.progression = []
                    st.rerun()

            # suggestions change when the detected key changes
            suggested_chords = suggest_diatonic_chords(get_detected_key())
            if suggested_chords:
                show_section_label("Suggested next chords")
                show_add_chord_buttons(suggested_chords, "suggested_chord")

            with st.expander("Remove specific chords"):
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
                    "Remove selected",
                    key="remove_progression_chords",
                    disabled=not selected_to_remove,
                    use_container_width=True,
                ):
                    selected_indices = {
                        progression_options.index(option)
                        for option in selected_to_remove
                    }
                    st.session_state.progression = [
                        chord
                        for index, chord in enumerate(st.session_state.progression)
                        if index not in selected_indices
                    ]
                    st.rerun()
        else:
            show_empty_state(
                "No chords yet. Pick a key or a preset to start the progression."
            )


# streamlit's default user avatar is red, which is off-palette
CHAT_AVATARS = {"assistant": str(ICON_PATH), "user": str(USER_ICON_PATH)}

CHAT_STARTERS = (
    "What is this song really about?",
    "Give me three hook lines",
    "What should the second verse do?",
)


def _ghost_reply(question):
    """Append the question, ask Ghost, append the answer. Returns an error string
    when the model could not be reached, so the caller can show it."""
    st.session_state.chat_messages.append({"role": "user", "content": question})

    api_key = _read_api_key()
    if not api_key:
        return (
            "Brainstorming needs a Gemini API key, because there is no template "
            "for an open conversation. Add one to .streamlit/secrets.toml."
        )

    with st.spinner("Ghost is thinking..."):
        try:
            reply = chat_with_ghost(
                st.session_state.chat_messages,
                api_key,
                st.session_state.get("song_brief", ""),
                get_key_text(),
                get_progression_text(),
            )
        except RateLimitError:
            return "Gemini's free tier rate limit was hit. Wait a moment and try again."
        except APIStatusError as error:
            if error.status_code in (500, 502, 503):
                return "The free Gemini models are all busy. Try again in a moment."

            return "Gemini could not answer that one."
        except OpenAIError:
            return "Gemini could not answer that one."

    st.session_state.chat_messages.append({"role": "assistant", "content": reply})
    return None


def render_brainstorm_workspace():
    # a conversation, where the Ghost tab gives a one-shot direction
    st.markdown(
        """
        <div class="gw-page-heading">
            <h1>Brainstorm with Ghost</h1>
            <p>Talk the song through. Ghost knows your idea, key, and progression.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.chat_messages:
        show_empty_state(
            "No conversation yet. Ask a question below, or start with one of these."
        )

        starter_columns = st.columns(len(CHAT_STARTERS))
        for column, starter in zip(starter_columns, CHAT_STARTERS):
            with column:
                if st.button(starter, key=f"starter_{starter}", use_container_width=True):
                    st.session_state.pending_question = starter
                    st.rerun()

    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"], avatar=CHAT_AVATARS.get(message["role"])):
            st.markdown(message["content"])

    question = st.chat_input("Ask Ghost about the song...")

    # a starter button click is handled on the next run, like a typed question
    pending = st.session_state.pop("pending_question", None)
    question = question or pending

    if question:
        error = _ghost_reply(question)
        if error:
            st.session_state.chat_messages.append(
                {"role": "assistant", "content": error}
            )
        st.rerun()

    if st.session_state.chat_messages:
        if st.button("Clear conversation", key="clear_chat"):
            st.session_state.chat_messages = []
            st.rerun()
