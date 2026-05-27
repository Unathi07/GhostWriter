from chord_utils import detect_key, get_chord_name

type_map = {
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

def test_get_chord_name_major_chord():
    selected_chord, notes = get_chord_name("C", "Major", type_map)

    assert selected_chord == "C Major"
    assert notes == ["C", "E", "G"]


def test_detect_key_empty_progression():
    assert detect_key([], type_map) is None

def test_detect_key_c_major_progression():
    progression = ["C Major", "G Major", "A Minor", "F Major"]

    assert detect_key(progression, type_map) == "C major"