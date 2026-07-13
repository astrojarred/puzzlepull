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

# Free / publicly pasteable hosts we are willing to fetch for users.
# Keep NYT and other auth-gated outlets off this list.
ALLOWED_SUFFIXES = (
    "theguardian.com",
    "observer.co.uk",
    "latimes.com",
    "theatlantic.com",
    "vox.com",
    "thedailybeast.com",
    "newsday.com",
    "thewalrus.ca",
    "derstandard.at",
    "usatoday.com",
    "simplydailypuzzles.com",
    "washingtonpost.com",
    "newyorker.com",
    "billboard.com",
    "dailyprincetonian.com",
    "mckinsey.com",
    "amuselabs.com",
    "amuniversal.com",
)

ORIGIN_BY_SUFFIX = {
    "theguardian.com": "The Guardian",
    "observer.co.uk": "The Observer",
    "latimes.com": "Los Angeles Times",
    "theatlantic.com": "The Atlantic",
    "vox.com": "Vox",
    "thedailybeast.com": "The Daily Beast",
    "newsday.com": "Newsday",
    "thewalrus.ca": "The Walrus",
    "derstandard.at": "Der Standard",
    "usatoday.com": "USA Today",
    "simplydailypuzzles.com": "Simply Daily Puzzles",
    "washingtonpost.com": "The Washington Post",
    "newyorker.com": "The New Yorker",
    "billboard.com": "Billboard",
    "dailyprincetonian.com": "The Daily Princetonian",
    "mckinsey.com": "McKinsey",
    "amuselabs.com": "AmuseLabs",
    "amuniversal.com": "Universal",
}

# Outlets where xword-dl is keyword-oriented (or landing pages don't match_url).
KEYWORD_BY_SUFFIX = {
    "usatoday.com": "usa",
    "washingtonpost.com": "wp",
    "latimes.com": "lat",
    "theatlantic.com": "atl",
    "vox.com": "vox",
    "thedailybeast.com": "db",
    "newsday.com": "nd",
    "thewalrus.ca": "wal",
    "derstandard.at": "std",
    "billboard.com": "bill",
}


def _hostname(url: str) -> str:
    return urlparse(url).hostname or ""


def _allowed_suffix(hostname: str) -> str | None:
    host = hostname.lower().removeprefix("www.")
    for suffix in ALLOWED_SUFFIXES:
        if host == suffix or host.endswith("." + suffix):
            return suffix
    return None


def is_allowed_url(url: str) -> bool:
    return _allowed_suffix(_hostname(url)) is not None


def _origin_for_url(url: str) -> str:
    suffix = _allowed_suffix(_hostname(url))
    if not suffix:
        return "puzzlepull"
    return ORIGIN_BY_SUFFIX.get(suffix, suffix)


def _keyword_for_url(url: str) -> str | None:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower().removeprefix("www.")
    path = parsed.path.lower()

    if "simplydailypuzzles.com" in host:
        if "cryptic" in path:
            return "sdpc"
        if "quick" in path:
            return "sdpq"
        return "sdp"

    if "newyorker.com" in host:
        if "mini" in path:
            return "tnym"
        # Dated crossword article URLs are handled by by_url; landing pages use keyword.
        if path.rstrip("/") in {
            "/puzzles-and-games-dept/crossword",
            "/puzzles-and-games-dept/mini-crossword",
            "",
        }:
            return "tny"

    suffix = _allowed_suffix(host)
    if not suffix:
        return None
    return KEYWORD_BY_SUFFIX.get(suffix)


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

    if not is_allowed_url(url):
        raise PermissionError(f"Host not allowed: {_hostname(url) or url}")

    errors: list[str] = []

    # 1) Prefer URL matching when xword-dl recognizes the page.
    try:
        puzzle, filename = by_url(url, preserve_html=True)
        return _to_ipuz(puzzle, filename, url)
    except Exception as exc:
        errors.append(f"by_url: {exc}")

    # 2) Landing pages / keyword-only outlets (USA Today, WaPo, etc.).
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
