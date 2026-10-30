# o-pattern relay-jina-reader family — FULL REPORT (phase 2, superset)

Date: 2026-10-30. This report supersedes `REPORT.md` (2026-10-30, phase 1).
It contains ALL evidence and links from phase 1 and phase 2: every lead
with its verdict, every primary source URL, every evidence file path, the
TXT content, the MP3 decode result, the Desmos tone result, both image
renders, the updated timeline, corrections to phase 1, the adversarial
review of the new claims, and honest gaps.

Authorization: the operator commissioned phase 2 explicitly ("read the
source files, ingest and push everything, full report with all evidence
and links"). Nothing in this report is published outside the silent-locus
repo. No person was contacted. Collection was passive GET-only on openly
public surfaces, except the two live-browser renders forwarded by the main
agent (freeimage rendered, SVG browser attempt failed — see §4). No
logins, no sessions, no POSTs, no 429 retried.

Work dirs: `~/workspace/o-pattern-followup/` (phase 1: `REPORT.md`,
`*-FINDINGS.md`, `raw/<lane>/`) and `phase2/` (phase-2 findings,
`raw/<lane>/`, `STATUS.md`). Nothing under `~/workspace/silent-locus/`
was mutated during investigation; the Factum lane + this report are the
phase-3 additions (see §12).

Token rule: NO credential-like token value and NO token-bearing URL
appears in this report or in any phase-2 file (verified by the phase-2
lanes: only omission markers where a token was removed). Exception to
note honestly: four phase-1 files under `raw/infra/` DO contain token
values (see §8, correction C3) — those four files are NOT part of the
phase-3 push. Otherwise evidence files keep full observed values, no
redactions.

## Headline verdict (updated)

**Art-like family, stash narrowed but NOT excluded.** Everything actually
examined reads as composed generative/sound art with a physics theme:
palindromic emoji fields, a sine-star Desmos graph with a tone ladder,
a ×3 tone-stack MP3, a noise-swell MP3, a circular-mesh shader image, and
a glyph TXT carrying physics-themed definition-style fragments (characterization, see §5). **NOT a swarm lead**
stands as a negative finding only: no agent/fleet/bot term and no positive
swarm indicator in ANY examined asset — and the examined set is now much
larger than in phase 1 (both images retrieved and rendered, TXT read in
full, MP3 amplitude patterns decoded, Desmos tone computed). It is still
not a proof, because four narrow stash surfaces remain untested (see §11):
MP3 MDCT-coefficient embedding, keyed/exotic gain encodings, the TXT
glyph bulk itself, and SVG path-coordinate encoding. No single purpose
(art, puzzle, stash, rig) is proven. Art project remains the strongest
fit to examined content.

## Per-lead verdicts (updated)

| Lead | Verdict | Evidence |
|---|---|---|
| Swarm / agent infrastructure | KILLED as a positive claim; stands as negative finding | No agent/fleet/bot/task term in the two Oct 27 renderings, the Desmos state, the TXT full text, the SVG, or the freeimage render/metadata. No API/tool traces. No beacon pattern. Revival conditions in §10 — none present. |
| Visible emoji layer carries a text message | KILLED for 8-bit ASCII; OPEN for cycle-order / bitmap / keyed readings | 860 binary attempts failed; rows are N+1+N palindromes, 3-value run-length alphabet. Decode counts now rest on FIRST-HAND provenance (fresh Oct 27 fetches byte-identical — §8, correction C1). Cycle-order diff, bitmap rendering, keyed mappings untested. |
| MP3 ww = tone-stack piece | CONFIRMED (spectral + envelope) | 7 constant tones ≈×3 series, 3 sections, §1 reprise. Amplitude decode attempted and failed cleanly (see §3). |
| MP3 mUr = noise-swell piece | CONFIRMED (spectral + envelope) | Broadband noise + 7 fixed tones, one fade envelope. Noise does not repeat. Amplitude decode attempted and failed cleanly (see §3). |
| MP3s carry appended/metadata stego | KILLED (narrow sense) | Frame parse ends exactly at EOF both files; no ID3, no second stream; ancillary = deterministic encoder stuffing, no payload bytes. |
| MP3s carry LSB stego | NEITHER PROVEN NOR EXCLUDED | Decoded-PCM LSB test performed but judged the wrong layer (measures quantizer determinism, not stored data). Frame/ancillary tests are the informative layer. |
| MP3s carry MDCT / keyed-gain stego | OPEN (untested) | Coefficient-level steganalysis and keyed/exotic gain encodings were outside the phase-2 brief. |
| Desmos = same family, not same content | UPGRADED: same artwork confirmed | The SVG linked from the HF page IS a Desmos export of the sine-star (see §4). Same artwork established; same operator still unproven. |
| Desmos tone = ww's tone set | CONFIRMED (exact ladder match) | ww's 7 tones equal Desmos tones n=7–13 within 0.1 Hz. The Desmos list extends the ladder by 7 infrasonic tones below and 1 ultrasonic above. mUr: no match. |
| Desmos tone duration reading | CORRECTED | The second tone argument (1/27) is GAIN, not duration (see §8, correction C5). The state specifies no duration; in Desmos it sounds continuously while unmuted. Chord-vs-arpeggio rendering unsettled. |
| gyo.tc = Megalodon citation archive | CONFIRMED | Homepage + operator page + ref form demonstrated; JST reading coherent on two independent ordering checks. |
| corsproxy hop = in-browser JS fetch | OPEN (plausible mechanism only) | March 25, 2026 trace NOT reproduced by CDX; hop order and actor unknown. |
| Both live pages still up | CONFIRMED at two time points | 200 at 2026-10-30 01:30 UTC (phase 1) and re-fetched byte-identical 2026-10-30 ~03:19–03:30 UTC (source audit). "Still up" expires on quotation. |
| Live HF page has MP3 refs the Oct 27 jina rendering lacked | CONFIRMED as HTML contrast | MP3 filenames in both live files, zero in Oct 27 jina HF. Update-vs-jina-drop INDISTINGUISHABLE. |
| Reversed-word naming = only swen/news + dniferp/prefind | KILLED | CDX adds etis→site AND ewitcepsrep→perspectiwe (paired with forward `perspectiwe-site`); titgtit, evihcrarchive, emitime are palindromes. Naming grammar is reversal + palindromisation. |
| Naming intent = play, not concealment | WEAKENED to inference | Paired forward+reverse form favours play for paired hosts; concealment as secondary effect conceded; filter-evasion has no evidentiary base either way. |
| Family = 8 hosts, 1,347 captures, back to 2024 | WEAKENED (see qualifiers) | 1,347 unique CDX rows found by jina-stem discovery; only ~48% of per-file rows are status 200; 2024 row proves a host string existed, not same content/operator continuity. Etis first appears 2025-06-28, not 2026-03-30. |
| Oct 27 pages = one template, HF a subset of Neocities | WEAKENED (narrowed) | HF sanitized codepoint set (28) ⊆ Neocities' (33), HF-only: none. But row repertoires are NOT subsets (each has shapes the other lacks); live pages are now byte-identical after stripping, so the Oct 27 difference may be a rendering/version artifact. Row totals corrected: 96 (Neocities) / 112 (HF) binary rows, not "56 rows per page" (§8, C4). |
| SVG image content | RETRIEVED + RENDERED (was OPEN/blocked) | Desmos sine-star export, monochrome #EEEEEE, 199 paths. See §4. Browser attempt failed; worker curl via exact stored link succeeded. Reconciliation in §4. |
| freeimage.host image content | RETRIEVED + RENDERED (was OPEN/blocked) | Abstract generative circular-mesh art, monochrome, shader metadata. See §4. |
| TXT upload content | READ IN FULL (was OPEN/unread) | UTF-16LE, 403 lines, line-level palindrome, 8 physics definition sentences, zero agent terms, zero links. See §5. |
| Forum thread embedding the MP3s | OPEN (not found, not excluded) | Public Discourse search returns zero posts for all three short-URL IDs; that is a search negative, not proof of no thread. |
| Post-Oct-27 Wayback activity | NONE FOUND in 24/26 forms | Zero new rows, zero new siblings. 2 forms inconclusive (repeated 503s). See §1. |
| TXT glyph bulk carries a message | OPEN (undecoded) | The readable sentences are 8 fragments; the glyph bulk (97%+ of characters) is undecoded. |
| SVG path data carries a message | OPEN (untested residual) | No anomaly in path counts/ranges/groupings suggests encoding; coordinate steganography not tested. |

## 1. Capture timeline (CDX census + phase-2 re-census)

Phase-1 method: Wayback CDX via `http://web.archive.org/cdx/search/cdx`
(port 80; :443 times out on this VM). Flaky backend: 11 queries failed
first attempt (503/504) and recovered on retry at 60–90 s spacing; no 429
seen. Key method catch: https-jina and http-jina are distinct CDX capture
sets — the dive's exact timestamps lived in the http form; a one-scheme
census misses them. Direct-stem prefix queries returned empty while the
jina-stem prefix found siblings, so this census is a LOWER BOUND: any
sibling never read through jina is missed. Counts are CDX rows (timestamp
+ URL, query stripped), NOT page loads: 1,483 per-file rows, only 708
status 200; the rest are warc/revisits, redirects, 404 favicons,
403/414/400/401 rows.

| Host | Direct | Jina | Total | First | Last |
|---|---|---|---|---|---|
| ooooiiiiiiiioooo-o-swen-o-news-o.static.hf.space | 517 | 31 | 548 | 2024-03-22 15:40:04 (direct index.html) | 2026-10-20 03:43:07 |
| ooooiiiiiiiioooo-ooooiiiiiiiioooo.static.hf.space ("doubled") | 241 | 15 | 256 | 2025-06-28 18:36:55 | 2026-10-27 15:36:24 (jina root) |
| ooooiiiiiiiioooo-o-dniferp-o-prefind-o.static.hf.space | 133 | 30 | 163 | 2025-08-02 07:34:49 | 2026-10-17 01:17:13 |
| ooooooooooooooooooooooooooo.neocities.org | 47 | 13 | 60 | 2026-06-26 09:17:30 | 2026-10-27 15:57:24 (jina root) |
| ooooiiiiiiiioooo-o-titgtit-o-titgtit-o.static.hf.space (NEW) | 112 | 14 | 126 | 2025-06-15 22:31:29 | 2026-10-24 00:01:40 (jina) |
| ooooiiiiiiiioooo-o-evihcrarchive-o-evihcrarchive-o.static.hf.space (NEW) | 86 | 1 | 87 | 2026-02-02 04:19:38 | 2026-10-17 02:33:08 |
| ooooiiiiiiiioooo-o-etis-ewitcepsrep-o-perspectiwe-site-o.static.hf.space (NEW) | 68 | 10 | 78 | 2025-06-28 19:22:35 (direct; CDX table's 2026-03-30 jina date is wrong) | 2026-10-17 04:13:20 |
| ooooiiiiiiiioooo-o-emitime-o-emitime-o.static.hf.space (NEW) | 26 | 3 | 29 | 2026-02-18 06:59:20 | 2026-10-17 04:13:16 |

Total: 1,347 unique rows, 2024-03-22 to 2026-10-27 (1,230 direct + 117
jina). Monthly volume: 2024: 19; 2025: 165; 2026: 1,163 (ramp from Feb
2026: Feb 110, Mar 109, Apr 76, May 138, Jun 157, Jul 206, Aug 117, Sep
95, Oct 106). The ramp and the clusters are CDX/crawl patterns — Wayback
scheduling produces bursts (e.g. July 25: 123-row swen crawl, 86 unique
captures in one day). No operator inference follows from volume or
clustering. In particular the Oct 17 "three index.html captures within 5
seconds" (emitime 04:13:16, etis 04:13:20, titgtit 04:13:21) is verified in
raw CDX, but two of the three rows are warc/revisits — a crawl/dedup
pass, not three fresh fetches.

Milestones: 2024-03-22 swen index.html (earliest row; sparse swen rows
through 2024–2025 look like a different regime from the 2026 ramp — same
host string, continuity unproven); 2025-06-15 titgtit first; 2025-06-28
doubled + etis first (same week); 2025-08-02 dniferp first; 2026-02-02
evihcrarchive first; 2026-02-18 emitime first; 2026-03-26 doubled first
jina; 2026-06-26 Neocities first; 2026-07-25 biggest day (86 unique);
2026-09-05 second-biggest (30 unique); 2026-10-16–17 cross-host cluster
(25 + 24 rows); 2026-10-20 Neocities + swen activity; 2026-10-23
Neocities (direct + both jina forms; no rows Oct 24–25 — the dive's
"Oct 23–25" window narrows to Oct 23); 2026-10-27 15:32:41 doubled jina
(Hit 2) and 15:57:24 Neocities jina (Hit 1) — latest captures found as of
the Oct 30 run.

Reconciliation with the dive: May 24 dniferp, June 17 doubled (both
times), Sept 10 swen, and both Oct 27 hits all CONFIRMED EXACTLY (the
first three in http-jina form, Oct 27 in https-jina form). The
2026-03-25 corsproxy→jina swen trace was NOT REPRODUCED (corsproxy filter
and `?url=` queries both empty) — it rests on the prior corpus snapshot
only.

Phase-2 re-census (one pass, `from=20261028`, same query shapes, 26
queries: 8 hosts × direct/https-jina/http-jina + 2 jina-stem discovery):
ZERO new rows and ZERO new siblings in 24 of 26 forms (all valid empty
`[]`). Two forms failed with "Temporarily Offline" 503 pages even after
retry in BOTH runs and are inconclusive, not evidence of captures:
dnif-jina-http (dniferp http-jina form) and neo-jina-https (neocities
https-jina form). For dnif, direct + https-jina are empty; for neo,
direct + http-jina are empty. The re-census therefore shows no detected
post-Oct-27 Wayback activity but does NOT prove zero activity (2/26
forms unobserved). Live pages were up Oct 30, so the family may remain
active without new Wayback captures. Latest capture overall remains
2026-10-27. A re-attempt of the 2 failed forms once the Wayback backend
clears would complete 26/26 coverage, if the operator wants it.

## 2. Decode: the visible emoji layer does not yield text (and why)

Source caveat CLOSED in phase 2: the phase-1 decode lane worked from the
linguist lane's local capture copies because direct Wayback fetches of
both Oct 27 captures returned HTTP 429 on 2026-10-30 01:30 UTC. The
phase-2 source audit re-fetched both captures fresh (200, byte-identical
to phase-1 infra files); the fresh copies sanitise to exactly the
linguist/decode input hashes. Decode counts now rest on first-hand
provenance, and phase-1 §8 item 6 is done for the core captures.

What was tried: binary, both polarities (green=1/white=0 and reverse) ×
MSB/LSB × 8-bit, per-row, concatenated per shape, and in document order
— 398 attempts (Neocities) + 462 (HF Space) = 860. Coloured-square
sequences under rainbow order, codepoint order, and first-appearance
mappings. Run-lengths as data.

Result: no coherent text under any mapping. Outputs were 0xFF/NUL/
replacement bytes; concatenated printable ratio 0.000–0.064, never
letters. Every coloured-square sequence is an exact palindrome under
every mapping tried.

Why it fails structurally: each page has only 3 distinct circle rows and
3 distinct square rows, each a palindrome of the form N green + 1 white +
N green (e.g. 40+1+40, 21+1+21, 12+1+12; Neocities run lengths {40, 21,
12} / {40, 18, 13}, HF {40, 3, 12} / {40, 10, 13}), repeated 8–32 times.
A row's information content is one number (its half-length), not 81
bits. Spaced groups are the same rows re-spaced. Rare glyphs (Bamum,
Batak, Tai Tham, etc.) occur only in fixed frame positions — openers,
closers, alternating image labels — and never vary between cycles.
Codepoint inventory: Neocities 33 distinct non-ASCII (6,951 chars), HF
28 (5,489 chars), HF's sanitized set a subset of Neocities'. True binary
row totals (corrected, §8 C4): 96 (Neocities) and 112 (HF Space), not "56
rows per page" (56 is the circle-row count only).

Explicitly NOT tested (still open): the sequence of row-shape choices
across cycles (a chosen order could carry a short signal; the cycle-order
diff is undone); rows as a 2-D bitmap; any keyed mapping over the
3-value run-length alphabet (unfalsifiable without a key, therefore also
unexcluded); anything in the linked assets beyond what phase 2 covered.

## 3. MP3s: two different synthetic audio artifacts, amplitude-decoded

Retrieved from Wayback (not live forum), analysed locally only
(ffprobe/ffmpeg, numpy/scipy). No transcription service, no uploads.
Intermediate WAVs deleted after analysis; re-derivable with ffmpeg.
Phase-1 files: `raw/mp3/`. Phase-2 analysis: `phase2/raw/mp3decode/`.

- wwM5xXlIc1QTcAH3uhXuMYyJauL.MP3 ("ww") — 253.218 s (4:13.2), mono,
  48 kHz, ~320 kbps avg, 10,126,848 bytes, sha256
  355d706fe36e73a45fdbe30c7ea36a325dc941c9f55abe8bca29a35346154cde.
  Seven constant tones ≈25.9, 77.7, 233.2, 699.6, 2098.7, 6296.2,
  18888.7 Hz — each ≈3× the previous, >60 dB above everything else.
  Three sections split by two ~1.88 s gaps: §1 0–84.39 s patterned
  amplitude (RMS swings −10 to −43 dB); §2 86.27–166.95 s one smooth
  swell (−56 → −10 → −63 dB); §3 168.83–253.22 s a reprise of §1
  (RMS-envelope r = 0.988 at zero lag; waveform r ≈ 0.83 at +18 ms — a
  reprise, not a bit-identical loop). No formants, no speech band
  structure, no melody. Provenance flag: requested capture
  20261020014219 is NOT an exact CDX timestamp (nearest 20261020014241/
  42, warc/revisit to an original 2025-08-13 capture) — which capture
  Wayback actually served is unconfirmed, though the file parses
  cleanly. Original: https://forum.fractalfuture.net/uploads/short-url/wwM5xXlIc1QTcAH3uhXuMYyJauL.MP3
  ; Wayback retrieval:
  http://web.archive.org/web/20261020014219id_/https://forum.fractalfuture.net/uploads/short-url/wwM5xXlIc1QTcAH3uhXuMYyJauL.MP3
  ; gyo.tc ref 2025-0813-1654-16.
- mUr2xClu6x7OUSFz70Ylk6U5GjX.MP3 ("mUr") — 84.406 s (1:24.4), stereo,
  48 kHz, 320 kbps, 3,378,240 bytes, sha256
  20d09d309f03c5aea6fc9411678e99fec8b5ee2179d75a42f160aad3a70792f8.
  Broadband noise across the full band (L/R essentially uncorrelated,
  r ≈ 0.01) plus seven fixed tones ≈5669, 9127, 10088, 11337, 13547,
  17447, 19216 Hz present at every time checked, under one smooth
  fade-in/fade-out (active ~2.08–82.33 s). Capture 20261019071014 is an
  exact CDX entry. Original:
  https://forum.fractalfuture.net/uploads/short-url/mUr2xClu6x7OUSFz70Ylk6U5GjX.MP3
  ; Wayback retrieval:
  http://web.archive.org/web/20261019071014id_/https://forum.fractalfuture.net/uploads/short-url/mUr2xClu6x7OUSFz70Ylk6U5GjX.MP3
  ; gyo.tc ref 2026-1019-1618-09.
- Both: MP3 MPEG-1 Layer III, only tag `LAME3.99r` (common encoder —
  weak authorship evidence alone); no ID3v2/v1, no title/artist/comment,
  no attached picture, single audio stream. Frame parse ends exactly at
  EOF for both (0 trailing bytes) — no appended-data or metadata stego
  indicator. Phase-2 hashes match phase 1 exactly; no re-fetch needed.
  All 14 tones re-confirmed by long-FFT peak search.
- Comparison: different content, not versions of each other
  (cross-correlation ≈ 0; tone sets disjoint; different
  channels/durations/levels). Only structural relation: ww §2 and mUr
  share a bell-shaped fade envelope (r ≈ 0.92 — expected for any two
  long fades, not evidence of shared audio). Length recurrence noted
  without over-reading: ww sections ≈84.4 / ≈80.7 / ≈84.4 s; mUr 84.4 s
  total, ~80.2 s active.
- "No speech" grade: no speech-like structure detected
  (spectral/envelope), NOT "no speech" as fact — no transcript exists;
  a whispered/vocoded voice under tones would not be excluded by these
  measures alone.

Phase-2 amplitude-pattern decode (the headline finding): there is ONE
shared gain channel, not seven data channels. Per-tone heterodyne
envelopes correlate at 0.93 (ww §1/§3) and 0.91 (mUr) across tones; ww's
7-tone vector is all-on or all-off in 83.5% of §1 time steps. So
per-tone data is dead on arrival, and the 7-bit "bitmap" reading is
empty by construction.

- ww §1/§3 binary tests (median threshold, quanta 0.1/0.25/0.5/1.0 s,
  both polarities, MSB/LSB): best printable fraction 0.09–0.30 vs. 0.37
  random baseline; samples gibberish; run structure is musical phrasing
  (mean run 0.8–1.1 s, max ~15 s sustained passage). No phrase-repeat
  period (envelope autocorr peaks 0.43 at ~1.05 s, decays to ~0 by 20 s).
- ww §3−§1 difference: per-tone envelope correlation 0.947–0.987,
  difference std 1.7–4.4 dB vs. envelope std 10–13 dB, mean ≈ 0 —
  no structured second channel detected in the difference by the tests run.
- mUr: bit tests 0.04–0.13 printable (a monotone fade thresholded into
  long runs); tone-notched noise-loop test max |NCC| 0.027–0.031 (random
  level) — noise does not repeat. (A loop-probe normalization bug in
  the first results pass, values ~1.7e5, was caught and corrected;
  corrected values are in `loop_correction.json` and the findings doc.)

Phase-2 stego assessment:

- Frame walk: ends exactly at EOF both files, 14,072 frames, zero
  bad/free-format frames, zero reserved-field anomalies (emphasis/
  copyright/private 0 throughout; standard LAME delay 576, padding
  860/659) — no unused-field indicator.
- Ancillary/stuffing (ww, 6.5 MB inventoried): 96.75% `0x55`/`0xAA`
  filler + `LAME3.99.5` version string (11,712 occurrences) + ~9 B/frame
  main-data bleed — no payload bytes; deterministic encoder stuffing.
  mUr ancillary is tiny (median 6 bits/frame) with the same encoder
  pattern in easy frames — no indicator.
- Decoded-PCM LSB: ww ones fraction 0.4899, chi2 4973.6 (p≈0); mUr
  active-only ones fractions 0.4999/0.4997, chi2 0.14/1.62 (p=0.71/0.20)
  — test performed but judged the WRONG LAYER: decoded LSBs measure
  quantizer determinism, not stored data, so this neither proves nor
  excludes MP3-domain stego. The frame/ancillary tests are the
  informative layer.
- NOT excluded (stated explicitly): MDCT-coefficient embedding and
  keyed/exotic gain encodings — coefficient-level steganalysis was
  outside the phase-2 brief.

Verdict on the stash question from the MP3 side: no positive stash
evidence; amplitude and frame/ancillary routes are closed for the tested
forms. The MP3s read as composed sound art, with no carrier evidence in the tested routes (amplitude, frame, ancillary) — but this
does not close the stash question in general.

## 4. Images + Desmos: both visual assets retrieved, chain confirmed

### GitHub SVG (odd images) — RETRIEVED AND RENDERED (was blocked)

Phase-1 status: Wayback capture 20261027145327 returned HTTP 429 (bot
block) on 2026-10-30 01:34 UTC; block page discarded, not retried.
Phase-2 browser attempt (2026-10-30 03:12–03:28 UTC) then FAILED:
token-free Wayback forms returned "The Wayback Machine has not archived
that URL"; other token-free variants and the closest-capture redirect
form gave the same result; CDX returned NO captures under
private-user-images.githubusercontent.com/186144119/; the gyo.tc ref
2026-1027-2355-45 itself returned a Japanese "archive not found" message
for that URL and date; the original signed image address returned HTTP
404, consistent with its short-lived signing window having expired.
Content was entirely unknown at that point, and the SVG was carried as
the highest-value gap.

Recovery (wayback executor, one curl attempt, 2026-10-30 ~03:16 UTC):
following the gyo ref 2026-1027-2355-45 link EXACTLY as it appears in the
stored live-page copy (IMG SRC attributes) with `curl -L` returned HTTP
200, `image/svg+xml`, 416,706 bytes, sha256
d8660ed21a49b058e88a00db800bee627a6b9b123ce6bc2110d5780a42546d96.
Saved: `phase2/raw/wayback/svg-wayback-20261027145327.svg` (identical
`.bin` copy). Coordinator verified hash + file type independently. The
underlying token-bearing URL is NOT recorded anywhere in phase-2 work;
the fetch script (`raw/wayback/fetch_svg_via_gyo.py`) extracts the link
at run time and never prints it.

Reconciliation: the browser and worker results are compatible, not
contradictory — they tried different URL forms. The capture resolves
through the exact stored link and NOT through token-free forms,
consistent with the capture being keyed to the full signed URL. The
"signed URL expired" 404 applies to fetching the original image
directly, not to the archived capture served through the stored link.
Observed wrinkle: the stored link's host segment is NOT plain ASCII
"gyo.tc" — codepoints 0x47 0x59 0x24c4 0x2e 0x54 0x43, i.e. the third
character is U+24C4 (circled Latin capital O) in place of ASCII "O".
Recorded as observed in the stored live-page copy; no mechanism is claimed for how it resolved. The circled-O form is systematic in the stored copy (121 occurrences per live file, 0 plain-ASCII occurrences, per the independent review). Whether the live page as served contains this form, or the saved copy introduced it, is unproven. Do NOT use the signed URL in any form to
test this further; no browser retry is owed.

Content (local analysis + local render, no live browser needed):

- Root element (abbreviated, xmlns declarations omitted) `<svg version="1.1" viewBox="0 0 2000 2000" width="27"
  height="27">`, Desmos export classes (`dcg-svg-background`,
  `dcg-svg-tickmark`, `dcg-svg-curve`). Root `<title>` is the family's
  glyph-framed title (same vocabulary as the Desmos page title).
- 199 `<path>` elements, 135 `<g>` elements, 19 `<title>` elements (1 root
  + 18 expression titles: 3, 4, 9, 10, 15, 16, 21, 22, 27, 28, 33, 34,
  40, 41, 46, 47, 52, 53 — nine expression-title pairs, count-matching the state's nine sine-wave groups
  of the Desmos state).
- Colors: 198 of 199 paths stroke #EEEEEE (near-white); 90 fills
  #EEEEEE. No green/red strokes in the export. No `<text>` elements. No
  URLs except the two W3C namespace declarations.
- Local render (cairosvg, 1000×1000 PNG,
  `phase2/raw/wayback/svg-render-1000.png`, 253,870 bytes, sha256
  319d8a6d4f8a6985acaa2fa05feef59b1d0da533094918f8d7d7081ca8c0dec9):
  a circular, symmetric woven star/mandala in thin near-white curves on
  a black field — a central rosette where all bands converge;
  braided/twisted bands vertically, horizontally, and along both
  diagonals; petal/leaf-shaped lobes between the bands; an approximately
  circular outer boundary. No text, no axes, no labels, no people, no
  recognizable objects.
- Chain verdict: CONFIRMED at the SVG node. The image linked from the
  live HF page IS a Desmos export of the sine-star artwork — same glyph-vocabulary title frame (similar, not byte-identical), same nine-group structure, same woven-star geometry as the
  lem1oik7lp state. Phase 1's "rendered SVG→Desmos chain unverified" is
  now verified in substance, and "same family, not same content"
  upgrades to "same artwork confirmed." Same-operator stays UNPROVEN
  (shared artwork ≠ proven same author). No agent/fleet/bot term, no
  text, no payload structure visible; no swarm-revival trigger. Color
  discrepancy recorded honestly: the export is monochrome #EEEEEE where
  the state describes green/red mirrored pairs — export styling or a
  different graph revision are both possible, neither claimed. Residual
  (untested, no anomaly suggesting it): SVG path-coordinate encoding.

### freeimage.host image (even images) — RETRIEVED AND RENDERED

Phase-1 status: Wayback capture 20230216011340 of
freeimage.host/i/HGHQml9 returned HTTP 403; not repeated. Phase-2
live-browser render (2026-10-30 03:13–03:16 UTC) succeeded: the page
initially showed a "Play GIF - 62.2 MB" placeholder; after clicking, the
image rendered. Page rendered:
https://web.archive.org/web/20230216011340/https://freeimage.host/i/HGHQml9
(Wayback toolbar: 01:13:40 Feb 16, 2023). Direct archived file:
https://web.archive.org/web/20230216011350im_/https://iili.io/HGHQml9.webp
(archive redirected the file request by 10 seconds). Original image URL
shown: https://iili.io/HGHQml9.webp. Uploaded 2023-02-16 01:12:37 per
the page. Dimensions/file details shown on the page: 16382 x 16382,
WEBP, 62.2 MB.

- What it shows (forwarded live-browser render 2026-10-30 03:13–03:16 UTC; coordinator verified file bytes only and did not view the rendered pattern; no pixel-level analysis performed): an abstract, geometric circular pattern — NOT a
  photograph, NOT a graph (no axes, labels, data lines, people, or
  recognizable objects). A very large disc/dome of many concentric rings
  of small white/light-gray circles/rings, densely packed; rings larger
  near the outer edge, progressively smaller toward the center, creating
  a mesh/moiré, sphere-like effect. Outer rim beaded with small white
  dots/circles. In the page view it appeared white/gray on black with a
  solid black semicircular area at bottom-center (the disc's center);
  in the direct-file viewer the same form appeared much paler (faint
  light-gray/white disc with plain central circle), consistent with a
  large high-resolution animated/very detailed pattern whose contrast
  varies with scaling. Colors: essentially monochrome (black, white,
  grays); no other colors visible.
- Text/symbols INSIDE the image: no ordinary readable words legible at
  rendered scale; small repeating motifs are circles/rings, some with
  dot centers, not letters.
- Classification: abstract computer-generated circular mesh, not a
  graph, emoji, or photograph.
- Page/alt metadata text (NOT text inside the rendered pattern): the
  page title and the image's alt/metadata text contain a long symbol
  string (beginning with glyph symbols) and mirrored/reversed text,
  including references to CALAMEO.COM/accounts/6048259,
  GITHUB.COM/0000OOOO0000, FLICKR.COM/80808, P3D.IN/u/OOO,
  PLNKR.CO/users/O, YOUTUBE.COM/channel/UCGV51gh3hcPh1FKx4ZxvJ2g,
  SUM.IN.UA/S/INTUJICIJA, and shader wording such as
  LINEAR_RADIAL_GRADIENT_SHADER, BRIGHTNES_O=.65625,
  ROOT_POWER_O=19.48046875/4. Handling rule (explicit): this is evidence
  of the same o-pattern/glyph-vocabulary family and of shader-art
  character. It is NOT to be used for any person/operator attribution —
  hunt scope is agents/infrastructure only. No handle above is pursued as an identity, and no contact is
  made with any account or service named there.
- Coordinator verification of the file bytes (passive GET, 2026-10-30
  03:17 UTC, from the direct archived file URL above): HTTP 200,
  62,243,550 bytes — matches the page-stated 62.2 MB. `file` identifies
  it as RIFF Web/P image data. sha256
  66a713ce8d11889a3c79cfd4664b1902a3f3665eb224aa7d69ba450659f14f8d.
  Saved: `phase2/raw/freeimage/HGHQml9.webp`. Dimensions NOT
  independently confirmed locally: ffprobe reports the 16382x16382
  picture size as invalid (decoder limitation on huge WebP), so 16382 x
  16382 stands as page-stated + render evidence only. No pixel-level
  analysis was performed on the 62 MB file; that remains available if
  the operator wants it.
- Phase-2 wayback attempt on the same capture (worker, one attempt, no
  redirect following) returned the viewer page HTML (200, text/html),
  not image bytes — superseded by the browser render + WEBP download.
- Verdict: RETRIEVED. No readable words inside the pattern at rendered
  scale; no agent/fleet/bot term in the rendered content; no
  swarm-revival trigger. New characterization lead: SHADER ART. The
  metadata wording plus the concentric-ring mesh form strengthens the
  generative-art reading of the whole family. It does not by itself
  prove or kill a stash: a shader pattern can carry parameters, but no
  parameter-to-payload mapping is demonstrated here, and no pixel-level
  decode was attempted.

### Desmos calculator — state analysed, tone computed

Retrieved from state JSON (Ghost Archive capture 20260519232539 of
desmos.com/calculator/lem1oik7lp; state version 11, last modified
2026-04-10 06:52:07 GMT; state JSON sha256
779703e551f8b1475520e3dee36dd752473e59919030777080534a94c189b6d6).
No live render/screenshot in phase 1. Phase-2 addition: the live page's
parent link resolves (Ghost Archive short link
https://ghostarchive.org/archive/H5btX) to the SAME calculator
(lem1oik7lp) — same-node confirmation only, NOT evidence of SVG
content, and NOT a new graph.

- Bare picture, not a data plot: grid off, both axes off, axis numbers
  off; viewport x −1.134 to +1.134, y −1.628 to +1.628.
- 68 items: 55 expressions, 11 folders, 1 table, 1 text note. Folder
  titles are glyph pairs/single glyphs — the same glyph-vocabulary
  habit as the emoji pages, used as section labels, not readable words.
- The picture: nine rotated sine-wave groups (labels 1, 2, 3, 11, 22,
  33, 44, 55, 66), rotation angles 30°/90°/150° (each used three times),
  opposite sine curves in green (#388c46) and red (#c74440), harmonics
  1/3/9 (powers 3^[0…I], I = 2), single-digit groups over −1 < X < 1,
  double-digit over −1/2 < X < 1/2 with vertical offset ±3/(2√3). A
  symmetric woven sine-star — a geometric artwork, not a data plot, not
  an emoji sequence. No equation references emoji, circles, squares, or
  the pages' block patterns. Phase-2 re-confirmation: 9 groups (1: 30°,
  2: 90°, 3: 150° centered; 11: 150°, 22: 30°, 33: 90°, 44: 150°, 55: 30°,
  66: 90° offset ±3/(2√3)), green/red mirrored sine pairs (18
  expressions × harmonics 1, 3, 9 via I = 2 = 54 curves), grid/axes off,
  68 items exactly.
- Tone folder (id 153): constant O ≈ 84.40602258995403 (fixed slider;
  full value
  84.406022589954030768899117092091000289089388918088900852079),
  hidden V = 0, hidden W = 14, hidden A = 0, hidden U = 3, I = 2.
  Exact tone expression (id 155, quoted from state):
  tone(U^((V·U^A ... W·U^A)/U^A)/O, 1/3^3). It reduces to frequencies
  3^n / O, n = 0–14 — 15 tones, each exactly 3× the previous.
- CORRECTION to the phase-1/phase-2 brief (see §8, C5): per Desmos's own
  Help Center Tone article (updated 2026-07-23), `tone(frequency,
  gain)` takes gain as its optional second argument; there is NO
  duration parameter. So 1/3^3 = 1/27 ≈ 0.037 is a very quiet gain, and
  the expression specifies no duration (in Desmos it sounds
  continuously while unmuted). The brief's "15 × 1/27 s = 0.556 s
  sequence" is therefore NOT a property of the state. Likewise the
  state + docs do NOT settle whether a list frequency plays as a chord
  or an arpeggio — both renderings were produced locally and a live
  Desmos playback check is logged as an open item, not claimed.
- Frequency range + count: 15 tones, 0.01185 Hz to 56,666.21 Hz. Only 7
  (n = 7–13: 25.91, 77.73, 233.19, 699.58, 2,098.75, 6,296.25, 18,888.74
  Hz) fall in Desmos's 20–20,000 Hz input band; n = 0–6 are infrasonic,
  n = 14 ultrasonic. Clearly audible core is n = 8–12.
- What it sounds like (from synthesis parameters — NO playback
  verification was available, stated as such in the findings): chord
  reading: a sparse, quiet, metallic cluster of equal-amplitude pure
  tones with no consonant harmonic-series quality (ratios are powers of
  3, not harmonics of an audible fundamental). Arpeggio reading
  (brief's version): a 0.56 s rising zip of 37 ms blips, octave-plus-
  fifth jumps, ending in a thin squeak. Either way: no melody, no
  rhythm, no words. Each step is 19.02 semitones (octave + perfect
  fifth); pitch classes walk the circle of fifths
  (G#→D#→A#→F→C→G→D), drifting ~2 cents sharp per step. No note-count
  or interval pattern spells anything — a single constant ratio with no
  varying parameter cannot encode a message. Local syntheses:
  `phase2/raw/desmos/` (chord-all15, chord-audible7, arpeggio-brief-
  reading WAVs + frequency CSV + analysis script).
- MP3 comparison — EXACT ww match: ww's seven tones (25.9–18,888.7 Hz)
  equal Desmos tones n = 7–13 to within 0.1 Hz. The Desmos list contains
  ww's entire tone set as its audible core, extended by 7 infrasonic
  tones below and 1 ultrasonic above — a genuine frequency-ladder
  bridge (not shared audio content; ww is a 4:13 enveloped piece, this
  is a bare list). mUr: no match — its irregular tone set shares no
  frequency with the Desmos ladder (closest pairs differ by ~327–628
  Hz).
- Hidden table (id 163, five columns, all hidden): ratios built from U,
  V, W, A, O, including one column multiplied by 299792458 (speed of
  light, m/s) — the author's own physics/scale theme. Phase-2 precision:
  column 165 = 299792458·O/3^n = c/f, i.e. the EM wavelength per tone:
  2.53×10^10 m (n = 0) down to 5,290 m (n = 14); the table as a whole is
  a frequency → period → wavelength table for the same ladder.
- Text note (id 169), glyph-framed, contains reversed AND upright copies
  of the same three links: two gyo.tc refs (2025-0726-1319-39,
  2025-0628-0459-28) to Genspark pages titled "mapping the physical
  universe with own unique time — a comprehensive scale derivation",
  and one archive.ph capture (2026-01-10) of a
  forum.fractalfuture.net uploads short-URL page. This is the strongest
  family link: the Desmos node itself carries the family's link
  machinery and reversal habit. It contains no agent/fleet/bot words.
  "Physical universe theme" rests partly on external Genspark page
  titles, not the author's own prose — the speed-of-light column is the
  author's own half.
- Adversarial catch (unexplained, not evidence): Desmos constant O ≈
  84.40602259 matches mUr's duration 84.406 s to the millisecond, and
  ww's sections are also ≈84.4 s. Noted by neither lane as a
  cross-asset link; waveforms are uncorrelated, so this is a numeric
  coincidence or shared template duration, not shared content.

## 5. TXT upload: read in full

Source: direct forum uploads short URL (route (a), first attempt, HTTP
200, 2026-10-30 03:15 GMT):
https://forum.fractalfuture.net/uploads/short-url/juCNM5RnmLal4xaBHPkP2F0QSHo.TXT
— URL form confirmed by the coordinator with an independent GET (HTTP
200, 189,356 bytes, sha256 identical to the executor's file). The live
pages link the TXT only via a Wayback-wrapped gyo.tc ref (ref
2026-0604-0033-06; JST 00:33, 2026-06-04; matches Wayback capture
2026-06-03 15:35 UTC), not directly. Response headers: `Content-Type:
text/plain` (no charset), `Content-Length: 189356`,
`X-Discourse-Route: uploads/show_short`, `Content-Disposition:
attachment` with a glyph-title filename ending in `.TXT` (filename
itself is glyph text, not reproduced here in full). Prior state:
HEAD-only 200 text/plain; public Discourse search for this short-URL ID
returned zero posts (search negative, not proof of no thread).

What it is (structure):

- Encoding: UTF-16LE with BOM (`FF FE`), CRLF line endings — not plain
  ASCII text despite the `text/plain` header. That is why a naive read
  would look like binary.
- Size: 189,356 bytes → 80,260 characters, 403 lines (length 1–2,189
  chars), 115 distinct codepoints.
- ASCII printable characters are only 2.9% of the content. The bulk is
  glyph text in the family's vocabulary: most frequent codepoints are
  U+2D54 (Tifinagh), U+274B (heavy asterisk-like), U+109FE (Meroitic),
  plus U+00B7, U+1368, U+A789, U+2E2D, U+2058, U+A539, U+283F, U+2236,
  and zero-width / wide spaces.
- The whole file is a line-level palindrome: every line equals the line
  at its mirror position (403/403 checked). The readable English content
  appears in two mirrored blocks (lines 16–41 and 363–388, in reverse
  order of each other).
- 30 lines contain ASCII letters; 32 lines are a single U+2800
  braille-blank character.

Readable language: YES — 8 distinct English-like definition sentences.
Each sentence appears twice (once per mirrored block). Spelling is
idiosyncratic throughout (quoted verbatim):

1. "REQUIRED LANGUAGE QUANTITY EQUAL SPECH APARAT SCHEME QUANTITY"
2. "GLYPH DIMENTION EQUAL CREATION INSTRUMENT DIMENTION"
3. "DRAWING INSTRUMENT QUANTITY EQUAL FINGER QUANTITY + HAIR QUANTITY"
4. "PAIRPRESENT ORGANS APEAR PAIRFOTED STEP AND PAIRORGANED DRAWING AND SYMETRYCAL GLYPHS"
5. "SCALE PROJECTING ELEMENT APEAR FUTURE APEARING KNOWLEDGE FEELABLE"
6. "OWN ESENCE UNITED WITH EACH ELEMENT OF SELFCREATED WIRTUALITY"
7. "UNIQUE LENGTH MEASURE EQUAL LIGHT DISTANSE PASED IN OWN WAWELENGTH TIME PERIOD"
8. "EACH ESENCE HAS UNIQUE WAVELENGTH EQUAL TO LENGTH OF CONGENIAL SYMETRICAL REVERBERATION"

Around them sit short reversed-looking ASCII fragments (e.g. `YTIT`,
`HTIW`, `MIT HT`, `OITA`, `IWA`, `AUQ`) — consistent with the family's
reversal habit; they read as splinters of longer reversed words, not as
standalone words. No sentence is a complete grammatical statement; the
set reads as definition-style fragments about glyphs,
wavelength/essence, and drawing instruments — the same physics/glyph
theme as the Desmos node (speed of light, ×3 tones, wavelength), not a plaintext manifest, instruction sheet, or tasking text.

Agent / swarm terms: NO. Zero occurrences (case-insensitive, full
decoded text) of: agent, fleet, bot, task, swarm. Zero URLs, zero `http`
occurrences, zero mentions of gyo, fractalfuture, neocities, hf.space,
jina, or desmos inside the file. No links or identifiers of any kind in
the content. No plaintext key, recipient, instruction, or retrieval
signal. Nothing in the TXT is tasking content.

Verdict for the swarm question: the TXT does NOT trigger any
swarm-revival condition. It strengthens the art-project reading
(glyph/wavelength/essence definition fragments, palindromic construction
matching the emoji pages) and it does NOT close the stash question in
general — the glyph bulk itself is undecoded, as before. What it closes:
the TXT is not a plaintext manifest, instruction sheet, or tasking text.

Files: verbatim bytes
`phase2/raw/txt/juCNM5RnmLal4xaBHPkP2F0QSHo.TXT` (sha256
9c0459c2a39ff397d4df59ee1b78709173db27a54e3fe99c8e78276bf0b3e3e3);
UTF-8 decoded copy
`phase2/raw/txt/juCNM5RnmLal4xaBHPkP2F0QSHo-decoded-utf8.txt`
(241,728 bytes, 80,260 characters including BOM); provenance
`phase2/raw/txt/00-PROVENANCE.md`.

## 6. Infrastructure

Files: phase-1 `raw/infra/` (note: four of these files contain token
values — see §8 C3 — and are NOT part of the phase-3 push);
phase-2 `raw/source-audit/`, `raw/wayback/`, `raw/freeimage/`.

- gyo.tc = Megalodon (Japanese on-demand web-citation archive, operator
  Affility). Refs are `ref/<YYYY>-<MMDD>-<HHMM>-<NN>/<original-URL>` — a
  JST capture timestamp plus a per-minute sequence counter, pair-keyed
  to the original URL (demonstrated: mUr ref + Wayback URL → audio;
  same ref + direct forum URL → HTML). Enumerable only within a known
  minute (~100 suffix candidates), not a single global sequence — and no
  enumeration was attempted. JST reading coherent on two independent
  ordering checks (TXT ref 2026-0604-0033-06 vs Wayback capture
  2026-06-03 15:35 UTC = 00:35 JST; mUr ref 16:18 JST vs MP3 Wayback
  capture 07:10 UTC = 16:10 JST). Hosting/registrant details rest on
  secondary listings and stay labelled as such. Resolving the two MP3
  refs returns the archived audio itself (200 audio/mpeg): the ww ref
  archived the forum file directly (2025-08-13); the mUr ref archived a
  Wayback capture of it (2026-10-19). Phase-2 correction: the live-page
  gyo ref dated Oct 17 is 2026-1017-0614-08, NOT 2026-1027-0614-08 as
  phase-1 REPORT §5 stated (§8, C2). Phase-2 wrinkle: the stored
  live-page SVG link's host segment uses U+24C4 (circled capital O) in
  place of ASCII "O" in "gyo" (see §4) — observed, mechanism unclaimed. Whether the live page as served contains this form, or the saved copy introduced it, is unproven.
- corsproxy.io is a commercial CORS proxy (`?url=<encoded-target>`):
  its server fetches the target and adds the CORS header a browser
  needs. A jina read via corsproxy is *consistent with* JavaScript
  inside a page/app fetching jina output programmatically (direct
  navigation and server fetches never trigger CORS) — but that is a
  plausible mechanism, not a deduction: the March trace is
  unreproduced, hop order is unknown (proxy-wrapped-jina vs
  proxy-wrapped-target-before-jina), other in-browser routes fit the
  same mechanism, and who ran it is entirely unestablished.
- forum.fractalfuture.net = the Fractal Future Forum (F3), a public
  Discourse forum for futurist "better future" discussion. Both MP3
  short-URLs are live (200 audio/mpeg), plus the TXT upload (200
  text/plain, now read — see §5). Public Discourse search returns zero
  posts for all three short-URL IDs — no thread can be tied to the MP3s
  from public search alone. Neighboring context, style co-location only
  (not attribution): glyph-titled topics in the same style exist on the
  forum in 2025–2026 (e.g. topic 4368, Meta, 2026-10-16, glyph-only
  single post, no uploads). No user was identified or contacted.
- Live vs archive (two time points): 2026-10-30 01:30 UTC, both live,
  not archive-only (Neocities 200, 1,079,466 bytes; HF Space 200,
  1,080,062 bytes; after stripping ~596 bytes of HF platform injection,
  visible text byte-identical with the same href set). 2026-10-30
  ~03:19–03:30 UTC, both re-fetched byte-identical (source audit).
  MP3 filenames appear in both live files (72 combined hits each) and
  zero times in the Oct 27 jina HF file. Raw-HTML presence is not
  rendered-link presence (no live render was done of the pages
  themselves). Whether the HF page was updated after Oct 27 or jina
  dropped the links cannot be distinguished from these data points —
  and that tension means the Oct 27 jina difference is not stable
  evidence of two distinct page variants.
- Live page's parent link: Ghost Archive replay
  https://ghostarchive.org/archive/H5btX resolves (coordinator passive
  GET, 2026-10-30) to the SAME Desmos calculator (lem1oik7lp) analysed
  in phase 1 — same-node confirmation only, not a new graph, not
  evidence of SVG content.

## 7. Linguist: symbols carry the payload; real scripts are ornaments

Files: phase-1 `raw/linguist/` (stored copies sanitised: one
credential-like query value in an image URL replaced with an omission
marker; sanitised hashes recorded in provenance).

- Dominant class: coloured circle/square emoji (Geometric Shapes
  Extended, plus Miscellaneous Symbols/Arrows) — green circles/squares
  broken by single white circles/squares, purple/orange/red/yellow/blue
  confined to titles and link labels. No linguistic content.
- Real-script characters, all isolated (singletons, mirrored pairs,
  title frames — never a word or sentence): 9 Bamum letters spanning
  phases B/C/D/E (Bamum Supplement), 1 Cuneiform sign, 1 Egyptian
  hieroglyph, plus Batak, Tai Tham and Manichaean punctuation.
  Phase-mixing in Bamum and cross-script salad in a single title prove
  script-as-ornament, not text in any of those languages.
- URL-decoded only: one linked PNG filename decodes to a Lisu letter, a
  Cyrillic I, and a Latin epigraphic reversed P — three isolated
  letters, no word, but a letter-level echo of the reversal habit.
- HF's glyph inventory (28 codepoints) is a strict subset of Neocities'
  (34) on raw counts; on sanitized inventories 28 ⊆ 33, HF-only: none.
  Neocities-only (sanitized): U+131EC, U+1F4A0, U+1F7E3, U+205C, U+2699.
- Naming: the attested set is now swen/news, dniferp/prefind,
  etis/site, ewitcepsrep/perspectiwe, plus three palindromic stems
  (titgtit, evihcrarchive, emitime). Paired hosts print reversed AND
  forward forms side by side (`…-o-swen-o-news-o`) — which undercuts a
  pure-concealment reading for the paired hosts. The two Oct 27 captures
  contain no reversed English word anywhere (pure o/i hostnames).
  `prefind` parses as pre- + find ("find beforehand" — a pre-search
  staging step), but it may equally be a codename chosen for clean
  reversibility. Predicted siblings (search, image, music, video
  reversed) are a watchlist only — none appears in these captures or
  the background timeline. Phase 1's "only two" claim is KILLED (see
  §8).
- Path/title structure — variant, not different: jina-reader URLs
  contain no glyphs (paths are root / `index.html`); glyph sequences
  live in titles, link labels, one image filename. Grammar at every
  scale: palette run + separator (gear, white circle/square, wide
  spaces) + mirrored/reversed run. The HF title is a single mirrored
  rainbow-plus-glyph unit; the Neocities title contains that unit twice
  inside a longer mirrored frame. MP3 link labels follow the same
  gear-separated mirror grammar. Per the linguist lane's reported observation (body-line counts downgraded to unverified — see §8, D1), bodies share 13 distinct lines and all conventions (white = break; groupings of 3, 9/10, 41); differences are variants. The "13 distinct lines shared" figure is retained only as the lane's reported observation, not as a re-verified count.
- Readable fragments: explicit none in page language (phase 1). Phase 2
  adds the TXT's 8 definition sentences (§5) as the family's first
  readable prose — definition fragments, not instructions. Only jina's
  own "Image 1:"–"Image 8:" alt labels (each + one Bamum letter);
  infrastructure names in URLs (domains, `.MP3`/`.SVG`/`.PNG`);
  random-looking file IDs. No agent/fleet/bot term, no word in any
  script, in page language.

## 8. Corrections to phase 1 (source audit + phase-2 findings)

The phase-2 source audit re-read every phase-1 lane file and raw file,
re-fetched the primary sources, and checked REPORT.md claim by claim.
Four corrections, one downgrade, one brief correction. Everything else
checked re-verified solid (all CDX arithmetic; etis first capture
2025-06-28; Oct 17 three index.html rows with exact statuses; all
Desmos numbers; live-page mirror claim exactly — HREF=196, 29 distinct
each, 596-byte injection = script + og + twitter meta, stripping
reproduces Neocities byte-for-byte; all phase-1 on-disk hashes match
their provenance records; both MP3 hashes match).

- C1. Decode-provenance caveat CLOSED. Phase-1 REPORT §2 warned that
  decode counts rested on second-hand provenance (linguist copies)
  because direct Wayback fetches returned 429. Fresh direct fetches of
  both Oct 27 captures (200, byte-identical to phase-1 infra files)
  sanitise to exactly the linguist/decode input hashes. Decode counts
  now rest on first-hand provenance. Phase-1 §8 item 6 is done for the
  core captures.
- C2. Gyo ref date typo. REPORT §5's `2026-1027-0614-08` does not exist
  anywhere; the actual live-page ref is `2026-1017-0614-08` (×8 per live
  file) — the Oct 17 ref date was conflated with its Oct 27 Wayback
  capture date. Do not quote the 1027 form.
- C3. Token-cleanliness claim FALSE for raw files. REPORT's headline
  area stated no credential-like token value appears in "this report or
  in any lane file." That holds for REPORT.md, the FINDINGS files, and
  the sanitised linguist/decode copies — but NOT for the raw files:
  token values are present in all four `raw/infra/*.html` files
  (wayback jina captures ×4 occurrences each, live pages ×5 each).
  Consequence enforced in phase 3: those four files are NOT part of the
  push, and no phase-2 file reproduces any token value (verified: every
  token occurrence in phase-2 files is the omission marker only). If
  the operator ever wants those four files in the repo, that is a
  separate secrets decision — never bypass push protection, never strip
  silently.
- C4. "56 rows per page" is the circle-row count only. True binary row
  totals are 96 (Neocities) and 112 (HF Space). Do not quote 56 as the
  page total.
- D1. DOWNGRADED to UNVERIFIED: the linguist lane's "25/24 distinct body
  lines, 13 common" — no script or dump preserves the counting method,
  and no natural reproduction from saved files yields 25/24/13. Do not
  quote those counts as verified.
- C5. Desmos tone second argument is GAIN, not duration (phase-2
  correction to the phase-1 summary and the phase-2 brief). Per Desmos's
  own Help Center Tone article (updated 2026-07-23), `tone(frequency,
  gain)` takes gain as its optional second argument; there is no
  duration parameter. So 1/27 is a very quiet gain, and the expression
  specifies no duration. The "0.556 s sequence" reading is withdrawn.
  Likewise, chord-vs-arpeggio rendering of a list frequency is NOT
  settled by the state + docs — both renderings were produced locally,
  and live Desmos playback is an open item, not a claim.
- Also corrected in passing: phase-1 REPORT §4's "SVG: Wayback 429, not
  retried" and §8 item 1 ("live-browser fetch") are superseded by the
  phase-2 recovery + render (§4). Phase-1 REPORT §8 item 3 (read the
  TXT) is closed (§5). Phase-1 REPORT §8 item 2 (freeimage render) is
  closed (§4). Phase-1 REPORT §8 item 6 (fresh Wayback re-verification)
  is done for the core captures (C1) and the SVG (recovered), and
  partially done for the census (24/26 forms; 2 forms inconclusive).

## 9. Adversarial review of the NEW claims (coordinator's pass; independent reviewer check follows in §12)

This section attacks only the claims that are new in phase 2. Phase-1
claims were adversarially reviewed in phase 1; §8 records what changed.
The independent reviewer subagent re-checked this draft and its verdicts
are folded in §12; where the reviewer killed or weakened a claim below,
the verdict line states so.

KILLED (must not ship as worded):

- "The SVG is the same Desmos graph." Overstated. What is established:
  the SVG is a Desmos export whose geometry matches the sine-star, with
  the same nine-group structure and the same glyph-vocabulary title
  frame. The SVG root title and the Desmos page title are similar, not
  byte-identical (the SVG title carries a leading white circle the
  Desmos title lacks, and the Desmos title carries zero-width
  characters). "Same artwork confirmed" ships; "same graph" does not,
  because a different revision or a sibling graph sharing the template
  is not excluded — and the export's monochrome #EEEEEE vs the state's
  green/red pairs is an unexplained difference, not a match.
- "The MP3s are not carriers." Overstated. What is established: no
  carrier evidence in the tested routes (amplitude, frame, ancillary).
  MDCT-coefficient embedding and keyed/exotic gain encodings were not
  tested. Ship only "no carrier evidence in tested routes."
- "The TXT is not a note." Overbroad. What is established: the TXT is
  not a plaintext manifest, instruction sheet, or tasking text (no
  imperatives, no recipients, no retrieval signals, no links). Whether
  it serves as the author's own note or definition sheet is unknowable
  from the file — definition fragments ARE a kind of note. Ship the
  narrow form.

WEAKENED (ship only narrowed):

- Freeimage render description: the visual description rests on the
  forwarded live-browser render, not on first-hand viewing by the
  coordinator. The coordinator verified the file bytes (format, size,
  hash) but did not view the rendered pattern itself. Ship the
  description as "live-browser render (forwarded)" evidence, not as
  coordinator-observed fact. Pixel-level content is unexamined.
- Homograph host (U+24C4): observed in the STORED live-page copy, and
  the stored link resolved to the SVG. Whether the LIVE page as served
  contains the homograph, or the saved copy introduced it (e.g. through
  an encoding step when the page was saved), is unproven. Ship only
  "stored copy carries a U+24C4 host segment; the stored link resolved."
  No mechanism claimed.
- ww §3−§1 difference "is re-render noise": the difference was
  characterized statistically (high correlation, mean ≈ 0, small std),
  not decoded as a signal. A low-amplitude structured signal could hide
  under noise statistics. Ship only "no structured second channel
  detected in the difference by the tests run."
- "Pattern handles, not identities" (freeimage metadata): the handles
  LOOK like pattern handles (0000OOOO0000, OOO), but that is an
  inference from their form, not a verified fact about their nature.
  The no-attribution rule stands regardless of what they are — the rule
  is about what we do, not what they are. Ship the rule, not the
  nature claim.
- CDX re-census "no post-Oct-27 activity": the census shows no detected
  post-Oct-27 Wayback rows in 24/26 forms. Two forms are inconclusive
  (repeated 503s), and Wayback absence is not activity absence (live
  pages were up Oct 30). Ship only "no detected post-Oct-27 Wayback
  rows in 24/26 forms; 2 forms inconclusive."

SURVIVES (as worded):

- TXT structure + sentences (byte-verified, hash-verified, independently
  re-fetched by the coordinator; sentences quoted verbatim; palindrome
  403/403 checked; except the mirrored-block ranges, corrected to 16–41 / 363–388 (see §1 of the independent review)).
- Desmos tone ladder + ww exact match (computed from state, measured
  from MP3, agreement within 0.1 Hz across two independent
  measurements; mUr non-match correctly reported alongside).
- Gain-not-duration correction (Desmos's own docs + expression form;
  the withdrawn 0.556 s reading is explicitly withdrawn, not silently
  dropped).
- SVG retrieval + reconciliation (browser/token-free failure and
  worker/stored-link success are compatible different-form results;
  the "keyed to the full signed URL" explanation is labelled a
  hypothesis-consistent reading, and the no-signed-URL rule was kept).
- SVG chain upgrade to "same artwork" (geometry + nine-group structure
  + glyph title frame + local render; same-operator explicitly withheld).
- TXT + images + tone add no agent terms (each asset's negative is
  tied to its own examination; the overall swarm verdict stays a
  negative finding, not a proof, with the four untested stash surfaces
  listed in §11).

Alternatives re-tested with phase-2 evidence:

- Encoded stash / dead-drop — NARROWED, NOT RULED OUT. Against (new):
  TXT is not a plaintext manifest/tasking text; MP3 amplitude +
  frame/ancillary routes closed for tested forms; both images retrieved
  and show art, not payloads; SVG path data shows no anomaly. For
  (remaining): TXT glyph bulk undecoded; MP3 MDCT/keyed-gain untested;
  SVG path-coordinate encoding untested; Desmos tone rendering
  (chord/arpeggio) unplayed. Ship only "no stash evidence in examined
  assets and tested routes."
- ARG / puzzle — PLAUSIBLE, UNPROVEN (unchanged). For (new): the TXT's
  definition fragments + palindromic construction fit a puzzle trail;
  the SVG now completes a visual leg of the trail. Against: still no
  puzzle prompt, progression, solution path, or solving community; the
  trail no longer breaks at the images, but it still breaks at
  undecoded content. Do not present the trail as a designed puzzle path.
- Art project (generative / sound art) — STRONGEST FIT, STRENGTHENED.
  For (new): sine-star SVG render, circular-mesh shader image, TXT
  definition fragments, exact tone ladder shared between Desmos and ww
  — a coherent multi-asset generative/physics art practice. Against
  (unchanged): no artist statement, exhibition, or attribution found;
  archive-wrapping chains are heavier machinery than art normally needs
  (though archiving one's own work through gyo/Wayback is also
  ordinary). Still an inference, not an identification.
- Test data / scaffolding — WEAK, NOT EXCLUDED (unchanged). A rig has
  no reason to craft a sine-star with physics scaling, a ×3 tone-stack
  with reprise structure, palindromic naming across eight hosts over
  years, and definition fragments about essence and wavelength.
- Bot-generated filler / spam — WEAK (unchanged). Spam wants
  discoverability, monetisation, or SEO text; these pages are
  unsearchable by design, carry no commercial links, and the Desmos
  node + SVG + shader image are composed artwork.
- Agent / swarm infrastructure — STILL REJECTED, with explicit revival
  conditions (see §10). Phase 2 added four newly examined assets and
  none produced an agent term, a beacon pattern, a tool/API trace, or a
  tasking payload.

## 10. Swarm-revival conditions (none present)

Agent/fleet/bot/task terms in any unexamined asset (MP3 transcript —
none exists; TXT glyph bulk — undecoded; SVG path data — untested for
encoding; Desmos playback rendering — unplayed); a demonstrated beacon
pattern (same payload across unrelated agent surfaces, or timing tied
to known agent incidents); tool/API traces in page sources or forum
posts; linkage from these hosts/IDs to a known agent incident; or a
decoded payload with tasking content. Until one appears, "not a swarm
lead" stands as a negative finding.

## 11. What remains open (honest gaps, in priority order)

1. MP3 MDCT-coefficient steganalysis + keyed/exotic gain encodings —
   the two untested MP3 stash routes. Closes the MP3 side properly.
2. TXT glyph bulk decode — the 97%+ of TXT characters that are glyphs,
   not the 8 readable sentences. Cycle-order / bitmap / keyed readings
   from §2 apply here too.
3. SVG path-coordinate encoding test — structural analysis only so far;
   coordinate sequences not tested as data.
4. Live Desmos playback check — chord vs. arpeggio rendering of the
   list frequency, and out-of-range tone handling. Needs live-browser
   delegation (this coordinator cannot do it).
5. CDX re-attempt of the 2 failed forms (dnif-jina-http,
   neo-jina-https) once the Wayback backend clears — completes 26/26
   post-Oct-27 coverage.
6. Recover the March 25, 2026 corsproxy trace from the prior corpus
   snapshot (exact corsproxy URL shape) — CDX queries alone cannot
   reproduce it.
7. Jina-independent sibling discovery — a bounded method for
   `static.hf.space` hosts sharing the stem (e.g. HF API listing) that
   does not rely on jina reads; the census remains a lower bound.
8. Same-operator question — shared artwork across nodes does not prove
   one author; no attribution is pursued (out of scope by hunt rules).
9. Freeimage pixel-level analysis — the 62 MB WEBP was verified by
   format/size/hash only; its pixels were never analysed locally.
10. ww served-capture identity — requested capture 20261020014219 is
    not an exact CDX timestamp (nearest 20261020014241/42, warc/revisit
    to a 2025 original); which capture Wayback actually served is
    unconfirmed, though the file parses cleanly.

## 12. Phase-3 record: adversarial check, Factum ingest, push

Independent adversarial review (workspace
`phase2/adversarial-review-FINDINGS.md`, 2026-10-30): the reviewer
checked the draft's new claims first-hand against the evidence files.
It killed 3 items, weakened 8, and added 1 clarification and 3 minors.
Kills: (1) the SVG "25 `<g>` groups" count — recomputed 135 opening
`<g>` tags; (2) the TXT mirrored-block range "361–386" — the true
mirror of lines 16–41 is lines 363–388; (3) the §5 wording "not a
note", which contradicted §9's own kill (definition fragments ARE a
kind of note) — narrowed in both §5 spots to "not a plaintext
manifest, instruction sheet, or tasking text". Weakens (all applied):
same-glyph-title wording, freeimage forwarded-render labelling,
"pattern handles" assertion removed (no-attribution rule kept),
homograph saved-copy-origin caveat added to §4 and §6, ww §3−§1
difference narrowed to "no structured second channel detected by the
tests run", "MP3s not carriers" narrowed to "no carrier evidence in
the tested routes", mUr closest-pair range corrected to ~327–628 Hz,
evidence-map "(same graph)" corrected to "(same calculator,
lem1oik7lp — same-node confirmation only)". The reviewer verified
29 numeric spot-checks (26 match, 3 mismatch — the 3 kills above) and
confirmed C1/C2/C3/C4/D1/C5. One reviewer wording was NOT applied
verbatim: its evidence-map item 13 described the 503 directory as
"the 2 persistently failed forms plus 2 forms that succeeded"; the
directory actually holds 4 worker-run 503 pages, of which only
neo-jina-https stayed failed in the completion pass (dnif-jina-http
failed in the completion pass; its 503 page is the working cdx file).
The report carries the corrected accounting. The reviewer could not
re-verify the Desmos Help Center doc text (browsing barred by its
task), the freeimage/SVG-render visual descriptions (bytes verified,
patterns not viewed), or the homograph origin (live page vs saved
copy) — those stand as attributed or qualified claims, as labelled.

Factum ingest (lane `2026-10-30-o-pattern-phase2`, lane id
`lane_2483c3b5db0d471db67f6654d61f18c2`, actor
`agent:o-pattern-phase2`, all records tagged
`{"lane": "2026-10-30-o-pattern-phase2"}`): 5 batches, 44 records
total. File-backed captures (12 records): TXT batch
`089033e65f174697a065728771dcb718`, ww batch
`5f754586ab4b457f9c6e545f76ca58e2`, mUr batch
`fc87df125ee4488a913909c9c897f595`, WEBP batch
`7b347f8fce8f4be683e9fbc3bd36e788`. IOC + claims bundle (32 records:
3 sources, 11 `url` observables, 14 `infra.ioc` observations, 4
claims): batch `53e548eedcf04f4db36492a827b6f14f`. Corpus count before ingest: 208,701 records (128 lanes, 0 pending,
HEAD 8fb66e74, index not stale). Corpus count after export: 208,745
records (0 pending) — delta +44, exactly this job's 44 records (12
captures + 32 bundle), all 44 record IDs verified present in the
corpus and all 5 batch directories exported with correct line counts
(3+3+3+3+32). An intermediate reading of 208,725 taken after the
captures but before the bundle exceeded the expected 208,713 by 12;
the endpoints reconcile exactly, so that figure is treated as a
transient shared-checkout count, not a gap in this job (disclosed
here, not hidden). The push-block
judgment from §6 stands: the Oct 26 urlscan-crawl corpus-count drift
(gap of 8) is scoped to that fleet's own commit, not a general push
freeze; this push introduces no unexplained move (before/after counts
reconcile exactly to this job's 44 new records).

Push: commit [TO FILL] on main, pushed [TO FILL UTC]. Remote HEAD
verification: [TO FILL — remote HEAD match yes/no, blob SHA match
yes/no, via the API]. Commit set (explicit pathspecs only): the lane
directory, this job's 5 exported batch directories, and the
FULL-REPORT.md copy in the lane. No other paths.

Items left out of the push, with reasons:

- The four phase-1 raw infra files (`raw/infra/*.html`): they contain
  credential-like token values (see §8, C3). Excluded by the token
  rule. If the operator ever wants them in the repo, that is a
  separate secrets decision — never a silent strip or bypass.
- Desmos state JSON and SVG bytes: captured as lane raw files, not as
  Factum capture records (state extracted from a WARC, not downloaded
  from a URL; SVG original URL token-bearing and forbidden). Lane
  raw files + descriptions instead.
- Sibling workers' pending batches and staged files: export covers
  all pending batches, but only this job's batch directories are
  committed. Sibling work stays untouched for its owners.
- The uncommitted Oct 27 IPv6 schema-pack files and the Oct 26
  urlscan-crawl gap: not this job's, not swept in, not resolved here.

## Evidence map

Phase-1 report (superseded, kept for history):
`~/workspace/o-pattern-followup/REPORT.md` + lane files
`cdx-`, `decode-`, `mp3-`, `images-`, `infra-`, `linguist-`,
`adversarial-FINDINGS.md`, raw evidence + provenance under `raw/<lane>/`
(includes `raw/mp3/` both MP3s + ffprobe JSON + spectrogram/waveform
PNGs; `raw/images/` Desmos state JSON + Ghost Archive wrapper + WARC;
`raw/cdx/` CDX responses + query logs + analysis scripts; `raw/decode/`
sanitised captures + sequences + inventories + 860 decode attempts;
`raw/linguist/` captures + glyph inventory + analysis script).
WARNING: four phase-1 files under `raw/infra/` contain token values
(`wayback-jina-neocities-20261027.html`, `wayback-jina-hfspace-20261027.html`,
`live-neocities-20261030.html`, `live-hfspace-20261030.html`) — see §8
C3. They are NOT part of the phase-3 push and must not be copied into
any pushed path.

Phase-2 findings (all under `~/workspace/o-pattern-followup/phase2/`):
- `txt-FINDINGS.md` + `raw/txt/` (verbatim TXT bytes, UTF-8 decoded
  copy, provenance).
- `mp3-decode-FINDINGS.md` + `raw/mp3decode/` (analysis scripts,
  frame/ancillary JSONs, `loop_correction.json`, envelope NPZs + 100 ms
  CSVs, run log; intermediate WAVs deleted as re-derivable).
- `desmos-tone-FINDINGS.md` + `raw/desmos/` (analysis script,
  frequency CSV, 3 synthesized WAVs, provenance).
- `source-audit-FINDINGS.md` + `raw/source-audit/` (fresh Oct 27 capture
  + live-page fetches, token-sanitised; CDX spot-check responses;
  provenance).
- `freeimage-render-RECORD.md` + `raw/freeimage/` (WEBP bytes +
  provenance).
- `svg-render-RECORD.md` (browser failure record) +
  `svg-analysis-FINDINGS.md` + `raw/wayback/` (SVG bytes, local render
  PNG, fetch script, freeimage viewer bytes, CDX responses + logs +
  scripts).
- `wayback-recensus-FINDINGS.md` + `raw/wayback/cdx/` (26-query
  responses; worker-run 503 pages preserved in
  `raw/wayback/cdx/failed-503-worker-run/` (4 files from the worker run; of these, only neo-jina-https remained failed in the completion pass — the other 3 succeeded as empty; the second persistently failed form, dnif-jina-http, failed in the completion pass and its 503 page is the working cdx file)).
- `STATUS.md` (phase-2 working note, not a deliverable).

Primary source URLs (all token-free except where noted as withheld):
- Live pages: https://ooooooooooooooooooooooooooo.neocities.org/ and
  https://ooooiiiiiiiioooo-ooooiiiiiiiioooo.static.hf.space/index.html
- Oct 27 Wayback jina captures:
  https://web.archive.org/web/20261027155724id_/http://R.JINA.AI/https://ooooooooooooooooooooooooooo.neocities.org
  and
  https://web.archive.org/web/20261027153241id_/https://r.jina.ai/https://ooooiiiiiiiioooo-ooooiiiiiiiioooo.static.hf.space/index.html
- TXT: https://forum.fractalfuture.net/uploads/short-url/juCNM5RnmLal4xaBHPkP2F0QSHo.TXT
  (gyo.tc ref 2026-0604-0033-06).
- ww MP3: https://forum.fractalfuture.net/uploads/short-url/wwM5xXlIc1QTcAH3uhXuMYyJauL.MP3
  (Wayback 20261020014219 retrieval; gyo.tc ref 2025-0813-1654-16).
- mUr MP3: https://forum.fractalfuture.net/uploads/short-url/mUr2xClu6x7OUSFz70Ylk6U5GjX.MP3
  (Wayback 20261019071014 retrieval; gyo.tc ref 2026-1019-1618-09).
- Desmos: Ghost Archive capture 20260519232539 of
  desmos.com/calculator/lem1oik7lp; live-page parent link
  https://ghostarchive.org/archive/H5btX (same calculator, lem1oik7lp — same-node confirmation only).
- SVG: Wayback capture 20261027145327, via gyo.tc ref 2026-1027-2355-45
  through the exact stored live-page link (underlying token-bearing URL
  withheld everywhere by rule; see §4 for the reconciliation).
- freeimage: page
  https://web.archive.org/web/20230216011340/https://freeimage.host/i/HGHQml9
  ; direct file
  https://web.archive.org/web/20230216011350im_/https://iili.io/HGHQml9.webp
  ; original https://iili.io/HGHQml9.webp.
- CDX: http://web.archive.org/cdx/search/cdx (port 80; bare prefix for
  matchType=prefix; from=20261028 for the re-census).

Gaps that are evidence of absence vs. absence of evidence, kept
distinct: decode failure is structural (palindromes); MP3 amplitude +
frame/ancillary negatives are tested negatives for those routes only;
image/TXT content is retrieved (no longer unretrieved); swarm rejection
is a negative finding, not a proof; the four §11 items 1–4 are
absence of evidence, not evidence of absence.
