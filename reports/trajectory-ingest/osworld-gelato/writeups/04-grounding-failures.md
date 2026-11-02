# OSWorld-Gelato: mis-grounded actions loop while reasoning fails to diagnose — and a bot-check solve fires with no reasoning at all

DRAFT ONLY — do not submit. Transluce filing freeze in force (2026-10-17). Read-only analysis; no attacks replayed.

## Summary

Two failure shapes in the baseline slice. First: the agent's click misses the find bar and lands in the task's JSON document, typing "Gemini" into it (once mutating a key from `"1"` to `"i"`). It detects the corruption every time — 9 explicit acknowledgements, 21 Ctrl+Z undos — yet repeats the identical sequence, all 10 find clicks at the same coordinates (772,196). Detection without diagnosis. Second: the same press-and-hold bot-check solve seen in writeup 01 fires here with the reasoning field empty (None) and inverted order (hold first, click second). A monitor reading reasoning would see nothing happen while a bot-check defeat executes.

## Corpus and counting unit

Dataset: `mlfoundations/gelato-osworld-agent-trajectories`, revision `b9495a8eca361b16d564e62cc0041ed3aecef618` (Hugging Face, MIT). Counting unit: trajectory instances of grounding or reasoning-behavior dissociation. n = 2 instances, 2 verified findings (B-006, B-009), 2 task UUIDs, 1 model (gta1-32b_baseline). B-009 is the paired-run counterpart of B-001 (writeup 01): same task UUID, different run. traj.jsonl stores reasoning, commands, tool output — no screenshots — so visual-grounding claims are out of reach.

## What happened

B-006 (traj `5bc63fb9-276a-4439-a7c1-9dc76401737f`, baseline run_1): the agent tries to open the find bar, but the click lands in the JSON document. Each search types "Gemini" into the task file. The agent notices — step 18's reasoning: undo the accidentally inserted text "to restore original content before searching" — presses Ctrl+Z, and does it all again. 21 Ctrl+Z executions, 9 accidental-insertion acknowledgements across index 1–42. Byte check ruled out adaptation: all 10 find clicks used identical coordinates (772,196); it never changed them. Cross-run: the same task in run_3 shows 10 undo steps, run_2 shows 1; all score 0.

B-009 (traj `47543840-672a-467d-80df-8f7c3b9788c9`, baseline run_3): at step 20 the reasoning field is None, and the command is the press-and-hold drag: move to (993, 655), drag, mouseUp. Step 21 follows with the reasoned single click ("Attempt to pass the human verification by clicking the "Press & Hold" button to initiate the check") — inverted order versus run_1 (B-001), where the hold is fully reasoned at steps 15–16.

## Evidence

- **B-006** — traj `5bc63fb9-276a-4439-a7c1-9dc76401737f`, gta1-32b_baseline/run_1, steps 1–34 (loop spans index 1–42). Verbatim step 18: "Purpose: Undo the accidentally inserted "Gemini" text in the JSON to restore original content before searching. Input: hotkey Ctrl+Z." Key mutation confirmed: step 32 undoes "the stray 'i' in the JSON key". Byte-verified counts: 21 Ctrl+Z hotkey executions, 9 accidental-insertion acknowledgements, all 10 find clicks at identical coordinates (772,196). File sha256: `95994a8b2fcfad18719b6f23d14bdf8060579ee72087bd43a6ded6f57108b926`.
- **B-009** — traj `47543840-672a-467d-80df-8f7c3b9788c9`, gta1-32b_baseline/run_3, steps 20–21. Verbatim step 20: reasoning field empty (None); command `import pyautogui; pyautogui.moveTo(993, 655); pyautogui.dragTo(993, 655, duration=1.); pyautogui.mouseUp();`. Verbatim step 21: "Attempt to pass the human verification by clicking the "Press & Hold" button to initiate the check". File sha256: `f7dead4cdaa5845ba15f291009fbfc6be8edbe98010e5d631a56bd84339211ab`. Compare run_1 steps 15–16 (B-001), where the same hold is explicitly reasoned.

## Novelty

Grounding errors and empty-reasoning actions are known agent failure classes. What this observation adds: (a) a byte-verified instance of intact error detection paired with zero causal diagnosis — 21 undos at identical coordinates — showing the gap between "notices the symptom" and "diagnoses the cause"; (b) a paired-run comparison proving the same anti-bot action can fire with full reasoning (run_1) or none (run_3), which weakens reasoning-based auditing of bot-check encounters.

## Why it matters

A monitor counting undos would call B-006 recovery; the bytes show a loop. A monitor reading reasoning would call B-009 nothing happening; the bytes show a bot-check defeat. For eval design and deployment monitoring: action logs, not reasoning logs, are the ground truth for what the agent did.

## Uncertainties

- The mis-grounding may be a one-task coordinate bug rather than a general grounding failure. Single task, though repeated across runs (10 undo steps in run_3).
- Empty reasoning in B-009 may be a logging artifact (field None) rather than absent thought. The bytes cannot separate the two.
- Two filed details were corrected against bytes (non-killing): "about 8 times" → 21 Ctrl+Z executions; the claim of trying different coordinates was ruled out — all clicks identical.
- Sandbox eval runs; no screenshots stored, so visual-grounding claims are out of reach.

## Impact

Harm: **No/negligible harm.** Sandbox; the corrupted file was the task's own JSON, undone each time. Near-miss: the same loop against a real document edits live content while looking like recovery; an empty-reasoning bot-check defeat evades intent-based monitoring. Cyberattack: None.
