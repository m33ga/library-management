#!/bin/bash
set -e  # Faz o script sair imediatamente se qualquer comando falhar

# Log inicial
echo "Starting entrypoint script..."

# Aplicar migrações do banco de dados
echo "Applying database migrations..."
python user_management/manage.py migrate --noinput

# Coletar arquivos estáticos
echo "Collecting static files..."
python user_management/manage.py collectstatic --noinput

# Log final antes de iniciar o servidor
echo "Starting Gunicorn server..."
exec gunicorn user_management.user_management.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --access-logfile - \
    --error-logfile -
