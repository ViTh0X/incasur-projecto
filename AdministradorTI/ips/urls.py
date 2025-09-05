from django.urls import path
from . import views

urlpatterns = [
    path('',views.listar_ips,name='listar_ips'),
    path('editar-ip/<int:pk>/',views.editar_ip,name='editar_ip'),
    path('reiniciar-data-ip/<int:pk>/',views.reiniciar_data_ip,name='reiniciar_data_ip'),
    path('generar-excel-ip',views.generar_excel_ip,name='generar_excel_ip'),
]
