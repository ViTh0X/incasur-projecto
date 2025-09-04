from django.urls import path
from . import views

urlpatterns = [
    path('',views.listar_ips,name='listar_ips'),
    path('editar-ip/<int:pk>/',views.editar_ip,name='editar_ip'),
]
