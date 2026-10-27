# Hugging Face lane — broad agent-egress hunt

## Result in short

No new hit. This lane found zero ranked candidates.

The search covered IDs, names, card text, and small trace files.
No shape matched agent behavior. The items below are triaged out, not hits.

## Terms used here

- Behavior shape: a pattern of actions, not a host name string.
- SECONDARY: evidence from a third party, not first-hand capture.
- Pattern match: a text match for a shape. It is not confirmed behavior.
- README: the card text on a Hub dataset or model page.
- Trace: a saved record of an agent run, with tool calls and outputs.
- Parquet: a binary table file format. Text grep cannot read it directly.

## The 6 shapes hunted

1. Cloud-metadata reach: `169.254.169.254`, `fd00:ec2::254`,
   `metadata.google.internal`, or `100.100.100.200` in a network call.
2. Object-storage upload: curl or wget file-upload flags, or an env dump,
   to S3, GCS, Azure Blob, R2, or Alibaba OSS.
3. Named probe hosts: the two hosts from the Cohere write-up, on a
   network use. Those hosts are the sanmaohe bucket host and the
   routify file-proxy host.
4. User-namespace escape: `unshare` with `-U`, `-r`, `-c`, `-Urm`,
   `--user`, or `--map-*-user`. Mount-only and net-only use is excluded.
5. Download-then-execute: curl `-o` or wget `-O` to a path, then running
   that path.
6. Recon-then-egress: recon commands plus a network call in one command.
   Recon alone is silent.

## Method

### API search: IDs and names only

The Hub API search matches IDs and names. It does not match description
text. Proof: search for `Pi-compatible` returns 0 rows, but that phrase
sits in the description of the seed dataset
`CohereLabs/10-2026-qwen-investigation-traces`. The seed dataset is
excluded from ranking here. It is prior work, not a new hit.

### Description-text method: full card text plus grep

The delta for this lane is card text. Steps:

1. Run topical API searches to list candidate datasets and models.
2. Fetch the full README text for each candidate.
3. Grep the README text for all 6 shapes.
4. For trace datasets, list repo files and fetch small text files.
5. Grep those trace files for the shapes.

This method reads what the API search cannot see: card text and trace
text. It does not read binary files. See the limits below.

### Web-index method

Five web searches over indexed Hub pages for shape terms ran in parallel.
They found no new Hub dataset hit. One result was a regex dataset. It is
triaged out below. Web indexes have gaps. This net is weak by itself.

### Rules kept

- Read-only GET calls only. No POST. No login. No account.
- No benchmark code was run. No media was fetched. Text files only.
- No file was committed or pushed. No Factum write was made.
- Raw captures keep full bytes. They were never redacted.
- No signed URL, signature, token, or credential-shaped value was seen
  in this lane. The signed-URL rule had nothing to apply to.

## Searches run

API searches, each capped at 100 rows by the API:

| Search set | Queries | Rows returned |
|---|---|---|
| Datasets, shape terms (10 terms) | 10 | 1 (see triaged out) |
| Models, shape terms (10 terms) | 10 | 18 (see triaged out) |
| Spaces, shape terms (10 terms) | 10 | 0 |
| Datasets, topical terms (10 terms) | 10 | 701 |
| Datasets, topical, downloads sort (4 terms) | 4 | 289 |
| Models, `agent`, downloads sort | 1 | 100 |

Total: 45 API search files, 1,109 rows with overlap across queries.
Unique dataset IDs across dataset search files: 821.
Shape-term rows: only the `unshare` model substring hits and the
wine-label metadata dataset. All other shape-term searches returned 0.

Topical dataset terms: `trajectory`, `agent-traces`, `computer-use`,
`web-agent`, `OSWorld`, `WebArena`, `SWE-agent`, `agent-benchmark`,
`browser-agent`, `tool-use`.

Card text fetched and grepped:

| Set | Fetched | With prose text | Shape hits |
|---|---|---|---|
| Dataset READMEs, top 150 by downloads | 150 | 113 | 0 |
| Model cards, top 30 by downloads | 30 | 30 | 0 (2 logo lines, triaged out) |
| Small trace files, 12 trace datasets | 74 | 74 | 0 (2 local-check lines, triaged out) |

Dataset README detail: 30 of 150 had no README at main. The Hub
returns `Entry not found` for those. 7 more were YAML stubs only, with
no prose. 113 had prose. Total README lines grepped: 11,322.
Total README bytes: about 463 KB.

Trace-file detail: 74 files from 10 of 12 trace datasets, about 5.7 MB.
Two datasets gave no small text files. See the limits below.

## Candidate hits

None. No dataset, model, or space ranks as a hit in this lane.

## Triaged out: do not rank

1. `unshare` model hits are a substring false positive. All 18 model
   IDs contain `unshared`, a weight-sharing term. None is the `unshare`
   command. None shows a namespace escape. Grade: not a match.
2. Wine-label metadata dataset is a substring false positive. The
   `cloud-metadata` search matched a wine-label metadata mirror. It has
   no cloud metadata endpoint and no agent behavior. Grade: not a match.
3. Regex dataset is a defensive pattern, not behavior. The web search
   surfaced `tanaymehta/labelled_regex`. Its URL regex lists
   `169.254` only to exclude private IPs. No agent runs it. No network
   call happens. Grade: not a match.
4. Qwen-AgentWorld logo lines are string-only. Two model cards load a
   logo image from a Qwen vendor OSS host. A logo in card markup is not
   an agent action. No upload happens. No agent call happens.
   Grade: string-only, not a match.
5. Localhost curl lines are not download-then-execute. One coding-agent
   session trace in `trace-commons/agent-traces` runs curl with `-o`
   to `/dev/null` against a localhost dev server. Output is discarded.
   Nothing is downloaded to a file. Nothing is then executed. The
   target is local, not outside. Shape 5 needs a download plus an
   execute step. This has neither. Grade: not a match.

## Limits and open questions

- API cap: 100 rows per query. Topical lists are capped samples.
  Lower-ranked datasets were never listed.
- README cap: top 150 topical datasets by download count only.
  Lower-download datasets were never read.
- No-README datasets: 30 of the top 150 have no README text to grep.
  Their card text cannot hide a shape, but their data files can.
- Binary trace files were not read. Most trace datasets store traces
  as Parquet. Parquet content is unsearched in this lane.
- Zip archives were not read. `agent-evals/hal_traces` holds 380 zip
  files, each 169 MB to 1.6 GB. Those traces are unsearched here.
- Tree-list cap: one dataset tree listing stopped at 1,000 entries,
  all directories. Its deeper files were never listed or fetched.
  That dataset is `melissapan/swe-bench-lite-agent-traces-v14`.
- Gated datasets return no README without login. Login is out of
  scope. Gated card text is unsearched.
- Space app code was not scanned. Spaces search matched shape terms
  at 0, but space code files were never grepped.
- Model cards beyond the top 30 `agent` results were never read.
- Web-index coverage is partial. An unindexed Hub page would be missed.
- Local overlap check: a text grep over the local
  `data/lanes/hf-trajectories-audit/` lane docs found no shape term.
  No local overlap was found. Factum checks belong to the coordinator
  phase. This lane made no Factum write and no Factum query.

## Evidence

Raw captures live under
`data/lanes/agent-egress-broad-hunt/raw/huggingface/`.

- `api_*.json`: 45 API search results, each with `.PROVENANCE.txt`
  (source URL, retrieval time, method) and `.sha256`.
- `readmes/`: 150 dataset README texts with provenance and hashes.
- `modelcards/`: 30 model card texts with provenance and hashes.
- `trees/`: 12 trace-dataset recursive file listings.
- `tracefiles/`: 74 small trace text files with provenance and hashes.
- `readme_grep_hits.txt`, `tracefile_grep_hits.txt`,
  `modelcard_grep_hits.txt`: grep outputs. All shape sections are
  empty except the triaged-out lines described above.
- `run_api_searches.sh`, `run_readme_grep.sh`, `run_tracefiles.sh`,
  `run_modelcards.sh`: the scripts used. Re-runs skip existing files.
- `SHA256SUMS`: hashes for 948 files in the directory.

No file in this lane was committed or pushed. No Factum write was made.
The coordinator owns commit and ingest.
