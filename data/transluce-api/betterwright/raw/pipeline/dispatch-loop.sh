W=/job/work
export PATH=$W/opt/bun:$PATH BETTERWRIGHT_CHROMIUM_ARGS=--no-sandbox BETTERWRIGHT_HEADLESS=1 BETTERWRIGHT_NO_DAEMON=1
while [ ! -f $W/control/EXIT ]; do
  rm -f $W/control/RESTART_DISPATCHER
  bun $W/dispatcher.mjs >> /job/logs/dispatcher.log 2>&1
  echo "$(date -Is) dispatcher exited $?" >> /job/logs/dispatcher.log
  [ -f $W/control/RESTART_DISPATCHER ] || break
  sleep 3
done
