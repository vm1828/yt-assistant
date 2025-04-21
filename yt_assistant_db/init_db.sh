#!/bin/bash
set -e

if [ "$ENV" = "local" ]; then
    echo "Seeding development data..."
    psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /docker-entrypoint-initdb.d/seed_dev.sql
else
    echo "Skipping seed data."
fi
