#!/bin/bash

# Ruta a tu entorno virtual
VENV_PATH="/var/www/incasur-projecto/venv"
# Ruta a tu archivo .env
ENV_PATH="/var/www/incasur-projecto/AdministradorTI/.env"
# Ruta al directorio de la aplicación Celery (donde está celery.py)
APP_DIR="/var/www/incasur-projecto/AdministradorTI"

# Carga las variables de entorno del archivo .env
if [ -f "$ENV_PATH" ]; then
    export $(grep -v '^#' "$ENV_PATH" | xargs)
fi

# Cambia al directorio del proyecto para que Celery encuentre la app
cd "$APP_DIR"

# Activa el entorno virtual e inicia el worker de Celery
source "$VENV_PATH/bin/activate"

# Inicia el worker de Celery
exec celery -A AdministradorTI worker -l info -c 4 --settings=AdministradorTI.settings