from chord_utils import detect_key, get_chord_name, suggest_diatonic_chords


def test_get_chord_name_major_chord():
    selected_chord, notes = get_chord_name("C", "Major")

    assert selected_chord == "C Major"
    assert notes == ["C", "E", "G"]


def test_detect_key_empty_progression():
    assert detect_key([]) is None


def test_detect_key_c_major_progression():
    progression = ["C Major", "G Major", "A Minor", "F Major"]

    assert detect_key(progression) == "C major"


def test_suggest_diatonic_chords_returns_c_major_suggestions():
    assert suggest_diatonic_chords("C major") == [
        "C Major",
        "D Minor",
        "E Minor",
        "F Major",
        "G Major",
        "A Minor",
        "B Diminished",
    ]


def test_suggest_diatonic_chords_returns_empty_list_without_key():
    assert suggest_diatonic_chords(None) == []


def test_suggest_diatonic_chords_returns_g_major_suggestions():
    assert suggest_diatonic_chords("G major") == [
        "G Major",
        "A Minor",
        "B Minor",
        "C Major",
        "D Major",
        "E Minor",
        "F# Diminished",
    ]


def test_suggest_diatonic_chords_returns_a_minor_suggestions():
    assert suggest_diatonic_chords("A minor") == [
        "A Minor",
        "B Diminished",
        "C Major",
        "D Minor",
        "E Minor",
        "F Major",
        "G Major",
    ]
