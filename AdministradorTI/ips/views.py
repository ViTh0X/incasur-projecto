from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.conf import settings
# Create your views here.

import pandas as pd
import os
from datetime import datetime

from .models import lista_ips, oficinas, tipo_equipos_informaticos, niveles_firewall, tipo_secciones, tipo_estado_ips, ipForm
from colaboradores.models import lista_colaboradores


def listar_ips(request):
    query_sql = """
    select *,(select nombre_colaborador from lista_colaboradores as c where c.ip_colaborador_id = i.ip and c.estado_colaboradores_id = 1) as nombre_colaborador from lista_ips as i order by id asc
    """
    ips = lista_ips.objects.raw(query_sql)
    resultado = {
        'ips':ips
    }
    return render (request,'ips/lista_ips.html',resultado)
    
    
def editar_ip(request,pk):
    ip = get_object_or_404(lista_ips,pk=pk)         
    if request.method == 'POST':
        formulario = ipForm(request.POST, instance=ip)
        if formulario.is_valid():
            formulario.save()
            return redirect('listar_ips')            
    else:        
        formulario = ipForm(instance=ip)        
        data_usuario = lista_colaboradores.objects.filter(ip_colaborador=ip).first()
        print(data_usuario)                                
    return render(request,'ips/editar_ip.html',{'formulario':formulario,'ip':ip,'data_usuario':data_usuario})

def reiniciar_data_ip(request,pk):
    ip = get_object_or_404(lista_ips,pk=pk)
    if request.method == 'POST':
        ip.ip_seccion = None
        ip.ip_nivel_firewall = None
        ip.tipo_equipo = None
        ip.marca_equipo = None
        ip.modelo_equipo = None
        ip.oficina = None
        ip.save()
        return redirect('listar_ips')
    
    return render(request,'ips/confirmar_reinciar.html',{'ip':ip})

def generar_excel(request):
    fecha_hora = datetime.now()
    query_sql = """
    select *,(select nombre_colaborador from lista_colaboradores as c where c.ip_colaborador_id = i.ip and c.estado_colaboradores_id = 1) as nombre_colaborador from lista_ips as i order by id asc
    """
    ips = lista_ips.objects.raw(query_sql)
    data_list = []
    for item in ips:
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
    df['codigo_estado_id'] = df['codigo_estado_id'].replace({1:'Ocupada',2:'Libre',3:'Sin Nivel'})
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
    })
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="Lista de IPs {fecha_hora}.xlsx"'
    df.to_excel(response,index=False,sheet_name='IPs')
    return response