from django.urls import path
from . import views

urlpatterns = [
    path('',views.listar_colaboradores,name='listar_colaboradores'),
    path('agregar-colaborador/',views.agregar_colaborador,name='agregar_colaborador'),
    path('generar-excel-nuevocolab/<int:pk>/',views.generar_excel_nuevocolab,name='generar_excel_nuevocolab'),
    path('editar-colaborador/<int:pk>/',views.editar_colaborador,name='editar_colaborador'),
    path('cesar-colaborador/<int:pk>/',views.cesar_colaborador,name='cesar_colaborador'),    
]
