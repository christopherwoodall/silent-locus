# Lane D — March-7 code-execution modality gems (2026-09-27)

colonist-one (thecolony.ai incident wiki) reported a SECOND registry modality,
distinct from the May/June go-import meta-tag campaign: a code-execution probe
— doc-builder RCE + egress test — delivered through 3 RubyGems packages,
11 same-day versions, starting March 7, 2026. All yanked as of 2026-09-28.

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

## Elastic

Own index `march7-rce-modality` under the canonical shared schema
(`notes/gems-es-mapping.json`), with the `event.dataset.keyword` multi-field
at creation. Record flavors: `package`, `version`, `sweep_hit`.

## Caveats

- The modality characterization (doc-builder RCE + egress test, 11 versions,
  March-7 start) is colonist-one's claim via thecolony.ai incident wiki —
  cited as reported, not independently re-verified.
- Compact-index 404s are an oracle for "yanked from rubygems.org", not a
  claim about Diffend availability (Diffend is an independent snapshot).
