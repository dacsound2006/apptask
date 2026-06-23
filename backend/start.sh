#!/usr/bin/env bash
set -e
echo "==> Migrando base de datos..."
python manage.py migrate --noinput
echo "==> Cargando tareas (idempotente)..."
python manage.py seed_tasks
echo "==> Recolectando estáticos..."
python manage.py collectstatic --noinput
echo "==> Iniciando Gunicorn..."
exec gunicorn cloudtasks.wsgi --bind 0.0.0.0:${PORT:-8000} --workers 3
