#!/bin/bash

while ! nc -z mysql 3306; do
  sleep 1
done

python manage.py migrate
python manage.py collectstatic --noinput

exec gunicorn --bind 0.0.0.0:$DJANGO_PORT apps.wsgi