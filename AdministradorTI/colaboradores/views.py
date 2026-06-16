from django.shortcuts import render, get_list_or_404,get_object_or_404 ,redirect
from django.http import HttpResponse, Http404
from django.conf import settings
from io import BytesIO

import os
import datetime
import openpyxl
import pandas as pd

from datetime import datetime
from django.db.models import Max, IntegerField
from django.db.models.functions import Cast

from bkinformacion.models import faltantes_backup_informacion
from administracion_windows.models import FaltantesRevisionEquiposWindows, EstadoAccionesWindows
from home.models import cuentas_forticlient
from inventario_hardware.models import inventario_hardware, faltantes_inventario_hardware
from inventario_software.models import faltantes_inventario_software

from .models import colaboradores, colaboradorForm, estado_colaboradores,colaboradorForm_editar
from ips.models import tipo_estado_ips, ips, ipForm, equipos_informaticos_ti

from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url="pagina_login")
def listar_colaboradores(request):
    try:
        estado_colaborador = get_object_or_404(estado_colaboradores,pk=1)
        lista_colaboradores = colaboradores.objects.filter(estado_colaboradores=estado_colaborador).order_by("codigo_colaborador")
        #lista_colaboradores = colaboradores.objects.all()
    except:
        pass
    return render(request,'colaboradores/lista_colaboradores.html',{'lista_colaboradores':lista_colaboradores})   

@login_required(login_url="pagina_login")
def agregar_colaborador(request):
    ip_disponibles = ips.objects.filter(codigo_estado=2)
    cod_impresion_libre = colaboradores.objects.annotate(
        codigo_numero=Cast('codigo_impresion_colaborador',IntegerField())
    ).aggregate(maximo=Max('codigo_numero'))
    codigo_impresion_mostrar = cod_impresion_libre['maximo'] if cod_impresion_libre['maximo'] is not None else 0
    codigo_impresion_mostrar = codigo_impresion_mostrar + 1 
    if request.method == 'POST':
        formulario = colaboradorForm(request.POST)
        formulario_ip = ipForm(request.POST)
        ip_colaborador_str = request.POST.get('ip_colaborador')        
        if formulario.is_valid() and formulario_ip.is_valid():            
            add_colaborador = formulario.save(commit=False)
            ip = formulario_ip.save(commit=False)            
            estado_colaborador_activo = get_object_or_404(estado_colaboradores,pk=1)            
            add_colaborador.estado_colaboradores = estado_colaborador_activo
            add_colaborador.save()            
            ip_colaborador = get_object_or_404(ips,ip=ip_colaborador_str)
            estado_ip_ocupada = get_object_or_404(tipo_estado_ips,codigo_estado=1)
            ip.roll_ip = "Computador de Colaborador"
            ip.codigo_estado = estado_ip_ocupada
            ip.save()            
            faltantes_hardware = faltantes_inventario_hardware(codigo_ip=ip_colaborador,codigo_colaborador=add_colaborador)
            faltantes_hardware.save()
            faltantes_software = faltantes_inventario_software(codigo_ip=ip_colaborador,codigo_colaborador=add_colaborador)
            faltantes_software.save()
            revision_equipos_windows = EstadoAccionesWindows(id_ip=ip_colaborador)
            revision_equipos_windows.save()
            faltantes_revision_windows = FaltantesRevisionEquiposWindows(codigo_ip=ip_colaborador,codigo_colaborador=add_colaborador)
            faltantes_revision_windows.save()                                  
            
            return redirect('listar_colaboradores')
    else:        
        formulario =  colaboradorForm()
        formulario_ip = ipForm()
        #formulario.fields['ip_colaborador'].queryset = ip_disponibles
    
    return render(request,'colaboradores/agregar_colaborador.html',{'formulario':formulario,'formulario_ip':formulario_ip,'ip_disponibles':ip_disponibles,'codigo_impresion_mostrar':codigo_impresion_mostrar})

@login_required(login_url="pagina_login")
def generar_excel_nuevocolab(request,pk):
    colaborador = get_object_or_404(colaboradores,pk=pk)
    list_ip_colaborador = get_list_or_404(ips,colaborador_asignado=colaborador.codigo_colaborador)
    ip = ""
    if len(list_ip_colaborador) == 1:
        for instancia_ips in list_ip_colaborador:
            ip = instancia_ips.ip
    else:
        for instancia_ips in list_ip_colaborador:
            ip += instancia_ips.ip + "-"        
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
    hoja['O13'] = ip                      
    usuario_correo_str = str(colaborador.correo)
    usuario_correo_str = usuario_correo_str[0:usuario_correo_str.find('@')]
    hoja['H11'] = str(colaborador.usuario_windows).lower()
    hoja['H12'] = str(usuario_correo_str).lower()
    hoja['R12'] = str(colaborador.usuario_sbs)
    hoja['H13'] = str(colaborador.codigo_impresion_colaborador)
    hoja['G29'] = str(colaborador.nombre_colaborador).upper()
    hoja['N30'] = str(colaborador.cargo_colaborador.nombre_cargo).upper()
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
    colaborador = get_object_or_404(colaboradores,pk=pk)
    #ip_colaborador_antigua = colaborador.ip_colaborador.ip
    if request.method == 'POST':
        formulario = colaboradorForm_editar(request.POST, instance=colaborador)
        if formulario.is_valid():
            #ip_colaborador_nueva = formulario.cleaned_data['ip_colaborador']
            #Cambia el estado de la ip a ocupada
            #estado_ip_ocupada = get_object_or_404(tipo_estado_ips,pk=1)
            #ip_colaborador_nueva.codigo_estado = estado_ip_ocupada
            #ip_colaborador_nueva.save()             
            #Libera la otra ip            
            formulario.save()
            #if str(ip_colaborador_nueva) != ip_colaborador_antigua:
            #    estado_ip_libre = get_object_or_404(tipo_estado_ips,pk=2)
            #    ip_antigua = get_object_or_404(lista_ips,ip=ip_colaborador_antigua)
            #    ip_antigua.codigo_estado = estado_ip_libre
            #    ip_antigua.save()
            return redirect('listar_colaboradores')
    else:
        # Obtener los estados de forma segura por nombre en lugar de PK
        estado_ip_libre = get_object_or_404(tipo_estado_ips, nombre_estado='Libre')
        # IPs libres
        #ips_libres = lista_ips.objects.filter(codigo_estado=estado_ip_libre)        
        # IP actual del colaborador
        #ip_actual = lista_ips.objects.filter(pk=colaborador.ip_colaborador.pk)        
        # Combina los dos querysets
        #ips_para_formulario = ips_libres | ip_actual
        formulario = colaboradorForm_editar(instance=colaborador)
        #formulario.fields['ip_colaborador'].queryset = ips_para_formulario     
    
    return render(request,'colaboradores/editar_colaborador.html',{'formulario':formulario})

@login_required(login_url="pagina_login")
def cesar_colaborador(request,pk):
    colaborador = get_object_or_404(colaboradores,pk=pk)
    if request.method == 'POST':
                        
        nombre_colaborador = colaborador.nombre_colaborador
        estado_colaborador = get_object_or_404(estado_colaboradores,pk=2)
        colaborador.estado_colaboradores = estado_colaborador
        colaborador.save()        
                        
        equipo_libre = tipo_estado_ips.objects.get(pk=2)
        pcs_laptops = ips.objects.filter(colaborador_asignado=colaborador)        
        for pc_laptop in pcs_laptops:                        
            FaltantesRevisionEquiposWindows.objects.filter(codigo_ip=pc_laptop).delete()
            faltantes_backup_informacion.objects.filter(codigo_ip=pc_laptop).delete()                    
            faltantes_inventario_hardware.objects.filter(codigo_ip=pc_laptop).delete()
            faltantes_inventario_software.objects.filter(codigo_ip=pc_laptop).delete()        
        equipos_informaticos = equipos_informaticos_ti.objects.filter(colaborador_asignado=colaborador)         
        pcs_laptops.update(colaborador_asignado=None,codigo_estado=equipo_libre,switch=None,puerto='?')        
        equipos_informaticos.update(colaborador_asignado=None,codigo_estado=equipo_libre)
                                 
        try:      
            cuenta_forticlient = get_object_or_404(cuentas_forticlient,usuario_asignado=colaborador)
            cuenta_forticlient.usuario_asignado = None
            cuenta_forticlient.save()            
        except Exception as e:
            print(e)        
                                                
                                       
        return redirect('listar_colaboradores')
    
    return render(request,'colaboradores/confirmar_cesar.html',{'colaborador':colaborador})

@login_required(login_url="pagina_login")
def generar_excel_colab(request):
    fecha_hora = datetime.now()
    lista_colaboradores = colaboradores.objects.all()
    data_df = lista_colaboradores.values('codigo_colaborador',
                                         'nombre_colaborador',
                                         'usuario_sistema',
                                         'correo',
                                         'usuario_sentinel',
                                         'usuario_windows',
                                         'usuario_reloj_control',
                                         'codigo_impresion_colaborador',
                                         'cargo_colaborador__nombre_cargo',
                                         'estado_colaboradores__nombre_estado')
    df = pd.DataFrame(list(data_df))
    #df['estado_colaboradores'] = df['estado_colaboradores'].replace({1:'ACTIVO',2:'CESADO'})
    df = df.rename(columns={ 
        'codigo_colaborador' : 'codigo_colaborador',
        'nombre_colaborador': 'Nombre Completo',        
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


def filtrar_usuarios_nombres(request):
    pista_nombre = request.GET.get('nombre','').strip()
    lista_colaboradores = colaboradores.objects.filter(nombre_colaborador__icontains=pista_nombre)    
    return render(request,'colaboradores/colaboradores_filtrados.html',{'lista_colaboradores':lista_colaboradores})