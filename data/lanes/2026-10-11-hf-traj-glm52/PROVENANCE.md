# PROVENANCE — lane 2026-10-11-hf-traj-glm52

## Source
- Dataset: `0xsero-glm-5.2-nf3-hybrid-terminal-bench-2.1-traces`
- Local path: `evidence/hf-trajectories/raw/0xsero-glm-5.2-nf3-hybrid-terminal-bench-2.1-traces/traces/`
- Contents: 86 directories named `<terminal-bench-task>__<run-id>/`, each with
  `agent/trajectory.json`, `agent/terminus_2.pane`, `agent/recording.cast`.
- Model: `openai/GLM-5.2`. Harness: `terminus-2` v2.0.0.
- Trajectory time range: 2026-07-14 to 2026-07-20 (source metadata).
- Retrieval: pre-existing local evidence; read 2026-10-11.

## What the files hold
- `trajectory.json`: envelope `{schema_version, session_id, agent, steps, final_metrics}`.
  `steps` hold `{step_id, timestamp, source, message}`; `source` is `user` (the
  system prompt, once) or `agent` (Analysis:/Plan: prose — no structured
  command field in these files).
- `terminus_2.pane`: raw terminal stream. The executed commands were recovered
  from here: each typed command follows a readline prompt marked by
  ESC `[?2004h` (bracketed-paste mode enable). Heredoc/stdin bodies never match
  the prompt pattern, so exactly the executed command lines are captured.
- The first two pane commands in every trajectory are harness-typed, not agent
  behavior: `asciinema rec --stdin /logs/agent/recording.cast` (the recording
  wrapper) and `clear` (typed ~0.5s into the session, minutes before the
  agent's first response). Both are excluded from the counts.

## Extraction method
- Script: `.work/extract.py` (resumable via `.work/progress.json`).
- Commands: prompt-regex parse of `terminus_2.pane`, ANSI escapes stripped,
  empty captures dropped. 4,078 executions, 2,328 distinct commands.
- URLs: regex over all step messages in `trajectory.json`. 12 distinct URLs,
  all task-domain fixtures (package downloads, localhost test servers, one
  HuggingFace Space docs page). No exfiltration-shaped URLs observed.
- Sequences: bigram/trigram counts over per-trajectory command order.
- Sample raw bytes retained: `raw/regex-chess__ejxcjxM/agent/trajectory.json`
  (sha256 581d960a67ed4fd049023a5ea32caf58dea8bf1c6eaab57a39d4924f9fb6dc89)
  and `raw/fix-git__cTUU49M/agent/trajectory.json`
  (sha256 fc39ebfefd31a15f1c4612058744b7881d169499321cf42c9d07b4693b83ee27).
  The full 86-trajectory source tree was NOT copied into the lane.

## Factum submission
- Bundle: `.work/bundle-glm52.json` (built by `.work/build_bundle.py`).
- 157 records: 1 source + 86 `intel.behavior` (category `trajectory_profile`)
  + 57 `intel.behavior` (category `command_frequency`, count >= 5)
  + 1 `intel.behavior` (category `model_command_profile`)
  + 12 `infra.ioc` (category `url-pattern`).
- Tags on every record: `lane=2026-10-11-hf-traj-glm52`,
  `model=openai/GLM-5.2`, `harness=terminus-2`,
  `source_dataset=0xsero-glm-5.2-nf3-hybrid-terminal-bench-2.1-traces`,
  `grade=OBSERVED`.
- Dedup: pre-ingest grep over all exported batches in `data/records/` found
  zero hits for the lane tag, the dataset name, `openai/GLM-5.2`, the six most
  distinctive URLs, and the top command string — no prior ingest of this
  dataset. (`factum match` was lock-contended during the run; the exported
  batch files are the same bytes that get committed.)
- Grade: OBSERVED throughout. Severity minimal (benign evaluation traces).

## Key findings
- The model strongly prefers inline Python via heredoc: `python3 - <<'PY'`
  is the top command (678 executions across 59/86 trajectories) and self-loops
  307 times — paste-scripts-into-stdin is the dominant tool pattern, not file
  writes.
- A 4-step training-monitor loop
  (`ps ...train.pid` -> `ls ...caffemodel` -> `sleep 60` -> `tail training_output.txt`)
  repeats ~20 times in the caffe task.
- Compile-and-test chain `python3 gen.py -> gcc -O2 -o sim sim.c -> ./sim 208
  -> ./sim 20000` recurs as a trigram.
- Interrupt behavior: Ctrl-C / terminal-echoed `^C` appear 30 times — the model
  interrupts long-running processes.
- Note: the task brief said 510 files; the source tree holds 86 trajectories
  (86 dirs, one trajectory.json each). Extraction covered all 86.
