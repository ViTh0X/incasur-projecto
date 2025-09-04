from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.conf import settings
# Create your views here.

import os
import datetime

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