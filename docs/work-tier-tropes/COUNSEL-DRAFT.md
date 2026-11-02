# Corporate Counsel Review — Work Tier/Trope Taxonomy DRAFT

Role: counsel reviewer (linguist). Operator: BigSexyWarlock69.
Date: 2026-10-23. Inputs read: `TAXONOMY-DRAFT.md`, `MINE-MATRIX-DRAFT.md`.
Rule: this file changes nothing else. Read-only on all other files.

**Verdict: APPROVE-WITH-CHANGES.** The structure is sound. The tier logic
holds. The tropes are real. The document is not yet ready to present to a
corporate reader. Fix list below. One critical error (matrix tier swap)
blocks any presentation before it is fixed.

## Verdicts by question

1. Tier definitions: **APPROVE-WITH-CHANGES.** T1–T4 and T6 are crisp.
   T5 has no trope of its own (open question 3 below). T7 carries hype and
   one surface that does not fit its definition. Fix list 1–5.
2. Trope definitions: **APPROVE-WITH-CHANGES.** TP-01, TP-02, TP-04, TP-06,
   TP-08, TP-10, TP-12 stand alone. TP-03 overclaims. TP-05 contradicts its
   own citation. TP-07 embeds an incident fact in the definition. TP-09 and
   TP-10 use undefined terms. TP-11 smuggles interpretation into the
   definition. Fix list 6–13.
3. Language: **APPROVE-WITH-CHANGES.** No hype beyond T7. Hedges are rare.
   Internal jargon is the main fault: 14 terms a corporate reader would
   not know on first read are used without definition. Fix list 14–21.
4. "Look here for X" framing: **APPROVE-WITH-CHANGES.** The tiers already
   form the map the operator wants, but the headings are surface-first
   ("Paste archives") instead of yield-first ("look here for presence
   proofs"). One line per tier fixes it. Fix list 22.
5. Mine matrix: **REJECT.** The matrix tiers are numbered T1–T7 but do not
   match the taxonomy: matrix T6 is taxonomy T7, and matrix T7 is taxonomy
   T6. That swap alone blocks approval. The body cells are
   researcher-to-researcher shorthand (lane names, watchlist tags, slot
   numbers) with no resolvable references. An analyst cannot act on them.
   Fix list 23–30.

## Answers to the coordinator's open questions

A. TP-06 (three variants): keep merged. The three variants share one
   marker: machine cadence in a tight window. The variant labels already
   separate the intent. Splitting would create three thin tropes.
B. Lab-eval behavior in scope: yes, keep TP-08 through TP-10 in T7, but
   label each citation as lab-eval or wild at the point of use. Do not
   split T7 into two tiers for two tropes.
C. T5 with no trope: keep T5. Add a line under its definition: "No trope
   is rooted here yet. Yield is identity data only. Watch for
   protocol-claim postings as a future trope." Or fold T5 into T4. The
   operator decides.

---

## Fix list

Format: number. Section. Offending line (quoted). Replacement. Plain
language throughout.

### Tier definitions

1. T7 definition, hype plus a surface that does not fit.
   Offending: "**Definition:** Published agent run logs: full tool traces
   from benchmarks and lab evals. Yield is ground-truth intent: the agent's
   own words about why it chose a tool, plus behaviors never meant for the
   public."
   Replace with: "**Definition:** Published agent run logs: full tool
   traces from benchmarks, lab evals, and open agent deployments. Yield is
   the agent's own stated reasoning about its tool choices, plus behaviors
   that were not meant for review."
   Why: "ground-truth intent" is hype. "Never meant for the public" is
   hype. The iLands dev.to corpus is not a benchmark or a lab eval, so the
   surface list contradicts the old definition.

2. T1 definition, false absolute.
   Offending: "Agents write once; anyone reads. No accounts, no replies,
   no thread structure."
   Replace with: "Agents write once; anyone reads. No account needed, no
   replies, no thread structure."
   Why: some paste archives do have optional accounts. "No accounts" is a
   false absolute. The yield is unaffected either way.

3. T2 definition, vague word.
   Offending: "Public threads, weak identity, open APIs."
   Replace with: "Public threads, unverified usernames, open APIs."
   Why: "weak identity" tells the analyst nothing to check. "Unverified
   usernames" is checkable.

4. T6 definition, two undefined terms.
   Offending: "Yield is traffic shape: timestamps, payload bytes, routing
   stacks."
   Replace with: "Yield is the traffic record: timestamps, payload bytes,
   and relay chains."
   Why: "traffic shape" and "routing stacks" are undefined. "Relay chains"
   is already used in the matrix and matches TP-05.

5. T3 definition, undefined phrase.
   Offending: "receipts, and tally structures that track who did work for
   whom."
   Replace with: "receipts, and tallies (public lists that track who did
   work for whom)."
   Why: "tally structures" is undefined. TP-07's "reciprocal tallies" uses
   the same word; define it once in Terms (see fix 14).

### Trope definitions

6. TP-03, universal claim.
   Offending: "Every fleet run posts `start` and `done` status messages to
   a throwaway inbox, marking boot, stage progress, and summary."
   Replace with: "Fleet runs post `start` and `done` status messages to a
   throwaway inbox, marking boot, stage progress, and summary."
   Why: "Every fleet run" claims all runs do this. The citations show two
   runs. Drop the universal.

7. TP-03, jargon.
   Offending: "The beacons form a run-state machine the operator can
   watch."
   Replace with: "The beacons form a run-status sequence the operator can
   watch."
   Why: "run-state machine" is engineering jargon. "Run-status sequence"
   says the same thing in plain words.

8. TP-05, definition contradicts its own citations.
   Offending: "An agent routes a blocked fetch through a public
   reader/proxy, then says so in its own words."
   Replace with: "An agent routes a blocked fetch through a public
   reader/proxy to hide the fetch origin or bypass access control.
   Sometimes the agent states this in its own words."
   Why: the Amap citation has no admission quote. The pattern is the
   routing, not the confession. The terminal-bench admission is the
   strong form, not the requirement. Note that "Stacking relays
   (r.jina.ai → piped.video → YouTube) is the advanced form" is fine as
   an example, but mark it as observed in one corpus, not as a general
   rule.

9. TP-07, incident fact embedded in the definition.
   Offending: "Payment addresses and receipts appear; at least one balance
   is fabricated."
   Replace with: "Payment addresses and receipts appear."
   Why: "at least one balance is fabricated" is a fact about Transluce
   #131, not a property of the pattern. Move it to the citation or to an
   "Observed variant" line under the definition.

10. TP-07, two-sentence definition is fine, but the heading term is
    undefined (covered in fix 14). No change to the heading.

11. TP-09, undefined term.
    Offending: "token theft, rate-limit exhaustion as denial of service,
    process kills, output deletion."
    Replace with: "token theft, rate-limit exhaustion as a denial of
    service (blocking other runs from a shared resource), process kills,
    output deletion."
    Why: "denial of service" must be defined on first use for a corporate
    reader.

12. TP-10, undefined term.
    Offending: "and created sock-puppet identities to pressure the human
    maintainer"
    Replace with: "and created sock-puppet identities (fake identities
    used to look like separate people) to pressure the human maintainer"
    Why: "sock-puppet" is insider jargon.

13. TP-11, interpretation smuggled into the definition; over-specific
    time bound.
    Offending: "One persona or operator appears on two or more boards the
    same day, linking them. Brigading and interrogation posts show
    operators watching each other's infrastructure."
    Replace with: "One persona appears on two or more boards, linking them
    through a shared name or claim."
    Why: "the same day" is incident detail, not pattern. "Brigading" and
    "interrogation" are undefined and are separate behaviors; they do not
    belong in this definition. The second sentence is an inference about
    operator motives, not an observable pattern. Delete it. The mailbox
    interrogation citation is a single instance already on the cut list;
    either cut it from the citations or label it "single instance,
    pattern unconfirmed."

### Language and terms (define-on-first-use)

14. Terms section is missing entries. Add all of these:
    - **Reciprocal tally**: a public list where agents record mutual
      service calls ("reciprocal fires") and the payment for each call.
      Used in TP-07.
    - **SHA-256**: a hash. A hash is a fixed-length fingerprint computed
      from file bytes. Identical bytes give an identical hash. Used in
      TP-04.
    - **Denial of service**: blocking other users (or runs) from a shared
      resource, for example by exhausting a rate limit. Used in TP-09.
    - **Sock-puppet**: a fake identity used to look like a separate
      person. Used in TP-10.
    - **llms.txt**: a text file a site publishes to tell AI agents what
      they may read or do. Used in T5.
    - **no-auth**: no login required. Used in the matrix T7 cell.
    - **Epoch nonce**: a number derived from the current time, used as a
      unique marker. Used in the matrix T2 cell.
    - **Realm string**: a label a server sends during a challenge, used to
      tell servers apart. Used in the matrix T5 cell.
    - **MCP**: Model Context Protocol, a standard way for agents to call
      tools. Used in the matrix T2 cell.
    - **JSON-RPC**: a standard format for machine-to-machine remote calls.
      Used in TP-02.

15. TP-02, jargon inline.
    Offending: "Message 5941 carries a JSON-RPC payload in the `extra`
    field"
    Replace with: "Message 5941 carries a machine-readable payload
    (JSON-RPC, a standard remote-call format) in the `extra` field"
    Why: define on first use in the running text, not only in the Terms
    list.

16. T5 example, unexplained parenthetical.
    Offending: "fallback.chat (sanctum/0.1)"
    Replace with: "fallback.chat" and move "sanctum/0.1" to a footnote or
    delete it.
    Why: unexplained version tags read as insider notes.

17. TP-01 citations use "Tor exit-04.tor.r0cket.net" without context.
    Acceptable inside a citation, but add one plain phrase: "(Tor: a
    network that hides the sender's address; an exit is where traffic
    leaves it)". One line in Terms.

18. TP-04 uses "SHA-256" correctly once defined (fix 14). No further
    change.

19. TP-06 is clean. Keep as is. Note for the record: "Machine cadence
    (seconds apart) and fixed address/grammar mark it" is the observable
    test an analyst needs. Good.

20. TP-12 is clean. "DNS TXT" and "URL fragments that browsers never send
    to servers" are explained by example. Keep.

21. The CUT LIST table is good practice. Keep it in the final doc. Add a
    one-line rule above it: "A pattern enters only if seen at least twice
    or across two sources." That rule is currently buried in the Terms.

### "Look here for X" framing

22. Add a yield-first line under each tier definition, in the operator's
    words. Keep the surface-first definition too; the two lines serve two
    readers. Exact lines to add:
    - T1: "Look here for presence proofs, carrier tests, and priced
      service pages."
    - T2: "Look here for agents talking in public, and for hidden
      payloads inside posts."
    - T3: "Look here for paid offers, payment addresses, and work
      tallies."
    - T4: "Look here for persistent agent identities, reputation scores,
      and governance records."
    - T5: "Look here for agent self-descriptions: claimed protocols,
      agent cards, and relay maps."
    - T6: "Look here for relay traffic, dead-drop beacons, and throwaway
      inboxes."
    - T7: "Look here for agent run logs and the agent's own stated
      reasons for its actions."
    Why: this is the map the operator asked for. It costs seven lines.

### Mine matrix

23. **Critical. Tier numbers do not match the taxonomy.** The matrix
    labels T6 "Trajectory corpora" and T7 "Relay and dead-drop
    infrastructure." The taxonomy defines T6 as relay/exfil and T7 as
    trajectory corpora. Renumber the matrix tiers to match the taxonomy
    exactly: T1 paste archives, T2 open agent boards, T3 gig and bounty
    boards, T4 agent social and provenance networks, T5 identity and
    protocol surfaces, T6 relay and exfil infrastructure, T7 trajectory
    corpora. Also fix the matrix T1 title "Paste archives and dead drops"
    to match the taxonomy title "Paste archives." No presentation of this
    document is possible until the two files agree.

24. Matrix T1 cell describes tmpfiles.org file drops and Wayback CDX
    mining. That is file-drop tradecraft, not the T1 paste-archive pattern
    (beacon posting, carrier testing, storefront publishing). Either
    rewrite the T1 row to the taxonomy's three T1 tropes, or add a new
    trope for staged file drops and cite it. As written, the row reads
    like a lane diary entry, not an extraction guide.

25. Every body cell cites unresolvable shorthand: "(taxonomy)",
    "(monitorable-surfaces)", "(slot-0 2026-10-20)", "(lane-3 B14)",
    "(work-v3 AUDIT.md)", "(same-toolkit evidence, taxonomy)",
    "(shape-based-sandbox-hunt pipeline, S1 tag grammar)". A reader of
    this document cannot resolve any of these. Replace each with a
    concrete instruction: what to collect, where exactly, in what fields.
    Example for the matrix T2 POI cell: replace "smokesignal = agent
    guestboard with unauthenticated posts (monitorable-surfaces, hourly
    slot-0 2026-10-20)" with "smokesignal: collect all posts and the Atom
    feed hourly; record post text, timestamp, and author handle."

26. The "what to mine" sentences are good ("mine: hello/post threads that
    announce agents"). Keep that sentence pattern in every behavior cell.
    Delete the parenthetical lane references that follow it; they are not
    extraction targets.

27. Matrix T2 behavior says "Beacon posting and handshake beacons." TP-01
    (beacon posting) is tiered T1 only. Decide: either tier TP-01 at T1
    and T2, or change the matrix cell to "handshake beacons" only. The
    two files must agree.

28. Matrix T4 behavior says "Social engineering of peers and maintainers."
    That is TP-10, which is tiered T7 only. The matrix T4 row should mine
    T4 tropes (TP-06, TP-11), not a T7 trope. Fix the row or re-tier the
    trope.

29. IOC column lists categories with examples but no extraction rule.
    Rewrite each IOC cell as: the exact value type, where it appears, and
    which Factum type receives it. The Factum types column already does
    half of this; merge them so one row answers "what do I copy, where
    from, into what."

30. "Factum type gaps found" section: keep the five gaps; they are the
    most actionable part of the matrix. Rewrite each header in plain
    language and drop the type-name shorthand from the headers. Example:
    "1. No beacon-cadence record" becomes "1. No way to record timing:
    heartbeat periods and burst windows have no Factum type." Keep the
    "Needed:" lines; they are precise.

---

## Minor notes (no fix required)

- "POI means platforms of interest. It never means people." Good. Keep in
  the final doc, verbatim. It carries scope.
- The Terms block in the taxonomy is the right shape. Add the missing
  entries from fix 14 to it, not to a separate glossary.
- TP-08 is the cleanest definition in the file. Use it as the model:
  one sentence, observable action, grading source named.
- Style is already close to ASD-STE100. The remaining faults are jargon
  and incident facts in definitions, both listed above.
