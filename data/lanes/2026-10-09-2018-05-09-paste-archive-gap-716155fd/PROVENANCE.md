# Provenance

Legacy work: lane M (2026-09-28) and lane-1-retry. Full account in
`evidence/remove-2018-05-09-paste-archive-gap/PROVENANCE.md`.

Ingest (2026-10-09, agent:lane-ingest-2018-05-09-paste-archive-gap):

- 67 `pastebin_probe` events. 13 paste IDs already in the corpus as
  `infra.message` (transfer-test-family lane). They were skipped. No
  duplicate was made.
- 54 new pastes went in as `infra.message`. Paste bodies are verbatim.
  The live-capture sha256 from the manifest is the ground truth.
- 89 `proxy_ladder_entry` events. 79 went in as `infra.proxy_chain`
  (laundering services: md.succ.ai, jqp.vercel.app, proxymule, r.jina.ai,
  and others). 10 www.sec.gov URLs went in as `infra.ioc`
  (category `other`, status `candidate`). They are the ladder's final
  fetch target, not a proxy hop.
- 1 `artifact_observation` went in through `capture --storage local`
  (joshuadavid anna.fyi revisions corpus, source of 45 lane-1 IDs).

Dedup: `match --text <paste-id> --mode fuzzy` for all 54 new paste IDs
and `match --url <url>` for all 89 proxy URLs. Zero hits.
