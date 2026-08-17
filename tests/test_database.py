from database import get_song, initialize_database, list_songs, save_song


def test_save_and_get_song(tmp_path):
    db_path = tmp_path / "ghostwriter.db"
    initialize_database(db_path)

    song_id = save_song(
        "Late night idea",
        "missing someone",
        "hook line",
        ["C Major", "G Major"],
        "C major",
        {"Hook idea": "Say the truth plainly."},
        {"Song idea": "missing someone"},
        db_path=db_path,
    )

    song = get_song(song_id, db_path)

    assert song["title"] == "Late night idea"
    assert song["song_brief"] == "missing someone"
    assert song["song_notes"] == "hook line"
    assert song["progression"] == ["C Major", "G Major"]
    assert song["detected_key"] == "C major"
    assert song["writing_direction"] == {"Hook idea": "Say the truth plainly."}
    assert song["writing_direction_context"] == {"Song idea": "missing someone"}


def test_save_song_updates_existing_song(tmp_path):
    db_path = tmp_path / "ghostwriter.db"
    initialize_database(db_path)

    song_id = save_song(
        "First title",
        "",
        "",
        [],
        None,
        None,
        None,
        db_path=db_path,
    )
    updated_id = save_song(
        "Updated title",
        "new brief",
        "new notes",
        ["A Minor"],
        "A minor",
        "markdown direction",
        {"Key": "A minor"},
        song_id=song_id,
        db_path=db_path,
    )

    song = get_song(song_id, db_path)

    assert updated_id == song_id
    assert song["title"] == "Updated title"
    assert song["progression"] == ["A Minor"]
    assert song["writing_direction"] == "markdown direction"


def test_list_songs_returns_latest_saved_songs(tmp_path):
    db_path = tmp_path / "ghostwriter.db"
    initialize_database(db_path)

    first_id = save_song("First", "", "", [], None, None, None, db_path=db_path)
    second_id = save_song("Second", "", "", [], None, None, None, db_path=db_path)

    songs = list_songs(db_path)

    assert [song["id"] for song in songs] == [second_id, first_id]
    assert songs[0]["title"] == "Second"
