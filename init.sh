#!/bin/bash
# Local dev build script

set -e

# Parse the command line arguments
BUILD=true
if [ "$1" == "--no-build" ]; then
    BUILD=false
fi

echo "" && echo "===================================================== SETUP ENVIRONMENT" && echo ""

export ENV=local

env_files=(
    "env/.client.env"
    "env/.db.env"
    "env/.api.env"
)

for env_file in "${env_files[@]}"; do
    echo "Sourcing $env_file"
    set -o allexport
    source "$env_file"
    set +o allexport
done

echo "" && echo "===================================================== INSTALL DEPENDENCIES" && echo ""

if [ "$BUILD_FLAG" = true ]; then
    echo "Installing Python dependencies..."
    cd yt_assistant_api
    poetry install --no-root
    cd ..

    echo "Instaling Node.js dependencies..."
    npm install --prefix yt_assistant_client/
else
    echo "Skipping dependencies installation."
fi

echo "" && echo "===================================================== BUILD PROJECT" && echo ""

if [ "$BUILD" = true ]; then
    echo "Building and starting Docker containers..."
    docker-compose up --build
else
    echo "Starting Docker containers without rebuilding..."
    docker-compose up
fi

echo ""
