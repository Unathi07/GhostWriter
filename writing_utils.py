def build_writing_direction(song_brief, detected_key, current_progression):
    return {
        "Core idea": f"Build the song around: {song_brief}",
        "Hook angle": "Focus the chorus on one simple emotional truth the listener can repeat.",
        "Verse scene": "Start with a specific moment, place, or memory instead of explaining the whole feeling.",
        "Questions to explore": [
            "What does the singer want but cannot say directly?",
            "What small detail makes the emotion feel real?",
            "What changes between the first verse and the final chorus?",
        ],
        "Starter line": (
            f"In {detected_key}, let the progression {current_progression} "
            "carry a feeling of honesty and movement."
        ),
    }