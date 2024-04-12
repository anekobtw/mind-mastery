import sqlite3


class SettingsManager:
    def __init__(self) -> None:
        self.connection = sqlite3.connect("databases/settings.db")
        self.cursor = self.connection.cursor()

        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS settings (
            user_id INTEGER,
            tz_offset INTEGER
        )
        """
        )
        self.connection.commit()

    def insert_settings(self, user_id: int, tz_offset: int) -> None:
        self.cursor.execute("INSERT INTO settings(user_id, tz_offset) VALUES (?, ?)", (user_id, tz_offset))
        self.connection.commit()

    def delete_settings(self, user_id: int) -> None:
        self.cursor.execute("DELETE FROM settings WHERE user_id = ?", (user_id,))
        self.connection.commit()

    def get_user_settings(self, user_id: int) -> list:
        self.cursor.execute("SELECT * FROM settings WHERE user_id = ? LIMIT 1", (user_id,))
        settings = self.cursor.fetchone()
        return settings if settings else None
