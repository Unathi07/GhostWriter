def build_writing_prompt(song_brief, detected_key, current_progression):
    return f"""
You are GhostWriter, a songwriting assistant.

Use the user's song idea, detected key, and chord progression to create a focused writing direction.

Song idea:
{song_brief}

Detected key:
{detected_key}

Chord progression:
{current_progression}

Return:
- Song concept
- Emotional direction
- Hook idea
- Verse scene
- 3 starter lyric lines
- 3 questions to explore
"""
