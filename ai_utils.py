from openai import OpenAI


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

Format the response in Markdown.

Return:
- Song concept
- Emotional direction
- Hook idea
- Verse scene
- 3 starter lyric lines
- 3 questions to explore
"""


def generate_writing_direction(prompt, api_key):
    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt,
    )

    return response.output_text
