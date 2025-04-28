import asyncio
import datetime
import json
import requests
from urllib.parse import quote

from bs4 import BeautifulSoup

from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright

from .db import increment_counter as increment


def generate_xword_url(
    url: str, uid: str = "dd9a2d93-741d-493c-975c-cbe37256c8cc"
) -> str:
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    # find div with class pm-embed-div
    div = soup.find("div", class_="pm-embed-div")

    # get the data-id attribute
    data_id = div.get("data-id")

    # data-set is the set name
    data_set = div.get("data-set")

    xword_url = f"https://cdn2.amuselabs.com/puzzleme/crossword?&set={data_set}&embed=js&id={data_id}&uid={uid}&src={quote(url, safe='')}"
    return xword_url


async def get_rendered_puzzle_html_async(url):
    async with async_playwright() as p:
        # print("launching browser")
        browser = await p.chromium.launch(headless=True)
        # print("browser launched")
        page = await browser.new_page()
        # print("page created")
        await page.goto(url)
        # print("page navigated")
        await page.wait_for_selector(".player-transition-in", timeout=5000)
        # print("puzzle container found")
        html = await page.content()
        # print("html content retrieved")
        await browser.close()
        # print("browser closed")
        return html


def get_rendered_puzzle_html_sync(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_selector(".player-transition-in", timeout=5000)
        return page.content()


def parse_crossword_clues(soup: BeautifulSoup, is_across: bool) -> list:
    """
    Parses either the Across or Down clues from the provided soup
    into a list of lists format [number, text_with_lengths].

    Args:
        soup: The BeautifulSoup object of the rendered puzzle page.
        is_across: A boolean flag. True to parse Across clues, False for Down clues.

    Returns:
        A list of lists, where each inner list contains [clue_number_integer,
        "clue text (word lengths)"]. Returns an empty list if the specified
        clue section is not found or no clues are found within it, or if
        essential data for a clue is missing or malformed.
    """

    # List to store the clues in the new format [number, text]
    clues_list_format = []

    # Determine the CSS class based on the is_across flag
    section_class = "aclues" if is_across else "dclues"
    clue_direction = "Across" if is_across else "Down"

    print(f"Attempting to parse {clue_direction} clues...")

    # Find the div containing the list of clues for the specified direction
    # We look for the 'clue-list' div inside the specific section div
    clue_list_div = soup.select_one(f"div.{section_class} div.clue-list")

    if not clue_list_div:
        print(
            f"Warning: Could not find '{section_class}' section (for {clue_direction} clues) in the HTML."
        )
        return []  # Return empty list if the section is not found

    # Find all individual clue divs within the clue-list
    clue_divs = clue_list_div.find_all("div", class_="clueDiv")

    if not clue_divs:
        print(
            f"Warning: No 'clueDiv' elements found within the '{section_class}' section."
        )
        return []  # Return empty list if no clue divs are found

    print(f"Found {len(clue_divs)} {clue_direction} clue divs.")

    for clue_div in clue_divs:
        clue_number_element = clue_div.find("div", class_="clueNum")
        clue_text_element = clue_div.find("span", class_="clueText")
        word_lens_element = clue_div.find("span", class_="wordlens")

        # Extract raw text, stripping whitespace
        clue_number_raw = (
            clue_number_element.get_text(strip=True) if clue_number_element else None
        )
        clue_text = (
            clue_text_element.get_text(strip=True) if clue_text_element else None
        )
        word_lens_raw = (
            word_lens_element.get_text(strip=True) if word_lens_element else None
        )  # Keep parentheses and format

        # --- Formatting for the new output structure ---

        # 1. Parse clue number as integer
        clue_number_int = None
        if clue_number_raw:
            try:
                # Remove zero-width joiner (\u200d) if present before converting
                num_str_cleaned = clue_number_raw.replace("\u200d", "")
                clue_number_int = int(num_str_cleaned)
            except ValueError:
                print(
                    f"Warning: Could not parse clue number '{clue_number_raw}' into an integer for a {clue_direction} clue. Skipping clue."
                )
                # If number parsing fails, we cannot form the required [number, text] structure for this clue
                continue  # Skip to the next clue_div

        # 2. Combine clue text and word lengths
        # The required format is "Clue text (Word lengths)"
        combined_text = None
        if clue_text is not None and word_lens_raw is not None:
            combined_text = f"{clue_text} {word_lens_raw}"
        else:
            # If either text or word_lens is missing, we can't form the combined text
            # Print a warning if the number was successfully parsed, otherwise the number parsing warning is enough
            if clue_number_int is not None:
                print(
                    f"Warning: Clue {clue_number_int} ({clue_direction}) is missing text or word lengths. Skipping clue."
                )
            continue  # Skip to the next clue_div

        # 3. Append to the results list in the specified format
        # We only append if the number parsing was successful AND we successfully combined the text
        if clue_number_int is not None and combined_text is not None:
            clues_list_format.append([clue_number_int, combined_text])

    return clues_list_format


def parse_crossword_grid(soup: BeautifulSoup) -> list[list]:
    """
    Parses the crossword grid structure from the provided BeautifulSoup object.

    Args:
        soup: The BeautifulSoup object of the rendered puzzle page.

    Returns:
        A 2D list representing the grid. Black squares are '#',
        numbered white squares have their number (integer), and
        empty white squares are 0. Returns an empty list if the
        grid container is not found or no grid data is present.
    """

    grid = []
    current_row = []

    # Find the main grid container
    crossword_div = soup.find("div", class_="crossword")

    if not crossword_div:
        print("Warning: Could not find the main 'crossword' div.")
        return []  # Return empty grid if container not found

    # Iterate through the direct children of the crossword div
    # The children are either box divs or endRow divs, which correctly structures the rows
    for child in crossword_div.children:
        # Check if the child is a Tag (specifically a div)
        if child.name == "div":
            classes = child.get("class", [])  # Get classes as a list

            if "box" in classes:
                # This is a grid cell
                cell_value = 0  # Default for a white square (empty initially)

                # Check if it's a black square
                if (
                    "empty" in classes or "stop" in classes
                ):  # Include 'stop' class just in case
                    cell_value = "#"
                else:  # It's a white square ('letter' box)
                    # Check if it contains a clue number
                    cluenum_span = child.select_one(".cluenum-in-box")
                    if cluenum_span:
                        try:
                            # Extract the number, strip whitespace and zero-width joiner (‍)
                            num_str = cluenum_span.get_text(strip=True).replace(
                                "\u200d", ""
                            )
                            cell_value = int(num_str)
                        except ValueError:
                            print(
                                f"Warning: Could not parse clue number '{num_str}' into an integer. Placing 0."
                            )
                            # Cell value remains 0

                current_row.append(cell_value)

            elif "endRow" in classes:
                # This marks the end of a row
                if current_row:  # Only append if the row is not empty
                    grid.append(current_row)
                current_row = []  # Start a new row
            # Ignore other div types if they exist

    # After the loop, check if there's any leftover content in current_row
    # (Shouldn't happen if HTML is well-formed with endRow after each row,
    # but good practice)
    if current_row:
        print("Warning: Found leftover boxes after the last endRow.")
        grid.append(current_row)

    print(f"Parsed a grid with {len(grid)} rows.")
    if grid:
        print(f"Each row has {len(grid[0])} cells.")  # Assuming rectangular grid

    return grid


def get_title(soup: BeautifulSoup) -> str:
    # from this <meta content="Play this Crossword - Everyman 4097" property="og:title"/>

    title_div = soup.find("meta", property="og:title")
    title = title_div.get("content")

    # remove "Play this Crossword - "
    title = title.replace("Play this Crossword - ", "")

    if title == "obs.speedy":
        title = "Speedy"

    # replace space with underscore
    title = title.replace(" ", "_")

    return title


def get_observer_puzzle(
    soup: BeautifulSoup,
    url: str,
    filepath: str = None,
    download: bool = False,
    increment_counter: bool = False,
) -> dict:
    across_clues = parse_crossword_clues(soup, True)
    down_clues = parse_crossword_clues(soup, False)
    grid = parse_crossword_grid(soup)
    title = get_title(soup)

    dt = datetime.datetime.now()

    puzzle = dict()
    puzzle["origin"] = "The Observer"
    puzzle["version"] = "http://ipuz.org/v2"
    puzzle["kind"] = ["http://ipuz.org/crossword"]
    puzzle["copyright"] = f"{dt.year} Tortoise Media"
    puzzle["author"] = "Everyman Crossword"
    puzzle["publisher"] = "The Observer"
    puzzle["url"] = url
    puzzle["title"] = title
    puzzle["date"] = dt.strftime("%m/%d/%Y")
    puzzle["dimensions"] = dict(width=len(grid[0]), height=len(grid))
    puzzle["puzzle"] = grid
    puzzle["clues"] = {"Across": across_clues, "Down": down_clues}

    filename = f"Observer_{title}_{dt.strftime('%m%d%Y')}.ipuz"
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


def get_observer_puzzle_sync(url: str = "https://observer.co.uk/everyman") -> dict:
    xword_url = generate_xword_url(url)
    html = get_rendered_puzzle_html_sync(xword_url)
    soup = BeautifulSoup(html, "html.parser")
    return get_observer_puzzle(soup, url)


async def get_observer_puzzle_async(
    url: str = "https://observer.co.uk/everyman",
) -> dict:
    xword_url = generate_xword_url(url)
    html = await get_rendered_puzzle_html_async(xword_url)
    soup = BeautifulSoup(html, "html.parser")
    return get_observer_puzzle(soup, url)
