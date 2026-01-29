from django.shortcuts import render, redirect
from django.http.response import JsonResponse

from django.http import HttpResponse
from datetime import datetime
from .models import inventario_software,faltantes_inventario_software
#from colaboradores.models import colaboradores
from home.models import logs_actividades_celery
from ips.models import ips
from celery.result import AsyncResult
from .task import ejecutar_faltantes_inventario_software,ejecutar_inventario_software, actualizar_ejecutable

from django.contrib.auth.decorators import login_required

import pandas as pd
from io import BytesIO
# Create your views here.

@login_required(login_url="pagina_login")
def listar_inventario_software(request):
    año_actual = datetime.now().year
    mes_actual = datetime.now().month
    data_inventario_software = inventario_software.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual)
    if not data_inventario_software:
        return render(request,'inventario_software/no_realizo_inventario_este_mes.html')
    else:
        inventario_agrupado = {}   
        for data in data_inventario_software:
            ip =  data.codigo_ip.ip
            ip_filtrada = ips.objects.get(ip=ip)            
            if ip not in inventario_agrupado:
                inventario_agrupado[ip] ={
                    'Office' : [],
                    'Acceso Remoto' : [],
                    'Editores Texto' : [],
                    'Base Datos' : [],
                    'PDF' : [],
                    'FTIA' : [],
                    'Impresoras' : [],
                    'Navegadores' : [],
                    'Compresores' : [],
                    'Drivers' : [],
                    'Drive' : [],
                    'TI' : [],
                    'Otros' : [],
                    'fecha' : data.fecha_modificacion,
                    'nombre_colaborador' : ip_filtrada.colaborador_asignado.nombre_colaborador
                }
            if data.tipo_software.nombre_tipo == 'Office':
                inventario_agrupado[ip]['Office'].append(data.nombre_software)
            elif data.tipo_software.nombre_tipo == 'Acceso Remoto':
                inventario_agrupado[ip]['Acceso Remoto'].append(data.nombre_software)
            elif data.tipo_software.nombre_tipo == 'Editores Texto':
                inventario_agrupado[ip]['Editores Texto'].append(data.nombre_software)
            elif data.tipo_software.nombre_tipo == 'Base Datos':
                inventario_agrupado[ip]['Base Datos'].append(data.nombre_software)
            elif data.tipo_software.nombre_tipo == 'PDF':
                inventario_agrupado[ip]['PDF'].append(data.nombre_software)
            elif data.tipo_software.nombre_tipo == 'FTIA':
                inventario_agrupado[ip]['FTIA'].append(data.nombre_software)
            elif data.tipo_software.nombre_tipo == 'Impresoras':
                inventario_agrupado[ip]['Impresoras'].append(data.nombre_software)
            elif data.tipo_software.nombre_tipo == 'Navegadores':
                inventario_agrupado[ip]['Navegadores'].append(data.nombre_software)
            elif data.tipo_software.nombre_tipo == 'Compresores':
                inventario_agrupado[ip]['Compresores'].append(data.nombre_software)
            elif data.tipo_software.nombre_tipo == 'Drivers':
                inventario_agrupado[ip]['Drivers'].append(data.nombre_software)
            elif data.tipo_software.nombre_tipo == 'Drive':
                inventario_agrupado[ip]['Drive'].append(data.nombre_software)
            elif data.tipo_software.nombre_tipo == 'TI':
                inventario_agrupado[ip]['TI'].append(data.nombre_software)
            elif data.tipo_software.nombre_tipo == 'Otros':
                inventario_agrupado[ip]['Otros'].append(data.nombre_software)
        
        
        lista_inventarios = []
        for ip, datos in inventario_agrupado.items():
            lista_inventarios.append({
                'ip': ip,
                'nombre_colaborador' : datos['nombre_colaborador'],
                'Office' : datos['Office'],
                'Acceso_Remoto' : datos['Acceso Remoto'],
                'Editores_Texto' : datos['Editores Texto'],
                'Base_Datos' : datos['Base Datos'],
                'PDF' : datos['PDF'],
                'FTIA' : datos['FTIA'],
                'Impresoras' : datos['Impresoras'],
                'Navegadores' : datos['Navegadores'],
                'Compresores' : datos['Compresores'],
                'Drivers' : datos['Drivers'],
                'Drive' : datos['Drive'],
                'TI' : datos['TI'],
                'Otros' : datos['Otros'],
                'fecha' : datos['fecha']
            })
        if mes_actual < 10:
            fecha_software = f"{año_actual} - 0{mes_actual}"
        else:
            fecha_software = f"{año_actual} - {mes_actual}"
        return render(request,'inventario_software/lista_inventario_s.html',{'lista_inventarios':lista_inventarios,'fecha_software':fecha_software})

@login_required(login_url="pagina_login")
def listar_faltantes_software(request):
    año_actual = datetime.now().year
    mes_actual = datetime.now().month
    lista_faltantes = faltantes_inventario_software.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual)
    if not lista_faltantes:
        return render(request,'inventario_software/no_tiene_faltantes.html')
    else:
        return render(request,'inventario_software/lista_faltantes_s.html',{'lista_faltantes':lista_faltantes})

#TEst


@login_required(login_url="pagina_login")    
def listar_logs_s(request):    
    lista_logs = logs_actividades_celery.objects.all()
    return render(request,'logs/listar_logs_is.html',{'lista_logs':lista_logs})


@login_required(login_url="pagina_login")
def iniciar_inventario_software(request):
    if request.method == 'POST':
        tarea = ejecutar_inventario_software.delay()
        
        return JsonResponse({'task_id':tarea.id})
    return redirect('listar_inventario_hardware')


@login_required(login_url="pagina_login")
def actualizar_ejecutable_s(request):
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
def iniciar_faltantes_software(request):
    if request.method == 'POST':
        tarea = ejecutar_faltantes_inventario_software.delay()
        
        return JsonResponse({'task_id':tarea.id})
    return redirect('listar_inventario_hardware')

@login_required(login_url="pagina_login")
def generar_excell_all_s(request):
    fecha_hora = datetime.now()
    año_actual = datetime.now().year
    mes_actual = datetime.now().month
    data_inventario_software = inventario_software.objects.all()
    #data_inventario_software = inventario_software.objects.filter(fecha_modificacion__year=año_actual,fecha_modificacion__month=mes_actual)
    inventario_agrupado = {}   
    for data in data_inventario_software:
        ip =  data.codigo_ip.ip
        ip_filtrada = ips.objects.get(ip=ip)
        #nombre_colab_filtrado = lista_colaboradores.objects.get(ip_colaborador=ip)
        if ip not in inventario_agrupado:
            inventario_agrupado[ip] ={
                'Office' : [],
                'Acceso Remoto' : [],
                'Editores Texto' : [],
                'Base Datos' : [],
                'PDF' : [],
                'FTIA' : [],
                'Impresoras' : [],
                'Navegadores' : [],
                'Compresores' : [],
                'Drivers' : [],
                'Drive' : [],
                'TI' : [],
                'Otros' : [],
                'fecha' : data.fecha_modificacion,
                'nombre_colaborador' : ip_filtrada.colaborador_asignado.nombre_colaborador
            }
        if data.tipo_software.nombre_tipo == 'Office':
            inventario_agrupado[ip]['Office'].append(data.nombre_software)
        elif data.tipo_software.nombre_tipo == 'Acceso Remoto':
            inventario_agrupado[ip]['Acceso Remoto'].append(data.nombre_software)
        elif data.tipo_software.nombre_tipo == 'Editores Texto':
            inventario_agrupado[ip]['Editores Texto'].append(data.nombre_software)
        elif data.tipo_software.nombre_tipo == 'Base Datos':
            inventario_agrupado[ip]['Base Datos'].append(data.nombre_software)
        elif data.tipo_software.nombre_tipo == 'PDF':
            inventario_agrupado[ip]['PDF'].append(data.nombre_software)
        elif data.tipo_software.nombre_tipo == 'FTIA':
            inventario_agrupado[ip]['FTIA'].append(data.nombre_software)
        elif data.tipo_software.nombre_tipo == 'Impresoras':
            inventario_agrupado[ip]['Impresoras'].append(data.nombre_software)
        elif data.tipo_software.nombre_tipo == 'Navegadores':
            inventario_agrupado[ip]['Navegadores'].append(data.nombre_software)
        elif data.tipo_software.nombre_tipo == 'Compresores':
            inventario_agrupado[ip]['Compresores'].append(data.nombre_software)
        elif data.tipo_software.nombre_tipo == 'Drivers':
            inventario_agrupado[ip]['Drivers'].append(data.nombre_software)
        elif data.tipo_software.nombre_tipo == 'Drive':
            inventario_agrupado[ip]['Drive'].append(data.nombre_software)
        elif data.tipo_software.nombre_tipo == 'TI':
            inventario_agrupado[ip]['TI'].append(data.nombre_software)
        elif data.tipo_software.nombre_tipo == 'Otros':
            inventario_agrupado[ip]['Otros'].append(data.nombre_software)
    
    
    lista_inventarios = []
    for ip, datos in inventario_agrupado.items():
        lista_inventarios.append({
            'ip': ip,
            'nombre_colaborador' : datos['nombre_colaborador'],
            'Office' : datos['Office'],
            'Acceso_Remoto' : datos['Acceso Remoto'],
            'Editores_Texto' : datos['Editores Texto'],
            'Base_Datos' : datos['Base Datos'],
            'PDF' : datos['PDF'],
            'FTIA' : datos['FTIA'],
            'Impresoras' : datos['Impresoras'],
            'Navegadores' : datos['Navegadores'],
            'Compresores' : datos['Compresores'],
            'Drivers' : datos['Drivers'],
            'Drive' : datos['Drive'],
            'TI' : datos['TI'],
            'Otros' : datos['Otros'],
            'fecha' : datos['fecha']
        })            
    df = pd.DataFrame(lista_inventarios)
    df = df.fillna('')
    columnas_con_listas = ['Office','Acceso_Remoto','Editores_Texto','Base_Datos','PDF','FTIA','Impresoras','Navegadores','Compresores','Drivers','Drive','TI','Otros']
    for columna in columnas_con_listas:
        if columna in df.columns:
            df[columna] = df[columna].apply(lambda x: '\n'.join(x) if isinstance(x, list) else x)
    # output = BytesIO()
    # with pd.ExcelWriter(output, engine='openpyxl') as writer:
    #     df.to_excel(writer, sheet_name='Inventario', index=False)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="InventarioSoftware{fecha_hora}.xlsx"'
    df.to_excel(response,index=False,sheet_name='InventarioSoftware')
    return response
    
    