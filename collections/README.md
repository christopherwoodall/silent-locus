# Collections

Stateful, durable collection lanes for the Transluce us-canada-gov follow-up hunt.
Source: `notes/transluce-us-canada-gov-2026-10-01.md` ("Hunt implications" section).

## Lanes

| Lane | Dir | What | Status |
|---|---|---|---|
| arquivo-pt | `collections/arquivo-pt/` | Arquivo.pt capture metadata for incident domains+windows; adopts prior `data/2026-10-01-arquivo-pt/` pull | active |
| deepsearchqa | `collections/deepsearchqa/` | DeepSearchQA benchmark question fingerprints (hunt primitives) | active |
| fake-org | `collections/fake-org/` | "OpenAI Research" + self-identification string hunt over corpora | active |
| sec-county-watch | `collections/sec-county-watch/` | Watch spec + sweeps for `sec.gov/files/county.json` laundering | active |

## Durability contract (every lane)

- `state.json`: `{"lane", "started_utc", "watermark", "items_collected", "status"}` — updated as work progresses.
- `data/`: raw captures (small JSON/JSONL). Pulls > ~50MB: store a manifest + sample, note the full location.
- `collect.sh` (or `.py`): **idempotent** — re-running resumes from `state.json`, never re-collects, never invents IDs.
- Existing corpora/exports are **read-only**. Keep-all + annotate: new finds are annotated/staged, never merged into canonical datasets.
- Polite crawling only (≤1 req/2s). On block/rate-limit: stop the lane, record in `state.json`, move on.
- Scope: agents and agent infrastructure ONLY. No human/operator attribution, ever.

## Resume

```bash
cd ~/workspace/silent-locus && git checkout local
cat collections/<lane>/state.json        # where it stands
bash collections/<lane>/collect.sh       # idempotent resume
```

## Git

Work on the `local` branch. Commit each lane's progress with clear messages.
**Never push to GitHub. Never touch `main`.**
