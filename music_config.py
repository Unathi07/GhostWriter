# Music options used by the progression builder.
TYPE_MAP = {
    "Major": "",
    "Minor": "m",
    "7th": "7",
    "Major 7th": "maj7",
    "Minor 7th": "min7",
    "Suspended": "sus",
    "Diminished": "dim",
    "9th": "9",
    "Major 9th": "maj9",
    "Minor 9th": "min9",
    "Add9": "add9",
}
CHORD_TYPES = (
    "Major",
    "Minor",
    "7th",
    "Major 7th",
    "Minor 7th",
    "Suspended",
    "Diminished",
    "9th",
    "Major 9th",
    "Minor 9th",
    "Add9",
)
ROOT_NOTES = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")

# Builds options like "C major" and "A minor" for the starting-key selector.
KEY_OPTIONS = tuple(
    f"{root_note} {mode}"
    for root_note in ROOT_NOTES
    for mode in ("major", "minor")
)

# Ready-made progressions give users a fast starting point.
PRESET_PROGRESSIONS = {
    "Pop": ["C Major", "G Major", "A Minor", "F Major"],
    "Sad": ["A Minor", "F Major", "C Major", "G Major"],
    "R&B": ["A Minor 7th", "D Minor 7th", "G 7th", "C Major 7th"],
    "Hopeful": ["C Major", "F Major", "A Minor", "G Major"],
}
