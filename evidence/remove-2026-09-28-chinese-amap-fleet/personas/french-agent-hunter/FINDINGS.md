# FRENCH AGENT HUNTER — FINDINGS

**Persona:** foreign-agent hunt — find AGENT-shaped activity in French surfaces. Agents, not operators.
**Date:** 2026-10-05. Egress UP (urlquery 200, urlscan API working).
**Prior work consulted first:** `french-hunt/FINDINGS.md` + `FINDINGS2.md` (two thorough prior hunts, both honest zeros on urlquery). This pass does NOT redo them — it covers only new angles: local-corpus verification, urlscan.io (unused by prior hunts), OVH/Scaleway infra, and the staged-but-unrun time-blast.

## Verdict: no French agent fleet found — the French zero stands, now cross-checked on urlscan

## 1. Local-corpus verification (all three sets)

- `2026-09-28-chinese-amap-fleet/events.jsonl` (2,141): **zero** `gouv.fr` / `gov.fr` hits.
- `2026-10-03-openai-agent-traces/events.jsonl` (589,972): **zero**.
- `2026-10-01-oai-tag-sweep/events.jsonl`: 5 `.fr/` substring hits — all FALSE POSITIVES: Telegram invite-link path fragments (`fr/tr/cl/HHqrQTyUh83MwbbDe9QncDgy8EQMYj5Lyr-ZLfVVUNBqDmPzc_...`), not French targets.

Our fleets do not touch French government domains.

## 2. urlscan.io — French government surface (new surface for this hunt)

### 2a. `service-public.fr` phishing-kit cluster (NEW, programmatic, NOT an agent fleet)

21 scans, 2026-09-19 → 2026-10-02, against `sp-bas-magenta.pic-sp.service-public.fr`:
- Subdomains: `m.vosdroits`, `acte-naissance`, `interactif`, `api`, `entreprendre`, `mon`, `www.entreprendre.gouv`
- Timing: paired submissions ~1 second apart (e.g. 2026-09-30 19:45:50.181Z + 19:45:51.911Z) — scripted submission
- Target IP: 146.183.11.145, country FR, tiny 214-byte pages
- `r.at.entreprises.service-public.fr`: 2 scans 2 seconds apart, 2026-09-27, Cloudflare IPs 104.17.155.243/104.17.156.243

Verdict: a French phishing kit impersonating service-public.fr (birth certificates, citizen rights, business creation) being programmatically submitted to urlscan — either a security vendor's phishing-feed auto-submitter or the phisher testing their own kit. Cybercrime infra being scanned, not an agent operating. Agents and swarms only — this is human cybercrime, filed as context, not a find.

### 2b. `gouv.fr` overall: 401 results — ordinary government browsing

Top domains: `sondage.apps.education.fr` (6), `livekit-24/38.prd.beta.numerique.gouv.fr` (4+3), `www.service-public.gouv.fr`, `www.impots.gouv.fr`, `www.education.gouv.fr`. No bursts, no markers, no enumeration grammar.

Notables:
- `livekit-*.prd.beta.numerique.gouv.fr` (4 scans, Sep 27–Oct 4): LiveKit WebRTC infra on the French digital-services beta domain. Scans don't resolve IPs, plain HTTP, bare-hostname titles. Sparse recon-ish probing — thin, not agent-shaped.
- `beta-gouv-fr.pages.dev` (2 scans, Sep 8 / Oct 4): Cloudflare Pages deployment mirroring beta.gouv.fr's "Incubateur de services publics numériques" title. Legit deploy preview or phishing clone — unconfirmed, worth one look.
- `sondage.apps.education.fr` (34 scans): individual `/poll/answer/<id>?type=MEETING` links scanned one at a time over days — humans sharing survey links. Not agent-shaped.

### 2c. Wildcard `*.gouv.fr` on urlscan: unsupported syntax (total: null) — not a negative, tool limitation.

## 3. OVH / Scaleway (French native infra)

- `url.domain:ovh.com` (urlquery htmx): 5 hits — `ovh.com` / `www.ovh.com` homepage scans (2024-07 → 2026-05), one IPFS mirror mentioning `simon.lecroard@ovh.com`. All ordinary. Zero agent-shaped.
- `url.domain:scaleway.com`: 0 hits (empty result set).

## 4. Time-blast on `data.gouv.fr` — BLOCKED, not completed

The staged follow-up from FINDINGS2 (histogram the 19 data.gouv.fr reports by hour/day, flag >10/hr or >30/day bursts) could not run: the htmx query `url.domain:data.gouv.fr` fails with `IncompleteRead` on two attempts — transport failure on this query, not evidence of absence. **Highest-value remaining open item.** Retry on a calm window.

## 5. Interpretation

1. **No French Amap-equivalent on either surface.** urlquery (two prior hunts) and now urlscan both show zero systematic French place/API/gov scanning. Either no French-language agent fleet exists, or it uses infrastructure invisible to both scanners.
2. **French gov's urlscan footprint is ordinary browsing + phishing victims.** The only programmatic cluster is the service-public.fr phishing kit being submitted — cybercrime, not agents.
3. **French open-data APIs remain pristine** (prior hunt) and our three corpora contain zero French gov touches (this hunt).
4. The hunt-for-French-agents playbook that would still work: French *task* markers (French place names in program titles, `uq*`-style tag grammars) rather than French *infrastructure* — agents optimize for no-login Western services regardless of origin.

## Open follow-ups

1. Retry `url.domain:data.gouv.fr` htmx time-blast (IncompleteRead ×2).
2. One look at `beta-gouv-fr.pages.dev` — legit preview or phishing clone.
3. German and Russian lanes remain open per the user's direction.

Nothing pushed, per instructions.

## All observed URLs

### urlscan phishing-kit cluster
- http://m.vosdroits.sp-bas-magenta.pic-sp.service-public.fr/
- http://acte-naissance.sp-bas-magenta.pic-sp.service-public.fr/
- http://interactif.sp-bas-magenta.pic-sp.service-public.fr/
- http://api.sp-bas-magenta.pic-sp.service-public.fr/
- http://entreprendre.sp-bas-magenta.pic-sp.service-public.fr/
- http://www.entreprendre.gouv.sp-bas-magenta.pic-sp.service-public.fr/
- http://mon.sp-bas-magenta.pic-sp.service-public.fr/
- http://www.sp-bas-magenta.pic-sp.service-public.fr/
- http://sp-bas-magenta.pic-sp.service-public.fr/
- https://r.at.entreprises.service-public.fr/

### urlscan gouv.fr notables
- http://livekit-24.prd.beta.numerique.gouv.fr/
- http://livekit-38.prd.beta.numerique.gouv.fr/ (4+3 scans)
- https://beta-gouv-fr.pages.dev/
- https://sondage.apps.education.fr/poll/answer/gHY6nnZ8v2wA2pE49?type=POLL
- https://sondage.apps.education.fr/poll/answer/4ab9fpGubZne7sQA5?type=MEETING

### urlquery htmx (OVH)
- https://urlquery.net/report/e2c2ba91-fa82-47b9-9c66-d6da4bd6d765 (ovh.com, 2026-05-02)
- https://urlquery.net/report/03c66445-3037-4fd9-b0c4-0fe0567db3f2 (www.ovh.com, 2026-03-25)
- https://urlquery.net/report/6786d542-11c8-4297-b082-5f1d3034eccc (ovh.com, 2025-05-29)
- https://urlquery.net/report/8af2b3bd-d7a3-412d-a10b-ed348f3a771a (www.ovh.com, 2024-07-01)

### urlscan API queries used
- https://urlscan.io/api/v1/search/?q=domain%3Aservice-public.fr&size=50
- https://urlscan.io/api/v1/search/?q=domain%3Asp-bas-magenta.pic-sp.service-public.fr&size=100
- https://urlscan.io/api/v1/search/?q=domain%3Ar.at.entreprises.service-public.fr&size=50
- https://urlscan.io/api/v1/search/?q=domain%3Agouv.fr&size=100
- https://urlscan.io/api/v1/search/?q=domain%3Alivekit-24.prd.beta.numerique.gouv.fr&size=20
- https://urlscan.io/api/v1/search/?q=domain%3Abeta-gouv-fr.pages.dev&size=20
- https://urlscan.io/api/v1/search/?q=domain%3Asondage.apps.education.fr&size=20
