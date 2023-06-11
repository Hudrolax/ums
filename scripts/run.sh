#!/bin/sh
set -e

# wait for db
python wait_for_db.py

echo "Starting the application."

# apply migrations
alembic upgrade head

# run the app
exec uvicorn main:app --host 0.0.0.0 --port 8000