from django.db import models

# Create your models here.
from ips.models import ips
from colaboradores.models import colaboradores

class faltantes_backup_informacion(models.Model):
    id = models.AutoField(primary_key=True)
    codigo_ip = models.ForeignKey(ips,on_delete=models.CASCADE)
    codigo_colaborador = models.ForeignKey(colaboradores,on_delete=models.CASCADE)
    fecha_modificacion = models.DateField(auto_now=True)
    
    class Meta:
        db_table = 'faltantes_backup_informacion'
        ordering = ['id']
        
    def __str__(self):
        return self.ip


class backups_informacion(models.Model):
    id = models.AutoField(primary_key=True)
    codigo_ip = models.ForeignKey(ips,on_delete=models.CASCADE)
    codigo_colaborador = models.ForeignKey(colaboradores,on_delete=models.CASCADE)
    detalle = models.CharField(max_length=50)
    fecha_modificacion = models.DateField(auto_now=True)
    
    class Meta:
        db_table = 'lista_backups_informacion'
        ordering = ['id']
    
    def __str__(self):
        return self.ip
    

