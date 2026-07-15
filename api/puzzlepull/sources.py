"""Supported puzzle sources backed by xword-dl.

NYT outlets are intentionally excluded: they require authentication and are a
poor fit for a public URL-paste service.
"""

from __future__ import annotations

# Host suffix -> display name. Matching is "equals or subdomain of".
ORIGIN_BY_SUFFIX: dict[str, str] = {
    # Guardian / Observer
    "theguardian.com": "The Guardian",
    "observer.co.uk": "The Observer",
    # AmuseLabs-backed newspapers / magazines
    "latimes.com": "Los Angeles Times",
    "theatlantic.com": "The Atlantic",
    "vox.com": "Vox",
    "thedailybeast.com": "The Daily Beast",
    "newsday.com": "Newsday",
    "thewalrus.ca": "The Walrus",
    "derstandard.at": "Der Standard",
    "billboard.com": "Billboard",
    "crosswordclub.com": "Crossword Club",
    "vulture.com": "Vulture",
    # USA Today / Universal / Uclick
    "usatoday.com": "USA Today",
    "universaluclick.com": "Universal",
    "amuniversal.com": "Universal",
    "uclick.com": "USA Today / Universal",
    # New Yorker / Puzzmo
    "newyorker.com": "The New Yorker",
    "puzzmo.com": "Puzzmo",
    # Simply Daily
    "simplydailypuzzles.com": "Simply Daily Puzzles",
    # Washington Post
    "washingtonpost.com": "The Washington Post",
    "wapo.pub": "The Washington Post",
    # Daily Pop
    "puzzlenation.com": "Daily Pop",
    # Globe and Mail (URL match still works in xword-dl; no keyword)
    "theglobeandmail.com": "The Globe and Mail",
    # Generic AmuseLabs embeds / CDNs
    "amuselabs.com": "AmuseLabs",
}

# Landing pages / keyword-only outlets -> xword-dl command.
# More specific path rules are handled in pull._keyword_for_url().
KEYWORD_BY_SUFFIX: dict[str, str] = {
    "usatoday.com": "usa",
    "uclick.com": "usa",
    "universaluclick.com": "uni",
    "amuniversal.com": "uni",
    "washingtonpost.com": "wp",
    "wapo.pub": "wp",
    "latimes.com": "lat",
    "theatlantic.com": "atl",
    "vox.com": "vox",
    "thedailybeast.com": "db",
    "newsday.com": "nd",
    "thewalrus.ca": "wal",
    "derstandard.at": "std",
    "billboard.com": "bill",
    "crosswordclub.com": "club",
    "vulture.com": "vult",
    "puzzlenation.com": "pop",
    "puzzmo.com": "pzm",
}

# Human-facing compatibility list (unique display names, stable order).
COMPATIBLE_SITES: list[str] = [
    "The Guardian",
    "The Observer (Everyman & Speedy)",
    "USA Today",
    "Universal",
    "The Washington Post",
    "The New Yorker (+ Mini)",
    "Los Angeles Times (+ Mini)",
    "The Atlantic",
    "Vox",
    "The Daily Beast",
    "Newsday",
    "The Walrus",
    "Der Standard",
    "Billboard",
    "Crossword Club",
    "Vulture",
    "Simply Daily Puzzles (American, Cryptic, Quick)",
    "Puzzmo (+ Big)",
    "Daily Pop",
    "The Globe and Mail",
    "AmuseLabs CDN embeds",
]

# Frontend hostname allowlist: exact host -> display name.
# Includes common www / product subdomains used in paste URLs.
FRONTEND_HOSTNAMES: dict[str, str] = {
    "localhost": "localhost",
    # Guardian / Observer
    "www.theguardian.com": "The Guardian",
    "theguardian.com": "The Guardian",
    "observer.co.uk": "The Observer",
    "www.observer.co.uk": "The Observer",
    # LAT / Atlantic / Vox / Daily Beast / Newsday / Walrus / Der Standard
    "www.latimes.com": "Los Angeles Times",
    "latimes.com": "Los Angeles Times",
    "www.theatlantic.com": "The Atlantic",
    "theatlantic.com": "The Atlantic",
    "www.vox.com": "Vox",
    "vox.com": "Vox",
    "www.thedailybeast.com": "The Daily Beast",
    "thedailybeast.com": "The Daily Beast",
    "www.newsday.com": "Newsday",
    "newsday.com": "Newsday",
    "thewalrus.ca": "The Walrus",
    "www.thewalrus.ca": "The Walrus",
    "www.derstandard.at": "Der Standard",
    "derstandard.at": "Der Standard",
    # USA Today / Universal
    "puzzles.usatoday.com": "USA Today",
    "play.usatoday.com": "USA Today",
    "www.usatoday.com": "USA Today",
    "usatoday.com": "USA Today",
    "embed.universaluclick.com": "Universal",
    "www.universaluclick.com": "Universal",
    "universaluclick.com": "Universal",
    "picayune.uclick.com": "USA Today / Universal",
    "gamedata.services.amuniversal.com": "Universal",
    # Simply Daily
    "simplydailypuzzles.com": "Simply Daily Puzzles",
    "www.simplydailypuzzles.com": "Simply Daily Puzzles",
    # WaPo
    "www.washingtonpost.com": "The Washington Post",
    "washingtonpost.com": "The Washington Post",
    "games-service-prod.site.aws.wapo.pub": "The Washington Post",
    # New Yorker / Puzzmo
    "www.newyorker.com": "The New Yorker",
    "newyorker.com": "The New Yorker",
    "www.puzzmo.com": "Puzzmo",
    "puzzmo.com": "Puzzmo",
    # Billboard / Club / Vulture
    "www.billboard.com": "Billboard",
    "billboard.com": "Billboard",
    "www.crosswordclub.com": "Crossword Club",
    "crosswordclub.com": "Crossword Club",
    "www.vulture.com": "Vulture",
    "vulture.com": "Vulture",
    # Daily Pop
    "api.puzzlenation.com": "Daily Pop",
    "dailypopcrosswordsweb.puzzlenation.com": "Daily Pop",
    "www.puzzlenation.com": "Daily Pop",
    "puzzlenation.com": "Daily Pop",
    # Globe and Mail
    "www.theglobeandmail.com": "The Globe and Mail",
    "theglobeandmail.com": "The Globe and Mail",
    # AmuseLabs CDNs
    "cdn2.amuselabs.com": "AmuseLabs",
    "cdn3.amuselabs.com": "AmuseLabs",
    "cdn-eu1.amuselabs.com": "AmuseLabs",
    "www.amuselabs.com": "AmuseLabs",
    "amuselabs.com": "AmuseLabs",
}

# Explicitly blocked (auth / disabled upstream).
BLOCKED_SUFFIXES: tuple[str, ...] = (
    "nytimes.com",
    "wsj.com",
    "mckinsey.com",
    "puzzlesociety.com",
)
