from django.db import models
from ips.models import lista_ips

# Create your models here.

class iventario_hardware(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.ForeignKey(lista_ips,on_delete=models.CASCADE)
    nombre_equipo = models.CharField(max_length=50)
    placa = models.CharField(max_length=60)
    procesador = models.CharField(max_length=100)
    ram = models.CharField(max_length=6)
    video_integrada = models.CharField(max_length=100)
    video_dedicada = models.CharField(max_length=100)
    so = models.CharField(max_length=20)
    almacenamiento = models.CharField(max_length=200,null=True,blank=True)
    puertas_enlace = models.CharField(max_length=150)
    fecha = models.DateField(auto_now=True)
    
    