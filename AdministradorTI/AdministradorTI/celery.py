import os
from celery import Celery

# Establece el módulo de configuración de Django para el programa 'celery'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AdministradorTI.settings')

# Crea una instancia de Celery
app = Celery('AdministradorTI')

# Carga la configuración de Celery desde las configuraciones de Django.
# Con el prefijo 'CELERY', todas las variables de configuración de Celery
# en settings.py se usarán.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descubre y carga las tareas automáticamente de todos tus apps de Django.
app.autodiscover_tasks()