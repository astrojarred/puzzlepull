import json
import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import Response

from xword_dl.util import XWordDLException

from puzzlepull.db import get_counter, increment_counter
from puzzlepull.guardian import get_guardian_puzzle
from puzzlepull.observer import get_observer_puzzle_sync
from puzzlepull.pull import get_puzzle_from_url

# xword-dl creates a config file under XDG_CONFIG_HOME on import/use.
os.environ.setdefault("XDG_CONFIG_HOME", "/tmp/xdg-config")

app = FastAPI()


def _download_or_json(puzzle: dict, download: bool):
    if download:
        return Response(
            content=json.dumps(puzzle),
            media_type="application/json",
            headers={
                "Content-Disposition": f"attachment;filename={puzzle['annotation']}"
            },
        )
    return puzzle


@app.get("/")
async def root():
    return {"message": "puzzlepull API"}


@app.get("/counter")
async def counter():
    return {"counter": get_counter()}


@app.get("/pull")
def pull_puzzle(url: str, download: bool = False):
    """Download a puzzle with xword-dl (native Guardian/Observer fallback)."""

    try:
        puzzle = get_puzzle_from_url(url)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except XWordDLException as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    increment_counter()
    return _download_or_json(puzzle, download)


@app.get("/guardian")
def guardian_puzzle(url: str, download: bool = False):
    """Scrape a puzzle from the Guardian website and convert to .ipuz."""

    puzzle = get_guardian_puzzle(url)
    increment_counter()
    return _download_or_json(puzzle, download)


@app.get("/observer")
def observer_puzzle(url: str, download: bool = False):
    """Scrape Observer Everyman/Speedy puzzles and convert to .ipuz."""

    puzzle = get_observer_puzzle_sync(url)
    increment_counter()
    return _download_or_json(puzzle, download)
