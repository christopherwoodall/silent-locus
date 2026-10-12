# Factum record types

Registered observation and observable types across the installed schema
packs. This doc names the record shapes used in the corpus; it is generated
from the packs' `definitions.json` and kept in sync by the weekly
taxonomy-maintenance job.

## New since last review

- `malware.family` (observation, `urn:factum:malware:family:1`) — added
  2026-10-11 with the factum-malware 1.0.0 pack (GTIG AI-malware families
  ingest: PROMPTFLUX, PROMPTSTEAL, PROMPTLOCK, QUIETVAULT, FRUITSHELL).

## factum-behavior

- `model` (observable) — `urn:factum:core:raw-string:1` — normalized model identity
- `harness` (observable) — `urn:factum:core:raw-string:1` — normalized harness identity
- `exhibits` (predicate) — model/harness → behavior relationships
- `uses` (predicate) — behavior → tool relationships
- `behavior.profile` (observation) — `urn:factum:behavior:profile:1` — ranked marker entries for one (model, harness) pair
- `behavior.tool_sequence` (observation) — `urn:factum:behavior:tool-sequence:1` — ordered tool-call steps from one agent trajectory

## factum-core

- `text`, `quote`, `term`, `ngram`, `sha256`, `api_key`, `external_id` (observables) — `urn:factum:core:raw-string:1`
- `incident.reported`, `activity.network_request`, `activity.data_transfer`, `activity.tool_use`, `change.infrastructure` (events) — `urn:factum:core:empty:1`
- `in_lane`, `part_of`, `derived_from`, `related_to`, `supports`, `contradicts`, `copied_from`, `updates` (predicates)

## factum-datasets

- `dataset.snapshot` (observation) — `urn:factum:datasets:snapshot:1`
- `dataset.record` (observation) — `urn:factum:datasets:record:1`
- `dataset_id` (observable) — `urn:factum:core:raw-string:1`

## factum-hunt

- `proxy.chain` (observation) — `urn:factum:hunt:proxy-chain:1`
- `exfil.dead_drop` (observation) — `urn:factum:hunt:dead-drop:1`
- `intel.ioc` (observation) — `urn:factum:hunt:ioc:1`

## factum-infra

- `infra.dead_drop` (observation) — `urn:factum:infra:dead-drop:1` — exfiltration endpoint
- `infra.ioc` (observation) — `urn:factum:infra:ioc:1` — indicator term with category and status
- `infra.message` (observation) — `urn:factum:infra:message:1`
- `infra.package` (observation) — `urn:factum:infra:package:1`
- `infra.proxy_chain` (observation) — `urn:factum:infra:proxy-chain:1` — observed proxy usage
- `infra.proxy_instance` (observation) — `urn:factum:infra:proxy-instance:1` — deployed proxy infrastructure
- `infra.shortcut` (observation) — `urn:factum:infra:shortcut:1` — short URL with destination
- `infra.tunnel` (observation) — `urn:factum:infra:tunnel:1` — reverse tunnel

## factum-intel

- `intel.report` (observation) — `urn:factum:intel:report:1` — a lab report or intel publication
- `intel.behavior` (observation) — `urn:factum:intel:behavior:1` — one classified behavior observation, using a category from behavior-categories.md
- `intel.ttp` (observation) — `urn:factum:intel:ttp:1` — one technique, using a slug from ttp-taxonomy.md

## factum-malware

- `malware.family` (observation) — `urn:factum:malware:family:1` — an AI-assisted malware family (added 2026-10-11)

## factum-web

- `web.capture` (observation) — `urn:factum:web:web-capture:1`
- `reachability.check` (observation) — `urn:factum:web:reachability-check:1` — note: registered WITHOUT the `web.` prefix; `web.reachability.check` is rejected
- `url`, `domain`, `hostname`, `ipv4`, `email` (observables) — `urn:factum:core:raw-string:1`
