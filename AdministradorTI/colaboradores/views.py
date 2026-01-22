from django.shortcuts import render, get_list_or_404,get_object_or_404 ,redirect
from django.http import HttpResponse, Http404
from django.conf import settings
from io import BytesIO

import os
import datetime
import openpyxl
import pandas as pd

from datetime import datetime

from home.models import cuentas_forticlient
from inventario_hardware.models import inventario_hardware
from .models import lista_colaboradores, colaboradorForm, estado_colaboradores
from ips.models import tipo_estado_ips, lista_ips

from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url="pagina_login")
def listar_colaboradores(request):
    try:
        estado_colaborador = get_object_or_404(estado_colaboradores,pk=1)
        colaboradores = lista_colaboradores.objects.filter(estado_colaboradores=estado_colaborador).order_by("codigo_colaborador")
    except:
        pass
    return render(request,'colaboradores/lista_colaboradores.html',{'colaboradores':colaboradores})   

@login_required(login_url="pagina_login")
def agregar_colaborador(request):
    if request.method == 'POST':
        formulario = colaboradorForm(request.POST)
        if formulario.is_valid():
            #Obtenemos un objeto ip de la lista de ips
            ip_colaborador = formulario.cleaned_data['ip_colaborador']
            #Aqui cambiar la actualioacion de nombre para hardware y tambien para 
            #ip
            
            
            
            #Por medio del formulario obtenemos un objeto de lista_colaboradores
            add_colaborador = formulario.save(commit=False)
            estado_colaborador_activo = get_object_or_404(estado_colaboradores,pk=1)            
            add_colaborador.estado_colaboradores = estado_colaborador_activo
            add_colaborador.save()
            #Recordar que si es un foreign key, necesitamos pasarle una instancia de el fk estado_colaborador_activo = get_object_or_404(estado_colaboradores,pk=1)  a nuestro formulario para guardar,            
            estado_ip_ocupada = get_object_or_404(tipo_estado_ips,pk=1)
            ip_colaborador.codigo_estado = estado_ip_ocupada
            ip_colaborador.save() 
            #LLena usuario Plantilla            
            
            return redirect('listar_colaboradores')
    else:
        ip_disponibles = lista_ips.objects.filter(codigo_estado=2)
        formulario =  colaboradorForm()
        #formulario.fields['ip_colaborador'].queryset =ip_disponibles
    
    return render(request,'colaboradores/agregar_colaborador.html',{'formulario':formulario,'ip_disponibles':ip_disponibles})

@login_required(login_url="pagina_login")
def generar_excel_nuevocolab(request,pk):
    colaborador = get_object_or_404(lista_colaboradores,pk=pk)
    plantilla_ruta = os.path.join(settings.MEDIA_ROOT,'plantillas_excel','PLANTILLA-USUARIOS-NUEVOS.xlsx')
    try:
        libro = openpyxl.load_workbook(plantilla_ruta)
        hoja = libro.active
    except FileNotFoundError:
        return HttpResponse("Error:La plantilla no fue encontrada")
    
    hoja['G5'] = str(colaborador.nombre_colaborador).upper()
    hoja['N6'] = str(colaborador.cargo_colaborador).upper()
    hoja['P9'] = str(colaborador.correo).lower()
    hoja['H10'] = str(colaborador.usuario_sistema)
    hoja['R10'] = str(colaborador.usuario_sentinel) 
    hoja['R11'] = str(colaborador.usuario_reloj_control)
    hoja['R13'] = colaborador.ip_colaborador.ip                      
    usuario_correo_str = str(colaborador.correo)
    usuario_correo_str = usuario_correo_str[0:usuario_correo_str.find('@')]
    hoja['H11'] = str(colaborador.usuario_windows).lower()
    hoja['H12'] = str(usuario_correo_str).lower()
    hoja['R12'] = str(colaborador.usuario_sbs)
    hoja['H13'] = str(colaborador.codigo_impresion_colaborador)
    hoja['G29'] = str(colaborador.nombre_colaborador).upper()
    hoja['N30'] = str(colaborador.cargo_colaborador).upper()
    #Opcional guardar el libro en memoria para mas robustes
    # buffer = BytesIO()
    # libro.save(buffer)
    # buffer.seek(0)
    #si hacemos esto no es necessario guardar el archiuvo al final
    
    # response = HttpResponse(buffer.getvalue(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=colaborador_{colaborador.nombre_colaborador}.xlsx'
    libro.save(response)
    return response


@login_required(login_url="pagina_login")            
def editar_colaborador(request,pk):
    colaborador = get_object_or_404(lista_colaboradores,pk=pk)
    ip_colaborador_antigua = colaborador.ip_colaborador.ip
    if request.method == 'POST':
        formulario = colaboradorForm(request.POST, instance=colaborador)
        if formulario.is_valid():
            ip_colaborador_nueva = formulario.cleaned_data['ip_colaborador']
            #Cambia el estado de la ip a ocupada
            estado_ip_ocupada = get_object_or_404(tipo_estado_ips,pk=1)
            ip_colaborador_nueva.codigo_estado = estado_ip_ocupada
            ip_colaborador_nueva.save()             
            #Libera la otra ip            
            formulario.save()
            if str(ip_colaborador_nueva) != ip_colaborador_antigua:
                estado_ip_libre = get_object_or_404(tipo_estado_ips,pk=2)
                ip_antigua = get_object_or_404(lista_ips,ip=ip_colaborador_antigua)
                ip_antigua.codigo_estado = estado_ip_libre
                ip_antigua.save()
            return redirect('listar_colaboradores')
    else:
        # Obtener los estados de forma segura por nombre en lugar de PK
        estado_ip_libre = get_object_or_404(tipo_estado_ips, nombre_estado='Libre')
        # IPs libres
        ips_libres = lista_ips.objects.filter(codigo_estado=estado_ip_libre)        
        # IP actual del colaborador
        ip_actual = lista_ips.objects.filter(pk=colaborador.ip_colaborador.pk)        
        # Combina los dos querysets
        ips_para_formulario = ips_libres | ip_actual
        formulario = colaboradorForm(instance=colaborador)
        formulario.fields['ip_colaborador'].queryset = ips_para_formulario     
    
    return render(request,'colaboradores/editar_colaborador.html',{'formulario':formulario})

@login_required(login_url="pagina_login")
def cesar_colaborador(request,pk):
    colaborador = get_object_or_404(lista_colaboradores,pk=pk)
    if request.method == 'POST':
        ip_colaborador = colaborador.ip_colaborador
        nombre_colaborador = colaborador.nombre_colaborador
                        
        estado_colaborador = get_object_or_404(estado_colaboradores,pk=2)
        colaborador.estado_colaboradores = estado_colaborador
        colaborador.save()
        
        estado_ocupado_ip = get_object_or_404(tipo_estado_ips,pk=2)
        ip_colaborador.codigo_estado = estado_ocupado_ip
        ip_colaborador.save()
        
        try:      
            cuenta_forticlient = get_object_or_404(cuentas_forticlient,usuario_asignado=nombre_colaborador)
            cuenta_forticlient.usuario_asignado = None
            cuenta_forticlient.save()
        except Exception as e:
            print(e)
        
        return redirect('listar_colaboradores')
    
    return render(request,'colaboradores/confirmar_cesar.html',{'colaborador':colaborador})

@login_required(login_url="pagina_login")
def generar_excel_colab(request):
    fecha_hora = datetime.now()
    colaboradores = lista_colaboradores.objects.all()
    data_df = colaboradores.values('nombre_colaborador','ip_colaborador','usuario_sistema','correo','usuario_sentinel','usuario_windows','usuario_reloj_control','codigo_impresion_colaborador','cargo_colaborador','estado_colaboradores')
    df = pd.DataFrame(list(data_df))
    df['estado_colaboradores'] = df['estado_colaboradores'].replace({1:'ACTIVO',2:'CESADO'})
    df = df.rename(columns={        
        'nombre_colaborador': 'Nombre Completo',
        'ip_colaborador': 'IP Asignada',
        'usuario_sistema': 'Codigo Sistema',
        'correo': 'Correo Interno',
        'usuario_sentinel': 'Usuario Sentinel',
        'usuario_windows': 'Usuario Windows',
        'usuario_reloj_control' : 'Usuario Reloj Control',
        'codigo_impresion_colaborador': 'Codigo Impresion',
        'cargo_colaborador':'Cargo',
        'estado_colaboradores' :'Estado'        
    })
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="Colaboradores {fecha_hora}.xlsx"'
    df.to_excel(response,index=False,sheet_name='IPs')
    return response