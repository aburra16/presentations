# Find the humans — BitFest 2026 (Nostrshire keynote)

Self-contained talk. Open `index.html` in a browser, press F for full screen.

- Click the right half of the screen (or →, space) to advance; the left half (or ←) goes back.
- N shows the speaker notes under the slide. P opens a presenter window with a clock, notes and the next slide.
- S jumps to the end of the current slide's animation. M turns motion off. C switches the cast (Benjamin's Brainstorm figures, or the illustrated lineup); `?cast=ill` in the URL opens with the illustrated one.
- `#12` in the URL opens slide 12.

Slots to fill (drop files in, nothing else changes):

- `assets/photos/2023.jpg`, `2024.jpg`, `2025.jpg` — Červený Jelen, 16:9 or wider, 1920px+ wide.
- `assets/video/manchester-events.mp4`, `praha-places.mp4`, `wuthering-heights.mp4`, `nathan-day.mp4` — screen recordings, H.264, 1600×894, 30 fps, muted, played once per visit; a click in the middle third of the screen, or the R key, replays the clip.

Cast: `assets/cast/*.svg` (avi, jan, man, son, libor, robot). Each is a plain SVG; swap a file and the scenes pick it up. Sprites are placed with feet on a common baseline; `SPR` in `index.html` holds each file's size and the horizontal anchor.

Fonts are local (Figtree, IBM Plex Mono), so the talk works offline. Design: the Brainstorm design system.
