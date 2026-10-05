# GEM GRAVEYARD — v3 STORYBOARD (vertical 1080×1920)

Halloween thriller · chibi ghosts · night sky, pumpkin orange, violet.
Dry infosec narration over cute ghosts — the contrast IS the bit.
All counts audit-corrected 2026-09-29. Every "researchers report" /
"our read" hedge is load-bearing. Jokes never smuggle facts.

## Beat 1 — the rehearsal (early May)
Visual: sparse gems drifting in, "a handful a day"; then the May-11
crescent counter: 39 gems, May 11th 04:42–14:31 UTC.
Cards: "Early May: probing uploads. A handful a day."
/ "May 11th: thirty-nine gems. A rehearsal. Nobody noticed."
Narration: "In early May, probing uploads — a handful a day. Then May 11th:
thirty-nine gems. A rehearsal. Nobody noticed."

## Beat 2 — the blitz (May 12)
Visual: storm red, gem grid, big counter 521; pill "273 in one hour ·
02:00 UTC".
Cards: "The next day: 521 more in under fourteen hours — 273 in a single
hour. The registry was flooding."
Narration: "The next day: 521 more in under fourteen hours — 273 in a
single hour. The registry was flooding."

## Beat 3 — the decoy (go-import canaries)
Visual: tag in a Halloween disguise; file panel "lib/hack.rb → 0 bytes";
note "empty shells. canaries."
Cards: "Inside each gem: a go-import tag cosplaying as a supply-chain
attack." / "Aimed at council calendars through a reader proxy, cycling
git, hg, fossil, bzr, svn — via the registry's own API. It could never
fire." / "Our read: canaries. Proof raw HTML could be planted in the
registry's metadata at scale." / "The code did nothing: empty shells.
Signed: southwarkssrfhack."
Narration: go-import tag cosplaying as a supply-chain attack; address was
the registry's own API; no real go get could fire it; our read = canaries;
code did nothing: empty shells; signed southwarkssrfhack.

## Beat 4 — the real payload (builders + keys)
Visual: 51 glowing builder gems; redacted key panel ("full-format keys —
values redacted"); counters "70 versions carried full push credentials"
/ "27 distinct keys — one held four".
Cards: "Fifty-one gems carried builders. Certificate checks off. Steal a
council calendar page…" / "…forge a brand-new gem, push it straight back
into RubyGems — on API keys hardcoded inside the gems. Seventy versions.
Twenty-seven distinct keys." / "It wasn't probing the registry. It was
living in it."  ← anchor line, do not touch.
Narration: builders stole calendar pages (cert checks off), forged new
gems, pushed them back on hardcoded API keys; 70 versions, 27 keys; anchor.

## Beat 5 — the docs server (externally reported)
Visual: library scene, violet RCE stamp (framed as reported), split panel:
"researchers report: crafted config → build workers ran it" vs "our bytes:
.yardopts = 1-byte empty files, 'YARD RAN' in build logs". Dry footer:
"the remote-code part is their finding, not ours".
Cards: "Researchers report a second loop: every gem gets free documentation,
built by RubyDoc.info — and a crafted config file turned those build
workers into scrapers." / "Same council sites. The haul published back as
new gems. Our bytes show the config files and the build timestamps." /
"The remote-code part is their finding, not ours."
Narration: second loop per researchers; build workers turned scrapers; our
bytes = configs + timestamps; remote-code part is their finding, not ours.

## Beat 6 — the tells
Visual: innocent gem → weaponized flip; 403 log page ("southfetchprobe42",
"builder alive"); timestamp "02:17:55 UTC"; key-rotation glyphs.
Cards: "One gem flipped innocent to weaponized between versions." / "A
captured log shows their own rig blocked by a network filter. An internal
timestamp — 02:17:55 UTC — confirms the burst from the inside." / "And the
keys rotated: two gems fetched fresh ones on the fly. Revoking the leaked
ones wouldn't have stopped it."
Narration: as cards; two gems fetched fresh keys on the fly.

## Beat 7 — the takedown
Visual: gems yanked one by one; "REGISTRATIONS PAUSED" (RubyGems' word);
"actor unconfirmed".
Cards: "RubyGems yanked the gems, paused registrations, disclosed a cache
bug — and says it can't confirm who was behind it. In June, a smaller wave
tried plain link-posting at a US federal dataset. Simpler trick."
Narration: yanked, paused registrations, cache bug disclosed, can't confirm
who; June: plain link-posting at a US federal dataset.

## Beat 8 — the twist (July)
Visual: full-campaign panel "JFrog · full campaign inventory — 3,025
packages · 3,323 releases / July 7th wave: 215"; dead-drop envelope A000;
footer "dead drops A000→ZZEND · ours: May wave".
Cards: "Then July: JFrog's full inventory — 3,025 packages, 3,323 releases
across the whole campaign. July 7th wave: 215." / "Webhook dead drops,
sequenced chunks marked A000 to ZZEND. The marked drops we can verify came
from the May wave."
Narration: JFrog full inventory 3,025 / 3,323, July 7th wave of 215;
webhook dead drops A000→ZZEND; verified marks are May-wave artifacts.

## Sting
"The registry was haunted. We just don't know for how long." — keep verbatim.

## Production notes (v3)
- Narration source: build/narration_script_v3.txt (9 paragraphs, exact).
- TTS: foreground preferred (background calls flaked with HTTP 500);
  synth_narration_v3.py hardened against sub-1KB stubs. Delete stale
  work/v3_phrase_*.{mp3,wav} before re-synth (phrase filenames reused).
- Audio: build_audio_gg_v3.py → work/final_audio_gg_v3.m4a; measured timings.
- Render: resume_render_v3.sh (lock-guarded, resumable) → work/frames_v3/.
- Encode: encode_v3.sh → gem-graveyard-v3-vertical.mp4 (24fps, yuv420p, AAC).
- Verify: verify_v3.py (24fps, dims, audio, duration, size, credential scan).
- Never publish hardcoded credential bytes — all illustrated keys redacted.
- V1/V2 outputs untouched; sting override is v3-only (G.sting_frame kept).
- Raw frames deleted before commit; all staged paths under animation/.
