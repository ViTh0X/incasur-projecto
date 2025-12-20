from django.urls import path
from . import views

urlpatterns = [
    path('',views.listar_inventario_software,name='listar_inventario_software'),
    path('iniciar-inventario-software/',views.iniciar_inventario_software,name='iniciar_inventario_software'),
    path('iniciar-faltantes-software/',views.iniciar_faltantes_software,name='iniciar_faltantes_software'),
    path('listar-faltantes-software/',views.listar_faltantes_software,name='listar_faltantes_software'),
    path('status/<str:task_id>/',views.verificar_estado_tarea,name='verificar_estado_tarea'),
    # path('actualizar-tabla/',views.actualizar_tabla,name='actualizar_tabla'),
    path('generar-excel-all-inventario-s',views.generar_excell_all_s,name='generar_excell_all_s'),
    path('listar-logs-s',views.listar_logs_s,name='listar_logs_s'),
    path('actualizar-ejecutable-s/',views.actualizar_ejecutable_s,name='actualizar_ejecutable_s'),
]
