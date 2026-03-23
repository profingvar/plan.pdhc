#!/usr/bin/env bash
# start.sh — Single entry-point for the PDHC PlanDef Builder (Rule 16)
# Backs up DB before restart, starts DB + app, handles graceful shutdown.

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLANP_DIR="$PROJECT_DIR/planp"
BACKUP_DIR="$PROJECT_DIR/db_backups"
DOCKER_COMPOSE="docker-compose"

# Use homebrew docker-compose if available (macOS server)
if [ -x /opt/homebrew/bin/docker-compose ]; then
    DOCKER_COMPOSE="/opt/homebrew/bin/docker-compose"
fi

echo "=== PDHC PlanDef Builder Startup ==="

# 1. Backup database if DB container is running
if docker ps --format '{{.Names}}' 2>/dev/null | grep -q '^pdhc_db$'; then
    echo "Backing up database before restart..."
    mkdir -p "$BACKUP_DIR"
    TIMESTAMP=$(date -u +"%Y-%m-%dT%H-%M-%SZ")
    BACKUP_FILE="$BACKUP_DIR/pdhc_${TIMESTAMP}.sql.gz"
    if docker exec pdhc_db pg_dumpall -U pdhc_admin 2>/dev/null | gzip > "$BACKUP_FILE"; then
        SIZE=$(ls -lh "$BACKUP_FILE" | awk '{print $5}')
        echo "  Backup saved: $BACKUP_FILE ($SIZE)"
        # Keep only last 10 backups
        ls -t "$BACKUP_DIR"/pdhc_*.sql.gz 2>/dev/null | tail -n +11 | xargs rm -f 2>/dev/null || true
    else
        echo "  WARNING: Backup failed (DB may not be accepting connections)"
        rm -f "$BACKUP_FILE"
    fi
else
    echo "No running DB container found — skipping backup."
fi

# 2. Kill project ports (9030-9033)
echo "Cleaning up ports 9030-9033..."
for port in 9030 9031 9032 9033; do
    pids=$(lsof -ti :"$port" 2>/dev/null || true)
    if [ -n "$pids" ]; then
        echo "  Killing processes on port $port: $pids"
        echo "$pids" | xargs kill -9 2>/dev/null || true
    fi
done

# 3. Ensure Docker/Colima is running
if ! docker info > /dev/null 2>&1; then
    echo "Docker is not running. Trying colima..."
    if command -v colima > /dev/null 2>&1; then
        colima start
    else
        echo "Attempting to start Docker Desktop..."
        open -a Docker
    fi
    echo "Waiting for Docker to be ready..."
    while ! docker info > /dev/null 2>&1; do
        sleep 2
    done
    echo "Docker is ready."
fi

# 4. Activate virtual environment
if [ -d "$PLANP_DIR/venv" ]; then
    echo "Activating virtual environment..."
    source "$PLANP_DIR/venv/bin/activate"
else
    echo "WARNING: No venv found at $PLANP_DIR/venv"
fi

# 5. Graceful stop of existing containers (no -v flag — preserves volumes)
cd "$PLANP_DIR"
echo "Stopping existing containers (if any)..."
$DOCKER_COMPOSE down 2>/dev/null || true

# 6. Start DB and app
echo "Starting services..."
$DOCKER_COMPOSE up -d --build

# 7. Wait for health check
echo "Waiting for DB to be healthy..."
for i in $(seq 1 30); do
    if docker exec pdhc_db pg_isready -U pdhc_admin -d pdhc_gateway > /dev/null 2>&1; then
        echo "  DB is ready."
        break
    fi
    if [ "$i" -eq 30 ]; then
        echo "  WARNING: DB health check timed out after 30s"
    fi
    sleep 1
done

echo ""
echo "=== Services started ==="
echo "  App:      http://localhost:9030"
echo "  Database: localhost:9031"
echo ""
echo "Tailing logs (Ctrl+C to stop)..."
echo ""

# 8. Graceful shutdown on Ctrl+C
cleanup() {
    echo ""
    echo "=== Shutting down ==="
    cd "$PLANP_DIR"
    $DOCKER_COMPOSE down
    if [ -n "$VIRTUAL_ENV" ]; then
        deactivate 2>/dev/null || true
    fi
    echo "Shutdown complete."
    exit 0
}
trap cleanup INT TERM

# Tail logs
$DOCKER_COMPOSE logs -f
