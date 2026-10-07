#!/usr/bin/env bash
# ============================================================
# plan.pdhc — #786 item 4: retire /transfer.
#
#   ./deploy_retire.sh            # compare only. Writes NOTHING.
#   ./deploy_retire.sh --apply
#
# Three kinds of change, and the last two are why this is not the #786 script:
#   FILES      — copy, baseline-checked as usual
#   DELETE     — remove from the server (checked against baseline first, so a
#                file edited on the server is never silently destroyed)
#   ENV_UNSET  — remove named settings from the live .env
#
# The .env edit is the actual point of the retirement: the code removal stops
# plan USING cdr_6's sim key, and this stops plan HOLDING it. Done by writing a
# new file and copying over the target, never `sed -i`, which replaces a
# symlink with a regular file and silently un-shares it.
# cdr_6's own SIM_PDHC_SERVICE_KEY is NOT touched — this removes plan's copy of
# a borrowed credential, it does not rotate sim's key.
# ============================================================
set -euo pipefail
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
docker context use colima >/dev/null 2>&1 || true

MODE="${1:---check}"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TS="$(date -u +%Y%m%dT%H%M%SZ)"
BACKUP="$HOME/backups/predeploy/plan.pdhc/$TS"

LIVE="$(docker inspect pdhc_app --format '{{ index .Config.Labels "com.docker.compose.project.working_dir" }}' 2>/dev/null || true)"
[ -n "$LIVE" ] && [ -d "$LIVE" ] || { echo "ERROR: cannot resolve pdhc_app working_dir"; exit 2; }
REPO="$(dirname "$LIVE")"
[ -d "$REPO/planp/app" ] || { echo "ERROR: $REPO/planp/app missing"; exit 2; }
ENVFILE="$LIVE/.env"
[ -f "$ENVFILE" ] || { echo "ERROR: no .env at $ENVFILE"; exit 2; }

echo "live repo : $REPO"
echo "env file  : $ENVFILE$([ -L "$ENVFILE" ] && echo '  (SYMLINK -> '"$(readlink "$ENVFILE")"')')"
echo "mode      : $MODE"
echo

DRIFT=0; WORK=0

echo "--- files to copy ---"
while read -r f; do [ -n "$f" ] || continue
  new="$SRC/new/$f"; old="$REPO/$f"; base="$SRC/baseline/$f"
  if [ ! -f "$old" ]; then echo "NEW-FILE       $f"; WORK=1; continue; fi
  h_new="$(shasum -a 256 "$new"|cut -d' ' -f1)"; h_old="$(shasum -a 256 "$old"|cut -d' ' -f1)"
  h_base=""; [ -f "$base" ] && h_base="$(shasum -a 256 "$base"|cut -d' ' -f1)"
  if   [ "$h_new" = "$h_old" ]; then echo "IDENTICAL      $f"
  elif [ -z "$h_base" ];       then echo "NO-BASELINE    $f"; DRIFT=1
  elif [ "$h_old" = "$h_base" ]; then echo "SAFE-REPLACE   $f"; WORK=1
  elif grep -q "^$f	" "$SRC/ACCEPT_STALE" 2>/dev/null; then
       echo "STALE-ACCEPTED $f"
       echo "               $(grep "^$f	" "$SRC/ACCEPT_STALE" | cut -f2)"
       WORK=1
  else echo "*** DIFFERS FROM BASELINE ***  $f"
       echo "               the server is either AHEAD (edited there, never"
       echo "               committed) or merely BEHIND. This check cannot tell."
       echo "               '<' my baseline, '>' the server:"
       diff "$base" "$old" | head -20 | sed 's/^/               /' || true; DRIFT=1
  fi
done < "$SRC/FILES"
echo

echo "--- files to delete ---"
while read -r f; do [ -n "$f" ] || continue
  old="$REPO/$f"; base="$SRC/baseline/$f"
  if [ ! -f "$old" ]; then echo "ALREADY-GONE   $f"; continue; fi
  if [ ! -f "$base" ]; then echo "NO-BASELINE    $f (refusing to delete)"; DRIFT=1; continue; fi
  if [ "$(shasum -a 256 "$old"|cut -d' ' -f1)" = "$(shasum -a 256 "$base"|cut -d' ' -f1)" ]; then
    echo "SAFE-DELETE    $f"; WORK=1
  else
    echo "*** DIFFERS, NOT DELETING ***  $f"
    echo "               the server copy was edited; deleting would destroy it"
    DRIFT=1
  fi
done < "$SRC/DELETE"
echo

echo "--- .env settings to remove (names only; values never printed) ---"
ENVWORK=0
while read -r k; do [ -n "$k" ] || continue
  if grep -qE "^[[:space:]]*$k=" "$ENVFILE"; then
    echo "WILL-REMOVE    $k   (line $(grep -nE "^[[:space:]]*$k=" "$ENVFILE" | cut -d: -f1 | tr '\n' ',' | sed 's/,$//'))"
    ENVWORK=1; WORK=1
  else
    echo "NOT-PRESENT    $k"
  fi
done < "$SRC/ENV_UNSET"
echo

if [ "$DRIFT" = "1" ]; then
  echo "ABORT: a server file is not what I started from. Nothing changed."
  echo "Inspect the diff. If the server is AHEAD, reconcile it into git. If it"
  echo "is merely BEHIND, verify no server-only content is lost and write what"
  echo "you checked into ACCEPT_STALE."
  exit 6
fi
[ "$WORK" = "1" ]  || { echo "Nothing to do."; exit 0; }
if [ "$MODE" != "--apply" ]; then
  echo "Compare only. NOTHING was written."
  echo "  ./deploy_retire.sh --apply"
  exit 0
fi

echo "Backing up to $BACKUP"
mkdir -p "$BACKUP"
# `[ -f x ] && { ... }` returns 1 when x is absent. Under `set -e` that makes
# the whole while-loop fail, and the script exits. It did: the first --apply run
# backed up 9 files, hit the last entry (an already-deleted test file), and
# died before copying or deleting anything. Fail-safe, but silent. An explicit
# `if` keeps a missing file from being an error, because for this list it is
# not one -- new and already-removed files are both expected.
while read -r f; do
  [ -n "$f" ] || continue
  if [ -f "$REPO/$f" ]; then
    mkdir -p "$BACKUP/$(dirname "$f")"
    cp -p "$REPO/$f" "$BACKUP/$f"
  fi
done < <(cat "$SRC/FILES" "$SRC/DELETE")
cp -p "$ENVFILE" "$BACKUP/planp_dot_env.backup"
chmod 600 "$BACKUP/planp_dot_env.backup"
echo "Backed up $(find "$BACKUP" -type f | wc -l | tr -d ' ') file(s), including the .env (chmod 600)."
echo

while read -r f; do [ -n "$f" ] || continue
  mkdir -p "$REPO/$(dirname "$f")"; cp "$SRC/new/$f" "$REPO/$f"; echo "copied   $f"
done < "$SRC/FILES"
while read -r f; do [ -n "$f" ] || continue
  if [ -f "$REPO/$f" ]; then rm -f "$REPO/$f"; echo "deleted  $f"; fi
done < "$SRC/DELETE"
echo

if [ "$ENVWORK" = "1" ]; then
  TMP="$(mktemp)"
  PATTERN="$(paste -sd'|' "$SRC/ENV_UNSET")"
  grep -vE "^[[:space:]]*($PATTERN)=" "$ENVFILE" > "$TMP"
  {
    echo ""
    echo "# #786 — CDR6_BASE_URL / CDR6_SERVICE_KEY / CDR6_TIMEOUT /"
    echo "# CDR_TRANSFER_TARGETS removed $TS. The /transfer page and its cdr_6"
    echo "# proxy are retired: plan.pdhc is the authoring plane and was holding"
    echo "# cdr_6's SIM service key, presenting itself as sim.pdhc. The"
    echo "# capability lives where the credential does: 'sim cdr-transfer'."
    echo "# config.py no longer reads these under any name."
  } >> "$TMP"
  # Written as a new file and copied over: sed -i would replace a symlinked
  # .env with a regular file and silently un-share it.
  cp "$TMP" "$ENVFILE"; rm -f "$TMP"
  echo ".env: removed $(wc -l < "$SRC/ENV_UNSET" | tr -d ' ') setting name(s); tombstone appended"
  echo "  remaining CDR6 references in .env: $(grep -cE '^[[:space:]]*CDR6_|^[[:space:]]*CDR_TRANSFER' "$ENVFILE" || true)"
fi
echo

for f in $(grep '\.py$' "$SRC/FILES"); do python3 -m py_compile "$REPO/$f"; done
echo "py_compile OK"
echo

DC="docker compose"; command -v docker-compose >/dev/null 2>&1 && DC="docker-compose"
echo "Rebuilding pdhc_app (up -d --build also re-reads .env at create time) ..."
( cd "$LIVE" && $DC up -d --build app )
echo

echo "Waiting for health ..."
for i in $(seq 1 30); do
  if curl -fsS https://plan.pdhc.se/api/health >/dev/null 2>&1; then
    echo "HEALTHY: $(curl -fsS https://plan.pdhc.se/api/health)"; break; fi
  sleep 2
  [ "$i" = "30" ] && { echo "WARNING: no health in 60s"; docker logs --tail 40 pdhc_app
    echo "Roll back: cp -rp $BACKUP/planp $REPO/planp && cp $BACKUP/planp_dot_env.backup $ENVFILE && (cd $LIVE && $DC up -d --build app)"; exit 5; }
done
echo

echo "=== in-container verification ==="
docker exec pdhc_app sh -c 'test -f /app/app/api/transfer.py && echo "  api/transfer.py: *** STILL PRESENT ***" || echo "  api/transfer.py: gone"'
docker exec pdhc_app sh -c 'test -f /app/app/routes/transfer.py && echo "  routes/transfer.py: *** STILL PRESENT ***" || echo "  routes/transfer.py: gone"'
docker exec pdhc_app sh -c 'test -f /app/app/templates/transfer.html && echo "  transfer.html: *** STILL PRESENT ***" || echo "  transfer.html: gone"'
echo "  CDR6_* in the container environment:"
docker exec pdhc_app sh -c 'env | grep -c "^CDR6_\|^CDR_TRANSFER" || true' | sed 's/^/    count: /'
echo "  config no longer carries the settings:"
docker exec pdhc_app python -c "
import sys; sys.path.insert(0,'/app')
from app import create_app
app = create_app()
bad = [k for k in ('CDR6_BASE_URL','CDR6_SERVICE_KEY','CDR6_TIMEOUT','CDR_TRANSFER_TARGETS') if k in app.config]
print('    %s' % ('all four absent from config' if not bad else '*** STILL IN CONFIG: %r' % bad))
rules = [str(r) for r in app.url_map.iter_rules() if 'transfer' in str(r)]
print('    url rules mentioning transfer: %d %s' % (len(rules), rules if rules else ''))
"
echo
echo "Done. Backup: $BACKUP"
echo "Roll back: cp -rp $BACKUP/planp $REPO/planp && cp $BACKUP/planp_dot_env.backup $ENVFILE && (cd $LIVE && $DC up -d --build app)"
