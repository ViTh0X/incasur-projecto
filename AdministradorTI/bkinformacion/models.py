from django.db import models

# Create your models here.
from ips.models import lista_ips
from colaboradores.models import lista_colaboradores

class faltantes_backup_informacion(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.ForeignKey(lista_ips,on_delete=models.CASCADE,to_field='ip')
    nombre_colaborador = models.ForeignKey(lista_colaboradores,on_delete=models.CASCADE,to_field='nombre_colaborador')
    fecha_modificacion = models.DateField(auto_now=True)
    
    class Meta:
        db_table = 'faltantes_backup_informacion'
        ordering = ['id']
        
    def __str__(self):
        return self.ip


class lista_backups_informacion(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.ForeignKey(lista_ips,on_delete=models.CASCADE)
    nombre_colaborador = models.ForeignKey(lista_colaboradores,on_delete=models.CASCADE)
    detalle = models.CharField(max_length=50)
    fecha_modificacion = models.DateField(auto_now=True)
    
    class Meta:
        db_table = 'lista_backups_informacion'
        ordering = ['id']
    
    def __str__(self):
        return self.ip
    

