# puzzlepull

This code converts crossword puzzles from around the web into the [`.ipuz`](http://www.ipuz.org/) format.
This allows the puzzles to be uploaded and solved on sites like [squares.io](http://squares.io/).

You can use the service by visiting [the associated webpage](https://puzzlepull.space.jarred.green).

### How it works

The backend primarily uses [`xword-dl`](https://github.com/thisisparker/xword-dl) to download a puzzle from a pasted URL, then converts the result from `.puz` to `.ipuz`.

Native scrapers for **The Guardian** and **The Observer** remain as fallbacks when `xword-dl` cannot fetch those sites.

### Compatible Sites

Paste a puzzle URL from one of these publishers (and related AmuseLabs embed hosts):

- The Guardian
- The Observer (Everyman & Speedy)
- USA Today
- The Washington Post
- The New Yorker
- Los Angeles Times
- The Atlantic
- Vox
- The Daily Beast
- Newsday
- The Walrus
- Der Standard
- Simply Daily Puzzles
- Billboard
- The Daily Princetonian
- McKinsey
- AmuseLabs CDN embeds

Please open an issue if you would like to see a site added.

Subscription-only sources (for example the NYT crossword) are not supported.
