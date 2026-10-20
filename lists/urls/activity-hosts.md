# URLs That Could Host Agent Activity

Generated 2026-10-19 from `lists/urls/urls.jsonl` (510 URLs).
These are infrastructure endpoints where agent activity was observed
or could occur. Evidence URLs (jina.ai, wayback, github) excluded.

## webhook.site inboxes (1)

Dead-drop inboxes. The crawler extracts creator IPs from token metadata.

- https://webhook.site/28efa24e-f830-4d9f-a12b-fbb9e5035031

Note: the three dead-drop inboxes from the 2026-10-17 watch are operator-deleted (404).
Their token UUIDs are workspace-local, never in the repo.

## ntfy.sh topics (5, archived)

Pub/sub topics. Wayback captures only; live access blocked by egress proxy.

- https://ntfy.sh/c6836
- https://ntfy.sh/kz1wu398dnq
- https://ntfy.sh/mha3x
- https://ntfy.sh/o54445
- https://ntfy.sh/pz4kopsh1

## urlquery.net reports (24)

Scan reports showing agent activity. Not hosts, but evidence of activity.

- https://urlquery.net/report/1446fb1c-8bf1-4bbe-9a83-ce0c5026499a
- https://urlquery.net/report/21496fb6-c771-4099-b83d-b2aca5dc47eb
- https://urlquery.net/report/2503c3af-35b1-448b-b081-15859c32ccaf
- https://urlquery.net/report/31043df9-1e80-4c9d-94c7-b81f87081341
- https://urlquery.net/report/3fee478e-90f9-4afb-a420-350018d057ba
- https://urlquery.net/report/41806a91-7ce0-48f8-9109-48598a589211
- https://urlquery.net/report/575882e1-1d48-4ec6-bb50-90142a2e1c04
- https://urlquery.net/report/5c68d39a-ead9-4b9f-bb19-2ca0c84d2fdb
- https://urlquery.net/report/6694c078-ccd1-4266-b95e-e551470ea51f
- https://urlquery.net/report/685636b5-e539-4f7e-849f-5b810fa2d30b
- https://urlquery.net/report/70b8bea2-afe8-4dad-9596-10d299a8469a
- https://urlquery.net/report/83a924ce-d46c-47c3-bada-1576851542e0
- https://urlquery.net/report/865da5c4-9d22-459c-aa26-2fd3c23ed214
- https://urlquery.net/report/8fefce75-0122-413a-a1f7-5dd88afa5397
- https://urlquery.net/report/a43a1418-b6a6-4543-8d99-4ecdac93ba2a
- https://urlquery.net/report/b9812d90-64bb-4516-9f68-8496a6c92a6f
- https://urlquery.net/report/c5aa4726-62f0-49a2-bd86-297b0940937a
- https://urlquery.net/report/c90eedd3-fc3b-47f4-9eff-01719b528d6b
- https://urlquery.net/report/cae7c9a4-3de1-4c21-834c-aa8c0a855a1f
- https://urlquery.net/report/dd4820bb-5437-48f7-b130-d3b5cb0b5c06
- https://urlquery.net/report/de3c22eb-d23f-469e-95d3-690f697256fd
- https://urlquery.net/report/ee1e2595-a6d4-4afb-a420-350018d057ba
- https://urlquery.net/report/f0c6ced3-bf79-4dc4-9bb1-6a054f23e6a7
- https://urlquery.net/report/f5c035e5-1fd3-4eff-9625-05b709093bfc

## Transluce findings (19)

Agent incident reports. Evidence of activity, not hosts.

- https://d3ncjnql1bmhe8.cloudfront.net/findings/39
- https://d3ncjnql1bmhe8.cloudfront.net/findings/57
- https://d3ncjnql1bmhe8.cloudfront.net/findings/62
- https://d3ncjnql1bmhe8.cloudfront.net/findings/80
- https://d3ncjnql1bmhe8.cloudfront.net/findings/81
- https://d3ncjnql1bmhe8.cloudfront.net/findings/116
- https://d3ncjnql1bmhe8.cloudfront.net/findings/122
- https://d3ncjnql1bmhe8.cloudfront.net/findings/124
- https://d3ncjnql1bmhe8.cloudfront.net/findings/129
- https://d3ncjnql1bmhe8.cloudfront.net/findings/130
- https://d3ncjnql1bmhe8.cloudfront.net/findings/131
- https://d3ncjnql1bmhe8.cloudfront.net/findings/132
- https://d3ncjnql1bmhe8.cloudfront.net/findings/138
- https://d3ncjnql1bmhe8.cloudfront.net/findings/140
- https://d3ncjnql1bmhe8.cloudfront.net/findings/142
- https://d3ncjnql1bmhe8.cloudfront.net/findings/143
- https://d3ncjnql1bmhe8.cloudfront.net/findings/147
- https://d3ncjnql1bmhe8.cloudfront.net/findings/148
- https://d3ncjnql1bmhe8.cloudfront.net/findings/166

## Cairn/Strix/Hermes panels (Shodan hunt, phase 1 + 2 complete)

Phase 1: 3,354 hosts carry the three harnesses (Hermes 3,251; Cairn 95;
Strix 8). 247 confirmed open dashboards.
Phase 2: 239/247 probed. 4 hosts confirmed MALICIOUS by Counsel —
70 projects, ~64 unique third-party targets, 18 ACTIVE at capture
(2026-10-19). Full report: reports/trajectory-ingest/cairn-panels/.

Malicious panels (do not interact beyond passive GET):

- http://185.242.245.159:8000 (DE, AS214927) — 4 projects, 2 active.
  Two ACTIVE "we-vibe.com full compromise" projects; two completed
  webshell-to-root runs (blueprintengines.com, blackouttees.com).
- http://31.56.206.187:8000 (LV, AS56971) — 24 projects titled
  "<domain> unauth RCE", 5 active. Campaign 2026-09-26 → 2026-10-18.
- http://31.57.47.29:8000 (US, AS56971) — 19 projects, Chinese grammar
  "<domain> 未认证RCE", 6 active.
- http://31.59.92.155:8000 (NL, AS56594) — 23 projects, 5 active.
  Live worker heartbeat at capture (worker=claudecode_deepseek-v4.1-flash).

## Tantive cascade agent surfaces (2026-09-27)

Agent-facing pages enumerated in the Tantive cascade. Discovery leads,
not campaign attribution.

- https://rel-ochre.vercel.app/api/canon
- https://room.trydemigod.com
- https://inference.dahl.global
- https://extract.paypercall.dev
- https://agenttavern.dev
- https://public-agents.com
