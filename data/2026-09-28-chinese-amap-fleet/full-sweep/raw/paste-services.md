# Paste-services sweep — 2026-10-04

**Lane:** paste services only (rentry.co, pastebin.com, ix.io, termbin.com, 0x0.st, paste.rs, hastebin, privatebin instances)
**Task:** hunt undiscovered agent/swarm fleets via our markers.
**Method:** rentry.co direct API probe (`curl https://rentry.co/api/search?q=MARKER`), web search `site:` scoping per service, plus cross-service marker queries.
**Sweeper:** subagent (depth 2), 2026-10-04 ~22:50 CDT.

## Verdict: NO new agent/swarm hits. One known-public-tooling note.

No pasted agent configs, harness scripts, tunnel URLs with agent context, dead-drop inboxes, or prompt/tooling leaks matching our markers were found on any paste service checked. The known operator context (Chinese Amap-map data-collection fleet, `uqscan=<word><date>` tags, `<hex>.lhr.life` tunnels, webhook.site dead-drops, Jan–Oct 2026) has zero paste-service footprint in this sweep.

## rentry.co

- `curl "https://rentry.co/api/search?q=uqscan"` → **no such endpoint**; the API probe returned an HTML Error page (rentry.co serves markdown pastes; search is site-internal only). Fallback to web search used instead.
- `site:rentry.co uqscan` → 0 results.
- `site:rentry.co pandalegacy` → 0 results.
- `site:rentry.co "r.jina.ai"` → 0 results.
- `site:rentry.co "webhook.site" bot config` → 0 results.
- `site:rentry.co lhr.life OR webhook OR amap` → 0 results.

## pastebin.com

- `site:pastebin.com uqscan` → 0 results.
- `site:pastebin.com sub_poi_navi` → 0 results.
- `site:pastebin.com pandalegacy` → 0 results.
- `site:pastebin.com "lhr.life"` → 0 results.
- `site:pastebin.com "webhook.site" agent harness` → 11 results, **all generic noise, none agent-fleet**:
  - WhatsApp webhook dispatcher config (Jun 2024, PT-BR comments), Discord "ping/vote" bot (2021), Stable Diffusion payload with webhook callback (Jul 2023), 3x AWS-credential exfil snippets (Jun/Jul 2025 — generic stealer material), kumod SMTP debug log, contract-generation JSON callback, account-switcher license trigger, XSS probe, `webhook.site/token/.../latest/raw` curl cheatsheet. None carry agent-harness structure, tunnel grammar, or our markers.
- `site:pastebin.com "r.jina.ai" agent` → 1 hit, **known public tooling, not a fleet**:
  - `https://pastebin.com/3j1466Da` ("people will ask for this autoblogger", SEO spam wrapper) — embeds the public **OpenDeepResearcher by Matt Shumer** harness: `JINA_BASE_URL = "https://r.jina.ai/"` alongside OpenRouter/SERPAPI keys and `anthropic/claude-3.5-haiku` default model. This is a publicly attributed, named research-agent tool circulating as SEO-spam paste; r.jina.ai usage here is generic fetch-proxy for a known open-source agent, not a new swarm. Filed as noise, kept for the record because it IS "past fetch-proxy usage in pasted configs."

## ix.io / termbin.com / 0x0.st (write-mostly termbin-style)

- `site:ix.io uqscan OR site:termbin.com uqscan OR site:0x0.st uqscan` → 0 results.
- `site:0x0.st OR site:ix.io OR site:termbin.com pandalegacy OR uqscan OR uqcors` → 0 results.
- `site:termbin.com OR site:ix.io "webhook.site" OR "jina"` → 0 results.
- As expected: these are append-only FIFO text drops with no browseable index; only search-engine-cached copies exist. Nothing cached matches.

## paste.rs / hastebin.com

- `site:paste.rs OR site:hastebin.com uqscan OR uqcors OR pandalegacy` → 0 results.

## privatebin instances

- `"uqscan" OR "uqcors" OR "pandalegacy" privatebin` → 1 result, **noise**: `panda-scanner.com` (FREQTY CLOUD dental/medical scanner manual PDF) — matched on the word "privatebin"? No — this was a false positive (panda-scanner vs pandalegacy string proximity). No actual privatebin instance content matched. Encrypted-by-default pastes on privatebin are not indexable by construction; the blind spot stands and is noted rather than cleared.

## Cross-cutting marker queries (no service scoping)

- `"uqscan" paste` → only noise (UAH test-scanning form PDF, iqscan-widgets typosquat list, uOttawa barcode form, a TikTok URL whose checksum param coincidentally contains `uqscan`). Zero paste-service content.
- `"uqcors" OR "lhr.life" paste` → polluted by LHR (OCLC library "Local Holdings Record" docs). Zero agent content.
- `"uqcors" pastebin OR rentry OR ix.io` → noise (vaccination.gov.ng PDF, ingress passcodes PDF, 4chan share-thread FAQ). Zero.
- `"pandalegacy" agent` → **marker is a name collision**: PandaLegacy is a Fortnite Creative creator (@PandaLegacy, fchq.io/@PandaLegacy, maps like "Disco Delivery", "Wild West Sniper Shootout"). All web hits are the gamer, not a fleet tag. This marker will generate 100% false positives in unscoped web search — keep it service-scoped (all service-scoped checks were clean).

## Metadata notes

- No paste timestamps, author handles, or config structures surfaced for any marker — there was nothing to do metadata forensics on. The sweep is a clean negative on the marker set as of 2026-10-04.
- rentry.co: no public search API exists (verified by probe); future sweeps should go through its site-internal search in a live browser or targeted `site:rentry.co` engine queries.
- Search-engine coverage of paste services is thin (pastebin blocks most indexing; termbin pastes expire); a negative here is "not found in the indexable surface," not "does not exist."

## Not pushed (per brief). File written; awaiting orchestrator merge.
