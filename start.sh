#!/usr/bin/env bash
# start.sh — Single entry-point for the PDHC PlanDef Builder (Rule 16)
# Kills legacy and project ports, starts DB + app, handles graceful shutdown.

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
GATEWAY_DIR="$PROJECT_DIR/gateway"

echo "=== PDHC PlanDef Builder Startup ==="

# 1. Kill project ports (9030-9033)
echo "Cleaning up ports 9030-9033..."
for port in 9030 9031 9032 9033; do
    pids=$(lsof -ti :"$port" 2>/dev/null || true)
    if [ -n "$pids" ]; then
        echo "  Killing processes on port $port: $pids"
        echo "$pids" | xargs kill -9 2>/dev/null || true
    fi
done

# 3. Ensure Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Docker is not running. Attempting to start Docker Desktop..."
    open -a Docker
    echo "Waiting for Docker to start..."
    while ! docker info > /dev/null 2>&1; do
        sleep 2
    done
    echo "Docker is ready."
fi

# 4. Activate virtual environment
if [ -d "$GATEWAY_DIR/venv" ]; then
    echo "Activating virtual environment..."
    source "$GATEWAY_DIR/venv/bin/activate"
else
    echo "WARNING: No venv found at $GATEWAY_DIR/venv"
fi

# 5. Start DB and app
echo "Starting services via Docker Compose..."
cd "$GATEWAY_DIR"
docker compose up -d --build

echo ""
echo "=== Services started ==="
echo "  App:      http://localhost:9030"
echo "  Database: localhost:9031"
echo ""
echo "Tailing logs (Ctrl+C to stop)..."
echo ""

# 6. Graceful shutdown on Ctrl+C
cleanup() {
    echo ""
    echo "=== Shutting down ==="
    cd "$GATEWAY_DIR"
    docker compose down
    if [ -n "$VIRTUAL_ENV" ]; then
        deactivate 2>/dev/null || true
    fi
    echo "Shutdown complete."
    exit 0
}
trap cleanup INT TERM

# Tail logs
docker compose logs -f
