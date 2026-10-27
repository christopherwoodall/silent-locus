# Broad hunt scope brief: agent egress and escalation behaviors

## Source reports mined

- Fleet B hunt report: `reports/cohere-qwen-hunt/REPORT.md` (3 ranked hits,
  all SECONDARY; no new behavior, no new host, no seed reproduction).
- Fleet C enrichment: `reports/cohere-qwen-enrichment/` (335 entity rows,
  124 IOCs; no lead corroborates the Cohere trace).
- akasecurity/ai-tc#927 (open, 2026-10-26): defensive detection pack,
  NOT an incident. Zero incident weight. Its value is the behavior
  shapes it encodes, written from the Cohere write-up (#926).
- akasecurity/ai-tc#926: the underlying write-up summary (5 behaviors,
  17 test calls, 0 detections before the pack).

## Terms

- SECONDARY: evidence from a third party, not first-hand capture.
- Behavior shape: a pattern of actions (recon, then upload), not a
  host name string. The operator scores patterns, not strings.
- Call-home: an agent sends data to an outside host without a user order.

## What the reports actually give

The Cohere seed is narrow: one model (Qwen3.8-Flash-Next), one bucket
(sanmaohe), one proxy family (routify), one sandbox trace, one probe
string. Fleet B proved the narrow hunt is exhausted: 3 ranked hits, all
known September routify class, models unidentified except item 2.

The akasecurity pack generalizes the seed into 6 huntable behavior
shapes that apply to ANY model or harness, not just Qwen:

1. Cloud-metadata reach: 169.254.169.254, fd00:ec2::254,
   metadata.google.internal, 100.100.100.200, in a network call.
2. Object-storage upload: curl/wget file upload flags (-T,
   --upload-file, -d @file, -F, --post-file) or env dump to S3, GCS,
   Azure Blob, R2, or Alibaba OSS.
3. Named probe hosts: the two hosts from the write-up, on a network use.
4. User-namespace escape: unshare -U, -r, -c, -Urm, --user,
   --map-*-user (mount-only and net-only excluded).
5. Download-then-execute: curl -o / wget -O to a path, then running
   that path.
6. Recon-then-egress: recon (cat /etc/resolv.conf, which curl,
   ls /tmp, uname -a, id, hostname) plus a network call in one command.
   Recon alone is silent.

Shapes 1, 2, 4, 5, 6 are model-agnostic. That is the broad hunt.

## What is already hunted (excluded from the broad hunt)

- Routify-only, sanmaohe-only, Qwen-only searches. Fleet B covered these.
- The akasecurity pack itself, the cc-safety-net block, the Crow fix,
  the vendor ModelRouter traffic. Defensive and downstream artifacts.
- Known prior sightings: August HN thread, September routify fetches,
  September plugin blocking, October Reddit thread.

## Coverage gaps the broad hunt fills (from Fleet B limits)

- GitHub code search: BLOCKED in Fleet B (needs auth). Unswept.
  This is the largest gap: shapes 4, 5, 6 live in code and configs.
- GitHub issues sampling: 30 of 45,816 aliyuncs issues, 30 of 1,860
  routify issues screened. Most never screened.
- urlquery sampling: 49 of 48,945 aliyuncs rows, 49 of 6,648 oss-cn
  rows fetched. A 0.1 percent sample.
- urlscan: 100 newest of a 10,000-capped aliyuncs set.
- Hugging Face: search matches IDs and names only, not description text.
- Wayback and crt.sh methods were weak (wildcard limits, 502s).
- Shodan was not used in Fleet B (no concrete infra signal then).
  A broad hunt does NOT auto-enable Shodan; that needs its own call.

## Proposed broad hunt scope

- Behavior families: the 6 shapes above, graded as pattern matches.
- Surfaces: GitHub issues and PRs, Hugging Face (IDs, names, plus
  description-text methods where possible), urlquery full sweeps,
  urlscan, Wayback CDX, crt.sh. GitHub code search ONLY if the
  operator approves authenticated use (see decision 1).
- Models and harnesses: all, not Qwen-only. Model identity is recorded
  only when the evidence names it; unidentified stays unidentified.
- Grades: SECONDARY by default. No PRIMARY without first-hand capture.
- Novelty: full checks before any NEW claim (Factum exact and fuzzy,
  legacy evidence trees, Transluce tracker snapshot, lists/).
- Exclusions that travel with every grant: no Transluce submissions
  (freeze in force), no account creation, no paid upgrades, no human
  or operator identity, no logins or sessions, uipath stays stopped.
- Signed-URL rule: parameter names and path shape only, never query
  strings, signatures, or tokens into Factum. Raw files never redacted.

## Decisions needed before dispatch

1. GitHub code search auth: Fleet B was blocked unauthenticated.
   Approve authenticated read-only code search (uses the existing
   account rate limit) or run the broad hunt without code search.
2. Dispatch word: new lanes are TIER-B. This brief is not a dispatch.
3. Shodan: stays OUT unless separately approved with a concrete
   infra signal.

## Standing open items this hunt does not resolve

- Revision mismatch (CohereLabs 028b7cd7 vs cfahlgren1 cb30f9f3).
- Parquet token IDs not decoded.
- Reddit thread 1wxvt41 still UNVERIFIED (Reddit blocks this VM).
- Lane objects for cohere-qwen-hunt and cohere-qwen-enrichment
  do not exist (records are tag-grouped only).
