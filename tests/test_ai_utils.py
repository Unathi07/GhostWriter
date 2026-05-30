from ai_utils import build_writing_prompt


def test_build_writing_prompt():
    prompt = build_writing_prompt(
        "I want to write about love",
        "C major",
        "C Major -> G Major -> A Minor -> F Major",
    )

    assert "I want to write about love" in prompt
    assert "C major" in prompt
    assert "C Major -> G Major -> A Minor -> F Major" in prompt
    assert "Format the response in Markdown" in prompt
    assert "Song concept" in prompt
    assert "3 starter lyric lines" in prompt
