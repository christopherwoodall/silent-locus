# Eval hunt: what is the Chinese fleet actually doing?

## Question
Is the Amap fleet (Tencent Hunyuan agents, 28 Sep 2026 →, 216 places, entrance navigation shares via `sub_poi_navi`/`clk_ratio`) running a benchmark? If so, which one — so we can find more of its traces.

## Verdict: no public eval matches. The shape is dataset construction, not a benchmark run.

### Candidates graded

| Candidate | Match | Why |
|---|---|---|
| ABot-Navigation POIBench (amap-cvlab) | WEAK | "Navigate to a named POI entrance" (163 POIs) is thematically adjacent — POI entrances! — but it is embodied 3D navigation (3DGS scenes), not web data collection. Different modality. https://github.com/amap-cvlab/ABot-Navigation |
| BrowseComp-ZH | WEAK | Chinese web-browsing Q&A benchmark (289 questions, 11 domains). Q&A shape; the fleet does systematic collection, not question-answering. https://arxiv.org/pdf/2504.19314 |
| DeepSearchQA | WEAK | List-style web questions; our dsqa_250→DoE precedent shows this family drives data collection, but it is English/US-focused with no known map tasks. https://benchlm.ai/benchmarks/deepsearchqa |
| ExplorationBench (Tencent/Fudan, released 25 Sep 2026) | NO | Synthetic alien worlds (AlienCode/AlienLogic). Ruled out on task shape. Timing (3 days before fleet start) is coincidence. https://explorationbench.com/ |
| C3-Bench (tencent-hunyuan) | NO | Tool-use robustness benchmark. Wrong task family. https://github.com/tencent-hunyuan/c3-benchmark |
| MAP (Multimodal Accessibility Planning) | WEAK | About POI entrances, but accessibility features — not navigation shares. https://arxiv.org/pdf/2608.28384 |

### Why dataset construction fits better
- **Task shape**: "collect X for N=216 items" builds a table; evals answer questions. Only 2 readouts from 216 places — still collecting, not scoring.
- **Tags**: `research20261004full`, `research20261004final` read as research data-collection runs, not benchmark submissions.
- **No public dataset exists**: HuggingFace search for Amap entrance/POI datasets returns nothing (checked 2026-10-05). They are building what does not yet exist.
- **Strategic timing**: Amap launched 千舆 (map-data-as-agent-tools) 23 Sep; Tencent launched 盖亚 (its own spatial-intelligence platform) mid-Sep. Both platforms need exactly this data (entrance popularity, POI dynamics). A Tencent team scraping Alibaba's Amap for entrance shares is competitive data acquisition for the map-platform war — not a benchmark.

### Alternative: Tencent internal eval
Cannot be ruled out or observed publicly. If it exists, it would surface as: evolved `uqscan=` tag grammars in continued urlquery runs, a published dataset (watch HF + ModelScope), or a paper from Tencent/Amap-affiliated authors.

## Where else runs would be observable
1. **urlscan.io** — same programs submitted as scans (coordinator lane running).
2. **Continued urlquery runs** — live monitor watching; tag-grammar evolution signals new phases. `uqscan=` is fleet-exclusive so far (1,217 hits, all Amap).
3. **Dataset publication** — HuggingFace + ModelScope watch for Amap entrance-share datasets (none as of 2026-10-05). This is the payoff event.
4. **arXiv** — entrance-share / POI navigation papers from Tencent/Amap authors.
5. **千舆 / 盖亚 platforms** — if the data feeds Amap's or Tencent's agent-tool offerings, it may surface in platform changelogs or docs.

## Follow-ups
- Extract the 216 place IDs from the collection and fingerprint against known POI datasets (tags encode hints: `shaanxihistory`, `dalian`, `gzhosp`, `cdhv`).
- The `user_loc` params (e.g. Chengdu coords 104.05,30.59) suggest simulated users per city — cluster places by `user_loc` to reconstruct the sampling frame.
- Watchlist: `uqscan=`/`uqtag=` on non-Amap domains = the same harness on a new task.

## Bottom line for the operator
Stop looking for the eval — there is no public one. Hunt the dataset instead: its construction is observable now (urlquery), its publication later (HF/ModelScope). The technique fingerprint (`uqscan=` tags, `sub_poi_navi`/`clk_ratio` reads, webhook.site dead-drops) is what will reveal the next instance.
