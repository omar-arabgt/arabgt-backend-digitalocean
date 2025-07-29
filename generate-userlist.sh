#!/bin/bash

# PGBouncer wrapper script that generates userlist.txt and starts PGBouncer

echo "Starting PGBouncer with dynamic userlist generation..."

# Generate userlist.txt with credentials from environment variables
echo "\"${POSTGRES_USER}\" \"${POSTGRES_PASSWORD}\"" > /etc/pgbouncer/userlist.txt

echo "Generated userlist.txt with user: ${POSTGRES_USER}"
echo "Userlist content:"
cat /etc/pgbouncer/userlist.txt

# Start the original PGBouncer entrypoint
echo "Starting PGBouncer..."
exec /opt/pgbouncer/entrypoint.sh