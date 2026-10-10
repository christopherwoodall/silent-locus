# proxy-fresh-blood

Lane for the 2026-10-08 proxy-fresh-blood hunt ingest.

## Source

Legacy lane: `evidence/2026-10-09-proxy-fresh-blood/`
(renamed to `evidence/remove-2026-10-09-proxy-fresh-blood/` after ingest).
Primary sources: the hunt's consolidated writeups FRESH.md and NOVELTY.md
(2026-10-08), copied verbatim into the legacy lane's `raw/`.

## Provenance caveat

The hunt's raw machine outputs (`/tmp/proxy-*.json`, `/tmp/shape-*.json`,
`/tmp/exfil-services.json`) were NOT preserved and no longer exist. This
ingest is a transcription of the two surviving writeups, which the hunt
states transcribed "key entries" with "nothing redacted". Fine-grained raw
rows (individual urlquery report records, per-host scan rows) are NOT
recoverable. Per-finding timestamps were not recorded in the source
documents. 2026-10-08 is the hunt date, not per-finding observation time.
Every record carries this caveat in `tags.provenance_caveat`.

## Records

49 records submitted 2026-10-09 (batch `728553a22ded4d13a2270f3e2e78bb26`):

- 27 `infra.proxy_instance` — 21 live/open (Tier 1 + Tier 2 services) and
  6 dead/gated Tier 3 services (corsproxy.our.buildo.io, yacdn.org,
  crossproxy.me, fuck-cors.com, cors.hyoo.ru, crossorigin.me).
- 8 `infra.proxy_chain` — observed proxy usage: 4 Zibri fleet liveness
  probes (example.com, HTTP 200), terabox-url-fixer red-team verification
  (example.com, HTTP 200), translate.goog Amap timing, xudaolong relay in
  front of pie.dev/base64, corsfix abcecd1d chain.
- 8 `infra.dead_drop` — livecodes.io, bytebin.rkslot.nl, litter.catbox.moe,
  bytebin.lucko.me, 2 ntfy.sh topics, httpstat.us, stash.legible.sh.
- 5 `infra.ioc` — post-audit fingerprint survivors (candidate status).
- 1 `source` record for the lane.

## Dedup

Pre-ingest `match --text` (fuzzy) ran against all 35 candidate key terms.
Zero true duplicates. Fuzzy hits were substring noise (e.g.
`darenx-corsanywhere.hf.space` matching `cors-anywhere.fly.dev`) or
distinct legacy ladder entries (2018-05-09-paste-archive-gap holds an
`infra.proxy_chain` for jqp.vercel.app and ladder URLs containing
cors.bwa.workers.dev — related evidence, not duplicate claims).

## Excluded from records

- 14-throwaway-workers burst: zero identifiers in source, graded
  UNVERIFIED. No record (placeholder terms are not allowed). Recorded here
  as a note, per the audit.
- Tier 3 herokuapp/glitch.me/cors-anywhere clones: unnamed in source.
- hunt_negative (paste.rs, 0x0.st, ix.io, dpaste.org, request-bin family,
  rentry.co, termbin, spoo.me): checked, zero agent markers. Kept as
  negative evidence in raw/FRESH.md.
- hunt_audit scoreboard and fingerprint_change: covered by per-record
  grades and the 5 `infra.ioc` fingerprint-survivor records.
