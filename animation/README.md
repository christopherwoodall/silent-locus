# animation — render projects

Vertical-format video renders (dark chibi style, vertical cut first) built
with resumable render pipelines.

## Subdirs

| Dir | Contents |
|---|---|
| `un-heist-that-wasnt/` | "The UN Heist That Wasn't" — narrated vertical TTP explainer on the UNCTAD incident. Render complete (`un-heist-v1-vertical.mp4`); verify PASS |
| `gem-graveyard/` | Second render project: narration scripts (`build/narration_script*.txt`), render/audio/synth scripts (`build/`), working frames (`work/`) |
| `build/` | Top-level build scratch (`__pycache__`) |
| `work/` | Top-level render working state (`render.log`, `render.lock`, `pipeline_done`) |

## Layout convention (per project)

- `build/` — render + encode scripts (`render_*.py`, `encode.sh`, `verify.py`, `resume_render.sh`)
- `work/` — intermediate frames (`frames_v/`), progress and verify JSON, logs
- Final `.mp4` lands at the project root; nothing upstream of verification is
  treated as deliverable.
