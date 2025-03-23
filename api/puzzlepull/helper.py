# make a blank puzzle
def make_blank_puzzle(width: int, height: int) -> list[list[str]]:
    puzzle = []
    for row in range(height):
        puzzle.append(["#"] * width)

    return puzzle
