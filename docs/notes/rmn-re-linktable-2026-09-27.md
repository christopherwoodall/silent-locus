# rmn.re public link table — full crawl + chain decode (2026-09-27)

Source: https://rmn.re/admin/ — YOURLS 1.7.1 public index, world-readable, no auth.
Method: read-only crawl, 51 pages, ≥5s pacing, browser UA. No admin functions touched, no links created.

## Capture

- `data/rmn-re/link_table_2026-09-27.jsonl` — 764 links, full rows: slug, target URL, creation date, click count, creator IP (stored /16 as `creator_ip16`)
- Manifest: `data/rmn-re/link_table_2026-09-27_manifest.json` (page count, SHA-256)
- Decoded table: `data/rmn-re/link_table_decoded_2026-09-27.json` — same rows plus `decoded_target`, `chain[]`, `chain_depth`, `final_encodings`, `grammars`, `board_markers`, `status` (new/preserved)
- Total clicks across table: 84,023 (matches recon lane's 84,022 within crawl drift)
- Parser note: YOURLS puts the page *title* in the anchor `title=` attr; the real target is the first anchor's `href` (or the `<small>` anchor). First pass parsed titles as targets; re-crawled with the href fix.

## Cross-reference vs preserved 499-link log

- All 499 preserved slugs still live on rmn.re (0 gone).
- 265 NEW slugs since the preserved log.
- New slugs are mostly general-purpose YOURLS abuse, not campaign: dating spam (meetonlyhot.com, bgdaejd.bustydatng.com), phishing kits (portailsecureremboursementimpotgouv.justns.ru ×3), mail.ru business spam, ebay/YouTube. Top new by clicks: `5` (1,806), `lr` (1,396), `mobile` (1,334, justns.ru vocal-message phish).
- New-slug dates spread 2016–2026 — this install has been open for years; the campaign links are a subset of a much older public shortener.

## Chain decoding (static, URL strings only — no target fetches)

73 of 764 links carry proxy-chain wrappers. Decoded layer by layer (URL-decode + base64 per layer):

| wrapper | n |
|---|---|
| md.succ.ai | 34 |
| allorigins | 20 |
| proxymule | 9 |
| jqp.vercel.app | 4 |
| r.jina.ai | 3 |
| markdown.new | 2 |
| cors.bwa.workers.dev | 1 |
| corsfix | 1 |

- 65 decoded targets land on **www.sec.gov/files/county.json** with `?dummyagent=` / `?proxyunique=` nonces — the `zzmasscounty*` eval family (all preserved-status; this is the June campaign's SEC task).
- Deepest chain: `rmnmasec3xx24` — allorigins → allorigins → sec.gov/county.json (depth 2).
- `wpcagent2018md`/`wpcagent2020md` — markdown.new → api.worldpoverty.io GraphQL poverty queries (eval task targets).
- `masscounty1781813461d` — cors.bwa.workers.dev → sec.gov county.json.
- 2 rows carry scheme-obfuscated `HtTpS:` artifacts (failed URL parse, kept raw).
- da.gd appears as a nested shortener inside 4 chains (second shortener service).

## New board / agent surfaces (new-status slugs)

- `fieldnotes` → https://public-board.com/llms.txt
- `centaurinvitation` → https://thecolony.ai/for-agents
- `jk` → wixsite boutique page (echo keyword hit, likely noise)
- `lx` → https://example.org/agent-verify-test ("agent-verify" slug, preserved-era)
- `pbsweb95618278` (preserved) → viz.aihw.gov.au PBS dashboard PNG with `bridge` keyword in path

## New grammar slugs

- `zzzz` → youtube.com (zz, 331 clicks)
- `lw` → http://zzmasscounty (zz, bare host)
- `l2`/`l1`/`l0`/`kz` → example.com/global*47*/rmn-re/<10-digit-epoch>-<rand> — test/exfil scaffolding pattern (`global47-q-final-1784614860720-…`)

## Elastic

New index **`rmn-re-linktable`** — 764 docs, 0 errors, shared schema (`notes/gems-es-mapping.json`):
`event.dataset=rmn-re-linktable`, `record_kind=shortlink`, `package`=slug,
`labels`={clicks, creator_ip16, chain_depth, chain_wrappers, final_encodings, grammars, link_status},
`tags`={source:rmn-re, status:*, grammar:*, proxy:*}. Script: `scripts/es_ingest_rmnre.py`.

## Assessment

rmn.re is a years-old open shortener the campaign used as one tool among many — not campaign-owned infra. The 65 sec.gov/county.json chain-decoded links confirm the wiki-documented SEC eval task ran through these exact slugs. New slugs show no new campaign wave; the abuse is generic phish/spam. The `example.com/global47-*/rmn-re/<epoch>-<rand>` family and the two new agent-board surfaces (public-board.com, thecolony.ai) are the only new leads.
