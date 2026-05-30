from export_utils import build_song_draft_export


def test_build_song_draft_export_includes_song_parts():
    draft = build_song_draft_export(
        ["C Major", "G Major", "A Minor", "F Major"],
        "C major",
        {
            "Song concept": "Build the song around love.",
            "Starter lyric lines": [
                "I keep replaying the words I never said",
                "The room feels different when your name comes up",
            ],
        },
        "Use the second verse to reveal the real conflict.",
    )

    assert "GhostWriter Song Draft" in draft
    assert "C Major -> G Major -> A Minor -> F Major" in draft
    assert "C major" in draft
    assert "Song concept:" in draft
    assert "- I keep replaying the words I never said" in draft
    assert "Use the second verse to reveal the real conflict." in draft


def test_build_song_draft_export_handles_missing_content():
    draft = build_song_draft_export([], None, None, "")

    assert "No progression" in draft
    assert "No key detected" in draft
    assert "No writing direction" in draft
    assert "No lyric notes" in draft
