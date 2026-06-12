#!/bin/bash
set -e

echo "[STEP 1] Copying cloned repo to /code..."
cp -arf "$GIT_TEMP_DIR/." "$TARGET_DIR/"

# Move into working directory
cd "$TARGET_DIR"

echo "[STEP 2] Installing Python dependencies..."
pip install -r requirements.txt

echo "[STEP 3] Running Django migrations..."
python manage.py makemigrations
python manage.py migrate

echo "[STEP 4] Starting Gunicorn..."
gunicorn -c gunicorn_config.py config.wsgi:application
