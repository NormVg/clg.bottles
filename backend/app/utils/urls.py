"""Small url helpers."""


def default_title_for(url: str) -> str:
    """A link's title when the user gives none: the hostname, no www."""
    without_scheme = url.split("://", 1)[-1]
    host = without_scheme.split("/", 1)[0]
    return host.replace("www.", "", 1) or url
