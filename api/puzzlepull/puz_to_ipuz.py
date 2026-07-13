"""Convert a puzpy Puzzle into puzzlepull's ipuz-shaped dict."""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any

from puz import Puzzle


def _safe_filename(name: str) -> str:
    cleaned = re.sub(r"[^\w.\-]+", "_", name).strip("._")
    if not cleaned:
        cleaned = "puzzle"
    if not cleaned.endswith(".ipuz"):
        cleaned += ".ipuz"
    return cleaned


def _annotation_from_filename(filename: str | None, fallback: str) -> str:
    if not filename:
        return _safe_filename(fallback)
    name = filename.strip()
    if name.endswith(".puz"):
        name = name[: -len(".puz")]
    if name.endswith(".ipuz"):
        name = name[: -len(".ipuz")]
    return _safe_filename(name)


def puz_to_ipuz(
    puzzle: Puzzle,
    *,
    url: str,
    origin: str | None = None,
    publisher: str | None = None,
    date: datetime | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Build an ipuz v2 crossword dict from a puz.Puzzle."""

    width = int(puzzle.width)
    height = int(puzzle.height)
    numbering = puzzle.clue_numbering()

    grid: list[list[Any]] = []
    solution: list[list[str]] = []
    letter_count = 0

    for y in range(height):
        grid_row: list[Any] = []
        sol_row: list[str] = []
        for x in range(width):
            idx = y * width + x
            cell = puzzle.solution[idx]
            if cell == ".":
                grid_row.append("#")
                sol_row.append("#")
            else:
                grid_row.append(0)
                if cell and cell not in {"-", " "}:
                    sol_row.append(cell)
                    letter_count += 1
                else:
                    sol_row.append(" ")
        grid.append(grid_row)
        solution.append(sol_row)

    for entry in numbering.across + numbering.down:
        cell = entry["cell"]
        y, x = divmod(cell, width)
        grid[y][x] = entry["num"]

    across = [[entry["num"], entry["clue"]] for entry in numbering.across]
    down = [[entry["num"], entry["clue"]] for entry in numbering.down]

    origin_name = origin or "puzzlepull"
    publisher_name = publisher or origin_name

    ipuz: dict[str, Any] = {
        "origin": origin_name,
        "version": "http://ipuz.org/v2",
        "kind": ["http://ipuz.org/crossword"],
        "copyright": puzzle.copyright or "",
        "publisher": publisher_name,
        "url": url,
        "title": puzzle.title or "",
        "dimensions": {"width": width, "height": height},
        "puzzle": grid,
        "clues": {"Across": across, "Down": down},
    }

    if puzzle.author:
        ipuz["author"] = puzzle.author

    if date:
        ipuz["date"] = date.strftime("%m/%d/%Y")

    if letter_count:
        ipuz["solution"] = solution

    ipuz["annotation"] = _annotation_from_filename(
        filename, f"{origin_name}_{puzzle.title or 'puzzle'}"
    )
    return ipuz
