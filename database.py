import json
import sqlite3
from contextlib import closing, contextmanager
from datetime import datetime
from pathlib import Path


DB_PATH = Path(__file__).parent / "ghostwriter.db"


def get_connection(db_path=DB_PATH):
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


@contextmanager
def _reading(db_path):
    # sqlite3's own "with connection" commits but never closes, and streamlit
    # reruns this script constantly, so the handles would pile up all session
    with closing(get_connection(db_path)) as connection:
        yield connection


@contextmanager
def _writing(db_path):
    # closing() shuts the handle, the inner "with connection" commits or rolls back
    with closing(get_connection(db_path)) as connection:
        with connection:
            yield connection


def initialize_database(db_path=DB_PATH):
    # make the songs table if it is not there yet
    with _writing(db_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS songs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                song_brief TEXT NOT NULL,
                song_notes TEXT NOT NULL,
                progression TEXT NOT NULL,
                detected_key TEXT,
                writing_direction TEXT NOT NULL,
                writing_direction_context TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )


def save_song(
    title,
    song_brief,
    song_notes,
    progression,
    detected_key,
    writing_direction,
    writing_direction_context,
    song_id=None,
    db_path=DB_PATH,
):
    now = datetime.now().isoformat(timespec="seconds")
    clean_title = title.strip() or "Untitled song"
    song_data = (
        clean_title,
        song_brief or "",
        song_notes or "",
        json.dumps(progression or []),
        detected_key,
        json.dumps(writing_direction),
        json.dumps(writing_direction_context),
        now,
    )

    with _writing(db_path) as connection:
        if song_id:
            result = connection.execute(
                """
                UPDATE songs
                SET title = ?,
                    song_brief = ?,
                    song_notes = ?,
                    progression = ?,
                    detected_key = ?,
                    writing_direction = ?,
                    writing_direction_context = ?,
                    updated_at = ?
                WHERE id = ?
                """,
                (*song_data, song_id),
            )

            if result.rowcount:
                return song_id

        cursor = connection.execute(
            """
            INSERT INTO songs (
                title,
                song_brief,
                song_notes,
                progression,
                detected_key,
                writing_direction,
                writing_direction_context,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (*song_data, now),
        )

        return cursor.lastrowid


def list_songs(db_path=DB_PATH):
    with _reading(db_path) as connection:
        rows = connection.execute(
            """
            SELECT id, title, updated_at
            FROM songs
            ORDER BY updated_at DESC, id DESC
            """
        ).fetchall()

    return [
        {
            "id": row["id"],
            "title": row["title"],
            "updated_at": row["updated_at"],
        }
        for row in rows
    ]


def get_song(song_id, db_path=DB_PATH):
    with _reading(db_path) as connection:
        row = connection.execute(
            """
            SELECT id,
                   title,
                   song_brief,
                   song_notes,
                   progression,
                   detected_key,
                   writing_direction,
                   writing_direction_context,
                   created_at,
                   updated_at
            FROM songs
            WHERE id = ?
            """,
            (song_id,),
        ).fetchone()

    if not row:
        return None

    return {
        "id": row["id"],
        "title": row["title"],
        "song_brief": row["song_brief"],
        "song_notes": row["song_notes"],
        "progression": json.loads(row["progression"]),
        "detected_key": row["detected_key"],
        "writing_direction": json.loads(row["writing_direction"]),
        "writing_direction_context": json.loads(row["writing_direction_context"]),
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }
