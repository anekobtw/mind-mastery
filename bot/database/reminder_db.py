import sqlite3


class ReminderManager:
    def __init__(self) -> None:
        self.connection = sqlite3.connect("databases/reminder.db")
        self.cursor = self.connection.cursor()

        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS reminder (
            reminder_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            user_id INT,
            purpose TEXT,
            time TEXT,
            frequency TEXT
        )
        """
        )
        self.connection.commit()

    def create_reminder(self, user_id: int, purpose: str, time: str, frequency: str) -> None:
        self.cursor.execute(
            "INSERT INTO reminder(user_id, purpose, time, frequency) VALUES (?, ?, ?, ?)",
            (user_id, purpose, time, frequency),
        )
        self.connection.commit()

    def get_user_reminders(self, user_id: int) -> list:
        self.cursor.execute("SELECT * FROM reminder WHERE user_id = ?", (user_id,))
        reminder = self.cursor.fetchall()
        return reminder if reminder else None
