import json

from fastapi import FastAPI
from fastapi.responses import Response

from puzzlepull.guardian import get_guardian_puzzle
from puzzlepull.observer import get_observer_puzzle_sync
from puzzlepull.db import increment_counter, get_counter

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "puzzlepull API"}

@app.get("/counter")
async def counter():
    return {"counter": get_counter()}


@app.get("/guardian")
def guardian_puzzle(url: str, download: bool = False):
    """Scrape a puzzle from the Guardian website and
    convert to .ipuz (JSON) format."""

    print(f"The URL provided is: {url}")

    print(f"Current counter: {get_counter()}")

    puzzle = get_guardian_puzzle(url, download=download)

    increment_counter()

    print(f"Incremented counter: {get_counter()}")

    if download:
        return Response(
            content=json.dumps(puzzle),
            media_type="application/json",
            headers={
                "Content-Disposition": f"attachment;filename={puzzle['annotation']}"
            },
        )
    else:
        return puzzle


@app.get("/observer")
def observer_puzzle(url: str, download: bool = False):
    """Scrape a puzzle from the Observer website and
    convert to .ipuz (JSON) format.

    NOTE: Only compatible with the Everyman and Speedy puzzles.
    """

    print(f"Current counter: {get_counter()}")

    puzzle = get_observer_puzzle_sync(url)

    increment_counter()

    print(f"Incremented counter: {get_counter()}")

    if download:
        return Response(
            content=json.dumps(puzzle),
            media_type="application/json",
            headers={
                "Content-Disposition": f"attachment;filename={puzzle['annotation']}"
            },
        )
    else:
        return puzzle
