# Auditor brief — silent-locus chibi animation (frame-accurate sync edition)

## What you're auditing
Two finished MP4s (after encode):
- `animation/swarm-locus-v1-vertical.mp4` (1080x1920)
- `animation/swarm-locus-v1-landscape.mp4` (1920x1080)
Plus the source frames in `animation/work/chibi_v/` and `animation/work/chibi_l/` (f%05d.png, 24fps).

## Method
1. Read `animation/work/audit_cache.json`. Any scene already marked `"status": "pass"` is DONE — do not re-grade it. Grade only `pending` (or `fail` being re-checked after a fix).
2. Extract the representative frames listed below (ffmpeg or direct PNG reads).
3. Grade each scene in BOTH cuts. Write results back to `audit_cache.json`:
   `{"vertical": {"<scene>": {"status": "pass"|"fail", "notes": "...", "at": "<utc>"}}}, ...}` — update in place, never reset other entries.

## Grades (all must pass)
1. **Caption fit** — text fully inside the white card with padding; no overflow, no clipping.
2. **No occlusion** — no character or key element hidden behind the caption card.
3. **Style** — soft rounded pastel chibi throughout; zero hard pixel blocks.
4. **Legibility** — caption readable at phone size.
5. **No glitches** — no half-drawn elements, no transition artifacts frozen mid-frame.
6. **SYNC (frame-accurate)** — at the sync frames below, the counter must read its final
   value (or be within 2 of it): the visual lands exactly on the spoken word.
   Scene changes must coincide with narration phrase starts (no visual lagging a full
   second behind the words).

## Representative frames (24fps; stable mid-scene, clear of transitions)
- title f30 | breakout f150 | msgboard f350 | registry f505 | wiki f580
- escape f610 | health f636 | tunnels f662 | federal f688 | webwave f712
- cagebreaks f740 | heist f900 | after f1110 | reckoning f1210 | pattern f1290
- stillonline f1390 | sting f1500

## Sync frames (counter must show final value ±2)
- f387 → 1,200 agents ("twelve" @ 16.14s)
- f419 → 70,000 ("seventy" @ 17.47s)
- f547 → 2,000 ("two" @ 22.78s)
- f808 → 700 ("seven" @ 33.65s)
- f874 → 17,600 ("seventeen" @ 36.41s)

## On-screen numbers to verify against timeline.json
1,200 agents | 70,000 messages | 2,000 packages | 111 of 113 | 107 tunnels (tunnels scene)
| 215 packages | 700 agents | 17,600 actions | dates: 2026-05-07, 2026-05-12, 2026-07-10.

## IMPORTANT display quirk
The image-viewing tool may render these PNGs with a DARKENED sky. This is a viewer
artifact — verify by sampling actual pixels (sky should read ~(215,235,248) light
blue). Do NOT fail a scene for "dark sky" unless pixel samples confirm it.

## If anything fails
Report the exact scene/cut/frame and what's wrong. Do NOT fix it yourself — the
parent will regenerate and ask you to re-grade (your cache entries make this cheap).
