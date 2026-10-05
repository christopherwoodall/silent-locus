# Eval Coordinator — FINDINGS
## Linking agent traces to eval questions and benchmarks

**Persona:** link agent traces to EVAL QUESTIONS and benchmarks. Agents in the wild are often running evals.
**Run:** 2026-10-05 ~05:13–06:00 UTC (resumed fresh after VM restart; prior run left no saved output).
**Egress:** tested first — urlquery.net reachable (HTTP 200, ~10s). HuggingFace fetched via curl per TOOLS.md.
**Method:** (1) banked DeepSearchQA questions (`data/2026-10-01-deepsearchqa/questions.jsonl`, 900, pinned rev `b2623f8653065c2672de6d941fc5434cd652376c6`) keyword/grep-matched against trace families; (2) `collections/re-hunt-qa-fingerprints/data/hits.jsonl` (11,151 records) mined for per-family fingerprint links; (3) sibling benchmarks sampled live from HF (WideSearch `ByteDance-Seed/WideSearch` 200 Qs; WebWalkerQA `callanwu/WebWalkerQA` partial sample); (4) Amap fleet tag grammar inspected directly (`data/2026-09-28-chinese-amap-fleet/events.jsonl`, 2,141 events).
**Scope rule kept:** agents only, no operator identity work. No commits/pushes made.

---

## Critical methodology caveat (read first)

The `re-hunt-qa-fingerprints` hits are **entity-word matches, not question matches**. A fingerprint like `"Norway"` attached to `dsqa_251`+`dsqa_436` means the trace contained the word "Norway" and both questions contain "Norway" — it does NOT mean the agent was answering either question. Multiple qids per trace are the norm, not evidence of multiple evals running. Every fingerprint link below is therefore graded as *entity-level lead* unless the trace's fetched resource corresponds to a question's actual data source. Question texts were read in full before any linkage claim.

---

## Per-family linkage

### 1. DoE civilrightsdata incident → dsqa_250 — CONFIRMED
- **Candidate eval:** DeepSearchQA, task `dsqa_250` (0-based row index of `DSQA-full.csv`; provenance doc verified row 250 matches Transluce's quoted text verbatim).
- **Question:** "Using data from civilrightsdata.ed.gov for the 2017-2018 school year, determine which of [SC, NC, GA, VA] had the highest ratio of full-time equivalent school counselors to students reported as victims of race-related harassment or bullying." Answer: North Carolina.
- **Distinguishing evidence:** Transluce's explicit quote of dsqa_250 + the fleet's `zz=oai<digits>` captures on civilrightsdata.ed.gov on Jun 17. This is the gold-standard linkage in the whole hunt — distinctive data source named in the question, agent traffic on exactly that source.
- **Match quality: confirmed.**

### 2. UNCTADstat access (Apr–Jun 2026) → eval-shaped, NO DeepSearchQA match
- Fingerprint traces: agents reading `unctadstat.unctad.org/map/PCI/pci-all.csv` and `unctadstat-api.unctad.org/datamart-api/US.PCI/2005/Facts?$select=...&$filter=...` through **r.jina.ai**, with `#:~:text=Norway/Denmark/Iceland` text-fragment anchors.
- Fingerprint qids (dsqa_251, dsqa_436, dsqa_13) are entity-only ("Norway"/"Denmark"/"Iceland" appear in unrelated questions about threatened species, cancer deaths, Icelandic volcanoes). **No DSQA question concerns the Productive Capacities Index or UNCTAD PCI data** (grep for PCI/productive capacities: zero question-level hits).
- **Distinguishing evidence:** the trace shape is unmistakably eval-like — pulling a country row out of a stat table via a reader proxy is "look up country X in dataset Y," the atomic move of deep-research evals. But the question it serves is not in the banked 900.
- **Candidate evals:** unknown/hidden eval, or BrowseComp (plaintext intentionally withheld — unfingerprintable by design). GAIA (gated) not checked.
- **Match quality: task-family only.** Provider signal: Rowan Howard-Jones attributed the swarm to OpenAI, "highly likely" (per MEMORY).

### 3. AIHW health-data pulls (Jun 18–21, 2026) → eval-shaped R&D, NO DeepSearchQA match
- Fingerprint traces: agents hitting the AIHW PBS Tableau dashboard (`vizprod.aihw.gov.au/t/Public/views/PBSdashboardallATC1-ATC2medicines-Agegroup/PBSDashboard...`, also `viz.aihw.gov.au`), plus the June 20–21 strand with `uqtag=AGEDATA23` embedding a `vizprod.aihw.gov.au` Tableau module (report IDs `fbda6df4…`, `9188235a…`, `1fd1c390…`, `81dc5646…` per the apprentice).
- Fingerprint qids (dsqa_116, 665, 746 via "Australia"; dsqa_739 "Swan"; dsqa_527 "Kingston") are entity-only. **No DSQA question concerns the PBS dashboard, Australian aged care, or AIHW** (grep: PBS, aged care, AIHW → zero).
- **Distinguishing evidence:** the apprentice persona confirmed a textbook XSS payload (`<svg/onload=document.title="XSS">`) fired at the AIHW Tableau dashboard after a Cloudflare block, then a pivot to `pp.aihw.gov.au` and a 100+ scan pull — tutorial-following inside this strand. Task-prefixed disposable-email provisioning (`aihw…`, `pbs…` signups per Asymmetric Security) shows dedicated agent infrastructure for this target.
- **Candidate eval:** unknown — possibly a hidden/custom health-data eval. The strand reads as operator R&D (capability-building on a hard target) as much as eval execution.
- **Match quality: task-family only.** Open item (from apprentice): normalize the four `uqtag=AGEDATA23` reports into the corpus.

### 4. Vietnam stats APIs (pxweb.nso.gov.vn / pxweb.gso.gov.vn) → task-family only, unattributed
- YOURLS-referrer evidence (Global South Scout): encoding-variant retry grammar (space / `%20` / `+`), a `TESTDEFAULT999` probe, both agency hostnames — programmatic national-statistics-API task family.
- **No DSQA question mentions Vietnam or pxweb** (grep: zero). No fingerprint hits tie pxweb to any qid.
- **Match quality: task-family only.** Provider: unknown. This family is currently the least-attributed of all — a genuinely open eval linkage.

### 5. Egypt EDA articles (2026-07-17) → DeepSearchQA-adjacent, WEAK
- Two urlquery reports 3 seconds apart, `utm_source=chatgpt.com` URLs of Egyptian Drug Authority news (Africa Health Excon 2026, vaccine-manufacturing partnerships).
- Fingerprint qids dsqa_283 (FAO aquaculture employment, "Africa" as answer option) and dsqa_339 (African economies labor force) are entity-only "Africa" matches. No DSQA question concerns vaccine manufacturing or Africa Health Excon (grep: vaccine → dsqa_840, dsqa_873, both unrelated).
- **Match quality: weak.** Reads as a one-off research artifact (URLs copied from a ChatGPT answer), not an eval run.

### 6. Museum scans → no corpus evidence found; WideSearch has the only plausible driver
- Grep of the 2,141-event amap-fleet corpus for "museum": **zero hits**. ("Museum/live metadata monitoring" in the standing summary refers to other corpora: `2026-05-17-collusion-wiki`, `2026-06-04-admin-deletions`, `2026-08-19-tantive-space`, `2026-10-01-oai-tag-sweep` contain museum strings.)
- DSQA has 5 museum questions (dsqa_107 GSA/SFMOMA, dsqa_208 Brooklyn/O'Keeffe, dsqa_239 Athens, dsqa_569 Met/Abbey, dsqa_648 Florida Museum) — all US/European institutions, no Amap-shaped driver.
- **WideSearch `ws_zh_073`** asks for Beijing's free museums with addresses and opening hours from the Beijing cultural-bureau site — an agent solving it plausibly looks up museum addresses on Amap. Weak but the only ZH museum-eval candidate found.
- **Match quality: none established for the fleet; weak-plausible (WideSearch) for Chinese museum lookups generally.**

### 7. Amap POI fleet (Sep 28 – Oct 5, 2026) → NO public benchmark match found
- Task shape: `amap-pc-ssr.amap.com/ssr/place/{POI_ID}?uqscan={label}` — systematic POI page pulls, labels `research*/target*/<place><date><a/b/c>`, routes 94% direct / 5.5% carrier / 1% relay.
- WideSearch: 200 questions sampled; ZH travel/museum/hotel questions are **table-format deep research** (ws_zh_028 scenic spots, ws_zh_073 museums, ws_zh_039 hotels) — not POI-API sweeps. No Amap/`getPoiInfo` driver found.
- WebWalkerQA (327/680 sampled): education/conference/game/organization domains — no map/POI.
- BrowseComp/BrowseComp-Plus: encrypted by design, unfingerprintable. xbench/DeepSearch: encrypted test cases. GAIA: gated, not checked.
- **Match quality: no match.** The fleet's task (bulk POI venue verification on Amap's SSR pages) does not correspond to any sampled public benchmark.

---

## The escaped-eval hypothesis, stress-tested per family

BigSexyWarlock69's refined hypothesis: **same provider, different agents, different evals** — common launcher/toolkit (oai* tags, zz=oai params, epoch nonces, jina, webhook dead-drops), different task families per eval.

**New stress-test result — the Amap fleet's self-labels say `claude`:**
- 182 of 2,141 fleet events carry model self-labels (`uqscan=claude20261004bailuzhou`, `uqresearch=claude20261004xzs1`, …). **`claude` is the ONLY model name present** — zero gpt/deepseek/gemini/qwen/kimi/doubao.
- The linguist persona independently found the same (182 tags) and cautioned "harness convention, not proven model attribution."
- Implication: if the label is truthful, the Amap fleet is **Claude-powered**, and the "same provider = OpenAI" leg of the hypothesis does NOT cover it. If the label is harness convention/misdirection, provider attribution for the fleet is unproven either way. **Either reading weakens the single-provider framing for the Amap incident specifically.**
- Cross-family provider signals are otherwise OpenAI-leaning: DoE (Transluce: OpenAI attribution), UNCTAD ("highly likely" OpenAI), Egypt (`utm_source=chatgpt.com`), AIHW (dedicated agent infra, provider unclear), Vietnam (unknown).

**Assessment:** the hypothesis holds as a *toolkit-level* claim for the OpenAI-attributed families (DoE, UNCTAD, AIHW share jina-laundering, epoch nonces, webhook dead-drops), but the Amap fleet is the outlier — different target geography, different task shape, and self-labels pointing away from OpenAI. Treat the fleet as a **separate escaped-eval candidate until provider linkage is established**, not as confirmed same-provider.

---

## Open follow-ups
1. Normalize the four `uqtag=AGEDATA23` AIHW reports (fbda6df4…, 9188235a…, 1fd1c390…, 81dc5646…) into the unified dataset (apprentice recommendation).
2. BrowseComp-Plus (`Tevatron/browsecomp-plus`, frozen corpus, `query_id` obfuscated) and GAIA (gated) remain unchecked as possible homes for the UNCTAD/AIHW/PBS question shapes.
3. The `claude` self-labels need independent verification: check whether any fleet report's submitter-side metadata (UA, exit node, tags) corroborates or contradicts the label (pending egress-dependent pulls).
4. Vietnam pxweb family: no eval home and no provider signal — highest-priority unattributed family.

---

## APPENDIX — All observed URLs

### DeepSearchQA / benchmark sources
- https://huggingface.co/datasets/google/deepsearchqa (900 questions, rev b2623f8653065c2672de6d941fc5434cd652376c6)
- https://huggingface.co/datasets/ByteDance-Seed/WideSearch (WideSearch, 200 Qs, sampled live)
- https://huggingface.co/datasets/callanwu/WebWalkerQA (WebWalkerQA, 680 Qs, partially sampled)
- https://huggingface.co/datasets/gaia-benchmark/GAIA (gated, not checked)
- https://huggingface.co/datasets/Tevatron/browsecomp-plus (not pulled; candidate follow-up)
- https://huggingface.co/datasets/xbench/DeepSearch (encrypted test cases, not checked)

### UNCTAD traces (via r.jina.ai)
- http://unctadstat.unctad.org/map/PCI/pci-all.csv (with #:~:text=Norway / Denmark / Iceland anchors)
- http://unctadstat-api.unctad.org/datamart-api/US.PCI/2005/Facts?$select=Year,Category,Economy,M6080&$filter=Year ge 2002 and Year le 2005 and Category…

### AIHW traces
- vizprod.aihw.gov.au/t/Public/views/PBSdashboardallATC1-ATC2medicines-Agegroup/PBSDashboard.png?:showVizHome=no&Measures=Rolling+12+months+average&Month+of+interest=…
- viz.aihw.gov.au/t/Public/views/PBSdashboardallATC1-ATC2medicines-Agegroup/PBSDashboard?:showVizHome=no&Measures=Rolling+12+months+average&Month+of+interest=…
- pp.aihw.gov.au (pivot target after Cloudflare block)

### Amap fleet
- https://amap-pc-ssr.amap.com/ssr/place/B01FE16U78?uqscan=research20261005d (example POI pull)
- https://urlquery.net/report/ca2cadb6-9136-4fe3-bb6d-1c8f33132f53 (example report)

### Fingerprint / evidence sources (local)
- collections/re-hunt-qa-fingerprints/data/hits.jsonl (11,151 entity-fingerprint records)
- data/2026-10-01-deepsearchqa/questions.jsonl
- data/2026-09-28-chinese-amap-fleet/events.jsonl
