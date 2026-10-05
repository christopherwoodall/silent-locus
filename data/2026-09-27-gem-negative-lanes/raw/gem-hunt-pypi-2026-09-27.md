# Hunt lane 5 — PyPI, same tradecraft other registry — 2026-09-27

**Verdict: no GemStuffer fingerprints found on PyPI.** 20 campaign/June-18 names checked
via the PyPI JSON API — all absent. Beacon strings, go-import tags, jina
laundering, and council/SEC target references return zero indexed hits on
pypi.org (only legitimate-package noise).

## Method (read-only, ~1/s, metadata only)

- PyPI JSON API: `GET https://pypi.org/pypi/<name>/json` per candidate name.
  Sanity check: `requests` → HTTP 200 (API healthy, so 404s are real absences).
- Web search with `site:pypi.org` for beacon strings, `go-import`, `r.jina.ai` /
  `s.jina.ai`, `modern.gov`, `sec.gov "county.json"`.
- PyPI's HTML search page serves a JS "Client Challenge" to non-browser clients,
  so description full-text search was done via search-engine indexing instead.
  **Caveat:** absence of beacon-string hits means "not indexed", not "provably
  absent from all descriptions".
- Nothing downloaded or installed; no logins.

## Name-squat checks (all 404 — not present on PyPI)

May-12 campaign names:
`tryf3zz`, `southwarkssrfhack`, `londonyardtestabc`, `southfetchprobe42`,
`wandsworthprobe1778551714`, `zzsouthrunnerb`, `uxjinalamb2`,
`oaitest1778473828`, `trya1zz`, `zzsouthrunner`, `slnleaker4`,
`exfiltestwand`, `prx1b49033907`, `yardbreaker`, `probejiqptzco`

June-18 wave names:
`q--00cfmapjson726`, `m--00cfproxy47`, `amdwc56692`,
`mapanchorcf202704`, `amdvar152054`

## Content-pattern searches (site:pypi.org)

| pattern | result |
|---|---|
| `"builder alive"` | 0 hits |
| `"YARD RAN"` | 0 hits |
| `"yard exploit"` | 0 hits |
| `"go-import"` | noise only — matches are `import plotly.graph_objects as go` etc.; no `<meta name="go-import">` payloads |
| `r.jina.ai` / `s.jina.ai` | only the legitimate `jina` package (Jina AI's own framework) — https://pypi.org/project/jina/ |
| `modern.gov` | only legitimate `pyPreservicaGov` (Modern.Gov records archiving tool) — https://pypi.org/project/pyPreservicaGov/ |
| `sec.gov "county.json"` | only unrelated `topo2geo` — https://pypi.org/project/topo2geo/ |

## Conclusion

The operator class did not mirror the campaign onto PyPI under any tested
name, beacon string, laundering URL, or target reference. PyPI shows no
evidence of the go-import metadata-poisoning technique. Combined with the
urlquery invisibility finding, the campaign's footprint remains RubyGems-only
(RubyGems + Diffend + RubyDoc.info build workers, all since yanked/scrubbed).
