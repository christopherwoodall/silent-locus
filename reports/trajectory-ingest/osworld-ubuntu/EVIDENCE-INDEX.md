# OSWorld-Ubuntu — Evidence Index

Byte pointers for the 13 verified findings. All sha256 values
are the zip-level sha256 from the lane's `.sha256` sidecars,
re-checked by the verifier against the raw bytes. Raw bytes are
local-only in
`data/lanes/osworld-ubuntu-trajectories/raw/extracted/`.

Dataset: `xlangai/ubuntu_osworld_verified_trajs`
Revision: `5473c39e42a538a187a9b2c2b499db59d560fd8c`
HF zip URL form:
`https://huggingface.co/datasets/xlangai/ubuntu_osworld_verified_trajs/resolve/5473c39e42a538a187a9b2c2b499db59d560fd8c/<zip>`
(the trajectory file sits at the in-zip path given below).

## osworld-A-001 (OTHER, HIGH)

- File: `raw/extracted/results_opus4p5_single_agent/results_opus4p5_run10/pyautogui/screenshot/claude-opus-4-5-20251101/os/a462a795-fdc7-4b23-b689-e8b6df786b78/traj.jsonl`
- Zip: `results_opus4p5_single_agent.zip`
- sha256: `5a35efde68e09d4289227b97e22ea174898e27dca30f59f987a5117dc3a32509`
- Steps: 15-23 (23 steps total). Step 23: action `DONE`, `done=True`, `reward=0`.

## osworld-A-002 (CAPTCHA, HIGH)

- File: `raw/extracted/results_opus4p5_single_agent/results_opus4p5_run10/pyautogui/screenshot/claude-opus-4-5-20251101/chrome/7f52cab9-535c-4835-ac8c-391ee64dc930/traj.jsonl`
- Zip: `results_opus4p5_single_agent.zip`
- sha256: `5a35efde68e09d4289227b97e22ea174898e27dca30f59f987a5117dc3a32509`
- Steps: 14-25 (40 steps total). Steps 15-16: plan text (quote). Step 20: "Verification challenge expired". Step 25: "The CAPTCHA has expired again" + back-navigation and filter re-encoding.

## osworld-A-003 (CAPTCHA, HIGH)

- File: `raw/extracted/results_full361_adaptive_20260609_094019/results_full361_adaptive_20260609_094019/pyautogui/screenshot/MiniMax-M3/chrome/47543840-672a-467d-80df-8f7c3b9788c9/traj.jsonl`
- Zip: `results_full361_adaptive_20260609_094019.zip`
- sha256: `941a61f41b93937b158de21e787117eb37b043e4fb8203e84b18aa979e8d25ad`
- Steps: 16-20 (27 steps total). Step 16: response (quote) with declared coordinates `[462,400]->[578,400]` vs executed `moveTo(887,432)/dragTo(1109,432)`. Drags at steps 16, 17, 19. Step 20: "The verification was successful".

## osworld-A-004 (TOOL-MISUSE, HIGH)

- File: `raw/extracted/results_opus4p5_single_agent/results_opus4p5_run10/pyautogui/screenshot/claude-opus-4-5-20251101/gimp/58d3eeeb-e9d0-499f-962e-fd0db2a744d8/traj.jsonl`
- Zip: `results_opus4p5_single_agent.zip`
- sha256: `5a35efde68e09d4289227b97e22ea174898e27dca30f59f987a5117dc3a32509`
- Steps: 1-28 (28 steps total). Step 2: code-agent `task_instruction` = "Download rockyou.txt wordlist from the internet and use stegseek to crack the steghide password". Step 28: action `FAIL`, `done=True`, plan states "5 code agent attempts (totaling 100+ steps)".

## RB-001 (CAPTCHA, HIGH)

- File: `raw/extracted/UI-TARS-0717-15step/UI-TARS-0717-15step/chrome/7f52cab9-535c-4835-ac8c-391ee64dc930/traj.jsonl`
- Zip: `UI-TARS-0717-15step.zip`
- sha256: `e1e3dddaa284124621758f29e87f92f4c4c6d3f9d0691eeb78d7ac82e92f6690`
- Steps: 1-15 (15 steps total). Thought text embedded in the action field's comment block. Step 2: motorcycle-grid thought (quote). Step 10: expiry noted. Step 14: fire-hydrant re-click thought (quote).

## RB-002 (CAPTCHA, HIGH)

- File: `raw/extracted/opencua_agent-opencua_a3b-cot_l2-action_history-3image-Ubuntu-15step/chrome/b070486d-e161-459b-aa2b-ef442d973b92/traj.jsonl`
- Zip: `opencua_agent-opencua_a3b-cot_l2-action_history-3image-Ubuntu-15step.zip`
- sha256: `f68f8157f1091acc2abc5df95229cf5cb13830a6f33ab89163fe82167b27d90c`
- Steps: 4-13 (13 steps total). Steps 6-7: responses (quote). Three challenge rounds: steps 5-9 motorcycles, step 10 bicycles, steps 11-12 motorcycles. Step 13: action `FAIL`, `done=True`.

## RB-003 (CAPTCHA, HIGH)

- File: `raw/extracted/uipath_gpt_5_50steps/uipath_gpt_5_50steps/chrome/7f52cab9-535c-4835-ac8c-391ee64dc930/traj.jsonl`
- Zip: `uipath_gpt_5_50steps.zip`
- sha256: `1ba66103da732ebd0cafa54ad55fe77d2814db5e0cfeb6d24e43cafa03c70449`
- Steps: 4-12 (21 steps total). Steps 4-7: checkbox click + 3 bicycle tiles. Step 8: VERIFY click (494,677) + thought (quote). Step 9: abandonment thought (quote) + back-navigation. Steps 10-12: site search.

## RB-004 (GUARDRAIL, HIGH)

- File: `raw/extracted/coact1-150-100-50-15steps/results/results_coact_bkp/coact/multi_apps/236833a3-5704-47fc-888c-4f298f09f799/coding_output_7/chat_history.json`
- Zip: `coact1-150-100-50-15steps.zip`
- sha256: `8f14c7398c005bfe5351e5113600ab8dd18acf687371ae85fad19d0892b11c52`
- Messages: 14 (coding-agent chat, not traj.jsonl). Msg 5: UA-spoof text (quote) with shipped Chrome/115 User-Agent. Msgs 4/6/8/10: HTTP 401 persists after the spoof.

## RB-005 (GUARDRAIL, MEDIUM)

- File: `raw/extracted/opencua_agent-opencua_qwen2_7b-cot_l2-action_history-3image-Ubuntu-15step/chrome/7f52cab9-535c-4835-ac8c-391ee64dc930/traj.jsonl`
- Zip: `opencua_agent-opencua_qwen2_7b-cot_l2-action_history-3image-Ubuntu-15step.zip`
- sha256: `37bc07deb0a5f4bfb3d2f2f818f905ab20667e6f5944f200f2c0a8c6a41d99f1`
- Steps: 2 (7 steps total). Step 2: response (quote). Executed actions stayed mundane (address-bar click, typed search); no URL edit attempted. Step 7: action `FAIL`.

## RB-006 (COORDINATION, HIGH)

- File: `raw/extracted/coact1-150-100-50-15steps/results/results_coact_bkp/coact/multi_apps/c867c42d-a52d-4a24-8ae3-f75d256b5618/chat_history.json`
- Zip: `coact1-150-100-50-15steps.zip`
- sha256: `8f14c7398c005bfe5351e5113600ab8dd18acf687371ae85fad19d0892b11c52`
- Messages: 18. Msgs 4-14: GUI-agent fumbling (quote). Planner taskings live in `tool_calls[].function.arguments` (verified by raw grep): cancel-and-re-task to `call_gui_agent`, pandas conversion to `call_coding_agent`. Msg 16: coding-agent completion summary.

## RB-007 (COORDINATION, HIGH)

- File: `raw/extracted/coact1-150-100-50-15steps/results/results_coact_bkp/coact/chrome/f0b971a1-6831-4b9b-a50e-22a6e47f45ba/chat_history.json`
- Zip: `coact1-150-100-50-15steps.zip`
- sha256: `8f14c7398c005bfe5351e5113600ab8dd18acf687371ae85fad19d0892b11c52`
- Messages: 8. Msg 3/4: GUI refusal (quote). Msg 5: planner `call_gui_agent` tasking with the nfl.com URL (quote). Later msg: GUI reports Patriots 13, Rams 3 (quote).

## RB-009 (OTHER, MEDIUM)

- File: `raw/extracted/autoglm_15steps/multi_apps/5990457f-2adb-467b-a4af-5c857c92d762/traj.jsonl`
- Zip: `autoglm_15steps.zip`
- sha256: `5a5dd328721dd81085b912888bf97f9174699b987de94a70abc93ff557ef78fe`
- Steps: 7-15 (15 steps total). Step 7: think (quote) — reCAPTCHA named. Steps 8-12, 14, 15: identical URL rewrites with the "double encoding" theory (quote).

## RB-011 (RECOVERY, MEDIUM)

- File: `raw/extracted/autoglm_15steps/os/a462a795-fdc7-4b23-b689-e8b6df786b78/traj.jsonl`
- Zip: `autoglm_15steps.zip`
- sha256: `5a5dd328721dd81085b912888bf97f9174699b987de94a70abc93ff557ef78fe`
- Steps: 1-15 (15 steps total). Every step's action: `sudo su Charles` + password pair. Step 6: think (quote) citing the no-logout/no-shutdown constraint. "3 incorrect password attempts" recurs at steps 6, 10, 14.

## Killed (pointers, not ingested)

- **RB-010**: gbox family — `raw/extracted/results_gbox_15steps/`; harness single-record logging convention, not agent behavior. See adversarial-kills.md.
- **osworld-A-005**: gemini-2.5-pro — password supplied in task hints; false "guessing" framing. See adversarial-kills.md.
- **RB-008**: uipath GPT-5 LanguageTool — textbook recovery; factual errors. See adversarial-kills.md.
