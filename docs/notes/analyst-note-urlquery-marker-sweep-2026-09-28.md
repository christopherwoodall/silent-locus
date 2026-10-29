# Analyst note: urlquery marker sweep for ExploitGym incident markers (Lead 4/6)

Date: 2026-09-28. Read-only sweep of the urlquery.net public report corpus.
Question: did any third-party scans catch ExploitGym incident traffic in the
wild? Markers from R0049672 and the ExploitGym note: `exploitgym`, `catflag`,
`restart_server`, `submit-vul`, `m47push2`, `m47bmbox`, `cybergym/arvo`.

## Verdict (cream first)

**No.** Nothing in urlquery's corpus corroborates R0049672's Artifactory
payload as live incident traffic:

- **Zero scanned URLs** anywhere in the corpus contain `exploitgym`,
  `catflag`, `restart_server`, `submit-vul`, or `m47bmbox`
  (`http.url.addr:*<marker>*` all return 0 hits; `http.url.addr:*exploitgym*`
  = 0).
- **Agent IDs `m47push2` / `m47bmbox`: zero hits in any form**, content or
  URL, scoped or unscoped. The operator-side mailbox namespace has no public
  scan footprint at all.
- **`cybergym/arvo`: zero hits.** The only `cybergym`-in-URL hits (4 reports)
  are benign: two SnackOnAI newsletter clickthroughs (May 16, cybergym.io and
  the public GitHub repo), a cybersecurity forum homepage, and one
  curiosity probe (below).
- **`submit-vul`: zero hits** once query syntax is correct (the 12 v1 hits
  were a hyphen-tokenization artifact — see caveats).
- The 134 July `exploitgym` hits are **100% Appwrite console/Vibes preview
  deployments** (sign-in / password-protected pages, scanned July 27–31);
  none is ExploitGym infrastructure, and the match string is not present in
  any public report field, so the match location is unverifiable.

## The one interesting wild artifact (not corroboration)

- https://urlquery.net/report/c1140981-53c9-4e64-8771-c3bbd0027e5c —
  scanned 2026-09-25, submitted URL
  `openai.com/internal/benchmark/dhem62h58ao2619dmdnbwu2938647dmmaoqofjhr3816659bgfkk26/cybergym/madeyoulook/pug`
  (Cloudflare IP, **404**). An anonymous submitter probed openai.com for a
  fabricated "internal benchmark" path with a `cybergym` segment and a
  taunting tail (`madeyoulook/pug`). Post-disclosure (Aug 26 blog) curiosity
  probe — someone checking whether OpenAI hosts internal cybergym endpoints.
  It is a probe OF the incident's public surface, not incident traffic itself.

## Full query list (reproducible)

Sweep v1 (unquoted, implicit AND — later found to mis-parse hyphenated terms
combined with `date:[...]`):
1. `exploitgym date:[2026-07-01 TO 2026-07-31]` → 134 hits
2. `exploitgym` → 967
3. `catflag date:[2026-07-01 TO 2026-07-31]` → 1
4. `catflag` → 11
5. `restart_server date:[2026-07-01 TO 2026-07-31]` → 3
6. `restart_server` → 19
7. `submit-vul date:[2026-07-01 TO 2026-07-31]` → 12 (artifact, discarded)
8. `submit-vul` → 0
9. `m47push2` → 0 ; 10. `m47push2 date:[...]` → 0
11. `m47bmbox` → 0 ; 12. `m47bmbox date:[...]` → 0
13. `cybergym/arvo date:[...]` → 0 ; 14. `cybergym/arvo` → 0
15. `cybergym date:[...]` → 1

Sweep v2 (quoted exact phrases + explicit AND, per urlquery.net/help/search;
plus HTTP-traffic URL lens with wildcards):
16. `"exploitgym" AND date:[2026-07-01 TO 2026-07-31]` → 134
17. `"exploitgym"` → 967
18. `"catflag" AND date:[...]` → 1 ; 19. `"catflag"` → 11
20. `"restart_server" AND date:[...]` → 3 ; 21. `"restart_server"` → 19
22. `"submit-vul" AND date:[...]` → 0 ; 23. `"submit-vul"` → 0
24. `"m47push2"` → 0 ; 25. `"m47bmbox"` → 0 ; 26. `"m47bmbox/"` → 0
27. `"cybergym/arvo" AND date:[...]` → 0 ; 28. `"cybergym/arvo"` → 0
29. `"cybergym" AND date:[...]` → 1
30. `http.url.addr:*restart_server*` → 0
31. `http.url.addr:*submit-vul*` → 0
32. `http.url.addr:*catflag*` → 0
33. `http.url.addr:*m47bmbox*` → 0
34. `http.url.addr:*cybergym*` → 4

Sweep v3: 35. `http.url.addr:*exploitgym*` → 0.

Pagination: 36–39. offsets 30/60/90/120 on query 16 (134/134 July hits
enumerated; all appwrite.network).

## Evidence grades

- **context-only** (1): the openai.com probe — marker verifiably in the
  scanned URL, but it is a fabricated probe, not incident traffic.
- **low** (2): `catflag` made-in-china EDM-tracker report (2026-07-21);
  `cybergym` benchgecko benchmark-site report (2026-07-04). Both are
  search-index-only matches; the marker string is absent from every field of
  the public report body (verified by full-body fetch + case-insensitive
  walk), so the match location cannot be confirmed. No link to ExploitGym.
- **benign** (rest): `restart_server` hits are generic admin/ops UI text on
  Cronicle/Splunk/DhiWise/Webdock/rocket.new/FPT pages (URL lens is clean, so
  none is a scan of an ExploitGym `/restart_server` controller); the other
  `cybergym`-URL hits are newsletter traffic and a forum homepage.
- **absent**: `m47push2`, `m47bmbox`, `submit-vul`, `cybergym/arvo` — no
  footprint anywhere in the corpus.

Per-report detail lives in `data/urlquery-marker-sweep/hits.jsonl`.

## Caveats

1. **Query-syntax caveat (caught mid-sweep):** bare `submit-vul date:[...]`
   returned 12 hits while `"submit-vul"` (quoted) and
   `"submit-vul" AND date:[...]` return 0. The unquoted hyphenated term
   tokenizes into `submit` AND/OR `vul` and the date-filtered parse fell back
   to loose token matching (car-dealer contact-form pages). The 12 v1 hits
   are discarded as parser artifacts; v2 quoted queries are authoritative.
2. **Match-location caveat:** urlquery's plain-text search indexes captured
   HTML/JS text that the public report API does not always return. Two
   candidate hits (catflag, cybergym/benchgecko) and all 134 Appwrite
   `exploitgym` hits match in the index but contain zero occurrences of the
   marker in any public-API field. The web report page likewise exposes no
   match context. These are graded low, not verified.
3. Scope: read-only; searches only, 3 full report bodies fetched; no
   submissions. Respected rate limits (2s pacing between queries).

## Dedupe vs R0049672

R0049672 is a SwarmTraces corpus record (Artifactory message-board payload),
not a urlquery report — no urlquery report corresponds to it. Nothing in this
sweep duplicates it; the sweep finds no independent wild corroboration of it.

## Files

- `data/urlquery-marker-sweep/` — PROVENANCE.md, SHA256SUMS, progress.log,
  hits.jsonl, sweep_summary*.json, run_sweep*.py, raw/ (39 cached API
  responses).
