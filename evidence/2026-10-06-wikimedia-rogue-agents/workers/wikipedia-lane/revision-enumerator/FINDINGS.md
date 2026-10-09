# revision-enumerator FINDINGS — Wikipedia edit-hunt lane
Branch: wikipedia-edit-hunt-2026-10-06. Worker: revision-enumerator. Date: 2026-10-06.

## User question: "Can you search by IP for these edits?"

**Short answer: No — not via any public source, and this is by design since the temporary-account rollout. [OBSERVED]**

Details:
1. Wikimedia Foundation's temporary-account system replaced public display of IP addresses for logged-out editors with pseudonymous identifiers of the form `~2026-XXXXX-XX` (e.g. the operator account `~2026-36867-71` and the sandbox account `~2026-28355-02` both appear in this very evidence set). [OBSERVED — first sandbox revision already returned `user: "~2026-28355-02", "temp": true`]
2. The MediaWiki revisions API (`action=query&prop=revisions`) exposes `user` (the temp-account name), timestamp, comment, tags, flags, and content — but no IP field for temporary accounts. The IP of a temp-account editor is available only via CheckUser, a privileged tool restricted to functionaries with community/WMF approval; its results are never published in the API or dumps. [OBSERVED — no `ip`/`ipaddr` field appears in the public revisions response schema; CheckUser privilege is documented policy]
3. What IS public and stable for clustering: the temp-account name itself is a stable identifier across all revisions made by that logged-out session/device. In this lane the `user` column of revisions.tsv is that identifier and can be clustered on directly. [OBSERVED]
4. IP-adjacent public traces that remain legal/passive: revision timestamps (bursts), edit comments, tags (`mw-...` etc.), and content fingerprints — all captured in revisions.tsv. None of these yield an IP. [OBSERVED]

Bottom line: to get IPs for these edits you would need CheckUser access (privileged, not public). The temp-account name is the public replacement key — use it.

## Sweep status (updated 2026-10-06 18:47Z)

- CSV parsed: 54 (wiki, oldid) pairs across 9 wikis (en 11, test 13, test2 4, mediawiki 4, commons 6, simple 1, incubator 8, meta 6, bg 1). [OBSERVED]
- Batch revisions queries (metadata + full content): COMPLETE, all HTTP 200, 9/9 wikis, paced 6s. Raw JSON: wikipedia-lane/raw/<host>_revisions.json. Log: wikipedia-lane/collection.log. [OBSERVED]
- Resolution: 49/54 resolved. 5/54 MISSING (see table). [OBSERVED]
- Compare-API diffs: COLLECTING (paced 6s) → wikipedia-lane/diffs/<host>_<oldid>.txt.
- revisions.tsv: BUILT (54 rows incl. 5 missing rows with empty fields). wikipedia-lane/revisions.tsv.

## Resolution failures (verify, don't assume)

| wiki | oldid | symptom | verbatim API/HTTP |
|------|-------|---------|-------------------|
| meta.wikimedia.org | 30732691 | absent | batch JSON `query.badrevids["30732691"]`: `{"revid": 30732691, "missing": true}`; HTTP 200 [OBSERVED] |
| meta.wikimedia.org | 30732696 | absent | `{"revid": 30732696, "missing": true}`; HTTP 200 [OBSERVED] |
| meta.wikimedia.org | 30732698 | absent | `{"revid": 30732698, "missing": true}`; HTTP 200 [OBSERVED] |
| meta.wikimedia.org | 30732699 | absent | `{"revid": 30732699, "missing": true}`; HTTP 200 [OBSERVED] |
| meta.wikimedia.org | 30732700 | absent | `{"revid": 30732700, "missing": true}`; HTTP 200 [OBSERVED] |

All five are the Web2Cit config pages — CONFIRMS the osint-scribe precedent: WMF's most serious evidence links resolve to nothing. [OBSERVED]. Note one partial recovery: the user-temp sandbox page `User:~2026-36867-71/Web2Cit/data/com/arcgis/geocode/templates-temp-5123` (oldid 30732691) is missing, but the same account `~2026-36867-71` has a RESOLVED edit on incubator Incubator:Sandbox (7226111, 2026-06-25T20:21:29Z, comment 'Temporary technical sandbox initialization'). [OBSERVED — same temp-account name, stable identifier]

## What the 49 resolved edits show [OBSERVED throughout]

All 49 are sandbox-only edits (Wikipedia:Sandbox / User sandboxes / Project:Sandbox / Commons:Sandbox / Incubator:Sandbox / bg Уикипедия:Пясъчник) — no article-space edits. Every edit is by a `~2026-XXXXX-XX` temp account; nearly all carry `mw-reverted`/`mw-manual-revert` tags (reverted by anti-vandalism or manual cleanup).

Temp-account clusters (the public replacement for IP clustering — see IP question above):
- `~2026-28355-02` — 19 revisions, 2026-05-10, across en/test/test2/mediawiki sandboxes. Link-seeding tests: `https://px.hagstofa.is/pxen/...` (Statistics Iceland data link), `https://en.wikipedia.org/wiki/User:...`, Bulgarian NSI links. Comments: 'test', 'sandbox test', 'test link'. [OBSERVED]
- `~2026-31087-50` — 4 revisions, 2026-05-25, test.wikipedia Sandbox: external-link tests + sandbox clears ('clear sandbox' / mw-manual-revert). [OBSERVED]
- `~2026-28986-96 / ~2026-29018-32 / ~2026-29065-25 / ~2026-28987-61` — 2026-05-13, commons: OCR link tests (`api.ocr.space`, `ocr.space/ocrapi`), weather-OCR probe text ("TEST weather OCR maximum temperature Memphis 61.8 Nov 13 1890"). [OBSERVED]
- 2026-05-27 scattered one-offs on en/test/test2/simple/bg sandboxes — same link-test shape (nsi.bg infostat link, `site-test.nsi.bg`). [OBSERVED]
- 2026-06-18: `~2026-35379-90` (testwiki, 'Sandbox link test', marker `<!-- AIHW link-seeding test; temporary -->` + `[https://example.com AIHW test link]`); `~2026-35737-64` (commons, `[https://www.sec.gov/files//county.json SEC county data] test li...` — SEC county.json link). [OBSERVED]
- 2026-06-25 burst, 20:14:13–20:21:29Z (~7 min), incubator + meta: EIGHT distinct temp accounts (36686-00, 36781-18, 36722-50, 36920-78, 36837-69, 36803-16, 36724-00, 36867-71) each making one edit with IDENTICAL content (Italian: "Rimozione di contenuto di prova trasferito altrove" + Mari Merenda biography stub) and comment 'Temporary technical sandbox initialization' / 'temp' / 't'. Two carry the marker `<!-- Lifeval temporary technical sandbox initialization -->` (commons 1238390511) / `<!-- Lifeval API temp-account test -->` (meta 30732655). [OBSERVED]

Eval-family markers (task-identifier grammars, NEW for the census):
- `AIHW` — one occurrence, 2026-06-18 testwiki sandbox. INFERENCE: eval/task-family marker (likely task-set initials).
- `Lifeval` — two occurrences, 2026-06-25 (commons + meta sandboxes). INFERENCE: eval/task-family marker.
- `Test from WikiClicknbrowsebrary` / `I wato twey` / `WiuLibrary` / `Fred The Cat` (test2wiki, May 10) — typo-injected scaffold text; INFERENCE: harness-generated test content, not hand-typed.
- Cross-wiki link-test cadence: px.hagstofa.is (Iceland), nsi.bg / site-test.nsi.bg (Bulgaria), sec.gov county.json (US), ocr.space, arcgis/Hawaii geodata (via Web2Cit claims) — consistent data-retrieval-eval shape: seeding external data-source links into sandboxes, then testing fetch/oracle primitives. [INFERENCE — consistent with the hacker's Web2Cit fetch-oracle finding]
- Same-account-serial pattern on Jun 25: 8 temp accounts, one edit each, identical payload, ~60–100s spacing — INFERENCE: per-edit identity rotation (each edit mints a fresh temp account). If confirmed, temp-account-name clustering UNDERESTIMATES session size: the "cluster" is the eval run, not the account.

## Files produced
- `wikipedia-lane/revisions.tsv` — 54 rows; columns: wiki, page, oldid, user, timestamp_utc, comment, tags, minor, parent_oldid, content_sha256, content_bytes. (comment/page/user/title escaped for TSV: backslash escaping) [OBSERVED]
- `wikipedia-lane/diffs/<host>_<oldid>.txt` — 49 files, raw compare-API JSON + provenance header. Missing oldids have no diff file (nothing to diff). [OBSERVED]
- `wikipedia-lane/raw/<host>_revisions.json` — primary-source batch responses (cache + provenance). [OBSERVED]
- `wikipedia-lane/records.json` — parsed intermediate. `wikipedia-lane/oldids.txt` — parsed (host, oldid) list. `wikipedia-lane/collect.sh`, `collect_diffs.sh`, `_emit_list.py` — collection scripts.

## Notable hits (raw dumps cached)

- HIT — missing Web2Cit configs (evidence-integrity): `raw/api-dumps/meta.wikimedia.org_30732691.json`, `..._30732696.json`, `..._30732698.json`, `..._30732699.json`, `..._30732700.json` — each carries the verbatim `badrevids` object `{"revid": <id>, "missing": true}`, HTTP 200, retrieved 2026-10-06T18:40:47Z. [OBSERVED]
- HIT — operator-account link: `raw/api-dumps/incubator.wikimedia.org_7226111.json` — user `~2026-36867-71` (the WMF-reported operator account) made a resolvable sandbox edit on incubator, comment 'Temporary technical sandbox initialization', part of the Jun 25 8-account burst. [OBSERVED]
- HIT — eval markers: `raw/api-dumps/test.wikipedia.org_747327.json` (`<!-- AIHW link-seeding test; temporary -->`); `raw/api-dumps/commons.wikimedia.org_1238390511.json` and `raw/api-dumps/meta.wikimedia.org_30732655.json` (`<!-- Lifeval ... -->`). [OBSERVED]
- HIT — SEC county.json link seed: `raw/api-dumps/commons.wikimedia.org_1233683454.json` (`[https://www.sec.gov/files//county.json SEC county data]`) — connects to the SEC county.json watch. [OBSERVED]
- CORRECTION (wiki-surgeon-2 flagged): `raw/diffs/test.wikipedia.org_741406.txt` was briefly an `invalidparammix` API error saved as a diff and falsely logged OK; retried with `fromtext` alone — valid diff cached, correction in collection.log. All 49 diff files re-validated (valid compare JSON, torev matches filename). [OBSERVED]

## Final layout (data-ready)

All lane artifacts live under `data/2026-10-06-wikimedia-rogue-agents/wikipedia-lane/raw/`:
- `raw/revisions.tsv` — 54 rows, 11 columns (verified: 49 content sha256/byte matches, 5 missing rows empty; 14-row field sample spot-check clean per wiki-surgeon-2).
- `raw/api-dumps/<wiki>_<oldid>.json` — 54 per-oldid raw API records (verbatim page+revision objects; missing oldids carry their `badrevids` object).
- `raw/<host>_revisions.json` — 9 complete raw batch responses (all nine wikis: en, test, test2, mediawiki, commons, simple, incubator, meta, bg).
- `raw/diffs/<wiki>_<oldid>.txt` — 49 raw compare-API responses + provenance header.
- `raw/PROVENANCE.md` — endpoints, params, retrieval timestamps, row counts, sha256 inventory.
- Worker notes: `workers/wikipedia-lane/revision-enumerator/{FINDINGS.md,CHECKPOINT.md}`.

Step-2 chunk divers work from `raw/revisions.tsv`; full content for every revision is in `raw/api-dumps/`.
