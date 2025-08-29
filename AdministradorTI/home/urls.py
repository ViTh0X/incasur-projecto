from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('download-archivo/<str:filename>',views.descargar_archivo_guias,name='descargar_archivo'),
]