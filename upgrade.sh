#!/bin/bash
set -e

# Valid environments
VALID_ENVS=("esp32" "esp8266" "go_nodejs" "android")

# Get script directory (repo root)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAST_ENV_FILE="$SCRIPT_DIR/.last_env"

# Usage
usage() {
    echo "Usage: $0 [environment]"
    echo "Available environments: ${VALID_ENVS[*]}"
    echo ""
    echo "  1. Syncs this repo to latest (git pull)"
    echo "  2. Pulls the latest docker images for the specified environment"
    echo "  3. If the service is running, restarts it with the updated images"
    echo ""
    echo "If no argument is given, uses the last environment from start.sh."
    exit 1
}

# Determine target environment
if [ $# -eq 0 ]; then
    # No argument provided, use last environment
    if [ -f "$LAST_ENV_FILE" ]; then
        TARGET_ENV="$(cat "$LAST_ENV_FILE")"
        echo "No argument provided, using last environment: $TARGET_ENV"
    else
        echo "No argument provided and no last environment found."
        usage
    fi
else
    TARGET_ENV="$1"
fi

# Validate environment
VALID=0
for env in "${VALID_ENVS[@]}"; do
    if [ "$TARGET_ENV" = "$env" ]; then
        VALID=1
        break
    fi
done
[ "$VALID" -eq 0 ] && { echo "Invalid environment: $TARGET_ENV"; usage; }

echo "=== Step 1: Syncing repo to latest ==="
cd "$SCRIPT_DIR"
git pull
echo "Repo synced to latest."

echo ""
echo "=== Step 2: Pulling latest docker images for '$TARGET_ENV' ==="
cd "$SCRIPT_DIR/$TARGET_ENV"
docker compose pull
echo "Docker images pulled."

echo ""
echo "=== Step 3: Updating running service ==="
# Check if autopilot-dev container is running
if docker ps -q --filter "name=autopilot-dev" | grep -q .; then
    echo "Service is running, restarting with updated images..."

    # Recreate containers with new images
    docker compose up -d
    sleep 2
    echo "Service updated and running."
else
    echo "No running service detected. Start it with: ./start.sh $TARGET_ENV"
fi

echo ""
echo "Upgrade complete for environment: $TARGET_ENV"
