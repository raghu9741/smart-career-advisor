#!/usr/bin/env sh
set -eu

export FLASK_APP="${FLASK_APP:-backend.app}"

python -m flask --app "${FLASK_APP}" db upgrade -d backend/migrations
python -m backend.seed

exec gunicorn --bind "0.0.0.0:${PORT:-10000}" backend.app:app
