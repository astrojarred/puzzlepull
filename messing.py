import ipuz
import requests
from bs4 import BeautifulSoup

URL = "https://www.theguardian.com/crosswords/accessible/quiptic/1103"

page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

# notes:
# <div class="crossword__accessible-data">

# Extract clues
# =============

# get the across and down clues class
across = soup.find("div", class_="crossword__clues--across").find_all(
    "li", class_="crossword__clue"
)
down = soup.find("div", class_="crossword__clues--down").find_all(
    "li", class_="crossword__clue"
)

# create dictionaries for the clues
clues = dict()
clues["across"] = []
clues["down"] = []

# extract the clues from the divs to a list
for clue in across:
    value = int(clue.get_attribute_list("value")[0])
    close_parenthesis = clue.get_text().find(")") + 2
    text = clue.get_text()[close_parenthesis:]
    clues["across"].append([value, text])

for clue in down:
    value = int(clue.get_attribute_list("value")[0])
    close_parenthesis = clue.get_text().find(")") + 2
    text = clue.get_text()[close_parenthesis:]
    clues["down"].append([value, text])

# Extract puzzle structure
# ========================

size = [15, 15]
row_data = soup.find("div", class_="crossword__accessible-data")

row_data.find_all("li", class_="crossword__accessible-row-data")[0].get_text()

row_data
