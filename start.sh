#!/usr/bin/env bash
# ============================================================
# plan.pdhc — start.sh
# All-Docker service: DB + app via docker-compose.
# IMPORTANT: No kill -9 on ports — docker-compose down handles it.
# ============================================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLANP_DIR="$SCRIPT_DIR/planp"
BACKUP_DIR="$SCRIPT_DIR/db_backups"

# Detect docker-compose
if [ -x /opt/homebrew/bin/docker-compose ]; then
    DC="/opt/homebrew/bin/docker-compose"
elif command -v docker-compose >/dev/null 2>&1; then
    DC="docker-compose"
elif docker compose version >/dev/null 2>&1; then
    DC="docker compose"
else
    echo "[Plan] ERROR: No docker-compose found."
    exit 1
fi

echo "[Plan] === plan.pdhc starting ==="

# ── 1. Docker check ──────────────────────────────────────────
if ! docker info >/dev/null 2>&1; then
    echo "[Plan] ERROR: Docker is not running."
    echo "  Run: bash /usr/local/www/restart_all.sh"
    exit 1
fi
echo "[Plan] Docker OK"

# ── 2. Backup DB if running ──────────────────────────────────
if docker ps --format '{{.Names}}' 2>/dev/null | grep -q '^pdhc_db$'; then
    echo "[Plan] Backing up database..."
    mkdir -p "$BACKUP_DIR"
    TIMESTAMP=$(date -u +"%Y-%m-%dT%H-%M-%SZ")
    BACKUP_FILE="$BACKUP_DIR/pdhc_${TIMESTAMP}.sql.gz"
    if docker exec pdhc_db pg_dumpall -U pdhc_admin 2>/dev/null | gzip > "$BACKUP_FILE"; then
        echo "[Plan]   Backup saved: $BACKUP_FILE"
        ls -t "$BACKUP_DIR"/pdhc_*.sql.gz 2>/dev/null | tail -n +11 | xargs rm -f 2>/dev/null || true
    else
        echo "[Plan]   Backup failed (non-fatal)"
        rm -f "$BACKUP_FILE"
    fi
fi

# ── 3. Stop existing (docker-compose down only — no kill -9) ─
cd "$PLANP_DIR"
echo "[Plan] Stopping existing containers..."
$DC down 2>/dev/null || true
# Also stop any old containers by name in case project name changed
docker stop pdhc_db pdhc_app 2>/dev/null || true

# ── 4. Start services ────────────────────────────────────────
echo "[Plan] Starting services..."
$DC up -d --build

if [ $? -ne 0 ]; then
    echo "[Plan] ERROR: docker-compose up failed."
    exit 1
fi

# ── 5. Wait for health ───────────────────────────────────────
echo "[Plan] Waiting for app..."
for i in $(seq 1 30); do
    if curl -sf http://localhost:9030/api/health >/dev/null 2>&1; then
        echo "[Plan]   App is healthy."
        break
    fi
    [ "$i" -eq 30 ] && echo "[Plan]   WARNING: Health check timed out"
    sleep 2
done

echo "[Plan] === plan.pdhc is running ==="
echo "  App:      http://localhost:9030"
echo "  Database: localhost:9031"
echo "  Logs:     cd $PLANP_DIR && $DC logs -f"
echo "  Stop:     cd $PLANP_DIR && $DC down"
