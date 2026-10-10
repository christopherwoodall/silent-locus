# Mideast Scout — Summary (2026-10-04)

**Scout:** mideast (Middle East & Central Asia, Israel excluded)
**Mode:** LOCAL-CORPUS FALLBACK — egress outage, no live urlquery.net queries

## Egress outage (noted per instructions)

- 2026-10-04 ~23:37–23:42 CDT: `uq_htmx.py` live searches failed for all 7 assigned
  queries. Stderr shows urllib proxy-tunnel failures (`do_open` → `http/client`
  chain); curl to urlquery.net and google.com also failed from the VM.
- The 0-byte `mideast-*.json` files from that run were **replaced** with the
  local-corpus findings below; the `.err` files were kept as outage evidence.
- No further network retries were burned (per pivot directive).

## Method (local pivot)

Streamed `grep` (no full-file loads) over **80 jsonl files** —
`~/workspace/silent-locus/data/*/events.jsonl` + `~/workspace/silent-locus/collections/*/data/*.jsonl`
— totalling **~935 MB**, for the 7 assigned domains:
`gov.ae`, `gov.sa`, `gov.tr`, `gov.kz`, `gov.uz`, `gov.ir`, `gov.qa`.
Supplemental sweeps: 16 wider MENA/CA gov TLDs
(`gov.jo/iq/kw/om/bh/ye/sy/lb/az/ge/am/tm/tj/kg/ps/af`) and 19 regional
city names (dubai, riyadh, doha, ankara, istanbul, astana, tashkent, tehran,
baghdad, amman, kuwait, muscat, manama, baku, tbilisi, yerevan, ashgabat,
dushanbe, bishkek).

## Results per assigned domain

| Query | Real hits | Notes |
|---|---|---|
| `gov.ae` | **0** | — |
| `gov.sa` | **0** | — |
| `gov.tr` | **0** | 100 regex hits, ALL false positives (see below) |
| `gov.kz` | **0** | — |
| `gov.uz` | **0** | — |
| `gov.ir` | **0** | — |
| `gov.qa` | **0** | — |

### gov.tr false positives (documented, not real Turkish gov domains)

- ~97 hits are `*.translate.goog` Google-Translate proxy hostnames of **US**
  `.gov` sites from the already-tracked SEC county.json watch / collusion-wiki
  lanes: `www-sec-gov.translate.goog/files/county.json` (59),
  `investor-gov.translate.goog/files/county.json` (14),
  `www-investor-gov.translate.goog/files/county.json` (11),
  plus NIH/NCBI translate proxies (7). Context-verified: e.g.
  `https://www-investor-gov.translate.goog/files/county.json?_x_tr_sl=auto…`.
- 1 hit is the DeepSearchQA dataset **tag** `gov-trade` (category:travel) —
  matched only because regex `.` matched the hyphen in `gov-trade`. Not a domain.

### Supplemental sweep

- Wider MENA/CA gov TLDs: **0 hits** across all 16.
- City names: 3 mentions total —
  - `kuwait` ×2: a Berkeley climate-displacement case-study page scanned once
    via translate.goog (urlquery report `31e7b664…`) — single human/academic-shaped
    scan, no burst, no nonce grammar.
  - `dubai` ×1: `www.nasdaqdubai.com` inside DeepSearchQA question `dsqa_622`
    (fingerprint `NASDAQ`) — eval question content, not a scan target.

## Assessment vs the four agent-shape checks

(a) **Time clustering / bursts / metronome** — n/a; no matches to cluster.
(b) **Nonce/tag grammars in URLs** — n/a; none present.
(c) **Tunnel/shortener relays** (lhr.life, localhost.run, is.gd, ngrok) —
    n/a; none co-occur with any regional domain.
(d) **Systematic enumeration** — n/a; no enumeration sequences found.

**Verdict: honest zero.** No programmatic agent-shaped scanning of Middle East
or Central Asian government domains is present in the local corpora (~935 MB
across 80 event/hit files). The only "hits" resolve to the already-tracked US
SEC county.json watch via translate.goog proxies, a dataset tag, one academic
case-study scan, and one eval question string.

## Caveats

- Local corpora are a **partial** view — they reflect what prior lanes
  collected, not urlquery.net's live index. A live `gov.ae` / `gov.sa` /
  `gov.tr` / `gov.kz` / `gov.uz` / `gov.ir` / `gov.qa` query sweep should be
  re-run once egress is restored; the `.err` files document exactly which
  queries to replay.
- Grep was case-insensitive substring matching on raw jsonl; IDN/punycode or
  heavily obfuscated references would not match — noted as a residual blind spot.

## Raw files

- `mideast-gov-ae.json`, `mideast-gov-sa.json`, `mideast-gov-tr.json`,
  `mideast-gov-kz.json`, `mideast-gov-uz.json`, `mideast-gov-ir.json`,
  `mideast-gov-qa.json` — per-domain findings (this dir)
- `mideast-supplemental.json` — wider-TLD + city-name sweep
- `mideast-*.err` — egress-outage evidence from the failed live run

*Not pushed (per instructions). Clean negatives recorded.*
