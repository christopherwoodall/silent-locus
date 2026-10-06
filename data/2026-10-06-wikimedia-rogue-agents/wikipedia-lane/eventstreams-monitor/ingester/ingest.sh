#!/usr/bin/env bash
# =============================================================================
# ingest.sh — EventStreams SSE ingestion entry point (OFFLINE BUILD)
#
# HARD RULE (user): BUILD ONLY. This script is never to be run against the
# live stream as part of the build, and must never be wired to cron/systemd
# during development. It is committed unexecuted.
#
# TRANSPORT CONSTRAINT (this VM): Python HTTP stacks break on the egress
# proxy; curl works. The persistent SSE connection is OWNED BY CURL ONLY:
#
#     curl -N -s <stream-url> | python3 process.py ...
#
# Python never touches the network — it reads stdin lines. If curl is ever
# replaced, replace it with another non-Python transport (e.g. `wget -qO-`,
# `socat`), never with a Python HTTP client.
#
# Layout: raw events land in <out_dir>/raw/YYYY-MM-DD/HH.jsonl (UTC hours).
# Diagnostics (backoff, heartbeats, shutdown) go to stderr.
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG="${CONFIG:-$SCRIPT_DIR/config.yaml}"

# ---------------------------------------------------------------------------
# Config loading: a single python call validates the YAML and emits
# shell-quoted assignments. Values are quoted with shlex.quote so `eval` is
# safe for our own config file; a hostile config is not our threat model.
# ---------------------------------------------------------------------------
load_config() {
  python3 - "$CONFIG" <<'PYEOF'
import sys, shlex, yaml

cfg_path = sys.argv[1]
try:
    with open(cfg_path, encoding='utf-8') as f:
        cfg = yaml.safe_load(f) or {}
except FileNotFoundError:
    print('error: config file not found: %s' % cfg_path, file=sys.stderr)
    sys.exit(2)
except yaml.YAMLError as e:
    print('error: config YAML invalid: %s' % e, file=sys.stderr)
    sys.exit(2)

def get(key, default=None):
    v = cfg.get(key, default)
    return v if v is not None else default

stream      = get('stream') or {}
backoff     = get('backoff') or {}
rotation    = get('rotation') or {}

out = {
    'ES_STREAM_URL':      stream.get('url', 'https://stream.wikimedia.org/v2/stream/recentchange'),
    'ES_WIKIS':           ','.join(stream.get('wikis') or []),
    'ES_TITLE_REGEX':     stream.get('title_regex') or '',
    'ES_OUT_DIR':         get('out_dir', '.'),
    'ES_HEARTBEAT_N':     str(get('heartbeat_events', 1000)),
    'ES_BACKOFF_INIT':    str(backoff.get('initial_s', 2)),
    'ES_BACKOFF_MAX':     str(backoff.get('max_s', 300)),
    'ES_BACKOFF_FACTOR':  str(backoff.get('factor', 2)),
    'ES_CONNECT_TIMEOUT': str(get('connect_timeout_s', 15)),
    'ES_CURL_EXTRA':      ' '.join(get('curl_extra_args') or []),
}
for k, v in out.items():
    print('%s=%s' % (k, shlex.quote(str(v))))
PYEOF
}

# ---------------------------------------------------------------------------
# --dry-run: validate config, print the resolved plan, connect to NOTHING.
# ---------------------------------------------------------------------------
dry_run() {
  echo "== ingest.sh --dry-run: validating config =="
  eval "$(load_config)"
  echo "config file:      $CONFIG"
  echo "stream URL:       $ES_STREAM_URL"
  echo "wiki filter:      ${ES_WIKIS:-(none — all wikis)}"
  echo "title regex:      ${ES_TITLE_REGEX:-(none — all titles)}"
  echo "out dir:          $ES_OUT_DIR  (writes \$OUT_DIR/raw/YYYY-MM-DD/HH.jsonl, UTC)"
  echo "heartbeat:        every $ES_HEARTBEAT_N events (stderr)"
  echo "backoff:          ${ES_BACKOFF_INIT}s * ${ES_BACKOFF_FACTOR} up to ${ES_BACKOFF_MAX}s"
  echo "connect timeout:  ${ES_CONNECT_TIMEOUT}s"
  echo "curl extra args:  ${ES_CURL_EXTRA:-(none)}"
  echo ""
  echo "resolved pipeline:"
  echo "  curl -N -s -S --no-buffer --connect-timeout $ES_CONNECT_TIMEOUT $ES_CURL_EXTRA \"$ES_STREAM_URL\" \\"
  echo "    | python3 \"$SCRIPT_DIR/process.py\" --out-dir \"$ES_OUT_DIR\" \\"
  echo "        ${ES_WIKIS:+--wikis \"$ES_WIKIS\" }${ES_TITLE_REGEX:+--title-regex \"$ES_TITLE_REGEX\" }--heartbeat $ES_HEARTBEAT_N"
  echo ""
  echo "dry-run OK: config valid, no network touched."
}

if [[ "${1:-}" == "--dry-run" ]]; then
  dry_run
  exit 0
fi

# ---------------------------------------------------------------------------
# Live mode (operator-invoked only — never during the build).
# ---------------------------------------------------------------------------
eval "$(load_config)"

# ---------------------------------------------------------------------------
# Graceful shutdown: on SIGTERM/SIGINT, stop curl; the processor sees EOF on
# stdin, flushes and closes the current hour file via its finally block, then
# we wait for it and exit. Children are tracked so nothing is orphaned.
# ---------------------------------------------------------------------------
CURL_PID=""
PROC_PID=""
SHUTTING_DOWN=0

log() { echo "[ingest] $*" >&2; }

shutdown() {
  [[ $SHUTTING_DOWN -eq 1 ]] && return
  SHUTTING_DOWN=1
  log "signal received — draining stream, flushing current hour file..."
  [[ -n "$CURL_PID" ]] && kill "$CURL_PID" 2>/dev/null || true
  # Do NOT kill the processor: let it consume curl's EOF, close the file.
  [[ -n "$PROC_PID" ]] && wait "$PROC_PID" 2>/dev/null || true
  log "shutdown complete"
  exit 0
}
trap shutdown TERM INT

# ---------------------------------------------------------------------------
# Retry/backoff loop around the curl|processor pipeline.
# ---------------------------------------------------------------------------
sleep_s="$ES_BACKOFF_INIT"

while true; do
  log "connecting to $ES_STREAM_URL"
  # shellcheck disable=SC2086  # ES_CURL_EXTRA is intentionally word-split
  curl -N -s -S --no-buffer --connect-timeout "$ES_CONNECT_TIMEOUT" \
    $ES_CURL_EXTRA "$ES_STREAM_URL" \
    | python3 "$SCRIPT_DIR/process.py" \
        --out-dir "$ES_OUT_DIR" \
        ${ES_WIKIS:+--wikis "$ES_WIKIS"} \
        ${ES_TITLE_REGEX:+--title-regex "$ES_TITLE_REGEX"} \
        --heartbeat "$ES_HEARTBEAT_N" &
  PIPE_PID=$!

  # Track both halves of the pipeline. `jobs -p` lists both curl and python3.
  pids=($(jobs -p))
  CURL_PID="${pids[0]:-}"
  PROC_PID="${pids[1]:-}"
  wait "$PIPE_PID"
  rc=$?
  CURL_PID=""; PROC_PID=""

  [[ $SHUTTING_DOWN -eq 1 ]] && exit 0   # trap already reported

  log "stream ended (exit $rc) — reconnecting in ${sleep_s}s"
  sleep "$sleep_s"

  # Exponential backoff with cap.
  sleep_s=$(python3 -c "print(min(float('$ES_BACKOFF_MAX'), float('$sleep_s') * float('$ES_BACKOFF_FACTOR')))")
done
