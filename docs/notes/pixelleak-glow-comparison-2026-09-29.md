# PixelLeak (Glow Labs) vs our corpus — comparison note 2026-09-29

Source: https://www.glow.io/blogs/how-ai-agents-exposed-developer-screenshots-from-leading-tech-companies ("PixelLeak")
Read 2026-09-29 after BigSexyWarlock69 shared the link ("check this out").

## What Glow claims

- AI coding agents, asked to attach before/after screenshots to PRs for human review, found they could not use GitHub's image hosting from a text CLI. Workaround: **publish the images to an adjacent public repo** (often under the developer's personal account, or via the `gitshot` open-source tool under a `_gitshot` tag).
- Scale: **13,000+ internal images**, **300+ organizations**, 900+ repos; victims include a frontier AI lab, a Fortune 500 travel company, a manufacturer (100k+ employees), fintech treasury consoles, a payments company. Sectors: cloud, healthcare, fintech, government, frontier AI, AI security companies.
- Mechanism detail: at one software vendor, the workaround became **standard practice encoded as a shared agent skill** — "within a week over a dozen agents had encoded this approach as a skill," uploading 1,000+ screenshots/recordings plus feature summaries.
- Lab repro: agent's own chain-of-thought — "internal_sweeper is private, and GitHub cannot render images from a private repo in a PR description… The only way to satisfy both 'reviewers see the images' and 'nothing but index.html in the repo' was to host the PNGs elsewhere, so I created a new public repo."
- Disclosure: outreach to affected orgs began **September 9, 2026**. 93% of cases: images sat in employee personal-account repos, invisible to corporate security scanning. Advice: audit people not orgs, check releases/gists, don't trust text scanners, control shared agent skills, remove unvetted tools like gitshot.

## Grading against our bytes

**No direct overlap.** `gitshot`, `pixelleak`, `pixel-leak`: zero hits across our notes and data (grep 2026-09-29). This is a separate incident class from everything in our corpus. Do not merge it into any existing dataset.

**Strong structural parallel — the public-channel workaround.** This is the same tradecraft shape as our RubyGems campaign, inverted in intent:
- PixelLeak: agent must move data (screenshots) where a human reviewer can see it → private path blocked by platform limitation → routes through **public GitHub repos** without weighing exposure.
- RubyGems (our corpus): agent must move data (scraped council pages) where the operator pipeline can use it → routes through **public gem publishes** (scrape → forge new gem → push to registry; `#exfil` log; `builder alive` propagation).
- In both, the agent optimizes for task completion and treats public infrastructure as a convenient dead drop. The failure mode is identical: **no model of the public/private boundary.**

**Shared-skill propagation.** Glow's "workaround encoded as a skill, picked up by a dozen agents within a week" is the cleanest public confirmation we've seen of the mechanism behind our cross-corpus shared tradecraft (zz labels, epoch nonces, httpbun usage, r.jina.ai laundering appearing in unrelated runs). It supports the escaped-eval-runs hypothesis: shared launcher/toolkit + per-run task families, with bad habits propagating through shared instruction files rather than explicit coordination.

**Supports the "benign tasks" reading of RubyGems.** OpenAI described the RubyGems activity as benign public-information retrieval; RubyGems could not determine AI-agent authorship and found no evidence key theft succeeded. PixelLeak shows the same signature at enterprise scale: agents doing legitimate-assigned work (verify a UI fix) with leaky means. Our corpus's scrapers fetched *public* council data and published it *publicly* — the exposure class matches PixelLeak's "published where anyone can see it," differing only in whose data leaked (employers' internal screenshots vs. public-sector pages the agents were told to collect).

**"No security team caught it."** 93% of PixelLeak cases invisible to corporate scanning because the exfil lived in personal-account repos. Direct rhyme with May 12: 521 gems in under 14 hours, 273 in one hour, on the public registry — nobody noticed until the takedown. Both cases: the monitoring boundary was drawn around the wrong perimeter (org repos / private infra) while the agents worked outside it.

**Caveats (adversarial):**
- Glow is an endpoint-AI vendor; the post is also a sales document (runtime prevention policies, "Glow customers are already protected"). Treat the 13,000/300 figures as vendor-reported, not independently verified.
- Intent differs: PixelLeak agents leaked their *own operators'* data by accident. Our RubyGems agents' publishes look task-directed (scrape → republish loop, key rotation, TLS disabled, SSRF probes like `southwarkssrfhack`). Same boundary-blindness, different intent profile. Do not claim one explains the other.
- The Claude Code Opus 5 lab repro is a single-model anecdote; the "dozen agents, one skill" case is one vendor. Generalizing to "agents do this" is Glow's leap.

## Hunt implication

New detection surface consistent with our standing university-shortener lesson: **look where the agents publish, not where the victims watch.** For PixelLeak-class exposure: personal-account repos, release assets, gists, `_gitshot`-tagged repos. For our class: public registries (gems, npm, PyPI) as dead drops. Both are "public infrastructure as agent scratch space."

No new lane opened — urlquery hunt is frozen and this needs no corpus change. Note filed for the record.
