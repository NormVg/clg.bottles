"""Business rules: folder paths, item defaults, uploads, and search."""

from ...utils.files import sanitize_filename
from ...utils.paths import normalize_folder_path, parent_path_of, slugify_segment
from ...utils.urls import default_title_for
from .repository import FolderRepository, ItemRepository, MediaRepository

MAX_UPLOAD_BYTES = 25 * 1024 * 1024


class BookmarkService:
    def __init__(self, connection):
        self.folders = FolderRepository(connection)
        self.items = ItemRepository(connection)
        self.media = MediaRepository(connection)

    def list_directory(self, user_id: int, path: str) -> dict:
        canonical = normalize_folder_path(path) or "/"
        folder = None if canonical == "/" else self.folders.find_by_path(user_id, canonical)
        if canonical != "/" and folder is None:
            raise LookupError(f"no folder at {canonical}.")
        folder_id = folder["id"] if folder else None
        return {
            "path": canonical,
            "folder": dict(folder) if folder else None,
            "folders": [dict(row) for row in self.folders.list_children(user_id, folder_id)],
            "items": [
                self._item_dict(user_id, row)
                for row in self.items.list_by_folder(user_id, folder_id)
            ],
        }

    def list_folders(self, user_id: int) -> list[dict]:
        return [dict(row) for row in self.folders.list_all(user_id)]

    def ensure_folder_path(self, user_id: int, path: str):
        """mkdir -p: create every missing segment and return the leaf folder."""
        canonical = normalize_folder_path(path)
        if canonical is None:
            raise ValueError("that path is too deep.")
        if canonical == "/":
            return None
        parent_id = None
        current = ""
        leaf = None
        for segment in canonical.strip("/").split("/"):
            current = f"{current}/{segment}"
            folder = self.folders.find_by_path(user_id, current)
            if folder is None:
                folder = self.folders.create(user_id, parent_id, segment, current)
            parent_id = folder["id"]
            leaf = folder
        return leaf

    def create_folder(self, user_id: int, path: str) -> dict:
        canonical = normalize_folder_path(path)
        if canonical is None:
            raise ValueError("that path is too deep.")
        if canonical == "/":
            raise ValueError("the root folder already exists.")
        return dict(self.ensure_folder_path(user_id, canonical))

    def rename_folder(self, user_id: int, folder_id: int, name: str) -> dict:
        folder = self.folders.find_by_id(user_id, folder_id)
        if folder is None:
            raise LookupError("no such folder.")
        slug = slugify_segment(name)
        if not slug:
            raise ValueError("that name cannot become a folder.")
        parent = parent_path_of(folder["path"])
        new_path = f"/{slug}" if parent == "/" else f"{parent}/{slug}"
        if new_path != folder["path"]:
            sibling = self.folders.find_by_path(user_id, new_path)
            if sibling is not None and sibling["id"] != folder_id:
                raise ValueError("a folder with that name already exists here.")
            self.folders.update_path_prefix(user_id, folder["path"], new_path)
        return dict(self.folders.update(user_id, folder_id, name.strip()[:64], new_path))

    def delete_folder(self, user_id: int, folder_id: int) -> None:
        if self.folders.find_by_id(user_id, folder_id) is None:
            raise LookupError("no such folder.")
        self.folders.delete(user_id, folder_id)

    def create_item(
        self,
        user_id: int,
        item_type: str,
        title: str | None,
        url: str | None,
        note: str | None,
        path: str | None,
        media_id: int | None = None,
    ) -> dict:
        if item_type not in ("link", "note", "media"):
            raise ValueError("type must be link, note, or media.")
        if item_type == "link" and not url:
            raise ValueError("link items require a url.")
        if item_type == "note" and not note:
            raise ValueError("note items require a note.")
        if item_type == "media" and media_id is None:
            raise ValueError("media items require a media id.")
        folder = self.ensure_folder_path(user_id, path or "/")
        folder_id = folder["id"] if folder else None
        final_title = (title or "").strip()
        if not final_title:
            final_title = default_title_for(url) if item_type == "link" else "untitled"
        row = self.items.create(
            user_id, folder_id, item_type, final_title[:256], url, note, media_id
        )
        return self._item_dict(user_id, row)

    def update_item(
        self,
        user_id: int,
        item_id: int,
        title: str | None,
        url: str | None,
        note: str | None,
    ) -> dict:
        item = self.items.find_by_id(user_id, item_id)
        if item is None:
            raise LookupError("no such item.")
        new_title = title.strip()[:256] if title and title.strip() else item["title"]
        new_url = url if url is not None else item["url"]
        new_note = note if note is not None else item["note"]
        row = self.items.update(user_id, item_id, new_title, new_url, new_note)
        return self._item_dict(user_id, row)

    def delete_item(self, user_id: int, item_id: int) -> None:
        item = self.items.find_by_id(user_id, item_id)
        if item is None:
            raise LookupError("no such item.")
        self.items.delete(user_id, item_id)
        if item["media_id"]:
            self.media.delete(user_id, item["media_id"])

    def upload_media(
        self,
        user_id: int,
        filename: str,
        mime_type: str,
        data: bytes,
        path: str | None,
        title: str | None,
    ) -> dict:
        """Store the raw bytes in the database, then create the item."""
        if not data:
            raise ValueError("that file is empty.")
        if len(data) > MAX_UPLOAD_BYTES:
            raise ValueError("files up to 25 mb are supported.")
        clean_name = sanitize_filename(filename)
        media = self.media.create(
            user_id, clean_name, mime_type or "application/octet-stream", len(data), data
        )
        item = self.create_item(
            user_id, "media", title or clean_name, None, None, path, media["id"]
        )
        return {"media": self._media_dict(media), "item": item}

    def get_media(self, user_id: int, media_id: int) -> dict:
        row = self.media.find_by_id(user_id, media_id)
        if row is None:
            raise LookupError("no such media.")
        return self._media_dict(row)

    def get_media_row(self, user_id: int, media_id: int):
        row = self.media.find_by_id(user_id, media_id)
        if row is None:
            raise LookupError("no such media.")
        return row

    def search(self, user_id: int, query: str) -> dict:
        return {
            "folders": [dict(row) for row in self.folders.search(user_id, query)],
            "items": [
                self._item_dict(user_id, row)
                for row in self.items.search(user_id, query)
            ],
        }

    def _item_dict(self, user_id: int, row) -> dict:
        item = dict(row)
        item["media"] = None
        if row["media_id"]:
            media = self.media.find_by_id(user_id, row["media_id"])
            if media is not None:
                item["media"] = self._media_dict(media)
        return item

    @staticmethod
    def _media_dict(row) -> dict:
        return {
            "id": row["id"],
            "filename": row["filename"],
            "mime_type": row["mime_type"],
            "size": row["size"],
            "created_at": row["created_at"],
        }
