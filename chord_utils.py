from music21 import chord, harmony, key, roman, stream
from music_config import TYPE_MAP

# Splits chord into the root note and chord name.
def get_chord_name(root_note, chord_type, type_map=None):
    chord_map = type_map or TYPE_MAP
    chord_suffix = chord_map.get(chord_type)
    if chord_suffix is None:
        raise ValueError(f"Unsupported chord type: {chord_type}")

    chord_symbol = harmony.ChordSymbol(f"{root_note}{chord_suffix}")
    revised_notes = [pitch.name.replace("-", "b") for pitch in chord_symbol.pitches]
    selected_chord = f"{root_note} {chord_type}"

    return selected_chord, revised_notes

# Detecting the key of the progression.
def detect_key(progression, type_map=None):
    if not progression:
        return None

    chord_map = type_map or TYPE_MAP

    # Holds the progression.
    score = stream.Score()
    for chord_name in progression:
        root, chord_type = chord_name.split(" ", 1)
        suffix = chord_map.get(chord_type, "")
        chord_symbol = harmony.ChordSymbol(f"{root}{suffix}")
        real_chord = chord.Chord(chord_symbol.pitches)
        score.append(real_chord)

    # Detects the key.
    detected_key = score.analyze("key")
    return str(detected_key)


# Gives chord suggestions based on the detected key.
def suggest_diatonic_chords(detected_key):
    if detected_key is None:
        return []

    key_parts = detected_key.split()
    tonic = key_parts[0]
    mode = key_parts[1] if len(key_parts) > 1 else "major"
    detected = key.Key(tonic, mode)

    # Minor keys use different roman numerals from major keys.
    if mode == "minor":
        roman_numerals = ("i", "iio", "III", "iv", "v", "VI", "VII")
    else:
        roman_numerals = ("I", "ii", "iii", "IV", "V", "vi", "viio")

    suggestions = []
    for numeral in roman_numerals:
        roman_chord = roman.RomanNumeral(numeral, detected)
        root = roman_chord.root().name.replace("-", "b")
        quality = roman_chord.quality.title()
        suggestions.append(f"{root} {quality}")

    return suggestions
