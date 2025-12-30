from django.urls import path
from . import views

urlpatterns = [
    path('',views.listar_backup_informacion,name='listar_backup_informacion'),
    path('iniciar-backup-informacion/',views.iniciar_backup_informacion,name='iniciar_backup_informacion'),
    path('iniciar-faltantes-backup/',views.iniciar_faltantes_backup,name='iniciar_faltantes_backup'),
    path('listar-faltantes-backup/',views.listar_faltantes_backup,name='listar_faltantes_backup'),
    path('status/<str:task_id>/',views.verificar_estado_tarea,name='verificar_estado_tarea'),
    path('listar-logs/',views.listar_logs,name='listar_logs'),
    path('descargar-log-errores/<int:pk>/',views.descargar_logs_errores,name='descargar_logs_errores'),
    path('iniciar_backup_individual/<int:pk>/',views.iniciar_backup_individual,name='iniciar_backup_individual'),    
]
