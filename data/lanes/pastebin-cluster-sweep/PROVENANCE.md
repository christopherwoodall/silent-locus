# PROVENANCE — pastebin-cluster-sweep (2026-09-28)

Lane: sweep of the 8 pastebin venues referenced in the 51 new anna.fyi pastes
(`data/2018-05-09-paste-archive-gap/`), per Christopher's "sick agents on this" directive.

## Trigger
Paste `b22dd745` ("List-of-subdomains") links `https://nicepaste.com/list-of-subdomains`;
other new pastes reference porkpad.com, pasteview.com, pastebox.to,
pastebin.irixnet.org, mcbin.dev, gritpost.com, gotit.pub.

## Method (read-only, passive recon only)
- Fetched each venue's public homepage/listing via page-text fetch (no logins,
  no submissions, no accounts, no API keys).
- Where a public listing/recent/search surface existed, swept visible titles
  (and sampled bodies) for swarm markers: `zz` labels, epoch nonces,
  transfer-test grammar (`XFER`, `TRANSFER_TEST`, `REPLY_PAYLOAD`),
  proxy-ladder URLs (jqp, pure.md, md.succ.ai, r.jina.ai, allorigins),
  machine-grammar "Adjective Animal" authors, NSI/stats-venue references.
- Supplementary web-search queries for listing surfaces and marker terms
  (engine-indexed pages only).

## Result
9 explicit-event documents in `sweep.jsonl` (8 venue probes + 1 summary finding).
**Zero swarm-marker hits.** 3 of 8 are not paste venues at all; of the 5 live
pastebins, 2 have fully sweepable listings (both clean) and 3 have no
enumerable public surface.

## Files
- `events.jsonl` — 9 docs (renamed from `sweep.jsonl` at the canonical-layout migration), one per observable probe/finding, deterministic
  `fingerprint` per doc.
- `progress.log` — resumable run log with DONE marker.
- `SHA256SUMS` — checksums.

## Limits
- nicepaste.com internal search: query interface not discoverable passively;
  engine-indexed pages only.
- pasteview.com paste bodies render via JS shell; API search needs paid
  entitlement (not attempted).
- pastebox.to: no public listing discoverable (guest pastes delisted per v3.0).
- pastebin.irixnet.org: "Recent Pastes" nav broken (resolves to forums site).
- No hosted Elastic writes (write freeze); disk + git only.

## raw/-missing exception 2026-09-29

2026-09-29: no raw/ layer — recon lane: ephemeral page-text fetches of public
venue surfaces plus web searches, recorded inline as probe records in
events.jsonl; zero swarm-marker hits, so no captures exist to preserve.
Verified: no raw/ files ever committed in git history; no stray evidence files
on disk; SHA256SUMS green. Ratified as a canonical-layout exception.
