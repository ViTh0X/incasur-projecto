from django.shortcuts import render, get_list_or_404,get_object_or_404 ,redirect
from django.http import HttpResponse, Http404
from django.conf import settings

import os
import datetime

from .models import lista_colaboradores, colaboradorForm, estado_colaboradores
from ips.models import tipo_estado_ips, lista_ips
# Create your views here.
def listar_colaboradores(request):
    colaboradores = lista_colaboradores.objects.all()
    return render(request,'colaboradores/lista_colaboradores.html',{'colaboradores':colaboradores})   

def agregar_colaborador(request):
    if request.method == 'POST':
        formulario = colaboradorForm(request.POST)
        if formulario.is_valid():
            #Obtenemos un objeto ip de la lista de ips
            ip_colaborador = formulario.cleaned_data['ip_colaborador']            
            #Por medio del formulario obtenemos un objeto de lista_colaboradores
            add_colaborador = formulario.save(commit=False)
            estado_colaborador_activo = get_object_or_404(estado_colaboradores,pk=1)            
            add_colaborador.estado_colaboradores = estado_colaborador_activo
            add_colaborador.save()
            #Recordar que si es un foreign key, necesitamos pasarle una instancia de el fk estado_colaborador_activo = get_object_or_404(estado_colaboradores,pk=1)  a nuestro formulario para guardar,            
            estado_ip_ocupada = get_object_or_404(tipo_estado_ips,pk=1)
            ip_colaborador.codigo_estado = estado_ip_ocupada
            ip_colaborador.save()            
            return redirect('listar_colaboradores')
    else:
        ip_disponibles = lista_ips.objects.filter(codigo_estado=2)
        formulario =  colaboradorForm()
        formulario.fields['ip_colaborador'].queryset =ip_disponibles
    
    return render(request,'colaboradores/agregar_colaborador.html',{'formulario':formulario})
            
            