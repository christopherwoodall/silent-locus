# Transluce comparison — Cairn / Strix / Hermes panels

- Compared: 2026-10-19
- Our lane: `cairn-panels` (3,354 hosts, Shodan 2026-10-19)
- Transluce source: `data/lanes/2026-10-09-transluce-intel/raw/` — 127 finding files, pulls of 2026-10-07, 2026-10-08, 2026-10-11, 2026-10-13, 2026-10-17
- Method: full-text case-insensitive search for `cairn`, `strix`, `hermes` across every finding JSON

## Result

6 of 127 finding files mention one of the terms. **None reports panel infrastructure.** No finding lists panel IPs, ports, or the enrollment flow. The panel inventory is **NEW** to the corpus.

## What each hit actually is

| Finding | Term | What it is | Panel overlap |
|---|---|---|---|
| #149 | hermes | ClawBench V2 task path `hermes-v2-1112-...` in a filename. Benchmark task naming, not the harness. | None |
| #170 | hermes | Mentions "hermes agent skill repo" as prior documentation of jina laundering. A repo reference, not a panel. | None |
| #173 | cairn | A **self-described agent ("Cairn")** posted an unanswered greeting into a fleet dead-drop inbox. Also a sender with user agent **Cairn-Contact/1.0** posted a bilingual greeting into inbox 009f7... on Oct 7, 23:22 UTC. | Behavioral only |
| #183 | hermes | ClawBench V2 task paths (`hermes-v2-610-...`). Benchmark naming. | None |
| #184 | hermes | ClawBench V2 task path (`hermes-v2-531-...`). Benchmark naming. | None |
| #190 | hermes | ClawBench V2 task paths (`hermes-v2-635-...`, `hermes-v2-1138-...`). Benchmark naming. | None |

No finding mentions `strix` at all.

## Reading of finding #173

Finding #173 ("Follow-up to #171", created 2026-10-08) documents outside parties writing into the Amap fleet's webhook dead-drop inboxes on Oct 5–7. Two mentions matter:

1. "a self-described agent ('Cairn') whose greeting went unanswered"
2. "Oct 7, 23:22: a sender with user agent Cairn-Contact/1.0 posts a bilingual greeting into 009f7..."

This is loose corroboration that a **"Cairn" identity exists in the wild** and that it interacts with agent fleets. It says nothing about Cairn panels, hosts, or operators. It neither confirms nor contradicts our inventory. It is a behavioral touchpoint, not infrastructure overlap.

## Novelty verdict

- **The 3,354-host inventory is PRIMARY and new.** No Transluce finding covers it.
- **The Cairn coordinator enrollment flow (46.4.115.187:8443) is new.** No Transluce finding covers it.
- **The Cobalt Strike C2 co-location (47.97.206.32) is new.** No Transluce finding covers it.
- Finding #173's "Cairn" agent is the only related Transluce item. Mark it as related-but-distinct: same name, different evidence class (behavior vs infrastructure).
