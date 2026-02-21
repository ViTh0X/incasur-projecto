from django.db import models
from ips.models import ips
from colaboradores.models import colaboradores
# Create your models here.


class EstadoAccionesWindows(models.Model):
    id_estado = models.AutoField(primary_key=True)
    id_ip = models.ForeignKey(ips,on_delete=models.CASCADE)
    estado_puertos_usb = models.CharField(max_length=40,blank=True,null=True)
    estato_actualizacion = models.CharField(max_length=40,blank=True,null=True)
    
    class Meta():
        db_table = 'estado_acciones_windows'
    
    def __str__(self):
        return self.id_ip.ip
    
class FaltantesRevisionEquiposWindows(models.Model):
    id = models.AutoField(primary_key=True)
    codigo_ip = models.ForeignKey(ips,on_delete=models.CASCADE)
    codigo_colaborador = models.ForeignKey(colaboradores,on_delete=models.CASCADE)
    fecha_modificacion = models.DateField(auto_now=True)
    
    class Meta():
        db_table = 'faltantes_revision_equipos_windows'
    
    def __str__(self):
        return self.codigo_ip.ip