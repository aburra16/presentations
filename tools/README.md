# tools

Scripts that generate things from the deck. Run them from this folder.

## PowerPoint backup (`export-states.js` + `build.py`)

The .pptx is a stack of screenshots, one per click state, with a fade-in per click so
the click count matches the HTML by construction. Motion, typing and video playback
are lost; videos are embedded and autoplay on arrival.

```sh
cd tools
npm i playwright python-pptx 2>/dev/null   # Playwright + Chromium are preinstalled in the Claude container
node export-states.js                       # screenshots every click state into states/, writes states.json
node export-states.js chain-agent           # one slide only (by section id)
python3 build.py                            # -> bitfest-2026-backup.pptx
```

- `export-states.js` opens `../bitfest-2026/index.html` (or the path given as 2nd arg),
  calls `window.__deck.go(i)` / `__deck.next()`, waits for `__deck.busy` plus a settle
  time (flight 3600 ms, chain-agent 4200 ms, else 1400 ms), freezes videos on their
  last frame and screenshots at 1920×1080.
- `build.py` reads `states.json`, stacks the frames per slide, writes a custom
  `<p:timing>` (presetID 10 fade entrance per click), embeds `assets/video/*.mp4` with
  an autoplay node, and copies the `<aside>` notes into speaker notes.
- Validate with the pptx skill's `validate.py` if available; render with `soffice` for a
  static check.
- The output lives in Avi's `~/Downloads/site/`, not in the repo.

## Map (`mapgen/gen.mjs`)

Generates the Americas outline and the NYC → Mato Grosso great circle used on the flight
slide (slide 10). `cd mapgen && npm i && node gen.mjs` writes `map.json`; the path data
is pasted into `index.html` by hand. Only rerun if the projection or route changes
(the landing spot must stay outside Paraguay).
