from django.urls import path
from . import views

urlpatterns = [
    path('',views.listar_inventario_software,name='listar_inventario_software'),
    path('iniciar-inventario-software/',views.iniciar_inventario_software,name='iniciar_inventario_software'),
    path('iniciar-faltantes-software/',views.iniciar_faltantes_software,name='iniciar_faltantes_software'),
    path('listar-faltantes-software/',views.listar_faltantes_software,name='listar_faltantes_software'),
    path('status/<str:task_id>/',views.verificar_estado_tarea,name='verificar_estado_tarea'),
    # path('actualizar-tabla/',views.actualizar_tabla,name='actualizar_tabla'),
    path('generar-excel-all-inventario',views.generar_excell_all,name='generar_excell_all'),
    path('listar-logs',views.listar_logs,name='listar_logs'),        
]
