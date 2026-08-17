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


MAX_HISTORY_MESSAGES = 20


def _complete(api_key, messages):
    """Send messages to Gemini, retrying and dropping to an older model when the
    newest one is busy. Raises the last real error if every model refuses."""
    client = OpenAI(api_key=api_key, base_url=GEMINI_BASE_URL)
    last_error = None

    for model in GEMINI_MODELS:
        for attempt in range(ATTEMPTS_PER_MODEL):
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                )

                return response.choices[0].message.content
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


def generate_writing_direction(prompt, api_key):
    return _complete(api_key, [{"role": "user", "content": prompt}])


def build_chat_system_prompt(song_brief, detected_key, current_progression):
    # ghost should talk about THIS song, not songwriting in general
    return f"""
You are Ghost, a songwriting collaborator having a brainstorming conversation.

Keep replies short and conversational, two or three sentences unless the writer
asks for more. Offer concrete lines, images, and questions rather than general
advice. Ask one question back when it would move the song forward.

Never invent music theory context that is not given below. If the key or the
progression is missing, work from the idea and say chords can come later.

Song idea:
{song_brief or "Not written yet"}

Detected key:
{detected_key}

Chord progression:
{current_progression}
""".strip()


def chat_with_ghost(history, api_key, song_brief, detected_key, current_progression):
    system_prompt = build_chat_system_prompt(
        song_brief,
        detected_key,
        current_progression,
    )

    # only the recent turns are sent, so a long session does not burn the free tier
    recent = history[-MAX_HISTORY_MESSAGES:]

    return _complete(
        api_key,
        [{"role": "system", "content": system_prompt}, *recent],
    )
