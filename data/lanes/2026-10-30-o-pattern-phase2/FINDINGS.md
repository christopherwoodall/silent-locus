# Findings — o-pattern relay-jina-reader, phase 2

Lane: `2026-10-30-o-pattern-phase2` (lane id `lane_2483c3b5db0d471db67f6654d61f18c2`).
Full report: `FULL-REPORT.md` in this lane directory (copy of the workspace
report). Prior report: workspace `o-pattern-followup/REPORT.md` (phase 1).

## Verdict (OBSERVED, as a negative finding)

NOT a swarm lead. The family reads as generative art with a mirrored
glyph vocabulary. No agent term, no fleet term, no tasking text, and no
beacon pattern was found in any asset examined. This is a negative
finding only. It does not prove the family has no hidden content. The
untested surfaces are in section "Gaps" below.

## Graded claims

All claims below are OBSERVED unless marked INFERENCE. Each claim cites
a capture observation. Full claim records are in Factum (see PROVENANCE.md).

- TXT content (claim on observation_45fee6f3d5e946a98695d068067788ca):
  the TXT is a UTF-16LE glyph file, 403 lines, a line-level palindrome
  (403/403). It carries 8 English-like definition-style sentences, each
  twice, in mirrored blocks lines 16-41 and 363-388. It has no
  imperatives, no recipients, no retrieval signals, and no links. It is
  not a plaintext manifest, instruction sheet, or tasking text. The glyph
  bulk is undecoded.
- Desmos tone match (claim on observation_9ad883229886433d8fbcead45fd06b0c):
  the ww MP3 7 tones equal the Desmos lem1oik7lp tones n=7-13
  (3^n/O, O=84.40602258995403) within 0.1 Hz (max diff 0.025 Hz). The
  Desmos tone second argument is gain (1/27), not duration. The state
  gives no duration. Chord-vs-arpeggio rendering is unsettled.
- MP3 carrier assessment (claim on observation_8507abf71bc740bfb7335687fb4eb43a):
  the mUr MP3 shares no Desmos tone (closest pairs differ by ~327-628 Hz).
  There is no carrier evidence in the tested routes (amplitude, frame,
  ancillary) for either MP3. MDCT-coefficient embedding and keyed or
  exotic gain encodings are untested. The stash question is not closed
  in general.
- Freeimage render (claim on observation_2066139ee96a497683b6d44201d5c6b0):
  the forwarded live-browser render (2026-10-30 03:13-03:16 UTC) shows
  an abstract computer-generated circular mesh: concentric rings of
  small circles, a beaded outer rim, essentially monochrome, no readable
  words at rendered scale. Page and alt metadata carry a glyph string
  plus shader wording (a generative-art lead). No pixel-level analysis
  was performed. The coordinator verified file bytes only and did not
  view the rendered pattern.
- SVG chain (INFERENCE from geometry plus export classes plus title
  frame plus count-matched structure; lane raw file, no capture record):
  the SVG linked from the HF page IS a Desmos export of the sine-star
  artwork. Same artwork is confirmed. Same operator stays unproven.
  The SVG root title and the Desmos page title are similar, not
  byte-identical. The export is monochrome (#EEEEEE) while the state
  uses green/red pairs. That difference is unexplained.
- CDX re-census (lane raw files, no capture record): no detected
  post-Oct-27 Wayback rows in 24 of 26 forms. Two forms are inconclusive
  (dnif-jina-http, neo-jina-https: "Temporarily Offline" 503 pages in
  both runs). Latest capture overall stays 2026-10-27. Live pages were
  up Oct 30, so Wayback absence does not mean activity absence.

## Corrections to phase 1 (all honored in FULL-REPORT.md section 8)

- C1: decode-provenance caveat closed (fresh Oct 27 fetches byte-identical).
- C2: gyo ref date typo fixed (2026-1017-0614-08, not 2026-1027-0614-08).
- C3: token-cleanliness claim was false for the four phase-1 raw infra
  files. Those files are NOT in this push. No phase-2 file reproduces a
  token value.
- C4: "56 rows per page" is the circle-row count only. True binary row
  totals are 96 (Neocities) and 112 (HF Space).
- D1: linguist body-line counts (25/24 distinct, 13 common) downgraded
  to unverified. The "13 distinct lines shared" figure stays only as
  the linguist lane's reported observation.
- C5: Desmos tone second argument is gain, not duration. The "0.556 s
  sequence" reading is withdrawn.

## Gaps (in priority order)

1. MP3 MDCT-coefficient steganalysis plus keyed or exotic gain encodings.
2. TXT glyph bulk decode.
3. SVG path-coordinate encoding test.
4. Live Desmos playback check (chord vs arpeggio; needs live-browser
   delegation).
5. CDX re-attempt of dnif-jina-http and neo-jina-https once the Wayback
   backend clears.
6. Recovery of the March 25, 2026 corsproxy trace from the prior corpus
   snapshot.
7. Jina-independent sibling discovery (for example HF API listing).
   The census stays a lower bound.
8. Same-operator question (no attribution pursued; out of scope).
9. Freeimage pixel-level analysis (62 MB WEBP verified by format, size,
   and hash only).
10. ww served-capture identity (20261020014219 is not an exact CDX
    timestamp; nearest 20261020014241/42, warc/revisit to a 2025-08-13
    original).

## Swarm-revival conditions (none present)

Agent terms in any unexamined asset; a demonstrated beacon pattern;
tool or API traces; linkage to a known incident; a decoded tasking payload.
