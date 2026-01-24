from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.conf import settings
# Create your views here.

import pandas as pd
import os
from datetime import datetime

from .models import historial_acciones, ipForm,historial_accionForm, ips
from colaboradores.models import colaboradores, estado_colaboradores


from django.contrib.auth.decorators import login_required

@login_required(login_url="pagina_login")
def listar_ips(request):
    #query_sql = """
    #select *,(select nombre_colaborador from lista_colaboradores as c where c.ip_colaborador_id = i.ip and c.estado_colaboradores_id = 1) as nombre_colaborador from lista_ips as i order by id asc
    #"""
    #ips = lista_ips.objects.raw(query_sql)
    #resultado = {
    #        'ips':ips
    #}
    listado_ips = ips.objects.all()            
    return render (request,'ips/lista_ips.html',{'listado_ips':listado_ips})
    
@login_required(login_url="pagina_login")    
def editar_ip(request,pk):
    ip = get_object_or_404(ips,pk=pk)         
    if request.method == 'POST':
        formulario = ipForm(request.POST, instance=ip)
        if formulario.is_valid():
            formulario.save()
            return redirect('listar_ips')            
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
    listado_ips = ips.objects.all()
    data_df = listado_ips.values('id',
                                 'ip',
                                 'roll_ip',
                                 'colaborador_asignado__nombre_colaborador',
                                 'seccion__nombre_seccion',
                                 'nivel_firewall__nombre_nivel',
                                 'tipo_equipo_asignado__nombre_tipo_equipo',
                                 'marca_equipo_asignado',
                                 'modelo_equipo_asignado',
                                 'oficina__nombre_oficina',
                                 'codigo_estado__nombre_estado')
    df = pd.DataFrame(list(data_df))
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="Lista de IPs {fecha_hora}.xlsx"'
    df.to_excel(response,index=False,sheet_name='IPs')
    return response
    #query_sql = """
    #select *,(select nombre_colaborador from lista_colaboradores as c where c.#ip_colaborador_id = i.ip and c.estado_colaboradores_id = 1) as #nombre_colaborador from lista_ips as i order by id asc
    #"""                
    #ips = ips.objects.raw(query_sql)
    #data_list = []
    '''for item in ips:
        data_list.append({
            'ip': item.ip,
            'nombre_colaborador': item.nombre_colaborador,
            'ip_seccion_id': item.ip_seccion_id,
            'ip_nivel_firewall_id': item.ip_nivel_firewall_id,
            'tipo_equipo_id': item.tipo_equipo_id,
            'marca_equipo': item.marca_equipo,
            'modelo_equipo': item.modelo_equipo,
            'oficina_id': item.oficina_id,
            'codigo_estado_id': item.codigo_estado_id,
        })
    df = pd.DataFrame(data_list)
    df['codigo_estado_id'] = df['codigo_estado_id'].replace({1:'OCUPADA',2:'LIBRE',3:'SIN NIVEL'})
    df = df.rename(columns={
        'ip': 'IP del Equipo',
        'nombre_colaborador': 'Nombre Completo',
        'marca_equipo': 'Marca del Equipo',
        'modelo_equipo': 'Modelo de Equipo',
        'ip_nivel_firewall_id': 'Nivel Firewall',
        'oficina_id': 'Oficina',
        'tipo_equipo_id': 'Tipo de Equipo',
        'codigo_estado_id':'Estado de la IP',
        'ip_seccion_id' :'Seccion IP'        
    })'''

@login_required(login_url="pagina_login")
def agregar_accion(request):
    if request.method == 'POST':
        formulario = historial_accionForm(request.POST)
        if formulario.is_valid():            
            agregar_accion = formulario.save(commit=False)                                                                
            ip=formulario.cleaned_data['ip_historial']
            ip_colaborador = get_object_or_404(ips,id=ip)            
            agregar_accion.nombre_colaborador = ip_colaborador.colaborador_asignado.nombre_colaborador
            agregar_accion.save()
            return redirect('listar_ips')
    else:
        ip_disponibles = ips.objects.exclude(codigo_estado = 3)
        formulario =  historial_accionForm()
        formulario.fields['ip_historial'].queryset = ip_disponibles        
    
    return render(request,'ips/agregar_accion.html',{'formulario':formulario})            


@login_required(login_url="pagina_login")            
def ver_historial_acciones(request,pk):    
    ip_seleccionada = ips.objects.get(pk=pk)
    historiales = historial_acciones.objects.filter(ip_historial=ip_seleccionada)
    if not historiales: 
        return render(request,'ips/historial_vacio.html')
    else:
        return render(request,'ips/ver_historial_acciones.html',{'historiales':historiales})    