# SE/South Asia agent-activity scout — summary (2026-10-04)

## ⚠️ Egress outage
Live urlquery.net queries were NOT possible. Egress died mid-run (curl to
urlquery.net AND google.com both fail; the `uq_htmx.py` proxy tunnel errors
out; the first exec backgrounded by the parent is stuck/unreachable). Only 5
of 8 planned queries fired and all returned 0-byte JSON (their `.err` sidecars
hold the Python traceback). No live-search verdicts were obtained.

**Pivot:** full scan of local silent-locus corpora instead:
`data/*/events.jsonl` (streamed grep) + all `collections/*/data/*.jsonl`.
Results below are from that local sweep.

## Findings

### 1. INDONESIA (go.id) — PROGRAMMATIC agent scanning ✓ (frozen urlquery incidents)
Five urlquery incident records in `data/2026-10-01-oai-tag-sweep/events.jsonl`,
all tagged `urlquery-hunt` + `agent-activity` + campaign `cors-laundering-ops`
(indicator `cors_conversion_proxy`, wrapper `corsproxy.json`):

| report (urlquery) | submitted URL (url_original) | date |
|---|---|---|
| 1df03d5a-ba13-474d-8036-26fe31526ee7 | `pa-gresik.go.id/index.php?option=com_media` | 2026-07-08 |
| faa48376-8a90-4980-a965-357ad03914e7 | `jdih.balikpapan.go.id/dokumen/610/detail?utm_source=chatgpt.com` | 2026-07-15 |
| a9c7e089-c55a-4a95-8d41-c57cd6cb346a | `www.dinkes.semarangkota.go.id/` | 2026-07-15 |
| 09195203-e3e2-4e42-92b1-735a684ff56f | `dinkes.acehprov.go.id/detailpost/abcde-cegah-stunting` | 2026-07-19 |
| 1e16f79e-0006-48e2-b450-1d99f6a78165 | `www.kkp.go.id/djpdskp/kkp-permudah-produk-umkm-tembus-pasar-global-dengan-gmp-sertifikat65c30481d5d51/detail.html` | 2026-08-31 |

Agent-shaped signals: (a) CORS-conversion-proxy laundering wrapper on every
hit — agents routing gov-site fetches through a CORS proxy so an XHR-only
client can read cross-origin responses; (b) `?utm_source=chatgpt.com` — the
agent self-identifying in the submitted URL; (c) hex nonce fragment
`65c30481d5d51` embedded in a kkp.go.id path (nonce grammar); (d) two reports
~3h apart on 2026-07-15 on different city/district health-service hosts —
systematic municipality-by-municipality enumeration (Gresik, Balikpapan,
Semarang, Aceh, national KKP ministry).
Raw: `seasia-local-goid-incidents.jsonl` (5 records).

### 2. VIETNAM (gov.vn) — PROGRAMMATIC stats-API task family ✓ (known family)
`pxweb.nso.gov.vn` + `pxweb.gso.gov.vn` (Vietnam National Statistics / General
Statistics Office PX-Web APIs) appear as YOURLS referrers on the UNM
`goto.unm.edu/7t6-o` shortener stats surface — the swarm's proxy stack leaking
the task targets: host_total_hits=59, host_url_count=32 distinct referrer URLs.
Agent-shaped signals: (a) **encoding-variant retry grammar** — the same table
endpoint hit as literal-space, `%20`, and `+` variants
(`api/v1/en/National Accounts and State budget/`); (b) a `TESTDEFAULT999`
probe URL (`pxweb.nso.gov.vn/TESTDEFAULT999`); (c) both agency hostnames used
(nso + gso). Corroborated by lane N (`data/2026-09-28-pxweb-national-stats/`,
`data/2026-09-28-nsi-venue-sweep/`); fits the swarm's national-stats-API task
family (UK ONS Census 2021 via rmn.re shortlinks in the same dataset).
Raw: `seasia-local-govvn-pxweb-referrers.jsonl` (39 records).

### 3. INDIA (gov.in) — agent link-laundering, not urlquery triage
11 records, all `frozen:collusion-wiki` (wiki_record/wiki_link) — no urlquery
incident reports. All carry `https://proxy.cors.sh/https://www.indiascienceandtechnology.gov.in/res...`
(a CORS relay wrapped around India's science-and-technology portal), some with
Google-Translate params `_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=en` — the same
agent laundering pattern as the sec.gov county.json CORS record
(`proxy.cors.sh/https://www.sec.gov/files/county.json`). Verdict: programmatic
agent-side relay usage, single-target, NOT human triage and NOT a urlquery
scanning campaign. Raw: `seasia-local-govin-cors.jsonl` (11 records).

### 4. MALAYSIA / PHILIPPINES / THAILAND / BANGLADESH / PAKISTAN — honest zero
Zero corpus hits for `gov.my`, `gov.ph`, `gov.th`, `gov.bd`, `gov.pk` across all
`data/*/events.jsonl` (host-name patterns filtered for infrastructure terms).
No agent activity in the frozen corpora for these five countries' gov domains.

## Verdict matrix
| Region | Programmatic? | Evidence |
|---|---|---|
| Indonesia (go.id) | **YES** | 5 urlquery incidents, cors-laundering-ops, self-ID, nonce, municipality enumeration |
| Vietnam (gov.vn) | **YES** | 59 hits/32 URLs, encoding-variant retries, TESTDEFAULT999, stats-API task family |
| India (gov.in) | agent-shaped link, no urlquery campaign | CORS-relay + translate-param grammar in collusion-wiki |
| MY/PH/TH/BD/PK | **NO (honest zero)** | zero local-corpus hits |
