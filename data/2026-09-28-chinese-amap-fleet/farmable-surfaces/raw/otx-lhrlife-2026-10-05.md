# OTX lhr.life deep pull — raw evidence (2026-10-05 ~05:00 UTC)

Method: OTX no-auth `GET /api/v1/indicators/domain/lhr.life/url_list?limit=50&page=N`
fetched via runtime browser-fetch fallback (VM direct egress down — proxy 407;
see FINDINGS.md). Pages 1–5 pulled = 2026-10-02 back to ~2026-06-22.
Page 5 is the last retrieved before OTX 429'd (rate-limit; hard stop per policy).

## Other-operator: /c/NN payload-distribution campaign (NOT our operator)
Host: `02e18ab88f2ece.lhr.life` — absent from our 78-subdomain fleet corpus.
Grammar: `/883120a1824c6dce00679806/c/NN-<12hex>/` and
`/883120a1824c6dce00679806/c/NN-<12hex>/downloads/payload-<12hex>.zip`
Slots NN = 01..20 (all twenty observed). ~60+ URLs in 63 seconds,
2026-08-16T10:20:48Z–10:21:51Z. Per-slot payload zips = campaign/panel
serving per-build artifacts. Reads as malware/RAT payload staging or a
red-team C2 panel, NOT agent-swarm behavior — logged as other-operator lead.
Sample URLs:
- `https://02e18ab88f2ece.lhr.life/883120a1824c6dce00679806/c/01-95f221eb28ff/downloads/payload-c930beecb81cf62e5e17.zip`
- `https://02e18ab88f2ece.lhr.life/883120a1824c6dce00679806/c/20-0bb7e7c03b3d/`

## /c + /r tunnel family (shared toolkit convention, NOT our operator)
- `https://b6c89c319da971.lhr.life/c` — 2026-09-30T14:15:24Z
- `https://a329f5f3e67568.lhr.life/c` — 2026-08-30T01:26:59Z
- `https://a329f5f3e67568.lhr.life/r` — 2026-08-30T01:26:05Z (54s before /c)
Same `/c`, `/r` endpoint convention across tunnels a month apart → shared
tool or same operator family. Neither host in our fleet corpus.

## Agent-server surface exposed via tunnel (NOT our operator)
Host `48e0cb905290ad.lhr.life` — absent from our fleet corpus:
- `/agents.json` — 2026-08-24T07:47:54Z
- `/llms.txt` — 2026-08-24T07:47:43Z
- `/openapi.yaml` — 2026-08-24T07:47:32Z
Three agent-framework discovery/API-spec files within 22 seconds = an agent
server's API exposed through a localhost.run tunnel. Agent infrastructure,
not necessarily malicious. Worth watching for recurrence.

## API-surface recon (unknown actor)
Host `2580d75923f5e1.lhr.life` — not in our fleet:
- `/api/changelog` — 2026-08-16T14:19:48Z
- `/api/manifest` — 2026-08-16T14:19:41Z (7s apart)

## Phishing-shaped tunnels (various actors, not ours)
- `9016ab811b4c55.lhr.life/login.html.php` — 2026-09-28 and 2026-08-06
- `fba273774a5210.lhr.life/login.html` — 2026-08-15
- `12c8d35fd1acad.lhr.life/login.html` — 2026-08-02
- `cb7c3eaf86e74c.lhr.life/login` — 2026-07-23
- `cb56d587e48d89.lhr.life/PRICE_CALCULATOR.html` — 2026-07-26

## OUR operator cross-surface confirmations
1. `c2679a7c8e852b.lhr.life/login.html` — OTX 2026-06-25T15:14:32Z.
   Our corpus: urlquery report 63692518-acdc-432c-8303-328e3ccfab77,
   2026-06-25T10:54:00Z, same URL. Independent confirmation that our
   operator's tunnel served a login page — phishing-shaped payload inside
   the Amap-scraping fleet's infrastructure.
2. `www.820eea12fec476.lhr.life/` — OTX 2026-09-09T10:58:32Z (prior overlap #2,
   re-confirmed on page 1 this run).

## Third-party fuzzing against OUR operator tunnel
Host `a35c2e7d29722e.lhr.life` — IN our 78-subdomain fleet corpus (one urlquery
report: `/runo-`, 2026-06-22T03:46:00Z, report 013e27aa-1436-49d9-9eb2-8a304be62a6d).
OTX shows ~30 short garbage paths against the same host over 2026-06-22–25:
`/~H`, `/ll`, `/;.EXI`, `/no`, `/esult`, `/D`, `/resultexe`, `/uno-`,
`/resultH`, `/H`, `/dlldH`, `/dll`, `/7UsF`, `/resultp`, `/llq`, `/result=`,
`/oH`, `/-`, `/result`, `/CH`, `/resultk`, `/result$6`, `/%`, `/l`, `/m~`,
`/pH`, `/dows`, `/aH`, `/resultU`, `/(H` …
Burst pattern = automated path fuzzer enumerating endpoints against the live
operator tunnel during its active window. Attribution unknown (third-party
scanner vs operator's own testing); logged as observed behavior, not conclusion.
Sibling host `2d5f8eb0b18e42.lhr.life` (NOT in our fleet) shows the same fuzz
pattern (`/dll`, `/resultP`, `/result`, `/llz`, `/llw`, `/f`, `/result6`,
`/dllH`, `/e`, `/4`, `/l`, `/q`, `/ll`, `/resultxt` — 2026-06-22T08:44,
~40 seconds) → same fuzzer hit multiple tunnels.

## OTX zeros
- `pingllo.com` url_list: empty (0 URLs). Operator's June CORS proxy has no OTX footprint.
- `urlcap.com` url_list: empty (0 URLs).
- OTX `passive_dns` for `c2679a7c8e852b.lhr.life`: HTTP 429 — rate-limited;
  OTX polling hard-stopped for this run per policy.

## Infra notes
- Every OTX urlworker hit on these tunnels returned http_code 503 (dead
  tunnels) except a few http_code 0 (no route). Tunnels are ephemeral as expected.
- OTX urlworker egress IPs seen: 3.208.46.244, 54.172.225.3, 3.234.18.192
  (all AWS; OTX's workers, not operator infra).
- SafeBrowsing matches: [] across all entries. 0 pulses on overlap subdomains.
