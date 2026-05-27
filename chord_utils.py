from music21 import harmony, stream, key ,chord

#Splits chord into the root note and chord name
def get_chord_name(root_note, chord_type, type_map):
    chord_suffix = type_map.get(chord_type)
    if chord_suffix is None:
        raise ValueError(f"Unsupported chord type: {chord_type}")

    chord_symbol = harmony.ChordSymbol(f"{root_note}{chord_suffix}")
    revised_notes = [pitch.name.replace("-", "b") for pitch in chord_symbol.pitches]
    selected_chord = f"{root_note} {chord_type}"

    return selected_chord,revised_notes

#Detecting the key of the progression
def detect_key(progression,type_map):
    if not progression:
        return None

    score = stream.Score()
    for chord_name in progression:
        root, chord_type = chord_name.split(" ", 1)
        suffix = type_map.get(chord_type, "")
        chord_symbol = harmony.ChordSymbol(f"{root}{suffix}")
        real_chord = chord.Chord(chord_symbol.pitches)
        score.append(real_chord)

    detected_key = score.analyze('key')

    return str(detected_key)
