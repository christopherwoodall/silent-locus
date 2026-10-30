# E1 extraction summary — AIID incidents 1–900

## Terms

- AIID: Artificial Intelligence Incident Database, a curated public database of AI incidents. Content from AIID is SECONDARY (curated, not first-hand observation).
- TTP: tactic, technique, and procedure. A short slug names a known technique.
- IOC: indicator of compromise or interest. A domain, URL, model name, or similar value tied to an incident.
- Slug "none-established": no slug in the established taxonomy fits the behavior. No slug was invented.

## Counts

- Incidents in range present in the snapshot: 889.
- Incident JSON files written: 889.
- Incidents with at least one behavior: 889.
- Total behavior entries: 1524.
- Incidents with at least one IOC: 888.
- Total IOC entries: 13896.
- IOC kinds: URL 9561, domain 4240, model or tool 95.
- TTP entries with an established slug: 0.
- Incidents that could not be parsed: 0.
- JSON files that failed validation: 0. Every file passed `python json.load`.

## Method

- Source 1: snapshot structured files `raw/snapshot/extracted/mongodump_full_snapshot/incidents.csv` and `reports.csv`. These gave incident id, title, date, linked report ids, and the incident description.
- Source 2: local fetch files in `raw/fetch/f1-1-450/` and `raw/fetch/f2-451-900/`, plus their FETCH-LOG.json files. These gave the `files_used` list per incident and the 404 gap list.
- Source 3: incident HTML pages, parsed only for linked external URLs. Boilerplate links (social sites, analytics, donation pages, AIID internal pages) were dropped. All URLs in outputs have query strings stripped. No signed values, tokens, or full query strings appear in outputs.
- Behavior text: one entry per sentence of the snapshot incident description, in plain words from the source. No behavior text was graded as OBSERVED from press articles, because linked press articles were not fetched. All content here is SECONDARY.
- TTP mapping: keyword rules against the established taxonomy in `docs/taxonomy/ttp-taxonomy.md` only. Rules were kept strict. A loose first pass produced 5 false hits (price-coordination wording in unrelated reports, and a human token misconfiguration). Each was checked by hand and the rules were tightened. Result: 0 established-slug TTPs in this range.
- IOC extraction: report URLs and source domains from `reports.csv`, model and tool names by pattern match (ChatGPT, GPT-3, GPT-4, Claude, Gemini, Llama, and similar), plus domain, IP, hash, and file-path patterns in descriptions. No IP addresses, file hashes, or file paths were found in incident descriptions in this range.
- Personal names: no submitter or editor names are included. Names in incident descriptions and titles were scrubbed mechanically: snapshot harmed-party names, report submitter names, first-name-led capitalized runs, role-plus-surname pairs, and same-incident surnames were replaced with `[person]`. A checked list of known names (including high-profile public figures in this range) returns zero hits after scrubbing. Note: scrubbing is mechanical. An uncommon name that is not in the first-name list and not tied to a snapshot field could still remain in a behavior sentence. Treat behavior text as scrubbed, not as proven name-free.
- No network fetches, no logins, no sessions, no POST requests, no Shodan, no package repos, no Docker Hub. Nothing was executed from evidence. Nothing was committed or pushed. No Factum records were written.
- Writing style: short sentences, simple words, terms defined on first use.

## Gaps

- Incident ids absent from the snapshot in this range (11, not gaps to fill): 90, 130, 237, 247, 269, 338, 342, 365, 442, 512, 542.
- Report pages that returned HTTP 404 at fetch (5, not re-fetched): report 3447 (incident 3), report 2587 (incident 464), report 3205 (incident 530), report 3875 (incident 665), report 3916 (incident 668).
- Incident 88 has no linked reports in the snapshot, so it has behaviors but zero IOCs. Its incident HTML file was still used.
- Zero 403 or 429 responses were recorded in fetch for this range.

## Near misses (recorded as none-established, not forced into a slug)

- Incidents 376 and 894 (RealPage YieldStar): landlords coordinated rent pricing through shared nonpublic data via an algorithm. This is algorithmic pricing coordination. It does not meet the taxonomy definition of back-channel price collusion, which requires agents with a private back-channel explicitly agreeing on price floors. Recorded as none-established.
- Incident 571 (Microsoft AI research team data exposure): a human team misconfigured Shared Access Signature tokens. No agent extracted tokens from client configuration. Recorded as none-established.
- Incident 473 (Bing Chat prompts revealed by prompt injection): prompt injection is present, but the established prompt-injection slug covers API-key exfiltration from LiteLLM deployments, which this is not. Recorded as none-established. This is the closest agent-relevant behavior in the range, and it needs a taxonomy decision before any slug is applied.
- Incident 443 (ChatGPT used to develop malware): the taxonomy slugs for LLM runtime payload generation cover malware that calls a model during execution. Here a human used a chatbot to write malware. Recorded as none-established.

## Agent and swarm relevant notes (no TTP slug claimed)

- Most incidents in 1–900 predate agent systems or concern crashes, bias, misinformation, and faulty outputs. They are not agent-coordination evidence.
- Model and tool IOCs are led by ChatGPT (44 incidents), GPT-3 (11), Waymo (7), Copilot (6), Alexa (5), DALL-E (5), Stable Diffusion (5), Gemini (4), GPT-4 (3).
- Incidents worth a later read for agent behavior, all slug none-established: 65 (reinforcement learning agents in video games), 420 (ChatGPT filter bypass), 443 (ChatGPT malware writing), 473 (Bing Chat prompt injection), 622 (dealer chatbot agrees to sell a vehicle for $1), 757 (ChatGPT macOS app stored conversations in plain text), 866 (network of 171 AI-powered bot accounts spreading political content).
- No swarm, fleet, dead-drop, relay, or shortener-abuse behavior was found in this range under the established taxonomy.
