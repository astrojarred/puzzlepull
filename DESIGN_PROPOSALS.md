# PuzzlePull — three design proposals

Simple directions for a full visual overhaul. Same product job in all three: paste a puzzle URL → download `.ipuz`. Ditch the sidebar dashboard look.

---

## 1. Grid Ink

**Feel:** Quiet crossword atmosphere. Tool-first, not a control panel.

- **Palette:** Soft slate wash, deep ink navy, cobalt accent
- **Type:** Fraunces (brand) + DM Sans (UI)
- **Layout:** Slim top nav; brand + URL + Download
- **Visual:** Faint full-bleed crossword grid

---

## 2. Moss Utility

**Feel:** Calm workshop tool. Almost no chrome.

- **Palette:** Cool stone, charcoal, moss green accent
- **Type:** Space Grotesk
- **Layout:** Centered single column
- **Visual:** Soft grain, no grid motif

---

## 3. Signal Clear ← **shipping this one**

**Feel:** Sharp little converter. Friendly, high contrast, zero clutter.

- **Palette:** Warm white (`#FAFAF8`), near-black (`#121212`), vermillion CTA (`#E23D28`)
- **Type:** Syne (brand) + Source Sans 3 (UI), IBM Plex Mono for status / counts
- **Layout:** Huge brand, paste+download centered, empty-cell motif, responsive top nav (Menu on small screens)
- **Pages:** Download (with Redis download count), Compatible sites, Help & contact, GitHub links
- **Motion:** Empty-cell breathe; CTA fill while downloading; respect `prefers-reduced-motion`

**Why:** Strongest brand punch and the clearest “one job” silhouette.
