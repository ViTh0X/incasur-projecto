from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, FileResponse, Http404
from django.conf import settings

import os
import datetime

from colaboradores.models import colaboradores, estado_colaboradores
from .models import cuentas_forticlient, forms_cuentas_forticlient
# Create your views here.

from .forms import Formulario_Login
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required(login_url="pagina_login")
def home(request):
    return render(request,'home/home.html')


@login_required(login_url="pagina_login")
def instalar_forticlient(request):
    return render(request,'home/configuracion_forticlient.html')

@login_required(login_url="pagina_login")
def listar_usuarios_forticlient(request):
    usuarios_forticlient = cuentas_forticlient.objects.all()
    return render(request,'home/listar_usuarios_forticlient.html',{'usuarios_forticlient':usuarios_forticlient})


@login_required(login_url="pagina_login")
def descargar_archivo_guias_pdf(request,filename):
    ruta_archivo = os.path.join(settings.MEDIA_ROOT,'guias_pdf',filename)
    
    if os.path.exists(ruta_archivo):
        with open(ruta_archivo,'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'inline' #No descarga el archivo lo abre en otra ventana
            #response['Content-Disposition'] = f'attachment;'#ESTE ES PARA DESCARGAR EL ARCHIVO
            ####response['Content-Disposition'] = f'attachment;'# filename="{os.path.basename(ruta_archivo)}"'
            return response
    else:
        raise Http404

@login_required(login_url="pagina_login")    
def descargar_archivo_instaladores(request,filename):
    ruta_archivo = os.path.join(settings.MEDIA_ROOT,'instaladores',filename)
    
    if os.path.exists(ruta_archivo):
        with open(ruta_archivo,'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")            
            response['Content-Disposition'] = f'attachment;'#ESTE ES PARA DESCARGAR EL ARCHIVO
            ####response['Content-Disposition'] = f'attachment;'# filename="{os.path.basename(ruta_archivo)}"'
            return response
    else:
        raise Http404


@login_required(login_url="pagina_login")    
def editar_usuario_forti(request,pk):
    usuario_forticlient = get_object_or_404(cuentas_forticlient,pk=pk)
    tiempo_actual = datetime.date.today()
    if request.method == 'POST':
        form = forms_cuentas_forticlient(request.POST, instance=usuario_forticlient)
        if form.is_valid():
            form.save()
            return redirect('listar_usuarios_forticlient')
    else:
        estado_colabor_activo = get_object_or_404(estado_colaboradores,codigo_estado=1)
        usuarios_activos = colaboradores.objects.filter(estado_colaboradores=estado_colabor_activo)
        form = forms_cuentas_forticlient(instance=usuario_forticlient)
        form.fields['usuario_asignado'].queryset = usuarios_activos
    
    info = {'form':form,'usuario_forticlient':usuario_forticlient,'tiempo_actual':tiempo_actual}
        
    return render(request,'home/asignar_usuario.html',info)    

def pagina_login(request):
    if request.user.is_authenticated:
        next_url = request.GET.get('next')
        if next_url:
            return redirect(next_url)
        return redirect('home')
    else:
        if request.method == 'POST':
            form = Formulario_Login(request.POST or None)
            if form.is_valid():
                data = form.cleaned_data
                username = data['usuario']
                password = data['password']
                user = authenticate(request,username=username,password=password)
                if user is not None:
                    login(request,user)
                    next_url = request.POST.get('next') or request.GET.get('next')
                    if next_url:
                        return redirect(next_url)
                    else:
                        return redirect('home')
                else:
                    messages.warning(request,"No te identificaste correctamente")
        else:
            form = Formulario_Login()
        return render(request,'login.html',{'form':form})


@login_required(login_url="pagina_login")        
def pagina_logout(request):
    logout(request) 
    return redirect('pagina_login')