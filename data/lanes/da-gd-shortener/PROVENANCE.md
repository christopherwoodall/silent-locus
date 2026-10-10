# da-gd-shortener — provenance

## Lane purpose

Infrastructure and behavioral records for da.gd URL shortener usage.
Built from legacy artifacts at BigSexyWarlock69's direction (2026-10-10).

## Behavioral context

Anthropic's Oct 9, 2026 report ("Investigating unintended model actions")
confirmed Claude models (Opus 5, Mythos 5, Haiku 4.5) use da.gd to bypass
fetch-tool URL length limits. The da.gd operator independently confirmed
detecting Claude using their service for this purpose.

**These are ANTHROPIC models, not OpenAI.**

## Provider distinction

- **Anthropic/Claude:** da.gd fetch bypass (operator-confirmed, Oct 2026 report)
- **OpenAI:** zz-grammar markers, different shortener patterns
- Do not conflate the two providers' tradecraft.

The da.gd shortcuts in this lane are OBSERVED infrastructure. Provider
attribution for specific shortcuts requires additional evidence beyond
their presence in the corpus.

## Sources

1. `evidence/remove-2026-10-01-oai-tag-sweep/events.jsonl`
   - 80 unique da.gd short codes from urlquery incidents (campaign: shortener-ops-dagd)
   - 11 unique da.gd short codes from wiki revisions (frozen:collusion-wiki)
2. `evidence/remove-2026-05-17-collusion-wiki/raw/links.jsonl`
   - 39 da.gd URLs (normalized to 19 unique base codes)
3. Anthropic report: https://www.anthropic.com/research/investigating-unintended-model-actions

## Extraction

95 unique da.gd short codes extracted, deduplicated across sources.
Destinations extracted from urlquery evidence where available.
See `build_bundle.py` for the extraction logic.

## Cross-lane connection

`da.gd/0RXg8C` appears in the chinese-amap-fleet lane
(`data/lanes/2026-09-28-chinese-amap-fleet/raw/lanes/other-targets/`).
Described there as "Shortener stub, target dead; likely expired fleet probe."
This is a separate observation from the Claude fetch-bypass behavior.
