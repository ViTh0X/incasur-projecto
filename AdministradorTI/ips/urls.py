from django.urls import path
from . import views

urlpatterns = [
    path('',views.listar_ips,name='listar_ips'),
    path('editar-ip/<int:pk>/',views.editar_ip,name='editar_ip'),
    path('reiniciar-data-ip/<int:pk>/',views.reiniciar_data_ip,name='reiniciar_data_ip'),
    path("agregar-accion/",views.agregar_accion, name="agregar_accion"),
    path("historial-acciones/<int:pk>/",views.ver_historial_acciones, name="ver_historial_acciones"),
    path('generar-excel-ip',views.generar_excel_ip,name='generar_excel_ip'),
]
