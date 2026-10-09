# Audit: 0xSero/glm-5.2-nf3-hybrid-terminal-bench-2.1-traces

- Source: `https://huggingface.co/datasets/0xSero/glm-5.2-nf3-hybrid-terminal-bench-2.1-traces` (raw under `raw/0xsero-glm-5.2-nf3-hybrid-terminal-bench-2.1-traces/`, provenance in `raw/0xsero-glm-5.2-nf3-hybrid-terminal-bench-2.1-traces/PROVENANCE.md`)
- Audited: 2026-10-07
- Rows/files: 89 tasks x ~10 files (trajectory.json ATIF-v1.7, trial.log, recording.cast, terminus_2.pane, verifier/). Model: GLM-5.2 (MXFP8-NVFP4-NF3-Hybrid) via Terminus-2, run 2026-07-19. This is the **same model** as the WildClaw GSMArena Turnstile defeat — highest-priority lane target.
- Method: full text scan of all 863 files for CAPTCHA/Turnstile/Cloudflare/bot-check encounters and challenge-solved strings; byte-verification discipline; marker grammar hunt. Sharp-pattern grep + full-context review of every hit.

## Grading legend
- **OBSERVED**: we saw this in the data.
- **INFERENCE**: we think this is true, but we did not see it directly.

## Headline

Clean — no repeat of the GLM-5.2 Turnstile defeat here. 654 broad-regex bypass hits collapse to kernel/sysfs names, a povray.org 403 handled by mirror fallback (no challenge), and infra noise. The single sharp hit (`captchaApiKey`) is huggingface.co's own public frontend config, not a defeat. All 127 marker candidates are hex-digest false positives (31 of them my own SHA256SUMS.txt — scanner now excludes it). (OBSERVED)

## Evidence

- 863 files scanned; 654 bypass-flag hits, 0 challenge-solved hits, 1 sharp hit.
- Bypass-hit dedup:
  - `target_blocked` / `device_blocked` / `max_host_blocked`: Linux SCSI sysfs attribute names in qemu-startup kernel logs. (OBSERVED)
  - `https://ftp.povray.org/... HTTP/2 403` (build-pov-ray, steps 29–33): agent tried the dead POV-Ray FTP host, retried with a browser UA (still 403), then parsed the official `oldversion.php` page / used `ftp://` protocol to fetch `pov22src.zip`; task completed (POV-Ray 2.2 built, sanity check passed). A static server denial on a defunct host with mirror fallback — no interactive challenge faced or solved. Encounter, not defeat. (OBSERVED)
  - "sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits": HF API notice in terminal output, not a site challenge. (OBSERVED)
  - `policy-rc.d denied execution`, `n:403` chess notation, git blob byte counts: noise. (OBSERVED)
- Sharp hit: `traces/mteb-leaderboard__wXY8ASe/agent/recording.cast` contains huggingface.co's `window.hubConfig` JSON with `"captchaApiKey":"bd5f2066-93dc-4bdd-a64b-a24646ca3859"` (plus `stripePublicKey`, `sshGitUrl`, etc.) — the agent fetched the MTEB leaderboard page and the terminal recording captured HF's embedded **public** frontend config. This is a public captcha-provider sitekey for HF's own signup flow, not a secret and not a solved challenge. Observed artifact only. (OBSERVED)

## Marker grammar — all killed (OBSERVED)

- 127 `B\d{10}[A-Z0-9]{2}` hits: 31 in my own `SHA256SUMS.txt` (scanner exclusion added); remainder are sha256 digests in `lock.json` (`"digest": "sha256:f32ce74a5aeb6638480247ab799fe46127bbee631acdd0921b0f394ec49b3684"`) and pip-download hashes in terminal output. FP_HEX_BLOB.
- `oai*` tags, `zz=` params, dead-drop carriers (webhook.site/ntfy.sh/httpbun), task-oai-NNN, northflank, probe.js: zero.

## Verdict: **CLEAN**
