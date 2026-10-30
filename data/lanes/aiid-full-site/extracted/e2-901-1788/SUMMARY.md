# E2 Extraction Summary — Incidents 901–1788

Lane: E2, AIID full-site follow-up fleet.
Operator: BigSexyWarlock69.
Date of work: 2026-10-30.

## Terms used

- AIID means the AI Incident Database. It is a curated database of AI incidents.
- TTP means tactic, technique, and procedure. It is a named way an AI system acts.
- IOC means indicator of compromise. It is a technical value such as a domain, an address, or a hash.
- SECONDARY means the content comes from a curated database. It is not direct observation.
- A slug is a short code name for a TTP.

## Counts

- Incidents in range in the snapshot file: 888.
- Incidents extracted: 886.
- Incidents with behaviors: 886.
- Behavior entries in total: 1,340.
- Incidents with IOCs: 886.
- IOC entries in total: 7,474.
- Incidents with a mapped TTP: 42.
- TTP mappings in total: 53.
- Incidents with no mapped TTP: 844. Their behaviors use the slug "none-established".
- Report slots in the snapshot file: 2,674.
- Report files used: 2,674. Every report slot has a local file.
- JSON files written: 886. Every file passed a JSON load check.
- Incidents that could not be parsed: 0.

## Count note

The task brief said 887 incidents were fetched.
The true count is 886.
The f3 range holds 449 incident files, not 450, because incident 1152 is an overlap skip.
The f4 range holds 437 incident files.
449 plus 437 equals 886.

## Overlaps

These two incidents were NOT extracted here. They belong to the prior lane.

- Incident 1152 (Replit). OVERLAP. Its 5 report files (5577, 5578, 5593, 6113, 6126) live in the incident-7050 lane. The f3 fetch skipped it for this reason.
- Incident 1433 (Antigravity). OVERLAP. Its reports (7050, 7051) live in the incident-7050 lane, Factum batch 756a273f. The f4 fetch skipped it for this reason.

## Gaps

- No unfetched incidents exist in this range except the two overlap skips above.
- No incident file was missing.
- No incident failed to parse.
- Zero fetch blocks (403 or 429) were reported in the fetch logs for this range.

## Method

- Structured fields (title, date, report links) come from the snapshot CSV files: incidents.csv and reports.csv.
- Full description text comes from the incident description in incidents.csv.
- Linked source URLs come from the incident and report HTML files, and from the report source URL in reports.csv.
- HTML links were kept only when the link host matched a report source domain for that incident. This rule drops site header and footer links.
- Behavior text is a sentence from the incident description. Up to 3 sentences were kept per incident. Sentences with AI action words scored highest.
- TTP mapping used only slugs from docs/taxonomy/ttp-taxonomy.md. No new slug was invented.
- A TTP was mapped only when all its key terms appeared in one unit. A unit is the incident description, one report title plus description, or a window of 5 sentences in one report text.
- Three candidate slugs were checked and then dropped as false matches: staged-host-diffing, false-front-journalist-persona-network, and apologia-and-truce-coordination. Their matches were about malware staging, news impersonation, and human apologies, not the taxonomy meanings.
- IOC kinds are: domain, URL, IP address, hash, model, tool, and file path.
- URL values keep the path shape and the query parameter names only. Query values were dropped. Long token-like path parts (32 or more characters) were replaced with "{segment}".
- IP addresses from private ranges were dropped. Only public addresses were kept.
- Hash values are hex strings found in report text. They are not verified file hashes.
- Model and tool names come from a fixed name list matched in description and report text.
- No submitter names, editor names, or author names appear in any output file.
- No personal names were added. Titles are copied verbatim from the snapshot CSV, as the schema requires.
- Grade for all content is SECONDARY. The linked press articles were not fetched. Nothing here is graded as observed from press.

## TTP counts by slug

- reasoning-transcript-extraction: 7
- form-auto-submission: 7
- exfil-via-public-github-repo: 5
- url-shortener-abuse: 4
- sql-injection-via-url: 4
- back-channel-price-collusion: 4
- vibe-hacking: 3
- dns-firewall-bypass-internet-access: 3
- reseller-relay-front: 3
- proxy-network-fraudulent-accounts: 2
- llm-runtime-payload-generation: 2
- ai-cli-assisted-secret-discovery: 2
- token-extraction-from-client-config: 2
- state-actor-ai-attack-lifecycle: 1
- guardrail-bypass-ctf-pretext: 1
- guardrail-bypass-student-pretext: 1
- peer-account-sabotage: 1
- decompile-loop-exploit-foundry: 1

## IOC counts by kind

- URL: 3,566
- Domain: 2,678
- Model: 652
- Hash: 377
- File path: 81
- Tool: 64
- IP address: 56

## Notes on IOC quality

- Most domains are press and publisher source domains. They are source links, not threat infrastructure.
- No webhook.site, da.gd, is.gd, httpbin.org, or httpbun.com source domains appear in this range.
- The largest IP groups sit in incidents 1661, 1669, 1670, 1766, and 1781. These are agent-operation and exposure reports, so they matter most for swarm review.
- Some IP values look like network addresses from articles (for example 138.0.0.0 and 104.28.0.0). Treat them as article quotes, not confirmed hosts.
- Hash values need a check before use as file hashes. They are hex strings from text, and some may be IDs or digests of other data.

## Outputs

- One JSON file per fetched incident: data/lanes/aiid-full-site/extracted/e2-901-1788/<incident_id>.json
- This summary: data/lanes/aiid-full-site/extracted/e2-901-1788/SUMMARY.md
- Nothing was committed. Nothing was pushed. No Factum records were written.
