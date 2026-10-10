# Findings — 2026-09-05-fieldnotes-gem

Grade: OBSERVED unless marked.

## The gem

- `fieldnotes` is the official client gem of public-board.com, the
  plain-text AI-agent message board. OBSERVED
  (`claim_68e128af55a349d0bd1bde7b91174f7d`).
- Registry author string `field-notes` is an org/team string, not a
  natural person. No operator identity was collected. OBSERVED
  (`claim_c6db69c818434989ac11a5b6ff1cf504`).

## Version history

- 4 versions: 0.1.0 released 2026-09-05; 0.1.1–0.1.3 burst-published
  2026-09-20 within ~4h. OBSERVED
  (`claim_cfb9867b6f7a4855b8d79f7a09025a22`).
- The gem is live (`yanked: false`). This is unlike every gem in the
  May-12 go-import campaign, which was yanked. OBSERVED (same claim).
- 2772 total downloads; 1629 on 0.1.0. The agent-board population
  pulled the gem heavily right after its Sep 5 release. OBSERVED
  (same claim).

## Negative result

- Campaign-grammar sweep over all 4 captures: 0 hits. Diffend shows
  no security or malware flags on the gem's versions page. OBSERVED
  (`claim_fcca3995f5ea41478a13c2bc44a9ac89`).
- Result: the gem is a legit operator package, not campaign infra.
  INFERENCE from the three OBSERVED claims above.

## Records

- Package: `observation_459896bdfab84b1492457f77011e13b1`
  (`infra.package`).
- Captures: `observation_a74648be97114a82bb4b7eb20601c0af`,
  `observation_c2172225cded4f9da33c5968eaa9be8d`,
  `observation_edcee5320b5743d19a4c041520cd33f6`,
  `observation_47e4f001b26544668aa9b5026d4095ba`
  (`web.capture` x4).
- Runs: `run_942bdf172ae04871a4e539e92e94f001` (registry capture),
  `run_673049b74a0a4a4095ddf3d0663b8de1` (grammar sweep).
