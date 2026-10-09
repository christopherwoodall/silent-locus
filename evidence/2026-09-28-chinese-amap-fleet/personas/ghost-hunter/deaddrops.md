# DEAD-DROP GRAVEYARD — webhook.site inbox liveness sweep

Sweep date: 2026-10-05 ~04:45–05:30 UTC (00:45–01:30 CDT). Ghost-hunter child of `FINDINGS.md`.
Question: which webhook.site dead-drop inboxes are still receiving after their agent died?

## Status: CATALOG COMPLETE, LIVE CHECKS BLOCKED

Total HTTPS egress through the VM's proxy (`hatch-egress-proxy:3128`) is DOWN — `webhook.site`, `urlquery.net`, `github.com`, even `example.com` all time out (HTTP 000, curl rc=28). Proxy port is open; CONNECT through it stalls. So:

- **Step 1 (extract all inbox URLs/UUIDs): DONE** — full catalog below, with campaign last-seen per inbox from the local corpus.
- **Step 2 (fetch public inbox pages): BLOCKED** — no ghost verdict can be established until egress returns. Recheck script saved at `recheck_deaddrops.sh` in this directory; run it when egress is back, or hand the endpoint list to a live-browser-capable agent.
- **Step 3 (urlquery htmx sweep for new submissions): BLOCKED** — `uq_htmx.py` needs urlquery.net. Command ready in "Recheck" section.

## Inbox catalog

### A. Amap-fleet dead-drops (campaign window: 2026-09-28 → 2026-10-04)

| Inbox UUID | First/collected seen (UTC) | How observed | Campaign last-seen | Preliminary read |
|---|---|---|---|---|
| `6ddc559e-5c08-4915-a5b2-f4addc42368a` | 2026-10-04T15:01:37Z (urlquery `97f0619b`, carrier route) | Submitted URL to urlquery | 2026-10-04T17:12:59Z (fleet's newest inbox created 2h later) | **FRESH** — created ~14h ago; free-tier inboxes live ~7d. Almost certainly still exists. Ghost check = revisit ≥2026-10-12: any request arriving after the fleet's last activity = still-firing cron. |
| `0a947514-5b43-4030-9f9f-b193dd2d519b` | 2026-10-04T17:12:59Z (urlquery `8213c4a1`) | Submitted URL to urlquery | same (fleet's newest artifact) | **FRESH** — same as above. |
| `a7753b69-2ceb-4221-adfa-80f69d57480c` | 2026-10-04T15:13:31Z (urlquery `eb4ecb55`, relay route via `href.li/?https://webhook.site/a7753b69-…?run=1791126770493`) | Fleet wrapping its own dead-drop in href.li (self-laundering the exfil URL) | 2026-10-04T17:12:59Z | **FRESH** — same as above. Note the `?run=<epoch>` query grammar = fleet epoch-nonce, matches live grammar. |

**The missing 14:** lane analysis (`raw/analysis/COLLECT.md:17`, `raw/analysis/INFRA.md:34`) records that the fleet had **14 additional inboxes visible via webhook.site's public API** (observed in report `97f0619b`'s page context on 2026-10-04; "created from Tencent Cloud via `python-requests/2.32.5`", deepseek-hunt notes 13/14 on AS132203 with `hysandbox-ats` marker) — but **their UUIDs were never collected into the dataset** ("Not collected here"). They are the highest-value ghost targets and are currently unknowable from the local corpus. Recovery path: view inbox `6ddc559e…` live when egress returns — if the operator's other inboxes still exist, webhook.site's public page may expose them; otherwise they are gone unless someone recorded them.

### B. Same-operator legacy dead-drops (Jun–Aug 2026 lhr.life/is.gd/httpbun/jina stack)

Per `infra-sweep/FINDINGS.md`, these belong to the known operator's June-2026 tradecraft stack (tunnel/probe + shortener + httpbun staging + jina + webhook.site dead-drop), three months before the Amap campaign. They are operator infra, not necessarily dead agents — but a June inbox receiving in October = a ghost cron worth flagging.

| Inbox UUID | Observed (UTC) | URL as observed | Campaign last-seen | Preliminary read |
|---|---|---|---|---|
| `6051dd2b-86dc-427d-8083-071a687af4f8` | 2026-06-21T19:46 | `?x=2` | 2026-07-07T02:41 (operator stack's newest below) | **LIKELY EXPIRED** — 106d old; free inboxes expire ~7d. If it still exists = notable. |
| `00f36f21-d00e-48b3-9456-8bf532e8c863` | 2026-06-22T01:58 | `?x=0` | same | **LIKELY EXPIRED** |
| `441b7745-1087-463e-b539-984a2ee3ea65` | 2026-06-24T10:09 | `?r=1782070800983511679` | same | **LIKELY EXPIRED** |
| `c1bf6b38-d6ea-4446-b17e-5f6c7a1cb357` | 2026-07-07T02:41 | `?r=1782071176301141190` | same | **LIKELY EXPIRED** — 89d old |
| `1eafadc3-9bb7-42d1-a9f0-0ced18cb6d56` | 2026-07-31T12:19 | bare | same | **LIKELY EXPIRED** |
| `35f6980c-7dc6-4af4-b646-56ca0070a200` | 2026-08-31T10:54 | bare | 2026-08-31 (single sighting) | **LIKELY EXPIRED** — 35d old |
| `c6aaa535-3b13-4b78-9ec8-cd0817a2f7a5` | 2026-08-08T12:30 | `?userId=<hex>&secret=<hex>&expire=2026-08-08T13:2…` (×4 variants) | 2026-08-08 (single sighting) | **NOT OURS** — callback URL embedded in a my.td.org-style flow (see ALL_LINKS.md:562); different actor/grammar. Excluded from ghost verdict. |
| `2ab7ca12-fdce-4475-8bf0-950c0cbf28f2` | 2026-08-08T12:25 (×2) | `/xss-osint-insert` | 2026-08-08 | **NOT OURS** — someone's XSS/OSINT test inbox, not agent exfil. Excluded. |
| `bee4dc9e-3935-451f-a724-b8c135763823.webhook.site` | 2026-08-08T12:24 | subdomain-style (old webhook.site format) | 2026-08-08 | **NOT OURS** — adjacent to the xss-osint test. Excluded. |

### C. urlscan-lane sweep noise (out of scope, recorded for completeness)

`raw/lanes/urlscan/q_domain_webhooksite.json` (100-result broad urlscan.io domain sweep) surfaced these additional UUIDs: `15c90e66-…` (`/undefined?otp=…` — GitHub Pages phishing kit), `577b82c3-…`, `0ef0dcf7-…`, `9dbf1485-…` (`/x.xml` — SSRF probe), `66ea3bbc-…`, `4fe5885c-…`, `db74eddf-…` (`/step6-uu`, `/bind-P1/P2/A` — exploit-test grammar), `127df518-…`, `5a230361-…` (`/ha-submit-test`), `5e4c7949-…`, `71f00be6-…`, `774cf5e1-…`, `9a9cdaf8-…`, `9c87649c-…`, `b10bd697-…`, `c618ea32-…`, `dd6e64a2-…`, plus literal `/abc`, `/abc123` test inboxes. These are a mix of phish-kit victims, SSRF scanners, and test inboxes — **not amap-fleet or known-operator agent dead-drops**. Not ghost-checked.

### Other tokens seen

- `webhook.site/#!/view/e691f66e-73c7-44ff-9d90-a79521173811` — a shared **view** token (not an inbox UUID) seen in `raw/lanes/chinese-infra/q_webhook.json`. View tokens render an inbox's request log publicly without the management UUID — a potential recovery path for the 14 missing inboxes if it points at one of them; unverifiable until egress returns.

## Ghost verdicts

| Inbox | Verdict |
|---|---|
| All of the above | **PENDING — live checks blocked by egress outage (2026-10-05 ~04:40–05:30 UTC).** Catalog and campaign last-seen are complete; no fabricated verdicts. |

**What a verdict looks like when the check runs** (per inbox): exists? → request count → newest request timestamp vs campaign last-seen above. Ghost = newest request timestamp strictly AFTER campaign last-seen (and after the 7-day natural-expiry window for the legacy set — any June/July inbox still receiving in October is a still-firing cron by definition).

## Recheck procedure (when egress returns)

1. Run `./recheck_deaddrops.sh` (in this directory). It probes, per inbox UUID:
   - `GET https://webhook.site/token/<uuid>` (frontend JSON endpoint — inbox metadata + request list)
   - `GET https://webhook.site/<uuid>` (HTML page; look for expiry/404 markers)
   and writes raw responses to `raw/deaddrop-probe-<YYYYMMDDTHHMM>.jsonl`.
2. Also resolve the view token: `https://webhook.site/#!/view/e691f66e-73c7-44ff-9d90-a79521173811` — needs a JS-capable (live) browser; a generic subagent cannot do this.
3. urlquery htmx sweep for new submissions (≤1 req/5s):
   `~/workspace/skills/urlquery/bin/uq_htmx.py search --query webhook.site --limit 30`
   then diff report IDs/URLs against this catalog — anything new, or any known inbox re-submitted after 2026-10-04, is a ghost lead. Also query per known UUID, e.g. `--query 6ddc559e`.
4. Ghost criterion: for the 3 fleet inboxes, any request timestamp after 2026-10-12 (fleet last-seen + 7d natural expiry) = still-firing cron. For legacy set, ANY existence = still-firing (they're 35–106 days past the ~7d free expiry).

## Open gaps (for parent)

- **14 fleet inboxes uncollected** (UUIDs unknown). If the egress outage persists, the only remaining recovery is the `e691f66e…` view token via a live browser, or re-derivation from urlquery report `97f0619b`'s rendered page (needs the live site).
- **No pushed changes.** Nothing committed or pushed from this sweep, per instructions.
