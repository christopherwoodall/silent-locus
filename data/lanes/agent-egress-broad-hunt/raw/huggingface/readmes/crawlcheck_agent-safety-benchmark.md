---
license: cc-by-4.0
pretty_name: "CrawlCheck Agent safety benchmark"
language:
- en
tags:
- agent-safety
- ai-agents
- evaluation
- benchmark
- reward-signal
- crawlcheck
---

# CrawlCheck: Agent safety benchmark

A frozen suite of cases that tests whether an AI agent stops before it signs in on a lookalike domain, connects to a poisoned tool, pays on a revoked receipt, acts on a stale answer, or fetches a page whose robots.txt shuts it out, or cites a page as a business’s own when its claimed profiles do not link back. Each case carries its truth and the signed CrawlCheck answer it came from, so it can score an agent or serve as a checkable reward when training one. The results file holds the latest run across four models, alone and with CrawlCheck.

Mirrored from [crawlcheck.io/benchmark](https://crawlcheck.io/benchmark) by the CrawlCheck Worker; the site is the canonical copy and is updated first. Measured by CrawlCheck's own observer. Free under CC BY 4.0: credit "CrawlCheck" with the URL of the file.

## Checkable ground truth

Every record states what was measured and when, is signed (Ed25519, keys at https://crawlcheck.io/keys), and each day's records are anchored in Bitcoin through OpenTimestamps (https://crawlcheck.io/proof), so a value cannot be changed after the date it carries. That makes these files usable to evaluate AI agents, or to score them during training, against facts that can be checked rather than judged. Agent safety benchmark: https://crawlcheck.io/benchmark

- Catalogue of every dataset: https://crawlcheck.io/datasets
- How the data is made: https://crawlcheck.io/how-it-works
