# ADVERSARIAL-v3 — adversarial review of monitorable-surfaces-ENRICHED-v3.xlsx

Reviewer: adversarial lane. Date: 2026-10-23 (America/Chicago).
Scope: read-only on the .xlsx. No cells written. No subagents.

## Verdict

**0 killed. 8 downgraded. Everything else attacked survived.**

The v3 build is honest work. The scrub is complete (0 self-referential
`github.com/christopherwoodall/silent-locus` URLs remain in any visible
sheet — verified by full scan), the INTERNAL lineage sheet preserves every
removed value, dead links are flagged on their rows, and the four
re-tallied counts trace exactly to trajectory-domains.md. The downgrades
below are real but none breaks a row's core claim.

---

## KILLED

None. Kill criterion: a kept direct link that does not support the row's
claim, or a row left with no sourcing and no honest flag. 25 URLs
re-fetched independently (list in Method). Every kept link either supports
its row's claim or the row already flags the problem (dead link,
UNCONFIRMED, unattributed). No kill warranted.

---

## DOWNGRADED

### D1 — Row 4, col F: scrub left a nonsense fragment
Cell reads: `Submit URL -> rendered scan and report | */raw/, scanner state`.
The v2 value was `data/lanes/urlquery-*/raw/`; the scrub regex stripped
`data/lanes/urlquery-` but could not match the `*`, leaving `*/raw/`.
A corporate reader sees a broken glob, not a path. Meaning is recoverable
from the INTERNAL sheet (row 2), but the visible cell is damaged. Only
residue of its kind in the workbook (scanned all changed POI cells).

### D2 — Rows 4, 7, 9, 11, 66, 67, 68: counts contradict the workbook's own cited source
The v3 re-tally reconciled rows 31/32/34/35 to trajectory-domains.md
(2026-10-19) but left seven other rows carrying counts that disagree with
that same file:

| Row | Domain | v3 count | trajectory-domains.md |
|-----|--------|----------|----------------------|
| 4 | urlquery.net | 2,341 | 2,321 |
| 7 | r.jina.ai | 803 | 636 |
| 9 | markdown.new | 366 | 328 |
| 11 | httpbin.org | 39 | 27 |
| 66 | anna.fyi | 179 | 177 |
| 67 | paste.linuxiarz.pl | 295 | 269 |
| 68 | pastebin.k4be.pl | 229 | 228 |

Rows 27/28/29/30/33/36/37/38/39/40/69 all match the file. So the workbook
now has two tiers: 4 stamped rows reconciled to the cited source, and 7
rows whose numbers contradict it — including r.jina.ai (Δ167), a larger
absolute gap than any of the fixed rows. The Notes disclose "a corpus-wide
re-tally awaits the next regeneration of that source," which is honest
about incompleteness, but a reader who cross-checks will find the workbook
disagreeing with its own authority. The "irreproducible error" framing for
row 34's 248 is defensible (see Survived S6), but the selective
application is the weakness, not the 248 call itself.

### D3 — Row 14 (DSEWiki): verdict is correct, but the Direct Links cell carries no surface URL
I verified the resolution independently and it is decisive, not a coin
flip (see S4). The defect: col K still contains only
`https://d3ncjnql1bmhe8.cloudfront.net/findings/42`. Neither
`prowiki.org/dse/wiki.cgi` (incident-time host) nor `wikiservice.at/dse`
(current host, HTTP 200, title "DseWiki: StartSeite" — fetched myself)
appears in Direct Links. The row asserts a canonical-host resolution the
reader cannot click through to check. Pre-existing gap (v2 K14 was the
same), but v3 resolved the name without adding the resolved URL — a missed
step, not scrub damage.

### D4 — Row 34: AGENT_COLONY judgment call is not surfaced on the row
The v2 role was "Agent swarm surface". The v3 maps it to AGENT_COLONY
("colony-style agent collectives and governed agent communities"). The
evidence on the row — "agent swarm surface; urlquery/tag scans" plus an
adjacent-lead note — does not establish a collective or governance. Notes
r218 admits "swarm treated as a collective" is a judgment call, but the
row's own Review flag (R34) mentions only the count reconciliation. A
corporate reader sees AGENT_COLONY with no caveat. The judgment is
documented — just not where the reader looks.

### D5 — Row 39 (jotspot.io): COORDINATION_LOG overclaims vs the row's own evidence
The Seen text: "Transluce #37: Jotspot page 'Economics reference reading
2012' as candidate research artifact (AI involvement and coordination
unconfirmed)". One page, AI involvement explicitly unconfirmed — yet Role
asserts COORDINATION_LOG ("public agent log/message archives, conversation
mirrors"). The v2 role ("Public agent-conversation board, cross-board
conversation guides") already overclaimed; the v3 prefix-match mapping
('Public agent…' → COORDINATION_LOG) laundered the overclaim into the
controlled set instead of correcting it. jotspot.io itself (fetched: "New
Jot | JotSpot" — shareable-notes app) is closer to a publish venue than a
log archive.

### D6 — Row 94: TEMP_FILE_HOST assigned to a placeholder with no endpoint
Row label: "Public object storage (no specific endpoint established)".
No URL, no hits, no evidence. The glossary's own UNCONFIRMED term is
defined as "named in reporting but role not established… or no specific
service identified" — a literal description of this row. The mechanical
mapping assigned TEMP_FILE_HOST anyway ('Possible persistent storage' →
TEMP_FILE_HOST; Notes r218 admits it "could equally sit in
ARTIFACT_REGISTRY"). A concrete functional role on a row with zero
established function misleads.

### D7 — "Internal corpus hits" counts are frozen snapshots, most without source stamps
Only rows 31/32/34/35 carry "(per trajectory-domains.md, 2026-10-19)".
Rows 27/28/29/30/33/36/37 cite the same source in J but without the stamp
(inconsistent labeling, same numbers — verified all match). The remaining
counts (2,341; 803; 366; 39; 179; 295; 229; 813…) are legacy Factum tallies
with no as-of date. The relabel from "Factum records" to "Internal corpus
hits" is per the operator's rule and documented, but the new label implies
a single coherent current corpus count — which D2 shows is not the case.
Recommend an as-of stamp or the existing source-stamp pattern on every
counted row.

### D8 — Two count phrasings from the two scrub regexes
"N Internal corpus hits" (rows 4, 31, 32…) vs "Internal corpus hits N"
(rows 39, 40, 65, 66, 67, 68…). Cosmetic, but a corporate reader will
notice. One form should win.

---

## SURVIVED

### S1 — Substitutions (25 URLs re-fetched, one at a time, curl GET)
Every kept direct URL was re-fetched independently of the substitute lane.
Results:

- **Support the claim (200 + matching content):** any.run ("ANY.RUN -
  Interactive Online Malware Sandbox"), developers.cloudflare.com/workers/playground/
  ("Playground · Cloudflare Workers docs"), agentgateway.pythonanywhere.com
  (404 "Coming Soon" — exactly matches the row's "mcp.json dead" note),
  commonlog.ai (200; body carries /a/&lt;ID&gt; agent-log links),
  public-board.com (200; body is timestamped message-board posts),
  github.com, gist.github.com, anna.fyi ("Pastebin courtesy of Miss Anna"),
  paste.rs (200 on retry — first attempt returned 000, transient egress;
  "Rocket Powered Pastebin"), gritpost.com, gotit.pub, mcbin.dev,
  bytebin.lucko.me, bytebin.rkslot.nl, hermes-agent.nousresearch.com,
  yourls.org (YOURLS site), fallback.chat ("a public board for AI agents";
  /llms.txt 200), artifactcouncil.com/llms.txt (200),
  joinsnail.com ("SNAIL — Social Network for Autonomous Intelligent Life"),
  agentsspeakup.com ("AI agent reporting & commitments"), agenttavern.dev
  ("Agent Tavern"), swarmsay.com, robots.wiki, agentcolony.one (all 200,
  agent-board titles).
- **Flagged-dead, flags confirmed accurate:** agents-relay.com (000, empty
  reply — matches R45), agent-community.com (HTTP 500 — matches R51),
  porkpad.com (000 — matches R75/R84), friendpaste.com (503 "Maintenance" —
  matches R93), pasteview.com (403 Cloudflare "Attention Required" —
  matches the R75/R85 caveat verbatim), messageboardforaiagents.com (522 —
  consistent with "dark since 2026-10-21"), webhook.site inbox UUID
  28efa24e… (404 "Token not found" — matches R81's "link dead" note;
  webhook.site home itself is 200).
- No kept link contradicts its row. The dead-link flags are accurate as of
  this review.

### S2 — Scrub damage
Full v2→v3 diff of Direct Links cells: every row kept at least its surface
URL or an honest marker ("unattributed — not previously catalogued" /
"unattributed — no specific URL established"). No row lost all sourcing.
No POI cell went from non-empty to empty. Zero remaining
`github.com/christopherwoodall/silent-locus` URLs in any visible sheet
(full scan). Zero remaining bare "Factum" mentions or `data/lanes/` paths
in visible POI/Intel cells. The single residue is D1 (`*/raw/`).

### S3 — The three third-party GitHub survivals hold
Operator rule (SUBSTITUTE.md): third-party project repos are direct
sources and may stay; silent-locus repo links are self-referential and go.
Rows 60 (github.com) and 61 (gist.github.com) are the surface itself, not
our repo — rule-compliant. The L60 evidence note names
github.com/youdotcom-oss/minimax-m3-deepsearchqa-skill-eval; I verified
that repo returns HTTP 200 — the evidence is real, not laziness. Nit: the
repo URL is named in prose (L60) but not added as a clickable link in K60,
though the rule's priority order would permit it.

### S4 — Row 14 DSEWiki: the verdict is decisive, not a coin flip
Three independent lines converge on the same wiki instance, and I checked
a fourth:
1. Transluce #42 incident-source link `prowiki.org/dse/wiki.cgi` — the /dse
   instance on the prowiki.org farm at incident time.
2. LEAD-3 live capture of the same DSE wiki ForumSeite at
   `wikiservice.at/dse` (2026-10-23).
3. Nightingale Collective dump lists `wikiservice.at/dse` as the main surface.
4. My own check: Helmut Leitner's wiki list documents
   `wikiservice.at/dse/wiki.cgi` as "Deutsches Software Entwickler Wiki";
   ProWiki is the wiki engine/farm (started 2001), not the wiki's name.
   The v2 ambiguity ("DSEWiki / ProWiki") was a host-vs-instance category
   error. Live fetch: `https://wikiservice.at/dse/wiki.cgi` → HTTP 200,
   title "DseWiki: StartSeite". The wiki calls itself DseWiki.
"DSEWiki (prowiki.org → wikiservice.at/dse)" is correct. The only defect
is D3 (no surface URL in col K).

### S5 — Role-set fit (20+ rows spot-checked)
12-term set is applied to all 101 rows; definitions (Notes r129–140) are
coherent and most mappings are exact: SCAN_EVIDENCE_SERVICE (4, 5),
MALWARE_SANDBOX (6), RETRIEVAL_PROXY (7, 10, 11 — glossary explicitly
covers browser proxies, request-echo, HTTP diagnostic utilities, and
webhook-inspection, which answers the directionality question on row 81),
PUBLIC_WIKI (14, 15, 18), AGENT_BOARD (19–33, 41–56, 100, 102–104),
AGENT_COLONY (23, 35, 101 — all colony/governed-community evidence),
COORDINATION_LOG (38), ARTIFACT_REGISTRY (57–61, 63 — pkg.go.dev factually
IS a module proxy; the role describes the service, and the row's qualifiers
say "unproven"), IDENTITY_SERVICE (64, 80), TEMP_FILE_HOST (65–90 paste
rows), URL_SHORTENER (82, 83, 96), UNCONFIRMED (12, 13, 16, 17, 97, 98 —
all honest). Row 91's "worst fit" (AGENT_BOARD for a harness endpoint) is
admitted on the row itself and in Notes r218 — disclosed, not hidden.
Row 8's 'Unknown' → RETRIEVAL_PROXY is aggressive but the capability
(fetcher) is established and the residual uncertainty is flagged on the
row. Downgrades D4/D5/D6 are the exceptions, not the pattern.

### S6 — The re-tallied counts trace exactly; the "irreproducible error" is not a cover
103/16/114/53 match trajectory-domains.md (2026-10-19) Tier 1 rows
character-for-character (verified against the file). The v2 review flags
on rows 31/32/34/35 already said "Factum count predates 2026-10-23 corpus;
re-tally pending" — v2 distrusted these numbers before v3 touched them.
Calling 248 "an error… not reproducible under a consistent method" is a
fair description of a number with no reproducible provenance, and the
replacement is fully traceable. Not a cover for a bad re-tally. The real
weakness is D2: the same treatment was not applied to the other rows whose
counts disagree with the same source.

### S7 — Flagged rows are handled, not hidden
Rows 45, 51, 62, 75, 84, 85, 93, 94, 95, 97, 98: dead links, unattributed
markers, and "no specific URL established" labels are all present in
Review flag cells with check dates. The Intel sheet's row 7
(wikidata-triage internal dataset) is flagged "direct source unavailable"
with no URL invented — correct per the no-invention rule. The "117 vs
120" changelog discrepancy: v2 data cells contain exactly 117
self-referential URL instances (recounted); Notes/SUBSTITUTE.md say 120.
Minor documentation overcount; the scrub itself removed all 117.

---

## Observations (not downgrades)

- **Row 13 new information:** the substitute lane saw HTTP 307 → login
  wall; I see HTTP 200 "LiftBrand BlogFlow — SEO Blog Publishing". The
  domain now serves an unrelated SEO product. The row is UNCONFIRMED and
  flagged, so nothing is misrepresented — but this strengthens the case
  that the domain is a false positive worth dropping in a future pass.
- **Rows 91–93 have no Priority value:** pre-existing in v2 (gap-fill rows
  from the domain audit never got priorities), not v3 damage.
- **Row 78's "link dead" flag for paste.ubuntu.com** (HTTP 000) reproduces
  from this VM; likely egress filtering rather than a dead service, but
  the flag matches observation.
- **INTERNAL sheet lineage counts:** factum 155 ✓ (matches brief),
  batchid 14 ✓, github-class 80 cells vs 117 URL instances (cells ≠
  instances — consistent).

## Method

- Compared v2 → v3 cell-by-cell (Agent POIs rows 4–104, cols F/I/J/K/L/R;
  Intel data rows; Notes role table).
- Re-fetched 25 kept direct URLs with curl (one at a time, GET only, no
  logins), checking HTTP status + title/body against each row's claim.
- Independently verified the DSEWiki resolution (Helmut Leitner wiki list,
  WikiIndex ProWiki category, live fetch of wikiservice.at/dse/wiki.cgi).
- Cross-checked every "Internal corpus hits N" count against
  trajectory-domains.md.
- Scanned all changed cells for scrub residue (regex sweep for leftover
  globs, dangling separators, Factum/GitHub/lane-path remnants).
- Counted self-referential URL instances in v2 (117) and confirmed 0 remain
  in v3 visible sheets.

## Bottom line for the operator

Ship it, with D2 and D7 as the follow-ups worth doing: reconcile the seven
contradicting counts (or stamp every count with its source), fix the
`*/raw/` fragment, and put the resolved DSEWiki surface URL into K14. The
Role downgrades (D4/D5/D6) are judgment calls already half-documented in
Notes r218 — they need one line each on their rows. Nothing here
invalidates the workbook.
