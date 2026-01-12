#!/bin/bash
# Build Docker image for 11+ Tutor Application

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Image name and tag
IMAGE_NAME="11plus-tutor"
TAG="${1:-latest}"

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                    Building 11+ Tutor Docker Image                           ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "  Project root: $PROJECT_ROOT"
echo "  Image name:   $IMAGE_NAME:$TAG"
echo ""

cd "$PROJECT_ROOT"

# Build the Docker image
echo "Building Docker image..."
docker build \
    --tag "$IMAGE_NAME:$TAG" \
    --tag "$IMAGE_NAME:latest" \
    --progress=plain \
    .

echo ""
echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║  Build Complete!                                                             ║"
echo "╠══════════════════════════════════════════════════════════════════════════════╣"
echo "║  To run the container:                                                       ║"
echo "║                                                                              ║"
echo "║    docker run -d -p 3783:3783 -p 8002:8002 --name 11plus-tutor $IMAGE_NAME   ║"
echo "║                                                                              ║"
echo "║  Or use Docker Compose:                                                      ║"
echo "║                                                                              ║"
echo "║    docker compose up -d                                                      ║"
echo "║                                                                              ║"
echo "║  Then open: http://localhost:3783                                            ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
