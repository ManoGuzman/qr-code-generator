"""Filename sanitization utilities."""


def sanitize_filename(url: str) -> str:
    """Turn a URL into a safe, readable filename."""
    return (
        url.replace("https://", "")
        .replace("http://", "")
        .replace("/", "_")
        .replace(":", "")
        .replace("?", "_")
        .replace("&", "_")
        .replace("=", "_")
        .strip("_")[:120]
    )
