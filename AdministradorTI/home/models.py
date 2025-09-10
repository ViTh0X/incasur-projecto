from django.db import models
from colaboradores.models import lista_colaboradores

from django import forms

# Create your models here.

class cuentas_forticlient(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=20,unique=True)
    contraseña = models.CharField(max_length=15,unique=True)
    usuario_asignado = models.ForeignKey(lista_colaboradores,null=True,blank=True,on_delete=models.CASCADE,to_field='nombre_colaborador')
    fecha_modificacion = models.DateField(auto_now=True)    
    class Meta:
        db_table = 'cuentas_forticlient'
        ordering = ['id']
        
        
    def __str__(self):
        return self.usuario
    
    
class forms_cuentas_forticlient(forms.ModelForm):
    class Meta:
        model = cuentas_forticlient
        fields = ['usuario_asignado']
# Create your models here.

class logs_actividades_celery(models.Model):
    id = models.AutoField(primary_key=True)
    tiempo_creacion = models.DateTimeField(auto_now=True)
    mensaje = models.CharField(max_length=250)
    
    class Meta:
        db_table = 'logs_invetario_hardware'
        ordering = ['id']
    
    def __str__(self):
        return self.mensaje