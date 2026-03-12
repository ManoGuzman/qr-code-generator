"""Filename sanitization utilities."""


def sanitize_filename(url: str) -> str:
    """
    Turn a URL into a safe, readable filename (without extension).

    Applies the following transformations in order:
    - Strips ``https://`` and ``http://`` scheme prefixes.
    - Replaces ``/`` with ``_``.
    - Removes ``:`` characters.
    - Replaces ``?``, ``&``, and ``=`` with ``_``.
    - Strips leading/trailing underscores produced by the replacements above.
    - Truncates the result to a maximum of 120 characters.

    Args:
        url (str): The raw URL string to sanitize.

    Returns:
        str: A filesystem-safe string suitable for use as a filename stem.
    """
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
