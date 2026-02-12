# Hunger — Digital Companion Edition

## Goal

Build a professional, minimal, dark-mode GitHub Pages site for Knut Hamsun's *Hunger* (1890) with:
- The full novel split into 4 parts
- A comprehensive body of companion texts (no redundancy across any essays)
- Two downloadable PDFs (Lexend font, professional, Speechify-friendly): one for the novel, one for all companion texts
- localStorage bookmarks (two: novel position + companion position)
- Optimized for reading with Speechify Chrome extension

## Site URL

https://bedwards.github.io/hunger/

## Content Architecture

### The Novel
- `part-1.html` through `part-4.html` — extracted from `hunger.html` via `build.py`

### Companion Texts (treated as a single cohesive body — no redundancy)

**Thematic Essays** (~3,000 words each, focused analytical angle):
- `extra-1.html` — "The Invention of the Interior" (Part I: psychological modernism, stream of consciousness)
- `extra-2.html` — "Christiania: A City of Ghosts" (Part II: historical city, bohemians, urban space)
- `extra-3.html` — "The Theater of Starvation" (Part III: pride, performance, shame, literary descendants)
- `extra-4.html` — "After Hunger" (Part IV: ending, Hamsun's legacy/controversy, influence)

**Close-Reading Companions** (~matching chapter word count, walking alongside the text):
- `companion-1.html` — Close reading of Part I
- `companion-2.html` — Close reading of Part II
- `companion-3.html` — Close reading of Part III
- `companion-4.html` — Close reading of Part IV

**Whole-Book Essay**:
- `essay.html` — Overarching analysis of the complete novel

### PDFs
- `hunger-novel.pdf` — The complete novel
- `hunger-companion.pdf` — All companion texts ordered: whole-book essay → Part I (thematic essay, close reading) → Part II → Part III → Part IV

## Process

1. Base site built on `main` branch (`docs/` folder, GitHub Pages)
2. Each companion text gets a GitHub issue with detailed, non-overlapping requirements
3. Background workers create git worktrees on feature branches
4. Workers write the essay, commit, push, create PR referencing the issue
5. PRs are reviewed and merged to `main`
6. Deploy frequently, verify at the live URL

## Technical Details

- **Font**: Lexend (Google Fonts) — 300/400/500 weights
- **Colors**: `--bg: #0d0d0d`, `--text: #c8c8c8`, `--accent: #b08d57`
- **Build script**: `build.py` extracts chapters from `hunger.html`
- **Bookmarks**: Two localStorage keys — `hunger_novel_bookmark` and `hunger_extra_bookmark`
- **Navigation**: Every page has prev/next + home + cross-links between novel and companion content

## Non-Redundancy Rule

All essays are part of a single body. Each has a strict scope:
- Close-reading companions: sentence-level annotation, passage-by-passage insight
- Thematic essays: step back, make arguments, draw intertextual connections
- Whole-book essay: synthetic, overarching — what the entire work achieves
- If a topic is covered by one essay, others reference it briefly and defer
