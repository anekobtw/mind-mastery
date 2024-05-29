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


class RNIManager(DBManager):
    def __init__(self) -> None:
        table_schema = """CREATE TABLE IF NOT EXISTS rni (
            reminder_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            user_id INTEGER,
            purpose TEXT,
            utc_timestamp INTEGER
        )"""
        super().__init__("databases/reminders.db", table_schema)

    def create_reminder(self, user_id: int, purpose: str, utc_timestamp: int) -> None:
        self.execute_query(
            "INSERT INTO rni(user_id, purpose, utc_timestamp) VALUES (?, ?, ?)",
            (user_id, purpose, utc_timestamp),
        )

    def delete_reminder(self, reminder_id: int) -> None:
        self.execute_query("DELETE FROM rni WHERE reminder_id = ?", (reminder_id,))

    def get_user_reminders(self, user_id: int) -> list:
        return self.fetch_all("SELECT * FROM rni WHERE user_id = ?", (user_id,))

    def get_reminder_info(self, reminder_id: int) -> list:
        return self.fetch_one("SELECT * FROM rni WHERE reminder_id = ?", (reminder_id,))

    def get_all_reminders(self) -> list:
        return self.fetch_all("SELECT * FROM rni")


class RWIManager(DBManager):
    def __init__(self) -> None:
        table_schema = """CREATE TABLE IF NOT EXISTS rwi (
            reminder_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            user_id INTEGER,
            purpose TEXT,
            hour INTEGER,
            minute INTEGER,
            days TEXT
        )"""
        super().__init__("databases/reminders.db", table_schema)

    def create_reminder(
        self, user_id: int, purpose: str, hour: int, minute: int, days: str
    ) -> None:
        self.execute_query(
            "INSERT INTO rwi(user_id, purpose, hour, minute, days) VALUES (?, ?, ?, ?, ?)",
            (user_id, purpose, hour, minute, days),
        )

    def delete_reminder(self, reminder_id: int) -> None:
        self.execute_query("DELETE FROM rwi WHERE reminder_id = ?", (reminder_id,))

    def get_user_reminders(self, user_id: int) -> list:
        return self.fetch_all("SELECT * FROM rwi WHERE user_id = ?", (user_id,))

    def get_reminder_info(self, reminder_id: int) -> list:
        return self.fetch_one("SELECT * FROM rwi WHERE reminder_id = ?", (reminder_id,))

    def get_all_reminders(self) -> list:
        return self.fetch_all("SELECT * FROM rwi")


class SettingsManager(DBManager):
    def __init__(self) -> None:
        table_schema = """CREATE TABLE IF NOT EXISTS settings (
            user_id INTEGER,
            tz_offset_secs INTEGER
        )"""
        super().__init__("databases/settings.db", table_schema)

    def create_settings(self, user_id: int, tz_offset_secs: int) -> None:
        self.execute_query(
            "INSERT INTO settings(user_id, tz_offset_secs) VALUES (?, ?)",
            (user_id, tz_offset_secs),
        )

    def delete_settings(self, user_id: int) -> None:
        self.execute_query("DELETE FROM settings WHERE user_id = ?", (user_id,))

    def get_user_settings(self, user_id: int) -> list:
        return self.fetch_one("SELECT * FROM settings WHERE user_id = ? LIMIT 1", (user_id,))
