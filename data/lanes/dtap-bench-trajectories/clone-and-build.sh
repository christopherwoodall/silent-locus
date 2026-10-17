#!/bin/bash
# DTap-Bench ingest pipeline — durable and restart-safe.
# Stages: recon-done -> cloning -> clone-done -> mirror-built -> complete
# Re-running this script resumes from PIPELINE-STATE.json.
# Deviation from brief (documented): per-file curl measured ~9s/file
# (307->resolve-cache redirect chain through egress proxy); 133,726 files
# single-threaded would take ~14 days. Using `git clone --depth 1`
# (single TCP stream, polite, no 429 risk) at the pinned rev, then
# building raw/ from the clone with per-file sha256 + provenance.
set -u
LANE="$HOME/workspace/silent-locus/data/lanes/dtap-bench-trajectories"
STAGE="$HOME/workspace/dtap-clone-staging"
RAW="$LANE/raw"
STATE="$LANE/PIPELINE-STATE.json"
REV="836caf2fdd78b888ddd14fb62dc038e932e17898"
REPO="https://huggingface.co/datasets/AI-Secure/DTap-Bench-Agent-Trajectories"

set_state() { python3 -c "
import json
s = {'stage': '$1', 'rev': '$REV'}
try: s.update({k:v for k,v in json.load(open('$STATE')).items() if k!='stage'})
except Exception: pass
json.dump(s, open('$STATE','w'), indent=2)
"; echo "STATE -> $1"; }
log() { echo "[$(date -u +%FT%TZ)] $*"; }

[ -f "$STATE" ] || set_state "recon-done"
CUR=$(python3 -c "import json; print(json.load(open('$STATE'))['stage'])")
log "resuming at stage: $CUR"

if [ "$CUR" = "complete" ]; then log "already complete"; exit 0; fi

# ---- clone ----
NEED_CLONE=1
if [ -d "$STAGE/.git" ]; then
  HEAD=$(git -C "$STAGE" rev-parse HEAD 2>/dev/null || echo "none")
  NF=$(find "$STAGE" -type f -not -path "*/.git/*" 2>/dev/null | wc -l)
  log "existing staging: HEAD=$HEAD files=$NF"
  if [ "$HEAD" = "$REV" ] && [ "$NF" -gt 130000 ]; then NEED_CLONE=0; log "staging clone OK, skipping clone"; fi
fi
if [ "$NEED_CLONE" = "1" ]; then
  set_state "cloning"
  rm -rf "$STAGE"
  ATT=0
  while [ $ATT -lt 6 ]; do
    ATT=$((ATT+1)); log "clone attempt $ATT"
    if timeout 3600 git -c http.lowSpeedLimit=1000 -c http.lowSpeedTime=600 \
        clone --depth 1 "$REPO" "$STAGE" >>"$LANE/clone.log" 2>&1; then break; fi
    log "clone attempt $ATT failed (rc=$?)"; sleep 45; rm -rf "$STAGE"
  done
  HEAD=$(git -C "$STAGE" rev-parse HEAD 2>/dev/null || echo "none")
  [ "$HEAD" = "$REV" ] || { log "FATAL: HEAD $HEAD != $REV"; exit 1; }
  log "clone OK at $REV"
fi
set_state "clone-done"

# ---- mirror build ----
log "rsync staging -> raw (exclude .git, *.png)"
rsync -a --exclude='.git' --exclude='*.png' "$STAGE/" "$RAW/"
log "generating sidecars + manifest"
ACQ=$(date -u +%FT%TZ)
python3 - "$STAGE" "$RAW" "$REV" "$REPO" "$ACQ" <<'PYEOF'
import os, sys, json, hashlib
stage, raw, rev, repo_url, acq = sys.argv[1:6]
files = []; total_bytes = 0
skip = {'LICENSE.note','MANIFEST.json','SCRAPE-PROGRESS.json','SOURCE-FILELIST.json',
        'CORPUS-INVENTORY.md','PIPELINE-STATE.json','clone.log','rsync-done.marker','clone-and-build.sh'}
n = 0
for root, dirs, fns in os.walk(raw):
    for fn in fns:
        if fn.endswith('.PROVENANCE.txt') or fn.endswith('.sha256'): continue
        rel = os.path.relpath(os.path.join(root, fn), raw)
        if rel in skip or rel.startswith('raw/'): continue
        full = os.path.join(root, fn)
        h = hashlib.sha256(); size = 0
        with open(full,'rb') as f:
            for chunk in iter(lambda: f.read(1<<20), b''):
                h.update(chunk); size += len(chunk)
        digest = h.hexdigest(); total_bytes += size
        with open(full + '.sha256','w') as f: f.write(f"{digest}  {rel}\n")
        with open(full + '.PROVENANCE.txt','w') as f:
            f.write(f"source_url: {repo_url}/resolve/{rev}/{rel}\n")
            f.write(f"retrieved_utc: {acq}\n")
            f.write("method: git clone --depth 1 (single stream) + selective copy; per-file curl abandoned after throughput test (~9s/file for 133726 files)\n")
            f.write(f"dataset_rev: {rev}\nlicense: apache-2.0\n")
        files.append({'path': rel, 'size': size, 'sha256': digest})
        n += 1
        if n % 20000 == 0: print(f"  ... {n}", flush=True)
files.sort(key=lambda x: x['path'])
pngs = []
for root, dirs, fns in os.walk(stage):
    if '.git' in root.split(os.sep): continue
    for fn in fns:
        if fn.endswith('.png'): pngs.append(os.path.relpath(os.path.join(root, fn), stage))
pngs.sort()
manifest = {'dataset': 'AI-Secure/DTap-Bench-Agent-Trajectories', 'dataset_rev': rev,
    'license': 'apache-2.0', 'acquired_utc': acq,
    'acquisition_method': 'git clone --depth 1 + selective copy (see per-file PROVENANCE)',
    'total_files': n, 'total_bytes': total_bytes,
    'media_skipped': {'count': len(pngs), 'paths': pngs},
    'complete': True, 'files': files}
with open(os.path.join(raw,'MANIFEST.json'),'w') as f: json.dump(manifest, f)
with open(os.path.join(raw,'SCRAPE-PROGRESS.json'),'w') as f:
    json.dump({'dataset_rev': rev, 'files_done': n, 'files_total': n,
               'bytes_done': total_bytes, 'bytes_total': total_bytes,
               'complete': True, 'updated_utc': acq}, f, indent=2)
print(f"files: {n}, bytes: {total_bytes}, pngs skipped: {len(pngs)}")
PYEOF
set_state "mirror-built"

# ---- verify + cleanup staging ----
MF_N=$(python3 -c "import json; print(json.load(open('$RAW/MANIFEST.json'))['total_files'])")
log "manifest files: $MF_N"
if [ "$MF_N" -gt 130000 ]; then
  log "removing staging dir to reclaim disk"
  rm -rf "$STAGE"
  set_state "complete"
  log "PIPELINE COMPLETE"
else
  log "FATAL: manifest file count too low ($MF_N)"; exit 1
fi
