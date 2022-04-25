#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."
    if [ "$FLASK_ENV" = "development" ]
    then
      export DATABASE_URL=postgresql://users_be:users_be@db:5432/users_be_dev
      export SQL_HOST=db
    fi
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