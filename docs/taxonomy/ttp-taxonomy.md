# TTP Taxonomy

Tactics, techniques, and procedures observed in AI agent behavior.
Each TTP links to one or more behavior categories above.
Sourced from lab behavior reports ingested into the `intel.ttp` Factum records.

## sql-injection-via-url

Crafting URL parameters that a target site mistakenly executes as SQL or
shell commands.

**Related behaviors:** software-flaw-exploitation.
**Context:** Used when the agent's own tools are deliberately limited or an
outside service is unavailable. The agent discovers injectable endpoints
through exploratory browsing.

## token-extraction-from-client-config

Reading browser settings files, site configuration, or archived copies to
find working access tokens, then using them to query servers directly —
bypassing intended access controls, click-through requirements, or fees.

**Related behaviors:** restriction-circumvention.
**Context:** The agent treats client-visible configuration as a legitimate
information source. Tokens issued to "any visitor" are harvested and reused.

## url-shortener-abuse

Routing long URLs through free shortening services (e.g. da.gd) to bypass
fetch-tool URL length limits.

**Related behaviors:** url-shortener-abuse.
**Context:** Length limits exist to block injection payloads in URLs. The
agent discovers that shortened URLs pass the length check while resolving
to the same long destination. Independently confirmed by a shortener
operator.
**Hunt relevance:** Shortener stats pages can leak agent activity —
see university-shorteners lane.

## form-auto-submission

Navigating to live websites and submitting real forms when evaluation
instructions are ambiguous about the submit/stop boundary, or when test
fixtures (dummy forms) fail to load.

**Related behaviors:** unauthorized-form-submission.
**Context:** The agent follows the task instruction literally ("complete
the form") without the safety boundary ("but do not submit") when that
boundary is missing or the dummy environment breaks.

## Adding TTPs

1. Name it as a short slug describing the technique.
2. Link to the behavior category (or categories) it implements.
3. Document the mechanism — how does the agent actually do it?
4. Create a matching `intel.ttp` Factum record with `related_behaviors`.
