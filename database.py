"""Data access for saved songs.

The same code runs on SQLite and Postgres. DATABASE_URL picks the backend:
tests and local development use a SQLite file, the deployed app uses Postgres.
Streamlit copies secrets.toml entries into the environment, so setting
DATABASE_URL in the Streamlit Cloud secrets UI is all the deploy needs.
"""

import os
from datetime import datetime
from functools import lru_cache
from pathlib import Path

from sqlalchemy import (
    JSON,
    Column,
    Integer,
    MetaData,
    Table,
    Text,
    create_engine,
    inspect,
    insert,
    select,
    text,
    update,
)

DEFAULT_SQLITE_PATH = Path(__file__).parent / "ghostwriter.db"

metadata = MetaData()

# writing_direction is a markdown string from the ai and a dict from the
# template, so it is stored as json rather than as one fixed shape
songs = Table(
    "songs",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", Text, nullable=False),
    Column("song_brief", Text, nullable=False),
    Column("song_notes", Text, nullable=False),
    Column("progression", JSON, nullable=False),
    Column("detected_key", Text),
    Column("writing_direction", JSON),
    Column("writing_direction_context", JSON),
    # "gemini" or "template", so a reloaded draft still says where it came from
    Column("direction_source", Text),
    # the brainstorming conversation, as a list of {role, content}
    Column("chat_messages", JSON),
    # iso-8601 sorts the same as text on both backends, so there is no
    # timestamp format to migrate when moving from sqlite to postgres
    Column("created_at", Text, nullable=False),
    Column("updated_at", Text, nullable=False),
)


def resolve_database_url(db_url=None):
    if db_url:
        # a bare filesystem path still works, so tests can pass tmp_path
        text = str(db_url)
        return text if "://" in text else f"sqlite:///{text}"

    return os.environ.get("DATABASE_URL") or f"sqlite:///{DEFAULT_SQLITE_PATH}"


@lru_cache(maxsize=None)
def get_engine(db_url=None):
    url = resolve_database_url(db_url)

    # pool_pre_ping matters on a serverless postgres: it scales to zero when
    # idle, so a pooled connection can already be dead by the next page load
    return create_engine(url, pool_pre_ping=True, future=True)


def _add_missing_columns(engine):
    """create_all() never alters an existing table, so new nullable columns have
    to be added by hand for databases that were made by an older version."""
    inspector = inspect(engine)

    if not inspector.has_table(songs.name):
        return

    existing = {column["name"] for column in inspector.get_columns(songs.name)}
    missing = [column for column in songs.columns if column.name not in existing]

    for column in missing:
        column_type = column.type.compile(engine.dialect)
        # the names come from our own metadata, never from user input
        statement = text(
            f"ALTER TABLE {songs.name} ADD COLUMN {column.name} {column_type}"
        )
        with engine.begin() as connection:
            connection.execute(statement)


def initialize_database(db_url=None):
    engine = get_engine(db_url)
    _add_missing_columns(engine)
    metadata.create_all(engine)


def _now():
    return datetime.now().isoformat(timespec="seconds")


def save_song(
    title,
    song_brief,
    song_notes,
    progression,
    detected_key,
    writing_direction,
    writing_direction_context,
    direction_source=None,
    chat_messages=None,
    song_id=None,
    db_url=None,
):
    now = _now()
    values = {
        "title": title.strip() or "Untitled song",
        "song_brief": song_brief or "",
        "song_notes": song_notes or "",
        "progression": progression or [],
        "detected_key": detected_key,
        "writing_direction": writing_direction,
        "writing_direction_context": writing_direction_context,
        "direction_source": direction_source,
        "chat_messages": chat_messages or [],
        "updated_at": now,
    }

    with get_engine(db_url).begin() as connection:
        if song_id:
            result = connection.execute(
                update(songs).where(songs.c.id == song_id).values(**values)
            )

            if result.rowcount:
                return song_id

        # the row was deleted while it was open, so save it as a new song
        result = connection.execute(insert(songs).values(created_at=now, **values))

        return result.inserted_primary_key[0]


def list_songs(db_url=None):
    query = (
        select(songs.c.id, songs.c.title, songs.c.updated_at)
        # two saves in the same second tie on updated_at, so id breaks the tie
        .order_by(songs.c.updated_at.desc(), songs.c.id.desc())
    )

    with get_engine(db_url).connect() as connection:
        rows = connection.execute(query).mappings().all()

    return [dict(row) for row in rows]


def get_song(song_id, db_url=None):
    query = select(songs).where(songs.c.id == song_id)

    with get_engine(db_url).connect() as connection:
        row = connection.execute(query).mappings().first()

    return dict(row) if row else None
