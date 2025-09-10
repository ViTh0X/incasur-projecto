from django.db import models
from ips.models import lista_ips
from colaboradores.models import lista_colaboradores
# Create your models here.

class faltantes_inventario_hardware(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.ForeignKey(lista_ips,on_delete=models.CASCADE,to_field='ip')
    nombre_colaborador = models.ForeignKey(lista_colaboradores,on_delete=models.CASCADE,to_field='nombre_colaborador')
    fecha_modificacion = models.DateField(auto_now=True)
    
    class Meta:
        db_table = 'faltantes_inventario_hardware'
        ordering = ['id']
        
    def __str__(self):
        return self.ip

class inventario_hardware(models.Model):
    id_inventario_h = models.AutoField(primary_key=True)
    ip = models.ForeignKey(lista_ips,on_delete=models.CASCADE,to_field='ip')
    nombre_colaborador = models.ForeignKey(lista_colaboradores,on_delete=models.CASCADE,to_field='nombre_colaborador')
    nombre_equipo = models.CharField(max_length=50,blank=True,null=True)
    placa = models.CharField(max_length=60,blank=True,null=True)
    procesador = models.CharField(max_length=100,blank=True,null=True)
    ram = models.CharField(max_length=6,blank=True,null=True)
    video_integrada = models.CharField(max_length=100,blank=True,null=True)
    video_dedicada = models.CharField(max_length=100,blank=True,null=True)
    so = models.CharField(max_length=20,blank=True,null=True)
    almacenamiento = models.CharField(max_length=200,null=True,blank=True)
    puertas_enlace = models.CharField(max_length=150,blank=True,null=True)
    fecha_modificacion = models.DateField(auto_now=True)
    
    class Meta:
        db_table = 'inventario_hardware'
        ordering = ['id_inventario_h']
        
    def __str__(self):
        return self.id
    

    
        