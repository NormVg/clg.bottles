"""Folder path rules: lowercase kebab segments, leading slash, no trailing slash."""

import re

MAX_DEPTH = 16
MAX_NAME_LENGTH = 64


def slugify_segment(name: str) -> str:
    """Turn a display name into a path segment: "Machine Learning" -> "machine-learning"."""
    text = name.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text[:MAX_NAME_LENGTH].rstrip("-")


def normalize_folder_path(raw: str) -> str | None:
    """Normalize user input to "/a/b", or None when the path is too deep."""
    segments = [slugify_segment(part) for part in raw.split("/")]
    segments = [segment for segment in segments if segment]
    if not segments:
        return "/"
    if len(segments) > MAX_DEPTH:
        return None
    return "/" + "/".join(segments)


def parent_path_of(path: str) -> str:
    """Parent of a canonical path: "/a/b" -> "/a", "/a" -> "/"."""
    segments = [part for part in path.split("/") if part]
    segments.pop()
    return "/" + "/".join(segments)
