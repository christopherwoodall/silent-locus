# EVAL-HUNT LANE 1: GAIA / deep-research-eval-shaped traces — raw notes

## Objective
Find wild agent activity on urlquery.net matching known evals (GAIA validation questions / deep-research-style tasks).
Inverse of eval-coordinator's Amap work: they confirmed DoE→dsqa_250 but Amap fleet matches NO public benchmark.

## Step 1: GAIA validation questions (2026-10-05 ~05:50 UTC)
- `huggingface.co/datasets/gaia-benchmark/GAIA` is gated (auto) — metadata.jsonl not fetchable anonymously.
- Repo `huggingface/gaia` GitHub: `shards/` empty; data lives on HF.
- Found OPEN copy: GitHub `zhengxiaodu/dify-agents`, dir `datasets--gaia-benchmark--GAIA/snapshots/682dd723ee1e1697e00360edccf2366dc8418dd9/2023/validation/`
  contains `metadata.parquet` + `metadata.level{1,2,3}.parquet` (Oct-2025 format). Files stored via Git LFS;
  fetched real blob via `https://media.githubusercontent.com/media/zhengxiaodu/dify-agents/HEAD/.../metadata.parquet` (116,994 bytes).
- Parsed with pyarrow: 165 validation questions, schema task_id / Question / Level / Final answer / file_name / file_path / Annotator Metadata.
- Local copies: /tmp/gaia_meta_real.parquet, /tmp/gaia_questions.md, /tmp/gaia_q.json, /tmp/gaia_files.txt
- NOTE: GAIA questions embed almost no raw URLs (3 total in 165 questions) — resources referenced BY NAME.
  Fingerprints for urlquery (agents with a browse-URL tool submit the target URL) are the named resources.

## Distinctive fingerprints extracted (task_id → target)
YouTube (agent would submit watch URL):
- a1e91b78: https://www.youtube.com/watch?v=L1vXCYZAYYM (bird species count)
- 9d191bce: https://www.youtube.com/watch?v=1htKBjuUWec (Teal'c "Isn't that hot?")
- 0383a3ee: BBC Earth "Top 5 Silliest Animal Moments" bird
- 20194330: Game Grumps Sonic 2006 LP ep1
- 7a4a336d: Game Grumps Mario Kart 8 Deluxe 2017-05-14
- 00d579ea: "The Thinking Machine (Artificial Intelligence in the 1960s)"
- 0512426f: YouTube 360 VR March 2018 narrated by Gollum VA (Andy Serkis)
GitHub:
- 851e570a: https://github.com/dwyl/english-words (words_alpha dict for Boggle)
- 7619a514: github numpy.polynomial Regression-label issues
Shops/pages:
- 624cbf11: benjerry.com flavor graveyard (oldest flavor headstone rhyme)
- e8cb5b03: web.archive.org snapshot of virtuerestaurant.com dinner menu 2021-03-22
- 5b2a14e8: dog harness brand ambassador stories (meat in Dec 8 2022 story)
Science DBs:
- 17b5a6a3 / 48eb8242 / 73c1b9fe: USGS NAS database nas.er.usgs.gov (Finding Nemo fish zip codes; FL crocodiles 2000-2020; alligator west of TX)
- 7dd30055: RCSB PDB 5wb7 (rcsb.org)
- bec74516: orcid.org pages (open researcher IDs in .jsonld attachment)
- 384d0dd8: NCATS PubChem
- 708b99c5: connectedpapers.com DeepFruits 2016 graph
- 1dcc160f: openreview.net NeurIPS 2022 author "Yuri"
- d1af70ea: data.census.gov
- 0a3cd321: World Bank gross savings 2001-2010
- 2dfc4c37: boxofficemojo.com 2020 Worldwide
- 9f41b083: 2023 IPCC report (85-page version) nuclear mentions
- c526d8d6: NIH translation of 1913 Michaelis-Menten paper
- 3da89939: "Trans fatty acid contents in chocolates and chocolate wafers in Turkey" bibliography
- ad37a656: phys.org 2008-07-15 catastrophe article + Encyclopedia Britannica yield
- 840bfca7: universetoday.com 2023-06-06 Carolyn Collins Petersen article
- 0a65cb96 / 0bdb7c40: apod.nasa.gov (2015-08 first week; 2006-01-21)
- a26649c6: nature.com chinstrap penguin global assessment 2020
- 0b260a57: ScienceDirect Life Science vs Health Sciences Reference Works
- 3627a8be: British Museum collection 2012,5015.17; Science Advances 2021 abstract
- b4cc024b: Whitney Museum accession 2022.128
- 6b078778: Met Museum accession 29.100.5
- c8b7e059: Smithsonian American Art Museum paintings (Federico Lauria 2014 diss fn 397)
- 853c8244: 2015 Met exhibition (Chinese zodiac animal of 2015)
- 50f58759: en.wikipedia August-day pages June 2023 versions (Twitter/X citations)
Misc distinctive:
- d0633230: Scikit-Learn July 2017 changelog
- dd3c7503 / cabe07ed: LibreTexts Introductory Chemistry 08/21/2023 (CK-12 Marisa Alviar-Agnew)
- 72e110e7: Bielefeld BASE base-search.net DDC 633
- b9763138: Tropicos ID tropicos.org Order Helotiales
- 16d825ff: Tri-Rail tri-rail.com Pompano Beach 2019-05-27
- 05407167: replit.com 2018 VSCode blog post
- 114d5fd0: doi 10.2307/j.ctv9b2xdv (JSTOR book)
- 65638e28: doi 10.1353/book.24372 (Project MUSE)
- e4e91f1c: doi 10.2979/tex.2008.3.1.44 (Project MUSE)
- 08cae58d: Google Finance AAPL >$50 first year
- 7673d772: Cornell LII law.cornell.edu federal rules
- a0068077: NIH clinicaltrials.gov H. pylori acne trial Jan-May 2018
- 7d4a7d1d: Girls Who Code stats
- ebbc1f13: Collins Spanish-English dictionary online
- 305ac316: Polish Everybody Loves Raymond / Magda M. (non-English media!)
- c714ab3a: Van Helsing / Șirnea vampire puzzle (Romanian names)
- bda648d7: Kuznetzov/Nedoshivina 2010 Vietnamese specimens (Vietnam link)
- 872bfbb1: "Embroidery from Uzbekistan" 2008 painting + ocean liner "The Last Voyage"
- 0bb3b44a: Babylonian cuneiform numerals
Attachments (UUID names — harness may fetch from HF or mirror):
- 58 validation attachments e.g. 32102e3e-....xlsx (Seattle rental inventory), 7dd30055-....pdb,
  076c8171-....xlsx (Liminal Springs mall), df6561b2-....png, bec74516-....jsonld, etc.
  Full list: /tmp/gaia_files.txt (test split) + dify snapshot listing.

## Step 2: urlquery searches (≤1 req/5s, via uq_htmx.py)
(pending — log each query + hits below)

## Step 3: verification vs our sets
grep targets:
- ~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/events.jsonl
- ~/workspace/silent-locus/data/2026-10-03-openai-agent-traces/events.jsonl
- ~/workspace/silent-locus/data/2026-10-01-oai-tag-sweep/events.jsonl
- ~/workspace/silent-locus/collections/*/data/*.jsonl
(pending)

## Candidates
(none yet)
