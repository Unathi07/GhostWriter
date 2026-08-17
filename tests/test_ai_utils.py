from ai_utils import build_chat_system_prompt, build_writing_prompt


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
    assert "## Song concept" in prompt
    assert "## Questions to explore" in prompt
    assert "3 starter lyric lines" in prompt


def test_chat_system_prompt_carries_the_song_context():
    prompt = build_chat_system_prompt(
        "missing a friend who moved away",
        "C major",
        "C Major -> G Major",
    )

    assert "missing a friend who moved away" in prompt
    assert "C major" in prompt
    assert "C Major -> G Major" in prompt
    assert "brainstorming conversation" in prompt


def test_chat_system_prompt_handles_a_song_with_no_idea_yet():
    prompt = build_chat_system_prompt("", "No key detected yet", "No progression yet")

    assert "Not written yet" in prompt
    # ghost must not be told to invent theory it was not given
    assert "Never invent music theory context" in prompt
