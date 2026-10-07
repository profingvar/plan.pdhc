#!/usr/bin/env bash
# ============================================================
# plan.pdhc — #786 reform deploy.
#
#   ./deploy_786.sh            # compare only. Writes NOTHING.
#   ./deploy_786.sh --apply    # back up, copy, compile, rebuild, verify
#
# Every bundle path in FILES is relative to the REPO root on the server
# (/usr/local/www/plan.pdhc), which is also the docker build context --
# planp/docker-compose.yml uses `context: ..`.
#
# The question asked before writing is not "does the server differ from my new
# file" (it must) but "does the server still match what I started from".
# `baseline/` holds the pre-change copies from git 042330e. A file that matches
# its baseline is provably safe to replace. A file that does not was edited on
# the server and never committed, and copying over it would destroy that work.
# ============================================================
set -euo pipefail
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
docker context use colima >/dev/null 2>&1 || true

MODE="${1:---check}"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TS="$(date -u +%Y%m%dT%H%M%SZ)"
BACKUP="$HOME/backups/predeploy/plan.pdhc/$TS"

LIVE="$(docker inspect pdhc_app \
        --format '{{ index .Config.Labels "com.docker.compose.project.working_dir" }}' 2>/dev/null || true)"
[ -n "$LIVE" ] && [ -d "$LIVE" ] || { echo "ERROR: cannot resolve pdhc_app working_dir (got '${LIVE:-empty}')"; exit 2; }
# working_dir is .../plan.pdhc/planp; the build context and all bundle paths
# are relative to its PARENT. Verified by checking planp/ exists under it.
REPO="$(dirname "$LIVE")"
[ -d "$REPO/planp/app" ] || { echo "ERROR: $REPO/planp/app missing — layout is not what this script expects"; exit 2; }

echo "live repo : $REPO"
echo "compose   : $LIVE"
echo "bundle    : $SRC"
echo "mode      : $MODE"
echo

DIFFER=0; DRIFT=0; MISSING=0
while read -r f; do
  [ -n "$f" ] || continue
  new="$SRC/new/$f"; old="$REPO/$f"; base="$SRC/baseline/$f"
  if [ ! -f "$new" ]; then echo "MISSING-NEW    $f"; MISSING=1; continue; fi
  if [ ! -f "$old" ]; then
    # Absent on the server. Fine when it is new to the repo too, and fine when
    # the server source is simply behind git (technical.md / user_manual.md).
    if [ -f "$base" ]; then
      echo "NEW-ON-SERVER  $f   (exists in git at baseline; server source is behind)"
    else
      echo "NEW-FILE       $f   (new in this change)"
    fi
    DIFFER=1; continue
  fi
  h_new="$(shasum -a 256 "$new" | cut -d' ' -f1)"
  h_old="$(shasum -a 256 "$old" | cut -d' ' -f1)"
  h_base=""; [ -f "$base" ] && h_base="$(shasum -a 256 "$base" | cut -d' ' -f1)"
  if [ "$h_new" = "$h_old" ]; then echo "IDENTICAL      $f   (already deployed)"; continue; fi
  if [ -z "$h_base" ]; then
    echo "NO-BASELINE    $f   — cannot prove the server copy is unmodified"; DRIFT=1
  elif [ "$h_old" = "$h_base" ]; then
    echo "SAFE-REPLACE   $f   ($(wc -c <"$old"|tr -d ' ') -> $(wc -c <"$new"|tr -d ' ') bytes)"
    DIFFER=1
  elif grep -q "^$f	" "$SRC/ACCEPT_STALE" 2>/dev/null; then
    # Inspected and recorded in ACCEPT_STALE: the server copy is an OLDER
    # version of the git file, not uncommitted server work.
    echo "STALE-ACCEPTED $f"
    echo "               $(grep "^$f	" "$SRC/ACCEPT_STALE" | cut -f2)"
    DIFFER=1
  else
    # Differs from baseline. This means one of two things and the check cannot
    # tell them apart: the server is AHEAD (someone edited it there and never
    # committed -- copying destroys that work) or the server is BEHIND (it is
    # simply an older release). Inspect, then either reconcile into git or
    # record the finding in ACCEPT_STALE. Do not just pass --apply.
    echo "*** DIFFERS FROM BASELINE ***  $f"
    echo "               server $(wc -c <"$old"|tr -d ' ') bytes, $(stat -f '%Sm' "$old")"
    echo "               baseline $(wc -c <"$base"|tr -d ' ') bytes"
    echo "               '<' = my baseline, '>' = the server:"
    diff "$base" "$old" | head -30 | sed 's/^/               /' || true
    DRIFT=1
  fi
done < "$SRC/FILES"
echo

[ "$MISSING" = "0" ] || { echo "ABORT: bundle incomplete. Nothing changed."; exit 3; }
if [ "$DRIFT" = "1" ]; then
  echo "ABORT: a server file is not what I started from. Nothing changed."
  echo "Read the diff above: '<' is my baseline, '>' is the server. If the"
  echo "server is AHEAD, save that copy and reconcile it into git. If it is"
  echo "merely BEHIND, verify no server-only content would be lost and record"
  echo "what you checked in ACCEPT_STALE."
  exit 6
fi
[ "$DIFFER" = "1" ] || { echo "Nothing to do — server already matches this bundle."; exit 0; }

if [ "$MODE" != "--apply" ]; then
  echo "Compare only. NOTHING was written."
  echo "Every line should read SAFE-REPLACE, NEW-ON-SERVER, NEW-FILE or IDENTICAL."
  echo "  ./deploy_786.sh --apply"
  exit 0
fi

echo "Backing up to $BACKUP"
mkdir -p "$BACKUP"
while read -r f; do
  [ -n "$f" ] || continue
  if [ -f "$REPO/$f" ]; then mkdir -p "$BACKUP/$(dirname "$f")"; cp -p "$REPO/$f" "$BACKUP/$f"; fi
done < "$SRC/FILES"
echo "Backed up $(find "$BACKUP" -type f | wc -l | tr -d ' ') file(s)."
echo

while read -r f; do
  [ -n "$f" ] || continue
  mkdir -p "$REPO/$(dirname "$f")"
  cp "$SRC/new/$f" "$REPO/$f"
  echo "copied  $f"
done < "$SRC/FILES"
echo

# Compile every Python file before anything restarts. A broken module here
# takes down the authoring plane, and plan.pdhc is what request.pdhc resolves
# PlanDefinitions against.
PYFAIL=0
for f in $(grep '\.py$' "$SRC/FILES"); do
  python3 -m py_compile "$REPO/$f" || PYFAIL=1
done
if [ "$PYFAIL" = "1" ]; then
  echo "ERROR: a Python file does not compile. Restoring the backup."
  while read -r f; do [ -f "$BACKUP/$f" ] && cp -p "$BACKUP/$f" "$REPO/$f"; done < "$SRC/FILES"
  echo "Restored. Service untouched."; exit 4
fi
echo "py_compile OK"
echo

# `COPY . .`-style build: a plain restart would run the old code.
DC="docker compose"; command -v docker-compose >/dev/null 2>&1 && DC="docker-compose"
echo "Rebuilding pdhc_app ..."
( cd "$LIVE" && $DC up -d --build app )
echo

echo "Waiting for health ..."
for i in $(seq 1 30); do
  if curl -fsS https://plan.pdhc.se/api/health >/dev/null 2>&1; then
    echo "HEALTHY: $(curl -fsS https://plan.pdhc.se/api/health)"; break
  fi
  sleep 2
  [ "$i" = "30" ] && { echo "WARNING: /api/health did not return in 60s"; docker logs --tail 40 pdhc_app
                       echo "Roll back: cp -rp $BACKUP/* $REPO/ && (cd $LIVE && $DC up -d --build app)"; exit 5; }
done
echo

echo "=== in-container verification ==="
docker exec pdhc_app sh -c 'test -f /app/app/services/canonical_libs.py && echo "  canonical_libs.py: present" || echo "  canonical_libs.py: MISSING"'
docker exec pdhc_app sh -c 'grep -c "What this builds" /app/app/templates/dashboard.html | sed "s/^/  dashboard explainer: /"'
docker exec pdhc_app sh -c 'grep -c "no canonical vocabulary (default)" /app/app/templates/concepts/create.html | sed "s/^/  create form defaults to local: /"'

# The defect class this change fixes is "a document is advertised and does not
# resolve". Assert it IN PRODUCTION rather than trusting the local test.
echo "  every DOCS_CATALOG entry resolves:"
docker exec pdhc_app python -c "
import sys
sys.path.insert(0, '/app')
from app.api.capability import DOCS_CATALOG, _resolve_doc_path
bad = [f for f in DOCS_CATALOG if _resolve_doc_path(f) is None]
print('    %d entries, %d unresolvable' % (len(DOCS_CATALOG), len(bad)))
if bad:
    print('    *** UNRESOLVABLE: %r' % bad)
    sys.exit(1)
print('    all resolve')
" || echo "    *** CATALOG CHECK FAILED — see above"
echo
echo "Done. Backup: $BACKUP"
echo "Roll back: cp -rp $BACKUP/* $REPO/ && (cd $LIVE && $DC up -d --build app)"
