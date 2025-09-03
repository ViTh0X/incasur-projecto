from django.urls import path
from . import views

urlpatterns = [
    path('',views.listar_colaboradores,name='listar_colaboradores'),
    path('agregar-colaborador/',views.agregar_colaborador,name='agregar_colaborador'),
]
