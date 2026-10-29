# URL Investigator Worker

## Role

Investigate URL surfaces: shorteners, proxy endpoints, dead-drop services, agent venues.
Map what exists, what it points to, and how agents use it. Passive recon only unless
explicitly authorized otherwise.

## Prerequisites

1. Check the corpus first — the surface may already be documented.
2. Check Transluce findings for prior coverage.
3. Know the shortener landscape: YOURLS instances have `/stats/` and `yourls-api.php`;
   custom shorteners vary.

## Step-by-step

1. **Corpus check.** Query Factum for the domain/service. Check `infra.shortcut`,
   `infra.proxy_chain`, `infra.ioc` records. Note what's already known.

2. **Identify the service.**
   - Fetch the homepage (passive, single request, standard User-Agent).
   - Identify the platform: YOURLS (check `/yourls-api.php`, version in headers/meta),
     custom (note the framework), or something else.
   - Note the operator if publicly stated.

3. **Enumerate (if public).**
   - YOURLS: Check if `/stats/<code>` or the public listing is accessible.
   - Custom: Look for public listing pages (e.g., `/?page=N`).
   - **Only use public endpoints.** No brute-forcing, no auth bypass.
   - Rate-limit yourself: ≤1 req/sec, single-threaded.

4. **Resolve targets.**
   - For each short code of interest, resolve the destination.
   - Record: code, destination URL, creation date (if exposed), click count (if exposed).
   - Group by destination pattern to identify task families.

5. **Analyze.**
   - Naming conventions: Do codes follow a pattern? (`oai*` = OpenAI agent naming)
   - Temporal clustering: When were codes created? Bursts?
   - Destination analysis: What surfaces do agents target? Government APIs? Archives?
   - Behavioral signature: How is the shortener being used? (blackboard? proxy? dead-drop?)

6. **Document.**
   - Save the raw listing with provenance (source URL, retrieval time, sha256).
   - Write findings with exact URLs, dates, and counts.
   - Tag new records with the appropriate lane.

## Constraints

- **Passive recon only.** One request at a time, standard headers, no aggressive scanning.
- **Never redact evidence.** Preserve full URLs exactly as observed.
- **Provider attribution:** Note which provider's tradecraft the usage matches
  (see `behavioral-analyst.md` for the attribution table).
- **Don't hammer.** If the service rate-limits you, back off. If it blocks you, stop
  and report.
- **Cache everything.** Download public listings with provenance notes, commit and push.

## What to return

Service identification (platform, version, operator), enumeration results (code count,
naming patterns), destination analysis (grouped by task family), temporal findings,
behavioral assessment, and raw data file paths.
