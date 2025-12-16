from django.db import models
from ips.models import lista_ips
from colaboradores.models import lista_colaboradores

# Create your models here.
class tipo_software(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_tipo = models.CharField(max_length=20)
    descripcion_tipo = models.CharField(max_length=120)
    
    class Meta:
        db_table = 'tipo_software'
        
    def __str__(self):
        return self.nombre_tipo



class faltantes_inventario_software(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.ForeignKey(lista_ips,on_delete=models.CASCADE)
    nombre_colaborador = models.ForeignKey(lista_colaboradores,on_delete=models.CASCADE,to_field='nombre_colaborador')
    fecha_modificacion = models.DateField(auto_now=True)
    
    class Meta:
        db_table = 'faltantes_inventario_software'
        ordering = ['id']
        
    def __str__(self):
        return self.ip
    
class inventario_software(models.Model):
    id_inventario_s = models.AutoField(primary_key=True)
    ip = models.ForeignKey(lista_ips,on_delete=models.CASCADE,to_field='ip')
    tipo_software = models.ForeignKey(tipo_software,on_delete=models.CASCADE)
    nombre_software = models.CharField(max_length=120)
    fecha_modificacion = models.DateField(auto_now=True)
    
    class Meta:
        db_table = 'inventario_software'
        ordering = ['id_inventario_s']
        
    def __str__(self):
        return self.nombre_software
    