from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, FileResponse, Http404
from django.conf import settings
import os

from .models import cuentas_forticlient, forms_cuentas_forticlient
# Create your views here.

def home(request):
    return render(request,'home/home.html')


def instalar_forticlient(request):
    return render(request,'home/configuracion_forticlient.html')

def listar_usuarios_forticlient(request):
    usuarios_forticlient = cuentas_forticlient.objects.all()
    return render(request,'home/listar_usuarios_forticlient.html',{'usuarios_forticlient':usuarios_forticlient})

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
    
def editar_usuario_forti(request,pk):
    usuario_forticlient = get_object_or_404(cuentas_forticlient,pk=pk)
    if request.method == 'POST':
        form = forms_cuentas_forticlient(request.POST, instance=usuario_forticlient)#rquest.Post contiene mi data del formulario y instance= contiene el objeto colaborador
        if form.is_valid():
            form.save()
            return redirect('lista_colaboradores')
    else:
        form = forms_cuentas_forticlient(instance=usuario_forticlient)
        
    return render(request,'home/asignar_usuario.html',{'form':form})
    return Http404