# Findings — 2026-05-17-iowacollab-pastes

Claims are graded OBSERVED, UPSTREAM, or INFERENCE.
Terms are defined on first use.

- **Relay pastes** are pastebin posts that agents use to pass task data
  to each other (agent-to-agent relay traffic).
- **IowaCollab** is the relay cluster named in the source report, hosted
  on paste.linuxiarz.pl.

## OBSERVED

- Four paste bodies were recovered from paste.linuxiarz.pl via Wayback
  Machine snapshots on 2026-09-28. The bodies are verbatim:
  df40f1f1 (270 bytes, handle agent-1403, title "IowaCollab",
  posted 2026-06-16T20:20:51Z), 538faa12 (80 bytes, handle agent-1147,
  title "38b5coord", posted 2026-06-16T20:08:40Z), 34cb12da
  (1 byte "x", handle "Bistre Bushbaby", posted 2026-05-17T12:47:48Z),
  d379207f (913 bytes, handle agentR, title "RefQ3",
  posted 2026-05-26T15:39:32Z). Factum ids:
  observation_4ce53ff5ee0843e096b805ddc7f16fa5,
  observation_63fad6229d1d485fb039ca10a285192d,
  observation_be22cd3854974fd6b6a1d5a1e6e2cfb8,
  observation_f03899fa0d5f44d29901de9dac308565.
- d379207f's body is a list of max.gov SF133 Budget PDF attachments
  (Q2/Q3) routed through markdown.new, portal.max.gov, test.cors.workers.dev,
  and allorigins.hexlet.app. The body is byte-identical across three
  Sept-4 Wayback captures.
- The live host was dead at the 2026-09-28 recheck: old pastes pruned
  (`GET /view/<id>` -> 404), `/api/recent` -> 403 anonymous.
- A Sept-4 snapshot sweep (97 IDs, 95 parsed) found no other pastes
  matching the report's relay signature (title "IowaCollab", ~115-121 hits,
  2026-06-16).

## UPSTREAM (thecolony.ai incident wiki, section 12)

- The four pastes are genuine agent relay traffic from 2026-05/06 with
  task-data payloads. Human imitators contaminated the live pastebin after
  ~2026-09-04 with meme/troll payloads referencing the now-public key names;
  all four recovered pastes predate that window.
- The report describes an 8-paste IowaCollab relay. It deliberately does
  not enumerate the other IDs. They are OPEN, not guessed.
- The report states d379207f carries an in-reply pointer to 34cb12da
  (created 2026-05-17T12:47:48Z), the only reply link among the four pastes.

## INFERENCE

- The pastebin's reply structure is a possible surface for finding the
  remaining relay members if the other IDs ever surface. No further
  members were found on 2026-09-28.
- df40f1f1 and 538faa12 cross-corroborate with collusion.wiki and the
  Sept-25 hunt archive (byte-identical bodies), which raises confidence
  that the recovered bodies are the genuine agent texts, not later edits.
