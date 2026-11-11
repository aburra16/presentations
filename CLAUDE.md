# Presentations — working notes for Claude

Avi's talks as self-contained web pages, served by GitHub Pages from `main`
(https://aburra16.github.io/presentations/). One folder per talk.

## bitfest-2026 — "Find the humans"

Nostrshire keynote, BitFest Manchester, Fri 20 Nov 2026, 10:25–10:45, Pendulum main
stage. Programme title "Agentic Reputations". Audience: non-technical attendees and
spouses. The story and script live in two Claude Docs, which are the source of truth
for words: "BitFest keynote: script and flow" (https://claude.ai/artifact/LvjrKhc7XQJkcEQe8mYeCT)
and "BitFest keynote: reading script" (https://claude.ai/artifact/Jf65nEMSKsgaaYpbBoUiQV).
Avi rewords everything himself; Claude removes AI tells (no em dashes, no "it's not X,
it's Y", no "Not X. Not Y. Just Z." — except deliberately on the slop card of slide 14).

### Three copies that must stay in step

1. This repo (`bitfest-2026/`), pushed to `main`; GitHub Pages serves it.
2. Avi's local copy at `~/Downloads/site/bitfest-2026/` on his Mac (written through the
   device bridge; `~/Downloads/site/_originals/` holds the .mov recordings and photo
   originals, which stay out of the repo).
3. The claude.ai artifact https://claude.ai/artifact/Usj3ZK7s42C1CTqV5QZtRf (same files).

After any change: publish the artifact, write the Mac copy, commit and push. Keep the
`.nojekyll` file.

### How the page works

- One file, `index.html`: 28 `<section class="slide">`, a Web-Animations runtime
  (seq/par/stag/fade/settle/rise/drop/pop/chip/type/fly/tween), and a `build(id, section)`
  switch that returns `{steps:[...], pre?, final?}` per slide. Step 1 plays on arrival;
  each later step is a click. `final()` is what a slide must look like when you step
  *back* onto it (needed where something fades out mid-sequence: slides 14 and 26).
- Navigation: right third of the screen / →, Space, PageDown, Enter = next; left third /
  ← , PageUp = back; middle third or R = replay the footage on that slide; S = finish the
  current animation; N = notes overlay (on the main screen — never on stage); P = presenter
  window (clock, notes, next slide; takes the same keys); F = fullscreen; C = switch cast;
  M = motion off. `window.__deck` exposes go/next/prev/cur/step/busy/steps for tooling.
- Two casts. Default `bs` is Benjamin's Brainstorm cast (one faceless figure, colour =
  relation: cyan you, purple close friend, light violet friend of a friend; name chips),
  drawn inline by `pin()`/`bot()` with optional props (outback hat on Me only, suit +
  sunglasses = agent, doctor's cap, hard hat). `?cast=ill` or C switches to the
  illustrated lineup in `assets/cast/*.svg` (recraft, recoloured to the palette).
- Footage slides (19–22) play their mp4 once on arrival, hold the last frame; the frame is
  1252×700 to match the recordings' 1600×894. Slide 23 is a drawn phone ("coming soon",
  "Drawn, not live").
- Design: Brainstorm design system — Aurora Purple #7237FF, Aurora Cyan #13D2E5, Ink
  #0A0E18, Balanced White #F2F3F0, Deep Violet #2B174F; Figtree + IBM Plex Mono, local
  fonts; 24px frames; no 3D, no textures. Light↔dark slide changes get a short dip.
- Class names are global: a new component must not reuse `.phone`, `.card`, `.panel`,
  `.labels`, `.scene` without scoping (slide 14's scam panel is `.panel.phone`).

### Click counts (28 slides, 64 states)

1 cover 1 · 2 intro 1 · 3 wink 3 · 4 restaurant 1 · 5–7 photos 1 each · 8 libor 2 ·
9 my-son 1 · 10 flight 2 · 11 discover 3 · 12 chain 5 · 13 asked 2 · 14 sss 8 ·
15 still-there 2 · 16 ask-someone 8 · 17 brainstorm 2 · 18 find-the-humans 1 ·
19–22 footage 1 each · 23 card 3 · 24 three-things 3 · 25 tagging 2 · 26 chain-agent 2 ·
27 photos-close 2 · 28 close 3. (Counts include the on-arrival step.)

### PowerPoint backup

`bitfest-2026-backup.pptx` is generated from the HTML by `tools/` (see tools/README.md)
and lives in Avi's `~/Downloads/site/`, not in the repo. Regenerate after the HTML settles.

### Open items (as of 2026-11-06)

- Renumber the reading script's slide cues (deck grew from 27 to 28; several slides changed).
- .pptx regenerated 2026-11-11 from commit 8af23f2 (64 states); regenerate again after any further deck change.
- Offered, not yet asked for: a one-page cue card (headline + click count per slide).
- From the flow doc: add Červený Jelen to the Food and Drink list; confirm Jan is happy to
  be named; check a spouse with no key can sign up quickly; Shipshow adaptation after BitFest.
- On the day: Avi presents from his own Mac, extended display, presenter window on the
  lectern; Nathan's stage has no confidence monitor.
