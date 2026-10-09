#!/bin/bash
set -e

# Get script directory (repo root)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if autopilot-dev container is running
if docker ps -q --filter "name=autopilot-dev" | grep -q .; then
    echo "Stopping running environment..."

    # Stop the main autopilot container
    docker stop autopilot-dev 2>/dev/null || true

    # Stop any running docling containers (by image name)
    docling_containers=$(docker ps -q --filter "ancestor=ghcr.io/docling-project/docling-rs-serve" 2>/dev/null || true)
    if [ -n "$docling_containers" ]; then
        echo "$docling_containers" | xargs docker stop 2>/dev/null || true
    fi

    sleep 1
    echo "Environment stopped."
else
    echo "No running environment detected."
fi
