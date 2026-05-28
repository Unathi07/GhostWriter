from chord_utils import detect_key, get_chord_name, suggest_basic_chords


def test_get_chord_name_major_chord():
    selected_chord, notes = get_chord_name("C", "Major")

    assert selected_chord == "C Major"
    assert notes == ["C", "E", "G"]


def test_detect_key_empty_progression():
    assert detect_key([]) is None


def test_detect_key_c_major_progression():
    progression = ["C Major", "G Major", "A Minor", "F Major"]

    assert detect_key(progression) == "C major"


def test_suggest_basic_chords_returns_c_major_suggestions():
    assert suggest_basic_chords("C major") == [
        "C Major",
        "D Minor",
        "E Minor",
        "F Major",
        "G Major",
        "A Minor",
    ]


def test_suggest_basic_chords_returns_empty_list_without_key():
    assert suggest_basic_chords(None) == []
