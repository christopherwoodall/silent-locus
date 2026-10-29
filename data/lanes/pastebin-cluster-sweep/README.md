# pastebin-cluster-sweep

Factum lane for the 2026-09-28 pastebin venue sweep. Legacy source:
`evidence/remove-2026-09-28-pastebin-cluster-sweep/` (was
`evidence/2026-09-28-pastebin-cluster-sweep/` before ingest).

## What the sweep did

On 2026-09-28 an agent probed 8 pastebin venues. The venues came from
references in 51 new anna.fyi pastes. The probe checked each venue for
swarm markers: `zz` labels, epoch nonces, transfer-test grammar
(`XFER`, `TRANSFER_TEST`, `REPLY_PAYLOAD`), proxy-ladder URLs
(`jqp`, `pure.md`, `md.succ.ai`, `r.jina.ai`, `allorigins`),
machine-grammar "Adjective Animal" authors, NSI/stats-venue references.

## Result

Zero swarm-marker hits. 3 of the 8 venues were not pastebins at all:
porkpad.com was a parked domain, gritpost.com a news blog, gotit.pub a
research-discussion platform. Of the 5 live pastebins, 2 had fully
sweepable public listings (nicepaste.com, mcbin.dev) and were clean.
3 had no enumerable public surface (pasteview.com JS-gated,
pastebox.to guest listing removed, pastebin.irixnet.org broken nav).

Swarm comms ponds remain anna.fyi plus the Iowa Stikked instance, as
far as public surfaces show. OBSERVED.

## Ingest model (2026-10-10)

9 legacy events became 10 Factum records:

- 8 `venue_probe` docs -> 8 `reachability.check` observations. The
  HTTP probe reached a page on all 8, so `outcome` is `response` for
  every probe. The venue verdict (`live_no_hits`,
  `dead_verified_negative`, `not_a_pastebin_verified_negative`,
  `live_no_hits_partial`, `live_no_listing`) stays verbatim in
  `tags.result`. Probe prose (`tags.detail`, `tags.markers_checked`)
  is byte-identical to the source events.jsonl.
- 1 `venue_finding` summary doc -> 1 `dataset.snapshot` observation.
  The dataset is the sweep's own event set, so `dataset_uri` holds
  the repo-relative events path, with a note in
  `tags.dataset_uri_note`. `coverage` is `complete`, `row_count` 9.
  This follows the lane-ingest precedent that maps `venue_finding`
  to `dataset.snapshot`.

Every record carries `{"lane":"pastebin-cluster-sweep"}` and a
`legacy_fingerprint` back to its source doc. Dedup check before
submit: no existing records held these 9 fingerprints or the lane
tag. Fuzzy venue matches came from other lanes' `pastebin_probe`
and `relay_paste` records, which cite the same venues in passing.
They are complementary, not duplicates.

Bundle builder: `build_pastebin_cluster_bundle.py` (kept here). It
reads events.jsonl and asserts byte-identical detail strings.
