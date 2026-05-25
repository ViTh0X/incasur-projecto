from django.urls import path
from . import views

urlpatterns = [
    path('',views.equipos_informaticos,name='equipos_informaticos'),
    path('agregar-laptop-pc',views.agregar_laptop_pc,name='agregar_laptop_pc'),
    path('listar-laptops-pc',views.listar_laptops_pc,name='listar_laptops_pc'),
    path('agregar-equipo-informatico-ti',views.agregar_equipo_informatico_ti,name='agregar_equipo_informatico_ti'),
    path('listar-equipos-informaticos-ti',views.listar_equipos_informaticos_ti,name='listar_equipos_informaticos_ti'),
    path('editar-equipo-informatico-ti/<int:pk>/',views.editar_equipo_informatico_ti,name='editar_equipo_informatico_ti'),
    path('editar-ip/<int:pk>/',views.editar_ip,name='editar_ip'),
    path('reiniciar-data-ip/<int:pk>/',views.reiniciar_data_ip,name='reiniciar_data_ip'),
    path("agregar-intervencion-ti/<str:ip>",views.agregar_intervencion_ti, name="agregar_intervencion_ti"),
    path("historial-acciones/<str:ip>/",views.ver_historial_acciones, name="ver_historial_acciones"),
    path('generar-excel-ip',views.generar_excel_ip,name='generar_excel_ip'),
    path('filtrar-equipos-nombres',views.filtrar_equipos_nombres,name='filtrar_equipos_nombres'),    
    path('filtrar-equipos-ti-nombres',views.filtrar_equipos_ti_nombres,name='filtrar_equipos_ti_nombres'),    
]
