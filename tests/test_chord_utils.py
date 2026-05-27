from chord_utils import detect_key, get_chord_name
from music_config import TYPE_MAP

def test_get_chord_name_major_chord():
    selected_chord, notes = get_chord_name("C", "Major", TYPE_MAP)

    assert selected_chord == "C Major"
    assert notes == ["C", "E", "G"]


def test_detect_key_empty_progression():
    assert detect_key([], TYPE_MAP) is None

def test_detect_key_c_major_progression():
    progression = ["C Major", "G Major", "A Minor", "F Major"]

    assert detect_key(progression, TYPE_MAP) == "C major"