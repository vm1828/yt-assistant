#!/bin/bash
# Db migration script
set -e

UTILS='./scripts/utils'

echo "" && echo "===================================================== SETUP ENVIRONMENT" && echo ""

export ENV=local
source "${UTILS}/source_env_vars.sh"

echo "" && echo "===================================================== RUN DB CONTAINER" && echo ""

if [ ! "$(docker ps -q -f name=yt_assistant_db)" ]; then
    echo "Starting db container it..."
    docker-compose up -d yt_assistant_db
    sleep 3
else
    echo "Db container is already running."
fi

echo "" && echo "===================================================== CREATE MIGRATION" && echo ""

docker-compose exec yt_assistant_api poetry run alembic revision --autogenerate -m "$1"

# Check if migration file was generated
if [ $? -eq 0 ]; then
    echo "Migration created successfully!"
else
    echo "Error: Migration was not created!"
    exit 1
fi

echo ""
echo "================================================================ SQL CHANGES"
docker-compose exec yt_assistant_api poetry run alembic upgrade --sql head

echo ""
read -p "Do you want to continue with the migration (y/n)? " confirm
if [[ $confirm != "y" && $confirm != "Y" ]]; then
    echo "Migration canceled."
    exit 0
fi

echo "Applying migration to the database..."
docker-compose exec yt_assistant_api poetry run alembic upgrade head

echo "Migration applied successfully!"
