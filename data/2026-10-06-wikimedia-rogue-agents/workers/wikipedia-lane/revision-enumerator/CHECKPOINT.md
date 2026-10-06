# CHECKPOINT — revision-enumerator
Lane dir: data/2026-10-06-wikimedia-rogue-agents/wikipedia-lane/
Worker dir: data/2026-10-06-wikimedia-rogue-agents/workers/wikipedia-lane/revision-enumerator/
Branch: wikipedia-edit-hunt-2026-10-06 (commit+push when lane complete; NEVER main).

## Done
- [x] Parsed raw/openai-wikimedia-edits-2026-10-04.csv → 54 unique (host, oldid) pairs → wikipedia-lane/oldids.txt (OBSERVED: 9 wikis, counts above).
- [x] Transport test: curl via egress proxy works; MediaWiki revisions + compare APIs respond 200 on en.wikipedia.org.
- [x] Wrote wikipedia-lane/collect.sh: paced (6s) batch revisions queries per host (metadata + full content), raw JSON → wikipedia-lane/raw/<host>_revisions.json, log → wikipedia-lane/collection.log.
- [x] compare edge case resolved: `fromrev` is required (tested, missingparam error observed); parentid=0 fallback = fromtext= (empty base).
- [x] FINDINGS.md: IP-search question answered (temp accounts ~2026-XXXXX-XX replaced public IPs; IPs are CheckUser-only; temp name is the public cluster key).
- [x] collect.sh batch phase — DONE: all 9 batch queries HTTP 200 (after fixing CRLF \r in oldids.txt; first attempt all HTTP=000 — transport-issue lesson banked).
- [x] Resolution: 49/54 resolve; 5/54 missing — ALL the meta Web2Cit config oldids (30732691/696/698/699/700), `{"missing": true}` in badrevids, HTTP 200 — confirms osint-scribe's evidence-integrity flag.
- [x] revisions.tsv built (54 rows); FINDINGS.md analysis section written (clusters, AIHW/Lifeval markers, per-edit identity-rotation inference).
- [ ] collect_diffs.sh phase 2 — RUNNING (bg session proc_2cd26f246ba3), 49 requests ≈ 5 min. compare edge case: fromrev required; parentid=0 -> fromtext=(empty).

## Exact commands to resume/verify
```
# oldids list
awk -F'[/?&=]' '{for(i=1;i<=NF;i++){if($i=="diff") id=$(i+1); if($i=="oldid") id=$(i+1)}; print $3, id; id=""}' \
  data/2026-10-06-wikimedia-rogue-agents/raw/openai-wikimedia-edits-2026-10-04.csv

# single revision metadata+content (adapt host + oldid)
curl -s -A "revision-enumerator/2026-10-06 (research; silent-locus hunt)" \
 "https://<host>/w/api.php?action=query&prop=revisions&revids=<oldid>&rvprop=ids%7Ctimestamp%7Cuser%7Ccomment%7Ctags%7Cflags%7Ccontent&rvslots=main&format=json&formatversion=2"

# single-revision diff (fromrev=parentid; parentid=0 -> use fromtext= instead)
curl -s -A "revision-enumerator/2026-10-06 (research; silent-locus hunt)" \
 "https://<host>/w/api.php?action=compare&fromrev=<parentid>&torev=<oldid>&format=json&formatversion=2"

# verify TSV↔diff-file integrity (after build)
python3 -c "import hashlib,glob; ..."

# final: git add data/2026-10-06-wikimedia-rogue-agents/wikipedia-lane data/2026-10-06-wikimedia-rogue-agents/workers/wikipedia-lane; git commit -m 'revision-enumerator: 54-revision table complete'; git push origin wikipedia-edit-hunt-2026-10-06
```

## Next
1. Parse batch JSONs → per-revision records + content sha256/bytes.
2. 54 compare-API calls (paced) → wikipedia-lane/diffs/<host>_<oldid>.txt (compare JSON + full content section; filename with www/incubator dots as-is).
3. Build revisions.tsv (columns: wiki, page, oldid, user, timestamp_utc, comment, tags, minor, parent_oldid, content_sha256, content_bytes).
4. Record every failed resolution + verbatim error in FINDINGS.md table.
5. Verify TSV↔diff integrity; commit + push branch.

## COMPLETE — 2026-10-06 18:52Z (data-ready signal)

- [x] collect_diffs.sh phase 2 — DONE: 49/49 diffs cached, all HTTP 200. One correction: test 741406 (invalidparammix on fromtext+fromslots mix) retried with fromtext alone; false "OK" log line corrected in collection.log.
- [x] External verification (wiki-surgeon-2): TSV VERIFIED — 54 pairs, zero misses/dupes/misassignments, 14 sampled rows zero field mismatches, 5 meta oldids genuinely absent upstream.
- [x] Restructure (data-first directive): revisions.tsv + diffs/ moved under wikipedia-lane/raw/; 54 per-oldid raw API dumps under raw/api-dumps/<wiki>_<oldid>.json; raw/PROVENANCE.md written (endpoints, params, retrieval timestamps, row counts, sha256s for all 113 files).
- [x] Self-verification: TSV<->api-dumps — 49/49 content sha256+byte matches, 5 missing rows empty, user/timestamp/parent spot-checks clean; 49/49 diff files valid compare JSON with matching torev.
- [x] Commit + push done (see git log). Lane is STEP 1 data; step-2 chunk divers work from raw/revisions.tsv + raw/api-dumps/.
