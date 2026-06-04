def build_writing_direction(song_brief, detected_key, current_progression):
    # template mode still needs to help before I add chords
    missing_music_context = (
        not detected_key
        or not current_progression
        or detected_key == "No key detected yet"
        or current_progression == "No progression yet"
    )

    if missing_music_context:
        emotional_direction = (
            "Start from the emotion and story first. Add a key or chord progression "
            "later if you want the melody and harmony to steer the mood."
        )
    else:
        emotional_direction = (
            f"Use the {detected_key} key and {current_progression} progression "
            "to shape the mood of the song."
        )

    return {
        "Song concept": f"Build the song around this idea: {song_brief}",
        "Emotional direction": emotional_direction,
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
