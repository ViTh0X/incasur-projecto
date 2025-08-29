from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('instalar_forticlient/',views.instalar_forticlient,name='instalar_forticlient'),
    path('download-archivo-pdf/<str:filename>',views.descargar_archivo_guias_pdf,name='descargar_archivo_pdf'),
    path('download-archivo-exe/<str:filename>',views.descargar_archivo_instaladores,name='descargar_archivo_instaladores'),
]