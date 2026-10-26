"""SQL for users and sessions."""

import sqlite3


class UserRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def create(self, name: str, email: str, password_hash: str) -> sqlite3.Row:
        cursor = self.connection.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, password_hash),
        )
        self.connection.commit()
        return self.find_by_id(cursor.lastrowid)

    def find_by_id(self, user_id: int) -> sqlite3.Row | None:
        return self.connection.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()

    def find_by_email(self, email: str) -> sqlite3.Row | None:
        return self.connection.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()


class SessionRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def create(self, token: str, user_id: int) -> None:
        self.connection.execute(
            "INSERT INTO sessions (token, user_id) VALUES (?, ?)", (token, user_id)
        )
        self.connection.commit()

    def find_user(self, token: str) -> sqlite3.Row | None:
        return self.connection.execute(
            "SELECT users.* FROM sessions JOIN users ON users.id = sessions.user_id "
            "WHERE sessions.token = ?",
            (token,),
        ).fetchone()

    def delete(self, token: str) -> None:
        self.connection.execute("DELETE FROM sessions WHERE token = ?", (token,))
        self.connection.commit()
