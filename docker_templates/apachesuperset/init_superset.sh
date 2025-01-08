#!/bin/bash

# Wait for the database to be ready
echo "Waiting for PostgreSQL to start..."
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "superset-metadata-db" -p "5432" -U "superset" -d "superset" -c '\q' 2>/dev/null; do
  echo "Postgres is unavailable - sleeping"
  sleep 3
done
echo "PostgreSQL is up!"

echo "Running superset db upgrade"
superset db upgrade

echo "Creating admin user (if not exists)"
superset fab create-admin \
  --username admin \
  --password admin \
  --firstname Superset \
  --lastname Admin \
  --email admin@example.com \

echo "Initializing roles and permissions"
superset init

echo "Starting Superset"
# Use the same command the official image runs by default (gunicorn)
exec gunicorn -w 2 -k gevent --timeout 60 -b 0.0.0.0:8088 "superset.app:create_app()"
