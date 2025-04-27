#!/bin/bash
# Local dev build script
set -e

# Parse the command line arguments
BUILD=true
if [ "$1" == "--no-build" ]; then
    BUILD=false
fi

UTILS='./scripts/utils'
find scripts/ -type f -exec chmod 700 {} +

echo "" && echo "===================================================== SETUP ENVIRONMENT" && echo ""

export ENV=local
source "${UTILS}/source_env_vars.sh"

echo "" && echo "===================================================== INSTALL DEPENDENCIES" && echo ""

if [ "$BUILD" = true ]; then
    "${UTILS}/install_local_deps.sh"
else
    echo "Skipping dependencies installation."
fi

echo "" && echo "===================================================== BUILD PROJECT" && echo ""

if [ "$BUILD" = true ]; then
    echo "Building and starting Docker containers..."
    docker-compose up --build -d
    sleep 3
    docker-compose exec yt_assistant_api poetry run alembic upgrade head
else
    echo "Starting Docker containers without rebuilding..."
    docker-compose up -d
fi

echo ""
