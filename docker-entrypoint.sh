#!/bin/bash
echo "Waiting for DB availability"
while ! </dev/tcp/db/5432; do sleep 1; done
while ! </dev/tcp/mysql_db/3306; do sleep 1; done
python manage.py migrate
python manage.py compilemessages
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8000
