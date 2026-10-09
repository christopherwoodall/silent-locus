# PROVENANCE — 2026-10-09-proxy-fresh-blood

Reconstructed source lane for the proxy-fresh-blood hunt findings.
Built 2026-10-09 on branch `factum-shaping` as part of the Factum rebuild
(missing-lane construction).

## Source

- Primary sources: `data/lanes/proxy-fresh-blood/FRESH.md`
  ("FRESH — new proxy-laundering + dead-drop services", 2026-10-08) and
  `data/lanes/proxy-fresh-blood/NOVELTY.md`
  ("NOVELTY AUDIT — fresh-blood finds", 2026-10-08). Both copied verbatim
  to `raw/` in this lane.
- These are the hunt's own consolidated writeups (8-lane hunt,
  branch `proxy-fresh-blood`, worked 2026-10-08) and carry the
  post-audit verdicts of 11 workers (10 research + 1 independent red team).

## Extraction method

Script `/tmp/build_proxy_lane.py` (ad-hoc, not retained in repo):
one legacy-lane event per finding section of the two documents,
transcribing the documented claims faithfully — proxy URLs, hostnames,
timestamps, report IDs, ntfy topics, counts, and audit grades kept
verbatim. Each event's `labels` carry: tier (Tier 1 / Tier 2 / Tier 3 /
Section 2 / Negatives), audit grade (REPORTED / ADJACENT / NOVEL with
confidence), claim basis (OBSERVED / INFERENCE), and campaign linkage.

Event envelope follows the existing legacy-lane convention
(@timestamp / event.dataset / record_kind / fingerprint / labels /
source_url / retrieved_at / retrieved_via / description).
`@timestamp` is the hunt date 2026-10-08 (per-finding timestamps were
not recorded in the source documents — the event carries
`timestamp_source: labels:hunt-date (2026-10-08)` so this is explicit).
`fingerprint` is sha256 of the canonical (sorted-keys, no-whitespace)
JSON of the event body, excluding the fingerprint field itself.

## Coverage

- 27 events: 18 `proxy_service_finding` (Tier 1: defuddle.md,
  Zibri cloudflare-cors-anywhere fleet, proxy.corsfix.com, Google
  Translate laundering, cors.bwa.workers.dev, jqp.vercel.app,
  cors-anywhere.fly.dev, pie.dev; Tier 2: api.cors.lol,
  corsproxy.marimo.app, cors.isomorphic-git.org,
  terabox-url-fixer.mohdamir7505.workers.dev,
  mcp-http-worker.james-sherborne.workers.dev,
  sovereign-llm-proxy.projectouroboroscollective.workers.dev,
  newfrontdoor/acailly/dex-nextjs trio,
  wispy-flower-cdf3.100brightli.workers.dev, 14-throwaway-workers burst;
  Tier 3 dead/gated generation summary),
  6 `deaddrop_finding` (livecodes.io, bytebin.rkslot.nl,
  litter.catbox.moe + bytebin.lucko.me + ntfy topic shmq-1791251472-a7x,
  ntfy topic zenity-repro-ad19805c36eb9602, httpstat.us, stash.legible.sh),
  1 `hunt_negative`, 1 `fingerprint_change`, 1 `hunt_audit`
  (scoreboard, storm-chaser identification, campaign linkages, systemic
  finding, method gaps).

## Caveats

1. The hunt's raw machine outputs (`/tmp/proxy-candidates.json`,
   `/tmp/proxy-agent-usage.json`, `/tmp/proxy-urlquery.json`,
   `/tmp/proxy-shapes.json`, `/tmp/shape-workers.json`,
   `/tmp/shape-clones.json`, `/tmp/shape-cfworkers.json`,
   `/tmp/exfil-services.json`) are VM-local files listed in FRESH.md
   but were NOT preserved — they no longer exist on this machine.
   This lane is a transcription of the two surviving consolidated
   documents, which the hunt states transcribed "key entries" with
   "nothing redacted". Fine-grained raw rows (individual urlquery
   report records, per-host scan rows) are therefore NOT recoverable
   from this lane.
2. The 14-throwaway-workers burst (2026-10-08) has zero identifiers in
   the source documents — the audit graded it UNVERIFIED (LOW); it is
   recorded as a note, not a service claim.
3. Audit grades are the 2026-10-08 audit's own verdicts (INFERENCE where
   marked); the hunt's systemic finding is that the novelty diff ran
   against the excluded-list, NOT the internal corpus — the
   `fingerprint_change` event carries the post-audit dedupe note.

## Grade

Claims carry the basis grades recorded in the source documents
(OBSERVED / INFERENCE). Audit grades (REPORTED / ADJACENT / NOVEL) are
the hunt's own novelty verdicts, not external corroboration.
