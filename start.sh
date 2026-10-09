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
    if [ -f "$LAST_ENV_FILE" ]; then
        echo "Last used environment: $(cat "$LAST_ENV_FILE")"
    fi
    echo ""
    echo "If no argument is given, the last used environment will be started."
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

# Check if autopilot-dev container is running
if docker ps -q --filter "name=autopilot-dev" | grep -q .; then
    echo "Detected running environment, stopping..."

    # Stop the main autopilot container
    docker stop autopilot-dev 2>/dev/null || true

    # Stop any running docling containers (by image name)
    docling_containers=$(docker ps -q --filter "ancestor=ghcr.io/docling-project/docling-rs-serve" 2>/dev/null || true)
    if [ -n "$docling_containers" ]; then
        echo "$docling_containers" | xargs docker stop 2>/dev/null || true
    fi

    sleep 1
    echo "Stopped previous environment."
fi

# Start the new environment
echo "Starting environment: $TARGET_ENV"
cd "$SCRIPT_DIR/$TARGET_ENV"
docker compose up -d

# Save last used environment
echo "$TARGET_ENV" > "$LAST_ENV_FILE"

echo ""
echo "Environment '$TARGET_ENV' is now running."
echo "  - Autopilot: http://localhost:8081"
echo "  - Docling:   http://localhost:5001"
