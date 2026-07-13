# Free puzzle providers for puzzlepull (ipuz scraping research)

Research date: 2026-07-13

## Context

puzzlepull does **not** download pre-existing `.ipuz` files. It scrapes HTML/embeds and **builds** [ipuz v2](http://www.ipuz.org/) JSON. Today that means:

| Source | Host | Method |
|--------|------|--------|
| The Guardian | `www.theguardian.com` | Static HTML → `gu-island[CrosswordComponent]` props JSON |
| The Observer | `observer.co.uk` | AmuseLabs iframe → Playwright DOM scrape (Everyman & Speedy only) |

Goal: identify **other free** crossword providers (cryptic or American-style) that could be scraped into ipuz the same way.

Primary references used:

- [xword-dl](https://github.com/thisisparker/xword-dl) (scrapes to `.puz`)
- [Crossword Scraper](https://github.com/jpd236/CrosswordScraper) (browser extension → `.puz`/`.jpz`/`.ipuz`)
- Live probes of publisher pages / CDNs (July 2026)

---

## Recommendation summary

Best next sources for puzzlepull, ranked by fit:

1. **Generalize AmuseLabs** (reuse Observer path) → unlocks LAT, Atlantic, Vox, Daily Beast, Newsday, Walrus, Der Standard, Princetonian, many embeds
2. **USA Today** → full puzzle JSON already in page/`__NEXT_DATA__` (Guardian-like)
3. **Crosshare** → free community puzzles + official `.puz` API
4. **Simply Daily Puzzles** (incl. **easy cryptic**) → Crossword Compiler XML in predictable `.js` URLs
5. **Washington Post Sunday** → public JSON API
6. **New Yorker** → free; currently Puzzmo/Condé Nast games API

Harder / lower priority free cryptics: Independent (Arkadium), FT (PDF-only), Hindu, Lovatts, MyCrossword/Exolve.

Avoid for free URL-paste UX: NYT, Telegraph, Times UK, WSJ (gated / anti-bot).

---

## Tier 1 — Strong free candidates

### 1. AmuseLabs / PuzzleMe publishers (platform reuse)

Observer already depends on AmuseLabs. Many free outlets use the same CDN embeds (`cdn3.amuselabs.com`, `cdn-eu1.amuselabs.com`, `cdn2.amuselabs.com`).

**Confirmed free / commonly free AmuseLabs outlets:**

| Outlet | Notes |
|--------|--------|
| Los Angeles Times (+ Mini) | Free; page embeds AmuseLabs date-picker (`set=latimes`) |
| The Atlantic | Free daily; CDN ids like `atlantic_YYYYMMDD` |
| Vox | Free daily Mon–Sat |
| The Daily Beast | Free (historically AmuseLabs `set=tdb`) |
| Newsday | Free daily |
| The Walrus | Free weekly (Canada) |
| Der Standard | Free Kreuzworträtsel (EU CDN) |
| Daily Princetonian (+ Mini) | Free student paper |
| Billboard | Free (xword-dl support) |
| Indie blogs / local papers | Any page with PuzzleMe iframe/`pm-embed-div` |

**Scrape approach options:**

| Approach | Pros | Cons |
|----------|------|------|
| **Playwright DOM** (current Observer) | Already in codebase; resilient to `rawc` obfuscation | Heavy; Chromium dependency |
| **Deobfuscate `rawc`** (xword-dl style) | No browser; structured JSON (`box`, `placedWords`, etc.) | AmuseLabs now obfuscates `rawc` (not plain base64); needs maintained deobfuscator |
| **Generic AmuseLabs URL handler** | One module covers many hostnames | Need per-site discovery of `id`/`set` (iframe, date-picker, or `pm-embed-div`) |

**Live check (2026-07-13):** Atlantic solver pages still embed `rawc` in `#params` JSON, but values are **obfuscated** (old `base64 → JSON` path fails). Playwright scraping of the rendered grid/clues still matches puzzlepull’s Observer strategy.

**Implementation note:** Prefer a shared `amuselabs.py` used by Observer + new hostnames, rather than one module per newspaper.

---

### 2. USA Today — free, rich embedded JSON

- Site: https://puzzles.usatoday.com/ (also `play.usatoday.com/crossword`)
- Access: free without login (probed July 2026)
- Data: Next.js `__NEXT_DATA__` → GraphQL `findGameData` / `CrosswordData` with:
  - `title`, `author`, `editor`, `date`, `width`, `height`
  - `layout[]`, `solution[]`, `acrossClue`, `downClue`
- Fit: very similar to Guardian’s “JSON already in the page” pipeline
- Convert layout/clues → ipuz is straightforward

Universal (AMUniversal `data.json` feeds) is related but a separate syndicate path; treat as optional follow-on.

---

### 3. Crosshare — free community + official download API

- Site: https://crosshare.org/ (open source, AGPL)
- Access: free, ad-free
- Content: community American-style puzzles + daily mini / featured
- API: `GET https://crosshare.org/api/puz/{puzzleId}` returns a real `.puz` (`application/x-crossword`) — verified
- Fit for puzzlepull:
  - Accept Crosshare URLs, fetch `.puz`, convert to ipuz; **or**
  - Parse puzzle JSON from the page (Crossword Scraper does both)
- Cryptic: some community cryptics exist, but the platform is mostly American-style

---

### 4. Simply Daily Puzzles — free cryptic + quick + American

- Site: https://simplydailypuzzles.com/
- Free puzzles:
  - Easy Cryptic — `/daily-cryptic-crossword/`
  - Quick — `/daily-quick-crossword/`
  - American — `/daily-crossword/`
- Engine: Crossword Compiler applet
- Data URL pattern (verified):

```text
https://simplydailypuzzles.com/{subdir}/puzzles/YYYY-MM/{prefix}-YYYY-MM-DD.js
```

Examples:

- Cryptic: `.../daily-cryptic-crossword/puzzles/2026-07/dc1-2026-07-13.js`
- American: `.../daily-crossword/puzzles/2026-07/dc1-2026-07-13.js`
- Quick prefix: `dq1` (per xword-dl)

Each `.js` file sets `CrosswordPuzzleData` to Crossword Compiler XML (`crossword-compiler-applet`). Parse XML → ipuz.

This is one of the easiest **free cryptic** additions that is not Guardian/Observer.

---

### 5. Washington Post — free Sunday crossword API

- Marketing: “crossword puzzles free” on WaPo games pages
- Cadence: **Sunday only** (Evan Birnholz), not daily
- API (used by xword-dl):

```text
https://games-service-prod.site.aws.wapo.pub/crossword/levels/sunday/YYYY/MM/DD
```

Returns JSON with title/creator/cells/clues → map to ipuz.

Also has daily Mini Meta (different product; lower priority unless requested).

---

### 6. The New Yorker — free; Puzzmo backend

- Site: https://www.newyorker.com/puzzles-and-games-dept/crossword
- Access: free on web
- Backend: moved from AmuseLabs to **Puzzmo** / Condé Nast games API (`puzzles-games-api.gp-prod.conde.digital`)
- Fit: doable, but more moving parts than USA Today / Simply Daily
- Crossword Scraper + xword-dl already support it

---

## Tier 2 — Free cryptics / other languages (harder or limited)

| Provider | Free? | Format / engine | Scrape notes |
|----------|-------|-----------------|--------------|
| **The Independent** Cryptic (+ Concise) | Yes (web) | **Arkadium** Arena | Free and high-quality cryptic, but proprietary player; **not** supported by Crossword Scraper; hard scrape |
| **Financial Times** Cryptic | Yes (PDF) | PDF download | No interactive grid for free users; PDF→ipuz is OCR/layout parsing, not HTML scrape |
| **The Hindu** Cryptic | Yes | Own player + PDF | Possible; less prior art than AmuseLabs/USA Today |
| **Lovatts** daily cryptic | Yes | Own web player | AU cryptic; custom scrape |
| **MyCrossword / Exolve** | Yes | Exolve (often ipuz-friendly) | Community cryptics; good long-term, varied page shapes |
| **Le Monde** mots croisés | Yes (some free IDs) | GraphQL `jeux-api.lemonde.fr` | See [lemonde-crosswords-fetcher](https://github.com/DodoLeDev/lemonde-crosswords-fetcher) (already outputs ipuz) |
| **Minute Cryptic** | Free daily + paid extras | Custom | Short teaching cryptics; different product shape |

---

## Tier 3 — Poor fit for free puzzlepull UX

| Provider | Why skip (for now) |
|----------|--------------------|
| **New York Times** | Paywalled; needs auth tokens |
| **Telegraph / Times (UK)** | Subscription puzzles |
| **Wall Street Journal** | Bot protections / gating; xword-dl WSJ downloader disabled |
| **Globe and Mail cryptic** | No longer a clean first-party source (xword-dl removed it after syndication change) |
| **Puzzle Society “The Modern”** | Behind paywall |

---

## Platform cheat sheet (how scrapers usually work)

| Platform | Example outlets | Typical extraction |
|----------|-----------------|--------------------|
| Guardian island JSON | Guardian | HTML props → entries/grid |
| AmuseLabs PuzzleMe | Observer, LAT, Atlantic, Vox, … | iframe/`rawc` (obfuscated) or Playwright DOM |
| USA Today Play | USA Today | `__NEXT_DATA__` CrosswordData |
| AMUniversal JSON | Universal (historical USA Today feed) | `/d/YYYY-MM-DD/data.json` |
| Crossword Compiler JS/XML | Simply Daily, many indies | `.js` with XML applet blob |
| Crosshare | crosshare.org | `/api/puz/{id}` or page JSON |
| Puzzmo | New Yorker | Condé/Puzzmo games API |
| WaPo games service | WaPo Sunday | AWS games JSON API |
| Arkadium | Independent | Opaque; avoid unless high demand |
| Exolve | MyCrossword, blogs | Often near-ipuz already |

---

## Suggested implementation order for puzzlepull

1. **Extract shared AmuseLabs helper** from `observer.py`
   - Accept publisher page URL *or* direct CDN crossword URL
   - Keep Playwright path initially; optionally add `rawc` deobfuscation later
   - Wire hostnames: LAT, Atlantic, Vox, Daily Beast, Newsday, Walrus, …

2. **USA Today module** — page JSON → ipuz (no Playwright)

3. **Simply Daily Cryptic (+ Quick/American)** — fetch Compiler `.js` → parse XML → ipuz

4. **Crosshare** — URL → `.puz` → ipuz (adds `.puz` conversion utility)

5. **WaPo Sunday** and/or **New Yorker** if demand remains

Frontend wiring for each: `validHostnames.json`, `ENDPOINT_MAP` in `getPuzzle/+server.ts`, compatibility page, README.

---

## Legal / product notes

- “Free to play on the publisher site” ≠ permission to redistribute puzzles at scale.
- puzzlepull’s current model is **user-initiated URL conversion** for personal solving (e.g. squares.io), not an archive mirror.
- Prefer first-party pages the user pastes; respect robots/ToS and rate limits.
- AmuseLabs/`rawc` obfuscation and Arkadium anti-scraping change often; Playwright DOM or maintained deobfuscators will need upkeep.

---

## Appendix — already covered Guardian cryptics

Guardian support is type-agnostic via `crosswordType` in embedded data. Free Guardian series typically include Cryptic, Quiptic, Quick, Prize, Weekend, Speedy, Everyman (Everyman/Speedy also on Observer). No separate cryptic provider work is needed for Guardian itself.
