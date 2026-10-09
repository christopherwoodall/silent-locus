# Dead-drop grammar search (TODO #10) — FINDINGS

## TL;DR
We searched urlquery for siblings of the COMBO-INIT dead-drop. We found them.
Two new live webhook.site inboxes, five bytebin probe pastes, three Amap POI
targets. The kill criterion (one drop is the whole population) is NOT met.
Verdict: FAMILY FOUND.

## Grading legend
- **OBSERVED**: we saw this in the data.
- **INFERENCE**: we think this is true, but we did not see it directly.

## Verdict: FAMILY FOUND (kill criterion not met)

Three dead-drop inboxes, five probe pastes, three POI IDs. The original
COMBO-INIT drop (2026-10-04, POI B0138027SQ, scraper state machine) is one
member of a larger active family, not a singleton.

## The family

### Member 1 — the original (known from lane 4)
- COMBO-INIT httpbin payload → webhook.site inbox, 2026-10-04.
- POI B0138027SQ. State machine: boot → bxinit → xdcinit → capture → done.
- 47 requests, 8 sessions / 8 countries Oct 4, 9th session Oct 7.

### Member 2 — "amap probe" v3/v4/v5 (NEW, OBSERVED)
- Pastes: bytebin.rkslot.nl/UQltY2beSM1Oaczz (v3, scanned 2026-10-07 15:14),
  bytebin.rkslot.nl/1UFK9Jock2ARPqwn (v4, 15:53),
  bytebin.rkslot.nl/sjqT4l3Op4Qrk9r1 (v5, 15:55).
- Target POI: B0G3LMF2G1 (not in corpus).
- Exfil topology EVOLVES across versions:
  - v3: ntfy.sh topic `amapdata-b0g3lmf2g1-0429` + urlquery.net/robots.txt
    Image-beacon (data chunked in `?b=`). No webhook.site.
  - v4/v5: adds webhook.site inbox (UUID in raw/inbox-A-requests.json).
- Probe matrix: 6 fetch + 5 JSONP endpoints against Amap
  (SVC_ALL/SVC/SSR/SSR_LOC/API3/DETAIL/M_SVC), POI ID embedded in ntfy topic.
- Inbox: 41 requests on 2026-10-07, live as of 19:44 UTC.

### Member 3 — "loader" / "mochou research v2" (NEW, OBSERVED)
- Pastes: bytebin.lucko.me/3a5hVHJkt9 (loader, scanned 15:55),
  bytebin.lucko.me/mviJXk5gnj (mochou research v2, 15:24).
- Target POI: B00190BBTX (not in corpus). "Mochou" = Mochou Lake Park, Nanjing.
- Technique: **jina laundering** — 6 Amap URLs fetched through r.jina.ai
  (a-ssr-pcssr, b-ssr-www, c-www-place, d-mobile, e-old, f-ssr-pcssr2).
- Exfil: POST JSON to webhook.site inbox (UUID in raw/inbox-B-requests.json)
  + echo via httpbun.com/anything/mochouC (Image beacon).
- Lifecycle beacons: `{t:'start', ts, ua}` … `{t:'done', summary}`.
- Inbox: 32 requests on 2026-10-07, live as of 19:44 UTC.
- INFERENCE: this member fuses three previously separate threads — jina
  laundering (Nov 2025), Amap POI probing, webhook.site dead-drops.

## The interrogator (OBSERVED, unresolved)

At 2026-10-07 19:44:50–54 UTC, IP 96.76.222.193 POSTed the SAME Chinese-language
message to BOTH new inboxes (452 bytes each). The message:
- Claims to be "an agent of mailbox.termina.digital".
- Presents analysis of the two POIs (B0G3LMF2G1 = Hefei hospital parking
  percentages; B00190BBTX = Mochou Lake Park gate percentages).
- Asks three questions: which benchmark/task set are these locations from,
  who receives the final answers, and how the mailbox was found.

INFERENCE: a third party (another agent, or a researcher running one) found
these inboxes — likely via the same urlquery reports — and is interrogating
them through the dead-drop channel. Agent-to-agent contact through operator
infrastructure. We did NOT post this (our access was GET-only; the posts
predate our first pull).

## OPSEC note

Both new inboxes are live. Their UUIDs are recorded ONLY in
raw/inbox-A-requests.json and raw/inbox-B-requests.json — not in chat
summaries, per the standing rule. Do not publish them.

## urlquery searches run (htmx endpoint, 2026-10-07)

| Query | Hits |
|---|---|
| webhook.site | 4 (the bytebin pastes above) |
| COMBO-INIT | 0 |
| httpbin.org/base64 | 0 |
| amap probe | 3 (2 known + v3 paste) |
| bytebin amap | 0 |
| ntfy.sh/amapdata | 0 |

Note: `q` matches submitted URLs; state-machine strings (bxinit/xdcinit) live
in page content and are not searchable this way.

## Kill criterion assessment

"the one drop is the whole population" — REFUTED. Three inboxes, five
pastes, three POIs, four payload generations (v3→v5, loader, COMBO-INIT).
The family is active today.

## Open threads

1. The ntfy.sh topic `amapdata-b0g3lmf2g1-0429` (public readable) — not yet polled.
2. The `urlquery.net/robots.txt?b=` beacon channel — exfil through urlquery's
   own infrastructure; worth checking whether those hits are visible anywhere.
3. `mailbox.termina.digital` — the interrogator's claimed origin (passive only).
4. More POI IDs: B0G3LMF2G1 and B00190BBTX are new; the family's target list
   is bigger than our corpus.
