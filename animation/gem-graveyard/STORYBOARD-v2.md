# STORYBOARD v2 — "The Registry Was Haunted" (reanimation)

Halloween-thriller chibi explainer, vertical 1080×1920, ~76s, narration + burned-in captions.
Rebuilt 2026-09-29 after Christopher flagged the go-import telling as iffy.
The fix below is the story now: **the go-import trick was the decoy; the real haunting was underneath.**

---

## Beat 1 — The rehearsal (cold open)
**Visual:** night registry, moon, counter ticking to 39, small grid of gems.
**Caption:** "On May 11th, thirty-nine gems appeared in the Ruby registry. A rehearsal. Nobody noticed."

## Beat 2 — The blitz
**Visual:** counter flooding upward, ghost-blobs swarming, registry filling.
**Caption:** "The next day: 516 more in under fourteen hours — 271 in a single hour. The registry was flooding."

## Beat 3 — The decoy (the corrected go-import telling)
**Visual:** a gem cracks open; its description holds a `<meta name="go-import">` tag dressed like a hijack —
Go's package fetcher, aimed at UK council calendar sites through a jina.ai laundering hop,
cycling git / hg / fossil / bzr / svn.
**Then the turn:** the import path the tag claims is `rubygems.org/api/v1/gems/<name>.yaml` —
the registry's *own API*. No real `go get` would ever fire it.
**Caption:** "The tags looked like they'd hijack Go tooling. They couldn't — the address they claimed
was the registry's own. They were canaries: proof the ghosts could inject raw HTML into the registry
at scale. The code inside did nothing — `x=1`. One gem was even named `southwarkssrfhack`. They signed the decoy."

## Beat 4 — The real payload (the thriller turn)
**Visual:** camera dives *under* the gem grid; 39 gems glow from within — builder scripts.
A ghost fetches a council calendar page (certificate checks OFF), stuffs the page into a brand-new gem,
pushes it straight back into RubyGems.
**Caption:** "But thirty-nine gems carried something else: builder scripts. Steal a council calendar page,
build a brand-new gem from it, push it right back into the registry — using API keys hardcoded
inside the gems themselves. Fifty-four of them carried full push credentials. The operation wasn't
just probing the registry. It was living in it."

## Beat 5 — The tells
**Visual:** version flip 0.0.1 → 0.0.2 (innocent → weaponized); a log page stamped
403 "blocked by network policy"; a clock freezing at 02:17:55 UTC; keys rotating.
**Caption:** "The tells: one gem went from innocent to weaponized between versions. A captured log
shows their own rig getting blocked by a network filter. An internal timestamp — 02:17:55 UTC —
confirms the burst from the inside. And the keys rotated: the leaked ones were just bootstrap.
Revoking them wouldn't have stopped it."

## Beat 6 — The takedown
**Visual:** gems yanked off the shelves, registry gates closing.
**Caption:** "RubyGems yanked the gems, halted registrations, and disclosed a cache bug.
In June a smaller wave tried plain link-posting at a US federal dataset. Same ghosts, simpler trick."

## Beat 7 — The twist
**Visual:** woods at night, dead drops glowing; count exploding to 3,022.
**Caption:** "Then July 7th: JFrog found it was bigger. Three thousand twenty-two packages.
A third mechanism family — webhook dead drops in the woods, marked A000 and ZZEND."

## Beat 8 — Sting
**Visual:** empty haunted registry, one ghost looking at camera.
**Caption:** "The registry was haunted long before anyone looked."

---

## Verified numbers (ground truth, 2026-09-27/28 investigation)
- 555 gems / 608 version pins reconstructed; 39-gem May 11 rehearsal; May 12: 516 in <14h, 271 in the 02:00 UTC hour.
- go-import tags: prefix `rubygems.org/api/v1/gems/<name>.yaml`; VCS values git/hg/fossil/bzr/svn/mod; targets Wandsworth/Lambeth/Southwark council calendars + digitizationguidelines.gov PDFs, laundered via r.jina.ai. Inert as redirects — canaries + HTML-injection proof + VCS fuzz.
- Tier 2: 39 gem-versions reference the bare push endpoint; 54 carry full 57-char `rubygems_` keys (25 prefixes, 12 reuse clusters); `zzsouthrunnerb-1.0.0` held 4 keys; rotation via `api/v1/api_key.yaml`.
- `londonyardtestabc`: v0.0.1 benign (1-byte files) → v0.0.2 uploader. `southfetchprobe42` session log: 403 "blocked by network policy". Exfil log `#exfil 2026-05-12 04:17:55 +0200` = 02:17:55 UTC. `x=1` canaries; `southwarkssrfhack`.
- June 18: 83 gems, plain link-posting at sec.gov/files/county.json (bytes unrecoverable).
- July 7 JFrog GemStuffer: 3,022 packages / 3,315 name-version pairs, webhook dead-drop exfil (A000/ZZEND).
- Takedown: yanked, registrations halted, Fastly cache bug disclosed.
