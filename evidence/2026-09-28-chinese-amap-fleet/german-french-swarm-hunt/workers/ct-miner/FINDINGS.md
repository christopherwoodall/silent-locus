# CT-MINER — crt.sh German/French agent-worded subdomain hunt

**Worker:** ct-miner (EUROSWARM wave 1) · **Date:** 2026-10-05 · **Analyst:** subagent session 6df3eaa3
**Mission angle:** German/French-WORDED subdomains carrying agent markers (dashboards, wikis,
harnesses, API servers, MCP endpoints). Distinct from the `farmable-surfaces` lane, which
established the known operator mints no certs (uqprobe/uqscan/sub_poi/httpbun = zero certs).

## Method (OBSERVED)
- crt.sh JSON API only: `https://crt.sh/?q=%25<keyword>%25&output=json` (+`&exclude=expired`
  where noted). Passive CT-log reads; **no candidate infrastructure was fetched or probed**,
  per hard rules. Scope kept to agents/swarms — no registrant/identity pursuit.
- Polite pacing: 2s sleep between requests; up to 4 retries with 5–10s backoff on crt.sh
  502/404 flaps (crt.sh returned multiple transient 502 Bad Gateway / 404 on 2026-10-05).
- Local filtering (`analyze.py`, this dir): crt.sh `q` matches against ALL certificate identities,
  **including subject-DN fields** (street addresses, org names), not just DNS names. Every count
  below is after restricting to DNS-shaped identities (labels/dots/`*.` only). Raw JSON kept in
  `raw/`; per-query analysis JSON in `analysis_<kw>.json`. Full observed values kept everywhere —
  nothing redacted.
- Agent-grammar screen on DNS identities: `oai`, `zz=`/`zz_`, `httpbun`, `uqprobe`, `uqscan`,
  `sub_poi`, `harness`, `mcp`, `board`, `wiki`, `dashboard`, `ki-`, `fleet`, `worker`, `node-`,
  `agent-`, `bot-`, `swarm`/`schwarm`/`essaim`, `aufgabe`/`tache`, `probe`, `relay`, `tunnel`,
  `webhook`; plus numbered-fleet regex and epoch-nonce regex (13+ digit labels).
- TLD buckets: DE = .de/.at/.ch, FR = .fr/.be/.lu.

## Limitation (carried from recon lane)
Agent tunnels hide behind wildcard certs and are CT-invisible. This lane therefore covers only
non-tunnel agent infra that would still mint visible certs. A zero here does not prove absence of
a swarm living entirely behind wildcards.

## Query log (OBSERVED)
| # | query | crt.sh result | certs | unique DNS idents |
|---|-------|--------------|-------|-------------------|
| 1 | `aufgabe` | ok (3 attempts) | 9 | 1 |
| 2 | `schwarm` | ok | 23 | 4 |
| 3 | `ki-agent` | `[]` (after 502 flaps) | 0 | 0 |
| 4 | `essaim` | `[]` | 0 | 0 |
| 5 | `tache` | ok | 11 | 0 — all subject-DN false positives |
| 6 | `werkzeug` | ok (3 attempts) | 193 | 39 |
| 7 | `forschung` | ok | 9,614 | 56 |
| 8 | `recherche` | ok (3 attempts) | 9,432 | 73 |
| 9 | `mission` | ok (2 attempts) | 6,854 | 557 |
| 10 | `outil` (+exclude=expired; 3 attempts) | ok | 2 | 1 |
| 11 | `harness` | ok | 648 | 92 |
| 12 | `mcp` | ok (2 attempts) | 6,462 | 217 |
| 13 | `oai` (+exclude=expired; 4 attempts) | ok | 114 | 28 |
| 14 | `zz=` | **502 ×4 — unresolved server-side** (see O1) | — | — |
| 15 | `uqprobe` / `uqscan` / `sub_poi` / `httpbun` | `[]` ×4 | 0 | 0 |
| 16 | `agent` (+exclude=expired) | ok | 533 | 418 |
| 17 | `bot` (+exclude=expired; 2 attempts) | ok | 4,614 | 3,109 |
| 18 | `daten` (+exclude=expired) | ok | 48 | 6 |
| 19 | `robot` (+exclude=expired; 2 attempts) | ok | 37 | 30 |

Cross-set composite: 4,629 unique DNS identities scanned for `zz=`/`zz_` (zero hits) and for
DE/FR-word × agent-grammar co-occurrence (4 hits, all Mission Federal Credit Union false positives —
`admin-onlinebanking.missionfed.com`, `cardwizapi.missionfcu.org`, `cardwizardapi.missionfcu.org`,
`theboardroom.missionfed.com`).

## Graded findings

### HONEST NEGATIVE — German-worded agent infra
- **N1 `aufgabe`:** 9 certs. Single DNS identity:
  `welche-aufgabe-hat-der-blinddarm--769930729.helpclean.de` (quiz article slug — "what is the
  appendix's function", helpclean.de). Remainder are T-Systems subject-DN fields
  ("Abteilung1: Zentrale Aufgabe"). No agent markers.
- **N2 `schwarm`:** 23 certs, 4 DNS: `remote.wolf-schwarm.de`, `www.remote.wolf-schwarm.de`
  (Wolf Schwarm IT UG — IT company, person-name match), plus
  `schaetzing-der-schwarm--346369.erfolgerfolg.de` (+www) — Frank Schätzing's novel
  "Der Schwarm", article slug. No agent markers.
- **N3 `ki-agent`:** zero certs (`[]`).
- **N6 `werkzeug`:** 193 certs, 39 DNS — tool retailers (`werkzeug-eylert.de`,
  `shop.werkzeugweber.de`, `werkzeugmobil.de`, `leihdirwerkzeug.de`) and SEO article-slug
  subdomains (`*-werkzeug-set--<digits>.*.de` on borsan.de/wingforum.de/helpclean.de etc.;
  company DN fields are tool manufacturers). No agent markers.
- **N7 `forschung`:** 9,614 certs, 56 DNS — German/Austrian research institutions only:
  DFN, Max-Planck-Gesellschaft, Charité, BMBF (`forschung.bmbf.bund.de`),
  kmuforschung.ac.at (incl. confluence/matomo/mattermost/nextcloud subdomains — ordinary
  institutional tooling). Top issuer GEANT (6,836). No agent markers.
- **N12 `daten`:** 48 certs, 6 DNS. The 2 DE identities are spec-sheet article slugs:
  `audi-q3-sportback-technische-daten--40110997.scienceandfaith.de`,
  `dyson-v6-technische-daten--92237888.forum-rettungsdienst.de`. No agent markers.

### HONEST NEGATIVE — French-worded agent infra
- **N4 `essaim`:** zero certs (`[]`).
- **N5 `tache`:** 11 certs, **zero** DNS identities — every match is a subject-DN field:
  "Tache USA Inc.", "350, boulevard Tache Ouest", "379 boul Alexandre Tache",
  "Str. TACHE IONESCU 8A București". Textbook crt.sh non-DNS false positive.
- **N8 `recherche`:** 9,432 certs, 73 DNS — French public research only: CNRS, INRA
  (`infrastructure-recherche.inra.fr`), Institut Curie (`activesyncs01-05`,
  `autodiscover01-05`, `mbxparis01-05`, `dag1-5`, `webmail01-03.recherche.curie.fr` —
  numbered but explainable corporate Exchange fleets), `*.recherche.gouv.fr`,
  `enseignementsup-recherche.gouv.fr`. Top issuer TERENA (6,733). No agent markers.
- **N9 `mission`:** 6,854 certs, 557 DNS — mission orgs + credit unions; DE hits
  `mission-leben.de`, `mission-one.de`, `permission-one.de`, `engadinmission.ch`. Sole
  grammar hit "board" = `theboardroom.missionfed.com` (false positive). Zero FR-TLD DNS.
  No agent markers.
- **N10 `outil`:** 2 certs (valid only), 1 DNS:
  `creer-un-outil-pour-prendre--gcg4b.useaivia.com` (Let's Encrypt, 2026-08-12 — French
  article slug "create a tool for taking"). No agent markers.
- **N14 `robot`:** 37 certs, 30 DNS. Sole FR identity: `*.robot-coupe.fr` (+ apex) —
  Robot Coupe, French commercial food-processor manufacturer. No agent markers.

### HONEST NEGATIVE — shared words (agent/bot), DE/FR TLD slice
- **N11 `agent`:** 533 certs (valid only), 418 DNS. DE-TLD: **0**. FR-TLD: 2 —
  `*.agentco.fr`, `agentco.fr` (French company "AgentCo", not infra). Numbered fleets present
  but English-lane (see L2). No DE/FR-worded agent infra.
- **N13 `bot`:** 4,614 certs (valid only), 3,109 DNS. DE/FR-TLD: **0**. Grammar hits all
  English-lane (see L5). No DE/FR-worded agent infra.
- **N15 campaign markers:** `uqprobe`, `uqscan`, `sub_poi`, `httpbun` all `[]` — confirms the
  farmable-surfaces lane's finding that the known operator mints no certs.

### LEAD — agent-shaped infra found, NOT DE/FR-worded (cross-lane, for coordinator)
These carry agent grammar (numbered fleets, oai tags, harness/MCP naming) but **no German or
French words** — logged, not probed, for other lanes:
- **L1 `task-oai-<NNN>` numbered fleet (Northflank).** Wildcard SANs on Let's Encrypt certs,
  one deployment suffix `--cvcq98f42btp`, `addon.code.run`:
  `*.task-oai-103-analytics-db--cvcq98f42btp.addon.code.run`,
  `*.task-oai-143-{analytics-db,jisr-db,redis}--cvcq98f42btp.addon.code.run`,
  `*.task-oai-261-{jisr-db,redis}--…`, `*.task-oai-263-{jisr-db,redis}--…`,
  `*.task-oai-267-{jisr-db,redis}--…`, `*.task-oai-346-{jisr-db,redis}--…`,
  `*.task-oai-377-{jisr-db,redis}--…`, plus `*.feature-oai-1-{analytics-db,jisr-db,redis}--…`,
  `*.feature-oai-228-{jisr-db,redis}--…`, `*.fin-8366-oai-phase2-{jisr-db,redis}--…`,
  `*.oai-1-phase-1-{analytics-db,jisr-db,redis}--…`. Certs minted 2026-09-03 → 2026-09-17
  (recent, active window). INFERENCE: `task-oai-NNN` parallels the corpus `zz=oai<digits>`
  grammar (oai + task numbering) but is a different formulation — possibly a related or
  convergent operator. Flag for cryptographer lane (oai-tag family).
- **L2 `hermes-agent--<NNN>.shadowmoon.vip` numbered fleet.** 7 certs: `hermes-agent--130`,
  `--159`, `--191`, `--192`, `--193`, `--1998`, `--joyyard`. All minted 2026-07-18 within
  ~70 minutes (14:44–15:54 UTC), Let's Encrypt, expiring 2026-10-16. INFERENCE: burst-minted
  numbered agent fleet. No DE/FR markers; no attribution attempted (out of scope).
- **L3 harness-shaped (English).** `*.codexai-harness-har-db--t99qf47qvqv2.dnrz9g8kbs.code.run`,
  `*.codexai-harness-upg-db--…`, `*.choreai-harness-con-db--…` (Northflank addon pattern, second
  deployment); `voice-harness-shurick--v1` through `--v7` `.sandbox.xsolla.dev` (numbered v1–v7
  voice-harness fleet, same cert); `pulumi-eng-544-eval-harness-fo--{admin,app,server}.dev.carebrain.app`
  ("eval-harness" naming); `deepseek-harness--v1.sandbox.xsolla.dev`;
  `harness-exec--5f10982ed5406ec20dcfa953.salvo.sh`.
- **L4 MCP-shaped (English).** `*.mcp-bear-agent--bear-agent-d23e5.europe-west4.hosted.app`,
  `pcc-c-agent-mcp{,-inspector}.pcm-sandbox.gcrm.sehlat.io`,
  `tsip--tsip-claude-mcp-e-a74760--claude-tag.coder.20-65-54-101.sslip.io` (coder workspace,
  Claude MCP), `*.mcp-deploy--z-r-z.workers.dev`, `mcp-ca-01/02`, `mcp-exca-01..04,10`,
  `mcp-exht-01..04.bmcp.local` (`.local` enterprise naming), `review-feat-mcp-tasks--8ed9ef43.digital-worker.dev.bytemethod.ai`.
  Also `mcp-storage.medien.hs-rm.de` (Hochschule RheinMain — German university, but "MCP storage"
  naming only, no agent grammar).
- **L5 `.bot` TLD (English).** `worker6/7/17/22.vanish.bot` (numbered worker fleet),
  `dashboard.jbot.bot`, `webhooks.bankr.bot`, `wiki.trsr.bot`, `zenoai.bot`, `pay.revioai.bot`,
  `fleetmesh.bot`, `agent---wiki.com` (agent wiki).

## Open items
- **O1 `zz=` unresolvable server-side:** crt.sh returned 502 on `q=%25zz%3D%25` across 4
  attempts on 2026-10-05. Mitigation applied: grepped all 4,629 downloaded DNS identities
  locally for `zz=` and `zz_` — zero hits. Residual gap: `zz=` certs outside the 19 keyword
  result sets remain unchecked.
- **O2 `agent` result size:** 533 certs (exclude=expired) is the observed return; an
  independent HTML count check 502'd and was not retried (per instruction). Treat as an
  observed sample, not a certified census.
- **O3 Wildcard invisibility:** any DE/FR swarm behind wildcard certs is CT-invisible (recon
  lane). This lane clears only non-tunnel infra.
- **O4 `agentur` (German "agency")** was not queried — outside the assigned keyword list;
  candidate for a follow-up wave if the coordinator wants it.

## Reuse notes (documented behavior, no new endpoints found)
- crt.sh JSON: `https://crt.sh/?q=%25<keyword>%25&output=json` (+ `&exclude=expired`).
  curl works; expect transient 502/404 — retry with backoff; keep ≥2s between requests.
- **Undocumented restriction (observed):** `%` is only accepted at the start/end of `q`.
  `q=%25agent%25.de` → `<BR><BR>Unsupported use of '%'</BODY>`. TLD-scoping must be done
  client-side after a broad pull.
- crt.sh `q` matches subject-DN fields (addresses, org names) as well as DNS names — always
  filter to DNS-shaped identities before counting, or street addresses like "Str. TACHE
  IONESCU" become false positives.
- Raw evidence: `raw/q_<keyword>.json` (19 files); analysis: `analysis_<keyword>.json`;
  analyzer: `analyze.py` (DNS filter + grammar screen + fleet/epoch-nonce regexes).

## Bottom line
**No German- or French-worded agent infrastructure found in CT logs across 19 queries /
~37k certs / 4,629 unique DNS identities — every DE/FR keyword resolves to article slugs,
legitimate research institutions, tool retailers, or subject-DN false positives.**
Genuine agent-shaped finds (task-oai-NNN fleet, hermes-agent fleet, harness/MCP fleets) are
all English-named with no DE/FR markers. If a DE/FR swarm exists, it either mints no certs
(like the known operator), hides behind wildcards, or doesn't use DE/FR wording in DNS.
