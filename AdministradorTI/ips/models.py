from django.db import models

# Create your models here.

class tipo_estado_ips(models.Model):
    codigo_estado = models.AutoField(primary_key=True)
    nombre_estado = models.CharField(max_length=40)
    descripcion_estado = models.CharField(max_length=60)
    
    class Meta:
        db_table = 'tipo_estado_ips'
        
    def __str__(self):
        return self.codigo_estado


class lista_ips(models.Model):  
    id = models.CharField(primary_key=True)  
    ip = models.CharField(max_length=15,unique=True)    
    codigo_estado = models.ForeignKey(tipo_estado_ips,on_delete=models.CASCADE)
    fecha_modificacion = models.DateField(auto_now=True)
    
    class Meta:
        db_table = 'lista_ips'
        # Ordena los resultados por el campo 'ip' de forma ascendente
        ordering = ['id']
        
    def __str__(self):
        return self.ip
    