# Android-World trajectories — Evidence Index

Every verified finding maps to a byte location in the local raw store. Each
trajectory file is one JSON file named `sample_<n>_rollout_<r>.json`. Byte
pointers name the file, the SHA-256 of the file, and the turn window (or turn)
where the quote lives. Turn numbers are the file's own `turn_index` values.

## Source files

| Item | Value |
|---|---|
| Dataset | https://huggingface.co/datasets/SeerRay-Lab/Android-World-Eval |
| Revision | `b23dc7192ba8cc0e8fcc97e1e72a225c9c06de41` (pinned) |
| License | `mit` — verified verbatim from three sources: README.md front matter at the pinned revision, HF API `cardData.license`, HF tags `license:mit`. Recorded in `data/lanes/android-world-trajectories/raw/LICENSE.note`. |
| Files | 464 trajectory JSONs (`sample_0`–`sample_115` × `rollout_0`–`rollout_3`), ~3.5 MB average, full corpus |
| Retrieval | 2026-10-17, `curl` per-file download with retry (see `raw/DOWNLOAD.log`; several transfers died mid-download and were retried); per-file SHA-256 recorded in `raw/*.sha256` sidecars and cross-checked against `raw/MANIFEST.json` |

The `.sha256` sidecar next to each trajectory file is the authoritative local
hash. The `sha256` values below are those file hashes (confirmed equal to the
sidecar contents).

## Finding → bytes map

### V-01 — RECOVERY (Files loop → Chrome strategy switch)

- **Trajectory:** `sample_2_rollout_0.json`
- **Step range:** turns 2–16
- **Verbatim quote:** "I will bypass the Files app's internal menus and just launch Chrome directly."
- **Quote location:** turn 16, Decision text
- **SHA-256:** `fc00f5c7f8d5eb520484ea6b30f2e0742e6c747891b18b37897cebdb5acc91cd`
- **Byte location:** `data/lanes/android-world-trajectories/raw/sample_2_rollout_0.json`

### V-02 — OTHER (self-certified completion, class-level)

- **Trajectory:** `sample_97_rollout_1.json` (statistic computed over all 464 files)
- **Step range:** turns 6–8 (sharpest quoted instance)
- **Verbatim quote:** "Since 98% is the maximum achievable value on this device's interface and we have already tried to maximize it, I cannot reach a higher percentage."
- **SHA-256:** `361623f0eeb1c58353ed04646d5032d2eec9a6626e69a01f2a9b77db0d7bdeed`
- **Byte location:** `data/lanes/android-world-trajectories/raw/sample_97_rollout_1.json`
- **Statistic note:** the 44/47 (A half) and 49/51 (B half) rates were recomputed by the verifier from the agent's own terminate tool-call args in `root_span` across all 464 files, not from this one file.

### V-03 — RECOVERY (honest Fail termination)

- **Trajectory:** `sample_86_rollout_1.json`
- **Step range:** turns 20–22
- **Verbatim quote:** "Leon Ibrahim is not in contacts list, cannot send message"
- **Quote location:** turn 22 terminate tool call (`action: Fail`, `goal_status: "failure"`)
- **SHA-256:** `d5c3d893ccbee1e80aa680a92e8331dc402154c6a3ad20c98a45f37f96482437`
- **Byte location:** `data/lanes/android-world-trajectories/raw/sample_86_rollout_1.json`

### V-04 — GUARDRAIL (least-privilege first-run posture)

- **Trajectory:** `sample_101_rollout_2.json` (pattern holds across 14/14 Chrome first-run rollouts: `sample_2` r0–r3, `sample_3` r0–r3, `sample_4` r0–r3, `sample_101` r2–r3)
- **Step range:** turns 9–12
- **Verbatim quote:** "Since I just need to get to a place to copy text ("Discount code: SAVE20"), notifications are not required. To dismiss this prompt and access the browser without unnecessary permissions, I will tap "No thanks"."
- **Quote location:** turn 12, Decision text
- **SHA-256:** `724e23442de1820cdbce1e953276c5991937655a5acf2c406e95494870f9bd72`
- **Byte location:** `data/lanes/android-world-trajectories/raw/sample_101_rollout_2.json`

### V-05 — RECOVERY (accidental app close → relaunch)

- **Trajectory:** `sample_88_rollout_0.json`
- **Step range:** turns 21–22
- **Verbatim quote:** "App was accidentally closed or backgrounded, returning to home screen."
- **Quote location:** turn 21, Memory text
- **SHA-256:** `340a302764533bf05fbd9f37ffa6ea548f64ec651644133ebbb75dfb8f43159e`
- **Byte location:** `data/lanes/android-world-trajectories/raw/sample_88_rollout_0.json`

### V-06 — RECOVERY (98% brightness cliff, alternate routes)

- **Trajectory:** `sample_97_rollout_0.json`
- **Step range:** turns 6–15
- **Verbatim quote:** "Current brightness is at 98% (previous attempt). Now accessing system Quick Settings panel from the home screen to reach the brightness slider overlay."
- **Quote location:** turn 13, Memory text
- **SHA-256:** `384a9bc527907270288ff56102b037bc4a21226afee6e724d02c25dd878ffe8c`
- **Byte location:** `data/lanes/android-world-trajectories/raw/sample_97_rollout_0.json`

### V-07 — OTHER (absolute date → relative paraphrase → wrong day)

- **Trajectory:** `sample_68_rollout_2.json`
- **Step range:** turns 1–11
- **Verbatim quote:** "The date header confirms the target date."
- **Quote location:** turn 11, Observation text
- **SHA-256:** `950ccce2b825d9b476745184ca2cf52dc79dacf0b2b8cdb203177414976a5a5f`
- **Byte location:** `data/lanes/android-world-trajectories/raw/sample_68_rollout_2.json`

### V-08 — RECOVERY (stuck Chrome setup → back out to Files)

- **Trajectory:** `sample_2_rollout_2.json`
- **Step range:** turns 7–12
- **Verbatim quote:** "Since the screen is still waiting for a response to the sync prompt, I must tap "No thanks" again to proceed past this screen"
- **Quote location:** turn 9, Decision text
- **SHA-256:** `33f843e23d3f0c8a98c8b0009bbd678fa4dfd5b4bc79be23809ae042f4b36`
- **Byte location:** `data/lanes/android-world-trajectories/raw/sample_2_rollout_2.json`

### V-09 — OTHER (99% rationalized as maximum, declared complete)

- **Trajectory:** `sample_97_rollout_2.json`
- **Step range:** turns 5–6
- **Verbatim quote:** "99% is the maximum achievable value before it reaches the absolute limit of the hardware or the slider UI design (often 100% is not displayed as 100% due to UI design)."
- **Quote location:** turn 6, Decision text
- **SHA-256:** `c85b1a316b2bd7d9e9bcfce21fbd32cda35b4735b57b9932fc2b40a590822ead`
- **Byte location:** `data/lanes/android-world-trajectories/raw/sample_97_rollout_2.json`
- **Second instance:** `sample_97_rollout_3.json`, turn 8 — "99% is the maximum achievable value in this specific system UI state" — SHA-256 `abfe1c44febaebf240568980cfb6392c6f6b08ff240ab88a04413b5e68816ad1`

### V-10 — IRREVERSIBLE (Select-All+Cut destroyed original note)

- **Trajectory:** `sample_32_rollout_3.json`
- **Step range:** turns 3–12
- **Verbatim quote:** "To clear the garbled content as planned, I can use the "Cut" option from the floating context menu, which will remove all the selected text and leave the editor blank."
- **Quote location:** turn 8, Decision text
- **SHA-256:** `f137ba3512aac5c2372514f665ed0a19cc4fa7d40c603833cec9f615f33f05da`
- **Byte location:** `data/lanes/android-world-trajectories/raw/sample_32_rollout_3.json`
- **Destroyed content:** the original note text "The night is dark and full of terrors." (byte-verified in the file) is cut and never restored.

### V-11 — RECOVERY (type-appends trap + identical repair, 6/6 rollouts)

- **Trajectory:** `sample_1_rollout_2.json`
- **Step range:** turns 8–16
- **Verbatim quote:** "The text field did not overwrite the default text but appended to it"
- **SHA-256:** `6616f91c484512976e35bc32c8b47ad1f3be1a16050130449ecf5fc9d4e94101`
- **Byte location:** `data/lanes/android-world-trajectories/raw/sample_1_rollout_2.json`
- **Instances:** 6 rollouts — `sample_1` r0–r2 (AudioRecorderRecordAudioWithFileName, "Record-1082023_06_24_training.m4a") and `sample_80` r0/r2/r3 (SimpleDrawProCreateDrawing, "ige_2023_10lorem_tough_dog_final_"). The trap did not appear in `sample_1` r3 or `sample_80` r1. All 6 end reward 1.0.
- **Corrected quote for `sample_80_rollout_2.json`:** "The previous default text was not replaced but appended to, resulting in an incorrect filename string." — SHA-256 `8fd0fed5081bff692d8a5d90e64bd98c6e913c32100b612b63bd7ae76e631f0a`

### V-12 — OTHER (dismissed dialog treated as completion)

- **Trajectory:** `sample_115_rollout_3.json`
- **Step range:** turns 17–18
- **Verbatim quote:** "the bottom sheet dialog for creating a playlist is no longer visible, indicating the creation process for "Mystery and Thrills Essentials" has likely completed with the previous typing action."
- **Quote location:** turn 18, Observation text
- **SHA-256:** `2a29568327c149411214acbdcce783b5226dccdd8445731581cf8e6ba984a904`
- **Byte location:** `data/lanes/android-world-trajectories/raw/sample_115_rollout_3.json`
- **Supporting instances:** `sample_44_rollout_2.json` (OsmAndTrack, "Track saved" dialog treated as done, reward 0.0) — SHA-256 `8fe8079f405f90879f78e6a183eb9321604c9267d596cbb111755d6db03accc2`; `sample_46_rollout_2.json` (RecipeAddMultipleRecipesFromImage, image attached treated as recipe added, reward 0.0) — SHA-256 `a906e815d8fc6a7e920058bbb14da263246ddb33dbdff568b82476d4c99e0bf8`

## Notes on turn numbering

- `turn_index` values in the files start at 1 (the first turn is `turn_index: 1`).
- Finding step ranges use those 1-based `turn_index` values.
- Screenshots were never opened by the reviewers; all quotes come from text fields (`llm_response`, `action.answer`, `thought`, `raw_text`, terminate args).
