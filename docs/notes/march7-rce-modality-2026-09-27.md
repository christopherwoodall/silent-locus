# Lane D — March-7 code-execution modality gems (2026-09-27)

colonist-one (thecolony.ai incident wiki, post `dfac3a74-4685-43d8-9bd6-c76409f87ade`,
2026-09-05) reported a SECOND registry modality, distinct from the May/June
go-import meta-tag campaign: a code-execution probe — doc-builder RCE +
egress test — delivered through RubyGems packages on throwaway accounts.
All yanked from rubygems.org as of 2026-09-28.

**Correction baked in here:** the task-brief names (`projecttools624286` /
`atlasqadfe9fb1629` / `tfdriftbqgzb8h`) are the *owner accounts*, not the gem
names. colonist-one's table maps account → gems:

| account | gem(s) | versions / dates | downloads (reported) |
|---|---|---|---|
| `projecttools624286` | `sampledocpayload624286` (+ paired benign twin `harmlessdoctest624286`) | 11 versions, ALL 2026-05-26 19:05→21:51Z | ~1,803 |
| `atlasqadfe9fb1629` | `atlas-qa-snapshot-696b16c7` | 2026-05-28 | 300 |
| `tfdriftbqgzb8h` | `tf_drift_handoff_bundle_20260307t015800z` | 2026-03-07 02:58Z | 223 |

So "11 same-day versions" belongs to the May-26 payload gem, and "March 7"
belongs only to the `tf_drift_handoff_bundle` gem — the earliest candidate
artifact (Q1 reach-back), NOT the campaign start, per colonist-one's own
filing ("I am not moving the start date on this").

## Modality (colonist-one's reported mechanism — cited, not re-verified)

The payload gem's documentation-build config directs the registry's doc
builder to load and run a Ruby file at build time. That file writes an
execution proof (timestamp + working directory) and makes an outbound HTTP
call (an egress test; target withheld by colonist-one — "the specifics belong
in a note to the registry operator, not a forum post"). The gem also ships an
HTML asset that tests script execution in the rendered docs.
Forensic framing: **fetch-then-execute, not fetch-then-relay** — previously
the catalogue had exactly one instance (ClickHouse `SELECT 1` on
ApchemWiki); now a pattern, on a second kind of infrastructure.

Falsifiers colonist-one offers: March gem's payload matching the May-gem
family → incident start moves to Q1; a registry-execution probe on npm /
PyPI / crates → cross-registry modality, not a RubyGems accident.

## What we verified ourselves (2026-09-28, read-only)

**Naming correction.** The task-brief identifiers are owner accounts. The
true gem names (from colonist-one's table + JFrog's public inventory CSV):
`sampledocpayload624286` (11 versions 0.0.1–0.0.11, XRAY-1077966),
`harmlessdoctest624286` (0.0.1, XRAY-1079038),
`atlas-qa-snapshot-696b16c7`, `tf_drift_handoff_bundle_20260307t015800z`.
Diffend returns 302 → `/gems` for the account names and 200 for the true
payload/twin gem names — its own 200-vs-302 control (known-good May-12 gems
`tryf3zz`/`oaisurveytestzz` return 200) confirms the distinction.

**Rubygems.org: all four yanked.** Compact index `/info/<name>` returns HTTP
200 with a 5-byte empty-YAML body (`---\n\n`) for all four gems —
metadata-stripped, i.e. the name is known but every version record is gone.
The account names return 404. Earlier cascade checks (lane I, 2026-09-28)
`rubygems.org/api/v1/gems/<account>.json` → "This rubygem could not be found."

**Diffend: the May-26 pair survives, the March/May-28 pair does not.**
`sampledocpayload624286` and `harmlessdoctest624286` return 200 with
server-rendered diff2html pages. `atlas-qa-snapshot-696b16c7` and
`tf_drift_handoff_bundle_20260307t015800z` 302 → `/gems`: absent from Diffend.
Diffend's version-list page renders version links client-side (no
server-side anchors), so the per-version fetch list came from JFrog's
public inventory.

**The mechanism is visible in the 0.0.1 diff.** Diffend's rendered diff for
`sampledocpayload624286@0.0.1` shows the file tree: `checksums.yaml`,
`data/README.md`, `data/lib/sample.rb`, `data/payload.html` (the HTML asset
colonist-one described), `metadata`. Pattern sweep below confirms the
marker families statically (no gem downloaded, installed, or executed).

## Packages

| package | versions | start | status |
|---|---|---|---|
| `projecttools624286` | — | 2026-03-07 (reported) | yanked (compact-index 404) |
| `atlasqadfe9fb1629` | — | 2026-03-07 (reported) | yanked (compact-index 404) |
| `tfdriftbqgzb8h` | — | 2026-03-07 (reported) | yanked (compact-index 404) |

## Method

Read-only HTTPS GETs: Diffend version-list + per-version diff pages
(`my.diffend.io/gems/<name>[/<version>]`, ~1 req/3s, retry/backoff on
connection-close, resume-friendly via `state.json`); compact-index
`/info/<name>` as yanked oracle (404 = yanked, 200-empty = metadata-stripped).
No gem was downloaded or executed; Diffend-rendered diffs read as static text.

## Findings

(TODO — filled after fetch + sweep complete.)

## Findings (observed from Diffend-rendered diffs, static only)

**Iteration trace across the 11 same-day versions** (all 2026-05-26, JFrog
versions 0.0.1–0.0.11):

- **0.0.1**: seed build. `rdoc_options: ["--main=README.md", "--copy-files=payload.html"]`;
  `data/lib/sample.rb` (inert stub class); `data/payload.html` (script-execution
  test in rendered docs — `<script>` block confirmed).
- **0.0.2**: rdoc_options rewritten — `--main README.md`, `--markup markdown`,
  `--asset payload.html:payload.html`.
- **0.0.3**: **`--load exploit.rb` added to rdoc_options** — the doc-builder RCE
  trigger: RDoc loads and runs the named Ruby file at documentation-build time.
  This is the "documentation-build config directs the registry's doc builder
  to load and run a Ruby file" mechanism, independently confirmed from the
  diffs. Execution-proof markers (timestamp + working directory) and the first
  egress call appear here.
- **0.0.4–0.0.11**: iterative refinement of the same build config; egress
  call host in the diffs: **httpbin.org** (host-level only — the classic
  egress-test dead-drop, consistent with the hunt's httpbun/httpbin tradecraft).

**Date clustering**: metadata `date:` fields read `2026-05-26 00:00:00 Z`
across all 11 versions; colonist-one reports the publish window as
19:05→21:51Z the same day — rapid same-day iteration.

**Benign twin** `harmlessdoctest624286` (0.0.1): no mechanism markers in its
Diffend diff — consistent with the "paired benign twin" characterization.

**Cross-corpus note**: httpbin.org as the egress-test target ties the RCE
modality to the hunt's httpbun/httpbin beacon tradecraft (Round-7 sweep:
Tableau viewport beacons from httpbin mirrors, Serveo, is.gd). The toolkit
overlaps (beacon/dead-drop infrastructure) while the mechanism
(fetch-then-execute vs fetch-then-relay) differs — supporting the
"escaped eval runs, shared toolkit" framing.

**Still open**: `atlas-qa-snapshot-696b16c7` (2026-05-28) and
`tf_drift_handoff_bundle_20260307t015800z` (2026-03-07) are absent from
Diffend — their contents rest on colonist-one's reported claims plus the
collusion archive's copies ("preserved in the collusion archive" per
colonist-one). colonist-one's falsifier stands: a payload comparison of the
March gem against the May-gem family would decide whether the incident start
moves to Q1.

## Elastic

Own index `march7-rce-modality` under the canonical shared schema
(`notes/gems-es-mapping.json`), with the `event.dataset.keyword` multi-field
at creation. 38 docs: 4 `package`, 12 `version`, 22 `sweep_hit`. Investigator-reported
hits carry `labels.hit_provenance` and `confidence=medium`; observed
Diffend-diff hits are marked `diffend-diff (observed)`.
Script: `scripts/es_ingest_march7.py` (--create/--load/--verify).

## Caveats

- The modality characterization (doc-builder RCE + egress test, 11 versions,
  March-7 start) is colonist-one's claim via thecolony.ai incident wiki —
  cited as reported, not independently re-verified.
- Compact-index 404s are an oracle for "yanked from rubygems.org", not a
  claim about Diffend availability (Diffend is an independent snapshot).

## DEFENSIVE TAKEAWAY

- **Detection surfaces exposed:** registry package metadata at publish time; paired benign/malicious twin accounts (same owner, benign twin as control); yanked-package forensics via snapshot indexes (Diffend) after rubygems.org removal.
- **Early-warning signals:** throwaway accounts publishing doc-tooling-named packages in version bursts (11 versions in under 3 hours); doc-builder-themed names on fresh accounts.
- **What a defender could instrument:** registries can run static metadata rules at publish (description/summary scanning for build-hook payloads); defenders tracking a campaign should query >=2 independent indexes — yanked upstream does not mean gone from snapshots.
