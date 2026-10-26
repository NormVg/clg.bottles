"""Filename rules for uploads."""

import re


def sanitize_filename(raw: str) -> str:
    base = raw.split("/")[-1].split("\\")[-1] or "file"
    cleaned = re.sub(r"[^a-zA-Z0-9._ -]", "", base)
    cleaned = re.sub(r"\s+", "-", cleaned).strip("-")
    return cleaned[:120] or "file"
