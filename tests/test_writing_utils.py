from writing_utils import build_writing_direction


def test_build_writing_direction_includes_song_context():
    direction = build_writing_direction(
        "I want to write about love",
        "C major",
        "C Major -> G Major -> A Minor -> F Major",
    )

    assert direction["Song concept"] == (
        "Build the song around this idea: I want to write about love"
    )
    assert "C major" in direction["Emotional direction"]
    assert "C Major -> G Major -> A Minor -> F Major" in direction["Emotional direction"]
    assert len(direction["Starter lyric lines"]) == 3
    assert len(direction["Questions to explore"]) == 3
