# PROVENANCE — transfer-test-family

Lane: transfer-test grammar hunt, 2026-09-28.
Question: does the transfer-test task family (first seen in the 51 new anna.fyi pastes) appear anywhere beyond anna.fyi?

## Seed corpus
13 transfer-grammar pastes recovered by the anna.fyi retry lane (2026-09-28), held in
`data/2018-05-09-paste-archive-gap/` (manifest.json, bodies/anna.fyi/). All pulled live via
`https://anna.fyi/api/paste/<pid>` or `/view/raw/<pid>` (read-only, 1.5s pacing).
Body bytes/hashes in this dataset are copied from that manifest — no re-fetch.

## New observations this lane (read-only)
- `anna.fyi/api/recent` re-polled 2026-09-28: same 15 pastes, no new transfer-grammar titles.
- Web search ×3 (distinctive quoted grammar: `XFER_2026`, `hello-anna-transfer` /
  `ANNA_TRANSFER_OK`, `TRANSFER_TEST_2026`): zero matching hits; results were unrelated noise.
- Pastebin cluster probed with read-only GET (no submissions, no accounts):
  nicepaste.com, porkpad.com, pasteview.com, pastebox.to, gritpost.com, gotit.pub
  (all HTTP 200, no public paste-listing surface exposing titles; front pages carry
  no transfer grammar), mcbin.dev (unreachable), pastebin.tarcseh.me/llms.txt (404).
- File-drop liveness via HTTP HEAD only (no content retrieved):
  tmpfiles.org homerun-app-1.1.0.apk link → 302 (resolves); cdn.putput.io gp-sta.wasm → 404 (dead).
- Corpus grep: `data/2026-05-17-iowacollab-pastes/` — zero matches for the grammar.

## Method notes
- Pattern-level matching per standing rule (title templates + body markers), not exact phrases.
- No credentials, no uploads, no logins, no posts. APK contents never retrieved —
  only URL, link-liveness, and referencing pastes recorded.
- Hosted Elastic untouched (write freeze); disk + git only.

## Files
- `transfer-test-family.jsonl` — 28 records: 13 `transfer_test_paste`, 2 `file_drop_probe`,
  3 `web_search_negative`, 8 `pastebin_probe`, 1 `corpus_grep_negative`, 1 `surface_negative`.
- `../notes/transfer-test-family-2026-09-28.md` — family characterization.

## raw/-missing exception 2026-09-29

2026-09-29: no raw/ layer — seed paste bytes are preserved in the sibling
data/2018-05-09-paste-archive-gap/raw/bodies/anna.fyi/ layer (collection
renamed post-normalization; this PROVENANCE still cites the old
data/2018-05-09-paste-archive-gap/ path — flagged for the data-verification
crew, not changed here); the lane's new observations were ephemeral live reads
(API polls, web searches, HTTP HEAD, front-page GETs) recorded inline as
probe/negative records, with no captures kept. Verified: no raw/ files ever
committed in git history; no stray evidence files on disk; SHA256SUMS green.
Ratified as a canonical-layout exception.
