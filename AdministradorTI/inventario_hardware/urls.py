from django.urls  import path
from . import views

urlpatterns = [
    path('',views.listar_inventario_hardware,name='listar_inventario_hardware'),
]