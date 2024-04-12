import sqlite3


class NotesManager:
    def __init__(self) -> None:
        self.connection = sqlite3.connect("databases/notes.db")
        self.cursor = self.connection.cursor()

        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS notes (
            note_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            user_id INTEGER,
            note TEXT
        )
        """
        )
        self.connection.commit()

    def create_note(self, user_id: int, note: str) -> None:
        self.cursor.execute("INSERT INTO notes(user_id, note) VALUES (?, ?)", (user_id, note))
        self.connection.commit()

    def delete_note(self, note_id: int) -> None:
        self.cursor.execute("DELETE FROM notes WHERE note_id = ?", (note_id,))
        self.connection.commit()

    def find_notes(self, user_id: str) -> list:
        self.cursor.execute("SELECT * FROM notes WHERE user_id = ?", (user_id,))
        notes = self.cursor.fetchall()
        return notes if notes else None

    def get_note_info(self, note_id: int) -> list:
        self.cursor.execute("SELECT * FROM notes WHERE note_id = ? LIMIT 1", (note_id,))
        note = self.cursor.fetchone()
        return note if note else None
