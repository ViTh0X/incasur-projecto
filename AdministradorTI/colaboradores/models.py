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
    nombre_colaborador = models.CharField(max_length=150,unique=True)
    ip_colaborador = models.ForeignKey(lista_ips,on_delete=models.CASCADE, to_field='ip')
    usuario_sistema = models.CharField(max_length=25,unique=True,default='SIN ACCESO AL SISTEMA')
    correo = models.CharField(max_length=50,unique=True)
    usuario_sentinel = models.CharField(max_length=15, unique=True,default="SIN SENTINEL")
    usuario_sbs = models.CharField(max_length=15,unique=True,default="SIN SBS")
    usuario_windows = models.CharField(max_length=15,unique=True,default="SIN WINDOWS")
    usuario_reloj_control = models.CharField(max_length=15,unique=True,default="SIN MARCACION")
    codigo_impresion_colaborador = models.CharField(max_length=20,unique=True)    
    cargo_colaborador = models.CharField(max_length=70)    
    estado_colaboradores = models.ForeignKey(estado_colaboradores,on_delete=models.CASCADE)    
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'lista_colaboradores'
    
    def __str__(self):
        return self.nombre_colaborador        


    
class colaboradorForm(forms.ModelForm):
    class Meta:
        model = lista_colaboradores
        fields = ['nombre_colaborador','ip_colaborador','usuario_sistema','correo','usuario_sentinel','usuario_sbs','usuario_windows','usuario_reloj_control','codigo_impresion_colaborador','cargo_colaborador']