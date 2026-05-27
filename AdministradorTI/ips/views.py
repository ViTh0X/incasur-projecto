from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.conf import settings
# Create your views here.

import pandas as pd
import os
from datetime import datetime

from .models import historial_acciones, ipForm,historial_accionForm, ips, equipos_informaticos_ti, EquiposInformaticosForm,tipo_estado_ips
from colaboradores.models import colaboradores, estado_colaboradores
from inventario_hardware.models import inventario_hardware, faltantes_inventario_hardware
from inventario_software.models import inventario_software, faltantes_inventario_software
from administracion_windows.models import EstadoAccionesWindows, FaltantesRevisionEquiposWindows 


from django.contrib.auth.decorators import login_required



@login_required(login_url="pagina_login")
def equipos_informaticos(request):
    return render(request,'ips/menu_opciones_equipos_informaticos.html')
    
    
@login_required(login_url="pagina_login")
def listar_laptops_pc(request):    
    listado_ips = ips.objects.exclude(codigo_estado__pk=5)            
    return render (request,'ips/listar_pcs_laptops.html',{'listado_ips':listado_ips})

@login_required(login_url="pagina_login")
def agregar_equipo_informatico_ti(request):
    if request.method == 'POST':
        form = EquiposInformaticosForm(request.POST)
        if form.is_valid():
            form_equipo_informatico = form.save(commit=False)
            estado_equipo_activo = tipo_estado_ips.objects.get(codigo_estado=1)
            form_equipo_informatico.codigo_estado = estado_equipo_activo
            form_equipo_informatico.save()
            return redirect('listar_equipos_informaticos_ti')
    else:
        formulario =  EquiposInformaticosForm()    
    return render(request,'ips/agregar_equipo_informatico_ti.html',{'formulario':formulario})

@login_required(login_url="pagina_login")
def agregar_laptop_pc(request):
    if request.method == 'POST':
        form = ipForm(request.POST)        
        if form.is_valid():
            colaborador =  form.cleaned_data['colaborador_asignado']
            form_pc_laptop = form.save(commit=False)
            estado_equipo_activo = tipo_estado_ips.objects.get(codigo_estado=1)
            form_pc_laptop.codigo_estado = estado_equipo_activo
            form_pc_laptop.save()
            faltantes_hardware = faltantes_inventario_hardware(codigo_ip=form_pc_laptop,codigo_colaborador=colaborador)
            faltantes_hardware.save()
            faltantes_software = faltantes_inventario_software(codigo_ip=form_pc_laptop,codigo_colaborador=colaborador)
            faltantes_software.save()
            revision_equipos_windows = EstadoAccionesWindows(id_ip=form_pc_laptop)
            revision_equipos_windows.save()
            faltantes_revision_windows = FaltantesRevisionEquiposWindows(codigo_ip=form_pc_laptop,codigo_colaborador=colaborador)
            faltantes_revision_windows.save()                                  
            
            return redirect('listar_laptops_pc')
    else:
        formulario = ipForm()
    return render(request,'ips/agregar_laptop_pc.html',{'formulario':formulario})

@login_required(login_url="pagina_login")
def editar_equipo_informatico_ti(request,pk):
    equipo_informatico = equipos_informaticos_ti.objects.get(pk=pk)
    if request.method == 'POST':
        form = EquiposInformaticosForm(request.POST, instance=equipo_informatico)
        if form.is_valid():
            form.save()
            return redirect('listar_equipos_informaticos_ti')
    else:
        formulario = EquiposInformaticosForm(instance=equipo_informatico)
    return render(request,'ips/editar_equipo_informatico_ti.html',{'formulario':formulario})
    
    
@login_required(login_url="pagina_login")    
def editar_ip(request,pk):
    ip = get_object_or_404(ips,pk=pk)         
    if request.method == 'POST':
        formulario = ipForm(request.POST, instance=ip)
        if formulario.is_valid():
            formulario.save()
            return redirect('listar_laptops_pc')            
    else:        
        trabajador_libre = get_object_or_404(estado_colaboradores,codigo_estado=1)
        formulario = ipForm(instance=ip)        
        colaboradores_activos = colaboradores.objects.filter(estado_colaboradores=trabajador_libre)        
        formulario.fields['colaborador_asignado'].queryset = colaboradores_activos         
    return render(request,'ips/editar_ip.html',{'formulario':formulario})


@login_required(login_url="pagina_login")
def reiniciar_data_ip(request,pk):
    ip = get_object_or_404(ips,pk=pk)
    if request.method == 'POST':
        ip.colaborador_asignado = None
        ip.seccion = None
        ip.nivel_firewall = None
        ip.tipo_equipo = None
        ip.marca_equipo_asignado = None
        ip.modelo_equipo_asignado = None
        ip.oficina = None        
        ip.save()
        return redirect('listar_ips')
    
    return render(request,'ips/confirmar_reinciar.html',{'ip':ip})

@login_required(login_url="pagina_login")
def generar_excel_ip(request):
    fecha_hora = datetime.now()
    listado_pcs_laptops = ips.objects.exclude(codigo_estado__pk=5)
    ano_actual = datetime.now().year    
    mes_actual = datetime.now().month
    inventarios_hardware = inventario_hardware.objects.filter(fecha_modificacion__year=ano_actual,fecha_modificacion__month=mes_actual)
    data_inventario_hardware = inventarios_hardware.values('codigo_ip__ip',                                          
                                          'placa',
                                          'procesador',
                                          'ram',
                                          'video_integrada',
                                          'video_dedicada',
                                          'so',
                                          'almacenamiento')
    df_inventario_hardware = pd.DataFrame(list(data_inventario_hardware))
    listado_equipos_ti = equipos_informaticos_ti.objects.exclude(codigo_estado__pk=5)
    pcs_laptops = listado_pcs_laptops.values('ip',
                                 'vlan__nombre',
                                 'switch__nombre',
                                 'puerto',
                                 'mac',
                                 'roll_ip',
                                 'colaborador_asignado__nombre_colaborador',                                 
                                 'nivel_firewall__nombre_nivel',
                                 'tipo_equipo_asignado__nombre_tipo_equipo',
                                 'marca_equipo_asignado',
                                 'modelo_equipo_asignado')
    df_pc_laptops = pd.DataFrame(list(pcs_laptops))
    df_final = pd.merge(df_pc_laptops,df_inventario_hardware,left_on='ip',right_on='codigo_ip__ip',how='left')
    df_final = df_final.drop(columns=['codigo_ip__ip'])
    df_final = df_final.fillna("Sin Informacion")
    equipos_ti = listado_equipos_ti.values('ip',
                                 'vlan__nombre',
                                 'switch__nombre',
                                 'puerto',
                                 'mac',
                                 'roll_ip',
                                 'colaborador_asignado__nombre_colaborador',                                 
                                 'nivel_firewall__nombre_nivel',
                                 'tipo_equipo_asignado__nombre_tipo_equipo',
                                 'marca_equipo_asignado',
                                 'modelo_equipo_asignado',
                                 'placa',
                                 'procesador',
                                 'ram',
                                 'video_integrada',
                                 'video_dedicada',
                                 'so',
                                 'almacenamiento')
    df_equipos_ti = pd.DataFrame(list(equipos_ti))
    df_final = pd.concat([df_final,df_equipos_ti],ignore_index=True)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="Lista de IPs {fecha_hora}.xlsx"'
    df_final.to_excel(response,index=False,sheet_name='IPs')
    return response   
@login_required(login_url="pagina_login")
def agregar_intervencion_ti(request,ip):
    try:
        equipo_encontrado = ips.objects.get(ip=ip)
    except:
        equipo_encontrado = equipos_informaticos_ti.objects.get(ip=ip)
    if request.method == 'POST':
        formulario = historial_accionForm(request.POST)
        if formulario.is_valid():            
            agregar_accion = formulario.save(commit=False)                                                                            
            agregar_accion.ip_historial = equipo_encontrado.ip            
            if equipo_encontrado.colaborador_asignado:                
                agregar_accion.nombre_colaborador = equipo_encontrado.colaborador_asignado.nombre_colaborador                
            else:                
                agregar_accion.nombre_colaborador = "Sin Colaborador Asignado"
            agregar_accion.save()
            return redirect('equipos_informaticos')
    else:
        formulario = historial_accionForm(
            initial={
                'ip_historial':equipo_encontrado.ip               
            }           
        )
    
    return render(request,'ips/agregar_accion.html',{'formulario':formulario})            


@login_required(login_url="pagina_login")            
def ver_historial_acciones(request,ip):        
    historiales = historial_acciones.objects.filter(ip_historial=ip)
    if not historiales: 
        return render(request,'ips/historial_vacio.html')
    else:
        return render(request,'ips/ver_historial_acciones.html',{'historiales':historiales})    
    
@login_required(login_url="pagina_login")    
def filtrar_equipos_nombres(request):
    pista_nombre = request.GET.get('nombre','').strip()
    listado_ips = ips.objects.filter(colaborador_asignado__nombre_colaborador__icontains=pista_nombre)    
    return render(request,'ips/equipos_informaticos_filtrados.html',{'listado_ips':listado_ips})

@login_required(login_url="pagina_login")    
def filtrar_equipos_ti_nombres(request):
    pista_nombre = request.GET.get('nombre','').strip()
    equipos_ti = equipos_informaticos_ti.objects.filter(roll_ip__icontains=pista_nombre)    
    return render(request,'ips/equipos_informaticos_filtrados_ti.html',{'equipos_ti':equipos_ti})

@login_required(login_url="pagina_login")
def listar_equipos_informaticos_ti(request):
    equipos_ti = equipos_informaticos_ti.objects.all()
    return render(request,'ips/listar_equipos_informaticos_ti.html',{'equipos_ti':equipos_ti})
    