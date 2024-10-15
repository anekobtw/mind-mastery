import sqlite3


class DBManager:
    def __init__(self, db_name: str, table_schema: str) -> None:
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

        self.cursor.execute(table_schema)
        self.connection.commit()

    def execute_query(self, query: str, params: tuple = ()) -> None:
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetch_all(self, query: str, params: tuple = ()) -> list:
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetch_one(self, query: str, params: tuple = ()) -> list:
        self.cursor.execute(query, params)
        return self.cursor.fetchone()


class NotesManager(DBManager):
    def __init__(self) -> None:
        table_schema = """CREATE TABLE IF NOT EXISTS notes (
            note_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            user_id INTEGER,
            note TEXT
        )"""
        super().__init__("databases/notes.db", table_schema)

    def create_note(self, user_id: int, note: str) -> None:
        self.execute_query("INSERT INTO notes(user_id, note) VALUES (?, ?)", (user_id, note))

    def delete_note(self, note_id: int) -> None:
        self.execute_query("DELETE FROM notes WHERE note_id = ?", (note_id,))

    def find_user_notes(self, user_id: int) -> list:
        return self.fetch_all("SELECT * FROM notes WHERE user_id = ?", (user_id,))

    def get_note_info(self, note_id: int) -> list:
        return self.fetch_one("SELECT * FROM notes WHERE note_id = ? LIMIT 1", (note_id,))
