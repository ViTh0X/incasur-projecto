from django.urls  import path
from . import views

urlpatterns = [
    path('',views.listar_inventario_hardware,name='listar_inventario_hardware'),
    path('iniciar-inventario-hardware/',views.iniciar_inventario_hardware,name='iniciar_inventario_hardware'),
    path('iniciar-faltantes-hardware/',views.iniciar_faltantes_hardware,name='iniciar_faltantes_hardware'),
    path('listar-faltantes-hardware/',views.listar_faltantes_hardware,name='listar_faltantes_hardware'),
    path('status/<str:task_id>/',views.verificar_estado_tarea,name='verificar_estado_tarea'),
    path('actualizar-tabla/',views.actualizar_tabla,name='actualizar_tabla'),
    path('generar-excel-all-inventario',views.generar_excell_all,name='generar_excell_all'),
    path('listar-logs',views.listar_logs,name='listar_logs'),
]