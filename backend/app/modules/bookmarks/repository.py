"""SQL for folders, items, and media. No business rules live here."""

import sqlite3


class FolderRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def list_all(self, user_id: int) -> list[sqlite3.Row]:
        return self.connection.execute(
            "SELECT * FROM folders WHERE user_id = ? ORDER BY path", (user_id,)
        ).fetchall()

    def find_by_path(self, user_id: int, path: str) -> sqlite3.Row | None:
        return self.connection.execute(
            "SELECT * FROM folders WHERE user_id = ? AND path = ?", (user_id, path)
        ).fetchone()

    def find_by_id(self, user_id: int, folder_id: int) -> sqlite3.Row | None:
        return self.connection.execute(
            "SELECT * FROM folders WHERE user_id = ? AND id = ?", (user_id, folder_id)
        ).fetchone()

    def list_children(self, user_id: int, parent_id: int | None) -> list[sqlite3.Row]:
        if parent_id is None:
            return self.connection.execute(
                "SELECT * FROM folders WHERE user_id = ? AND parent_id IS NULL ORDER BY name",
                (user_id,),
            ).fetchall()
        return self.connection.execute(
            "SELECT * FROM folders WHERE user_id = ? AND parent_id = ? ORDER BY name",
            (user_id, parent_id),
        ).fetchall()

    def create(
        self, user_id: int, parent_id: int | None, name: str, path: str
    ) -> sqlite3.Row:
        cursor = self.connection.execute(
            "INSERT INTO folders (user_id, parent_id, name, path) VALUES (?, ?, ?, ?)",
            (user_id, parent_id, name, path),
        )
        self.connection.commit()
        return self.find_by_id(user_id, cursor.lastrowid)

    def update(
        self, user_id: int, folder_id: int, name: str, path: str
    ) -> sqlite3.Row:
        self.connection.execute(
            "UPDATE folders SET name = ?, path = ? WHERE user_id = ? AND id = ?",
            (name, path, user_id, folder_id),
        )
        self.connection.commit()
        return self.find_by_id(user_id, folder_id)

    def update_path_prefix(self, user_id: int, old_path: str, new_path: str) -> None:
        self.connection.execute(
            "UPDATE folders SET path = ? || substr(path, ?) "
            "WHERE user_id = ? AND (path = ? OR path LIKE ?)",
            (new_path, len(old_path) + 1, user_id, old_path, old_path + "/%"),
        )
        self.connection.commit()

    def delete(self, user_id: int, folder_id: int) -> None:
        self.connection.execute(
            "DELETE FROM folders WHERE user_id = ? AND id = ?", (user_id, folder_id)
        )
        self.connection.commit()

    def search(self, user_id: int, query: str) -> list[sqlite3.Row]:
        return self.connection.execute(
            "SELECT * FROM folders WHERE user_id = ? AND path LIKE ? ORDER BY path LIMIT 50",
            (user_id, f"%{query}%"),
        ).fetchall()


class ItemRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def list_by_folder(self, user_id: int, folder_id: int | None) -> list[sqlite3.Row]:
        if folder_id is None:
            return self.connection.execute(
                "SELECT * FROM items WHERE user_id = ? AND folder_id IS NULL "
                "ORDER BY created_at DESC, title",
                (user_id,),
            ).fetchall()
        return self.connection.execute(
            "SELECT * FROM items WHERE user_id = ? AND folder_id = ? "
            "ORDER BY created_at DESC, title",
            (user_id, folder_id),
        ).fetchall()

    def find_by_id(self, user_id: int, item_id: int) -> sqlite3.Row | None:
        return self.connection.execute(
            "SELECT * FROM items WHERE user_id = ? AND id = ?", (user_id, item_id)
        ).fetchone()

    def create(
        self,
        user_id: int,
        folder_id: int | None,
        item_type: str,
        title: str,
        url: str | None,
        note: str | None,
        media_id: int | None = None,
    ) -> sqlite3.Row:
        cursor = self.connection.execute(
            "INSERT INTO items (user_id, folder_id, type, title, url, note, media_id) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_id, folder_id, item_type, title, url, note, media_id),
        )
        self.connection.commit()
        return self.find_by_id(user_id, cursor.lastrowid)

    def update(
        self, user_id: int, item_id: int, title: str, url: str | None, note: str | None
    ) -> sqlite3.Row:
        self.connection.execute(
            "UPDATE items SET title = ?, url = ?, note = ?, updated_at = datetime('now') "
            "WHERE user_id = ? AND id = ?",
            (title, url, note, user_id, item_id),
        )
        self.connection.commit()
        return self.find_by_id(user_id, item_id)

    def delete(self, user_id: int, item_id: int) -> None:
        self.connection.execute(
            "DELETE FROM items WHERE user_id = ? AND id = ?", (user_id, item_id)
        )
        self.connection.commit()

    def search(self, user_id: int, query: str) -> list[sqlite3.Row]:
        pattern = f"%{query}%"
        return self.connection.execute(
            "SELECT * FROM items WHERE user_id = ? "
            "AND (title LIKE ? OR url LIKE ? OR note LIKE ?) "
            "ORDER BY created_at DESC LIMIT 50",
            (user_id, pattern, pattern, pattern),
        ).fetchall()


class MediaRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def create(
        self, user_id: int, filename: str, mime_type: str, size: int, data: bytes
    ) -> sqlite3.Row:
        cursor = self.connection.execute(
            "INSERT INTO media (user_id, filename, mime_type, size, data) "
            "VALUES (?, ?, ?, ?, ?)",
            (user_id, filename, mime_type, size, sqlite3.Binary(data)),
        )
        self.connection.commit()
        return self.find_by_id(user_id, cursor.lastrowid)

    def find_by_id(self, user_id: int, media_id: int) -> sqlite3.Row | None:
        return self.connection.execute(
            "SELECT * FROM media WHERE user_id = ? AND id = ?", (user_id, media_id)
        ).fetchone()

    def delete(self, user_id: int, media_id: int) -> None:
        self.connection.execute(
            "DELETE FROM media WHERE user_id = ? AND id = ?", (user_id, media_id)
        )
        self.connection.commit()
