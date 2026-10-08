# Dataset scale metadata

Overview of the silent-locus dataset: what it holds and how big it is.
Numbers below were counted 2026-10-08; refresh with the commands in §5.

## 1. Headline numbers

| Metric | Value |
|---|---|
| Event dirs (`data/<date>-<slug>/`) | 82 |
| Date range covered | 2016-12-28 → 2026-10-06 |
| Total files in event dirs | 18,080 |
| Total bytes in event dirs | ~3.0 GB |
| HF farm: rows/files scanned | ~365,000 |
| HF farm: unique URLs | 213,584 |
| HF farm: keyword hits | 179,171 |
| Canonical word list (`lists/words/wordlist.txt`) | 3,847 lines |
| Canonical URL list (`lists/urls/urls.jsonl`) | 331 rows |
| Legacy URL inventory (`data/transluce-api/url-inventory.jsonl`) | 154 rows |
| Deduped hosts (`url-farm/hosts-deduped.json`) | 2,846 (2,540 kept, 306 dropped) |
| Transluce findings pulled (2026-10-08) | 109 |
| Transluce submissions prepared | 3 (001 live as #170, 002 prepared, 003 live as #171) |

## 2. Collection areas

| Area | What it holds | Scale |
|---|---|---|
| `data/<date>-<slug>/` (82 event dirs) | Per-event raw captures, findings, forensics (2016 → 2026) | 18,080 files, ~3.0 GB |
| `data/transluce-api/` | Tracker pulls, evidence, submissions, dead-drop captures | 274 files, 240 MB |
| `data/transluce-api/raw/` | Transluce findings JSON pulls | 109 findings (2026-10-08) |
| `data/transluce-api/submissions/` | Filed/prepared submission forms + LEDGER.md | 3 submissions |
| `data/transluce-api/betterwright/` | BetterWright agent traces (DeepSeek/Qwen bot-check evidence) | 29 files, 170 MB, 3,840 rows |
| `data/transluce-api/webhook-site/` + `deaddrop-grammar/` + `deaddrop-followup/` | Dead-drop family captures (webhook.site inboxes, ntfy) | 27 files |
| `data/transluce-api/wildclaw/` + `wildclaw-keys/` | WildClawBench leaked-key sessions | 2 sessions verified |
| `data/hf-trajectories/` | HF trajectory datasets (raw + farm) | 1,040 files, 943 MB |
| `data/hf-trajectories/raw/` | Raw HF trajectory corpora (local-only cache) | 863 MB |
| `data/hf-trajectories/url-farm/` | Farm rollups: merged URL lists, host dedup, TARGET.md, FRESH.md, NOVELTY.md | ~120 decoded targets |
| `lists/words/` | Canonical IOC word list + by-family splits (11 model families) | 3,847 words |
| `lists/urls/` | Canonical URL inventory (farm-fresh, dedup verified) | 331 URLs |
| `data/proxy-fresh-blood/` | New proxy/dead-drop hunt (FRESH.md, NOVELTY.md) | 12 reported / 8 adjacent / 9 novel |

## 3. Largest event dirs

| Dir | Size |
|---|---|
| `data/2026-10-06-wikimedia-rogue-agents` | 1.5 GB |
| `data/2026-09-28-chinese-amap-fleet` | 966 MB |
| `data/2026-10-06-wikipedia-top500-infra-scan` | 239 MB |
| `data/2026-10-01-arquivo-pt` | 164 MB |
| `data/2026-05-17-collusion-wiki` | 100 MB |
| `data/2026-10-01-oai-tag-sweep` | 74 MB |

## 4. Notable held datasets

- **BetterWright** (`data/transluce-api/betterwright/`): 3,840 accepted rows (DeepSeek-V4.1-Flash 2,722 / Qwen3.8-Flash-Next 1,118), 193 bot_challenge detections, 192 agent `captcha.solve()` calls, 141 cleared. ~170 MB.
- **TerminalBench trajectories** (`data/hf-trajectories/yoonholee-terminalbench-trajectories/`): source of the 37 Nov-2025 jina proxy-laundering instances (Transluce #170).
- **WildClawBench** (`data/transluce-api/wildclaw-keys/`): 2 leaked-key sessions, both agents' key-noticing moments quoted and verified.
- **Dead-drop family**: 3 webhook.site inboxes + ntfy topic, COMBO-INIT exfil grammar v3→v5, Amap POI payloads.
- **Farm corpus**: 10 HF datasets scanned (yoonholee/terminalbench, hcompany, tiger-lab ×3, aisa-group, djlougen/hermes, 0xsero, crownelius, tiger-lab-browseragent).

## 5. Regeneration commands

Run from the repo root:

```bash
# Event dirs: count, date range, size
ls -d data/20* | wc -l
ls -d data/20* | head -1; ls -d data/20* | tail -1
find data/20* -type f | wc -l
du -shc data/20* | tail -1

# Canonical lists
wc -l lists/words/wordlist.txt lists/urls/urls.jsonl data/transluce-api/url-inventory.jsonl

# Transluce findings pull count
python3 -c "import json;d=json.load(open('data/transluce-api/raw/findings-list-20261008.json'));i=d if isinstance(d,list) else d.get('findings',d.get('items',[]));print(len(i))"

# Host dedup
python3 -c "import json;d=json.load(open('data/hf-trajectories/url-farm/hosts-deduped.json'));print(len(d['kept']),len(d['dropped']))"

# Area sizes
du -sh data/transluce-api data/hf-trajectories data/hf-trajectories/raw
```

Field-level schemas for each area live in the sibling files in this directory
(`event-dirs.md`, `url-inventory.md`, `wordlists.md`, `submissions.md`,
`farm-reports.md`, `evidence-packs.md`, `transluce-api.md`).
