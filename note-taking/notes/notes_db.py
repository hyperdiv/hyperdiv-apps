import os
import uuid
from hyperdiv.sqlite import sqlite, migrate, sql

db = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "notes.db",
    )
)

migrations = [
    sql(
        """
        create table Note (
            note_id text primary key,
            note_title,
            note_body text,
            ts int
        )
        """
    )
]


def migrate_notes_db():
    migrate(db, migrations)


def create_empty_note():
    note_id = uuid.uuid4().hex
    with sqlite(db) as (_, cursor):
        cursor.execute(
            """
            insert into Note (
                note_id, note_title, note_body, ts
            ) values (
                ?, "", "", strftime('%s', 'now')
            )
            """,
            (note_id,),
        )
    return note_id


def read_note(note_id):
    with sqlite(db) as (_, cursor):
        cursor.execute(
            """
            select note_body, note_title, ts from Note
            where note_id = ?
            """,
            (note_id,),
        )
        results = cursor.fetchall()
        return results[0] if len(results) > 0 else None


def get_notes():
    with sqlite(db) as (_, cursor):
        cursor.execute(
            """
            select note_id, note_title, ts
            from Note
            order by ts desc
            """
        )
        return cursor.fetchall()


def save_note(note_id, note_title, note_body):
    with sqlite(db) as (_, cursor):
        cursor.execute(
            """
            update Note set
                note_body = ?,
                note_title = ?,
                ts = strftime('%s', 'now')
            where note_id = ?
            """,
            (note_body, note_title, note_id),
        )


def delete_note(note_id):
    with sqlite(db) as (_, cursor):
        cursor.execute(
            """
            delete from Note where note_id = ?
            """,
            (note_id,),
        )
