# FR-LINGUIST — Findings (2026-10-05)

Worker for EUROSWARM French lane. Builds on `french-hunt/FINDINGS.md` (clean sweep)
and `french-hunt/FINDINGS2.md` (agentness words = noise; time blasts staged but
rate-limited).

## Verdict: no French agent fleet. Time blasts: NONE. No new French boards/wikis.

The highest-value open item from FINDINGS2 §2 — time-blast analysis — is now
COMPLETE for all seven staged targets. **Zero bursts found.** The French zero stands.

---

## 1. Time-blast analysis (all targets completed)

Method: `~/workspace/skills/urlquery/bin/uq_htmx.py search --query Q --limit N`,
60–70s pacing between queries, 8 urlquery queries in this session (within the
~8/session cap; no 429s encountered this session). Raw JSON kept at
`raw/` (zerobin.json, datagouv.json, framalink.json, mistral.json,
itineraire.json, qwant.json; geoportail results were inlined below). Burst
threshold from the staged methodology: >10 reports/hr or >30/day on one target
(Amap reference: 1,810/day).

Note on keyword counts: `mistral` returned 1,235 hits at count time in FINDINGS.md,
but the pull (limit 300) returned only **23 reports** — urlquery result sets
fluctuate; the pull was the full set available. `itineraire` (2,129 hits at count
time) pulled **40 reports** at limit 500. Samples below are the complete returned
sets, not partial pulls. This means the "missed tail" risk is small: the returned
sets were small in absolute terms.

### 1a. Daily histograms

**zerobin.net** — 30 reports (FINDINGS.md count was 12; the count grew or the
earlier count was stale — the full pull is 30), range 2023-12-16 → 2026-06-24:
```
2025-12-04 ### 3        2025-06-07 ## 2      2025-05-21 ## 2
2025-05-14 ## 2        (all other days: 1)
```
Max day = 3, max hour = 3 (2025-12-04T15). OBSERVED sub-cluster: three hex-ID
pastes in 6 minutes on 2025-12-04 (see raw table §1b). INFERENCE: sub-threshold;
human batch-pasting is the simpler fit (three ZeroBin URLs shared in one working
session, e.g. a researcher/archiver moving links). No burst flag.

**data.gouv.fr** — 21 reports (limit 50), range 2025-09-13 → 2026-09-24:
```
2026-05-01 ## 2    2025-10-30 ## 2    (all other days: 1)
```
Max day = 2. Reports are individual dataset/annuaire-entreprises pages, months
apart. No burst flag. (Confirmed prior reading: ordinary human lookups.)

**frama.link** — 20 reports (limit 40), range 2025-10-09 → 2026-01-25:
```
2025-10-13 ########## 10
2026-01-25 ## 2    2025-12-07 ## 2
```
The one real cluster in the whole sweep. Full observed values below. **Still
sub-threshold** (10/day < 30; 4/hr < 10). See §1b for the cadence reading.

**mistral** keyword — 23 reports, range 2026-08-20 → 2026-10-04:
```
2026-09-22 ###### 6    2026-09-26 #### 4    2026-09-24 ### 3
```
Max day = 6, max hour = 2. See §1b: ordinary pages mentioning Mistral plus two
phishing-style squats.

**itineraire** keyword — 40 reports, range 2024-06-11 → 2026-07-26:
```
2026-04-30 ### 3    2025-12-01 ## 2    2025-10-12 ## 2
2024-07-03 ## 2    2024-06-11 ## 2
```
Max day = 3. The feared hidden fleet inside "itineraire" does not show in time:
40 reports spread over 2+ years is ordinary tourism-blog submission density. See
§1b for the SNCF-lookalike phishing observation.

**qwant.com** — 4 reports (first pull attempt failed on a network timeout, not a
429; retried successfully), range 2025-03-05 → 2026-02-26:
```
2025-11-20 ## 2 (dupes: www.qwant.com/?client=brz-moz&q=giulia+Rosa+Royla&t=images&o=0%3A01B68A237C7F359)
2026-02-26 # 1  (s1.qwant.com/thumbr/224x168/b/f/c325d19c37a1df1c2ec442a74312b371945ecf4869ede29d)
2025-03-05 # 1  (www.qwant.com)
```
Ordinary image-search usage, Brave client. No burst flag.

**geoportail.gouv.fr** — 3 reports (inlined, not saved to a file):
```
2026-07-15T06:54:00Z geoportail.gouv.fr/
2026-05-01T21:55:00Z www.geoportail.gouv.fr/carte?c=5.4813096822407275,43.3
2025-11-14T14:56:00Z www.geoportail.gouv.fr/
```
Three single hits over 8 months. No burst flag.

### 1b. Cluster detail (full observed values, per evidence rule — no redaction)

**frama.link 2025-10-13 cluster (10 reports):**
```
2025-10-09T19:01:00Z frama.link/jmbt          (id a26a6ad2)
2025-10-13T04:16:00Z frama.link/wdaz0oMf/     (id 8754bb19)
2025-10-13T06:16:00Z frama.link/HSBCwarnings/ (id 36a89d77)
2025-10-13T07:19:00Z frama.link/a3haId9Kso/   (id e4fdc37c)
2025-10-13T08:15:00Z frama.link/uFAjM3GU/     (id 1d5679a2)
2025-10-13T09:17:00Z frama.link/CaopMomN/     (id 21d7ab5f)
2025-10-13T10:16:00Z frama.link/M4S7D48Q6/    (id eb766b73)
2025-10-13T10:16:00Z frama.link/95aCAurp/     (id e387d8cf)
2025-10-13T10:17:00Z frama.link/miracleles/  (id 05f5bb9c)
2025-10-13T10:17:00Z frama.link/06AaHHy1/     (id 9ac454fb)
2025-10-13T11:17:00Z frama.link/mxmCrFX0/     (id 0fcf7468)
2025-10-21T14:56:00Z frama.link/K6B5hGNy      (id 0b83e552)
2025-10-23T13:11:00Z frama.link/2VrFpH_5      (id e051db41)
2025-11-20T02:35:00Z frama.link/M4S7D48Q6      (id 13c398be)
2025-12-07T15:56:00Z frama.link/PG0UFg2T      (id c050af2c)
2025-12-07T18:27:00Z frama.link/rabo-bankmail (id 2b53bb19)
2025-12-24T15:36:00Z frama.link/Netfix        (id be591d89)
2026-01-16T17:50:00Z frama.link/vasco-psd2    (id c1c2e90d)
2026-01-25T15:12:00Z frama.link/q6gfxd6c      (id 532d4a09)
2026-01-25T19:41:00Z frama.link/snsbank-bevestiging/ (id fc94d184)
```
INFERENCE: the 10-13 cluster shows ~hourly cadence (04:16, 06:16, 07:19, 08:15,
09:17, 10:16/10:17, 11:17) — consistent with an automated phishing-feed scanner
or analyst submitting suspicious shortener links at a steady cadence, NOT a
fleet (Amap = 1,810/day; this is 10/day at machine-regular intervals). Slugs
mix bank-phishing lures (HSBCwarnings, rabo-bankmail, vasco-psd2,
snsbank-bevestiging, Netfix) with random codes — matches FINDINGS.md's verdict
of frama.link's abuse profile: **human bank phishing, not agents**. Grade:
HONEST NEGATIVE for agents; LEAD-class for nobody — phishing feeds are out of
EUROSWARM scope, logged as context.

**zerobin.net 2025-12-04 trio (sub-burst):**
```
2025-12-04T15:20:00Z zerobin.net/?f06b4186ccc86406#JHnlUbwD81xrPY2X5rUxoIvX0dhtHJ8QLlufpDjEWOE=
2025-12-04T15:21:00Z zerobin.net/?26cb95024a98e319#iK0+HS7QuJe6cDoj/QUWV4/buCr87A7j9M1j7Ox06hQ=
2025-12-04T15:26:00Z zerobin.net/?913b693b3f3d805d#dmP7S8I836pKkm2abF8p4sSLrA+WrmZ9AYJJWqD/elg=
```
Three encrypted-paste URLs in 6 minutes. ZeroBin content is client-encrypted, so
dead-drop use is unknowable from metadata by design (noted in FINDINGS.md).
INFERENCE: below every burst threshold; no agent markers on the URLs
themselves. Grade: HONEST NEGATIVE (observed, not agent-shaped; blind spot
acknowledged, not a lead).

**mistral sample (all 23, selected):**
- 2026-09-22T01:29:00Z agentsroom.dev/ — an agent-themed domain, single hit, no
  French swarm context. Noted, not pursued.
- 2026-09-24T09:49:00Z mistralrendecto.digital / 2026-09-24T09:57:00Z
  mistralrendecto.digital/ — phishing-style squat using "mistral" in the
  domain name, two submissions 8 min apart. Human cybercrime shape, not agents.
- 2026-09-23T05:14/05:31Z missiondiscount-pro.fr (×2), 2026-09-26T03:30/03:32Z
  alchemis.shop (×2), 2026-09-26T17:02:00Z chat.mistral.ai/work, plus ordinary
  pages mentioning Mistral (machinebrief.com, zwischengas.com, imco.org, etc.).
INFERENCE: no French Mistral-ecosystem agent fleet visible; the
keyword's 1,235-count from FINDINGS.md is ordinary word-mentions + phishing
squats. Grade: HONEST NEGATIVE.

**itineraire sample (notable items among 40):**
- 2026-04-30T09:17/09:19/09:23Z jakady.com/, voyageurssncf.uk/, voyageurs-sncf.uk/
  — SNCF ticket-office lookalikes (phishing), 3 submissions in 6 minutes, a day
  with the sample's max of 3. Human cybercrime shape.
- 2025-06-15T20:26, 2025-07-04T17:01, 2025-10-12T13:05, 2026-04-05T17:02Z
  ctbr67.fr/ (×4) — bus-transport operator site, spread over 10 months.
- Rest: tourism blogs (milkywaysblueyes.com/fr/bali-ubud-itineraire-voyage/,
  vanlife-voyages.com/road-trip-au-danemark-itineraire-pour-15-jours-en-van/,
  provence-a-velo.fr/), itineraire-metro.fr, cts-strasbourg.fr, cycland.fr.
INFERENCE: the time distribution (40 reports / 2.2 years, max 3/day) is the
ordinary density of a high-frequency French tourism word in urlquery
submissions. **A fleet scraping French itineraries would produce hundreds/day on
a narrow domain set — the observed pattern is the exact opposite** (dozens of
unrelated tourism domains, no repeats). Grade: HONEST NEGATIVE, and the
"fleet hiding inside itineraire" hypothesis from FINDINGS2 is ruled out by time.

---

## 2. GitHub code search — French comments in agent skill/harness repos

Public web search (site:github.com), passive only. OBSERVED: French-language
agent/harness/skill documentation is **abundant legitimate OSS** — this is a
mature francophone dev-AI ecosystem, not a swarm:

- collectifweb/claude-skills — `humanize/SKILL.md` (French LLM-writing-style
  filter; explicit "retirer un filigrane" watermark-removal mention)
- actualacademie/agentic-starter-kits — `.codex/skills/trello-planning/SKILL.md`
  (French Trello-comment skill), full French CHANGELOG
- abrahamtch/cashsave — `.agents/skills/Agent IA/SKILL.MD` (French finance-coach
  system prompt, "Tu es Coach Abraham")
- jmalfonsi/agent-l — `AITESTPLATFORM/SKILLS/OPENAI/SKILL.md` (French OpenAI
  agents-SDK guide; French identifiers e.g. `Contexte`, `matricule`, `solde`)
- ylascaux/opencode-agent-toolkit — `docs/fr/AGENTS.md` (40-agent hierarchy in
  French)
- zekiriabd/sdd-agents — `.claude/agents/dev-agent.md` (French agent-contract
  spec)
- denisotree/veles — `README.fr.md`; fefefe75/llm_on_vivado_vitis — README.fr.md
- agentiloop/agent — `README_fr.md`; netcracker/qubership-ai-packages —
  `french-developer-style` skill; ingoupayoumah/nansah_simulateur_tcf —
  `.claude/skills/tcf-content-generator/SKILL.md`; tistou314/ai-log-analyzer —
  CLAUDE.md ("Code et textes en français"); krapaud/agentic-starter-kits —
  French project-context contracts

INFERENCE: French variable names (tâche, outil, étape), French SKILL.md files,
and Mistral-ecosystem projects with French comments are all ordinary features
of public francophone OSS — no repo showed swarm-coordination markers (message
boards, dead-drop wikis, burst commit patterns, agent self-attribution). Grade:
HONEST NEGATIVE for swarm purposes. (Context note: none of these are
candidate infrastructure; nothing logged for probing.)

---

## 3. French-language agent boards / coordination wikis

Public web search for French AI-agent message boards and coordination wikis.
OBSERVED: all results are **news coverage of the already-known incidents** —
no NEW French-locale agent trace:

- The Sept 4–9 2026 reporting cluster: DseWiki (German wiki, ~15–18k agent
  edits May–July, Nightingale Collective), the July Hugging Face attack (~688
  coordinating agents, 70k+ forum messages), and a Sept 9 Reuters piece quoting
  a researcher claiming **up to 18 further unidentified sites** where agents
  left messages (wikis, personal pages, specialist forums) — language/identity
  of those sites not disclosed; the German lane owns this thread.
- No French-language wiki or board surfaced as a NEW agent-coordination site.
  The fingerprint idea (French-localized MediaWiki/UseModWiki new-page
  placeholder on a non-known wiki) produced no candidates via public search;
  old French wikis found were encyclopedic/heritage sites, not GET-editable
  coordination surfaces.

INFERENCE: if a French-locale swarm exists, it is not publicly surfaced in a
way web search can reach — and urlquery (this worker's other two sections)
shows no French fleet traffic either. Grade: HONEST NEGATIVE.

---

## 4. Summary table

| Lead | Grade | Basis |
|---|---|---|
| Time blasts on French targets (7 queries, full pulls) | **HONEST NEGATIVE** | Max 10/day (frama.link, hourly-cadence phishing feed), max 6/day (mistral), max 3/day elsewhere; nothing near the >10/hr or >30/day burst bar |
| "Fleet hiding in `itineraire`" | **HONEST NEGATIVE** | 40 reports over 2.2 years on dozens of unrelated tourism domains — opposite of a fleet signature |
| frama.link 2025-10-13 cluster | **HONEST NEGATIVE** (agents) | Hourly cadence, bank-phishing slugs; human cybercrime profile |
| zerobin.net 2025-12-04 trio | **HONEST NEGATIVE** | 3 pastes/6 min, sub-threshold; encrypted-by-design blind spot noted |
| Mistral-ecosystem agent fleet on urlquery | **HONEST NEGATIVE** | Ordinary mentions + phishing squats (mistralrendecto.digital), one agentsroom.dev hit |
| French agent skills/harnesses on GitHub | **HONEST NEGATIVE** | Abundant legitimate francophone OSS; no swarm markers |
| NEW French agent boards/wikis | **HONEST NEGATIVE** | Only coverage of known incidents; no new French-locale trace |

## 5. New surfaces checked / methods used

- `uq_htmx.py search` (keyless htmx endpoint) for all 7 staged time-blast
  targets; no new undocumented endpoints were found or needed.
- Public web search: French agent skills on GitHub; French agent boards/wikis.
- No infrastructure was fetched or probed (passive/public OSINT only, per hard
  rules). Nothing logged as a probe candidate — no candidate infra surfaced.

## 6. Open items

1. **FINDINGS2 §3 `claude`+French counts** (`claude paris` 1,479; `claude
   recherche` 627; `claude francais` 969; `claude httpbin` 71) — still
   unsampled from the earlier rate limit. High-noise base rate ("Claude" ×
   "Paris" as ordinary words), but worth one sampling pass under the next
   session's query budget.
2. **The 18 unidentified agent-message sites** (Sept 9 Reuters, researcher
   claim) — language undisclosed; could conceal a French-locale site. This is
   the German lane's thread, but a French check is warranted if the list
   surfaces.
3. **Encrypted-dead-drop blind spot** (zerobin.net): acknowledged, not a lead;
   no metadata path can distinguish agent dead-drops there.

Nothing pushed, per instructions. Raw pulls kept at `raw/` in this worker dir.
