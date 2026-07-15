"""Download puzzles via xword-dl and convert them to ipuz."""

from __future__ import annotations

import os
from urllib.parse import urlparse

# Writable config dir for xword-dl's import-time config file creation.
os.environ.setdefault("XDG_CONFIG_HOME", "/tmp/xdg-config")

from xword_dl import by_keyword, by_url
from xword_dl.util import XWordDLException

from .guardian import get_guardian_puzzle
from .observer import get_observer_puzzle_sync
from .puz_to_ipuz import puz_to_ipuz
from .sources import (
    BLOCKED_SUFFIXES,
    KEYWORD_BY_SUFFIX,
    ORIGIN_BY_SUFFIX,
)


def _hostname(url: str) -> str:
    return urlparse(url).hostname or ""


def _suffix_match(hostname: str, suffixes: tuple[str, ...] | dict[str, str]) -> str | None:
    host = hostname.lower().removeprefix("www.")
    keys = suffixes.keys() if isinstance(suffixes, dict) else suffixes
    for suffix in keys:
        if host == suffix or host.endswith("." + suffix):
            return suffix
    return None


def is_blocked_url(url: str) -> bool:
    return _suffix_match(_hostname(url), BLOCKED_SUFFIXES) is not None


def is_allowed_url(url: str) -> bool:
    if is_blocked_url(url):
        return False
    return _suffix_match(_hostname(url), ORIGIN_BY_SUFFIX) is not None


def _origin_for_url(url: str) -> str:
    suffix = _suffix_match(_hostname(url), ORIGIN_BY_SUFFIX)
    if not suffix:
        return "puzzlepull"
    return ORIGIN_BY_SUFFIX[suffix]


def _keyword_for_url(url: str) -> str | None:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    path = parsed.path.lower()

    if "simplydailypuzzles.com" in host:
        if "cryptic" in path:
            return "sdpc"
        if "quick" in path:
            return "sdpq"
        return "sdp"

    if "newyorker.com" in host:
        # Section roots use keyword; dated article URLs rely on by_url.
        if path.rstrip("/") == "/puzzles-and-games-dept/mini-crossword":
            return "tnym"
        if path.rstrip("/") in {
            "/puzzles-and-games-dept/crossword",
            "",
        }:
            return "tny"

    if "puzzmo.com" in host:
        if "/crossword/big" in path or path.rstrip("/").endswith("/big"):
            return "pzmb"
        if path.rstrip("/") in {"", "/puzzle"} or "/crossword" not in path:
            return "pzm"

    if "latimes.com" in host and "mini" in path:
        return "latm"

    if "theguardian.com" in host:
        # Series / section roots -> latest via keyword. Numbered puzzle URLs use by_url.
        mapping = {
            "/crosswords/cryptic": "grdc",
            "/crosswords/series/cryptic": "grdc",
            "/crosswords/everyman": "grde",
            "/crosswords/series/everyman": "grde",
            "/crosswords/speedy": "grds",
            "/crosswords/series/speedy": "grds",
            "/crosswords/quick": "grdq",
            "/crosswords/series/quick": "grdq",
            "/crosswords/prize": "grdp",
            "/crosswords/series/prize": "grdp",
            "/crosswords/weekend": "grdw",
            "/crosswords/series/weekend": "grdw",
            "/crosswords/quiptic": "grdu",
            "/crosswords/series/quiptic": "grdu",
        }
        normalized = path.rstrip("/")
        if normalized in mapping:
            return mapping[normalized]
        # /crosswords/cryptic/29800 has an extra segment -> by_url only.

    if "observer.co.uk" in host:
        if "/everyman" in path and "/article/" not in path:
            return "ever"
        if "/speedy" in path and "/article/" not in path:
            return "spdy"

    if "universaluclick.com" in host or "amuniversal.com" in host:
        return "uni"

    if "puzzlenation.com" in host:
        return "pop"

    if "vulture.com" in host:
        return "vult"

    if "crosswordclub.com" in host:
        # Specific puzzle URLs work with by_url; index uses keyword.
        if path.rstrip("/") in {"", "/puzzles"}:
            return "club"

    if "billboard.com" in host:
        if path.rstrip("/") in {"", "/p", "/p/billboard-crossword"}:
            return "bill"

    suffix = _suffix_match(host, KEYWORD_BY_SUFFIX)
    if not suffix:
        return None
    return KEYWORD_BY_SUFFIX[suffix]


def _native_fallback(url: str) -> dict | None:
    host = _hostname(url).lower().removeprefix("www.")
    if host == "theguardian.com" or host.endswith(".theguardian.com"):
        return get_guardian_puzzle(url)
    if host == "observer.co.uk" or host.endswith(".observer.co.uk"):
        return get_observer_puzzle_sync(url)
    return None


def _to_ipuz(puzzle, filename: str, url: str) -> dict:
    origin = _origin_for_url(url)
    return puz_to_ipuz(
        puzzle,
        url=url,
        origin=origin,
        publisher=origin,
        filename=filename,
    )


def get_puzzle_from_url(url: str) -> dict:
    """Fetch a puzzle for a user-pasted URL and return ipuz JSON."""

    if not url:
        raise ValueError("URL is required")

    host = _hostname(url) or url
    if is_blocked_url(url):
        raise PermissionError(
            f"Host not supported (subscription/auth required or disabled): {host}"
        )

    if not is_allowed_url(url):
        raise PermissionError(f"Host not allowed: {host}")

    errors: list[str] = []

    # 1) Prefer URL matching when xword-dl recognizes the page.
    try:
        puzzle, filename = by_url(url, preserve_html=True)
        return _to_ipuz(puzzle, filename, url)
    except Exception as exc:
        errors.append(f"by_url: {exc}")

    # 2) Landing pages / keyword-only outlets.
    keyword = _keyword_for_url(url)
    if keyword:
        try:
            puzzle, filename = by_keyword(keyword, preserve_html=True)
            return _to_ipuz(puzzle, filename, url)
        except Exception as exc:
            errors.append(f"by_keyword({keyword}): {exc}")

    # 3) Native Guardian / Observer scrapers.
    try:
        fallback = _native_fallback(url)
        if fallback:
            return fallback
    except Exception as exc:
        errors.append(f"native: {exc}")

    raise XWordDLException(
        "Unable to download puzzle from {}. Tried: {}".format(url, " | ".join(errors))
    )
