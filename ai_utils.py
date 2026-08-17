import time

from openai import APIConnectionError, APIStatusError, OpenAI

# gemini exposes an openai-compatible endpoint, so the same client library works
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

# all free tier, newest first. the newest model is the busiest, so if it is
# overloaded we drop to an older one instead of failing the whole request
GEMINI_MODELS = [
    "gemini-3.7-flash",
    "gemini-3.5-flash",
    "gemini-2.5-flash",
]

# 503 means the model is busy, not that the request was wrong, so it is worth retrying
BUSY_STATUS_CODES = (429, 500, 502, 503)
ATTEMPTS_PER_MODEL = 2
RETRY_WAIT_SECONDS = 2


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


def _ask_model(client, model, prompt):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content


def generate_writing_direction(prompt, api_key):
    # keeping the model call here so the page code stays cleaner
    client = OpenAI(api_key=api_key, base_url=GEMINI_BASE_URL)
    last_error = None

    for model in GEMINI_MODELS:
        for attempt in range(ATTEMPTS_PER_MODEL):
            try:
                return _ask_model(client, model, prompt)
            except APIStatusError as error:
                # a bad key or a bad prompt will never succeed, so do not retry those
                if error.status_code not in BUSY_STATUS_CODES:
                    raise

                last_error = error
            except APIConnectionError as error:
                last_error = error

            if attempt + 1 < ATTEMPTS_PER_MODEL:
                time.sleep(RETRY_WAIT_SECONDS)

    # every free model was busy, let the page show the last real error
    raise last_error
