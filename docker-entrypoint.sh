#!/bin/bash
echo "Waiting for DB availability"
while ! </dev/tcp/db/3306; do sleep 1; done
python manage.py runserver 0.0.0.0:8000
