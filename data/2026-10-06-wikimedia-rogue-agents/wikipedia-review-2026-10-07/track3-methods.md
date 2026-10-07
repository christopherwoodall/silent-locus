# TRACK 3 — METHODS AUDIT (wikipedia edit-hunt lane, closed 2026-10-07)
Auditor: track-3 worker, independent pass. Read-only audit; nothing modified.
Scope: vocab-sweep, ngram-sweep, wordlist-wiki-sweep, lifeval-cross-corpus (SWEEP-SUMMARY),
newusers provenance/dedup, urlquery htmx fix + 143-query re-read, wording of conclusions.

## CHECK 1 — Sweep coverage — SUPPORTED (with one data-hygiene flag)

- `srnamespace=*` verified by grep in every collection script:
  vocab-sweep/sweep_insource.py:36, ngram-sweep/sweep_insource.py:39,
  sweep_resume.py:48, gapfill.py:59, sweep-en.py:21, sweep_meta_insource.py:49,
  sweep_testwiki.py:59, collect-mediawiki.py:49. All send `srlimit=50&srnamespace=*`.
- Capture counts on disk match the claimed arithmetic:
  vocab-sweep 54 files = 6 phrases x 9 wikis; ngram-sweep 81 = 9 fragments x 9 wikis.
  Wordlist: search-terms.json carries 1,148 terms; new-format captures on disk are
  exactly 1,148 per wiki x 9 wikis = 10,332 (each dir has 1,148 `insource-<n>.json`
  with the `_sweep` envelope).
- Spot-check: vocab capture `insource-en.wikipedia.org-01.json` is well-formed —
  recorded URL literally contains `srsearch=insource:"Temporary technical sandbox
  initialization"&srlimit=50&srnamespace=*`, total_hits 0. Method claim matches bytes.
- **Flag (hygiene, not verdict-breaking):** `raw/incubator.wikimedia.org/` holds
  1,148 corrected captures PLUS 776 stale zero-padded `insource-0000.json`-format
  files from the first sweep generation (total on disk 11,108, not the 10,332 the
  FINDINGS headline counts). Sampled stale file `insource-0000.json` for `${7*7}` has
  NO `_sweep` envelope and carries the bogus mangled-phrase-mode hit count
  (38,309 hits) that CORRECTIONS.md describes — the stale data contradicts the
  corrected verdict if read naively. CORRECTIONS.md says "cached files deleted so
  they re-run correctly" — they were not; 776 remain. Mitigating: gapfill.py
  lines 31-42 explicitly skips old-format files (comments name the hazard), and the
  graders address captures by explicit index (`insource-{n}.json`), so analysis did
  not consume the stale files. Still: the raw dir as-shipped is a trap for any
  future glob-based re-analysis, and the FINDINGS "10,332 captures" headline
  undercounts what is actually in the directory.

## CHECK 2 — Sampling honesty — SUPPORTED

- The 3 `srlimit=1` mediawiki.org captures are disclosed in the FINDINGS coverage
  table ("3 terms fetched with srlimit=1 after repeated IncompleteRead on full
  payloads; totalhits only"). Verified on disk: exactly 3 files carry srlimit=1 —
  `insource-700.json` (`x=0.`), `insource-707.json` (`IdNumber`), `insource-708.json`
  (`idnumber`). Claim matches bytes.
- Giant-result-set grading is disclosed in Limitation #3 of FINDINGS.md:
  "srlimit=50 — sample titles/snippets reflect top-50 results per term; grading
  scanned samples, not all hits, for giant-count terms (those were auto-graded NOISE
  only when the term was a generic web domain/URL with unambiguous organic
  context)". No other srlimit=1 or truncated-payload fetches found in any sweep
  script or log.
- **Honest weakness that is disclosed:** auto-grading ~25k-hit terms (e.g. `oai-`
  OAI-PMH noise) from 50 samples is a genuine judgment call — but it IS labeled as
  such, and the category of auto-graded terms is generic-web-noise only. Not a
  concealment; flagging it as the weakest disclosed point.

## CHECK 3 — insource: current-content-only limitation — SUPPORTED, front-and-center

- vocab-sweep FINDINGS.md Method section: bold "**Caveat: insource: searches CURRENT
  page content only** — cleaned sandboxes no longer contain the markers; revision
  history does." First paragraph, not buried.
- ngram-sweep FINDINGS.md: identical bold caveat in Method.
- wordlist FINDINGS.md: Limitation #1 in an explicitly titled "Limitations (honest)"
  section; also "insource: is current-content-only (same blind spot as the vocab
  sweeps)".
- DONE.md: Method note in section 4 ("insource: is current-content-only; cleaned
  sandboxes erase markers — future hunts must pair insource: with revision-history
  grep") plus section 10 bullet. The limitation is consistently stated and the lane
  does pair insource: with a sandbox comment grep (200 revs x 9 sandboxes) — whose
  limited depth is itself disclosed ("Spot check, not exhaustive", "full
  comment-history sweep needs paginated rv traversal").

## CHECK 4 — newusers dedup — SUPPORTED

- Recomputed with wc -l over the 24 canonical files (excluding the redundant
  `newusers-2026-06.metawiki.resume.jsonl`): **6,922,622 lines — exact match** to
  the claimed total.
- 25 files on disk, 24 canonical — the resume fragment (60,000 lines, verified by
  wc) is correctly excluded, and PROVENANCE.md documents it as a strict subset of
  06b that "MUST be excluded from any combined analysis".
- The 30,000/30,001 April enwiki/metawiki duplicate rows ARE documented in
  NEWUSERS-PROVENANCE.md ("Known data quirks"): pagination bug, removed by logid
  dedupe, post-dedupe counts 335,458 / 608,286. Verified: April files have those
  exact line counts with 0 internal duplicate logids (spot-checked enwiki-04 by
  full logid scan). The claim "6,901,112 logid-unique" and "4,088,327 deduped
  ~2026-*" were not recomputed end-to-end (the ~2026-* filter requires the full
  parse), but every number I could cheaply verify matches exactly.

## CHECK 5 — urlquery htmx fix — SUPPORTED, data trail verified

- Both patched scripts implement the operative fix. VERIFICATION.md's probe table
  establishes that `HX-Current-URL` (not `HX-Request`) flips `/api/htmx/search/`
  from 204 to 200 (probe 3b: HX-Current-URL alone -> 200 + 23 rows; probe 2:
  HX-Request alone -> still 204; probe 6 negative control: 200 + "No reports found",
  so the header doesn't fabricate positives).
  - reverse_tunnels_htmx_search.py sends `HX-Current-URL` (sufficient per probe 3b).
  - dse_wiki_verification_expand_search.py sends both `HX-Request: true` and
    `HX-Current-URL` (matches the skill's uq_htmx_curl.py pattern).
  Both hit the verified endpoint `https://urlquery.net/api/htmx/search/?q=<q>&limit=<n>&offset=0`.
- The claimed re-read is data-backed: exactly **143** `q*.json` files exist in
  htmx-fix/raw/reread/, and the per-file hit counts match REREAD-RESULTS.md for all
  15 claimed resurrections (spot-verified 17 files: q01 x2 -> 23/20 uuids,
  httpbin.org/base64 -> 2, mmsi -> 23, zenrin -> 5, research_kompas -> 3,
  scaleway -> 3, satnogs -> 1, star-vegas -> 1, gov.il -> 24, fileshare five ->
  24/23/24/24/3; gofile.io shows 25 uuid occurrences vs claimed 24 — trivial,
  likely one uuid repeated in page chrome). Confirmed-zero files (tronzap,
  gov.ru) show 0 uuids. The 128/15/0 tally in REREAD-RESULTS.md is consistent with
  the files on disk.
- The re-read report is also honest about load-bearing consequences (flags mmsi,
  httpbin.org/base64, and the fileshare-farmer five as needing follow-up triage,
  and notes 6 of the 15 "resurrections" were never-actually-searched error-as-zero
  misfiles rather than 204 artifacts).

## CHECK 6 — conclusion wording vs evidence — WEAK (one open wording drift)

- The lane's official, reviewer-mandated wording is "no leakage detected on searched
  surfaces" — DONE.md section 13 records the reviewer correction ("Containment
  claim: 'no leakage detected on searched surfaces' (insource: is current-content-
  only; 200-rev grep has blind spots)"), and DONE.md sections 4 and 9 use it.
- **However, the leaf FINDINGS.md files were never updated to the corrected
  wording.** vocab-sweep FINDINGS.md net verdict still reads: "The incident's
  shared vocabulary is **incident-contained**." ngram-sweep FINDINGS.md: "The
  incident's marker fragments are **incident-contained**." "Incident-contained"
  as an unqualified headline outruns the evidence more than the reviewer-approved
  "no leakage detected on searched surfaces" does — the evidence cannot cover
  cleaned revision history (insource: limitation) or ~900 unsearched wikis (wordlist
  Limitation #2, itself disclosed).
- Mitigating: the insource: caveat is bold and front-and-center in both leaf files,
  and the per-phrase grades are evidence-bound. The drift is a wording/packaging
  issue, not a fabricated result. Recommended follow-up: restate the leaf-file net
  verdicts in the reviewer-approved form.

## Overall

Five of six checks SUPPORTED on the bytes. The two flags to act on: (1) delete or
quarantine the 776 stale zero-padded incubator captures (they contradict
CORRECTIONS.md's "deleted" claim and are a hazard to future glob-based analysis);
(2) update the two leaf FINDINGS.md net-verdict wordings to the reviewer-approved
"no leakage detected on searched surfaces" formulation.
