from django.shortcuts import render , redirect
from django.http import Http404, JsonResponse 
from django.http.response import HttpResponse

from datetime import datetime

from home.models import logs_actividades_celery
from .models import inventario_hardware,faltantes_inventario_hardware

#Haciendo uso de Celery
from celery.result import AsyncResult
from .task  import ejecutar_inventario_hardware,ejecutar_faltantes_inventario_hardware, actualizar_ejecutable
# Create your views here.

from django.contrib.auth.decorators  import login_required

import pandas as pd

@login_required(login_url="pagina_login")
def listar_inventario_hardware(request):
    año_actual = datetime.now().year
    mes_actual = datetime.now().month
    inventarios_hardware = inventario_hardware.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual)
    if mes_actual < 10:
        fecha_hardware = f"{año_actual} - 0{mes_actual}"
    else:
        fecha_hardware = f"{año_actual} - {mes_actual}"
    if not inventarios_hardware:                  
        return render(request,'inventario_hardware/no_realizo_inventario_este_mes.html')        
    else:
        return render(request,'inventario_hardware/lista_inventario_h.html',{'inventarios_hardware':inventarios_hardware,'fecha_hardware':fecha_hardware})    
        
@login_required(login_url="pagina_login")
def iniciar_inventario_hardware(request):
    if request.method == 'POST':
        tarea = ejecutar_inventario_hardware.delay()
        
        return JsonResponse({'task_id':tarea.id})
    return redirect('listar_inventario_hardware')

@login_required(login_url="pagina_login")
def actualizar_ejecutable_h(request):
    if request.method == 'POST':
        tarea = actualizar_ejecutable.delay()
        
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
def iniciar_faltantes_hardware(request):
    if request.method == 'POST':
        tarea = ejecutar_faltantes_inventario_hardware.delay()
        
        return JsonResponse({'task_id':tarea.id})
    return redirect('listar_inventario_hardware')
    
@login_required(login_url="pagina_login")    
def listar_faltantes_hardware(request):
    año_actual = datetime.now().year
    mes_actual = datetime.now().month
    lista_faltantes = faltantes_inventario_hardware.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual)
    if not lista_faltantes:
        return render(request,'inventario_hardware/no_tiene_faltantes.html')
    else:
        return render(request,'inventario_hardware/lista_faltantes_h.html',{'lista_faltantes':lista_faltantes})

@login_required(login_url="pagina_login")
def generar_excell_all_h(request):
    fecha_hora = datetime.now()
    inventarios_hardware = inventario_hardware.objects.all()
    data_df = inventarios_hardware.values('ip','nombre_colaborador','nombre_equipo','placa','procesador','ram','video_integrada','video_dedicada','so','almacenamiento','puertas_enlace','fecha_modificacion')
    df = pd.DataFrame(list(data_df))
    df = df.rename(columns={
        'ip':'IP',
        'nombre_colaborador':'Nombre Colaborador',
        'nombre_equipo':'Nombre del Equipo',
        'placa':'Info Placa',
        'procesador':'Info Procesador',        
        'ram':'Info Ram',
        'video_integrada':'Info Video Integrada',
        'video_dedicada':'Info Video Dedicada',
        'so':'Info SO',
        'almacenamiento':'Info Almacenamiento',
        'puertas_enlace':'Info Puertas de Enlace',
        'fecha_modificacion':'Fecha Ejecutado'
    })
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="InventarioHardware{fecha_hora}.xlsx"'
    df.to_excel(response,index=False,sheet_name='InventarioHardware')
    return response

@login_required(login_url="pagina_login")
def listar_logs(request):    
    lista_logs = logs_actividades_celery.objects.all()
    return render(request,'logs/listar_logs_ih.html',{'lista_logs':lista_logs})

@login_required(login_url="pagina_login")
def actualizar_tabla(request):
    return Http404
