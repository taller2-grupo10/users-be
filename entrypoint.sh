#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

flask db upgrade

if [ "$FLASK_ENV" = "development" ]
then
    echo "[ENTRYPOINT.SH] Development mode"
    python app.py
else
    echo "[ENTRYPOINT.SH] Production mode"
    gunicorn app:app
fi

exec "$@"