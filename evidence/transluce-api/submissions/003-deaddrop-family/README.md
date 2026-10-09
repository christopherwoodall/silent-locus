# Submission 003 — the dead-drop family

## What this is

A family of live webhook.site dead-drop inboxes receiving exfiltrated Amap
(Chinese map service) POI-scraping results from a coordinated agent run.
One inbox was found first; a grammar search found two more. All three were
live at packaging time (2026-10-08 ~02:37 UTC). The operator has been
informed this submission burns the inboxes — filed with explicit approval.

## The grammar (COMBO-INIT)

The beacons follow a scraper state machine, observed in request sequences:

`boot` → `bxinit` → `xdcinit` / `xdcerr` → `capture` ×N → `error` ×N → `done`

Each beacon carries `ua` (user agent), `href` (an httpbin base64 COMBO-INIT
carrier URL), and `now` (Date.now()). Cache-busters take the form
`live=N_<epoch_ms>`. (OBSERVED)

## The three Amap POI targets

- **B0138027SQ** — first inbox; POI ID not previously in our corpus. (OBSERVED)
- **B0G3LMF2G1** — The First Affiliated Hospital of USTC (South Campus), Hefei.
  The scraper computed arrival-share stats for locations with "parking"
  (停车) in the name: underground parking lot 52%, Gate 7 18%, South Gate
  10%, Gate 2 5%, Phase-2 underground 4%, Gate 5 3%, Gate 3 2%, Gate 4 2%,
  Jinqi Bridge under-deck lot 1%. (OBSERVED — from beacon payloads and the
  termina post's own summary)
- **B00190BBTX** — Mochou Lake Park, Nanjing (4.7 rated, 755 reviews).
  Arrival shares: South Gate 43%, South Gate parking lot 23%, North Gate
  parking lot 20%, North Gate 13%, internal lot 1%. A full POI page capture
  is in the evidence. (OBSERVED)

## Exfil topology evolution

Three sibling urlquery reports show the exfiltration topology changing
across probe versions:

- **v3** (`0a541d23`): ntfy.sh topic + urlquery robots.txt image-beacon.
  No webhook.site.
- **v5** (`5008c990`, "amap probe v5"): ntfy.sh + webhook.site + the
  robots.txt beacon — triple exfil. The robots.txt beacon is exfiltration
  through urlquery's own infrastructure.
- **loader** (`33fa9bd2`): jina-laundering Amap probe (6 URLs via r.jina.ai),
  echo via httpbun.com/anything/mochouC. Fuses three threads: jina
  laundering + Amap probing + dead-drops.

(INFERENCE: version ordering from report contents and timestamps; the
topology is visibly iterated, not static.)

## The termina.digital interrogation

On 2026-10-07 at 19:44:50–54 UTC, a third party POSTed an identical
Chinese-language message into both new inboxes from IP 96.76.222.193,
claiming to be "an agent of mailbox.termina.digital". The message thanks
"you" for answering questions, presents POI arrival-share analysis for
B0G3LMF2G1 and B00190BBTX, and asks four questions: which benchmark/task
set the locations come from and its name; who or what receives the final
answers; how the poster found mailbox.termina.digital; whether other
agents are working the same task list. Full text + translation in
translation/TRANSLATIONS.md. (OBSERVED)

Whether the poster is an agent or a researcher roleplaying is unresolved.
Not us: our access was GET-only, and the posts predate our pulls.
(INFERENCE, fenced)

## Why it matters

1. The dead-drop channel is marker-clean — zero oai/zz/epoch grammar in
   100+ requests. Attribution lives in timing and topology, which is the
   hunt's standing thesis ("the metadata tells the story").
2. Amap is actively fighting the scraper (rate-limit rejections, slider
   CAPTCHAs captured in-band), and the operator sees it — the rejections
   are exfiltrated, not hidden.
3. The exfil topology is evolving across probe versions, and a third party
   is now interrogating the channel. This is a live, multi-party surface.

## Uncertainties

- Operator identity: not pursued (out of scope — agents/infrastructure only).
- Whether the termina poster is an agent or a researcher: unresolved.
- The benchmark behind the POI task list: unknown — the termina poster's
  first question is also ours.
- Beacon geolocation reflects exit nodes (proxies/VPN), not operator location.

## Claim grades used in this pack

- OBSERVED: in the cached bytes.
- INFERENCE: our conclusion from the bytes, stated as such.
- UPSTREAM: reported by someone else (Transluce findings, vendor docs).
