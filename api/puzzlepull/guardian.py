import datetime
import json

import requests
from bs4 import BeautifulSoup

from .helper import make_blank_puzzle
from .db import increment_counter as increment

# get the solution from the entries
def get_solution(data: dict, width: int = 15, height: int = 15) -> list[list[str]]:
    blank_puzzle = make_blank_puzzle(width, height)

    # fill in across answers to solution
    for clue in data["entries"]:
        x = clue["position"]["x"]
        y = clue["position"]["y"]
        length = clue["length"]
        solution = clue.get("solution")
        if not solution:
            return
        if clue["direction"] == "across":
            blank_puzzle[y][x : x + length] = list(solution)
        elif clue["direction"] == "down":
            for index, row in enumerate(range(y, y + length)):
                blank_puzzle[row][x] = solution[index]

    return blank_puzzle


# get the puzzle layout
def get_layout(data: dict, width: int = 15, height: int = 15) -> list[list[str]]:
    blank_puzzle = make_blank_puzzle(width, height)

    # fill in across answers to solution
    # across first
    for clue in data["entries"]:
        x = clue["position"]["x"]
        y = clue["position"]["y"]
        length = clue["length"]
        number = clue["number"]
        blank_puzzle[y][x] = number
        if clue["direction"] == "across":
            blank_puzzle[y][x + 1 : x + length] = [0] * (length - 1)

    # down next
    for clue in data["entries"]:
        x = clue["position"]["x"]
        y = clue["position"]["y"]
        length = clue["length"]
        number = clue["number"]
        blank_puzzle[y][x] = number
        if clue["direction"] == "down":
            for index, row in enumerate(range(y + 1, y + length)):
                if blank_puzzle[row][x] == "#":
                    blank_puzzle[row][x] = 0

    return blank_puzzle


# get the clues from the entry
def get_clues(data: dict) -> dict:
    clues = dict()
    clues["Across"] = []
    clues["Down"] = []

    for clue in data["entries"]:
        number = clue["number"]
        text = clue["clue"]
        direction = clue["direction"]

        clues[direction.capitalize()].append([number, text])

    return clues


def get_guardian_puzzle(URL: str, filepath: str = None, download: bool = True, increment_counter: bool = True) -> dict:
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    js_crossword = soup.find("gu-island", attrs={"name": "CrosswordComponent"})
    data = json.loads(js_crossword.get_attribute_list("props")[0]).get("data")

    if not data:
        return

    # get the datetime
    dt = datetime.datetime.fromtimestamp(data["date"] / 1000)
    width = int(data["dimensions"]["cols"])
    height = int(data["dimensions"]["rows"])

    puzzle = dict()
    puzzle["origin"] = "The Guardian"
    puzzle["version"] = "http://ipuz.org/v2"
    puzzle["kind"] = ["http://ipuz.org/crossword"]
    puzzle["copyright"] = f"{dt.year} Guardian News & Media Limited"

    try:
        puzzle["author"] = data["creator"]["name"]
    except KeyError:
        pass  # no author!

    puzzle["publisher"] = "The Guardian"
    puzzle["url"] = URL
    puzzle["title"] = data["name"]
    puzzle["date"] = dt.strftime("%m/%d/%Y")
    # puzzle["annotation"] = f"Puzzle type: {data['crosswordType']}"
    puzzle["dimensions"] = dict(width=width, height=height)

    puzzle["puzzle"] = get_layout(data, width, height)
    puzzle["clues"] = get_clues(data)
    solution = get_solution(data, width, height)

    if solution:
        puzzle["solution"] = solution

    filename = f"Guardian_{data['crosswordType']}_{data['number']}.ipuz"
    puzzle["annotation"] = filename

    if not filepath:
        filepath = "."

    if download:
        with open(f"{filepath}/{filename}", "w") as outfile:
            json.dump(puzzle, outfile)

    if increment_counter:
        new_count = increment()
        print(f"Puzzle pulled: {new_count}")

    return puzzle
