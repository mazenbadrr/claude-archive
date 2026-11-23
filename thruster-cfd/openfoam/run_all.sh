#!/bin/sh
# Run all 9 cases (resin/pla/smooth x 1500/1750/2000) in separate run dirs,
# then collate into results_all.csv.  Each case is independent.
cd "${0%/*}" || exit 1
ROOT=$(pwd)

for MAT in resin pla smooth; do
  for RPM in 1500 1750 2000; do
    RUN="$ROOT/runs/${MAT}_${RPM}"
    echo "##################  $MAT  $RPM  ##################"
    rm -rf "$RUN"; mkdir -p "$RUN"
    for d in 0.orig constant system scripts config; do cp -r "$ROOT/$d" "$RUN/"; done
    cp "$ROOT/Allrun" "$RUN/"; chmod +x "$RUN/Allrun" "$RUN"/scripts/*.py
    ( cd "$RUN" && ./Allrun "$MAT" "$RPM" ) || echo "!! $MAT $RPM failed, continuing"
  done
done

# combine the per-run results.csv
first=1
for f in "$ROOT"/runs/*/results.csv; do
  [ -f "$f" ] || continue
  if [ $first = 1 ]; then cat "$f"; first=0; else tail -n +2 "$f"; fi
done > "$ROOT/results_all.csv"
echo "=== ALL DONE -> results_all.csv ==="
cat "$ROOT/results_all.csv"
