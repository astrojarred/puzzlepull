import datetime
import json

import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI
from fastapi.responses import Response

from puzzlepull.guardian import get_guardian_puzzle

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/guardian")
def guardian_puzzle(url: str, download: bool = False):
    """Scrape a puzzle from the Guardian website and
    convert to .ipuz (JSON) format."""

    print(f"The URL provided is: {url}")

    puzzle = get_guardian_puzzle(url, download=False)

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
