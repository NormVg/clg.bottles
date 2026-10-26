"""SQL for folders and items. No business rules live here."""

import sqlite3


class FolderRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def list_all(self) -> list[sqlite3.Row]:
        return self.connection.execute("SELECT * FROM folders ORDER BY path").fetchall()

    def find_by_path(self, path: str) -> sqlite3.Row | None:
        return self.connection.execute(
            "SELECT * FROM folders WHERE path = ?", (path,)
        ).fetchone()

    def find_by_id(self, folder_id: int) -> sqlite3.Row | None:
        return self.connection.execute(
            "SELECT * FROM folders WHERE id = ?", (folder_id,)
        ).fetchone()

    def list_children(self, parent_id: int | None) -> list[sqlite3.Row]:
        if parent_id is None:
            return self.connection.execute(
                "SELECT * FROM folders WHERE parent_id IS NULL ORDER BY name"
            ).fetchall()
        return self.connection.execute(
            "SELECT * FROM folders WHERE parent_id = ? ORDER BY name", (parent_id,)
        ).fetchall()

    def create(self, parent_id: int | None, name: str, path: str) -> sqlite3.Row:
        cursor = self.connection.execute(
            "INSERT INTO folders (parent_id, name, path) VALUES (?, ?, ?)",
            (parent_id, name, path),
        )
        self.connection.commit()
        return self.find_by_id(cursor.lastrowid)

    def update(self, folder_id: int, name: str, path: str) -> sqlite3.Row:
        self.connection.execute(
            "UPDATE folders SET name = ?, path = ? WHERE id = ?",
            (name, path, folder_id),
        )
        self.connection.commit()
        return self.find_by_id(folder_id)

    def update_path_prefix(self, old_path: str, new_path: str) -> None:
        """Move a folder and everything under it in one statement."""
        self.connection.execute(
            "UPDATE folders SET path = ? || substr(path, ?) WHERE path = ? OR path LIKE ?",
            (new_path, len(old_path) + 1, old_path, old_path + "/%"),
        )
        self.connection.commit()

    def delete(self, folder_id: int) -> None:
        self.connection.execute("DELETE FROM folders WHERE id = ?", (folder_id,))
        self.connection.commit()

    def search(self, query: str) -> list[sqlite3.Row]:
        return self.connection.execute(
            "SELECT * FROM folders WHERE path LIKE ? ORDER BY path LIMIT 50",
            (f"%{query}%",),
        ).fetchall()


class ItemRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def list_by_folder(self, folder_id: int | None) -> list[sqlite3.Row]:
        if folder_id is None:
            return self.connection.execute(
                "SELECT * FROM items WHERE folder_id IS NULL ORDER BY created_at DESC, title"
            ).fetchall()
        return self.connection.execute(
            "SELECT * FROM items WHERE folder_id = ? ORDER BY created_at DESC, title",
            (folder_id,),
        ).fetchall()

    def find_by_id(self, item_id: int) -> sqlite3.Row | None:
        return self.connection.execute(
            "SELECT * FROM items WHERE id = ?", (item_id,)
        ).fetchone()

    def create(
        self,
        folder_id: int | None,
        item_type: str,
        title: str,
        url: str | None,
        note: str | None,
        media_id: int | None = None,
    ) -> sqlite3.Row:
        cursor = self.connection.execute(
            "INSERT INTO items (folder_id, type, title, url, note, media_id) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (folder_id, item_type, title, url, note, media_id),
        )
        self.connection.commit()
        return self.find_by_id(cursor.lastrowid)

    def update(
        self, item_id: int, title: str, url: str | None, note: str | None
    ) -> sqlite3.Row:
        self.connection.execute(
            "UPDATE items SET title = ?, url = ?, note = ?, updated_at = datetime('now') "
            "WHERE id = ?",
            (title, url, note, item_id),
        )
        self.connection.commit()
        return self.find_by_id(item_id)

    def delete(self, item_id: int) -> None:
        self.connection.execute("DELETE FROM items WHERE id = ?", (item_id,))
        self.connection.commit()

    def search(self, query: str) -> list[sqlite3.Row]:
        pattern = f"%{query}%"
        return self.connection.execute(
            "SELECT * FROM items WHERE title LIKE ? OR url LIKE ? OR note LIKE ? "
            "ORDER BY created_at DESC LIMIT 50",
            (pattern, pattern, pattern),
        ).fetchall()


class MediaRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def create(
        self, filename: str, mime_type: str, size: int, data: bytes
    ) -> sqlite3.Row:
        cursor = self.connection.execute(
            "INSERT INTO media (filename, mime_type, size, data) VALUES (?, ?, ?, ?)",
            (filename, mime_type, size, sqlite3.Binary(data)),
        )
        self.connection.commit()
        return self.find_by_id(cursor.lastrowid)

    def find_by_id(self, media_id: int) -> sqlite3.Row | None:
        return self.connection.execute(
            "SELECT * FROM media WHERE id = ?", (media_id,)
        ).fetchone()

    def delete(self, media_id: int) -> None:
        self.connection.execute("DELETE FROM media WHERE id = ?", (media_id,))
        self.connection.commit()
