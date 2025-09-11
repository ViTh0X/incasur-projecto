from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.conf import settings
from celery.result import AsyncResult
from .task import ejecutar_faltantes_backup_informacion,ejecutar_backup_informacion

from datetime import datetime
from .models import lista_backups_informacion,faltantes_backup_informacion
from home.models import logs_actividades_celery

import os
# Create your views here.

def listar_backup_informacion(request):
    mes_actual = datetime.now().month
    año_actual = datetime.now().year
    lista_backup = lista_backups_informacion.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual)
    if mes_actual < 10:
        fecha_bkup = f"{año_actual} - 0{mes_actual}"
    else:
        fecha_bkup = f"{año_actual} - {mes_actual}"
    if not lista_backup:
        return render(request,'bkinformacion/no_realizo_backup_este_mes.html')
    else:
        return render(request,'bkinformacion/lista_backup_informacion.html',{'lista_backup':lista_backup})

def listar_faltantes_backup(request):
    lista_faltantes = faltantes_backup_informacion.objects.all()
    if not lista_faltantes:
        return render(request,'bkinformacion/no_tiene_faltantes.html')
    else:
        return render(request,'bkinformacion/lista_faltantes_bk.html',{'lista_faltantes':lista_faltantes})

def listar_logs(request):
    lista_logs = logs_actividades_celery.objects.all().order_by('-tiempo_creacion')
    return render(request,'logs/listar_logs_bk.html',{'lista_logs':lista_logs})

def iniciar_backup_informacion(request):
    if request.method == 'POST':
        tarea = ejecutar_backup_informacion.delay()
        
        return JsonResponse({'task_id':tarea.id})
    return redirect('listar_inventario_hardware')

def verificar_estado_tarea(request,task_id):
    estado_tarea = AsyncResult(task_id)
    data = {
        'estado':estado_tarea.status,
        'resultado':estado_tarea.result
    }
    
    return JsonResponse(data)

def iniciar_faltantes_backup(request):
    if request.method == 'POST':
        tarea = ejecutar_faltantes_backup_informacion.delay()
        
        return JsonResponse({'task_id':tarea.id})
    return redirect('listar_inventario_hardware')

def descargar_logs_errores(request,pk):    
    backup_ip = get_object_or_404(lista_backups_informacion,pk=pk)
    ip_bk = backup_ip.ip.ip
    mes_bk = backup_ip.fecha_modificacion.month
    año_bk = backup_ip.fecha_modificacion.year
    nombre_archivo_completo = f"LogErrores-{ip_bk}-{año_bk}-{mes_bk}.txt"
    ruta_archivo = os.path.join(settings.MEDIA_ROOT,'logs_errores',nombre_archivo_completo)
    with open(ruta_archivo, 'rb') as archivo:
        contenido = archivo.read()
    response = HttpResponse(contenido,content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo_completo}"'
    return response