#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

echo 'Running migrations...'
# python3 manage.py flush --no-input
python3 manage.py migrate

# echo 'Collecting static files...'
python3 manage.py collectstatic --no-input

exec "$@"