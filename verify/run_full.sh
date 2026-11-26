#!/bin/bash
# Full verification of candidate.json.gz with sqverify-fast, every declared direction,
# stopped by a battery guard below 15 % on a discharging laptop (finished directions are kept).
# Usage: bash verify/run_full.sh /path/to/sqverify-fast [OUTDIR] [THREADS]
# To resume after a stop, set DIRS to a comma-separated list of the missing directions.
SQ=${1:?path to sqverify-fast}; O=${2:-verify/out}; TH=${3:-9}; DIRS=${DIRS:-all}
C=$(cd "$(dirname "$0")/.." && pwd)/candidate.json.gz; mkdir -p "$O/receipts"
echo "$(date '+%F %T') start dirs=$DIRS candidate sha256 $(shasum -a 256 "$C" | cut -c1-16)" >> "$O/run.log"
/usr/bin/time -l "$SQ" --candidate "$C" --n 31 --directions "$DIRS" --threads "$TH" --confirm --receipts "$O/receipts" >> "$O/directions.jsonl" 2>> "$O/run.err" & p=$!
while kill -0 $p 2>/dev/null; do
  bt=$(pmset -g batt 2>/dev/null); bp=$(echo "$bt" | grep -o '[0-9]*%' | head -1 | tr -d '%')
  if echo "$bt" | grep -q discharging && [ "${bp:-100}" -lt 15 ]; then
    echo "$(date '+%F %T') BATTERY GUARD at ${bp}%: stopped" >> "$O/run.log"; kill $p; break
  fi
  sleep 30
done
wait $p; echo "$(date '+%F %T') verifier exit $?" >> "$O/run.log"
