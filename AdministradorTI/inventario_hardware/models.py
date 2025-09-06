from django.db import models
from ips.models import lista_ips
from colaboradores.models import lista_colaboradores
# Create your models here.

class iventario_hardware(models.Model):
    id_inventario_h = models.AutoField(primary_key=True)
    ip = models.ForeignKey(lista_ips,on_delete=models.CASCADE)
    nombre_colaborador = models.ForeignKey(lista_colaboradores,on_delete=models.CASCADE,to_field='nombre_colaborador')
    nombre_equipo = models.CharField(max_length=50)
    placa = models.CharField(max_length=60)
    procesador = models.CharField(max_length=100)
    ram = models.CharField(max_length=6)
    video_integrada = models.CharField(max_length=100)
    video_dedicada = models.CharField(max_length=100)
    so = models.CharField(max_length=20)
    almacenamiento = models.CharField(max_length=200,null=True,blank=True)
    puertas_enlace = models.CharField(max_length=150)
    fecha_modificacion = models.DateField(auto_now=True)
    
    class Meta:
        db_table = 'iventario_hardware'
        ordering = ['id_inventario_h']
        
    def __str__(self):
        return self.id
    
class faltantes_inventario_hardware(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.ForeignKey(lista_ips,on_delete=models.CASCADE)
    fecha_modificacion = models.DateField(auto_now=True)
    
    class Meta:
        db_table = 'faltantes_inventario_hardware'
        
    def __str__(self):
        return self.ip
    
# class historial_acciones