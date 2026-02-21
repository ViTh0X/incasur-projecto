from django.urls import path
from . import views

urlpatterns = [
    path('',views.menu_opciones_windows,name='menu_opciones_windows'),
    path('faltantes-verificacion-windows',views.faltantes_verificacion_windows,name='faltantes_verificacion_windows'),
    path('usb-solo-lectura/<int:pk>/',views.usb_solo_lectura,name='usb_solo_lectura'),
    path('usb-desbloqueado-totalmente/<int:pk>/',views.usb_desbloqueado_totalmente,name='usb_desbloqueado_totalmente'),
    path('usb-bloqueado-totalmente/<int:pk>/',views.usb_bloqueado_totalmente,name='usb_bloqueado_totalmente'),
    path('resetear-contraseña-windows/<int:pk>/',views.resetear_contraseña_windows,name='resetear_contraseña_windows'),
    path('ejecutar-verficacion-usball',views.ejecutar_verificacion_usball,name='ejecutar_verificacion_usball'),
    path('ejecutar-verifiacion-usbfaltantes',views.ejecutar_verificacion_usbfaltantes,name='ejecutar_verificacion_usbfaltantes'),
]