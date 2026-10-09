# VILLAGE-JOIN — do our incident URLs appear in AI Village (2025, pre-recreation)?

Status: **COMPLETE — superseded by VILLAGE-JOIN-2.md.** The dataset was re-downloaded
2026-10-05 (13/13 tables, gated HF access restored) and the join ran in full.
See VILLAGE-JOIN-2.md for results. (Original blocked status preserved below for the audit trail.)

## What was asked
Do any URLs from our agent-incident corpora appear in the AI Village dataset
(`aidigestorg/ai-village`) in 2025 — i.e., *before* the incident-recreation
period, not during it.

## (a) Recreation window — UNVERIFIED
Could not be established: the village tables are not on disk and downloads
require gated HF authentication not available to this session. No date bounds
can be reported yet.

## (b) 2025 village rows scanned — 0
No village data was accessible. Nothing scanned.

## (c) Overlaps found — none yet (no data to join against)

## (d) Honest negatives per fingerprint set — not yet testable
Fingerprint families staged for the join (158 domains in our corpora):
dead-drop/relay (webhook.site, httpbun.com, pipedream, ntfy.sh, r.jina.ai,
catbox, pastebins, file.io, 0x0.st, transfer.sh), tunnels (*.ngrok.io,
*.trycloudflare.com, bore.pub, *.sslip.io, *.nip.io, localhost.run),
webhooks (discord.com/api/webhooks, api.telegram.org/bot), plus DeepSearchQA
phrase fingerprints and the IOC wordlist domains.

## Reference set built (ready)
`~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/village-join/`
- `our-urls-raw.txt` — 619,468 raw URL matches from our corpora
- `our-domains.txt` — 13,806 distinct domains with counts
- `our-fingerprint-domains.txt` — 158 dead-drop/tunnel/relay/webhook domains
- `ai-village-manifest.txt` — 390-file dataset manifest (sha
  838b4150303ca8228e8edb432d8b8ccae353d258, gated: manual)

## What unblocks this
The HF access token BigSexyWarlock69 granted on 2026-10-01 needs to reach an
authorized session via the secure flow (or the jsonl.gz tables re-downloaded
to `~/workspace/ai-village-data/`, skipping the ~380 screenshot tars).
Re-ping this session when data lands — the join plan in WORKLOG.md then runs
in a single pass.
