# EVAL-HUNT LANE 3: WebArena / WebVoyager / Mind2Web-shaped traces in the wild

Persona: eval-coordinator lane 3 (subagent session 7ba400f1), 2026-10-05 ~00:50 CDT.

## Premise
Hunt escaped web-agent benchmark runs on urlquery.net: WebArena task families
(OneStopMarket shopping, shopping admin panel, Reddit-style forum, GitLab clone,
map site), WebVoyager's 15-site task set, Mind2Web element-action traces.

Background: sibling persona confirmed DoE→dsqa_250; the Amap fleet matches NO
public benchmark. This lane hunts the inverse: wild agent activity that DOES
match known evals.

## Rules followed
- Agents only, never human operators. No commits/pushes.
- uq_htmx.py keyless search, ≤1 req/5s (used --delay 6).
- Egress test 2026-10-05 00:49 CDT: curl https://urlquery.net/ → 200 in 14.4s.
  Egress works but slow; htmx zeros treated as weak negatives per HTMX_ENDPOINTS.md.
- Verify every candidate against our sets:
  - data/2026-09-28-chinese-amap-fleet/events.jsonl
  - data/2026-10-03-openai-agent-traces/events.jsonl
  - data/2026-10-01-oai-tag-sweep/events.jsonl
  - silent-locus/collections/*/data/*.jsonl

## Steps

### Batch A — htmx keyword sweep (2026-10-05 ~00:55-00:58 CDT, delay 6s, limit 24)
| query | results | note |
|---|---|---|
| `webarena` | 0 | weak negative |
| `onestopmarket` | 0 | weak negative |
| `postmill` | ERROR (egress flake, retry in B) | |
| `mind2web` | 0 | weak negative |
| `webvoyager` | 0 | weak negative |
| `instruction=` | ERROR (egress flake, retry in B) | |
| `task_id=` | ERROR (egress flake, retry in B) | |
| `goal=` | 24 | examining — mostly shops/gambling domains; checking whether match is task-param or noise |

Local corpus greps (Amap fleet, OAI traces, OAI tag sweep, all collections data/*.jsonl):
zero hits on `webarena|onestopmarket|postmill|mind2web|webvoyager|instruction=|task_id=|add-to-cart` —
our sets contain NO benchmark-named eval traces by these terms.

### `goal=` verdict: NOISE (verified via keyless filter/http on 71548843-e43e-4cfc-b2ef-4b8a9acf4aa3)
Matches were Next.js RSC requests to a `/goal` page route (`goal?_rsc=1a78q`), not
`?goal=` task params. Result set = ordinary shops + sports sites (sportzone.co,
sportpolice.fr — "goal" as in soccer). Filed as negative.

### `postmill` verdict: WEAK NEGATIVE (verified via keyless filter/http + related/similar)
- 345e3cab-42a5-4b63-94f7-655cd4d3a665 (2026-08-16): single GET sequence on
  https://urlquery.net/report/345e3cab-42a5-4b63-94f7-655cd4d3a665 — postmill.app is a
  Next.js demo (/, /create?_rsc, /login?_rsc), NOT the PHP Postmill WebArena uses.
  No POST form payloads, no thread/comment creation, no similar reports.
  Looks like a page-load scan / curious visit, not a forum-task agent run.
- cdd11abb-5a0e-400f-aeff-8c6514273173 (2024-04-08): raddle.me, old, real Reddit-like
  site — not examined further (pre-dates current hunt window, human-traffic site).

### Batch B — cart-grammar + harness terms (2026-10-05 ~01:00-01:04 CDT)
| query | results | note |
|---|---|---|
| `add-to-cart` | 24 | NOISE: 24 WooCommerce shops scanned 05:19-05:46 UTC 2026-10-05; verified on e-byte.gr (88c04e28...) — keyword matched JS asset `add-to-cart.min.js`, submitted URL was plain homepage load. Bulk WooCommerce fingerprinting scan, not task runs. |
| `ajouter-au-panier` (FR) | 11 | NOISE: atmosphera.com product pages with `utm_campaign` email links, samaya-equipment `shpxid` shopper links, inmac-wstore `?coagent=*COAGENT*` template — marketing-email link scans, not eval tasks. |
| `agregar-al-carrito` (ES) | 5 | NOISE-ish: real shops (rotoplas.com.mx, amolca.com); commie.io#Y9WLvbuT + it-fc.de forum pair (2025-06-18) looks like phishing lure, not eval. |
| `eval-task` | 0 | weak negative |
| `magento` | ERROR (egress flake) | retry |
| `instruction=` | ERROR (egress flake) | retry |
| `in-den-warenkorb` (DE) | ERROR (egress flake) | retry |
