# Lane K — webhook dead-drop marker search (2026-09-27/28)

**Technique:** JFrog GemStuffer report documents a webhook dead-drop exfil in
`southpxdatapp6pi@0.0.1` — zlib+base64 Southwark calendar chunks in
`/api/v1/web_hooks` URLs shaped `https://example.com/A000/<chunk>` …
`ZZEND/<count>`. Same embedded key family as `yardxabc889`.
https://research.jfrog.com/post/gemstuffer-openai-rubygems/

## Hits (5 packages, 8 docs)

**Confirmed dead-drop family — May-12 wave:**
- `slvhg151` (0.0.2, published 2026-05-12T02:07Z) — lane-20 advisory Diffend sweep
  found the `web_hooks?|A000|ZZEND|southpxdatapp` pattern in its Diffend diff
  render; only one of 394 advisory names with the pattern. Payload bytes never
  recovered (sweep stored only mechanism_notes). Also in JFrog inventory
  (XRAY-1023618). Evidence level: pattern_match_page_render, medium confidence.
- `southpxdatapp6pi` (0.0.1, published 2026-05-12T01:57Z, sha256
  4d0754a0…, meta_summary "test", author "- A") — harvested by our Diffend
  reconstruction; gemspec metadata already carried the Southwark council-domain
  IOC (`moderngov.southwark.gov.uk/mgCalendarMonthView.aspx?GL=1&bcr=1`,
  fingerprint=council-domain, high). Reconstructed files are 1-byte stubs in
  this checkout, so payload content is not locally available. Evidence level:
  name_plus_metadata, high confidence on the name attribution.

**Webhook-named candidates — July-7 wave (name-only, low confidence):**
- `webhook-payload-1783405583` (0.0.1, 0.0.2) — epoch 1783405583 → 2026-07-07T06:26Z
- `webhook-fire-1783405247` (0.0.1) — epoch → 2026-07-07T06:20Z
- `webhook-capture-1783406220` (0.0.1, 0.0.2) — epoch → 2026-07-07T06:37Z

All three JFrog-only (XRAY-1079203/204/246), no Diffend presence, no payload
bytes. The July wave is the XSS/SSTI exfil family (xssname-1783397821 →
webhook.site per JFrog), so these could be exfil tooling — but the A000/ZZEND
dead-drop mechanism is May-attributed; the relation is unverified. First item
on the July-7 Diffend sweep target list.

**Ambiguous (logged, not claimed):**
- paste-linuxiarz paste 24775389 (Iowa agent-comms mesh): chunk_marker "A000"
  hit on the unredacted body; stored body is now redacted, context
  unrecoverable. Not gem corpus.
- thecolony-ai sweep.json: 2 unattributed A000 counts, no per-doc provenance;
  could be incidental hex.

## Negative results (high-confidence sweep)

- Full-repo grep across `data/` + both `diffend_sweep_results*.jsonl`: **zero**
  occurrences of `ZZEND`, `web_hooks` (in content), `oast.online`,
  `webhook.site`, chunk-label variants `/A0[0-9]{2,4}/`, `A0000`, `web_hook`
  singular. Byte-level scan of all 28 recovered `.gem` tarballs (outer + inner
  data tar): zero markers. No base64/zlib-encoded marker variants found — the
  sweep records store plaintext metadata only.
- ES `collusion-wiki` (read-only): 0 hits for southpxdatapp, ZZEND, web_hooks,
  webhook.site, oast.online, webhook, A000.
- ES `rubygems-goimport-campaign`: 0 hits for southpxdatapp / A000 content;
  slvhg151 exists only as jfrog_inventory; webhook-* hits are the three
  JFrog-only July names above.

## What landed

- `data/webhook-deaddrops/`: `webhook-deaddrop-hits-2026-09-27.jsonl` (8 docs),
  `PROVENANCE.md`, `progress.log`.
- Script: `scripts/es_ingest_webhook_deaddrops.py` (idempotent, deterministic
  `_id` = doc_id).
- ES index **`webhook-deaddrops`**: 8/8 docs (2 webhook_deaddrop, 3
  webhook_deaddrop_candidate, 2 marker_ambiguous, 1 sweep_negative); shared
  canonical schema + `marker`/`evidence_level` keywords; `event.dataset.keyword`
  multi-field present at creation (verified in mapping).

## Open

1. slvhg151 Diffend diff page re-fetch → recover actual `/api/v1/web_hooks`
   URL chunks (only real path to the A000…ZZEND URL shape).
2. July-7 Diffend sweep for the three webhook-* packages (payload bytes decide
   whether they're dead-drop or XSS-family tooling).
3. southpxdatapp6pi bulk-harvest JSON log may hold real payload bytes (local
   reconstruction is 1-byte stubs).
