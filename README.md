[![bounty](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/Andia86/makefun-news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/Andia86/makefun-news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

# The Day in World News — Thursday 19 November 2026

**44 stories · 6 continents · one page**

A single-image front page summing up Thursday 19 November 2026:
11 illustrated story cards, a world map with all 44 stories pinned at
their real locations, a 33-item "In Brief" column, and a source footer.

## Entry contract

- `main.py` (Python 3, standard library only, no network) copies the
  bundled `entry.png` to the output path (`/output/entry.png`, or
  `$MAKEFUN_OUTPUT_DIR/entry.png` locally). It is deterministic: the
  same bytes on every run.
- `entry.png` is 1024×1024, ~330 KB (limit 1 MiB).

## How the page was made

- `build_page.py` renders the poster with Pillow: masthead with the
  date in words, numbered cards with hand-drawn icons (the hero card
  uses a generated Shenzhen skyline), a halftone world map
  (`art/map.png`) with numbered pins — offset pins use leader lines to
  an anchor dot on the exact location — briefs, a one-line summary
  strip and the source footer.
- Every story was reported on 19 November 2026 and cross-checked
  against the outlets in `NEWS_SOURCES.md`. Pin positions were
  verified one by one against the map artwork's coastlines.

## Files

- `main.py` — entry program (kit contract)
- `entry.png` — the rendered page
- `build_page.py` — the renderer (not needed by the grader)
- `art/map.png` — map artwork used by the renderer
- `NEWS_SOURCES.md` — every story, its pin and its source
- `LICENSE` — MIT (kit starter)

## License

MIT — see `LICENSE`.
