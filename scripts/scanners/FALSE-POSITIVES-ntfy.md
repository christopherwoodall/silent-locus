# FALSE-POSITIVES.md — Lane 3 (ntfy.sh Amap fleet topic monitor)

What benign activity could match each detection rule, and how the scanner
mitigates it.

## 1. A message appears on the known topic `amapdata-b0g3lmf2g1-0429`

Benign: ntfy.sh topics are public and unauthenticated — anyone who knows
the topic name can POST to it. The topic name is published in hunt
writeups (deaddrop-grammar FINDINGS.md), so a researcher, the "mailbox.
termina.digital interrogator" (observed 2026-10-07), or a copycat could
post there. A message is evidence of SOMEONE using the channel, not
proof it is the fleet.
Mitigation: the scanner scores message CONTENT (`amap_mention`,
`poi_id`, `fleet_grammar`, `claude_label`) and only emits on >= 1
content match; HIGH confidence needs >= 2. Attribution to the fleet
still requires out-of-band evidence (message timestamps matching known
probe runs, POI ids matching the fleet's target list). Record the
message verbatim; do not redact.

## 2. Content rules match an unrelated message

- `amap_mention`: the word "amap" appears in unrelated contexts
  (e.g. someone testing whether ntfy works by posting a URL). Low
  specificity on its own → MEDIUM at best, and only in combination.
- `poi_id` (`B0[A-Z0-9]{9}`): the POI id grammar is Amap-specific and
  high-specificity; a random poster is unlikely to emit valid POI ids.
  This is the strongest single rule.
- `fleet_grammar` (`uqscan|uqframe|nfy(|webhook.site`): matches if a
  message discusses or copies the fleet's tooling — including a
  researcher quoting it. Context matters: a message that IS a probe
  result vs a message TALKING ABOUT probes look identical to regex.
  Read the body before attributing.
- `claude_label`: self-identification; spoofable, used by honest
  researchers too.

## 3. Topic-discovery false positives

Candidate patterns (`amapdata-*`, `fleet-*`, `uqscan-*`, `bcc-mort*`)
are guesses. `fleet-*` and `uqscan-*` are generic enough that unrelated
parties could own such topics. A discovered topic is a LEAD, not a hit:
the scanner only emits hits from message content on known topics, never
from topic-name existence alone. CDX prefix lookups document historical
existence; they say nothing about who owns the topic today.

## 4. Transport gap != clean negative (the big one)

ntfy.sh is blocked at our egress (verified 2026-10-14, HTTP 000) and
the r.jina.ai relay also fails for ntfy.sh (422). A scan that only
reaches the gap outcome emits ZERO hits and must be reported as
"unknown (transport blocked)", NEVER as "no fleet activity". The gap is
logged on stderr and embedded in hit provenance when partial data
exists. Wayback CDX is the only working fallback and it shows
HISTORICAL captures only (currently: none for the known topic).

## 5. Retention window truncation

ntfy.sh free tier retains ~12h. A `--since-hours 24` scan can only ever
see the last ~12h; messages older than that are invisible, not absent.
The scanner prints a note when the window exceeds 12h. Do not claim
"nothing in 24h" — the honest claim is "nothing in the retained window".

## 6. Polling semantics

`?poll=1` returns all retained messages; the scanner filters by the
`time` field against the window cutoff. Clock skew between ntfy and us
is small (both NTP) but a message exactly on the boundary may be
counted in two adjacent runs — dedup keys (`ntfy:<topic>:<id>`) make
this harmless.

## Residual risks (accepted)

- The fleet's v4/v5 grammar dropped ntfy in favor of webhook.site
  inboxes; the known topic may go permanently silent while the fleet
  continues elsewhere. Silence on this topic is not fleet death.
- New topics use unknown names; discovery is limited to guessed
  patterns plus archive history. A topic named outside the patterns is
  invisible to this lane until observed elsewhere (e.g. inside a
  urlquery-submitted payload — which is why lane 1 feeds lane 3).
