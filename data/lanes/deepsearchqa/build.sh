#!/usr/bin/env bash
# DeepSearchQA collection build script (2026-10-01-deepsearchqa)
# Reproducible pull of the DeepSearchQA question set used for the Transluce
# us-canada-gov task-family JOIN KEY map (lanes 2/4).
#
# Pins the exact HF revision; regenerates questions.jsonl (dsqa_NNN ids) from
# the upstream CSV. Per the 2026-09-29 convention, this single-collection
# build script lives IN the event dir.
#
# Prereqs: python3, huggingface_hub[cli] (pip install --user "huggingface_hub[cli]")
# Note: bundled httpx2 chokes on bracketed IPv6 entries in no_proxy — strip them.
set -euo pipefail
cd "$(dirname "$0")"

REPO="google/deepsearchqa"
REV="b2623f8653065c2672de6d941fc5434cd652376c"
HF_BIN="${HOME}/.local/bin/hf"

export NO_PROXY="localhost,127.0.0.1"
export no_proxy="localhost,127.0.0.1"

echo "== downloading ${REPO}@${REV} =="
"$HF_BIN" download "$REPO" --repo-type dataset --revision "$REV" --local-dir ./hf_raw

echo "== building questions.jsonl =="
python3 - <<'EOF'
import csv, json
with open('hf_raw/DSQA-full.csv', newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
with open('questions.jsonl', 'w', encoding='utf-8') as f:
    for i, r in enumerate(rows):
        f.write(json.dumps({
            "id": f"dsqa_{i}",          # 0-based row index; verified: row 250 == dsqa_250
            "problem": r['problem'],
            "category": r['problem_category'],
            "answer": r['answer'],
            "answer_type": r['answer_type'],
        }, ensure_ascii=False) + "\n")
print("questions:", len(rows))
EOF

echo "== done =="
