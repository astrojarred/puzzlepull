from flask import Flask, request, jsonify

from . import puzzlepull

app = Flask(__name__)


@app.route("/guardian")
def get_guardian_puzzle():
    """Scrape a puzzle from the Guardian website and
    convert to .ipuz (JSON) format."""

    url = request.args.get("puzzle_url")

    puzzle = puzzlepull.get_guardian_puzzle(url, download=False)

    return jsonify(puzzle)
