# PROVENANCE — paste.ubuntu.org.cn / xz_knowledge_p1 (xinzhai-2026-07) dataset

Campaign/venue/actor/evidence-level records for the encrypted-paste run on
`paste.ubuntu.org.cn` (Jul 10–20 2026), filed by the third-party investigator
catalog as campaign `xinzhai-2026-07` ("the xinzhai persistence run").
Separate dataset. Not part of collusion-wiki. Zero hits in our own corpora
(see `corpus_grep_negative` record) — this is external investigator data,
ingested with external-overlap annotations per keep-all + annotate.

## Sources (all read-only; paste.ubuntu.org.cn itself was NEVER fetched)

1. `joshuadavid/wikiagentswarminvestigation` commit
   `c09593ffc904954fb4a9acae96b946d2d3c853e6` ("Read-only scrape of thecolony.ai
   + Centaur investigator trail"): `analyses/thecolony-ai/README.md`.
2. Centaur's thecolony.ai finding posts (full text read 2026-10-05 from the
   public post pages; verbatim copies in `raw/`):
   - `https://thecolony.ai/post/c894f76a-c06a-47f3-8926-1a0a36b1e471` (2026-09-05 16:21Z)
   - `https://thecolony.ai/post/de97aec6-e967-443f-8b76-d5ab65935068` (2026-09-05 21:33Z)
3. `swarm.termina.digital` catalog (ai-safety-lab, CC0-1.0, schema v8, data
   through 2026-09-08T01:30Z), rows preserved verbatim in `raw/`:
   - `terminadigital_campaign_xinzhai-2026-07.json` (from `pub/campaign.jsonl`)
   - `terminadigital_venue_paste-ubuntu-cn.json` (from `pub/venue.jsonl`)
   - `terminadigital_actors_xz.json` — `handle:paste-ubuntu-cn:xz_knowledge_p1`
     and `handle:paste-ubuntu-cn:xz_improvement_plan_p1` (from `pub/actor.jsonl`)
   - `terminadigital_evidence_ubuntu-cn-crawl.json` — `ubuntu-cn-crawl`
     (from `pub/evidence.jsonl`): paste IDs 4548500–4552399, every page saved;
     author/tag/displayed-time/length/head indexed; retrieved 2026-09-05 by fable.
   Catalog rows obtained via the joshuadavid repo's
   `analyses/termina-digital-mirror/scrape/outputs/swarm.termina.digital/pub/`
   (SHA-256-verified scrape, 2026-09-08).
4. Wayback captures of the termina.digital db pages in our own
   `data/2026-09-05-termina-digital/raw/wayback/db/`
   (`venue/paste-ubuntu-cn.html`, `cluster/xinzhai-store.html`,
   `campaign/xinzhai-2026-07.html`).
5. Lane-4 verification (2026-10-05): spaces-to-plus base64 decode of Centaur's
   published 124-char sample → 93 bytes, entropy 6.251 bits/byte, no gzip magic,
   no UTF-8, not Fernet. Characterization only; nothing executed.
   Notes in `raw/sample_decode_verification.txt`.

## What is NOT in this dataset (deliberate gap)

Per-paste records for the 3,484 `xz_knowledge_p1` posts (timestamps, bodies)
are NOT ingested. The 59 MB `record.jsonl` table and the 9.9 MB
`xz-ubuntu-cn-2026-09-05.tar.gz` body bundle are absent from the joshuadavid
repo, and `https://swarm.termina.digital/pub/` returned HTTP 503 ("public
exports are temporarily unavailable") on 2026-10-05. Retry those URLs when the
exports recover; then a per-paste `relay_paste` layer can be built (paste IDs
4548500–4552399 per the `ubuntu-cn-crawl` evidence row).

## Method

- `build_events.py` (co-located, per the single-collection-build-script
  convention) reads `raw/` and emits `events.jsonl` (11 records) and
  `rollup.jsonl` (1 row). Re-running reproduces both byte-identically
  (`event.created` pinned to 2026-10-05T08:00:00Z).
- Record kinds (all registered in `schema/README.md`): `paste_venue_rollup`,
  `run_shape`, `finding` x3, `report_capture` x3, `source_reference` x2,
  `corpus_grep_negative`.
- Fingerprint identity strings: `paste-ubuntu-cn:venue`,
  `paste-ubuntu-cn:xinzhai-campaign`, `paste-ubuntu-cn:encoding-verification`,
  `paste-ubuntu-cn:cadence`, `paste-ubuntu-cn:agent-assessment`,
  `paste-ubuntu-cn:centaur-post-1`, `paste-ubuntu-cn:centaur-post-2`,
  `paste-ubuntu-cn:joshuadavid-commit-c09593`,
  `paste-ubuntu-cn:source-campaign-row`, `paste-ubuntu-cn:source-evidence-row`,
  `paste-ubuntu-cn:corpus-grep-negative`; rollup: `paste-ubuntu-cn:rollup`.
- Every record carries `labels.external_overlap.*` annotations (source catalog,
  investigation commit, in_our_corpus=false).
- `scripts/validate_schema.py`: 0 violations (12 records).
- No Elastic writes were attempted (hosted write freeze in effect). No live
  fetches of paste.ubuntu.org.cn at any point.

## Keep-all policy

Nothing dropped. The per-paste gap is recorded in the rollup row
(`rollup.per_paste_ingested=false` + blocker), not silently omitted.

## Caveats

- Attribution is `unattributed` everywhere: the investigators grade the
  agent-persistence-layer reading as inference; operator/model/country unknown.
- Timestamps: campaign phase times are UTC+8 as displayed on the paste site
  (converted to Z in `@timestamp`); venue `first_seen` is a date, not a time.
- The 124-char sample is investigator-published evidence, verified by lane 4;
  per AGENTS.md 2026-10-05 it is kept verbatim (no redaction).
- Date prefix `2026-07-10` = first event (write tests 2026-07-10 21:26 UTC+8),
  per schema/collections.md.

## Lane notes

Full characterization: `data/2026-09-28-chinese-amap-fleet/personas/pastebin-plunderer/raw/deep-dive/lane4-xz-knowledge/XZ_KNOWLEDGE.md`.
