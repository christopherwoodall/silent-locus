# Elastic ingest schema — urlquery agent-activity hunt (2026-09-25)

## 1. Schema choice: ECS, with STIX 2.1 as the conceptual model

**Primary schema: Elastic Common Schema (ECS).** Rationale:

1. Elastic Security speaks ECS natively. Detection-engine indicator-match rules,
   the Threat Intelligence views, and Timeline pivoting all key off
   `threat.indicator.*` / `related.*` / `event.category:threat`. Any other schema
   would need a translation layer at ingest to be usable there.
2. ECS already embeds STIX: `threat.indicator.type` is defined as *"Type of
   indicator as represented by Cyber Observable in STIX 2.0"* with the STIX 2.0
   SCO enum as expected values, and `threat.indicator.confidence` uses the
   *"None/Low/Medium/High scale defined in Appendix A of the STIX 2.1
   framework"*. Choosing ECS does not abandon STIX — it implements the STIX
   concepts Elastic understands.
3. STIX 2.1 as a *storage* schema was considered and rejected for this pipeline:
   STIX Relationship SROs model our graph edges more elegantly than anything in
   ECS, but Elastic has no native STIX document handling — STIX bundles would
   still be shredded into ECS-shaped docs (e.g. via Elastic's own STIX→ECS
   patterns) before the Security solution could use them. The STIX→ECS concept
   map below preserves the semantics; nothing is lost.
4. OpenTelemetry: the EDOT elasticsearch exporter defaults to `otel` mapping
   mode (OTel-native docs) but supports `ecs` mode, which translates OTel
   Semantic Convention attributes to ECS fields. The OTel badges on the ECS
   reference confirm 1:1 attribute names for `url.*` (`url.full`, `url.domain`,
   `url.scheme`, `url.path`, `url.query`, ...), `@timestamp` ←
   `time_unix_nano`, `message` ← log `body`, and `labels` ← resource labels.
   There is **no** OTel SemConv for `threat.*` — threat-intel concepts exist only
   in ECS. So: emit ECS field names directly (bulk NDJSON now); if this ever
   ships over OTLP, use ECS field names as attribute names with
   `elastic.mapping.mode: ecs` (scope attribute; the `mapping::mode` config key
   is deprecated) or `bodymap` mode to index the doc verbatim.

**Index design:** one index, three document flavors (see §4). Suggested name:
`urlquery-hunt` (or data-stream `logs-urlquery-hunt.threat-default`). The
converter emits `_bulk`-ready NDJSON: an `{"index":{...}}` action line per doc.

All field names below were verified against the ECS reference
(elastic.co/docs/reference/ecs, 8.x). No invented fields.

## 2. Timestamp normalization rules

| Raw value | Normalized `@timestamp` | `labels.hunt.date_precision` |
|---|---|---|
| `YYYY-MM-DD` | `YYYY-MM-DDT00:00:00.000Z` | `day` |
| `YYYY-MM` | `YYYY-MM-01T00:00:00.000Z` | `month` |
| empty | `2026-09-25T00:00:00.000Z` (dataset merge date) | `none` |

- All timestamps are UTC (`Z`); the source data is day-granularity with no
  timezone info, so midnight UTC is the honest representation.
- `@timestamp` = observation start (`first_seen`). `event.start` = first_seen,
  `event.end` = last_seen when present.
- Empty-date fallback rule (§5): `@timestamp` falls back to the dataset merge
  date `2026-09-25T00:00:00.000Z`, flagged with
  `labels.hunt.timestamp_source = "fallback:missing_first_seen"`. Rationale: a
  missing observation date must not silently become "now" (ingest time); pinning
  it to a fixed, documented constant keeps the fallback visible and queryable.
  When first_seen exists, `labels.hunt.timestamp_source = "first_seen"`.

## 3. Value mappings

### 3.1 Hunt IOC type → `threat.indicator.type` (STIX 2.0 SCO enum)

`threat.indicator.type` *must* be one of: `autonomous-system, artifact,
directory, domain-name, email-addr, file, ipv4-addr, ipv6-addr, mac-addr, mutex,
port, process, software, url, user-account, windows-registry-key,
x509-certificate`. The hunt's native type is always preserved in
`labels.hunt.ioc_type`.

| Hunt `type` | `threat.indicator.type` | Notes |
|---|---|---|
| `domain`, `proxy-domain`, `shortener-domain` | `domain-name` | |
| `url`, `tableau-endpoint`, `webhook-inbox`, `yourls-slug`, `wiki-endpoint`, `url_shortener_redirect` | `url` | values parsed into `threat.indicator.url.*` when they contain a scheme; bare `host/path` values get scheme-prepend heuristic for parsing (documented per-doc in `labels.hunt.url_parse = "heuristic"`) |
| `ip` | `ipv4-addr` / `ipv6-addr` | chosen by format; also copied to `threat.indicator.ip` (type `ip`) and `related.ip` |
| `ntfy-topic` | `url` | values are bare topic tokens; stored in `threat.indicator.url.original` verbatim, no URL reconstruction |
| `threatfox-hit` | `domain-name` | values are hex-subdomains of lhr.life etc. |
| `npm-package` | `software` | |
| `airtable-share-id`, `counterapi-namespace`, `file-path`, `wiki-page` | `artifact` | opaque tokens/paths/names, not URLs; original type kept in `labels.hunt.ioc_type` |

Node-only subtypes (from `graph/nodes.csv`, same STIX enum):

| Hunt `subtype` | `threat.indicator.type` | Notes |
|---|---|---|
| `gem-package` | `software` | RubyGems package names |
| `account` | `user-account` | e.g. `pastebin.com/u/jazzyjace` |
| `malformed-row` | `url` | value is a full URL |
| `ipv4` | `ipv4-addr` | dynamic branch shared with `ip` |
| `web-archive-capture`, `canary-beacon`, `dns-state`, `domain-observation`, `forum-thread`, `paste-set`, `forum-post`, `credential` | `artifact` | values are annotated descriptions/tokens, not clean observables |
| (empty) | sniffed | value sniff: IP → `ipv4-addr`/`ipv6-addr`; bare domain → `domain-name`; parseable URL → `url`; else `artifact`. Flagged with `labels.hunt.type_sniffed=true` |

### 3.2 Hunt confidence → `threat.indicator.confidence` (STIX 2.1 scale)

Expected values: `Not Specified, None, Low, Medium, High`.

| Hunt `confidence` | ECS value |
|---|---|
| `confirmed`, `high` | `High` |
| `likely` | `Medium` |
| `lead` | `Low` |
| (absent — all of `iocs.csv`) | `Not Specified` |

### 3.3 Status

No ECS indicator-status field exists. Hunt `status`
(`live`/`dead`/`unknown`/`new`/annotated variants) → `labels.hunt.status`
(keyword), plus a `status:<value>` entry in `tags` for faceting.

### 3.4 report_count → `threat.indicator.sightings`

`threat.indicator.sightings` = *"Number of times this indicator was observed
conducting threat activity"* (type `long`). `report_count` (urlquery reports
carrying the IOC) is the observation count — mapped directly.

## 4. Document flavors

Every doc carries the base set: `@timestamp` (required), `message`
(human-readable summary), `tags` (array), `labels.hunt.*` provenance,
`observer.product = "urlquery-agent-activity-hunt"`,
`observer.vendor = "urlquery-hunt"`, `observer.type = "research-pipeline"`
(no predefined list — free-form allowed), `event.module = "urlquery-hunt"`,
`event.provider = "urlquery-agent-activity-hunt"`,
`event.created` = converter run time (first time the pipeline saw the row, per
the ECS definition).

### Flavor A — indicator (`dataset/iocs.csv`, `graph/nodes.csv` type=`indicator`)

Per the ECS threat-intel usage pattern:

- `event.kind = "enrichment"`, `event.category = ["threat"]`,
  `event.type = ["indicator"]`
- `event.dataset = "urlquery-hunt.ioc"` (iocs.csv) or
  `"urlquery-hunt.graph-indicator"` (nodes.csv)
- `threat.indicator.name` = raw IOC value (display name)
- `threat.indicator.type` = §3.1 mapping (array — ECS says this field should
  contain an array of values)
- `threat.indicator.first_seen` / `last_seen` (date)
- `threat.indicator.description` = context (type `keyword` per ECS)
- `threat.indicator.confidence` = §3.2
- `threat.indicator.provider = "urlquery-agent-activity-hunt"`
- `threat.indicator.reference` = source_link
- `threat.indicator.sightings` = report_count
- `threat.indicator.url.*` populated for url-typed IOCs
  (`url.original` always; `url.full`/`url.domain`/`url.path`/`url.scheme`/
  `url.query` when parseable)
- `threat.indicator.ip` for ip-typed IOCs
- Pivot copies: `related.hosts += [domain values]`, `related.ip += [ip values]`
- `labels.hunt`: `ioc_type`, `status`, `node_id` (nodes.csv only),
  `date_precision`, `timestamp_source`, `url_parse` (when heuristic)

### Flavor B — entity (`graph/nodes.csv`, all other types)

- `event.kind = "event"`, `event.category = ["threat"]`,
  `event.type = ["info"]`
- `event.dataset = "urlquery-hunt.graph-node"`
- `message` = description (exactly what `message` is for: human-readable summary)
- `event.url` = source_url (verified ECS meaning: *"URL linking to an external
  system to continue investigation of this event"*)
- Type-specific enrichment:
  - `tactic` → `threat.tactic.name = [label]` (array per ECS)
  - `technique` → `threat.technique.name = [label]`
  - `campaign` → kept as a generic entity doc; **not** mapped to
    `threat.group.name` (that field is for named intrusion sets; our campaigns
    are activity clusters, and conflating them would corrupt group pivots)
  - `evidence` → `event.type = ["info"]`, evidence URL in `event.url`
  - `infrastructure` with domain-like subtype → `related.hosts += [label]`
- `labels.hunt`: `node_id`, `node_type`, `subtype`, `confidence`,
  `date_precision`, `timestamp_source`
### Flavor C — relationship (`graph/edges.csv`)

ECS has no native edge/generic-relationship type (the STIX 2.1 Relationship
SRO is the conceptually right model — see §6). Edges are emitted as event docs
with the triple preserved verbatim in flat labels (ECS `labels` must not
contain nested objects):

- `event.kind = "event"`, `event.category = ["threat"]`,
  `event.type = ["info"]` (`"relation"` is not an allowed `event.type` value)
- `event.dataset = "urlquery-hunt.graph-edge"`
- `message = "<source label> --<relation>--> <target label>"`
- `event.url` = evidence_url
- `labels.hunt.edge_source` = source node id, `labels.hunt.edge_target` =
  target node id, `labels.hunt.edge_relation` = relation verb,
  `labels.hunt.source_label` / `target_label` = display labels
- `@timestamp`: joined from the **source** node's `first_seen` (falling back to
  the target node's, then the §2 empty-date rule). Rationale: an edge describes
  usage/observation anchored at its source's first sighting.
- `related.hosts` gets source/target labels only when they parse as
  domain-like; otherwise pivot stays in the `labels.hunt.edge_*` fields.

### Dropped / parked fields

Nothing is dropped (keep-all). Parked in `labels.hunt.*` with justification:

| Parked | Where | Why |
|---|---|---|
| hunt-native IOC type | `labels.hunt.ioc_type` | `threat.indicator.type` is restricted to the STIX 2.0 enum |
| node type/subtype | `labels.hunt.node_type`, `labels.hunt.subtype` | no ECS taxonomy for hunt-internal classes (campaign, hop, agent_label, enhancement…) |
| liveness status | `labels.hunt.status` | no ECS indicator-status field exists |
| edge triple | `labels.hunt.edge_source/target/relation` | no ECS relationship object; STIX SRO semantics preserved as data |
| date precision / timestamp provenance | `labels.hunt.date_precision`, `labels.hunt.timestamp_source` | documents the §2 coercions so they stay queryable |

## 5. The 30 dateless nodes

30 `graph/nodes.csv` rows have neither `first_seen` nor `last_seen`. They are
overwhelmingly non-temporal classes (`tactic` 7, `technique` 4, `enhancement`
annotations, `evidence` records — the full breakdown is in the converter's
validation report). Rule applied: `@timestamp = 2026-09-25T00:00:00.000Z` (the
dataset merge date — a fixed, documented constant, never "now"),
`labels.hunt.timestamp_source = "fallback:missing_first_seen"`,
`labels.hunt.date_precision = "none"`. No row is dropped; the fallback is
explicitly flagged so it can be filtered out of time-series analysis.

## 6. STIX 2.1 concept map (for reference)

| STIX 2.1 concept | ECS realization in this schema |
|---|---|
| Indicator SDO (`pattern`, `valid_from`/`valid_until`, `labels`) | Flavor A: `threat.indicator.*` (`name`≈pattern value, `first_seen`/`last_seen`≈validity window, `labels.hunt.ioc_type`≈labels) |
| Relationship SRO (`source_ref`, `target_ref`, `relationship_type`) | Flavor C: `labels.hunt.edge_source/target/relation` + `message` |
| Campaign | Flavor B entity doc, `labels.hunt.node_type=campaign` |
| Infrastructure | Flavor B entity doc, `labels.hunt.node_type=infrastructure` (+ `related.hosts`) |
| Identity / Threat Actor | not present in the hunt data — no fabricated attribution |
| Observed Data | Flavor B `observation` nodes |
| Marking Definition (TLP) | `threat.indicator.marking.tlp` — unused; hunt data carries no TLP markings, so the field is omitted rather than invented |

## 7. Ingest notes

- The NDJSON files are `_bulk`-ready: each doc is preceded by
  `{"index":{"_index":"urlquery-hunt"}}`. Target a data stream
  (`logs-urlquery-hunt.threat-default`) for ILM/retention; the action lines work
  with `POST /<data-stream>/_bulk` unchanged.
- ECS dynamic mapping handles the field types; if a strict template is wanted,
  generate it from this doc — every field above is a verified ECS name.
- `threat.indicator.description` is `keyword` (not text) per ECS — long contexts
  are retrievable but not full-text analyzed. If full-text search over contexts
  matters, add an ingest pipeline `set` to a `text` sub-field or query
  `message` (match_only_text) on Flavor B docs.

## 8. References

- ECS field reference (8.x): https://www.elastic.co/docs/reference/ecs/
  (threat, event, url, related, base, observer field sets — all field names
  above verified against these pages on 2026-09-25)
- ECS threat-intel usage: event.kind=`enrichment`, event.category=`threat`,
  event.type=`indicator`, with indicators copied to `related.*`
- EDOT elasticsearch exporter mapping modes (`none`/`ecs`/`otel`/`raw`/`bodymap`);
  default `otel`; `ecs` mode maps OTel SemConv → ECS; mode selected via
  `elastic.mapping.mode` scope attribute
