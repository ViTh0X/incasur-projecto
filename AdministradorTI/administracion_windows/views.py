from django.shortcuts import render, get_object_or_404,redirect
from ips.models import ips, tipo_equipos_informaticos, tipo_estado_ips
from .models import EstadoAccionesWindows,FaltantesRevisionEquiposWindows
from .task import cambiar_usb_solo_lectura, cambiar_usb_bloqueo_total,cambiar_usb_desbloqueo_total, hacer_reset_contraseña_windows,verificacion_usb_all,verificacion_usb_faltantes


# Create your views here.
def menu_opciones_windows(request):
    #listado_ips =  ips.objects.all()
    estado_ips = get_object_or_404(tipo_estado_ips,pk=1)
    laptop = get_object_or_404(tipo_equipos_informaticos,pk=1)
    pc = get_object_or_404(tipo_equipos_informaticos,pk=2)
    nombres_a_filtrar = [laptop, pc]
    lista_ips_ocupadas = ips.objects.filter(codigo_estado=estado_ips,tipo_equipo_asignado__in=nombres_a_filtrar)
    acciones_windows = EstadoAccionesWindows.objects.filter(id_ip__in=lista_ips_ocupadas).order_by('id_estado')
    return render(request,'menu_opciones_windows/opciones_windows.html',{'acciones_windows':acciones_windows})

def faltantes_verificacion_windows(request):
    faltantes_windows = FaltantesRevisionEquiposWindows.objects.all()
    return render(request,'menu_opciones_windows/faltantes_revision_windows.html',{'faltantes_windows':faltantes_windows})

def usb_solo_lectura(request,pk):
    ip_filtrada = get_object_or_404(ips,pk=pk)        
    if request.method == 'GET':
        cambiar_usb_solo_lectura.delay(ip=ip_filtrada.ip)
        return redirect('menu_opciones_windows')
    return redirect('menu_opciones_windows')


def usb_desbloqueado_totalmente(request,pk):
    ip_filtrada = get_object_or_404(ips,pk=pk)        
    if request.method == 'GET':
        cambiar_usb_desbloqueo_total.delay(ip=ip_filtrada.ip)
        return redirect('menu_opciones_windows')
    return redirect('menu_opciones_windows')


def usb_bloqueado_totalmente(request,pk):
    ip_filtrada = get_object_or_404(ips,pk=pk)        
    if request.method == 'GET':
        cambiar_usb_bloqueo_total.delay(ip=ip_filtrada.ip)
        return redirect('menu_opciones_windows')
    return redirect('menu_opciones_windows')

def resetear_contraseña_windows(request,pk):
    ip_filtrada = get_object_or_404(ips,pk=pk)        
    if request.method == 'GET':
        hacer_reset_contraseña_windows.delay(ip=ip_filtrada.ip)
        return redirect('menu_opciones_windows')
    return redirect('menu_opciones_windows')


def ejecutar_verificacion_usball(request):
    if request.method == 'GET':
        verificacion_usb_all.delay()
        return redirect('menu_opciones_windows')
    return redirect('menu_opciones_windows')

def ejecutar_verificacion_usbfaltantes(request):
    if request.method == 'GET':
        verificacion_usb_faltantes.delay()
        return redirect('menu_opciones_windows')
    return redirect('menu_opciones_windows')