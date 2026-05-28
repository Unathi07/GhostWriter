def build_writing_direction(song_brief, detected_key, current_progression):
    return {
        "Song concept": f"Build the song around this idea: {song_brief}",
        "Emotional direction": (
            f"Use the {detected_key} key and {current_progression} progression "
            "to shape the mood of the song."
        ),
        "Hook idea": "Write one short chorus line that clearly says what the song is really about.",
        "Verse scene": "Start the first verse with a specific place, moment, or image.",
        "Starter lyric lines": [
            "I keep replaying the words I never said",
            "The room feels different when your name comes up",
            "I found a little truth hiding in the silence",
        ],
        "Questions to explore": [
            "What does the singer want?",
            "What are they afraid to admit?",
            "What changes by the end of the song?",
        ],
    }
