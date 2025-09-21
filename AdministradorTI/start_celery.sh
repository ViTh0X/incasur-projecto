#!/bin/bash

# Ruta a tu entorno virtual
VENV_PATH="/var/www/incasur-projecto/venv"
# Ruta a tu archivo .env
ENV_PATH="/var/www/incasur-projecto/AdministradorTI/.env"
# Ruta a tu proyecto
PROJECT_PATH="/var/www/incasur-projecto/AdministradorTI"

# Carga las variables de entorno del archivo .env
if [ -f "$ENV_PATH" ]; then
    export $(grep -v '^#' "$ENV_PATH" | xargs)
fi

# Activa el entorno virtual
source "$VENV_PATH/bin/activate"

# Cambia al directorio del proyecto
cd "$PROJECT_PATH"

# Inicia el worker de Celery
exec "$VENV_PATH/bin/celery" -A AdministradorTI worker -l info -c 4 --settings=AdministradorTI.settings