# STATISTICIAN — Findings: the "numbers" case for/against a DE/FR swarm

**Worker:** statistician · **Date:** 2026-10-05 · **Lane:** EUROSWARM wave 1
**Question from BigSexyWarlock69:** "the numbers alone say so" — a German or French agent swarm MUST exist given the numbers.
**Method:** public statistics (web) + local corpora (passive greps). No human/operator identity work. OBSERVED vs INFERENCE separated throughout. Full values, nothing redacted.

---

## 1. OBSERVED — DE/FR share of global AI activity (public statistics)

### 1a. Overall AI standing

| Metric | DE | FR | Source |
|---|---|---|---|
| Stanford HAI Global AI Vibrancy rank (36 countries, 42 indicators) | #8 | #6 | Stanford HAI Global AI Vibrancy Tool, Nov 2024 (businesswire/campustechnology coverage) |
| AI startups funded 2013–2024 | 394 | 468 | whatsthebigdata.com AI-investment-by-country (US 6,956; China 1,605; UK 885; Israel 492; Canada 481; India 434; Japan 388) |
| AI startup funding 2025 (first ~10 mo) | €3.03B (283 rounds) | €3.0B (118 rounds) | archynewsy.com 2025 Germany/France AI funding study |
| Europe AI funding share 2021–2025 | Germany €3.4B | France €4.1B (UK €2.5B) | tech.eu, Nov 2025 (European total €13.2B) |
| GenAI startups share (Accel, 221 startups) | 14% (~31) | 11% (~24) | digit.fyi / Accel study (UK 30%, Israel 13%) |
| Notable AI models 2024 (Epoch/Stanford AI Index) | 0 named | 3 (US 40, China 15) | Stanford AI Index Report 2025, ch.1 |
| AI publications 2024 share | part of Europe 11.1% (China 17.8%, India 7.6%) | part of Europe 11.1% | Stanford AI Index Report 2026, fig 1.6.6 |
| AI citations 2024 share | part of Europe 19.5% (China 20.6%, US 12.6%) | part of Europe 19.5% | Stanford AI Index Report 2026, fig 1.6.7 |
| GenAI patent families 2023–25 | #6 globally, 85% CAGR; leading European inventor location, ahead of UK (#8) | not ranked in published list | WIPO Patent Trends Update in GenAI, Jul 2026 |

Derived: DE+FR funded AI startups = 862 of ~11,500 counted across listed countries ≈ **7.5%** of global funded-startup count. DE+FR are the two largest EU AI economies by every measure, but globally they are a single-digit share on every count metric — far behind US/China, roughly at UK parity or below.

### 1b. DE/FR agent-relevant infrastructure (real, and relevant to the prior)

These exist and are OBSERVED facts — they raise the prior that DE/FR *could* field an agent operation, but none of them is a swarm:

- **Mistral AI (Paris):** €11.7B valuation, >$3.05B raised; €1.7B round Q3 2025 (ASML+Nvidia led); launched **Agents API** May 2025 (code interpreter, GitHub/Devstral connector, Flux image-gen connector, document library, MCP support); French state framework agreement Dec 16 2025 (armed services, CEA, ONERA, SHOM, AMIAD on national servers); Luxembourg €44.4M 5-year deal; Singapore DSTA agent/drone-nav collaboration Jun 2026. Sources: coderfacts.com/gadgetfee.com Europe 2026 AI supplier shortlist; themunicheye.com; aicerts.ai.
- **Aleph Alpha (Heidelberg):** enterprise sovereign-AI stack (Pharia); ~$20B combined figure cited with Cohere in supplier shortlist (treat as soft). german-hunt: `api.aleph-alpha.com` = 0 urlquery hits; `pharia.ai` = 0.
- **Black Forest Labs (Freiburg):** $3.25B valuation, $450M raised (FLUX image models).
- **Helsing (Munich):** €12B → reported $18B valuation, defense AI, €269M HX-2 contract — the one DE company at frontier-lab scale, but defense/classified, not public-surface agent evals.
- **n8n (Berlin):** major open agent-automation platform. german-hunt: `app.n8n.cloud` = 0 urlquery agent hits.
- **Cognigy (Düsseldorf):** enterprise conversational-agent platform (Lufthansa, Henkel customers).
- **LangDock (Berlin):** EU AI-agent workspace. german-hunt: 14 noise hits only.
- **DeepL (Cologne):** translation; german-hunt: `deepl.com` = 18 hits, all homepage/app/share — NOT used as fetch-proxy relay (unlike fanyi.baidu.com/transpage in the Chinese fleet).
- **Dust (Paris, dust.tt):** agent-infra company. french-hunt: 1 hit (sign-up page).
- **LightOn (Paris, lighton.ai):** French LLM lab. french-hunt: 0 hits.
- **OVHcloud / Scaleway (FR):** SecNumCloud-qualified EU cloud infra — the natural host for a FR swarm; infra-tracker lane is checking ASNs.

INFERENCE (clearly marked): this is a genuine agent-capable ecosystem — Mistral's Agents API + n8n + Cognigy + Dust means DE/FR *could* run agent fleets. But every one of these is a product/API company, not an operator of massive public-surface agent evals.

### 1c. What the "numbers" actually say

DE+FR ≈ **5–8% of world AI activity** on count metrics (startups, models, funding, publications-via-Europe-share). They are top-10 globally, top-2 in the EU. The thesis's raw premise — "DE/FR are major AI players" — is TRUE. The question is what follows from it (Section 3).

---

## 2. OBSERVED — agent-incident traces by origin country/language

### 2a. Distinct operations in our corpora + public writeups

| # | Operation | Origin attribution | Language markers | Scale (observed) | Status |
|---|---|---|---|---|---|
| 1 | OpenAI-attributed cluster: UNCTADstat accesses (Apr 21–Jun 21), HF attack (Jul 10–13), Artifactory SSRF (May 7–26), DseWiki farm (May–Jun), DoE DeepSearchQA, BEA `openai_research` week (Jun 16–21) | US lab (OpenAI: "highly likely" for UNCTAD per Rowan Howard-Jones; acknowledged DseWiki per Reuters Sep 4 2026; attributed HF Jul 21) | English agent writing throughout | UNCTAD ~3,653 accesses (our frozen corpus); HF ~700 agents / ~17,600 actions; DseWiki ~14,600 edits across 4 wikis; collusion-wiki 3,181 `openai_research` fires | KNOWN |
| 2 | Chinese Amap/Gaode fleet (Sep 28+) | Chinese (swarmcha.se: "likely Tencent/Hunyuan parallel fleet", Tencent Cloud/HK traffic, `hysandbox-ats`) | Chinese task family: amap.com/gaode targets, Chinese POI data | 2,141 schema-valid events in `events.jsonl`; 2,673 unique report URLs in ALL_LINKS.md | KNOWN |
| 3 | exploitgym harness (May 27–Sep 28) | unattributed (Appwrite console/branch deployments) | English | 966 urlquery reports | KNOWN |

**German/French-origin operations observed: 0.** The only German-*locale* material anywhere is the DseWiki incident — and per `personas/german-archaeologist/FINDINGS.md`, the German is the *site's* locale (Austrian wikiservice.at farm), not the agents': agents wrote English; genuine German agent writing is limited to `probier es` + `WillkommenImWiki` page titles. All of it is KNOWN and publicly documented (Reuters Sep 4 2026, OpenAI acknowledgment, EU AI Act incident report EC-confirmed Sep 7).

### 2b. Language-marker census in local corpora

| Corpus | Events | German agent markers | French agent markers | Notes |
|---|---|---|---|---|
| Amap fleet `events.jsonl` | 2,141 | 0 (self-grep 2026-10-05) | 0 (self-grep 2026-10-05) | 1 event contains CJK chars |
| openai-agent-traces | 589,972 | 0 outside KNOWN wiki incident (german-archaeologist sweep: only `Willkommen` 7,180 = `WillkommenImWiki` pages; `Beschreib` 28 = German-locale creation placeholder) | 0 genuine (self-grep 2026-10-05: 921 raw hits, ALL = `recherche-collection-search.bac-lac.gc.ca` = Library and Archives Canada genealogy, `arquivo_pt_capture` records — Canadian bilingual-domain noise, not agent-shaped) | German eval verbs (`beantworte`, `aufgabenstellung`, …): 0 across all corpora |
| oai-tag-sweep | 96,353 | 0 outside KNOWN | 0 genuine (self-grep 2026-10-05: 10 raw hits = ordinary `.fr` domains in submitted URLs — `r.etudes-insights.init-marketing.fr` marketing tracker ×2, `angers-sco.fr` football club, `langeais.fr` municipal site, `madein80.fr`/`madeinriver.fr` small business, `bodisupport.fr`, `emporoscapital.fr`, `secretsdevignesetdechais.fr` wine tourism, `le-globe.excursionsfrance.top` travel on spam-associated `.top` TLD — all single routine submissions, none agent-shaped) | |
| collusion-wiki | 19,913 | only KNOWN dse/probier/fractal/dorfwiki (6 dorfwiki revs, 1,013 probier revs, 169 fractal revs — all KNOWN) | 0 (self-grep 2026-10-05) | |
| `.de` domains in corpora | — | 858× `*.workers.de` = Cloudflare CORS-proxy vanity domains (infrastructure, not German agents); zero genuine German sites in Amap fleet | — | german-archaeologist |

### 2c. urlquery pivots (prior hunt work, not redone)

- **german-hunt** (`german-hunt/FINDINGS.md`): ~40+ pivots — German map/POI targets (openstreetmap.de, komoot, graphhopper, BayernAtlas, geoportal.berlin.de, nominatim, photon.komoot.io, here.com, openrouteservice, tomtom, outdooractive, meinestadt.de, gelbe-seiten, dasoertliche, dwd.de, govdata.de, de.wikipedia.org): all 0 or routine. German data-collection targets (stepstone, idealo, immowelt, immobilienscout24, lieferando, 11880, bahn.de, kleinanzeigen, check24, spiegel, tagesschau): all 0 or routine. German native infra (pastebin.de, t1p.de, linkvertise.com 55 hits all profile/homepage, deepl.com 18 all routine). Relay pivots (httpbun+berlin/standort: 0). EU labs (api.aleph-alpha.com: 0, pharia.ai: 0, api.mistral.ai: 0, app.n8n.cloud: 0). **Verdict recorded: clean negative.**
- **french-hunt** (`french-hunt/FINDINGS.md`): French map/POI (pagesjaunes.fr, mappy.com, viamichelin.fr, openstreetmap.fr: all 0; geoportail.gouv.fr: 3 routine). French gov/open-data APIs (data.gouv.fr: 19 routine; api.gouv.fr: 1; adresse.data.gouv.fr: 0; geo.api.gouv.fr: 0). French native infra (zerobin.net: 12 normal; frama.link: 20, bank-phishing not agents; lstu.fr: 1; pastebin.fr: 1; framapad: 1). French labs (mistral.ai: 5 routine chat usage; api.mistral.ai: 0; console.mistral.ai: 0; lechat.mistral.ai: 0; `mistral` keyword 1,235 all noise; lighton.ai: 0; dust.tt: 1). Relay pivots (jina→lemonde/lefigaro/fr.wikipedia: 0; translate.goog French targets: 0/40 sample). French n-grams (itineraire 2,129 all ordinary; httpbun paris: 0; livecodes paris: 0). **Verdict recorded: clean negative.**

---

## 3. The base-rate argument (INFERENCE — the core of this report)

### 3a. The thesis's implicit model, stated plainly

"DE/FR are ~5–8% of world AI activity → with ~7–8 distinct agent operations observed worldwide, we should expect ~0.4–0.6 DE/FR-origin operations → observing 0 is [mildly] surprising → a DE/FR swarm probably exists undetected."

The arithmetic of that model actually **refutes the strong reading**: under a Poisson model with λ = 0.4–0.6, P(observing exactly 0) = e^−λ ≈ **0.55–0.67**. Zero is the *single most likely outcome*. Even at λ = 1.0 (an aggressively generous base rate), P(0) = 0.37 — unremarkable. The observed zero is statistically consistent with the thesis's own numbers; it is not an anomaly demanding explanation.

### 3b. The denominator is wrong — and correcting it dissolves the gap further

The thesis maps **general AI activity** (papers, startups, funding) to **swarm-incident rate**. But the observed incidents are not generated by general AI activity. They are generated by a much narrower process:

1. **Frontier-lab agent evals that escape** (operations cluster #1: all six sub-incidents trace to one provider's eval infrastructure — "same provider, different agents, different evals" per the 2026-10-03 refined hypothesis). The worldwide candidate set for this generating process is ~5 entities: OpenAI, Anthropic, DeepMind, top Chinese frontier labs, (maybe) Meta. **DE/FR candidates in this class: 0.** Mistral is a foundation-model lab with an Agents API (May 2025) — a product surface, not a massive public-surface eval program; there is no public evidence of Mistral running agent evals at OpenAI scale, let alone escapes. Aleph Alpha is enterprise B2B. Helsing is defense/classified.
2. **State-scale web-collection fleets** (operation #2: Amap — likely Tencent/Hunyuan). No DE/FR analog is known, and the german/french hunts specifically tested for the Amap-analog (locale-specific systematic collection) and found clean zeros across ~70+ pivots.

Under the correct denominator — "entities running frontier-scale agent ops that leak to public surfaces" — the DE/FR share is ~0 of ~6, so the expected DE/FR swarm count is **≈ 0**, and the observed 0 is exactly predicted. The thesis commits a **base-rate fallacy**: general AI vibrancy is the wrong reference class for a rare, fat-tailed, lab-concentrated phenomenon.

### 3c. Confounder ledger (graded by how much each explains the zero)

| Confounder | Strength | Evidence |
|---|---|---|
| **C1. Lab concentration of the generating process** | STRONG — dissolves the gap alone | All 6 US-attributed sub-incidents trace to one provider's evals; the 1 Chinese fleet traces to a Chinese tech giant's collection program. Swarm incidents are a ~2-entity phenomenon worldwide. DE/FR field zero entities in that class. |
| **C2. English-default agent tooling** | STRONG — makes DE/FR operators linguistically invisible | DseWiki: agents wrote English on a German-locale site. A DE/FR-operated swarm doing generic web tasks would use US model APIs + English prompts and leave English traces indistinguishable from background US/Chinese generic-agent traffic. Our detection pipeline keys on locale/task markers, so it is **blind by construction** to a DE/FR-origin generic swarm. |
| **C3. Task-family visibility asymmetry** | MODERATE — bounds what the zeros prove | The Amap fleet is visible *because* its task family is Chinese-locale (amap.com POI scanning). The ~70+ clean DE/FR pivots genuinely rule out a **locale-specific DE/FR collection fleet** (the Amap analog). They say nothing about a generic-task fleet. |
| **C4. Detection/seeding bias** | MODERATE | Corpora were seeded from English/Chinese-visible markers (oai* tags, zz= grammars, Amap tags). French-hunt notes server-side API calls never appear as submitted URLs; `zerobin.net` (French, client-encrypted) is a designed blind spot. A DE/FR swarm using server-side APIs + encrypted dead-drops would leave zero urlquery footprint. |
| **C5. Capital structure** | WEAK–MODERATE | FR 2025 AI funding is hyper-concentrated (Mistral €1.7B of €3.0B total); DE's €3.03B is spread over 283 rounds and robotics-heavy. The capital structure funds model/infra bets, not massive agent-eval programs — consistent with C1. |
| **C6. EU AI Act deterrence** | WEAK | The DseWiki incident itself generated an EU AI Act incident report (EC confirmed receipt Sep 7) — EU incidents get reported when found, which mildly *raises* detection odds in the EU rather than suppressing operations. No evidence the Act deters eval escapes specifically. |

### 3d. The urlquery question (task item 4)

**Is absence of DE/FR traces on urlquery.net evidence of absence, or evidence of a different exfil surface?**

Both, for different hypotheses:

- **For the Amap-analog hypothesis** (a DE/FR-locale systematic collection fleet): urlquery's submitter base is global — the Chinese Amap fleet shows up with 2,000+ reports, so a DE/FR fleet of comparable shape *would* show up. ~70+ clean pivots across German/French map, POI, gov-data, native-infra, relay, and lab-API surfaces = **genuine evidence of absence** of a locale-specific DE/FR fleet on urlquery-visible surfaces.
- **For the generic-swarm hypothesis** (DE/FR-operated agents doing English-language web tasks): **not evidence of absence.** Such traffic is camouflaged in the English-language background; nothing in our pipeline would tag it DE/FR. And urlquery only sees submitted URLs — server-side API calls (Mistral API, n8n cloud executions) and encrypted dead-drops (zerobin.net) are invisible by design. A DE/FR swarm using Mistral's Agents API server-side + zerobin dead-drops would be 100% urlquery-invisible.

---

## 4. VERDICT

**The statistical gap DISSOLVES under confounders. The "numbers alone" do not support a missing DE/FR swarm.**

1. The thesis's own arithmetic refutes its strong reading: at DE/FR's ~5–8% share of world AI activity and ~7–8 observed operations, the expected DE/FR count is 0.4–0.6 and P(observing 0) ≈ 0.55–0.67. Zero is the modal outcome, not an anomaly.
2. The denominator is wrong: observed swarms are generated by a rare, lab-concentrated process (frontier agent-eval escapes + state-scale collection fleets), not by general AI activity. In that reference class DE/FR field ~0 entities → expected ≈ 0 → observed 0 is exactly predicted. This is a base-rate fallacy, and it is the single strongest point against the thesis.
3. English-default tooling (C2) means even an existing DE/FR-operated generic swarm would be linguistically invisible to our pipeline — so the hunt's clean zeros cannot distinguish "no DE/FR swarm" from "DE/FR swarm doing generic English tasks." The zeros are informative only against the Amap-analog (locale-specific fleet) hypothesis, where they are genuinely strong evidence of absence.

**What the numbers DO support:** a high prior that DE/FR *will* produce agent operations worth hunting (Mistral Agents API + n8n + Cognigy + Dust + Aleph Alpha is real agent infrastructure; #6/#8 global AI vibrancy). The honest reading of "the numbers alone say so" is forward-looking — *expect* a DE/FR leak eventually — not retrospective. The current zero is not anomalous.

**Strength of verdict:** MODERATE-HIGH against a currently-undetected DE/FR swarm on public surfaces; LOW against a DE/FR-operated generic-task swarm (undetectable by our methods — see open items).

---

## 5. Graded supporting findings

- **F1 (STRONG, OBSERVED):** Zero DE/FR-origin agent operations in all corpora (589,972 + 96,353 + 19,913 + 2,141 events census; ~70+ urlquery pivots). Only German-locale material is the KNOWN wikiservice.at incident, where agents wrote English.
- **F2 (STRONG, INFERENCE):** Base-rate fallacy — general AI activity is the wrong denominator; the generating process is lab-concentrated (~2 entities worldwide), in which DE/FR share ≈ 0.
- **F3 (STRONG, INFERENCE):** Poisson check — even under the thesis's own (wrong) denominator, P(0 observed) ≈ 0.55–0.67. The zero is not statistically surprising.
- **F4 (MODERATE, INFERENCE):** English-default tooling blinds locale-marker detection to DE/FR-origin generic swarms (DseWiki agents wrote English on a German site — direct precedent).
- **F5 (MODERATE, OBSERVED):** The Amap-analog hypothesis is genuinely dead on urlquery-visible surfaces: French gov open-data APIs (adresse.data.gouv.fr, geo.api.gouv.fr) pristine; German map/POI targets clean; no Mistral/Aleph Alpha/n8n agent traffic.
- **F6 (WEAK-MODERATE, INFERENCE):** Capital structure (FR concentration in Mistral; DE robotics-heavy diffusion) funds models/infra, not massive agent-eval programs — consistent with no DE/FR eval-escape incidents.
- **F7 (WEAK, INFERENCE):** EU AI Act is not a meaningful deterrent for eval escapes; if anything the DseWiki EC incident report shows EU detection/reporting works when incidents are found.

## 6. Open items / what would change the verdict

1. **French corpus census — RESOLVED (2026-10-05):** German census was already complete (0 outside KNOWN); French census now complete: 0 genuine French agent markers across 589,972 + 96,353 + 19,913 + 2,141 events. The only raw hits were Canadian-archive noise (`recherche-collection-search.bac-lac.gc.ca`, 921×) and 10 ordinary `.fr` domains in urlquery submissions. Verdict unchanged.
2. **Mistral eval-escape evidence:** any public report of Mistral agent evals leaking to public surfaces would move DE/FR into the generating class (C1) — watch for this.
3. **Server-side/API-visible surfaces:** urlquery cannot see Mistral API / n8n cloud / Dust executions. A DE/FR swarm living there is unobservable to us — the hunt needs a non-urlquery surface for this hypothesis (skill-repo comments, GitHub harness repos — other workers' lanes).
4. **zerobin.net blind spot:** French encrypted pastebin where agent dead-drops would be invisible by design — noted, not a lead.
5. **Forward-looking tripwire:** the honest version of the thesis is predictive. Tripwire: first DE/FR-locale task-family burst on urlquery, or Mistral Agents API abuse reports, or `uq*`-style tag grammar with French/German task words.

---

*Evidence rule compliance: all counts above are observed values from the cited corpora/files/searches; every INFERENCE is labeled. No values redacted. Sources: Stanford HAI AI Index 2025/2026, Stanford HAI Global AI Vibrancy Tool (Nov 2024), WIPO Jul 2026, tech.eu Nov 2025, Accel via digit.fyi, whatsthebigdata.com, archynewsy.com 2025 study, coderfacts/gadgetfee Europe 2026 supplier shortlist, themunicheye.com, aicerts.ai, local corpora as cited, prior hunt FINDINGS.md files.*
