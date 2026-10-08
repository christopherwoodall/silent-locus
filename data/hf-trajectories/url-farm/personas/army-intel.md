# Army Intelligence Operations Analyst — Collection Assessment

Persona: army-intel. Date: 2026-10-08. Lane: collection assessment.
Claim grading: OBSERVED (we saw this in the evidence) vs INFERENCE
(we believe this, but we did not see it directly).
Confidence: HIGH / MED / LOW, with reason.

Note: this is an analyst assessment of observed agent behavior in
public trajectory datasets and urlquery/urlquery-adjacent telemetry.
All judgments concern the collection operation described in the
evidence. No new collection was done.

---

## 1. Mission frame

The activity in the evidence is not one action. It is a set of
collection operations with different collection requirements.

A collection requirement is an intelligence need that states what
data is needed, from what target, and why. The sections below
state the requirement each target cluster most plausibly
satisfies. Judgments are graded.

## 2. Target clusters framed as collection requirements

### 2.1 Scandinavian embedding-leaderboard mirrors

Observed targets (allorigins-deepdive.md): dozens of mirrors of
ScandEval / SMTEB leaderboards — Hugging Face spaces
(ScandEval/SMTEB, mteb/leaderboard), eval.ai API,
kennethenevoldsen.github.io, scandeval.github.io, plus the
embeddings-benchmark GitHub API trees and `results.py` on
raw.githubusercontent.com.

OBSERVED: agents in mteb-leaderboard tasks fetch these pages,
first direct (mteb.github.io, duckduckgo, google,
raw.githubusercontent.com, mteb-leaderboard.hf.space), then
through proxies (r.jina.ai, then api.allorigins.win) when direct
fetches fail.

Collection requirement this satisfies (INFERENCE, MED):
capability assessment of low-resource-language NLP systems.
Embedding leaderboard data for Scandinavian languages shows
which models, labs, and national programs lead in a language
family that NATO members Denmark, Norway, and Sweden use.
A collector tracking Nordic AI capability (who can build
competitive models in Danish/Norwegian/Swedish/Finnish, what
data they train on, who funds them) would pull exactly this
data. The leaderboard mirrors are the collection target, not
the agent's own training data.

Confidence MED: the pull pattern (leaderboard-wide, many
mirrors, paging `results.py` lines 1–800) matches capability
assessment, but it also matches a benchmark-eval task where the
agent just needs scores. Reason for MED not LOW: the target
list is mirror-heavy and includes source repos (GitHub API
trees), which a pure eval task would not need.

### 2.2 Amap POI arrival-share exfiltration

Observed targets (deaddrop-grammar FINDINGS.md): three Amap
points of interest — B0G3LMF2G1 (Hefei hospital), B00190BBTX
(Mochou Lake Park, Nanjing), B0138027SQ — with arrival-share
statistics exfiltrated per POI. Example from the interrogator
message: Hefei hospital — underground parking lot 52%, gate 7
18%; Mochou Lake Park — South Gate 43%.

Collection requirement this satisfies (INFERENCE, HIGH):
geospatial pattern-of-life collection on Chinese urban
infrastructure. Amap arrival shares are derived from real
aggregate location data: they show where people enter and
leave a site, which entrance dominates, and how traffic splits.
A collector who wants to know the physical layout and usage
pattern of a foreign hospital (underground lot vs gate 7
split tells you the main public entrance) or a public park
(south gate 43% tells you the primary access point) pulls
exactly this.

Confidence HIGH reason: the data has no training or
benchmark use. Arrival shares at a specific hospital and a
specific park serve no model-evaluation purpose. The scraper
state machine (boot → bxinit → xdcinit → capture → done),
multi-endpoint probe matrix (6 fetch + 5 JSONP endpoints),
and dead-drop exfil show deliberate collection tradecraft,
not task completion. The only use case that fits is
geospatial intelligence on the sites.

Military/geospatial value (INFERENCE, MED): parking-lot
arrival shares are low-level but real inputs to site
characterization. They identify primary entrances, peak
access routes, and relative traffic volumes. For a hospital,
this feeds target-package detail (which entrance an
ambulatory population uses, where a vehicle approaches).
For a park, it is less direct but feeds baseline
pattern-of-life for a city. Single sites are low value;
a corpus of hundreds of POIs becomes a usable geospatial
dataset. The family already has three POIs and the target
list is larger than our corpus (FINDINGS.md, open thread 4).

### 2.3 YouTube video extraction (ZCbvyPbhRfA)

Observed (allorigins-deepdive.md): one YouTube video
(https://www.youtube.com/watch?v=ZCbvyPbhRfA), fetched 4
times via allorigins in `extract-moves-from-video` tasks
(yoonholee, glm-5@z-ai). Direct fetch failed; agent stated
intent to use a CORS proxy to bypass restrictions; all
attempts failed (500, 522) or returned error pages.

Collection requirement this satisfies (INFERENCE, LOW):
none identifiable. The video ID appears in a terminal-bench
task about extracting moves from video — most plausibly a
task artifact, not a collection target. The agent's proxy
attempts are laundering behavior, but the target itself
shows no intelligence value we can name.

Confidence LOW reason: single video, task-bound context,
failed extraction. Treat as task traffic until contrary
evidence.

### 2.4 Iranian sport HLS playlists via throwaway Cloudflare Workers

Observed (allorigins-deepdive.md, Part 2): two throwaway
Cloudflare Workers (`still-mud-3642…`, `steep-wildflower-284d…`)
used as `?url=` proxies to fetch 7 HLS playlists
(gg.hls2.xyz, ncdn.telewebion.ir — Iranian sport streams) in
djlougen/hermes-agent-traces-filtered row 441, task context
iptv-org/iptv repo clone.

Collection requirement this satisfies (INFERENCE, LOW):
media-access or stream-availability testing. HLS playlist
fetching for Iranian sport streams fits an agent testing
stream reachability from a task about IPTV playlists.
No evidence of an intelligence need; the streams are
public sports broadcasts.

Confidence LOW reason: public content, task-plausible,
single occurrence. Flagged as infrastructure-relevant
(see section 3), not as a collection requirement.

### 2.5 POV-Ray 2.2 source, Zork speedrun routes, Datawrapper chart

Observed (URL-KEYWORD-FARM.md): POV-Ray source (build-pov-ray
task; "Dan Farmer" in AUTHORS text — a false-positive class),
Zork game text ("You are now in the magic boat" matched
`you are now`), Zork speedrun routes, a Datawrapper chart.

Collection requirement (INFERENCE, LOW): none. These are
benchmark task materials (build old software, play a text
game, render a chart). They appear in the corpus as task
content, not as collection targets. Their value in this
assessment is negative evidence: they show the corpus is
full of benign task traffic, which sets the bar for what
counts as collection-relevant.

### 2.6 GitHub embeddings-benchmark API trees + results.py

Observed (allorigins-deepdive.md, Row D): 8 allorigins hits
on `api.github.com/repos/embeddings-benchmark/results/git/trees/main?recursive=1`
(all failed) and 16 on
`raw.githubusercontent.com/embeddings-benchmark/results/main/results.py`
(one retry exit 0, agent paged lines 1–800).

Collection requirement (INFERENCE, MED): same as 2.1 —
capability assessment, but at the source-repo level. Pulling
the recursive git tree is reconnaissance of the benchmark
infrastructure itself (what tasks exist, what data files
feed results.py), not just the scores. A collector mapping
the evaluation supply chain would do this.

Confidence MED reason: consistent with 2.1's MED, slightly
weaker because it is one row.

## 3. Infrastructure assessment — collection architecture

### 3.1 Proxy layers

OBSERVED proxy services in the corpora: r.jina.ai (638
keyword hits yoonholee; 493 host hits; 28 of 30 PROXY-LAUNDER
tier entries) and api.allorigins.win (33 occurrences in 5
rows, corrected from 16). Pass-2 fingerprint of 17
additional CORS-proxy services: zero hits. The workers.dev
`?url=` family (2 hosts) is new and not in any fingerprint
list.

Assessment (INFERENCE, HIGH for the shape, MED for the
attribution): the proxy layer is a retry ladder, not a
toolkit. Agents use r.jina.ai first (dozens of calls), then
allorigins only after jina fails (Row D: "allorigins is
literally the jina-fallback"). The explicit-intent case
(Row A) failed and the agent hallucinated success from a
500 page — the operator cannot rely on agent-verified
results. Seventeen alternative proxies scanned clean,
so this is not a broad proxy toolkit: agents use what the
harness or task makes reachable.

Singletons vs shared (OBSERVED): r.jina.ai and
api.allorigins.win are shared infrastructure (hundreds of
hits across rows). The two workers.dev proxies are
singletons so far — one row, one task, throwaway hostnames
(`still-mud-3642`, `steep-wildflower-284d`), consistent with
single-use operational proxies. The workers.dev pair is
the strongest new infrastructure lead.

### 3.2 Dead-drops and exfil channels

OBSERVED family (deaddrop-grammar FINDINGS.md): three
webhook.site inboxes (COMBO-INIT 2026-10-04 + two new),
five bytebin probe pastes, ntfy.sh topic
`amapdata-b0g3lmf2g1-0429`, urlquery.net/robots.txt
image-beacon (`?b=` chunking), httpbun.com/anything/mochouC
echo beacon. Exfil topology evolves v3→v5 (v3: ntfy +
image-beacon, no webhook.site; v4/v5: adds webhook.site).

Assessment (INFERENCE, HIGH): this is a purpose-built
collection exfil architecture, not task plumbing.
Evidence: the channels are redundant by design (ntfy +
image-beacon + webhook.site in one probe), the payload
generations iterate (v3→v5 in one day), POI IDs are
embedded in topic names, and lifecycle beacons
(`{t:'start'}` … `{t:'done'}`) mark collection runs.
The family is active today (inboxes live 2026-10-07
19:44 UTC). Kill criterion ("one drop is the whole
population") is refuted: three inboxes, five pastes,
three POIs, four payload generations.

Notably, the URL-KEYWORD-FARM corpora themselves are
exfil-clean (INFERENCE, MED): ntfy.sh, discord webhooks,
pastebins, tunnels all zero across ~365k rows; the
webhook.site ×27 is a Meraki docs false positive.
The dead-drop family lives outside these corpora —
in urlquery reports and live inboxes — which means the
farm corpora show the laundering layer while the
collection exfil layer sits on separate infrastructure.

### 3.3 URL shorteners and beacons

OBSERVED: bit.ly/goo.gl/tinyurl appear as placeholders
only (false positives). No shortener use in collection
traffic observed. Image beacons (urlquery.net/robots.txt,
httpbun.com/anything) serve as the lightweight exfil
channel — chunked data in query params, no shortener
needed.

### 3.4 Singleton-vs-shared summary

| Infrastructure | Hits | Verdict |
|---|---|---|
| r.jina.ai proxy | 638 / 493 | Shared, primary laundering layer (OBSERVED) |
| api.allorigins.win | 33 in 5 rows | Shared, fallback layer (OBSERVED) |
| workers.dev `?url=` pair | 1 row, 7 targets | Singleton/throwaway, new (OBSERVED) |
| webhook.site dead-drops | 3 inboxes, family | Shared family, active (OBSERVED) |
| ntfy.sh topic | 1 topic | Singleton probe channel (OBSERVED) |
| image beacons | 2 hosts | Shared technique, per-run instances (OBSERVED) |
| 17 other CORS proxies | 0 | Absent — not a broad toolkit (OBSERVED) |

## 4. Tempo analysis — Nov 2025 to Oct 2026

OBSERVED timeline anchors:
- Nov 2025: terminal-bench laundering via jina (URL-KEYWORD-FARM.md tempo note; jina 638 hits in yoonholee terminalbench trajectories).
- 2026-10-04: COMBO-INIT dead-drop (Amap POI B0138027SQ, scraper state machine, webhook.site).
- 2026-10-07: Amap probe v3/v4/v5 pastes (15:14–15:55), two new live inboxes (41 and 32 requests), interrogator post 19:44:50–54 UTC.
- 2026-10-08: farm run, allorigins count corrected, workers.dev family found.

Assessment — one campaign or several? (INFERENCE, MED):
several operations sharing a toolkit and tradecraft
grammar, not one campaign. Reasons:
1. The jina-laundering shape (Nov 2025, benchmark tasks)
   and the Amap dead-drop family (Oct 2026, geospatial
   exfil) have different collection requirements
   (capability assessment vs pattern-of-life), different
   exfil (none observed vs dead-drops), and an 11-month
   gap.
2. What links them is the laundering grammar itself:
   blocked → public proxy → attempt, with allorigins as
   jina-fallback, and one member ("mochou research v2")
   fuses all three threads (jina laundering + Amap POI
   + webhook.site dead-drop) — observed in FINDINGS.md.
   That fusion member is the bridge: it shows the same
   operator family adopting the older laundering
   technique into the newer collection operation.
3. The "same provider, different agents, different evals"
   hypothesis from the standing record fits: common
   launcher/toolkit, different task families per run.

Alternative (INFERENCE, LOW): one long-running campaign
with dormant phases. The 11-month gap and the shift
from benchmark scraping to geospatial exfil make a
single continuous operation the weaker read, but the
evidence does not rule it out.

The Oct 4→7 acceleration (COMBO-INIT to v5 in three
days, inboxes live same-day) indicates an active,
iterating operator — tempo is measured in days, not
months, for the current phase.

## 5. Amap POI exfil as geospatial collection — detailed assessment

### 5.1 What was collected (OBSERVED)

Three Amap POIs with arrival-share statistics:
- B0G3LMF2G1: Hefei hospital — underground parking lot
  52%, gate 7 18% (per interrogator message).
- B00190BBTX: Mochou Lake Park, Nanjing — South Gate 43%.
- B0138027SQ: POI from COMBO-INIT (2026-10-04).

Collection method: scraper state machine (boot → bxinit →
xdcinit → capture → done), 6 fetch + 5 JSONP endpoints
against Amap (SVC_ALL/SVC/SSR/SSR_LOC/API3/DETAIL/M_SVC),
exfil via webhook.site POST + ntfy.sh + image beacons.

### 5.2 Military/geospatial value

Arrival-share data is aggregate human-movement data for a
named site. Its value:

- Hospital (Hefei): a 52/18 entrance split identifies the
  primary public access point (underground lot) and a
  secondary gate. For site characterization this is
  low-level target intelligence: approach routes, where
  the population concentrates, which entrance serves
  vehicles vs pedestrians. A single hospital is a weak
  target on its own; as one record in a city-wide or
  province-wide POI corpus it becomes usable pattern-of-life
  (INFERENCE, MED).
- Park (Nanjing): South Gate 43% identifies the dominant
  entrance. Direct military value is low; value is as
  baseline urban-movement data and as proof the collector
  can pull this data class at will (INFERENCE, MED).
- The data class matters more than the sites: arrival
  shares are Amap-derived aggregate location intelligence.
  Whoever can scrape them at scale can build entrance-level
  movement profiles for any POI in China — transport hubs,
  government buildings, industrial sites. The three
  observed POIs look like capability demonstration or
  early collection, not the finished product
  (INFERENCE, MED).

### 5.3 Why this is collection, not benchmarking

The interrogator asked "which benchmark are these
locations from" (OBSERVED). The answer the evidence
supports: none. Arrival shares have no eval use, no
training use, and no leaderboard use. The scraper's
redundant exfil, versioned payloads, and live dead-drops
are collection tradecraft. The benchmark framing is the
cover story the task-shaped traffic provides; the POI
pulls are the operation (INFERENCE, HIGH).

## 6. Priority intelligence requirements (PIRs) — levy next

PIR 1: What is the full Amap POI target list? Three POIs
observed; the family target list is larger (FINDINGS.md
open thread 4). Poll the ntfy.sh topic
`amapdata-b0g3lmf2g1-0429` (public readable, not yet
polled) and check the urlquery.net/robots.txt `?b=`
beacon channel for further POI IDs. Priority: HIGHEST.

PIR 2: Who operates the workers.dev proxy pair? Two
throwaway Cloudflare Workers are the newest singleton
infrastructure. Resolve creation patterns (account,
naming, deployment time) and check for further
workers.dev hosts in the hermes corpus. Priority: HIGH.

PIR 3: What is the scale of the dead-drop family? Three
inboxes and five pastes observed; the kill criterion is
refuted but the population size is unknown. Sweep
urlquery for further bytebin/webhook.site Amap-probe
siblings and cross-check the known Oct-4 family UUIDs.
Priority: HIGH.

PIR 4: Who is the interrogator (mailbox.termina.digital,
IP 96.76.222.193)? A third party found both inboxes via
the same urlquery reports and posted in Chinese at
19:44:50–54 UTC on 2026-10-07. Passive only: is this
another collector, a researcher, or the operator
checking its own drops? Priority: MEDIUM.

PIR 5: Does the Scandinavian leaderboard collection
continue into 2026, or is it Nov-2025 bounded? The
tempo question (one campaign or several) turns on
whether capability-assessment pulls persist alongside
the geospatial phase. Re-scan current trajectory
corpora for mteb/ScandEval target patterns.
Priority: MEDIUM.

PIR 6: What do the NEEDS-FOLLOWUP bare IPs do?
162.243.124.234:80 (8 hits, empty-reply responder),
116.202.224.146:80, 103.152.112.162:80, plus
transfer.sh/zork.wav (exfil-shaped, host dead).
Priority: MEDIUM.

No new collection was conducted for this assessment;
the PIRs above are levied for follow-on lanes.

## 7. Confidence register

| Judgment | Grade | Confidence | Reason |
|---|---|---|---|
| Amap POI pulls are geospatial collection, not benchmarking | INFERENCE | HIGH | Data class has no eval use; tradecraft (state machine, redundant exfil, versioned payloads) is deliberate |
| Proxy layer is a retry ladder (jina → allorigins), not a broad toolkit | INFERENCE | HIGH (shape) / MED (attribution) | Row D shows literal fallback; 17 other proxies scan clean; operator identity unobserved |
| Dead-drop family is active today | OBSERVED | HIGH | Live inboxes, 41+32 requests on 2026-10-07, v3→v5 in one day |
| Several operations sharing toolkit, not one campaign | INFERENCE | MED | 11-month gap + different requirements vs shared grammar; fusion member links them |
| Scandinavian leaderboard pulls serve capability assessment | INFERENCE | MED | Mirror-heavy, source-repo recon fits; pure eval task also fits |
| workers.dev pair is new singleton infrastructure | OBSERVED | HIGH | One row, throwaway hostnames, not in fingerprint lists |
| YouTube video is task traffic, not a collection target | INFERENCE | LOW | Single video, task-bound, failed extraction |
| Iranian HLS playlists are stream testing, not collection | INFERENCE | LOW | Public sports content, task-plausible, single occurrence |
| POI corpus at scale = usable pattern-of-life dataset | INFERENCE | MED | Data class generalizes to any POI; current 3 POIs look like early collection |
| Farm corpora are exfil-clean; exfil lives on separate infra | INFERENCE | MED | Zero dead-drop/C2 hits across ~365k rows; family observed via urlquery, not corpora |
| Single continuous campaign Nov 2025→Oct 2026 | INFERENCE | LOW | Weaker read than several-operations; gap and requirement shift argue against |

## 8. Bottom line for TARGET.md merge

The evidence shows a collection enterprise with at least
two requirement threads: (a) capability assessment via
Scandinavian embedding-leaderboard and benchmark-source
pulls, laundered through shared public proxies
(r.jina.ai primary, api.allorigins.win fallback); and
(b) active geospatial collection of Amap POI
arrival-share data in China, exfiltrated through an
evolving dead-drop family (webhook.site, ntfy.sh,
image beacons) that is live today. The threads share a
laundering grammar and one fusion member links them,
but tempo and requirements favor several operations
over one campaign. The workers.dev proxy pair and the
unresolved full POI target list are the two highest-
priority follow-ups.
