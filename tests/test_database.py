import os

import pytest
from sqlalchemy import delete

from database import (
    get_engine,
    get_song,
    initialize_database,
    list_songs,
    save_song,
    songs,
)

# by default every test gets its own sqlite file. set GHOSTWRITER_TEST_DB_URL to
# run the same tests against postgres, which is what the deployed app uses.
SHARED_DB_URL = os.environ.get("GHOSTWRITER_TEST_DB_URL")


@pytest.fixture
def db_url(tmp_path):
    url = SHARED_DB_URL or f"sqlite:///{tmp_path}/ghostwriter.db"
    initialize_database(url)

    if SHARED_DB_URL:
        # one shared database keeps rows between tests, so start each test clean
        with get_engine(url).begin() as connection:
            connection.execute(delete(songs))

    return url


def test_save_and_get_song(db_url):
    song_id = save_song(
        "Late night idea",
        "missing someone",
        "hook line",
        ["C Major", "G Major"],
        "C major",
        {"Hook idea": "Say the truth plainly."},
        {"Song idea": "missing someone"},
        db_url=db_url,
    )

    song = get_song(song_id, db_url)

    assert song["title"] == "Late night idea"
    assert song["song_brief"] == "missing someone"
    assert song["song_notes"] == "hook line"
    assert song["progression"] == ["C Major", "G Major"]
    assert song["detected_key"] == "C major"
    assert song["writing_direction"] == {"Hook idea": "Say the truth plainly."}
    assert song["writing_direction_context"] == {"Song idea": "missing someone"}


def test_save_song_updates_existing_song(db_url):
    song_id = save_song("First title", "", "", [], None, None, None, db_url=db_url)
    updated_id = save_song(
        "Updated title",
        "new brief",
        "new notes",
        ["A Minor"],
        "A minor",
        "markdown direction",
        {"Key": "A minor"},
        song_id=song_id,
        db_url=db_url,
    )

    song = get_song(song_id, db_url)

    assert updated_id == song_id
    assert song["title"] == "Updated title"
    assert song["progression"] == ["A Minor"]
    # the ai returns markdown, the template returns a dict, both must round-trip
    assert song["writing_direction"] == "markdown direction"


def test_list_songs_returns_latest_saved_songs(db_url):
    first_id = save_song("First", "", "", [], None, None, None, db_url=db_url)
    second_id = save_song("Second", "", "", [], None, None, None, db_url=db_url)

    listed = list_songs(db_url)

    assert [song["id"] for song in listed] == [second_id, first_id]
    assert listed[0]["title"] == "Second"


def test_untitled_song_gets_a_default_title(db_url):
    song_id = save_song("   ", "", "", [], None, None, None, db_url=db_url)

    assert get_song(song_id, db_url)["title"] == "Untitled song"


def test_get_song_returns_none_when_missing(db_url):
    assert get_song(999999, db_url) is None


def test_direction_source_round_trips(db_url):
    song_id = save_song(
        "AI draft", "", "", [], None, "markdown direction", None,
        "gemini", db_url=db_url,
    )

    assert get_song(song_id, db_url)["direction_source"] == "gemini"


def test_missing_columns_are_added_to_an_older_database(tmp_path):
    # a database created before direction_source existed must keep working
    import sqlalchemy as sa

    if SHARED_DB_URL:
        pytest.skip("this test builds its own sqlite file")

    url = f"sqlite:///{tmp_path}/old.db"
    engine = get_engine(url)
    older = sa.Table(
        "songs",
        sa.MetaData(),
        *[
            sa.Column(c.name, c.type, primary_key=c.primary_key, nullable=c.nullable)
            for c in songs.columns
            if c.name != "direction_source"
        ],
    )
    older.create(engine)
    with engine.begin() as connection:
        connection.execute(
            older.insert().values(
                title="old song", song_brief="", song_notes="", progression=[],
                detected_key=None, writing_direction="old direction",
                writing_direction_context=None,
                created_at="2026-06-01T10:00:00", updated_at="2026-06-01T10:00:00",
            )
        )

    initialize_database(url)

    old_song = get_song(1, url)
    assert old_song["writing_direction"] == "old direction"
    assert old_song["direction_source"] is None

    new_id = save_song(
        "new song", "", "", [], None, "d", None, "template", db_url=url
    )
    assert get_song(new_id, url)["direction_source"] == "template"


def test_chat_messages_round_trip(db_url):
    conversation = [
        {"role": "user", "content": "what is this song about?"},
        {"role": "assistant", "content": "Sounds like distance."},
    ]
    song_id = save_song(
        "Chatty draft", "", "", [], None, None, None, "gemini",
        conversation, db_url=db_url,
    )

    assert get_song(song_id, db_url)["chat_messages"] == conversation


def test_chat_messages_default_to_empty(db_url):
    song_id = save_song("No chat", "", "", [], None, None, None, db_url=db_url)

    assert get_song(song_id, db_url)["chat_messages"] == []
