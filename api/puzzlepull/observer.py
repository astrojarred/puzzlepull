import asyncio
import datetime
import html
import json
import re
from html.parser import HTMLParser
from urllib.parse import quote, urlparse, parse_qs

import requests
from bs4 import BeautifulSoup

from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright

from .db import increment_counter as increment

PUZZLE_DATA_API = "https://content-api.slowdownwiseup.co.uk/api/mobile/v1"
PUZZLE_UUID_RE = re.compile(
    r'"type"\s*:\s*"puzzle"\s*,\s*"uuid"\s*:\s*"([0-9a-f-]{36})"',
    re.IGNORECASE,
)
PUZZLE_UUID_ESCAPED_RE = re.compile(
    r'\\"type\\"\s*:\s*\\"puzzle\\"\s*,\s*\\"uuid\\"\s*:\s*\\"([0-9a-f-]{36})\\"',
    re.IGNORECASE,
)


class _ClueTextExtractor(HTMLParser):
    """Strip tags from clue HTML while preserving spaces between text nodes."""

    def __init__(self):
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        if data:
            self.parts.append(data)

    def get_text(self) -> str:
        return "".join(self.parts).strip()


def _clean_clue_text(raw: str) -> str:
    unescaped = html.unescape(raw or "")
    parser = _ClueTextExtractor()
    parser.feed(unescaped)
    parser.close()
    text = parser.get_text()
    return re.sub(r"\s+", " ", text).strip()


def extract_puzzle_uuid(page_html: str) -> str | None:
    """Extract Marmalade puzzle UUID from Observer article HTML / RSC payload."""
    match = PUZZLE_UUID_RE.search(page_html)
    if match:
        return match.group(1)

    match = PUZZLE_UUID_ESCAPED_RE.search(page_html)
    if match:
        return match.group(1)

    # Next.js flight payloads often need unescaping before the UUID is visible.
    payloads = re.findall(
        r'self\.__next_f\.push\(\[1,"(.*?)"\]\)</script>', page_html, re.DOTALL
    )
    if payloads:
        try:
            unescaped = "".join(payloads).encode("utf-8").decode("unicode_escape")
        except UnicodeDecodeError:
            unescaped = "".join(payloads)
        match = PUZZLE_UUID_RE.search(unescaped)
        if match:
            return match.group(1)

    return None


def fetch_puzzle_data_json(uuid: str) -> dict:
    """Fetch structured crossword JSON for a Marmalade puzzle UUID."""
    meta_url = f"{PUZZLE_DATA_API}/puzzle-data/{uuid}/"
    meta_resp = requests.get(meta_url, timeout=30)
    meta_resp.raise_for_status()
    meta = meta_resp.json()

    files = meta.get("files") or {}
    data_path = files.get("data.json")
    if not data_path:
        raise ValueError(f"Puzzle data.json missing for uuid={uuid}")

    data_url = f"{PUZZLE_DATA_API}{data_path}"
    data_resp = requests.get(data_url, timeout=30)
    data_resp.raise_for_status()
    return data_resp.json()


def grid_from_puzzle_data(data: dict) -> list[list]:
    """Convert Marmalade grid cells to ipuz layout (# / number / 0)."""
    grid = []
    for row in data.get("grid") or []:
        out_row = []
        for cell in row:
            if cell.get("Blank") == "blank":
                out_row.append("#")
                continue
            number = (cell.get("Number") or "").strip()
            if number:
                try:
                    out_row.append(int(number))
                except ValueError:
                    out_row.append(0)
            else:
                out_row.append(0)
        grid.append(out_row)
    return grid


def clues_from_puzzle_data(data: dict) -> dict:
    """Convert Marmalade clue sections to ipuz Across/Down lists."""
    across: list[list] = []
    down: list[list] = []

    for section in data.get("copy", {}).get("clues") or []:
        title = (section.get("title") or "").strip().lower()
        target = across if title == "across" else down if title == "down" else None
        if target is None:
            continue

        for clue in section.get("clues") or []:
            number = clue.get("number")
            text = _clean_clue_text(clue.get("clue") or "")
            fmt = (clue.get("format") or "").strip()
            if number is None or not text:
                continue
            combined = f"{text} ({fmt})" if fmt else text
            target.append([int(number), combined])

    return {"Across": across, "Down": down}


def title_from_puzzle_data(data: dict) -> str:
    copy = data.get("copy") or {}
    meta = data.get("meta") or {}

    title = (copy.get("title") or data.get("headline") or "").strip()
    if not title:
        variant = meta.get("variant") or copy.get("crosswordtype") or "Observer"
        number = meta.get("number") or copy.get("id") or ""
        title = f"{variant} {number}".strip()

    if title.lower() in {"obs.speedy", "obs.speedy crossword"}:
        title = "Speedy"
    elif title.lower().startswith("observer "):
        title = title[9:].strip()

    return title.replace(" ", "_")


def author_from_puzzle_data(data: dict) -> str:
    copy = data.get("copy") or {}
    meta = data.get("meta") or {}
    variant = (
        meta.get("variant")
        or copy.get("crosswordtype")
        or "Everyman"
    ).strip()
    if variant.lower() == "speedy":
        return "Speedy Crossword"
    return f"{variant} Crossword"


def build_observer_ipuz(
    url: str,
    grid: list[list],
    clues: dict,
    title: str,
    author: str = "Everyman Crossword",
    filepath: str = None,
    download: bool = False,
    increment_counter: bool = False,
) -> dict:
    if not grid or not grid[0]:
        raise ValueError(f"Empty crossword grid for URL: {url}")

    dt = datetime.datetime.now()

    puzzle = dict()
    puzzle["origin"] = "The Observer"
    puzzle["version"] = "http://ipuz.org/v2"
    puzzle["kind"] = ["http://ipuz.org/crossword"]
    puzzle["copyright"] = f"{dt.year} Tortoise Media"
    puzzle["author"] = author
    puzzle["publisher"] = "The Observer"
    puzzle["url"] = url
    puzzle["title"] = title.replace("_", " ")
    puzzle["date"] = dt.strftime("%m/%d/%Y")
    puzzle["dimensions"] = dict(width=len(grid[0]), height=len(grid))
    puzzle["puzzle"] = grid
    puzzle["clues"] = clues

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


def get_observer_puzzle_from_data_json(
    url: str,
    page_html: str = None,
    filepath: str = None,
    download: bool = False,
    increment_counter: bool = False,
) -> dict:
    """Primary path: Marmalade UUID embedded in Observer article → data.json → ipuz."""
    if page_html is None:
        page = requests.get(url, timeout=30)
        page.raise_for_status()
        page_html = page.text

    uuid = extract_puzzle_uuid(page_html)
    if not uuid:
        raise ValueError(f"Could not find Marmalade puzzle UUID in page. URL: {url}")

    data = fetch_puzzle_data_json(uuid)
    grid = grid_from_puzzle_data(data)
    clues = clues_from_puzzle_data(data)
    title = title_from_puzzle_data(data)
    author = author_from_puzzle_data(data)

    return build_observer_ipuz(
        url=url,
        grid=grid,
        clues=clues,
        title=title,
        author=author,
        filepath=filepath,
        download=download,
        increment_counter=increment_counter,
    )


def generate_xword_url(
    url: str,
    uid: str = "dd9a2d93-741d-493c-975c-cbe37256c8cc",
    page_html: str = None,
) -> str:
    if page_html is None:
        page = requests.get(url, timeout=30)
        page.raise_for_status()
        page_content = page.content
    else:
        page_content = page_html.encode("utf-8") if isinstance(page_html, str) else page_html

    soup = BeautifulSoup(page_content, "html.parser")

    data_id = None
    data_set = None

    # First, try to find iframe with amuselabs URL (legacy structure)
    iframe = soup.find("iframe", src=lambda x: x and "amuselabs.com" in x)

    if iframe:
        iframe_src = iframe.get("src")
        if iframe_src:
            # Parse the iframe src URL to extract id and set parameters
            parsed_url = urlparse(iframe_src)
            query_params = parse_qs(parsed_url.query)

            # Extract id and set from query parameters
            if "id" in query_params:
                data_id = query_params["id"][0]
            if "set" in query_params:
                data_set = query_params["set"][0]

    # Fallback: try to find div with class pm-embed-div (old structure or dynamically loaded)
    if not data_id or not data_set:
        div = soup.find("div", class_="pm-embed-div")
        if div:
            data_id = div.get("data-id")
            data_set = div.get("data-set")

    # Error handling if neither method found the required data
    if not data_id or not data_set:
        raise ValueError(
            f"Could not find puzzle data (id and set) in the page. "
            f"Tried both iframe src and pm-embed-div. URL: {url}"
        )

    # Construct URL using new format (pmm instead of puzzleme)
    xword_url = f"https://cdn2.amuselabs.com/pmm/crossword?id={data_id}&set={data_set}&embed=js&uid={uid}&src={quote(url, safe='')}"
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
            clue_text_element.get_text(" ", strip=True) if clue_text_element else None
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

    return build_observer_ipuz(
        url=url,
        grid=grid,
        clues={"Across": across_clues, "Down": down_clues},
        title=title,
        filepath=filepath,
        download=download,
        increment_counter=increment_counter,
    )


def get_observer_puzzle_from_amuselabs(
    url: str,
    page_html: str = None,
) -> dict:
    """Legacy AmuseLabs iframe / pm-embed path (Playwright render)."""
    xword_url = generate_xword_url(url, page_html=page_html)
    html = get_rendered_puzzle_html_sync(xword_url)
    soup = BeautifulSoup(html, "html.parser")
    return get_observer_puzzle(soup, url)


def get_observer_puzzle_sync(url: str = "https://observer.co.uk/everyman") -> dict:
    page = requests.get(url, timeout=30)
    page.raise_for_status()
    page_html = page.text

    try:
        return get_observer_puzzle_from_data_json(url, page_html=page_html)
    except Exception as marmalade_error:
        print(f"Marmalade puzzle path failed ({marmalade_error}); trying AmuseLabs fallback")
        try:
            return get_observer_puzzle_from_amuselabs(url, page_html=page_html)
        except Exception as amuselabs_error:
            raise ValueError(
                f"Could not download Observer puzzle from {url}. "
                f"Marmalade error: {marmalade_error}. "
                f"AmuseLabs error: {amuselabs_error}"
            ) from amuselabs_error


async def get_observer_puzzle_async(
    url: str = "https://observer.co.uk/everyman",
) -> dict:
    page = await asyncio.to_thread(requests.get, url, timeout=30)
    page.raise_for_status()
    page_html = page.text

    try:
        return await asyncio.to_thread(
            get_observer_puzzle_from_data_json, url, page_html=page_html
        )
    except Exception as marmalade_error:
        print(f"Marmalade puzzle path failed ({marmalade_error}); trying AmuseLabs fallback")
        try:
            xword_url = generate_xword_url(url, page_html=page_html)
            html = await get_rendered_puzzle_html_async(xword_url)
            soup = BeautifulSoup(html, "html.parser")
            return get_observer_puzzle(soup, url)
        except Exception as amuselabs_error:
            raise ValueError(
                f"Could not download Observer puzzle from {url}. "
                f"Marmalade error: {marmalade_error}. "
                f"AmuseLabs error: {amuselabs_error}"
            ) from amuselabs_error
