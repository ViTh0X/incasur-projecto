from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.conf import settings
from celery.result import AsyncResult
from .task import ejecutar_faltantes_backup_informacion,ejecutar_backup_informacion,ejecutar_backup_individual

from datetime import datetime
from .models import backups_informacion,faltantes_backup_informacion
from home.models import logs_actividades_celery
from ips.models import ips

from django.contrib.auth.decorators  import login_required

import subprocess
import os
import openpyxl
import pandas as pd
# Create your views here.

@login_required(login_url="pagina_login")
def listar_backup_informacion(request):
    mes_actual = datetime.now().month
    año_actual = datetime.now().year
    lista_backup = backups_informacion.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual)
    if mes_actual < 10:
        fecha_bkup = f"{año_actual} - 0{mes_actual}"
    else:
        fecha_bkup = f"{año_actual} - {mes_actual}"
    if not lista_backup:
        return render(request,'bkinformacion/no_realizo_backup_este_mes.html')
    else:
        return render(request,'bkinformacion/lista_backup_informacion.html',{'lista_backup':lista_backup})

@login_required(login_url="pagina_login")
def listar_faltantes_backup(request):
    mes_actual = datetime.now().month
    año_actual = datetime.now().year
    lista_faltantes = faltantes_backup_informacion.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual)
    if not lista_faltantes:
        return render(request,'bkinformacion/no_tiene_faltantes.html')
    else:
        return render(request,'bkinformacion/lista_faltantes_bk.html',{'lista_faltantes':lista_faltantes})

@login_required(login_url="pagina_login")
def listar_logs(request):    
    lista_logs = logs_actividades_celery.objects.all()
    return render(request,'logs/listar_logs_bk.html',{'lista_logs':lista_logs})    
    

@login_required(login_url="pagina_login")
def iniciar_backup_informacion(request):
    if request.method == 'POST':
        tarea = ejecutar_backup_informacion.delay()
        
        return JsonResponse({'task_id':tarea.id})
    return redirect('listar_inventario_hardware')

@login_required(login_url="pagina_login")
def verificar_estado_tarea(request,task_id):
    estado_tarea = AsyncResult(task_id)
    data = {
        'estado':estado_tarea.status,
        'resultado':estado_tarea.result
    }
    
    return JsonResponse(data)

@login_required(login_url="pagina_login")
def iniciar_faltantes_backup(request):
    if request.method == 'POST':
        tarea = ejecutar_faltantes_backup_informacion.delay()
        
        return JsonResponse({'task_id':tarea.id})
    return redirect('listar_inventario_hardware')

@login_required(login_url="pagina_login")
def descargar_logs_errores(request,pk):    
    backup_ip = get_object_or_404(backups_informacion,pk=pk)
    ip_bk = backup_ip.codigo_ip.ip           
    nombre_archivo_completo = f"LogErrores-{ip_bk}.txt"
    ruta_archivo = os.path.join(settings.MEDIA_ROOT,'logs_errores',nombre_archivo_completo)
    with open(ruta_archivo, 'rb') as archivo:
        contenido = archivo.read()
    response = HttpResponse(contenido,content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo_completo}"'
    return response

@login_required
def descargar_cargo_backup(request,pk):
    instancia_backup = get_object_or_404(backups_informacion,pk=pk)    
    ip_colaborador = instancia_backup.codigo_ip.ip    
    instancia_ip = get_object_or_404(ips,ip=ip_colaborador)    
    nombre_colaborador = instancia_ip.colaborador_asignado.nombre_colaborador
    puesto_colaborador = instancia_ip.colaborador_asignado.cargo_colaborador.nombre_cargo
    plantilla_ruta = os.path.join(settings.MEDIA_ROOT,'plantillas_excel','BACKUP_BITACORA.xlsx')
    try:
        libro = openpyxl.load_workbook(plantilla_ruta)
        hoja = libro.active
    except FileNotFoundError:
        return HttpResponse("Error:La plantilla no fue encontrada")
    
    año = instancia_backup.fecha_modificacion.year
    mes = instancia_backup.fecha_modificacion.month
    dia = instancia_backup.fecha_modificacion.day
    mensaje_Observacion = f"La informacion del Disco D fue guardada correctamente segun archivo Log-{str(ip_colaborador)}-{año}-{mes}-{dia}.txt"
    ruta_archivo_backup = f'/backupcolaboradores/Backup/{ip_colaborador}/'
    if os.path.exists(ruta_archivo_backup):
        tamaño_bytes = subprocess.check_output(['du', '-sb', ruta_archivo_backup]).split()[0]
        for unidad in ['B', 'KB', 'MB', 'GB', 'TB']:
            if tamaño_bytes < 1024:
                return f"{bytes:.2f} {unidad}"
            tamaño_bytes /= 1024
        tamaño_archivo = f'{tamaño_bytes} MB'            
    hoja['C7'] = str(nombre_colaborador)
    hoja['C8'] = str(puesto_colaborador)
    hoja['C10'] = str(ip_colaborador)
    hoja['C11'] = mensaje_Observacion
    hoja['G10'] = tamaño_archivo
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=colaborador_{nombre_colaborador}.xlsx'
    libro.save(response)
    return response
    
    
    
@login_required
def iniciar_backup_individual(request,pk):
    backup_ip = get_object_or_404(backups_informacion,pk=pk)
    ip_bk = backup_ip.codigo_ip.ip    
    if request.method == 'GET':
        ejecutar_backup_individual.delay(ip=ip_bk)
        return redirect('listar_backup_informacion')
    return redirect('listar_backup_informacion')


    