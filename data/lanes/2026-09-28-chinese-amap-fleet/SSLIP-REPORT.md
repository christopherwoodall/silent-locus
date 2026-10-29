# sslip.io — observation report

Date: 2026-10-05. Source: urlquery hunt corpus + infra watchlist (update 3).

## What it is

sslip.io is a wildcard-DNS service: `178-63-67-153.sslip.io` resolves to
`178.63.67.153` (Hetzner). The operator used wildcard-DNS hostnames as
exfil/beacon receivers instead of raw IPs — the same role lhr.life tunnels
and webhook.site inboxes play in this operation's dead-drop grammar.

## The June-21 burst — direct observations

All four submitted to urlquery.net on 2026-06-21, inside the Tableau beacon
wave window (19:20–19:51 UTC):

| # | Observation | Time (UTC) | Submitted URL |
|---|---|---|---|
| 1 | https://urlquery.net/report/c7e56e55-869d-4c34-89a8-4ae1699dedfa | 2026-06-21 19:20 | `178-63-67-153.sslip.io/f5c8fe9a-b4db-4261-85a6-539d7a18d5b0` |
| 2 | https://urlquery.net/report/6a90f4a0-d096-42eb-9155-0d5e7cb51ed1 | 2026-06-21 19:41 | `178-63-67-153.sslip.io/a29f29eb-98e5-46b1-a6c6-e3aff643e54c?v=6089` |
| 3 | https://urlquery.net/report/9d42caec-2c11-4271-9350-b0957a6e65fd | 2026-06-21 19:41 | `178-63-67-153.sslip.io/5a831ee4-6b1a-478d-b5f4-9d73acabd750?v=8766` |
| 4 | https://urlquery.net/report/ebe1fe1b-9c59-4916-b50d-9087012b78ec | 2026-06-21 19:51 | `178-63-67-153.sslip.io/f5c8fe9a-b4db-4261-85a6-539d7a18d5b0?retry=3` |

Further UUID paths from the hunt-7 staging set (same host, same day):

- `178-63-67-153.sslip.io/6eef12c0-3a07-48ab-80e6-48b046bcad45?v=27234`
- `178-63-67-153.sslip.io/1fab05d4-2240-4a10-b852-b9a4de6d6c14?v=19655`
- `178-63-67-153.sslip.io/f5c8fe9a-b4db-4261-85a6-539d7a18d5b0?pre=1`

## Beacon protocol (observed)

Query-string grammar on UUID-pathed receivers:

- `?retry=3` — retry counter on the `f5c8fe9a` UUID (seen bare at 19:20, then
  `?retry=3` at 19:51 — client-side retry of the same beacon)
- `?v=<number>` — version/nonce per beacon (`v=6089`, `v=8766`, `v=27234`,
  `v=19655`)
- `?x=0`, `?x=1` (×2), `?x=2` — indexed beacon slots in the corpus
- `?pre=1` — pre-flight/probe variant

## IOC rows (hunt dataset)

- `sslip.io` — domain, 7 rows, 2026-06-21:
  https://urlquery.net/report/ebe1fe1b-9c59-4916-b50d-9087012b78ec
  "[hunt-round7-verify] sslip.io dynamic-DNS session pages
  (178-63-67-153.sslip.io/\<uuid\>?v=...): agent session/beacon infra
  adjacent to the June-21 Tableau beacon wave"
- `178-128-196-79.sslip.io` — ThreatFox botnet_cc win.cobalt_strike
  (conf 75, first 2026-09-24):
  https://threatfox.abuse.ch/ioc/1932288/
- `193-233-82-248.sslip.io` — ThreatFox payload_delivery js.clearfake
  (conf 100, first 2026-08-04):
  https://threatfox.abuse.ch/ioc/1868293/

## Graph relations

- `sslip.io --used_in--> AIHW Tableau PBS-dashboard extraction`
  "Rotating-subdomain beacon host (combo.html/probe) referencing the PBS
  dashboard" — https://urlquery.net/report/ebe1fe1b-9c59-4916-b50d-9087012b78ec
- `sslip.io tenants -> Cobalt Strike / ClearFake (ThreatFox)
  --shared_platform--> AIHW Tableau PBS-dashboard extraction`
  Platform overlap at tenant granularity — NOT a family tie:
  https://threatfox.abuse.ch/ioc/1932288/

## Assessment

OBSERVED: on 2026-06-21 the operator ran UUID-pathed beacons against a
wildcard-DNS hostname fronting 178.63.67.153, with a client-side retry
protocol, adjacent to the Tableau beacon wave. The same platform hosts
unrelated commodity tenants (Cobalt Strike, ClearFake) — shared
infrastructure, not shared operations.

INFERENCE: sslip.io was the operator's IP-masking layer for beacon
receivers — cheaper and less conspicuous than a fresh tunnel domain per
campaign, and it keeps working after webhook.site inboxes expire. The
standing sweep rule is now: `sslip.io`/`nip.io` UUID-pathed URLs alongside
webhook.site in every run.

## Watchlist status

Added 2026-10-05 (update 3) to
`data/2026-09-28-chinese-amap-fleet/infra-watchlist/INFRASTRUCTURE-WATCHLIST.md`:
`178-63-67-153.sslip.io` and `sslip.io` under Dead-drops/exfil (OUR FLEET);
`nip.io` as PREDICTED sweep guidance (not observed).

## Addendum — further sslip.io sightings (2026-10-05 sweep)

1. **Agent-relay on `relay.*.sslip.io` — GENUINELY NEW, agent-shaped.**
   Shodan stored observation, indexed 2026-10-05: `46.225.88.73` (Hetzner),
   port 443 titled "Agent Relay", `.codex/sessions` in the page HTML
   (possible transcript/session viewer); port 8081 on the same host titled
   "Droidrun — The AI Mobile Automation Framework". The `relay.*.sslip.io`
   hostname suggests an agent-relay service fronted by wildcard DNS.
   Source: `studies/shodan-chat-transcripts/FINDINGS.md` row 1.
   (INFERENCE, unverified — no live fetch per OPSEC.)

2. **Translate-laundered sslip.io page.** oai-tag-sweep corpus:
   `sslip-io.translate.goog/w939h.html?_x_tr_sl=auto&_x_tr_tl=en` — a Google
   Translate proxy of an sslip.io page. Same laundering pattern previously
   seen on httpbun (`httpbun-com.translate.goog/base64/`).

3. **EUROSWARM infra-tracker read:** `178-63-67-153.sslip.io` is a
   webhook.site application server — i.e. the June-21 exfil went to a public
   webhook dead-drop service hosted on Hetzner, consistent with the known
   webhook dead-drop tradecraft (not an agent-operator host).
