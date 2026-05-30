def build_song_draft_export(progression, detected_key, writing_direction, song_notes):
    progression_text = " -> ".join(progression) if progression else "No progression"
    detected_key_text = detected_key or "No key detected"
    writing_direction_text = _format_writing_direction(writing_direction)
    song_notes_text = song_notes or "No lyric notes"

    return f"""GhostWriter Song Draft

Progression:
{progression_text}

Detected key:
{detected_key_text}

Writing direction:
{writing_direction_text}

Lyric notes:
{song_notes_text}
"""


def _format_writing_direction(writing_direction):
    if not writing_direction:
        return "No writing direction"

    if isinstance(writing_direction, str):
        return writing_direction

    lines = []
    for section, content in writing_direction.items():
        lines.append(f"{section}:")

        if isinstance(content, list):
            for item in content:
                lines.append(f"- {item}")
        else:
            lines.append(str(content))

        lines.append("")

    return "\n".join(lines).strip()
