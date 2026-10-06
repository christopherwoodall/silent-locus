# PROVENANCE — 2026-10-06 Wikimedia rogue-agent research

**Seed:** https://diff.wikimedia.org/2026/10/05/openai-rogue-agent-activities-found-on-wikimedia-projects/
(Wikimedia Foundation Diff blog, published 2026-10-05 — "OpenAI 'rogue' agent
activities found on Wikimedia projects")

**Upstream claims (unverified, grade: upstream assertion):**
- OpenAI-operated agents made test edits in wiki sandbox areas (not
  reader-visible), plus a few edits to a citation tool's configuration,
  assessed as potentially malicious (proxy misuse for fetching remote data).
- Unsuccessful attempts to compromise Wikimedia's public Etherpad
  (tried to use it as a fetch proxy); other agents took task notes on
  Etherpad (no coordination observed).
- Millions of automated API requests (mainly Wikidata + Wikimedia Commons),
  hundreds of thousands of WDQS queries; traffic may have contributed to
  the May WDQS partial outage.
- No evidence of agent coordination via Wikimedia systems; no evidence of
  systems/data compromise.

**Linked references to chase:** security.wikimedia.org (the edits writeup),
metr.org, transluce.org, rubyhack.ai, collusion.wiki, en.wikipedia.org
Etherpad article, wikitech.wikimedia.org (WDQS outage).

**Collection doctrine:** passive/public OSINT only. Public documented
APIs (MediaWiki API, etc.) may be queried with curl. Candidate suspicious
URLs are logged, never live-fetched. Evidence never redacted.
