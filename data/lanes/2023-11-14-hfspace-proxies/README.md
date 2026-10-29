# 2023-11-14-hfspace-proxies

Factum lane for the HF Space proxy enumeration (Batch 3).

## What this lane holds

38 public Hugging Face Spaces with proxy shape. Proxy shape means a Space
that can fetch a URL for a caller. Two shapes dominate:

- CORS shims (generic `?url=` proxies, cors-anywhere clones).
- jina-reader clones (URL-to-markdown and web-reader Spaces).

One Space (`TheNacken/python-cors-proxy`) appears in the collusion-wiki
corpus (3 uses). The other 37 match the shape only. No swarm use is claimed
for them.

## Factum records

- 38 `infra.proxy_instance` observations, one per Space.
- 38 `source` records, one per Space page URL.
- Batch: `data/records/a3892bb8b0824e059adb92512d167785/`.
- Lane tag: `{"lane": "2023-11-14-hfspace-proxies"}`.
- Lane record: `lane_f2a273fa0e3d4131bec8807d2f9021b8`.

Host values: 24 use the observed `*.hf.space` live URL. 14 use a hostname
derived from the Space id. Derived hosts are flagged in record notes. The
derivation rule was checked against all 24 observed URLs.

## Source material

Legacy directory (renamed after ingest):
`evidence/remove-2023-11-14-hfspace-proxies/`. It holds `events.jsonl`
(38 rows), `PROVENANCE.md`, `SHA256SUMS`, and `raw/spaces.jsonl` (38 rows).
