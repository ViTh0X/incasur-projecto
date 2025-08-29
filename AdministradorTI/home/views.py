from django.shortcuts import render
from django.http import HttpResponse, FileResponse, Http404
from django.conf import settings
import os
# Create your views here.

def home(request):
    return render(request,'home/home.html')


def instalar_forticlient(request):
    return render(request,'home/usuarios_forticlient.html')

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