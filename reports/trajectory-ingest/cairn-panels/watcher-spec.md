# Watcher spec — new Cairn / Strix / Hermes panels (Shodan)

- Purpose: detect new exposed panels for the Cairn, Strix, and Hermes Agent harnesses.
- Baseline: `data/lanes/cairn-panels/working/host-inventory.jsonl` (3,354 hosts, keyed by `ip`).
- This file is a specification only. Do NOT create the cron without the operator's word.

## Schedule

Run once per day at an approximate time. Shodan re-scan cadence is slow. Daily is enough.

## Queries

Run each query through the Shodan host search API. Page until empty. Store banners verbatim with provenance sidecars, as in the 2026-10-19 pull.

| Harness | Query | Baseline banners |
|---|---|---|
| Cairn | `http.title:"Cairn" -hostname:kespry.com -http.title:"causal" -http.title:"Designs" -http.title:"Reader" -http.title:"started" -http.title:"Sign in" -http.title:"Boutique" -http.title:"Note" -http.title:"Synology" -http.title:"coffee" -http.title:"Cairn Cloud"` | 96 |
| Cairn login | `http.title:"Cairn - Login"` | 1 |
| Strix | `http.favicon.hash:-566184040` | 9 |
| Hermes dashboard | `http.title:"Hermes Agent - Dashboard"` | 387 |
| Hermes Chinese login | `http.title:"登录 — Hermes Agent"` | 10 |
| Hermes product (full set) | `product:"Hermes Agent"` | 4,200 of 5,499 (partial baseline) |

Notes:

- The Hermes product query is the full-recall query. The 2026-10-19 run only reached 4,200 of 5,499 banners. Deep pagination stopped returning pages past ~page 41. The per-country split retry (`country:<CC> product:"Hermes Agent"`, country filter FIRST in the query) is still owed once credits reset.
- `http.title:"Strix Results"` is a readable alias for the Strix favicon query. Same 9 banners.
- If Shodan returns 401 "Insufficient query credits", stop and log. Do not retry until credits reset.

## Diff logic

1. Normalize new banners to hosts (dedup by `ip`).
2. Load the baseline: set of `ip` from `host-inventory.jsonl`.
3. Compute: `new_ips = current_ips - baseline_ips`. Also compute `dropped_ips = baseline_ips - current_ips` (panels go dark fast; track both).
4. For each new IP, pull the full Shodan host record and record: ports, org, ASN, country, titles, tags.
5. Fetch the panel page once with curl, GET only. No login, no POST, no interaction. Save HTML + provenance + headers + sha256 under `data/lanes/cairn-panels/raw/panels/`.
6. Append new hosts to the inventory with `first_seen_utc` set to the run time. Do not rewrite old rows.

## Alert conditions

Alert the operator when ANY of these is true:

- A new host carries the title `cairn coordinator` or exposes `/enroll/install` (enrollment-flow panels are the highest-value class).
- A new Cairn or Hermes host co-locates a known C2 fingerprint (Shodan `c2` tag, Cobalt Strike product, or similar).
- A new host sits on AS56971 (CGI GLOBAL LIMITED) or the IR country set, with database or open-dir tags.
- Net new hosts in one run exceed 50 (panel fleet spin-up).
- The Cairn coordinator at 46.4.115.187:8443 goes dark (title no longer `cairn coordinator` on fetch).

## Report format

One short block per run: counts per query, new IPs with one-line context (harness, country, ASN, ports, title), dropped IPs count, credit state. No operator identity work. Panels and infrastructure only.
