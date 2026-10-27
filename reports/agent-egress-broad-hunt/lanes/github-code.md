# GitHub code search lane: agent egress broad hunt

## Status

This lane is STAGED, not filed. No Factum write was made. No file was
committed or pushed. No branch was switched. This lane is read-only.

## Terms used in this lane

- Behavior shape: a pattern of actions. One example is recon, then upload.
  A shape is not a host name string.
- Mention: code or text names a shape. It does not show an agent doing it.
- Behavior observation: evidence shows an agent doing the shape. A trace,
  a log, or a run record counts. A doc, a test, or a skill file does not.
- Instruction artifact: a skill file or agent config that tells an agent
  how to do a shape. It is a mention with agent context. It is not a run.
- SECONDARY: evidence from a third party, not a first-hand capture.
- LOW: the match is thin, or it is a string match only.

## Headline

No new agent egress behavior was found. Zero screened items show an
agent doing a hunted shape. All screened items are mentions, docs,
installers, detection rules, defensive guards, or instruction artifacts.

This is an honest null for new behavior. It is not proof of absence.
Only the first 30 results of each query were screened. See the limits.

## Method

- Tool: `gh api search/code` with the existing gh CLI auth. Read-only GET.
- Account: the existing configured account. No fresh login was made.
- No POST was made. Nothing was created or changed on GitHub.
- Each query fetched one page of 30 results. No second page was fetched.
- Fragments from the text-match response were screened. Full files were
  not fetched, except where a fragment was enough to classify.
- Pace: 8 seconds between calls. Code search quota is 10 calls per minute.
  No quota block was hit. No 429 or 403 was seen on this lane.
- First failure, then fix: the `gh api -f q=` form returned 404 for every
  query on this gh build. The URL form (`search/code?q=...`) returned 200.
  The 16 failed calls were not retried in a loop. The script was fixed
  once, then run once. That run passed all 16 queries.

## Queries run

Each row gives the exact query, the total GitHub reports, and how many
this lane fetched. Fetched means screened from fragments.

| ID | Query | Total | Fetched |
|----|-------|-------|---------|
| c01 | `"unshare -Urm"` | 1,326 | 30 |
| c02 | `"unshare --map-root-user"` | 890 | 30 |
| c03 | `"unshare -U"` | 11,520 | 30 |
| c04 | `"curl -o" "chmod +x"` | 102,272 | 30 |
| c05 | `"wget -O" "chmod +x"` | 110,080 | 30 |
| c06 | `"curl -fsSL" bash` | 1,280,000 | 30 |
| c07 | `"wget -qO-" bash` | 125,440 | 30 |
| c08 | `"cat /etc/resolv.conf" curl` | 14,976 | 30 |
| c09 | `"uname -a" curl` | 371,200 | 30 |
| c10 | `"169.254.169.254" curl` | 129,536 | 30 |
| c11 | `"metadata.google.internal" curl` | 26,560 | 30 |
| c12 | `"curl -T" amazonaws` | 361 | 30 |
| c13 | `"curl --upload-file" oss` | 2,848 | 30 |
| c14 | `sanmaohe` | 63 | 30 |
| c15 | `routify-file-proxy` | 73 | 30 |
| c16 | `"curl -F" amazonaws` | 59,264 | 30 |

Total fetched and screened: 480 items. Total reported by GitHub across
all 16 queries: about 2.4 million. The screened share is tiny. Broad
queries (c06, c09) are dominated by installer scripts and docs. They
have almost no power to find agent behavior without agent context.

## Ranked candidates

Rank order is by closeness to agent behavior. None is a behavior
observation. All are SECONDARY at best. Model identity is unidentified
in every case, except where the file itself is about a named model
family (Qwen repro tooling, item 3). No new host was found. No new
shape was found.

### 1. LOW — Agent skill and config files that teach cloud metadata reach (shape 1)

- Files:
  - `cdxiaodong/cain-agent`, `skills/gcp-attack.md` — an agent skill
    file. It lists metadata service reach steps for GCP.
  - `ASCIT31/Dark-Moon`, `conf/agents/gcp.md` — an agent config file.
    It lists metadata token and scope fetch commands for GCP.
  - `awarexone/Agentic-Bug-Hunter`, `SKILL.md` — an agent skill file.
    It lists cloud metadata endpoints, including the AWS metadata
    address and the GCP metadata host.
- Shape: 1 (cloud-metadata reach).
- Classification: instruction artifact, NOT behavior observation.
- Why it ranks first: these files are agent-facing. They put the shape
  in an agent's working context. That is closer to agent egress than a
  cheat sheet is. But no run, trace, log, or result is shown. Nothing
  proves an agent used these files to reach a metadata service.
- Caveat: skill files are common in security-agent repos. Presence of
  a skill is not use of a skill. Do not cite these as agent behavior.
- Grade: SECONDARY. Confidence: LOW.

### 2. LOW — Agent skill files that teach user-namespace escape (shape 4)

- Files:
  - `SnailSploit/Claude-Red`, `Skills/container/offensive-container-escape/SKILL.md`
    — an agent skill file. It lists user-namespace escape methods.
  - `Zyrexnn/Cybermes`, `skills/sandbox-escape-techniques/SKILL.md`
    — an agent skill file. It lists sandbox escape techniques.
- Shape: 4 (user-namespace escape).
- Classification: instruction artifact, NOT behavior observation.
- Why it ranks: same reason as item 1. The files are agent-facing.
  No run or escape result is shown.
- Caveat: these are offensive-skill repos. Their existence shows that
  escape knowledge is packaged for agents. It does not show an escape
  by an agent in the wild.
- Grade: SECONDARY. Confidence: LOW.

### 3. LOW — Seed-class repro and defensive tooling (shape 3, known class)

- Files:
  - `wtogami/qwen-block-proxy-artifacts` — a defensive plugin, a
    repro script, and ladder test results for the Qwen proxy shape.
  - `Enntity/sparkqwen`, `docs/TOOL-GUARD.md` and tool-guard result
    files — a defensive guard for the same shape.
  - `enncoded/pi-block-proxy-artifacts` — a second defensive plugin
    for the same shape.
  - `javierbits/qwen38-prefill-repro`, trace files — a repro of the
    Qwen prefill shape. The screened fragment matches the seed host
    names. No live egress is shown in the screened fragment.
  - `alextra-lab/personal_agent`, `src/personal_agent/security.py` —
    a blocklist addition. This is already known from the prior hunt
    (August blocklist, hearsay core). It is overlap, not new.
  - `bendyline/gezel`, `packages/core/src/security/egress-indicators.ts`
    — detection indicators, not an incident.
- Shape: 3 (named probe hosts).
- Classification: defensive or downstream artifact, NOT behavior
  observation. The repro traces are tests of a known class, not new
  live incidents.
- Why it ranks: it confirms the seed class is still the only Qwen
  shape visible in code search. It adds no new host and no new shape.
- Caveat: only fragments were screened for the trace files. A full
  trace read could change the classification of the repro item. That
  read was not done in this lane.
- Grade: SECONDARY. Confidence: LOW.

### 4. LOW — Defensive guard that lists upload patterns (shape 2)

- File: `ai-job-search-dev/ai-job-search`, `tools/security_guards.py`.
  It lists guarded shell patterns, including curl upload flags.
- Shape: 2 (object-storage upload).
- Classification: detection rule, NOT behavior observation.
- Caveat: this is the same class as the prior hunt's detection pack.
  Rule-writing convergence is not observation convergence.
- Grade: SECONDARY. Confidence: LOW.

### 5. LOW — Sandbox docs that note unshare is blocked (shape 4, negative note)

- Files:
  - `different-ai/openwork`, `evals/README.md`, and
    `omnirush-ai/omnirush-gui`, `evals/README.md` — eval docs. They
    state a sandbox blocks user-namespace creation, so no container
    runtime can start there.
  - `gadievron/raptor`, `core/sandbox/probes.py` — sandbox probe
    code. It tests whether user-namespace creation is available.
- Shape: 4 (user-namespace escape).
- Classification: mention, NOT behavior observation. The eval docs
  are a negative note: the escape is blocked, not done.
- Grade: SECONDARY. Confidence: LOW.

## Triaged out: not ranked

- Shape 5 (download-then-execute): the screened items are installer
  scripts and install docs. Examples include vendor install scripts,
  OS tool installers, and user install guides for agent tools. No
  screened item shows an agent downloading and running a file on its
  own. The shape is too common in installers to find agent behavior
  without agent context. Zero agent-behavior observations in sample.
- Shape 6 (recon-then-egress): the screened items are networking
  docs, container debug guides, and training histories. The recon
  term and the network term appear in the same file, but not as one
  agent command with egress. Zero agent-behavior observations in sample.
- Shape 1, general: the screened items are cloud docs, pentest cheat
  sheets, SSRF test notes, and defensive guards. No screened item
  shows an agent reaching a metadata service. The three agent-facing
  files are item 1 above.
- Shape 2, general: the screened items are upload docs, SDK examples,
  and build scripts that push files to their own buckets. No screened
  item shows an agent dumping environment data to object storage.
- Shape 4, general: the screened items are exploit write-ups, CVE
  records, container tooling, and test code. No screened item shows
  an agent escaping a sandbox.
- Shape 3, general: outside item 3, the screened items are news
  copies, wiki notes, and second copies of the Cohere write-up. No
  new host and no new live incident.

## Novelty statement

No new behavior, no new host, no seed reproduction. Items 1 and 2 are
new strings in this lane (agent skill files were not screened in the
prior hunt), but they are instruction artifacts, not behavior. Novelty
of a string is not novelty of a finding. Items 3 to 5 are known-class
or defensive material.

No full novelty check (Factum exact and fuzzy, legacy trees, Transluce
tracker) was run in this lane. The lane stages candidates only. The
coordinator runs novelty checks before any NEW claim. Until then, no
item here is claimed as NEW.

## Signed-URL rule note

This summary carries parameter names and path shapes only. No signed
query string, signature, token, or credential-shaped value is copied
here. Raw capture files are never redacted: they hold full bytes as
returned by the API. One screened fragment held a public example
upload URL with query parameters; it is not reproduced here.

## Limits and open items

1. Sampling: 30 of each total were screened. For broad queries, the
   screened share is under 0.1 percent. Most results were never seen.
2. Fragment-only screening: classification used API text-match
   fragments, not full file reads. A full read could reclassify an
   item, in either direction.
3. Ranking by relevance: GitHub orders code results by its own
   ranking, not by date or by agent link. The first page may miss
   agent-linked items deeper in the set.
4. Broad queries are weak: c06 and c09 match millions of files. A
   useful shape-5 or shape-6 code query needs an agent marker term
   added (harness name, skill path, or trace path) to cut installer
   noise. That refinement is proposed, not run.
5. No second pages were fetched. No file-content fetches were made
   for candidates. Both are open follow-ups for the coordinator.
6. The `gh api -f q=` 404 failure is recorded above. It cost no quota
   block, but the cause on this gh build is not diagnosed beyond the
   working URL-form fix.
7. No git push, commit, or branch switch was made in this lane.

## Evidence index

All raw captures live under:

- `data/lanes/agent-egress-broad-hunt/raw/github-code/`

Per query: `<id>.json` (full API response), `<id>.json.PROVENANCE.txt`
(source, query, retrieval time in UTC, method), `<id>.json.sha256`.
Directory checksum file: `SHA256SUMS` (verified: all 16 OK).
Query script (idempotent, skips existing captures):
`data/lanes/agent-egress-broad-hunt/run_queries.sh`.
