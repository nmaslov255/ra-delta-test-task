#!/bin/bash

while ! nc -z mysql 3306; do
  sleep 1
done

python manage.py migrate
python manage.py collectstatic --noinput

# Granting privileges to create test database
sql="GRANT ALL PRIVILEGES ON \`test_$MYSQL_DATABASE\`.* TO $MYSQL_USER@\`%\`;"
mysql --password=$MYSQL_ROOT_PASSWORD --execute="$sql"

exec gunicorn --bind 0.0.0.0:$DJANGO_PORT apps.wsgi