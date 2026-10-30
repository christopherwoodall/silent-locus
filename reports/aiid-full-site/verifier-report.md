# AIID full-site — verifier report

Role: independent verifier. Job: re-derive each claim from local bytes.
No Factum record was written. No commit was made. No push was made.
No network use. No login. No session. No Shodan use.
This report only adds this file. It changes no other file.

Terms used here, defined on first use:

- AIID: Artificial Intelligence Incident Database. A curated public
  database of AI incidents.
- Factum: the local structured evidence store. Records live in
  `data/records/`.
- Batch: one exported set of Factum records, with a manifest file.
- IOC: indicator of compromise. A value that can point to an incident.
  Examples: an IP address, a domain, a file hash.
- TTP: tactics, techniques, and procedures. A short slug names a known
  technique.
- Slug: a short code name for a TTP.
- Grade SECONDARY: content from a curated database, not first-hand
  observation.
- Basis UPSTREAM: a claim that rests on an upstream source, not on
  direct observation.

## Verdict: SHIP

All 11 checks pass. No fix is required before commit or push.
The open items that remain are operator gates, not defects:
cron creation and scanner enable need the operator word
(adversarial open fix O2), and first-live-run scanner checks
need a live run (open fix O3). The coordinator decision O1
is recorded in INGEST-REPORT.md and is accepted there.

## Per-check table

| # | Check | Result | Re-derived numbers |
|---|-------|--------|--------------------|
| 1 | Batch line counts; manifest hashes; lane tag on every record | PASS | Incident batch: 5,379 lines. IOC batch: 10,595 lines. Manifest file hashes match MANIFEST.md exactly (incident `20133579...400a`, IOC `202d71d0...72db`). Manifest `records_sha256` fields match recomputed file hashes. Every record in both batches carries `tags.lane = aiid-full-site` (5,379 of 5,379; 10,595 of 10,595), parsed from JSON, not grep-counted. Incident batch kinds: 1,775 source, 1,829 observation, 1,775 claim. IOC batch kinds: 1 source, 10,594 observation. |
| 2 | Corpus arithmetic; no other batch swept in | PASS | 5,379 + 10,595 = 15,974. 208,745 + 5,379 = 214,124. 214,124 + 10,595 = 224,719. Batch dirs by mtime: the two claimed batches are the newest (incident 2026-10-30 12:31 UTC, IOC 2026-10-30 13:10 UTC). The next newest dirs are 2026-10-30 05:53 UTC, lane `2026-10-30-o-pattern-phase2`, not this lane. No batch dir sits between or after the two claimed ids. Note: corpus totals rest on the builders' `verify` outputs plus this arithmetic; this verifier did not re-run the Factum index. |
| 3 | Reconciliation: snapshot, overlaps, PARTIAL, 404s, post-snapshot gap | PASS | Snapshot inventory holds 1,777 incidents. Extracted JSONs hold 1,775 incidents. Snapshot minus extracted = exactly 1152 and 1433. Ingested sources = 1,775, same two missing. Zero provenance records for 1152 or 1433 in either batch (incident-batch tags: none; IOC-batch provenance incident lists: none). All 8 PARTIAL incidents (16, 46, 68, 373, 1178, 1424, 1441, 1469) hold source records, so all 8 were ingested fully. The 5 HTTP-404 report pages (3447, 2587, 3205, 3875, 3916) hold zero files in the fetch lane, so the gap is real and recorded. The 5 post-snapshot incidents are stated as unknown IDs, never fetched, in MANIFEST.md, INGEST-REPORT.md, and HUNT-INDEX.json scope notes. |
| 4 | Extraction totals; HUNT-INDEX; novelty | PASS | e1: 889 JSON, 1,524 behaviors, 13,896 IOC mentions. e2: 886 JSON, 1,340 behaviors, 7,474 IOC mentions. Totals: 2,864 behaviors, 21,370 mentions. Mentions by kind re-derived exactly (url 13,127; domain 6,918; model 652; model_or_tool 95; file_path 81; hash 377; tool 64; ip 56). Distinct IOCs: 10,594 kind-plus-value pairs in `iocs.json` full_set, matching the IOC batch observation count. Raw distinct pairs before query-strip: 10,598; the drop of 4 is the URL query-strip merge (7,959 raw distinct URLs to 7,955). HUNT-INDEX.json: 1,777 entries, `hunt_relevance` true for 122, false for 1,655. The field name is `hunt_relevance`, not `hunt_relevant`. Novelty verdicts: 1,767 NEW, 2 OVERLAP, 8 PARTIAL. |
| 5 | Slug accounting: 53 TTP records plus 1 behavior record | PASS | Batch holds 53 `intel.ttp` records across 42 incidents, 18 distinct slugs, and exactly 1 `intel.behavior` record. The behavior record is incident 1395, slug `proxy-network-fraudulent-accounts`. The same incident and slug also hold one of the 53 TTP records. This is two record types for one slug assignment, not a double count of a TTP entry and not a 54th slug. The behavior record carries the verbatim text. The TTP record carries only the slug-to-incident link. Full slug list (18): ai-cli-assisted-secret-discovery, back-channel-price-collusion, decompile-loop-exploit-foundry, dns-firewall-bypass-internet-access, exfil-via-public-github-repo, form-auto-submission, guardrail-bypass-ctf-pretext, guardrail-bypass-student-pretext, llm-runtime-payload-generation, peer-account-sabotage, proxy-network-fraudulent-accounts, reasoning-transcript-extraction, reseller-relay-front, sql-injection-via-url, state-actor-ai-attack-lifecycle, token-extraction-from-client-config, url-shortener-abuse, vibe-hacking. Note: the other 2,863 extracted behaviors live only inside incident observation summaries, as INGEST-REPORT.md states. No slug was invented for them. |
| 6 | Split tarball; gitignore; 100 MB rule | PASS | Part hashes match `raw/snapshot/SPLIT-SHA256SUMS.txt` exactly (aa `53ab106d...7311`, ab `625d0ac5...8298`, ac `2ad1b797...0e79`). Part sizes: 52,428,800 + 52,428,800 + 16,632,467 = 121,490,067 bytes, the original size. Reassembly (`cat` parts, then `sha256sum`) gives `bc8c01b15417785d3753f95052d0c20816b57e9f41a954175e6aabf9f8eead07`, the original hash. `git check-ignore` confirms the original tarball is ignored (lane `.gitignore` line 3) and part-aa is NOT ignored. `find -size +100M` over the lane returns only the ignored tarball. |
| 7 | SHA256SUMS recompute | PASS | `sha256sum -c` over `reports/aiid-full-site/SHA256SUMS`: all 11 listed files OK (HUNT-INDEX.json, INGEST-REPORT.md, IOC-REPORT.md, TOOL-UPDATES.md, aiid-scanner-cron-body-DRAFT.md, build-ioc-bundle.py, ioc-bundle.json, iocs.json, scanner-fix-note.md, scanner-verification.md, adversarial-review.md). MANIFEST.md and SHA256SUMS itself are not in the list, as stated. This verifier report did not exist before this write, as expected. |
| 8 | Wordlist and config | PASS | `wordlist.json` parses: 3,991 entries, 0 duplicate terms. `wordlist.txt`: 3,967 non-comment lines, 0 duplicates. Old entries unchanged: the old 3,895 JSON entries are a byte-identical prefix of the new file (96 added, 0 removed, 0 changed); the old text lines are a prefix of the new file (64 added). Config diff by `git diff --numstat`: 149 insertions, 3 deletions. The earlier "152 insertions" wording was wrong; 152 is the total changed lines (149 + 3). The diff sits in 4 hunks, all inside `iocfeeds` (note, otx list) and `prcomment` (note, queries). No `aiid` block was added. `otx_indicators` = 52 (old 23 is an exact prefix; 29 added). `prcomment` queries = 11 (old 10 is an exact prefix; 1 added, the production-deletion query). |
| 9 | Scanner | PASS | `py_compile` passes. `--dry-run` exits 0, prints the dry-run lines plus `[]`, creates no `aiid_state.json` file, and leaves `error-log.jsonl` byte-identical (md5 checked before and after). Live run (no flags) prints the disabled refusal to stderr, prints `[]`, exits 0, and creates no state file. Code holds F1 (`_entry_key` gives `date|kind`, `STATE_VERSION = 2`, `_snapshot_kind` splits tarball and excel) and F2 (both degraded branches skip the state save when the baseline is fresh, with a "fresh baseline not persisted" note). Independent spot test: a synthetic listing with a 2026-10-26 tarball anchor and a 2026-10-26 Excel anchor parses to two entries, `('2026-10-26', 'tarball')` and `('2026-10-26', 'excel')`. Module size 29,346 bytes, matching scanner-fix-note.md. Config holds no `aiid` key, so the module stays inert. |
| 10 | Grades and hygiene | PASS | All 15,974 batch records grade SECONDARY. All 1,775 incident claims carry basis UPSTREAM. No record grades press content as observed. IOC confidence mapping holds: high 6, medium 8,247, low 2,341; status active 8,253, candidate 2,341. Low stays low: all 326 hash records carry confidence low, and 5 of 56 IP records carry confidence low (quoted-address forms, per the `iocs.json` caveats). No `token=`, `signature=`, `sig=`, `access_token`, or `api_key` string appears in either batch or in `iocs.json`. URLs with a query string: 74 distinct, all in `?params=` form except the 2 disclosed exceptions (one Amazon path-segment `=`, one incident 1162 path-like `?params=` value). The one other `=` is a path segment, not a query value. No signed value and no full query string is carried. No submitter, editor, or author personal name was added: the only `submitter` word hit in the incident batch sits inside one incident observation summary (verbatim incident text, incident 452), and no batch record holds a submitter, editor, or author field. Titles and descriptions are verbatim AIID text. The two behavior-text name residues are disclosed in INGEST-REPORT.md coordinator decision O1 (lines 312-314). The cited line numbers are correct: line 2669 is the incident 901 observation, and line 4522 is the incident 1512 observation, in `data/records/fc09b8bfbd7b4d719e070fed0d5c4d49/records.jsonl`. The names themselves are not reproduced here, per the task rule. |
| 11 | Adversarial fixes actually applied | PASS | F1: INGEST-REPORT.md line 57 now says 18 distinct slugs; the batch re-derives to 18. F2: INGEST-REPORT.md line 266 cites batch `8f3ed80b8fbb415a8fe399d6fb836d75`, and that directory exists. F3/F5: query exceptions are noted in IOC-REPORT.md line 40 and INGEST-REPORT.md lines 240-243; the underlying counts re-derive (84 mentions with a query string in extraction collapse to 74 distinct URLs; the incident 1162 path-like value is confirmed in extraction). F4: the snapshot-time precision warning is in INGEST-REPORT.md. F6: `iocs.json` counts block holds `incidents_with_iocs` 1774; extraction re-derives to 1,774 incidents with at least one IOC (incident 88 holds zero). F7: the name-claim qualification is in INGEST-REPORT.md. F8: the cron draft schedule reads Mondays 15:00 America/Chicago. F9: the cron draft state section reads `{date|kind: {url, anchor_hash}}` with schema version 2 and the version-1 quarantine note. Open items O1 (coordinator decision, now recorded), O2 (cron creation and enable, operator-gated), O3 (first-live-run scanner checks), O4 (stale git-status line, see observation below), and O5 (brief wording, no file to fix) are correctly left open, not silently closed. |

## Fix list

None. No file needs a change before commit or push.

## Observations (not fixes, no action required)

- Wordlist gap, pre-existing and already disclosed: `wordlist.txt`
  holds 3,967 non-comment lines while `wordlist.json` holds 3,956
  active terms, a gap of 11. TOOL-UPDATES.md section 1d flags it
  and leaves it out of scope. This verifier confirms the gap
  (3,967 vs 3,956) and confirms it predates this task (old files:
  3,903 vs 3,892, same gap of 11). No change is asked here.
- TOOL-UPDATES.md section 6 says git status showed exactly three
  modified files and `aiid.py` untouched. That line was true for
  that lane at write time. The current tree differs because sibling
  work and the scanner-fix lane landed after it. Adversarial
  review open fix O4 already flags this. The coordinator must
  re-check status at commit time and commit only the intended
  paths. No edit to the line is asked here.
- MANIFEST.md line 39 says the lane holds 25,553 files before
  split parts and extracted JSONs, and 3.1 GB. Re-derived size is
  3,297,881,099 bytes (3.07 GiB, about 3.1 GB in GiB terms, so the
  size line is sound). Re-derived file count on the same basis
  (fetch files 25,532 plus snapshot files other than parts and
  tarball 22) is 25,554, one more than stated. The counting basis
  for the stated figure is not recorded, so this verifier does
  not prescribe a corrected figure. The difference is immaterial
  to commit correctness.
- MANIFEST.md lists `verifier-report.md` among the reports. That
  file is this file. It now exists, so that list entry is now true.
- SHA256SUMS does not list MANIFEST.md, SHA256SUMS itself, or
  this verifier report. A fresh SHA256SUMS run after commit
  should add this file if the coordinator wants it covered.
