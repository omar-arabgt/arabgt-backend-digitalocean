#!/bin/bash

echo "Generating PGBouncer userlist..."
echo "User: $DATABASES_USER"
echo "Password: [HIDDEN]"

# Generate userlist.txt with proper credentials
echo "\"$DATABASES_USER\" \"$DATABASES_PASSWORD\"" > /etc/pgbouncer/userlist.txt

echo "Generated userlist.txt:"
cat /etc/pgbouncer/userlist.txt

echo "Starting PGBouncer..."
exec /opt/pgbouncer/entrypoint.sh