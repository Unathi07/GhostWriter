from openai import OpenAI


def build_writing_prompt(song_brief, detected_key, current_progression):
    # sometimes there are no chords yet, so the ai should not make them up
    return f"""
You are GhostWriter, a songwriting assistant.

Use the user's song idea, detected key, and chord progression to create a focused writing direction.
If the detected key or chord progression is missing, do not invent music theory context.
Start from the user's idea and suggest that chords can be added later.

Song idea:
{song_brief}

Detected key:
{detected_key}

Chord progression:
{current_progression}

Format the response in Markdown with these exact headings:
- ## Song concept
- ## Emotional direction
- ## Hook idea
- ## Verse scene
- ## Starter lyric lines
- ## Questions to explore

Include 3 starter lyric lines and 3 questions to explore.
"""


def generate_writing_direction(prompt, api_key):
    # keeping the openai call here so the page code stays cleaner
    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt,
    )

    return response.output_text
