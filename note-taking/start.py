import hyperdiv as hd
from notes.main import main
from notes.notes_db import migrate_notes_db

if __name__ == "__main__":
    migrate_notes_db()
    hd.run(main)
