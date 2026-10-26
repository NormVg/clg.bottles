"""Page previews: the title and og:image for a link, cached in memory."""

import re
import ssl
import time
import urllib.request
from urllib.parse import urljoin

import certifi

CACHE_TTL = 6 * 60 * 60
CACHE_MAX = 500

SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())

BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)

_cache: dict[str, tuple[float, dict]] = {}

TITLE_PATTERNS = [
    re.compile(r'<meta[^>]+property=["\']og:title["\'][^>]*?content=["\']([^"\']+)["\']', re.I),
    re.compile(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]*?property=["\']og:title["\']', re.I),
    re.compile(r'<meta[^>]+name=["\']twitter:title["\'][^>]*?content=["\']([^"\']+)["\']', re.I),
    re.compile(r"<title[^>]*>([^<]+)</title>", re.I),
]

IMAGE_PATTERNS = [
    re.compile(
        r'<meta[^>]+property=["\']og:image(?::secure_url)?["\'][^>]*?content=["\']([^"\']+)["\']',
        re.I,
    ),
    re.compile(
        r'<meta[^>]+content=["\']([^"\']+)["\'][^>]*?property=["\']og:image(?::secure_url)?["\']',
        re.I,
    ),
    re.compile(
        r'<meta[^>]+name=["\']twitter:image(?::src)?["\'][^>]*?content=["\']([^"\']+)["\']',
        re.I,
    ),
]


def resolve_page_preview(url: str) -> dict:
    """One cached fetch per url; hovers repeat constantly."""
    now = time.time()
    hit = _cache.get(url)
    if hit and hit[0] > now:
        return hit[1]

    preview = _fetch_preview(url)
    if len(_cache) >= CACHE_MAX:
        oldest = next(iter(_cache))
        _cache.pop(oldest, None)
    _cache[url] = (now + CACHE_TTL, preview)
    return preview


def _fetch_preview(url: str) -> dict:
    try:
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": BROWSER_UA,
                "Accept": "text/html,application/xhtml+xml",
                "Accept-Language": "en-US,en;q=0.9",
            },
        )
        with urllib.request.urlopen(request, timeout=5, context=SSL_CONTEXT) as response:
            content_type = response.headers.get("Content-Type", "")
            if "text/html" not in content_type and "xhtml" not in content_type:
                return {"title": None, "image": None}
            html = response.read(1_500_000).decode("utf-8", errors="ignore")
            base = response.geturl() or url
            return {"title": _first(html, TITLE_PATTERNS), "image": _image(html, base)}
    except Exception:
        return {"title": None, "image": None}


def _first(html: str, patterns: list[re.Pattern]) -> str | None:
    for pattern in patterns:
        match = pattern.search(html)
        if match and match.group(1):
            return _clean(match.group(1))
    return None


def _clean(raw: str) -> str | None:
    text = re.sub(r"\s+", " ", raw).strip()
    return text[:256] or None


def _image(html: str, base: str) -> str | None:
    raw = _first(html, IMAGE_PATTERNS)
    if not raw:
        return None
    try:
        absolute = urljoin(base, raw)
        return absolute if absolute.startswith(("http://", "https://")) else None
    except Exception:
        return None
