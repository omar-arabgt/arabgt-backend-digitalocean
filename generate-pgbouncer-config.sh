#!/bin/bash

# Source environment variables
if [ -f core/.env ]; then
    export $(grep -v '^#' core/.env | xargs)
fi

# Set database connection variables for PGBouncer
export DB_HOST=${POSTGRES_HOST:-db}
export DB_PORT=${POSTGRES_PORT:-5432}
export DB_USER=${POSTGRES_USER}
export DB_PASSWORD=${POSTGRES_PASSWORD}
export DB_NAME=${POSTGRES_DB}

# Generate pgbouncer.ini from template
envsubst < pgbouncer.ini.template > pgbouncer.ini

# Generate userlist.txt from template
envsubst < userlist.txt.template > userlist.txt

echo "PGBouncer configuration generated successfully"
echo "Using DB_HOST: ${DB_HOST}"
echo "Using DB_USER: ${DB_USER}"
echo "Using DB_NAME: ${DB_NAME}"