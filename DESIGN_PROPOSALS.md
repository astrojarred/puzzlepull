# PuzzlePull — three design proposals

Simple directions for a full visual overhaul. Same product job in all three: paste a puzzle URL → download `.ipuz`. Ditch the sidebar dashboard look.

---

## 1. Grid Ink ← **shipping this one**

**Feel:** Quiet crossword atmosphere. Tool-first, not a control panel.

- **Palette:** Soft slate wash (`#E8EDF2` → `#F4F6F8`), deep ink navy (`#1B2A41`), single accent in cobalt (`#2F6FED`)
- **Type:** Fraunces (brand) + DM Sans (UI)
- **Layout:** Slim top nav (Home / Compatibility / GitHub). First viewport = brand + one line + URL field + Download. No cards, no sidebar.
- **Visual:** Faint full-bleed crossword grid as atmosphere (CSS, not a hero image collage)
- **Motion:** Grid fades in; input focus soft-expands; button has a short press/loading spin

**Why:** On-brand for puzzles, still dead simple, and clearly not the old shadcn sidebar shell.

---

## 2. Moss Utility

**Feel:** Calm workshop tool. Almost no chrome.

- **Palette:** Cool stone (`#F0F2F0`), charcoal (`#222822`), moss green accent (`#3D6B4F`)
- **Type:** Space Grotesk everywhere
- **Layout:** Centered single column. Brand wordmark, input, button. Compatibility is a plain text list below the fold.
- **Visual:** Soft diagonal grain / noise, no grid motif
- **Motion:** Underline grows under the focused input; success state slides a short “saved” line

**Why:** Maximum clarity, almost no decoration. Good if we want “utility app” over “branded product.”

---

## 3. Signal Clear

**Feel:** Sharp little converter. Friendly, high contrast, zero clutter.

- **Palette:** Warm white (`#FAFAF8`), near-black (`#121212`), vermillion CTA (`#E23D28`) — not cream+terracotta, not purple
- **Type:** Syne (brand) + Source Sans 3 (UI), tiny monospace for status / counts
- **Layout:** Brand huge at top-left of the first viewport; paste+download locked to the vertical center. Footer link row only.
- **Visual:** Large abstract “empty cell” square behind the form (one shape, not a collage)
- **Motion:** Empty-cell square gently breathes; CTA fills left→right while downloading

**Why:** Strongest brand punch and the clearest “one job” silhouette.

---

## Decision

**Grid Ink** is implemented in this PR: crossword-native without going broadsheet, and a clean break from the current dashboard UI.
