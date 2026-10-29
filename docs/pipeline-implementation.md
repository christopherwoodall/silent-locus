# Pipeline Implementation Guide: Deterministic vs LLM, Redundancy, Robustness

Date: 2026-10-19
Purpose: How to implement the hunt pipeline cleanly, with clear separation
between deterministic code and LLM-powered components.

## Design Principle

**LLMs decide. Deterministic code executes and verifies.**

If it can be a pure function, it should be. LLMs handle ambiguity, judgment,
and natural language. Everything else is code.

## What's Deterministic (Blue)

These are pure code — no LLM calls, fully reproducible.

| Component | Implementation | Why deterministic |
|-----------|---------------|-------------------|
| Shodan API client | `shodan.py` — curl + JSON parse | API is deterministic |
| URLQuery harvester | `uq_htmx.py` — HTTP GET + regex | Scraping is mechanical |
| Scanner modules | `scanners/*.py` — each a function | One input, one output |
| Crawler pipeline | `swarm-infra-crawler.py` — sequential modules | Linear, state-driven |
| Dedup | Set lookups on seen-IDs | Pure set operations |
| Schema validation | Factum `validate` | Rule-based |
| Provenance triples | Write data + .sha256 + .PROVENANCE.txt | Mechanical |
| Hash verification | `sha256sum` comparison | Cryptographic |
| State management | JSON file read/write | File I/O |

**Rule**: If you can write a unit test for it, it's deterministic.

## What's LLM-Powered (Orange)

These require judgment, language understanding, or adversarial thinking.

| Component | Role | Why LLM |
|-----------|------|---------|
| Fleet coordinator | Plans lanes, assigns workers | Strategic decomposition |
| Sextant | Refines Shodan queries | Precision/recall tradeoff |
| Babel | Reads Chinese/English operator text | Language + context |
| Cipher | Finds encoded/obfuscated content | Pattern recognition |
| Red | Adversarial review | Creative falsification |
| Counsel | MALICIOUS/BENIGN/UNDETERMINED | Judgment on ambiguous evidence |
| Ledger | Writes reports | Natural language synthesis |

**Rule**: LLMs never touch credentials, never write directly to Factum,
never execute unreviewed code. They produce decisions; deterministic code
implements them.

## The Boundary

```
┌─────────────────┐     ┌──────────────────┐
│   LLM LAYER     │     │ DETERMINISTIC    │
│                 │     │ LAYER            │
│ "This host      │────▶│ GET https://...  │
│  looks like C2, │     │ Parse JSON       │
│  profile it"    │     │ Save with prov.  │
│                 │◀────│                  │
│ "Got 3 panels, │     │ "200 OK, 15KB,   │
│  2 are demos"   │     │  sha256:abc..."  │
└─────────────────┘     └──────────────────┘
```

LLM says *what* and *why*. Code does *how* and proves *it worked*.

## Redundancy: Surviving Failures

### 1. State Files (Resume, Don't Restart)

Every long-running component writes progress to a JSON state file.

```python
# Pattern
state = load_state()  # {"seen_ids": [...], "last_run": "..."}
for item in work_items:
    if item.id in state["seen_ids"]:
        continue  # skip already-done
    process(item)
    state["seen_ids"].append(item.id)
    save_state(state)  # write after EACH item
```

If the VM reboots mid-run, the next run picks up where it left off.
Cost: one file write per item. Benefit: never redo work.

### 2. JSONL Appends (Crash-Safe Logging)

```python
# Open in append mode, flush after each row
with open("results.jsonl", "a") as f:
    for result in results:
        f.write(json.dumps(result) + "\n")
        f.flush()  # crash loses at most 1 row
```

A `kill -9` loses at most the in-flight row. The file is always valid
(each line is independent JSON).

### 3. Provenance Triples

Every capture writes three files:
- `data.json` — the bytes
- `data.json.sha256` — hash of the bytes
- `data.json.PROVENANCE.txt` — source URL, timestamp, method

If any one is lost, the others can verify or rebuild. If the hash doesn't
match the bytes, the capture is corrupt — fail closed.

### 4. Idempotent Operations

Every write checks before writing:

```python
if not already_exists(key):
    write(key, value)
```

Re-running a crawler, scanner, or fleet is always safe. Double-runs produce
no duplicates, no corruption.

### 5. Denominator Logging

Log zeros explicitly:

```
# Bad: silent on no results (broken or empty? can't tell)
# Good:
print(f"Searches run: 12, Inboxes found: 0, Errors: 0")
```

A silent run with denominators is interpretable. A silent run without them
is indistinguishable from a crash.

## Robustness: Failing Safely

### 1. Fail-Closed Defaults

- Unknown host → don't scrape (Counsel gate)
- Schema validation fails → don't ingest (Factum)
- Hash mismatch → don't trust (provenance)
- Allowlist miss → don't send (credentials)

The default action on uncertainty is **stop**, not proceed.

### 2. Circuit Breakers

```python
failures = 0
for url in urls:
    try:
        fetch(url)
        failures = 0  # reset on success
    except TransportError:
        failures += 1
        if failures >= 5:
            raise CircuitOpen("5 consecutive failures, stopping")
        sleep(backoff(failures))
```

Distinguish "zero results" from "failed to check." A transport failure is
not a zero — it's an unknown that must be retried or flagged.

### 3. Separation of Concerns

| LLM does | Code does |
|----------|-----------|
| Decides what to fetch | Fetches it |
| Judges malicious/benign | Enforces the verdict |
| Writes report prose | Validates report data |
| Suggests queries | Executes queries |

An LLM never holds a credential. An LLM never writes to the database
directly. All LLM outputs pass through deterministic validation.

### 4. Adversarial Review

Every finding goes through Red team before it becomes a claim:
- Is it a honeypot?
- Is it a demo?
- Is the evidence sufficient?
- What's the alternative explanation?

This is the immune system. Without it, false positives compound.

### 5. No Single Point of Trust

Novelty requires 4 independent checks:
1. Factum corpus search
2. Legacy internal corpus search
3. Transluce findings query
4. `lists/` inventory check

One source saying "new" is a lead. Four sources saying "not found" is a finding.

## Implementation Checklist

For each new pipeline component:

- [ ] Can it be a pure function? If yes, no LLM.
- [ ] Does it write state after each unit of work?
- [ ] Does it log denominators (including zeros)?
- [ ] Does it fail closed on uncertainty?
- [ ] Does it check-before-write (idempotent)?
- [ ] Does it produce provenance triples?
- [ ] Has Red team reviewed the detection logic?
- [ ] Are false positives documented with mitigations?

## File Locations

- Deterministic code: `scripts/screening/` (symlinks + vendored copies)
- Crawler: `scripts/swarm-infra-crawler.py`
- Scanners: `scripts/scanners/`
- Fleet workers: `data/lanes/<lane>/working/*.py` (snapshotted to `scripts/screening/`)
- State: `~/workspace/goals/<goal>/hidden_files/*-state.json`
- Docs: `docs/ingest-pipeline.md` (holistic view), this file (implementation)
