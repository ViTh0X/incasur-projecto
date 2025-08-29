from django.db import models
from django import forms

from ips.models import lista_ips

# Create your models here.

class estado_colaboradores(models.Model):
    codigo_estado = models.AutoField(primary_key=True)
    nombre_estado = models.CharField(max_length=20)    
    
    class Meta:
        db_table = 'estado_colaboradores'
    
    def __str__(self):
        return self.nombre_estado


class lista_colaboradores(models.Model):
    codigo_colaborador = models.AutoField(primary_key=True)
    ip_colaborador = models.ForeignKey(lista_ips,on_delete=models.CASCADE, to_field='ip')
    nombre_colaborador = models.CharField(max_length=150,unique=True)
    puesto_colaborador = models.CharField(max_length=70)
    codigo_impresion_colaborador = models.CharField(max_length=10)    
    estado_colaboradores = models.ForeignKey(estado_colaboradores,on_delete=models.CASCADE)    
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'lista_colaboradores'
    
    def __str__(self):
        return self.nombre_colaborador        


    
class colaboradorForm(forms.ModelForm):
    class Meta:
        model = lista_colaboradores
        fields = ['ip_colaborador','nombre_colaborador','puesto_colaborador','codigo_impresion_colaborador']